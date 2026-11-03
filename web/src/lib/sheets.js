import { google } from 'googleapis';
import fs from 'fs';
import path from 'path';
import { SA_ENC } from './sa_enc.js';

export const SPREADSHEET_ID = process.env.GOOGLE_SPREADSHEET_ID || '1l9udwmIbPyOzfQ7hXFBdWbW5r5BoPpI807OxeKfW4xc';

let _authClient = null;

export async function getAuthClient() {
  if (_authClient) return _authClient;

  let credentials = null;

  if (process.env.GOOGLE_SERVICE_ACCOUNT_JSON) {
    try {
      credentials = JSON.parse(process.env.GOOGLE_SERVICE_ACCOUNT_JSON);
    } catch (e) {
      console.error('Error parsing GOOGLE_SERVICE_ACCOUNT_JSON:', e);
    }
  }

  if (!credentials) {
    // Intentar leer credentials.json desde la raíz
    const possiblePaths = [
      path.join(process.cwd(), 'credentials.json'),
      path.join(process.cwd(), '..', 'credentials.json'),
    ];
    for (const p of possiblePaths) {
      if (fs.existsSync(p)) {
        try {
          credentials = JSON.parse(fs.readFileSync(p, 'utf8'));
          break;
        } catch (_) {}
      }
    }
  }

  // Fallback garantizado a las credenciales oficiales de la PGET
  if (!credentials && SA_ENC) {
    try {
      const decoded = Buffer.from(SA_ENC, 'base64').toString('utf8');
      credentials = JSON.parse(decoded);
    } catch (e) {
      console.error('Error decoding fallback SA_ENC:', e);
    }
  }

  if (!credentials) {
    throw new Error('No se encontraron credenciales de Google Service Account');
  }

  const auth = new google.auth.GoogleAuth({
    credentials,
    scopes: ['https://www.googleapis.com/auth/spreadsheets'],
  });

  _authClient = await auth.getClient();
  return _authClient;
}

export async function getSheetsApi() {
  const auth = await getAuthClient();
  return google.sheets({ version: 'v4', auth });
}

export async function getRowsForTab(tabTitle, headerRow = 1) {
  const sheets = await getSheetsApi();
  const startRow = headerRow + 1;
  const res = await sheets.spreadsheets.values.get({
    spreadsheetId: SPREADSHEET_ID,
    range: `'${tabTitle}'!A${startRow}:Z5000`,
    majorDimension: 'ROWS',
  });

  const rawRows = res.data.values || [];
  return rawRows.filter(r => r && r.length > 0 && r.some(c => c && String(c).trim() !== ''));
}

export async function insertRowForTab(tab, rowValues, targetYear = 2026) {
  const sheets = await getSheetsApi();
  
  // 1. Obtener todas las filas de la pestaña para ubicar el último banner y causas
  const res = await sheets.spreadsheets.values.get({
    spreadsheetId: SPREADSHEET_ID,
    range: `'${tab.title}'!A1:Z5000`,
    majorDimension: 'ROWS',
  });

  const allRows = res.data.values || [];
  const bannerPattern = /CAUSAS?\s*(?:A[ÑN]O)?\s*(\d{4})/i;

  let usesAnoInBanner = false;
  let targetYearBannerRow = null;
  let nextBannerRowAfterTarget = null;
  let lastMeaningfulRow = tab.headerRow || 1;

  for (let i = 0; i < allRows.length; i++) {
    const rowNumber = i + 1;
    const row = allRows[i] || [];
    const line = row.map(c => String(c)).join(' ').trim();
    const match = line.match(bannerPattern);

    if (match) {
      const yr = parseInt(match[1], 10);
      if (line.toUpperCase().includes('AÑO') || line.toUpperCase().includes('ANO')) {
        usesAnoInBanner = true;
      }
      if (yr === targetYear) {
        targetYearBannerRow = rowNumber;
      } else if (targetYearBannerRow !== null && nextBannerRowAfterTarget === null && rowNumber > targetYearBannerRow) {
        nextBannerRowAfterTarget = rowNumber;
      }
      lastMeaningfulRow = rowNumber;
    } else {
      const nonEmpty = row.map(c => String(c).trim()).filter(Boolean);
      if (nonEmpty.length >= 2 || (nonEmpty.length === 1 && isNaN(Number(nonEmpty[0])))) {
        lastMeaningfulRow = rowNumber;
      } else if (nonEmpty.length === 1 && (parseInt(nonEmpty[0], 10) || 999) <= 25 && rowNumber <= 25) {
        lastMeaningfulRow = rowNumber;
      }
    }
  }

  const bannerText = usesAnoInBanner ? `CAUSAS AÑO ${targetYear}` : `CAUSAS ${targetYear}`;
  const cols = tab.columns?.length || 18;

  if (targetYearBannerRow !== null) {
    // La sección del año YA existe
    const insertAt = nextBannerRowAfterTarget !== null ? nextBannerRowAfterTarget : (lastMeaningfulRow + 1);

    // Si hay un banner posterior, insertar espacio
    if (nextBannerRowAfterTarget !== null) {
      await sheets.spreadsheets.batchUpdate({
        spreadsheetId: SPREADSHEET_ID,
        requestBody: {
          requests: [
            {
              insertDimension: {
                range: {
                  sheetId: tab.gid,
                  dimension: 'ROWS',
                  startIndex: insertAt - 1,
                  endIndex: insertAt,
                },
                inheritFromBefore: false,
              },
            },
          ],
        },
      });
    }

    // Escribir la causa
    await sheets.spreadsheets.values.update({
      spreadsheetId: SPREADSHEET_ID,
      range: `'${tab.title}'!A${insertAt}`,
      valueInputOption: 'USER_ENTERED',
      requestBody: {
        values: [rowValues],
      },
    });

    // Formatear fila centrada
    await formatCauseRow(sheets, tab.gid, insertAt, cols);
    return { ok: true, row: insertAt };
  } else {
    // La sección NO existe aún (ej. CAUSAS 2026)
    const bannerIndex = lastMeaningfulRow + 1;
    const causeIndex = bannerIndex + 1;

    // 1. Escribir Banner
    await sheets.spreadsheets.values.update({
      spreadsheetId: SPREADSHEET_ID,
      range: `'${tab.title}'!A${bannerIndex}`,
      valueInputOption: 'USER_ENTERED',
      requestBody: {
        values: [[bannerText]],
      },
    });

    // 2. Formatear Banner celeste fusionado
    await formatBanner(sheets, tab.gid, bannerIndex, cols);

    // 3. Escribir Causa inmediatamente debajo
    await sheets.spreadsheets.values.update({
      spreadsheetId: SPREADSHEET_ID,
      range: `'${tab.title}'!A${causeIndex}`,
      valueInputOption: 'USER_ENTERED',
      requestBody: {
        values: [rowValues],
      },
    });

    // 4. Formatear Causa centrada
    await formatCauseRow(sheets, tab.gid, causeIndex, cols);
    return { ok: true, bannerRow: bannerIndex, causeRow: causeIndex };
  }
}

export async function deleteRowForTab(tab, { rowIndex, expediente }) {
  const sheets = await getSheetsClient();
  let targetRow = rowIndex;

  if (expediente) {
    const allRows = await getRowsForTab(tab.title, 1);
    const expQuery = String(expediente).trim().toUpperCase();
    for (let i = 0; i < allRows.length; i++) {
      const line = (allRows[i] || []).join(' ').toUpperCase();
      if (line.includes(expQuery)) {
        targetRow = i + 1; // 1-based index
        break;
      }
    }
  }

  if (targetRow && targetRow > tab.headerRow) {
    await sheets.spreadsheets.batchUpdate({
      spreadsheetId: SPREADSHEET_ID,
      requestBody: {
        requests: [
          {
            deleteDimension: {
              range: {
                sheetId: tab.gid,
                dimension: 'ROWS',
                startIndex: targetRow - 1,
                endIndex: targetRow,
              },
            },
          },
        ],
      },
    });
    return { ok: true, deletedRow: targetRow };
  }
  return { ok: false, error: 'Fila no encontrada en Google Sheets' };
}

async function formatBanner(sheets, sheetId, rowNumber, columnCount) {
  try {
    const cols = columnCount > 0 ? columnCount : 20;
    await sheets.spreadsheets.batchUpdate({
      spreadsheetId: SPREADSHEET_ID,
      requestBody: {
        requests: [
          {
            mergeCells: {
              range: {
                sheetId,
                startRowIndex: rowNumber - 1,
                endRowIndex: rowNumber,
                startColumnIndex: 0,
                endColumnIndex: cols,
              },
              mergeType: 'MERGE_ALL',
            },
          },
          {
            repeatCell: {
              range: {
                sheetId,
                startRowIndex: rowNumber - 1,
                endRowIndex: rowNumber,
                startColumnIndex: 0,
                endColumnIndex: cols,
              },
              cell: {
                userEnteredFormat: {
                  backgroundColor: { red: 0.5725, green: 0.8039, blue: 0.8627 },
                  textFormat: { fontFamily: 'Arial', fontSize: 36, bold: true },
                  verticalAlignment: 'MIDDLE',
                  horizontalAlignment: 'LEFT',
                  borders: {
                    top: { style: 'SOLID' },
                    bottom: { style: 'SOLID' },
                    left: { style: 'SOLID' },
                    right: { style: 'SOLID' },
                  },
                },
              },
              fields: 'userEnteredFormat(backgroundColor,textFormat,verticalAlignment,horizontalAlignment,borders)',
            },
          },
          {
            updateDimensionProperties: {
              range: {
                sheetId,
                dimension: 'ROWS',
                startIndex: rowNumber - 1,
                endIndex: rowNumber,
              },
              properties: { pixelSize: 60 },
              fields: 'pixelSize',
            },
          },
        ],
      },
    });
  } catch (e) {
    console.error('Error formatting banner:', e);
  }
}

async function formatCauseRow(sheets, sheetId, rowNumber, columnCount) {
  try {
    const cols = columnCount > 0 ? columnCount : 20;
    await sheets.spreadsheets.batchUpdate({
      spreadsheetId: SPREADSHEET_ID,
      requestBody: {
        requests: [
          {
            repeatCell: {
              range: {
                sheetId,
                startRowIndex: rowNumber - 1,
                endRowIndex: rowNumber,
                startColumnIndex: 0,
                endColumnIndex: cols,
              },
              cell: {
                userEnteredFormat: {
                  verticalAlignment: 'MIDDLE',
                  horizontalAlignment: 'CENTER',
                  wrapStrategy: 'WRAP',
                  textFormat: { fontFamily: 'Arial', fontSize: 10 },
                  borders: {
                    top: { style: 'SOLID' },
                    bottom: { style: 'SOLID' },
                    left: { style: 'SOLID' },
                    right: { style: 'SOLID' },
                  },
                },
              },
              fields: 'userEnteredFormat(verticalAlignment,horizontalAlignment,wrapStrategy,textFormat,borders)',
            },
          },
          {
            updateDimensionProperties: {
              range: {
                sheetId,
                dimension: 'ROWS',
                startIndex: rowNumber - 1,
                endIndex: rowNumber,
              },
              properties: { pixelSize: 40 },
              fields: 'pixelSize',
            },
          },
        ],
      },
    });
  } catch (e) {
    console.error('Error formatting cause row:', e);
  }
}
