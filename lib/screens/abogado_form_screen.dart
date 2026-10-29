import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../models/abogado.dart';
import '../providers/abogados_provider.dart';
import '../theme/app_theme.dart';

class AbogadoFormScreen extends StatefulWidget {
  final Abogado? abogadoAEditar;

  const AbogadoFormScreen({Key? key, this.abogadoAEditar}) : super(key: key);

  @override
  State<AbogadoFormScreen> createState() => _AbogadoFormScreenState();
}

class _AbogadoFormScreenState extends State<AbogadoFormScreen> {
  final _formKey = GlobalKey<FormState>();

  late String _id;
  final TextEditingController _nombreCtrl = TextEditingController();
  final TextEditingController _identificacionCtrl = TextEditingController();
  final TextEditingController _colegiaturaCtrl = TextEditingController();
  final TextEditingController _telefonoCtrl = TextEditingController();
  final TextEditingController _correoCtrl = TextEditingController();
  final TextEditingController _despachoCtrl = TextEditingController();
  final TextEditingController _ciudadCtrl = TextEditingController();
  final TextEditingController _observacionesCtrl = TextEditingController();

  String _especialidadSeleccionada = 'Derecho Penal';
  String _estadoSeleccionado = 'Activo';

  final List<String> _especialidades = [
    'Derecho Penal',
    'Derecho Civil',
    'Derecho Laboral',
    'Derecho Corporativo',
    'Derecho Familiar',
    'Derecho Tributario',
    'Derecho Administrativo',
    'Derecho Constitucional',
    'General',
  ];

  final List<String> _estados = [
    'Activo',
    'En Trámite',
    'Inactivo',
    'Suspendido',
  ];

  @override
  void initState() {
    super.initState();
    final provider = context.read<AbogadosProvider>();

    if (widget.abogadoAEditar != null) {
      final a = widget.abogadoAEditar!;
      _id = a.id;
      _nombreCtrl.text = a.nombre;
      _identificacionCtrl.text = a.identificacion;
      _colegiaturaCtrl.text = a.colegiatura;
      _telefonoCtrl.text = a.telefono;
      _correoCtrl.text = a.correo;
      _despachoCtrl.text = a.despacho;
      _ciudadCtrl.text = a.ciudad;
      _observacionesCtrl.text = a.observaciones;
      _especialidadSeleccionada = a.especialidad;
      _estadoSeleccionado = a.estado;
    } else {
      _id = provider.generarSiguienteId();
    }
  }

  @override
  void dispose() {
    _nombreCtrl.dispose();
    _identificacionCtrl.dispose();
    _colegiaturaCtrl.dispose();
    _telefonoCtrl.dispose();
    _correoCtrl.dispose();
    _despachoCtrl.dispose();
    _ciudadCtrl.dispose();
    _observacionesCtrl.dispose();
    super.dispose();
  }

  void _guardar() async {
    if (!_formKey.currentState!.validate()) return;

    final provider = context.read<AbogadosProvider>();
    final nuevoAbogado = Abogado(
      id: _id,
      nombre: _nombreCtrl.text.trim(),
      identificacion: _identificacionCtrl.text.trim(),
      colegiatura: _colegiaturaCtrl.text.trim(),
      especialidad: _especialidadSeleccionada,
      telefono: _telefonoCtrl.text.trim(),
      correo: _correoCtrl.text.trim(),
      estado: _estadoSeleccionado,
      despacho: _despachoCtrl.text.trim(),
      ciudad: _ciudadCtrl.text.trim(),
      observaciones: _observacionesCtrl.text.trim(),
      fechaRegistro: widget.abogadoAEditar?.fechaRegistro ?? DateTime.now(),
    );

    bool exito;
    if (widget.abogadoAEditar != null) {
      exito = await provider.actualizarAbogado(nuevoAbogado);
    } else {
      exito = await provider.registrarAbogado(nuevoAbogado);
    }

    if (mounted) {
      if (exito) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            backgroundColor: AppTheme.statusActive,
            content: Row(
              children: [
                const Icon(Icons.check_circle, color: Colors.white),
                const SizedBox(width: 10),
                Text(
                  widget.abogadoAEditar != null
                      ? 'Abogado actualizado en Google Sheets'
                      : 'Abogado registrado exitosamente',
                  style: const TextStyle(fontWeight: FontWeight.w600),
                ),
              ],
            ),
          ),
        );
        Navigator.pop(context);
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            backgroundColor: AppTheme.statusInactive,
            content: Text('Error: ${provider.errorMessage ?? "No se pudo guardar"}'),
          ),
        );
      }
    }
  }

  Widget _buildSectionHeader(String title, IconData icon) {
    return Padding(
      padding: const EdgeInsets.only(top: 20, bottom: 12),
      child: Row(
        children: [
          Icon(icon, size: 20, color: AppTheme.primaryNavy),
          const SizedBox(width: 8),
          Text(
            title,
            style: const TextStyle(
              fontSize: 16,
              fontWeight: FontWeight.w700,
              color: AppTheme.primaryNavy,
              letterSpacing: 0.2,
            ),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final isEditing = widget.abogadoAEditar != null;
    final isSaving = context.watch<AbogadosProvider>().isSaving;

    return Scaffold(
      backgroundColor: AppTheme.backgroundLight,
      appBar: AppBar(
        title: Text(isEditing ? 'Editar Abogado' : 'Nuevo Registro'),
      ),
      body: Form(
        key: _formKey,
        child: ListView(
          padding: const EdgeInsets.all(20),
          children: [
            // Banner de ID Folio
            Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                gradient: const LinearGradient(
                  colors: [AppTheme.primaryNavy, AppTheme.secondaryNavy],
                  begin: Alignment.topLeft,
                  end: Alignment.bottomRight,
                ),
                borderRadius: BorderRadius.circular(16),
                boxShadow: [
                  BoxShadow(
                    color: AppTheme.primaryNavy.withOpacity(0.15),
                    blurRadius: 10,
                    offset: const Offset(0, 4),
                  ),
                ],
              ),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text(
                        'FOLIO DE REGISTRO',
                        style: TextStyle(
                          color: Color(0xFF94A3B8),
                          fontSize: 11,
                          fontWeight: FontWeight.w600,
                          letterSpacing: 1,
                        ),
                      ),
                      const SizedBox(height: 4),
                      Text(
                        _id,
                        style: const TextStyle(
                          color: AppTheme.accentGold,
                          fontSize: 22,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ],
                  ),
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                    decoration: BoxDecoration(
                      color: Colors.white.withOpacity(0.12),
                      borderRadius: BorderRadius.circular(20),
                    ),
                    child: const Row(
                      children: [
                        Icon(Icons.cloud_upload_outlined, color: Colors.white, size: 16),
                        SizedBox(width: 6),
                        Text(
                          'Google Sheets',
                          style: TextStyle(color: Colors.white, fontSize: 12, fontWeight: FontWeight.w600),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),

            // SECCIÓN 1: DATOS PERSONALES
            _buildSectionHeader('Datos Personales', Icons.person_outline),

            TextFormField(
              controller: _nombreCtrl,
              decoration: const InputDecoration(
                labelText: 'Nombre y Apellidos completos *',
                hintText: 'Ej. Dra. María Fernanda Gómez',
                prefixIcon: Icon(Icons.badge_outlined),
              ),
              validator: (val) {
                if (val == null || val.trim().isEmpty) return 'Por favor ingresa el nombre';
                return null;
              },
            ),
            const SizedBox(height: 14),

            Row(
              children: [
                Expanded(
                  child: TextFormField(
                    controller: _identificacionCtrl,
                    decoration: const InputDecoration(
                      labelText: 'Cédula / DNI *',
                      hintText: 'Ej. 1098452310',
                      prefixIcon: Icon(Icons.fingerprint),
                    ),
                    validator: (val) {
                      if (val == null || val.trim().isEmpty) return 'Requerido';
                      return null;
                    },
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: TextFormField(
                    controller: _telefonoCtrl,
                    keyboardType: TextInputType.phone,
                    decoration: const InputDecoration(
                      labelText: 'Teléfono / WhatsApp *',
                      hintText: 'Ej. +57 310 1234567',
                      prefixIcon: Icon(Icons.phone_outlined),
                    ),
                    validator: (val) {
                      if (val == null || val.trim().isEmpty) return 'Requerido';
                      return null;
                    },
                  ),
                ),
              ],
            ),
            const SizedBox(height: 14),

            TextFormField(
              controller: _correoCtrl,
              keyboardType: TextInputType.emailAddress,
              decoration: const InputDecoration(
                labelText: 'Correo Electrónico *',
                hintText: 'abogado@ejemplo.com',
                prefixIcon: Icon(Icons.email_outlined),
              ),
              validator: (val) {
                if (val == null || val.trim().isEmpty) return 'Por favor ingresa el correo';
                if (!val.contains('@') || !val.contains('.')) return 'Correo no válido';
                return null;
              },
            ),

            // SECCIÓN 2: INFORMACIÓN JURÍDICA
            _buildSectionHeader('Credenciales Jurídicas', Icons.gavel_outlined),

            Row(
              children: [
                Expanded(
                  child: TextFormField(
                    controller: _colegiaturaCtrl,
                    decoration: const InputDecoration(
                      labelText: 'N° Colegiatura / Matrícula *',
                      hintText: 'Ej. CAL-48902',
                      prefixIcon: Icon(Icons.verified_outlined),
                    ),
                    validator: (val) {
                      if (val == null || val.trim().isEmpty) return 'Requerido';
                      return null;
                    },
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: DropdownButtonFormField<String>(
                    value: _especialidadSeleccionada,
                    decoration: const InputDecoration(
                      labelText: 'Especialidad',
                      prefixIcon: Icon(Icons.category_outlined),
                    ),
                    items: _especialidades.map((esp) {
                      return DropdownMenuItem(value: esp, child: Text(esp, style: const TextStyle(fontSize: 13)));
                    }).toList(),
                    onChanged: (val) {
                      if (val != null) {
                        setState(() => _especialidadSeleccionada = val);
                      }
                    },
                  ),
                ),
              ],
            ),
            const SizedBox(height: 14),

            Row(
              children: [
                Expanded(
                  child: TextFormField(
                    controller: _despachoCtrl,
                    decoration: const InputDecoration(
                      labelText: 'Despacho / Bufete / Firma',
                      hintText: 'Ej. Bufete Gómez & Cía',
                      prefixIcon: Icon(Icons.business_outlined),
                    ),
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: TextFormField(
                    controller: _ciudadCtrl,
                    decoration: const InputDecoration(
                      labelText: 'Ciudad / Jurisdicción',
                      hintText: 'Ej. Bogotá D.C.',
                      prefixIcon: Icon(Icons.location_city_outlined),
                    ),
                  ),
                ),
              ],
            ),

            // SECCIÓN 3: ESTADO Y OBSERVACIONES
            _buildSectionHeader('Estado y Observaciones', Icons.rule_folder_outlined),

            // Selector de Estado
            Wrap(
              spacing: 8,
              children: _estados.map((est) {
                final isSelected = _estadoSeleccionado == est;
                return ChoiceChip(
                  label: Text(est),
                  selected: isSelected,
                  selectedColor: AppTheme.accentGold,
                  labelStyle: TextStyle(
                    color: isSelected ? AppTheme.primaryNavy : AppTheme.textDark,
                    fontWeight: isSelected ? FontWeight.bold : FontWeight.w500,
                  ),
                  onSelected: (_) => setState(() => _estadoSeleccionado = est),
                );
              }).toList(),
            ),
            const SizedBox(height: 14),

            TextFormField(
              controller: _observacionesCtrl,
              maxLines: 3,
              decoration: const InputDecoration(
                labelText: 'Observaciones / Casos Destacados',
                hintText: 'Notas adicionales sobre la experiencia, casos activos, etc.',
                alignLabelWithHint: true,
              ),
            ),

            const SizedBox(height: 28),

            // Botón de Guardado
            ElevatedButton(
              onPressed: isSaving ? null : _guardar,
              child: isSaving
                  ? const Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        SizedBox(
                          width: 20,
                          height: 20,
                          child: CircularProgressIndicator(color: Colors.white, strokeWidth: 2.5),
                        ),
                        SizedBox(width: 12),
                        Text('Sincronizando con Google Sheets...'),
                      ],
                    )
                  : Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        const Icon(Icons.save_outlined),
                        const SizedBox(width: 10),
                        Text(
                          isEditing ? 'Actualizar Información' : 'Registrar en Google Sheets',
                          style: const TextStyle(fontWeight: FontWeight.bold),
                        ),
                      ],
                    ),
            ),
            const SizedBox(height: 20),
          ],
        ),
      ),
    );
  }
}

