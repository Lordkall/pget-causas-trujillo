class AbogadoPGET {
  final String id;
  final String nombre;
  final String cedula;
  final String cargo;
  final String adscrito;
  final String telefono;
  final String correo;
  final String clave;
  final String rol; // 'admin' | 'abogado'
  final bool activo; // Si es false, se desactiva de asignaciones nuevas pero se CONSERVA todo su historial

  AbogadoPGET({
    required this.id,
    required this.nombre,
    required this.cedula,
    this.cargo = 'Abogado Adscrito',
    this.adscrito = 'Procuraduría General del Estado Trujillo',
    this.telefono = '',
    this.correo = '',
    this.clave = 'Pget2026*',
    this.rol = 'abogado',
    this.activo = true,
  });

  bool get esAdmin => rol == 'admin';

  AbogadoPGET copyWith({
    String? id,
    String? nombre,
    String? cedula,
    String? cargo,
    String? adscrito,
    String? telefono,
    String? correo,
    String? clave,
    String? rol,
    bool? activo,
  }) {
    return AbogadoPGET(
      id: id ?? this.id,
      nombre: nombre ?? this.nombre,
      cedula: cedula ?? this.cedula,
      cargo: cargo ?? this.cargo,
      adscrito: adscrito ?? this.adscrito,
      telefono: telefono ?? this.telefono,
      correo: correo ?? this.correo,
      clave: clave ?? this.clave,
      rol: rol ?? this.rol,
      activo: activo ?? this.activo,
    );
  }

  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'nombre': nombre,
      'cedula': cedula,
      'cargo': cargo,
      'adscrito': adscrito,
      'telefono': telefono,
      'correo': correo,
      'clave': clave,
      'rol': rol,
      'activo': activo,
    };
  }

  factory AbogadoPGET.fromMap(Map<String, dynamic> map) {
    return AbogadoPGET(
      id: map['id'] ?? '',
      nombre: map['nombre'] ?? '',
      cedula: map['cedula'] ?? '',
      cargo: map['cargo'] ?? 'Abogado Adscrito',
      adscrito: map['adscrito'] ?? 'Procuraduría General del Estado Trujillo',
      telefono: map['telefono'] ?? '',
      correo: map['correo'] ?? '',
      clave: map['clave'] ?? 'Pget2026*',
      rol: map['rol'] ?? 'abogado',
      activo: map['activo'] ?? true,
    );
  }
      cedula: map['cedula'] ?? '',
      cargo: map['cargo'] ?? 'Abogado Adscrito',
      adscrito: map['adscrito'] ?? 'PGET',
      telefono: map['telefono'] ?? '',
      correo: map['correo'] ?? '',
      activo: map['activo'] ?? true,
    );
  }
}
