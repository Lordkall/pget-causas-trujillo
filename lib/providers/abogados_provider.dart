import 'package:flutter/foundation.dart';
import 'package:intl/intl.dart';
import 'dart:convert';
import '../models/pget_tab.dart';
import '../models/abogado_pget.dart';
import '../models/causa_judicial.dart';
import '../models/auditoria_registro.dart';
import '../services/google_sheets_service.dart';

class AbogadosProvider with ChangeNotifier {
  final GoogleSheetsService _sheetsService = GoogleSheetsService();

  // Lista de todas las pestañas de la Procuraduría (menos Gráfico1)
  final List<PgetTab> _tabs = pgetTabsList;
  late PgetTab _currentTab;

  // Filas cargadas de la pestaña actual
  List<List<dynamic>> _currentTabRows = [];

  // Nómina de abogados
  List<AbogadoPGET> _abogados = [];

  // Registro de Auditoría para el Administrador
  List<AuditoriaRegistro> _auditoriaLogs = [];

  bool _isLoading = false;
  bool _isSaving = false;
  String? _errorMessage;

  // Rol activo
  bool _isAdminMode = true;
  AbogadoPGET? _abogadoSesion;

  String _searchQuery = '';
  String _selectedEstadoFilter = 'TODAS';
  String _selectedYearFilter = 'TODOS';

  AbogadosProvider() {
    _currentTab = _tabs.first; // JUZGADOS DE MUNICIPIOS ORDINARI
    _initAbogadosReales();
    _initAuditoriaBase();
  }

  // Getters
  List<PgetTab> get tabs => _tabs;
  PgetTab get currentTab => _currentTab;
  List<List<dynamic>> get currentTabRows => _currentTabRows;
  List<AbogadoPGET> get abogados => _abogados;
  List<AbogadoPGET> get abogadosActivos => _abogados.where((a) => a.activo).toList();
  List<AuditoriaRegistro> get auditoriaLogs => _auditoriaLogs;
  bool get isLoading => _isLoading;
  bool get isSaving => _isSaving;
  String? get errorMessage => _errorMessage;
  bool get isAdminMode => _isAdminMode;
  AbogadoPGET? get abogadoSesion => _abogadoSesion;
  String get searchQuery => _searchQuery;
  String get selectedEstadoFilter => _selectedEstadoFilter;
  String get selectedYearFilter => _selectedYearFilter;

  /// Retorna las causas mapeadas como objetos CausaJudicial usando la estructura de la pestaña activa
  List<CausaJudicial> get causas {
    return _currentTabRows.asMap().entries.map((entry) {
      final index = entry.key + 1;
      final row = entry.value;
      return CausaJudicial.fromTabRow(_currentTab, row, rowIndex: index);
    }).toList();
  }

  int get totalCausasTab => _currentTabRows.length;

  int get causasActivasTab {
    final estadoIdx = _getEstadoColumnIndex();
    if (estadoIdx == -1) return _currentTabRows.length;
    return _currentTabRows.where((r) {
      if (r.length <= estadoIdx) return false;
      final val = r[estadoIdx].toString().toUpperCase();
      return val.contains('ACTIV');
    }).length;
  }

  int get causasCerradasTab {
    final estadoIdx = _getEstadoColumnIndex();
    if (estadoIdx == -1) return 0;
    return _currentTabRows.where((r) {
      if (r.length <= estadoIdx) return false;
      final val = r[estadoIdx].toString().toUpperCase();
      return val.contains('CERRAD');
    }).length;
  }

  /// Lista de años disponibles en la pestaña actual para filtrar
  List<String> get availableYears {
    final Set<String> years = {};
    for (final r in _currentTabRows) {
      final y = _extractYearFromRow(r);
      if (y != null && y.isNotEmpty) {
        years.add(y);
      }
    }
    final sorted = years.toList()..sort((a, b) => b.compareTo(a));
    return ['TODOS', ...sorted];
  }

  String? _extractYearFromRow(List<dynamic> row) {
    final text = row.join(' ');
    // Buscar formato de 4 dígitos entre 1990 y 2030
    final regExp = RegExp(r'\b(199\d|20[0-3]\d)\b');
    final matches = regExp.allMatches(text);
    if (matches.isNotEmpty) {
      return matches.last.group(0);
    }
    return null;
  }

  int _getEstadoColumnIndex() {
    return _currentTab.columns.indexWhere((c) {
      final u = c.toUpperCase();
      return u.contains('ESTADO');
    });
  }

  int _getAbogadoColumnIndex() {
    return _currentTab.columns.indexWhere((c) {
      final u = c.toUpperCase();
      return u.contains('ABG') || u.contains('RESPONSABLE');
    });
  }

  void setCurrentTab(PgetTab tab) {
    _currentTab = tab;
    _selectedYearFilter = 'TODOS';
    notifyListeners();
    cargarFilasPestana();
  }

  void toggleRoleMode() {
    _isAdminMode = !_isAdminMode;
    if (!_isAdminMode && _abogadoSesion == null && _abogados.isNotEmpty) {
      _abogadoSesion = _abogados.first;
    }
    notifyListeners();
  }

  void setAbogadoSesion(AbogadoPGET abogado) {
    _abogadoSesion = abogado;
    notifyListeners();
  }

  void setSearchQuery(String query) {
    _searchQuery = query;
    notifyListeners();
  }

  void setEstadoFilter(String estado) {
    _selectedEstadoFilter = estado;
    notifyListeners();
  }

  void setYearFilter(String year) {
    _selectedYearFilter = year;
    notifyListeners();
  }

  // Filtrado de filas de la pestaña activa (por Búsqueda, Estado y Año - Sin obligar a seleccionar abogado)
  List<List<dynamic>> get filteredRows {
    final estIdx = _getEstadoColumnIndex();

    return _currentTabRows.where((row) {
      // 1. Filtro de Estado
      if (_selectedEstadoFilter != 'TODAS' && estIdx != -1) {
        if (row.length > estIdx) {
          final estadoFila = row[estIdx].toString().toUpperCase();
          if (!estadoFila.contains(_selectedEstadoFilter.toUpperCase())) {
            return false;
          }
        }
      }

      // 3. Filtro de Año
      if (_selectedYearFilter != 'TODOS') {
        final rowYear = _extractYearFromRow(row);
        if (rowYear != _selectedYearFilter) {
          return false;
        }
      }

      // 4. Búsqueda por Texto
      if (_searchQuery.isNotEmpty) {
        final query = _searchQuery.toLowerCase();
        final rowText = row.join(' ').toLowerCase();
        if (!rowText.contains(query)) {
          return false;
        }
      }

      return true;
    }).toList();
  }

  /// Cargar las filas de la pestaña actualmente seleccionada
  Future<void> cargarFilasPestana() async {
    _isLoading = true;
    _errorMessage = null;
    notifyListeners();

    try {
      final rows = await _sheetsService.getRowsForTab(_currentTab);
      _currentTabRows = rows;
    } catch (e) {
      _errorMessage = e.toString();
      debugPrint("Error loading tab rows: $e");
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  /// Registrar una nueva fila/causa en la pestaña correspondiente de Google Sheets
  Future<bool> registrarFilaEnPestana(PgetTab tab, List<dynamic> valores) async {
    _isSaving = true;
    notifyListeners();

    try {
      await _sheetsService.insertRowForTab(tab, valores);

      if (tab.title == _currentTab.title) {
        _currentTabRows.insert(0, valores);
      }

      // Registro de Auditoría
      final usuario = _isAdminMode ? 'Administrador PGET' : (_abogadoSesion?.nombre ?? 'Abogado PGET');
      final expIdx = tab.columns.indexWhere((c) => c.toUpperCase().contains('EXPEDIENTE'));
      final exp = (expIdx != -1 && valores.length > expIdx) ? valores[expIdx].toString() : 'Nuevo';

      registrarAuditoria(
        accion: 'CREACIÓN DE CAUSA',
        expediente: exp,
        pestana: tab.title,
        detalle: 'Se creó nueva causa en la materia con ${valores.length} campos diligenciados.',
        usuario: usuario,
      );

      _isSaving = false;
      notifyListeners();
      return true;
    } catch (e) {
      _errorMessage = e.toString();
      _isSaving = false;
      notifyListeners();
      return false;
    }
  }

  /// Actualizar una fila existente en la pestaña actual (ej. agregar actuación procesal)
  Future<bool> actualizarActuacionFila(int rowIndex, String nuevaActuacion, String? nuevoEstado) async {
    _isSaving = true;
    notifyListeners();

    try {
      final realIndex = rowIndex - 1;
      if (realIndex < 0 || realIndex >= _currentTabRows.length) {
        throw Exception("Índice de fila fuera de rango");
      }

      final List<dynamic> filaOriginal = List.from(_currentTabRows[realIndex]);
      final actuacionIdx = _currentTab.columns.indexWhere((c) => c.toUpperCase().contains('ACTUACION'));
      final estadoIdx = _getEstadoColumnIndex();
      final expIdx = _currentTab.columns.indexWhere((c) => c.toUpperCase().contains('EXPEDIENTE'));

      final hoy = DateFormat('dd/MM/yyyy').format(DateTime.now());

      if (actuacionIdx != -1) {
        while (filaOriginal.length <= actuacionIdx) {
          filaOriginal.add('');
        }
        final anterior = filaOriginal[actuacionIdx].toString();
        filaOriginal[actuacionIdx] = anterior.isNotEmpty
            ? '$anterior\n\nEN FECHA $hoy: ${nuevaActuacion.toUpperCase()}'
            : 'EN FECHA $hoy: ${nuevaActuacion.toUpperCase()}';
      }

      if (nuevoEstado != null && estadoIdx != -1) {
        while (filaOriginal.length <= estadoIdx) {
          filaOriginal.add('');
        }
        filaOriginal[estadoIdx] = nuevoEstado;
      }

      final sheetRowNumber = _currentTab.headerRow + 1 + realIndex;
      await _sheetsService.updateRowForTab(_currentTab, sheetRowNumber, filaOriginal);

      _currentTabRows[realIndex] = filaOriginal;

      // Registro de Auditoría
      final usuario = _isAdminMode ? 'Administrador PGET' : (_abogadoSesion?.nombre ?? 'Abogado PGET');
      final exp = (expIdx != -1 && filaOriginal.length > expIdx) ? filaOriginal[expIdx].toString() : 'Fila $sheetRowNumber';

      registrarAuditoria(
        accion: 'NUEVA ACTUACIÓN PROCESAL',
        expediente: exp,
        pestana: _currentTab.title,
        detalle: 'Actuación añadida: "${nuevaActuacion.toUpperCase()}". Estado resultante: ${nuevoEstado ?? "Sin cambio"}.',
        usuario: usuario,
      );

      _isSaving = false;
      notifyListeners();
      return true;
    } catch (e) {
      _errorMessage = e.toString();
      _isSaving = false;
      notifyListeners();
      return false;
    }
  }

  /// Wrapper para registrar actuación a partir de un objeto CausaJudicial
  Future<bool> registrarNuevaActuacion({
    required CausaJudicial causa,
    required String nuevaActuacion,
    String? nuevoEstado,
  }) async {
    final rowIndex = causa.rowIndex ?? 1;
    return await actualizarActuacionFila(rowIndex, nuevaActuacion, nuevoEstado);
  }

  /// Actualizar la fila completa de una causa
  Future<bool> actualizarFilaCompleta(PgetTab tab, int rowIndex, List<dynamic> nuevosValores) async {
    _isSaving = true;
    notifyListeners();

    try {
      final realIndex = rowIndex - 1;
      final sheetRowNumber = tab.headerRow + 1 + realIndex;
      await _sheetsService.updateRowForTab(tab, sheetRowNumber, nuevosValores);

      if (tab.title == _currentTab.title && realIndex >= 0 && realIndex < _currentTabRows.length) {
        _currentTabRows[realIndex] = nuevosValores;
      }

      final usuario = _isAdminMode ? 'Administrador PGET' : (_abogadoSesion?.nombre ?? 'Abogado PGET');
      final expIdx = tab.columns.indexWhere((c) => c.toUpperCase().contains('EXPEDIENTE'));
      final exp = (expIdx != -1 && nuevosValores.length > expIdx) ? nuevosValores[expIdx].toString() : 'Fila $sheetRowNumber';

      registrarAuditoria(
        accion: 'MODIFICACIÓN DE CAUSA',
        expediente: exp,
        pestana: tab.title,
        detalle: 'Se actualizaron los datos del expediente judicial.',
        usuario: usuario,
      );

      _isSaving = false;
      notifyListeners();
      return true;
    } catch (e) {
      _errorMessage = e.toString();
      _isSaving = false;
      notifyListeners();
      return false;
    }
  }

  /// Eliminar una causa judicial de Google Sheets y del registro local (permitido para Abogados y Admin)
  Future<bool> eliminarCausa(CausaJudicial causa) async {
    _isSaving = true;
    notifyListeners();

    try {
      final realIndex = (causa.rowIndex ?? 1) - 1;
      final sheetRowNumber = _currentTab.headerRow + 1 + realIndex;

      // Limpiar fila en Google Sheets
      final filaVacia = List.filled(_currentTab.columns.length, '');
      await _sheetsService.updateRowForTab(_currentTab, sheetRowNumber, filaVacia);

      if (realIndex >= 0 && realIndex < _currentTabRows.length) {
        _currentTabRows.removeAt(realIndex);
      }

      final usuario = _isAdminMode ? 'Administrador PGET' : (_abogadoSesion?.nombre ?? 'Abogado PGET');

      registrarAuditoria(
        accion: 'ELIMINACIÓN DE CAUSA',
        expediente: causa.numeroExpediente,
        pestana: _currentTab.title,
        detalle: 'Se eliminó la causa judicial por decisión de $usuario.',
        usuario: usuario,
      );

      _isSaving = false;
      notifyListeners();
      return true;
    } catch (e) {
      _errorMessage = e.toString();
      _isSaving = false;
      notifyListeners();
      return false;
    }
  }

  // --- GESTIÓN DE AUDITORÍA ---
  void registrarAuditoria({
    required String accion,
    required String expediente,
    required String pestana,
    required String detalle,
    String? usuario,
  }) {
    final u = usuario ?? (_isAdminMode ? 'Administrador PGET' : (_abogadoSesion?.nombre ?? 'Abogado PGET'));
    _auditoriaLogs.insert(
      0,
      AuditoriaRegistro(
        id: 'AUD-${DateTime.now().millisecondsSinceEpoch}',
        usuario: u,
        accion: accion,
        expediente: expediente,
        pestana: pestana,
        detalle: detalle,
      ),
    );
    notifyListeners();
  }

  // --- GESTIÓN CRUD DE ABOGADOS (PRESERVANDO HISTORIAL) ---

  /// Añadir abogado a la nómina
  void agregarAbogado(AbogadoPGET abogado) {
    _abogados.add(abogado);
    registrarAuditoria(
      accion: 'ALTA DE ABOGADO',
      expediente: 'NÓMINA',
      pestana: 'ADMINISTRACIÓN',
      detalle: 'Se dio de alta a ${abogado.nombre} (C.I. ${abogado.cedula}) con cargo ${abogado.cargo}.',
    );
    notifyListeners();
  }

  /// Editar datos del abogado
  void actualizarAbogado(AbogadoPGET abogadoActualizado) {
    final index = _abogados.indexWhere((a) => a.id == abogadoActualizado.id);
    if (index != -1) {
      final anterior = _abogados[index];
      _abogados[index] = abogadoActualizado;
      if (_abogadoSesion?.id == abogadoActualizado.id) {
        _abogadoSesion = abogadoActualizado;
      }
      registrarAuditoria(
        accion: 'MODIFICACIÓN DE ABOGADO',
        expediente: 'NÓMINA',
        pestana: 'ADMINISTRACIÓN',
        detalle: 'Se actualizaron datos de ${anterior.nombre} a ${abogadoActualizado.nombre} (C.I. ${abogadoActualizado.cedula}).',
      );
      notifyListeners();
    }
  }

  /// Desactivar / Eliminar abogado (Soft Delete): Se retira de la nómina activa pero se PRESERVA su nombre en expedientes
  void eliminarAbogado(String id) {
    final index = _abogados.indexWhere((a) => a.id == id);
    if (index != -1) {
      final abg = _abogados[index];
      // Marcamos como inactivo para no borrar su presencia en causas históricas
      _abogados[index] = abg.copyWith(activo: false);

      if (_abogadoSesion?.id == id) {
        _abogadoSesion = _abogados.firstWhere((a) => a.activo, orElse: () => _abogados.first);
      }

      registrarAuditoria(
        accion: 'DESACTIVACIÓN DE ABOGADO',
        expediente: 'NÓMINA',
        pestana: 'ADMINISTRACIÓN',
        detalle: 'Se desactivó a ${abg.nombre} de la nómina activa. Se mantiene su historial intacto en todas las causas judiciales.',
      );
      notifyListeners();
    }
  }

  /// Reactivar abogado previamente retirado
  void reactivarAbogado(String id) {
    final index = _abogados.indexWhere((a) => a.id == id);
    if (index != -1) {
      _abogados[index] = _abogados[index].copyWith(activo: true);
      registrarAuditoria(
        accion: 'REACTIVACIÓN DE ABOGADO',
        expediente: 'NÓMINA',
        pestana: 'ADMINISTRACIÓN',
        detalle: 'Se reactivó en nómina activa a ${_abogados[index].nombre}.',
      );
      notifyListeners();
    }
  }

  AbogadoPGET? _usuarioAutenticado;
  AbogadoPGET? get usuarioAutenticado => _usuarioAutenticado;
  bool get isAuthenticated => _usuarioAutenticado != null;

  bool login(String correo, String clave) {
    final c = correo.trim().toLowerCase();
    for (final a in _abogados) {
      if (a.correo.toLowerCase() == c && a.clave == clave) {
        _usuarioAutenticado = a;
        _isAdminMode = (a.rol == 'admin');
        _abogadoSesion = a;
        registrarAuditoria(
          accion: 'LOGIN',
          expediente: 'AUTENTICACIÓN',
          pestana: 'SEGURIDAD',
          detalle: 'Inicio de sesión exitoso: ${a.nombre} (${a.rol.toUpperCase()}).',
          usuario: a.nombre,
        );
        notifyListeners();
        return true;
      }
    }
    return false;
  }

  void logout() {
    _usuarioAutenticado = null;
    notifyListeners();
  }

  // Nómina oficial activa de 13 abogados (ordenados alfabéticamente) + históricos preservados
  void _initAbogadosReales() {
    _abogados = [
      // 13 ABOGADOS ACTIVOS OFICIALES (Ordenados Alfabéticamente de la A a la Z)
      AbogadoPGET(id: '1', nombre: 'BARRIOS JULIO ALEXANDER', cedula: '14.459.865', cargo: 'ABOGADO I', adscrito: 'PROCURADURÍA GENERAL', activo: true, correo: 'juliobarrios@pget.com', clave: 'Pget2026*Julio', rol: 'abogado', telefono: '+58 414 1122334'),
      AbogadoPGET(id: '2', nombre: 'BARRIOS MARIA ALCIRA', cedula: '17.037.437', cargo: 'ABOGADO I', adscrito: 'PROCURADURÍA GENERAL', activo: true, correo: 'mariabarrios@pget.com', clave: 'Pget2026*Maria', rol: 'abogado', telefono: '+58 412 2233445'),
      AbogadoPGET(id: '3', nombre: 'BRICEÑO FERNANDEZ ARMANDO JOSE', cedula: '5.780.167', cargo: 'ABOGADO', adscrito: 'CONTENCIOSO ADMINISTRATIVO', activo: true, correo: 'armandobriceno@pget.com', clave: 'Pget2026*Armando', rol: 'abogado', telefono: '+58 416 3344556'),
      AbogadoPGET(id: '4', nombre: 'BRICEÑO VALECILLOS LIZAMAR INDIRA', cedula: '20.400.747', cargo: 'DIRECTOR DE ASUNTOS JURIDICOS', adscrito: 'DIRECCIÓN DE ASUNTOS JURÍDICOS', activo: true, correo: 'lizamarbriceno@pget.com', clave: 'Admin2026*Lizamar', rol: 'admin', telefono: '+58 414 4455667'),
      AbogadoPGET(id: '5', nombre: 'DE ABREU HERNANDEZ CARLOS EDUARDO', cedula: '10.446.852', cargo: 'ABOGADO I', adscrito: 'PROCURADURÍA GENERAL', activo: true, correo: 'carlosdeabreu@pget.com', clave: 'Pget2026*Carlos', rol: 'abogado', telefono: '+58 424 5566778'),
      AbogadoPGET(id: '6', nombre: 'DORA ALICIA MATHEUS', cedula: '10.035.929', cargo: 'PROCURADORA', adscrito: 'DESPACHO DE LA PROCURADORA', activo: true, correo: 'doramatheus@pget.com', clave: 'Pget2026*Dora', rol: 'abogado', telefono: '+58 412 6677889'),
      AbogadoPGET(id: '7', nombre: 'MERCADO HIDALGO ROXANNA KAROLINA', cedula: '23.596.460', cargo: 'ABOGADO I', adscrito: 'JUZGADOS Y TRIBUNALES', activo: true, correo: 'roxannamercado@pget.com', clave: 'Pget2026*Roxanna', rol: 'abogado', telefono: '+58 414 7788990'),
      AbogadoPGET(id: '8', nombre: 'MOLINA UZCATEGUI HUMBERTO JOSE', cedula: '20.790.382', cargo: 'ABOGADO', adscrito: 'PROCURADURÍA GENERAL', activo: true, correo: 'humbertomolina@pget.com', clave: 'Pget2026*Humberto', rol: 'abogado', telefono: '+58 416 8899001'),
      AbogadoPGET(id: '9', nombre: 'MORENO HERNANDEZ YONEXI CAROLINA', cedula: '16.738.909', cargo: 'ABOGADO', adscrito: 'PROCURADURÍA GENERAL', activo: true, correo: 'yoneximoreno@pget.com', clave: 'Pget2026*Yonexi', rol: 'abogado', telefono: '+58 424 9900112'),
      AbogadoPGET(id: '10', nombre: 'OJEDA NUÑEZ MARIA DE LOS ANGELES', cedula: '26.046.163', cargo: 'ABOGADO I', adscrito: 'CONTENCIOSO TRUJILLO', activo: true, correo: 'mariaojeda@pget.com', clave: 'Pget2026*MariaO', rol: 'abogado', telefono: '+58 412 1100223'),
      AbogadoPGET(id: '11', nombre: 'RAMIREZ OROPEZA TATIANA MARILIN', cedula: '15.315.709', cargo: 'ABOGADO I', adscrito: 'PROCURADURÍA GENERAL', activo: true, correo: 'tatianaramirez@pget.com', clave: 'Pget2026*Tatiana', rol: 'abogado', telefono: '+58 414 2211334'),
      AbogadoPGET(id: '12', nombre: 'SANCHEZ MONSALVE LILIBETH DAYANA', cedula: '13.404.142', cargo: 'ABOGADO I', adscrito: 'PROCURADURÍA GENERAL', activo: true, correo: 'lilibethsanchez@pget.com', clave: 'Pget2026*Lilibeth', rol: 'abogado', telefono: '+58 416 3322445'),
      AbogadoPGET(id: '13', nombre: 'VALE VALERA YULIANOVA PAOLA', cedula: '26.591.763', cargo: 'ABOGADO I', adscrito: 'PROCURADURÍA GENERAL', activo: true, correo: 'paolavale@pget.com', clave: 'Pget2026*Paola', rol: 'abogado', telefono: '+58 424 4433556'),

      // Abogados Históricos preservados para causas previas de Google Sheets
      AbogadoPGET(id: '14', nombre: 'SAMANTHA POLANCO', cedula: '5.493.478', cargo: 'Apoderada Judicial PGET', adscrito: 'CORPOTURISMO / PGET', activo: false, telefono: '+58 414 7234411'),
      AbogadoPGET(id: '15', nombre: 'ANAIS PERDOMO', cedula: '19.876.543', cargo: 'Especialista Laboral', adscrito: 'LABORAL E INSPECTORÍAS', activo: false, telefono: '+58 414 8877665'),
      AbogadoPGET(id: '16', nombre: 'EDGARDO BASTIDAS', cedula: '16.234.567', cargo: 'Abogado Litigante', adscrito: 'PENAL Y AMPAROS', activo: false, telefono: '+58 412 8893321'),
      AbogadoPGET(id: '17', nombre: 'MARIA FERNANDA PEÑA', cedula: '21.345.678', cargo: 'Consultora Jurídica', adscrito: 'TRIBUTARIO Y MERCANTIL', activo: false, telefono: '+58 416 5501234'),
      AbogadoPGET(id: '18', nombre: 'YELITZA VÁSQUEZ', cedula: '15.432.109', cargo: 'Abogada de Sustanciación', adscrito: 'CIVIL Y BIENES', activo: false, telefono: '+58 414 9918231'),
      AbogadoPGET(id: '19', nombre: 'JESÚS ROJAS', cedula: '14.567.890', cargo: 'Abogado Asistente', adscrito: 'CONTENCIOSO TRUJILLO', activo: false, telefono: '+58 414 6629910'),
      AbogadoPGET(id: '20', nombre: 'MARÍA VALERA', cedula: '22.345.671', cargo: 'Abogada Litigante', adscrito: 'LABORAL', activo: false, telefono: '+58 424 5510982'),
      AbogadoPGET(id: '21', nombre: 'YURAIMA ALDANA', cedula: '13.987.654', cargo: 'Abogada de Sustanciación', adscrito: 'TIERRAS Y AGRARIO', activo: false, telefono: '+58 412 3349912'),
      AbogadoPGET(id: '22', nombre: 'FRANCISCO MORENO', cedula: '11.234.567', cargo: 'Abogado Asesor', adscrito: 'CASACIÓN Y TSJ', activo: false, telefono: '+58 416 7721098'),
      AbogadoPGET(id: '23', nombre: 'ZULAY CARRILLO', cedula: '17.890.123', cargo: 'Abogada Litigante', adscrito: 'JUZGADOS Y TRIBUNALES', activo: false, telefono: '+58 414 3328819'),
      AbogadoPGET(id: '24', nombre: 'CARLOS MARÍN', cedula: '18.901.234', cargo: 'Abogado Asistente', adscrito: 'PROTECCIÓN NIÑOS', activo: false, telefono: '+58 424 8812993'),
      AbogadoPGET(id: '25', nombre: 'GREGORIO DELGADO', cedula: '15.678.901', cargo: 'Abogado Litigante', adscrito: 'TRÁNSITO', activo: false, telefono: '+58 412 6654321'),
      AbogadoPGET(id: '26', nombre: 'ADOLFO SÁNCHEZ', cedula: '16.789.012', cargo: 'Abogado Litigante', adscrito: 'CONTENCIOSO ADMINISTRATIVO', activo: false, telefono: '+58 416 9901234'),
      AbogadoPGET(id: '27', nombre: 'RAFAEL VILORIA', cedula: '14.890.123', cargo: 'Abogado Adscrito', adscrito: 'AMPAROS', activo: false, telefono: '+58 414 2233445'),
      AbogadoPGET(id: '28', nombre: 'MIRYAM MONTERO', cedula: '12.901.234', cargo: 'Consultora Adjunta', adscrito: 'ADMINISTRACIÓN', activo: false, telefono: '+58 424 1122334'),
      AbogadoPGET(id: '29', nombre: 'JOSÉ LUIS BRICEÑO', cedula: '13.012.345', cargo: 'Abogado Litigante', adscrito: 'LABORAL', activo: false, telefono: '+58 412 4455667'),
      AbogadoPGET(id: '30', nombre: 'ANDREINA SEGOVIA', cedula: '19.345.678', cargo: 'Abogada Asistente', adscrito: 'CONTENCIOSO TRUJILLO', activo: false, telefono: '+58 412 3322110'),
      AbogadoPGET(id: '31', nombre: 'VERÓNICA MARKAN', cedula: '14.234.567', cargo: 'Abogada de Sustanciación', adscrito: 'JUZGADOS Y TRIBUNALES', activo: false, telefono: '+58 414 2211443'),
    ];
    _abogadoSesion = _abogados.firstWhere((a) => a.activo, orElse: () => _abogados.first);
  }

  void _initAuditoriaBase() {
    _auditoriaLogs = [
      AuditoriaRegistro(
        id: 'AUD-001',
        fechaHora: DateTime.now().subtract(const Duration(hours: 2)),
        usuario: 'Samantha Polanco',
        accion: 'NUEVA ACTUACIÓN PROCESAL',
        expediente: '11.114',
        pestana: 'JUZGADOS DE MUNICIPIOS ORDINARI',
        detalle: 'Se agregó auto de notificación y revisión de lapso procesal en la causa.',
      ),
      AuditoriaRegistro(
        id: 'AUD-002',
        fechaHora: DateTime.now().subtract(const Duration(hours: 5)),
        usuario: 'Admin PGET',
        accion: 'ALTA DE ABOGADO',
        expediente: 'NÓMINA',
        pestana: 'ADMINISTRACIÓN',
        detalle: 'Se incorporó a Kleiver Briceño como abogado activo en Contencioso.',
      ),
      AuditoriaRegistro(
        id: 'AUD-003',
        fechaHora: DateTime.now().subtract(const Duration(days: 1)),
        usuario: 'Diana Faria',
        accion: 'CREACIÓN DE CAUSA',
        expediente: '295-2015',
        pestana: 'JUZGADOS DE MUNICIPIOS ORDINARI',
        detalle: 'Apertura de expediente por recurso contra Domesa.',
      ),
    ];
  }
}
