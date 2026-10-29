class CausaJudicial {
  final String numero;
  final String juzgadoMunicipio;
  final String numeroJuzgado;
  final String demandante;
  final String demandado;
  final String motivo;
  final String numeroExpediente;
  final String abogadoResponsable;
  final String cedula;
  final String cargo;
  final String adscrito;
  final String fechaEntrada;
  final String estadoActual;
  final String actuacionesRealizadas;
  final String montoPagado;
  final String corte;
  final String numeroCorte;
  final String observaciones;
  final int? rowIndex;

  CausaJudicial({
    required this.numero,
    required this.juzgadoMunicipio,
    required this.numeroJuzgado,
    required this.demandante,
    required this.demandado,
    required this.motivo,
    required this.numeroExpediente,
    required this.abogadoResponsable,
    this.cedula = '',
    this.cargo = '',
    this.adscrito = '',
    this.fechaEntrada = '',
    this.estadoActual = 'ACTIVA',
    this.actuacionesRealizadas = '',
    this.montoPagado = '',
    this.corte = '',
    this.numeroCorte = '',
    this.observaciones = '',
    this.rowIndex,
  });

  // Convertir a fila para Google Sheets
  List<dynamic> toSheetRow() {
    return [
      numero,
      juzgadoMunicipio,
      numeroJuzgado,
      demandante,
      demandado,
      motivo,
      numeroExpediente,
      abogadoResponsable,
      cedula,
      cargo,
      adscrito,
      fechaEntrada,
      estadoActual,
      actuacionesRealizadas,
      montoPagado,
      corte,
      numeroCorte,
      observaciones,
    ];
  }

  // Parsear desde fila de Google Sheets
  factory CausaJudicial.fromSheetRow(List<dynamic> row, {int? rowIndex}) {
    String getCol(int index) {
      if (index < row.length && row[index] != null) {
        return row[index].toString().trim();
      }
      return '';
    }

    return CausaJudicial(
      numero: getCol(0),
      juzgadoMunicipio: getCol(1),
      numeroJuzgado: getCol(2),
      demandante: getCol(3),
      demandado: getCol(4),
      motivo: getCol(5),
      numeroExpediente: getCol(6),
      abogadoResponsable: getCol(7),
      cedula: getCol(8),
      cargo: getCol(9),
      adscrito: getCol(10),
      fechaEntrada: getCol(11),
      estadoActual: getCol(12).isNotEmpty ? getCol(12) : 'ACTIVA',
      actuacionesRealizadas: getCol(13),
      montoPagado: getCol(14),
      corte: getCol(15),
      numeroCorte: getCol(16),
      observaciones: getCol(17),
      rowIndex: rowIndex,
    );
  }

  // Parsear desde fila considerando la estructura dinámica de la pestaña
  factory CausaJudicial.fromTabRow(dynamic tab, List<dynamic> row, {int? rowIndex}) {
    String getVal(int idx) {
      if (idx >= 0 && idx < row.length && row[idx] != null) {
        return row[idx].toString().trim();
      }
      return '';
    }

    final List<String> cols = tab.columns is List<String> 
        ? tab.columns as List<String> 
        : (tab.columns as List).map((e) => e.toString()).toList();

    int findCol(List<String> keywords) {
      return cols.indexWhere((c) {
        final upper = c.toUpperCase();
        return keywords.any((k) => upper.contains(k));
      });
    }

    final expIdx = findCol(['EXPEDIENTE', 'INVESTIGACION', 'ASUNTO']);
    final demIdx = findCol(['DEMANDANTE', 'QUERELLANTE', 'SOLICITANTE', 'RECURRENTE']);
    final dmdIdx = findCol(['DEMANDADO', 'QUERELLADO', 'IMPUTADO', 'SOLICITADO', 'VICTIMA']);
    final motIdx = findCol(['MOTIVO', 'DELITO', 'ACCION', 'OBJETO', 'DESCRIPCION']);
    final abgIdx = findCol(['ABG', 'ABOGAD', 'RESPONSABLE', 'ASIGNAD']);
    final estIdx = findCol(['ESTADO']);
    final actIdx = findCol(['ACTUACION', 'OBSERVACION', 'DILIGENCIA']);
    final fecIdx = findCol(['FECHA']);

    final tabTitle = tab.title?.toString() ?? 'PGET';
    final expVal = getVal(expIdx);

    return CausaJudicial(
      numero: (rowIndex ?? 1).toString(),
      juzgadoMunicipio: tabTitle,
      numeroJuzgado: '',
      demandante: getVal(demIdx),
      demandado: getVal(dmdIdx),
      motivo: getVal(motIdx).isNotEmpty ? getVal(motIdx) : 'Asunto registrado',
      numeroExpediente: expVal.isNotEmpty ? expVal : 'REG-$rowIndex',
      abogadoResponsable: getVal(abgIdx),
      fechaEntrada: getVal(fecIdx),
      estadoActual: getVal(estIdx).isNotEmpty ? getVal(estIdx) : 'ACTIVA',
      actuacionesRealizadas: getVal(actIdx),
      rowIndex: rowIndex,
    );
  }

  CausaJudicial copyWith({
    String? numero,
    String? juzgadoMunicipio,
    String? numeroJuzgado,
    String? demandante,
    String? demandado,
    String? motivo,
    String? numeroExpediente,
    String? abogadoResponsable,
    String? cedula,
    String? cargo,
    String? adscrito,
    String? fechaEntrada,
    String? estadoActual,
    String? actuacionesRealizadas,
    String? montoPagado,
    String? corte,
    String? numeroCorte,
    String? observaciones,
    int? rowIndex,
  }) {
    return CausaJudicial(
      numero: numero ?? this.numero,
      juzgadoMunicipio: juzgadoMunicipio ?? this.juzgadoMunicipio,
      numeroJuzgado: numeroJuzgado ?? this.numeroJuzgado,
      demandante: demandante ?? this.demandante,
      demandado: demandado ?? this.demandado,
      motivo: motivo ?? this.motivo,
      numeroExpediente: numeroExpediente ?? this.numeroExpediente,
      abogadoResponsable: abogadoResponsable ?? this.abogadoResponsable,
      cedula: cedula ?? this.cedula,
      cargo: cargo ?? this.cargo,
      adscrito: adscrito ?? this.adscrito,
      fechaEntrada: fechaEntrada ?? this.fechaEntrada,
      estadoActual: estadoActual ?? this.estadoActual,
      actuacionesRealizadas: actuacionesRealizadas ?? this.actuacionesRealizadas,
      montoPagado: montoPagado ?? this.montoPagado,
      corte: corte ?? this.corte,
      numeroCorte: numeroCorte ?? this.numeroCorte,
      observaciones: observaciones ?? this.observaciones,
      rowIndex: rowIndex ?? this.rowIndex,
    );
  }
}

