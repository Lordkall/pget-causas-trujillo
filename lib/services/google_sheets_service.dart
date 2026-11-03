import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:flutter/services.dart';
import 'package:googleapis_auth/auth_io.dart';
import 'package:gsheets/gsheets.dart';
import 'package:http/http.dart' as http;
import '../models/pget_tab.dart';
import 'pget_credentials.dart';

/// Cliente HTTP interceptor que sanitiza las respuestas de metadatos de Google Sheets.
/// Evita que el paquete `gsheets` se caiga con `NoSuchMethodError: []("rowCount")`
/// cuando el libro contiene hojas de tipo gráfico u objeto ('OBJECT') como 'Gráfico1'
/// que carecen de la propiedad 'gridProperties'.
class _GsheetsSanitizingClient extends http.BaseClient {
  final http.Client _inner;
  final String targetSpreadsheetId;

  _GsheetsSanitizingClient(this._inner, this.targetSpreadsheetId);

  @override
  Future<http.StreamedResponse> send(http.BaseRequest request) async {
    final response = await _inner.send(request);
    final path = request.url.path;

    // Interceptar únicamente la solicitud de metadatos del documento (evitando lecturas/escrituras de celdas /values/)
    if (request.method.toUpperCase() == 'GET' &&
        path.contains(targetSpreadsheetId) &&
        !path.contains('/values/')) {
      final bytes = await response.stream.toBytes();
      try {
        final decoded = json.decode(utf8.decode(bytes));
        if (decoded is Map<String, dynamic> && decoded.containsKey('sheets')) {
          final sheets = decoded['sheets'] as List<dynamic>;
          for (final s in sheets) {
            if (s is Map<String, dynamic>) {
              final props = s['properties'];
              if (props is Map<String, dynamic>) {
                if (props['gridProperties'] == null) {
                  // Inyectar dimensiones mínimas para pestañas tipo OBJECT / gráficos
                  // para evitar NoSuchMethodError en el deserializador de gsheets
                  props['gridProperties'] = {
                    'rowCount': 100,
                    'columnCount': 26,
                  };
                }
              }
            }
          }
          final sanitizedBytes = utf8.encode(json.encode(decoded));
          final sanitizedHeaders = Map<String, String>.from(response.headers);
          sanitizedHeaders['content-length'] = sanitizedBytes.length.toString();

          return http.StreamedResponse(
            Stream.value(sanitizedBytes),
            response.statusCode,
            contentLength: sanitizedBytes.length,
            request: response.request,
            headers: sanitizedHeaders,
            isRedirect: response.isRedirect,
            persistentConnection: response.persistentConnection,
            reasonPhrase: response.reasonPhrase,
          );
        }
      } catch (e) {
        debugPrint("Notice: sanitización de metadatos de hojas omitida: $e");
      }

      return http.StreamedResponse(
        Stream.value(bytes),
        response.statusCode,
        contentLength: bytes.length,
        request: response.request,
        headers: response.headers,
        isRedirect: response.isRedirect,
        persistentConnection: response.persistentConnection,
        reasonPhrase: response.reasonPhrase,
      );
    }

    return response;
  }

  @override
  void close() {
    _inner.close();
    super.close();
  }
}

class GoogleSheetsService {
  static const String spreadsheetId = '1l9udwmIbPyOzfQ7hXFBdWbW5r5BoPpI807OxeKfW4xc';

  GSheets? _gsheets;
  Spreadsheet? _spreadsheet;
  AutoRefreshingAuthClient? _authClient;
  bool _isInitialized = false;
  Map<String, dynamic>? _cachedRowsMap;
  String? _lastError;

  bool get isInitialized => _isInitialized;
  String? get lastError => _lastError;

  /// Inicializa la conexión con Google Sheets usando las credenciales oficiales de la PGET
  Future<bool> init() async {
    if (_isInitialized && _spreadsheet != null) return true;

    try {
      dynamic creds;
      try {
        creds = pgetOfficialCredentialsMap;
      } catch (_) {
        final encData = await rootBundle.loadString('assets/pget_sa.enc');
        final cleanBase64 = encData.replaceAll('\r', '').replaceAll('\n', '').trim();
        final decodedBytes = base64.decode(cleanBase64);
        creds = json.decode(utf8.decode(decodedBytes));
      }

      final accountCreds = ServiceAccountCredentials.fromJson(creds);
      final scopes = const [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive',
      ];
      final sanitizingClient = _GsheetsSanitizingClient(http.Client(), spreadsheetId);
      final authClient = await clientViaServiceAccount(
        accountCreds,
        scopes,
        baseClient: sanitizingClient,
      );

      _authClient = authClient;
      _gsheets = GSheets.withClient(authClient);
      _spreadsheet = await _gsheets!.spreadsheet(spreadsheetId);

      if (_spreadsheet == null) {
        _lastError = "Google Sheets devolvió null para el ID del documento.";
        _isInitialized = false;
        return false;
      }

      _isInitialized = true;
      _lastError = null;
      return true;
    } catch (e, stack) {
      _isInitialized = false;
      _lastError = e.toString();
      debugPrint("Error initializing GSheets live connection: $e\n$stack");
      return false;
    }
  }

  static String _stripAccents(String text) {
    return text
        .toUpperCase()
        .replaceAll('Á', 'A')
        .replaceAll('É', 'E')
        .replaceAll('Í', 'I')
        .replaceAll('Ó', 'O')
        .replaceAll('Ú', 'U')
        .replaceAll('Ñ', 'N')
        .replaceAll(RegExp(r'[^A-Z0-9]'), '');
  }

  /// Cargar datos cacheados de respaldo desde assets/pget_all_rows.json
  Future<List<List<dynamic>>> _loadFallbackRows(String tabTitle) async {
    try {
      if (_cachedRowsMap == null) {
        String jsonString;
        try {
          jsonString = await rootBundle.loadString('assets/pget_all_rows.json');
        } catch (_) {
          jsonString = await rootBundle.loadString('assets/compact_causes_by_tab.json');
        }
        _cachedRowsMap = json.decode(jsonString) as Map<String, dynamic>;
      }

      if (_cachedRowsMap != null) {
        final normTarget = tabTitle.trim().toUpperCase();
        final strippedTarget = _stripAccents(tabTitle);

        // 1. Si el JSON es de formato directo: { "TAB_TITLE": [ [row1], [row2] ] }
        for (final entry in _cachedRowsMap!.entries) {
          final keyUpper = entry.key.trim().toUpperCase();
          final keyStripped = _stripAccents(entry.key);
          if (keyUpper == normTarget ||
              keyStripped == strippedTarget ||
              keyUpper.contains(normTarget) ||
              normTarget.contains(keyUpper) ||
              keyStripped.contains(strippedTarget) ||
              strippedTarget.contains(keyStripped)) {
            if (entry.value is List) {
              final list = entry.value as List<dynamic>;
              if (list.isNotEmpty && list.first is List) {
                return list.map((r) => (r as List<dynamic>)).toList();
              }
            }
          }
        }

        // 2. Si el JSON contiene "causes_by_tab"
        if (_cachedRowsMap!.containsKey('causes_by_tab')) {
          final causesByTab = _cachedRowsMap!['causes_by_tab'] as Map<String, dynamic>;
          for (final entry in causesByTab.entries) {
            final keyUpper = entry.key.trim().toUpperCase();
            final keyStripped = _stripAccents(entry.key);
            if (keyUpper == normTarget ||
                keyStripped == strippedTarget ||
                keyUpper.contains(normTarget) ||
                normTarget.contains(keyUpper) ||
                keyStripped.contains(strippedTarget) ||
                strippedTarget.contains(keyStripped)) {
              final list = entry.value as List<dynamic>;
              return list.map((item) {
                if (item is List) return item;
                if (item is Map) {
                  return [
                    item['row_index'] ?? '',
                    item['expediente'] ?? '',
                    item['motivo'] ?? '',
                    item['demandado'] ?? '',
                    item['abogado'] ?? '',
                    item['estado'] ?? 'ACTIVA',
                    item['fecha'] ?? '',
                    item['actuaciones'] ?? '',
                  ];
                }
                return [item.toString()];
              }).toList();
            }
          }
        }
      }
    } catch (e) {
      debugPrint("Error loading fallback rows for $tabTitle: $e");
    }
    return [];
  }

  /// Obtiene una pestaña específica por su GID o Título
  Future<Worksheet?> getWorksheet(PgetTab tab) async {
    final ok = await init();
    if (!ok || _spreadsheet == null) {
      _lastError ??= "No se pudo establecer la conexión remota con Google Sheets";
      return null;
    }

    try {
      // 1. Búsqueda por ID numérico (GID)
      final wsById = _spreadsheet!.worksheetById(tab.gid);
      if (wsById != null) return wsById;

      // 2. Búsqueda por título exacto
      final wsByTitle = _spreadsheet!.worksheetByTitle(tab.title);
      if (wsByTitle != null) return wsByTitle;

      // 3. Búsqueda por título normalizado / similitud
      final sheets = _spreadsheet!.sheets;
      final normTarget = _stripAccents(tab.title);
      return sheets.firstWhere(
        (s) => _stripAccents(s.title) == normTarget || s.id == tab.gid,
        orElse: () => sheets.firstWhere((s) => s.id != 2106549316, orElse: () => sheets.first),
      );
    } catch (e) {
      _lastError = "Error al localizar la pestaña ${tab.title}: $e";
      debugPrint("Error finding worksheet ${tab.title}: $e");
      return null;
    }
  }

  /// Carga las filas de datos de una pestaña respetando su fila de encabezados
  Future<List<List<dynamic>>> getRowsForTab(PgetTab tab) async {
    try {
      final ws = await getWorksheet(tab);
      if (ws != null) {
        // Las filas de datos inician después de la fila de encabezados (headerRow + 1)
        final startRow = tab.headerRow + 1;
        final rows = await ws.values.allRows(fromRow: startRow);
        final validRows = rows
            .where((r) => r.isNotEmpty && r.any((val) => val.toString().trim().isNotEmpty))
            .map<List<dynamic>>((r) => List<dynamic>.from(r))
            .toList();
        if (validRows.isNotEmpty) {
          return List<List<dynamic>>.from(validRows);
        }
      }
    } catch (e) {
      debugPrint("Live fetch failed for ${tab.title}, loading bundled rows: $e");
    }

    // Fallback garantizado a los datos cacheados
    return await _loadFallbackRows(tab.title);
  }

  /// Extrae el año asociado a una fila de causa a partir de fechas o número de expediente
  static int? _extractYearFromRow(List<dynamic> row) {
    if (row.isEmpty) return null;
    for (final cell in row) {
      final str = cell.toString();
      final dateMatch = RegExp(r'\b\d{1,2}[/-]\d{1,2}[/-](\d{4})\b').firstMatch(str);
      if (dateMatch != null) {
        final val = int.tryParse(dateMatch.group(1)!);
        if (val != null && val >= 1990 && val <= 2040) return val;
      }
    }
    for (final cell in row) {
      final str = cell.toString();
      final expMatch = RegExp(r'(?:19|20)\d{2}').allMatches(str);
      if (expMatch.isNotEmpty) {
        final val = int.tryParse(expMatch.last.group(0)!);
        if (val != null && val >= 1990 && val <= 2040) return val;
      }
    }
    return null;
  }

  /// Inserta una nueva causa en la pestaña seleccionada de Google Sheets.
  /// Si no existe el banner del año actual (ej. CAUSAS 2026), lo crea automáticamente
  /// e inserta la nueva causa inmediatamente debajo de dicho banner.
  Future<bool> insertRowForTab(PgetTab tab, List<dynamic> rowValues, {int? causeYear}) async {
    final ws = await getWorksheet(tab);
    if (ws == null) {
      throw Exception("No se pudo conectar a Google Sheets: ${_lastError ?? 'compruebe su conexión a internet'}");
    }

    final targetYear = causeYear ?? _extractYearFromRow(rowValues) ?? DateTime.now().year;

    try {
      final allRows = await ws.values.allRows();
      final bannerPattern = RegExp(r'CAUSAS?\s*(?:A[ÑN]O)?\s*(\d{4})', caseSensitive: false);

      bool usesAnoInBanner = false;
      int? targetYearBannerRow;
      int? nextBannerRowAfterTarget;
      int lastMeaningfulRow = tab.headerRow;

      for (int i = 0; i < allRows.length; i++) {
        final rowNumber = i + 1; // 1-based index
        final row = allRows[i];
        final line = row.map((c) => c.toString()).join(' ').trim();
        final match = bannerPattern.firstMatch(line);

        if (match != null) {
          final yr = int.tryParse(match.group(1)!);
          if (line.toUpperCase().contains('AÑO') || line.toUpperCase().contains('ANO')) {
            usesAnoInBanner = true;
          }

          if (yr == targetYear) {
            targetYearBannerRow = rowNumber;
          } else if (targetYearBannerRow != null && nextBannerRowAfterTarget == null && rowNumber > targetYearBannerRow) {
            nextBannerRowAfterTarget = rowNumber;
          }
          lastMeaningfulRow = rowNumber;
        } else {
          // Evaluar si es fila de causa con datos válidos
          final nonEmpty = row.map((c) => c.toString().trim()).where((c) => c.isNotEmpty).toList();
          if (nonEmpty.length >= 2 || (nonEmpty.length == 1 && int.tryParse(nonEmpty[0]) == null)) {
            lastMeaningfulRow = rowNumber;
          } else if (nonEmpty.length == 1 && (int.tryParse(nonEmpty[0]) ?? 999) <= 25 && rowNumber <= 25) {
            lastMeaningfulRow = rowNumber;
          }
        }
      }

      final bannerText = usesAnoInBanner ? 'CAUSAS AÑO $targetYear' : 'CAUSAS $targetYear';

      if (targetYearBannerRow != null) {
        // La sección del año YA existe. Se inserta después de la última fila de este año
        if (nextBannerRowAfterTarget != null) {
          final insertAt = nextBannerRowAfterTarget;
          await ws.insertRow(insertAt);
          final ok = await ws.values.insertRow(insertAt, rowValues);
          if (ok) {
            _formatCauseRow(ws.id, insertAt, tab.columns.length);
          }
          return ok;
        } else {
          final insertAt = lastMeaningfulRow + 1;
          final ok = await ws.values.insertRow(insertAt, rowValues);
          if (ok) {
            _formatCauseRow(ws.id, insertAt, tab.columns.length);
          }
          return ok;
        }
      } else {
        // La sección del año NO existe aún (ej. CAUSAS 2026):
        // 1. Insertar el banner de año
        final bannerIndex = lastMeaningfulRow + 1;
        final bannerOk = await ws.values.insertRow(bannerIndex, [bannerText]);
        if (!bannerOk) {
          throw Exception("No se pudo crear la cabecera de $bannerText en Google Sheets.");
        }
        _formatBanner(ws.id, bannerIndex, tab.columns.length);

        // 2. Insertar la nueva causa inmediatamente debajo del banner
        final causeOk = await ws.values.insertRow(bannerIndex + 1, rowValues);
        if (causeOk) {
          _formatCauseRow(ws.id, bannerIndex + 1, tab.columns.length);
        }
        return causeOk;
      }
    } catch (e) {
      debugPrint("Error inserting row in ${tab.title}: $e");
      rethrow;
    }
  }

  /// Actualiza una fila existente en la pestaña seleccionada
  Future<bool> updateRowForTab(PgetTab tab, int rowIndex, List<dynamic> rowValues) async {
    final ws = await getWorksheet(tab);
    if (ws == null) {
      throw Exception("No se pudo conectar a Google Sheets: ${_lastError ?? 'compruebe su conexión a internet'}");
    }

    try {
      final ok = await ws.values.insertRow(rowIndex, rowValues);
      if (ok) {
        _formatCauseRow(ws.id, rowIndex, tab.columns.length);
      }
      return ok;
    } catch (e) {
      debugPrint("Error updating row in ${tab.title}: $e");
      rethrow;
    }
  }

  /// Aplica el diseño institucional idéntico a las cabeceras anuales existentes (fondo celeste #92CDE0, 24pt, negrita, centrado vertical, fila fusionada)
  Future<void> _formatBanner(int sheetId, int rowNumber, int columnCount) async {
    if (_authClient == null) return;
    try {
      final cols = columnCount > 0 ? columnCount : 20;
      final body = {
        'requests': [
          {
            'mergeCells': {
              'range': {
                'sheetId': sheetId,
                'startRowIndex': rowNumber - 1,
                'endRowIndex': rowNumber,
                'startColumnIndex': 0,
                'endColumnIndex': cols,
              },
              'mergeType': 'MERGE_ALL',
            }
          },
          {
            'repeatCell': {
              'range': {
                'sheetId': sheetId,
                'startRowIndex': rowNumber - 1,
                'endRowIndex': rowNumber,
                'startColumnIndex': 0,
                'endColumnIndex': cols,
              },
              'cell': {
                'userEnteredFormat': {
                  'backgroundColor': {
                    'red': 0.5725,
                    'green': 0.8039,
                    'blue': 0.8627,
                  },
                  'textFormat': {
                    'fontFamily': 'Arial',
                    'fontSize': 24,
                    'bold': true,
                  },
                  'verticalAlignment': 'MIDDLE',
                  'horizontalAlignment': 'LEFT',
                  'borders': {
                    'top': {'style': 'SOLID'},
                    'bottom': {'style': 'SOLID'},
                    'left': {'style': 'SOLID'},
                    'right': {'style': 'SOLID'},
                  },
                }
              },
              'fields': 'userEnteredFormat(backgroundColor,textFormat,verticalAlignment,horizontalAlignment,borders)',
            }
          },
          {
            'updateDimensionProperties': {
              'range': {
                'sheetId': sheetId,
                'dimension': 'ROWS',
                'startIndex': rowNumber - 1,
                'endIndex': rowNumber,
              },
              'properties': {'pixelSize': 55},
              'fields': 'pixelSize',
            }
          }
        ]
      };
      await _authClient!.post(
        Uri.parse('https://sheets.googleapis.com/v4/spreadsheets/$spreadsheetId:batchUpdate'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode(body),
      );
    } catch (e) {
      debugPrint("Notice: could not format banner in Google Sheets: $e");
    }
  }

  /// Aplica el diseño centrado horizontal y verticalmente a las celdas de una causa nueva o modificada
  Future<void> _formatCauseRow(int sheetId, int rowNumber, int columnCount) async {
    if (_authClient == null) return;
    try {
      final cols = columnCount > 0 ? columnCount : 20;
      final body = {
        'requests': [
          {
            'repeatCell': {
              'range': {
                'sheetId': sheetId,
                'startRowIndex': rowNumber - 1,
                'endRowIndex': rowNumber,
                'startColumnIndex': 0,
                'endColumnIndex': cols,
              },
              'cell': {
                'userEnteredFormat': {
                  'verticalAlignment': 'MIDDLE',
                  'horizontalAlignment': 'CENTER',
                  'wrapStrategy': 'WRAP',
                  'textFormat': {
                    'fontFamily': 'Arial',
                    'fontSize': 10,
                  },
                  'borders': {
                    'top': {'style': 'SOLID'},
                    'bottom': {'style': 'SOLID'},
                    'left': {'style': 'SOLID'},
                    'right': {'style': 'SOLID'},
                  },
                }
              },
              'fields': 'userEnteredFormat(verticalAlignment,horizontalAlignment,wrapStrategy,textFormat,borders)',
            }
          },
          {
            'updateDimensionProperties': {
              'range': {
                'sheetId': sheetId,
                'dimension': 'ROWS',
                'startIndex': rowNumber - 1,
                'endIndex': rowNumber,
              },
              'properties': {'pixelSize': 40},
              'fields': 'pixelSize',
            }
          }
        ]
      };
      await _authClient!.post(
        Uri.parse('https://sheets.googleapis.com/v4/spreadsheets/$spreadsheetId:batchUpdate'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode(body),
      );
    } catch (e) {
      debugPrint("Notice: could not format cause row in Google Sheets: $e");
    }
  }
}
