import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:flutter/services.dart';
import 'package:gsheets/gsheets.dart';
import '../models/pget_tab.dart';
import 'pget_credentials.dart';

class GoogleSheetsService {
  static const String spreadsheetId = '1v2tCFT_JhXwjzX_hlRbR7PisfR4W-Y4IXQ0SgMrP9xg';

  GSheets? _gsheets;
  Spreadsheet? _spreadsheet;
  bool _isInitialized = false;
  Map<String, dynamic>? _cachedRowsMap;

  bool get isInitialized => _isInitialized;

  /// Inicializa la conexión con Google Sheets usando las credenciales oficiales de la PGET
  Future<bool> init() async {
    if (_isInitialized && _spreadsheet != null) return true;

    try {
      String credsString = pgetOfficialCredentialsJson;

      // Respaldo secundario desde assets/pget_sa.enc si estuviese disponible
      if (credsString.isEmpty || !credsString.contains('private_key')) {
        try {
          final encData = await rootBundle.loadString('assets/pget_sa.enc');
          final cleanBase64 = encData.replaceAll('\r', '').replaceAll('\n', '').trim();
          final decodedBytes = base64.decode(cleanBase64);
          credsString = utf8.decode(decodedBytes);
        } catch (e) {
          debugPrint("Notice: could not load pget_sa.enc: $e");
        }
      }

      if (credsString.isNotEmpty && credsString.contains('private_key')) {
        _gsheets = GSheets(credsString);
        _spreadsheet = await _gsheets!.spreadsheet(spreadsheetId);
        _isInitialized = true;
        return true;
      }

      _isInitialized = false;
      return false;
    } catch (e) {
      _isInitialized = false;
      debugPrint("Error initializing GSheets live connection: $e");
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
    if (!ok || _spreadsheet == null) return null;

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
        orElse: () => sheets.first,
      );
    } catch (e) {
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
        final validRows = rows.where((r) => r.isNotEmpty && r.any((val) => val.toString().trim().isNotEmpty)).toList();
        if (validRows.isNotEmpty) {
          return validRows;
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
      throw Exception("No se pudo conectar a Google Sheets. Verifique la conexión a internet.");
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
        final insertAt = (nextBannerRowAfterTarget != null)
            ? nextBannerRowAfterTarget
            : (lastMeaningfulRow + 1);
        final ok = await ws.values.insertRow(insertAt, rowValues);
        return ok;
      } else {
        // La sección del año NO existe aún (ej. CAUSAS 2026):
        // 1. Insertar el banner de año
        final bannerIndex = lastMeaningfulRow + 1;
        final bannerOk = await ws.values.insertRow(bannerIndex, [bannerText]);
        if (!bannerOk) {
          throw Exception("No se pudo crear la cabecera de $bannerText en Google Sheets.");
        }
        // 2. Insertar la nueva causa inmediatamente debajo del banner
        final causeOk = await ws.values.insertRow(bannerIndex + 1, rowValues);
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
      throw Exception("No se pudo conectar a Google Sheets para actualizar.");
    }

    try {
      return await ws.values.insertRow(rowIndex, rowValues);
    } catch (e) {
      debugPrint("Error updating row in ${tab.title}: $e");
      rethrow;
    }
  }
}
