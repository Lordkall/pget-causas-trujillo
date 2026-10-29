import 'package:intl/intl.dart';

class Abogado {
  final String id;
  final String nombre;
  final String identificacion;
  final String colegiatura;
  final String especialidad;
  final String telefono;
  final String correo;
  final String estado;
  final String despacho;
  final String ciudad;
  final DateTime fechaRegistro;
  final String observaciones;

  Abogado({
    required this.id,
    required this.nombre,
    required this.identificacion,
    required this.colegiatura,
    required this.especialidad,
    required this.telefono,
    required this.correo,
    this.estado = 'Activo',
    this.despacho = '',
    this.ciudad = '',
    DateTime? fechaRegistro,
    this.observaciones = '',
  }) : fechaRegistro = fechaRegistro ?? DateTime.now();

  // Columnas ordenadas para Google Sheets
  static const List<String> columns = [
    'ID',
    'Nombre Completo',
    'Cédula / DNI',
    'N° Colegiatura',
    'Especialidad',
    'Teléfono / WhatsApp',
    'Correo Electrónico',
    'Estado',
    'Despacho / Bufete',
    'Ciudad / Sede',
    'Fecha de Registro',
    'Observaciones',
  ];

  // Convertir a fila de Google Sheets (List<dynamic>)
  List<dynamic> toSheetRow() {
    final dateFormat = DateFormat('dd/MM/yyyy HH:mm');
    return [
      id,
      nombre,
      identificacion,
      colegiatura,
      especialidad,
      telefono,
      correo,
      estado,
      despacho,
      ciudad,
      dateFormat.format(fechaRegistro),
      observaciones,
    ];
  }

  // Crear desde fila o mapa de Google Sheets
  factory Abogado.fromSheetRow(List<dynamic> row) {
    DateTime parsedDate;
    try {
      if (row.length > 10 && row[10] != null && row[10].toString().isNotEmpty) {
        parsedDate = DateFormat('dd/MM/yyyy HH:mm').parse(row[10].toString());
      } else {
        parsedDate = DateTime.now();
      }
    } catch (_) {
      parsedDate = DateTime.now();
    }

    return Abogado(
      id: row.isNotEmpty ? row[0]?.toString() ?? '' : '',
      nombre: row.length > 1 ? row[1]?.toString() ?? '' : '',
      identificacion: row.length > 2 ? row[2]?.toString() ?? '' : '',
      colegiatura: row.length > 3 ? row[3]?.toString() ?? '' : '',
      especialidad: row.length > 4 ? row[4]?.toString() ?? 'General' : 'General',
      telefono: row.length > 5 ? row[5]?.toString() ?? '' : '',
      correo: row.length > 6 ? row[6]?.toString() ?? '' : '',
      estado: row.length > 7 ? row[7]?.toString() ?? 'Activo' : 'Activo',
      despacho: row.length > 8 ? row[8]?.toString() ?? '' : '',
      ciudad: row.length > 9 ? row[9]?.toString() ?? '' : '',
      fechaRegistro: parsedDate,
      observaciones: row.length > 10 ? row[11]?.toString() ?? '' : '',
    );
  }

  factory Abogado.fromMap(Map<String, dynamic> map) {
    DateTime parsedDate;
    try {
      if (map['Fecha de Registro'] != null) {
        parsedDate = DateFormat('dd/MM/yyyy HH:mm').parse(map['Fecha de Registro'].toString());
      } else {
        parsedDate = DateTime.now();
      }
    } catch (_) {
      parsedDate = DateTime.now();
    }

    return Abogado(
      id: map['ID']?.toString() ?? '',
      nombre: map['Nombre Completo']?.toString() ?? '',
      identificacion: map['Cédula / DNI']?.toString() ?? '',
      colegiatura: map['N° Colegiatura']?.toString() ?? '',
      especialidad: map['Especialidad']?.toString() ?? 'General',
      telefono: map['Teléfono / WhatsApp']?.toString() ?? '',
      correo: map['Correo Electrónico']?.toString() ?? '',
      estado: map['Estado']?.toString() ?? 'Activo',
      despacho: map['Despacho / Bufete']?.toString() ?? '',
      ciudad: map['Ciudad / Sede']?.toString() ?? '',
      fechaRegistro: parsedDate,
      observaciones: map['Observaciones']?.toString() ?? '',
    );
  }

  Map<String, dynamic> toMap() {
    final dateFormat = DateFormat('dd/MM/yyyy HH:mm');
    return {
      'ID': id,
      'Nombre Completo': nombre,
      'Cédula / DNI': identificacion,
      'N° Colegiatura': colegiatura,
      'Especialidad': especialidad,
      'Teléfono / WhatsApp': telefono,
      'Correo Electrónico': correo,
      'Estado': estado,
      'Despacho / Bufete': despacho,
      'Ciudad / Sede': ciudad,
      'Fecha de Registro': dateFormat.format(fechaRegistro),
      'Observaciones': observaciones,
    };
  }

  Abogado copyWith({
    String? id,
    String? nombre,
    String? identificacion,
    String? colegiatura,
    String? especialidad,
    String? telefono,
    String? correo,
    String? estado,
    String? despacho,
    String? ciudad,
    DateTime? fechaRegistro,
    String? observaciones,
  }) {
    return Abogado(
      id: id ?? this.id,
      nombre: nombre ?? this.nombre,
      identificacion: identificacion ?? this.identificacion,
      colegiatura: colegiatura ?? this.colegiatura,
      especialidad: especialidad ?? this.especialidad,
      telefono: telefono ?? this.telefono,
      correo: correo ?? this.correo,
      estado: estado ?? this.estado,
      despacho: despacho ?? this.despacho,
      ciudad: ciudad ?? this.ciudad,
      fechaRegistro: fechaRegistro ?? this.fechaRegistro,
      observaciones: observaciones ?? this.observaciones,
    );
  }
}

