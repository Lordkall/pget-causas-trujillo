import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../models/abogado_pget.dart';
import '../providers/abogados_provider.dart';
import '../theme/app_theme.dart';

class AbogadosAdminModal extends StatefulWidget {
  final AbogadoPGET? abogadoAEditar;

  const AbogadosAdminModal({Key? key, this.abogadoAEditar}) : super(key: key);

  @override
  State<AbogadosAdminModal> createState() => _AbogadosAdminModalState();
}

class _AbogadosAdminModalState extends State<AbogadosAdminModal> {
  final _formKey = GlobalKey<FormState>();
  late TextEditingController _nombreCtrl;
  late TextEditingController _cedulaCtrl;
  late TextEditingController _cargoCtrl;
  late TextEditingController _adscritoCtrl;
  late TextEditingController _telefonoCtrl;
  late TextEditingController _correoCtrl;

  @override
  void initState() {
    super.initState();
    final a = widget.abogadoAEditar;
    _nombreCtrl = TextEditingController(text: a?.nombre ?? '');
    _cedulaCtrl = TextEditingController(text: a?.cedula ?? '');
    _cargoCtrl = TextEditingController(text: a?.cargo ?? 'Abogado Adscrito');
    _adscritoCtrl = TextEditingController(text: a?.adscrito ?? 'Procuraduría General del Estado Trujillo');
    _telefonoCtrl = TextEditingController(text: a?.telefono ?? '');
    _correoCtrl = TextEditingController(text: a?.correo ?? '');
  }

  @override
  void dispose() {
    _nombreCtrl.dispose();
    _cedulaCtrl.dispose();
    _cargoCtrl.dispose();
    _adscritoCtrl.dispose();
    _telefonoCtrl.dispose();
    _correoCtrl.dispose();
    super.dispose();
  }

  void _guardarAbogado() {
    if (!_formKey.currentState!.validate()) return;

    final provider = context.read<AbogadosProvider>();
    final isEditing = widget.abogadoAEditar != null;

    final abogado = AbogadoPGET(
      id: isEditing ? widget.abogadoAEditar!.id : 'ABG-${provider.abogados.length + 1}',
      nombre: _nombreCtrl.text.trim().toUpperCase(),
      cedula: _cedulaCtrl.text.trim(),
      cargo: _cargoCtrl.text.trim(),
      adscrito: _adscritoCtrl.text.trim(),
      telefono: _telefonoCtrl.text.trim(),
      correo: _correoCtrl.text.trim(),
      activo: isEditing ? widget.abogadoAEditar!.activo : true,
    );

    if (isEditing) {
      provider.actualizarAbogado(abogado);
    } else {
      provider.agregarAbogado(abogado);
    }

    Navigator.pop(context);

    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        backgroundColor: AppTheme.vinotinto,
        content: Row(
          children: [
            const Icon(Icons.check_circle, color: AppTheme.oro),
            const SizedBox(width: 10),
            Text(isEditing
                ? 'Datos del abogado(a) ${abogado.nombre} actualizados'
                : 'Abogado(a) ${abogado.nombre} añadido a la nómina PGET'),
          ],
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final isEditing = widget.abogadoAEditar != null;

    return Container(
      padding: EdgeInsets.only(
        top: 20,
        left: 20,
        right: 20,
        bottom: MediaQuery.of(context).viewInsets.bottom + 20,
      ),
      decoration: const BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.vertical(top: Radius.circular(24)),
        border: Border(top: BorderSide(color: AppTheme.oro, width: 2.5)),
      ),
      child: Form(
        key: _formKey,
        child: SingleChildScrollView(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Row(
                    children: [
                      Container(
                        padding: const EdgeInsets.all(8),
                        decoration: BoxDecoration(
                          color: AppTheme.vinotinto,
                          borderRadius: BorderRadius.circular(10),
                          border: Border.all(color: AppTheme.oro, width: 1),
                        ),
                        child: Icon(
                          isEditing ? Icons.edit : Icons.person_add_alt_1,
                          color: AppTheme.oro,
                          size: 20,
                        ),
                      ),
                      const SizedBox(width: 10),
                      Text(
                        isEditing ? 'Editar Datos del Abogado' : 'Añadir Abogado a PGET',
                        style: const TextStyle(
                          fontSize: 16,
                          fontWeight: FontWeight.bold,
                          color: AppTheme.vinotinto,
                        ),
                      ),
                    ],
                  ),
                  IconButton(
                    icon: const Icon(Icons.close, color: AppTheme.textoSecundario),
                    onPressed: () => Navigator.pop(context),
                  ),
                ],
              ),
              const SizedBox(height: 6),
              Text(
                isEditing
                    ? 'Actualiza los datos del profesional para asignaciones en las 17 materias jurídicas.'
                    : 'Permite que el abogado registrado pueda ser asignado a causas y acceda al formulario para actualizar Google Sheets.',
                style: const TextStyle(fontSize: 12, color: AppTheme.textoSecundario),
              ),
              const SizedBox(height: 16),

              TextFormField(
                controller: _nombreCtrl,
                textCapitalization: TextCapitalization.characters,
                decoration: const InputDecoration(
                  labelText: 'Nombre y Apellido del Abogado *',
                  hintText: 'EJ. SAMANTHA POLANCO',
                  prefixIcon: Icon(Icons.badge),
                ),
                validator: (val) => val == null || val.trim().isEmpty ? 'Requerido' : null,
              ),
              const SizedBox(height: 12),

              Row(
                children: [
                  Expanded(
                    child: TextFormField(
                      controller: _cedulaCtrl,
                      decoration: const InputDecoration(
                        labelText: 'Cédula de Identidad *',
                        hintText: 'Ej. 14.929.335',
                        prefixIcon: Icon(Icons.fingerprint),
                      ),
                      validator: (val) => val == null || val.trim().isEmpty ? 'Requerido' : null,
                    ),
                  ),
                  const SizedBox(width: 10),
                  Expanded(
                    child: TextFormField(
                      controller: _cargoCtrl,
                      decoration: const InputDecoration(
                        labelText: 'Cargo Institucional',
                        hintText: 'Ej. Apoderado Judicial',
                        prefixIcon: Icon(Icons.work_outline),
                      ),
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 12),

              TextFormField(
                controller: _adscritoCtrl,
                decoration: const InputDecoration(
                  labelText: 'Adscrito a la Dirección / Organismo',
                  hintText: 'Ej. Procuraduría General / Corpoturismo / Dinfra',
                  prefixIcon: Icon(Icons.account_balance_outlined),
                ),
              ),
              const SizedBox(height: 12),

              Row(
                children: [
                  Expanded(
                    child: TextFormField(
                      controller: _telefonoCtrl,
                      keyboardType: TextInputType.phone,
                      decoration: const InputDecoration(
                        labelText: 'Teléfono / WhatsApp',
                        hintText: '+58 414 1234567',
                        prefixIcon: Icon(Icons.phone_outlined),
                      ),
                    ),
                  ),
                  const SizedBox(width: 10),
                  Expanded(
                    child: TextFormField(
                      controller: _correoCtrl,
                      keyboardType: TextInputType.emailAddress,
                      decoration: const InputDecoration(
                        labelText: 'Correo Electrónico',
                        hintText: 'abogado@pget.gob.ve',
                        prefixIcon: Icon(Icons.email_outlined),
                      ),
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 20),

              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  onPressed: _guardarAbogado,
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      const Icon(Icons.check_circle_outline, color: AppTheme.oro),
                      const SizedBox(width: 8),
                      Text(isEditing ? 'Guardar Cambios' : 'Registrar Abogado en Nómina'),
                    ],
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
