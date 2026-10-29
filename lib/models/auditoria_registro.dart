import 'package:intl/intl.dart';

class AuditoriaRegistro {
  final String id;
  final DateTime fechaHora;
  final String usuario;
  final String accion; // CREACIÓN, MODIFICACIÓN, NUEVA ACTUACIÓN, DESACTIVACIÓN
  final String expediente;
  final String pestana;
  final String detalle;

  AuditoriaRegistro({
    required this.id,
    DateTime? fechaHora,
    required this.usuario,
    required this.accion,
    required this.expediente,
    required this.pestana,
    required this.detalle,
  }) : fechaHora = fechaHora ?? DateTime.now();

  String get fechaFormateada {
    return DateFormat('dd/MM/yyyy, hh:mm a').format(fechaHora);
  }

  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'fechaHora': fechaHora.toIso8601String(),
      'usuario': usuario,
      'accion': accion,
      'expediente': expediente,
      'pestana': pestana,
      'detalle': detalle,
    };
  }
}

