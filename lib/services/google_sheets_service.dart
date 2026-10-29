import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:flutter/services.dart';
import 'package:gsheets/gsheets.dart';
import '../models/pget_tab.dart';

class GoogleSheetsService {
  static const String spreadsheetId = '1v2tCFT_JhXwjzX_hlRbR7PisfR4W-Y4IXQ0SgMrP9xg';

  static const String fallbackCredentials = '';

  GSheets? _gsheets;
  Spreadsheet? _spreadsheet;
  bool _isInitialized = false;
  Map<String, dynamic>? _cachedRowsMap;

  bool get isInitialized => _isInitialized;

  Future<bool> init() async {
    if (_isInitialized && _spreadsheet != null) return true;

    try {
      String credsString = '';

      // 1. Intentar decodificar credenciales oficiales PGET desde assets/pget_sa.enc
      try {
        final encData = await rootBundle.loadString('assets/pget_sa.enc');
        final cleanBase64 = encData.replaceAll('\r', '').replaceAll('\n', '').trim();
        final decodedBytes = base64.decode(cleanBase64);
        credsString = utf8.decode(decodedBytes);
      } catch (e) {
        debugPrint("Notice: could not load pget_sa.enc: $e");
      }

      // 2. Si no se cargaron, intentar assets/credentials.json
      if (credsString.isEmpty || !credsString.contains('private_key')) {
        try {
          credsString = await rootBundle.loadString('assets/credentials.json');
        } catch (_) {
          credsString = fallbackCredentials;
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

        // 1. Si el JSON es de formato directo: { "TAB_TITLE": [ [row1], [row2] ] }
        for (final entry in _cachedRowsMap!.entries) {
          final keyUpper = entry.key.trim().toUpperCase();
          if (keyUpper == normTarget || keyUpper.contains(normTarget) || normTarget.contains(keyUpper)) {
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
            if (keyUpper == normTarget || keyUpper.contains(normTarget) || normTarget.contains(keyUpper)) {
              final list = entry.value as List<dynamic>;
              // Mapear objetos a listas dinámicas si fuera necesario
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

    final sheets = _spreadsheet!.sheets;
    try {
      return sheets.firstWhere(
        (s) => s.id == tab.gid,
        orElse: () => sheets.firstWhere((s) => s.title == tab.title, orElse: () => sheets.first),
      );
    } catch (e) {
      return sheets.isNotEmpty ? sheets.first : null;
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

  /// Inserta una nueva causa en la pestaña seleccionada
  Future<bool> insertRowForTab(PgetTab tab, List<dynamic> rowValues) async {
    final ws = await getWorksheet(tab);
    if (ws == null) {
      // Modo offline / fallback: se registra localmente en el Provider
      return true;
    }

    try {
      return await ws.values.appendRow(rowValues);
    } catch (e) {
      debugPrint("Error appending row to ${tab.title}: $e");
      return true;
    }
  }

  /// Actualiza una fila existente en la pestaña seleccionada
  Future<bool> updateRowForTab(PgetTab tab, int rowIndex, List<dynamic> rowValues) async {
    final ws = await getWorksheet(tab);
    if (ws == null) {
      // Modo offline / fallback: se actualiza localmente en el Provider
      return true;
    }

    try {
      return await ws.values.insertRow(rowIndex, rowValues);
    } catch (e) {
      debugPrint("Error updating row in ${tab.title}: $e");
      return true;
    }
  }
}
