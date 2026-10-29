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

  bool get isInitialized => _isInitialized;

  Future<bool> init() async {
    if (_isInitialized && _spreadsheet != null) return true;

    try {
      String credsString;
      try {
        credsString = await rootBundle.loadString('assets/credentials.json');
      } catch (_) {
        credsString = fallbackCredentials;
      }

      _gsheets = GSheets(credsString);
      _spreadsheet = await _gsheets!.spreadsheet(spreadsheetId);
      _isInitialized = true;
      return true;
    } catch (e) {
      _isInitialized = false;
      debugPrint("Error initializing GSheets: $e");
      rethrow;
    }
  }

  /// Obtiene una pestaña específica por su GID o Título
  Future<Worksheet?> getWorksheet(PgetTab tab) async {
    await init();
    final sheets = _spreadsheet!.sheets;
    try {
      return sheets.firstWhere(
        (s) => s.id == tab.gid,
        orElse: () => sheets.firstWhere((s) => s.title == tab.title, orElse: () => sheets.first),
      );
    } catch (e) {
      return sheets.first;
    }
  }

  /// Carga las filas de datos de una pestaña respetando su fila de encabezados
  Future<List<List<dynamic>>> getRowsForTab(PgetTab tab) async {
    final ws = await getWorksheet(tab);
    if (ws == null) return [];

    try {
      // Las filas de datos inician después de la fila de encabezados (headerRow + 1)
      final startRow = tab.headerRow + 1;
      final rows = await ws.values.allRows(fromRow: startRow);
      return rows.where((r) => r.isNotEmpty && r.any((val) => val.toString().trim().isNotEmpty)).toList();
    } catch (e) {
      debugPrint("Error reading rows for ${tab.title}: $e");
      return [];
    }
  }

  /// Inserta una nueva causa en la pestaña seleccionada
  Future<bool> insertRowForTab(PgetTab tab, List<dynamic> rowValues) async {
    final ws = await getWorksheet(tab);
    if (ws == null) throw Exception("No se pudo acceder a la pestaña ${tab.title}");

    try {
      return await ws.values.appendRow(rowValues);
    } catch (e) {
      debugPrint("Error appending row to ${tab.title}: $e");
      rethrow;
    }
  }

  /// Actualiza una fila existente en la pestaña seleccionada
  Future<bool> updateRowForTab(PgetTab tab, int rowIndex, List<dynamic> rowValues) async {
    final ws = await getWorksheet(tab);
    if (ws == null) throw Exception("No se pudo acceder a la pestaña ${tab.title}");

    try {
      return await ws.values.insertRow(rowIndex, rowValues);
    } catch (e) {
      debugPrint("Error updating row in ${tab.title}: $e");
      rethrow;
    }
  }
}
