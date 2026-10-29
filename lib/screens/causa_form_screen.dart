import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import 'package:provider/provider.dart';
import '../models/pget_tab.dart';
import '../models/causa_judicial.dart';
import '../providers/abogados_provider.dart';
import '../theme/app_theme.dart';

class CausaFormScreen extends StatefulWidget {
  final PgetTab? tab;
  final CausaJudicial? causaAEditar;

  const CausaFormScreen({Key? key, this.tab, this.causaAEditar}) : super(key: key);

  @override
  State<CausaFormScreen> createState() => _CausaFormScreenState();
}

class _CausaFormScreenState extends State<CausaFormScreen> {
  final _formKey = GlobalKey<FormState>();
  final Map<int, TextEditingController> _controllers = {};
  final Map<int, String> _selectedDropdownValues = {};
  late PgetTab _tab;

  bool get isEditing => widget.causaAEditar != null;

  @override
  void initState() {
    super.initState();
    final provider = context.read<AbogadosProvider>();
    final hoy = DateFormat('dd/MM/yyyy').format(DateTime.now());

    // Si viene para editar, buscar la pestaña correspondiente
    if (widget.causaAEditar != null) {
      _tab = widget.tab ??
          provider.tabs.firstWhere(
            (t) => t.title == widget.causaAEditar!.juzgadoMunicipio,
            orElse: () => provider.currentTab,
          );
    } else {
      _tab = widget.tab ?? provider.currentTab;
    }

    // Inicializar controladores para cada columna de la pestaña seleccionada
    for (int i = 0; i < _tab.columns.length; i++) {
      final colName = _tab.columns[i].toUpperCase();
      final ctrl = TextEditingController();

      if (isEditing) {
        final c = widget.causaAEditar!;
        if (colName.contains('EXPEDIENTE') || colName.contains('INVESTIGACION')) {
          ctrl.text = c.numeroExpediente;
        } else if (colName.contains('DEMANDANTE') || colName.contains('QUERELLANTE') || colName.contains('SOLICITANTE')) {
          ctrl.text = c.demandante;
        } else if (colName.contains('DEMANDADO') || colName.contains('QUERELLADO') || colName.contains('IMPUTADO')) {
          ctrl.text = c.demandado;
        } else if (colName.contains('MOTIVO') || colName.contains('DELITO')) {
          ctrl.text = c.motivo;
        } else if (_isAbogadoField(colName)) {
          final abg = c.abogadoResponsable.isNotEmpty ? c.abogadoResponsable : (provider.abogadosActivos.isNotEmpty ? provider.abogadosActivos.first.nombre : '');
          _selectedDropdownValues[i] = abg;
          ctrl.text = abg;
        } else if (_isEstadoField(colName)) {
          final est = c.estadoActual.isNotEmpty ? c.estadoActual : 'ACTIVA';
          _selectedDropdownValues[i] = est;
          ctrl.text = est;
        } else if (colName.contains('ACTUACION') || colName.contains('OBSERVACION')) {
          ctrl.text = c.actuacionesRealizadas;
        } else if (colName.contains('FECHA')) {
          ctrl.text = c.fechaEntrada.isNotEmpty ? c.fechaEntrada : hoy;
        } else if (i == 0) {
          ctrl.text = c.numero;
        }
      } else {
        // Modo Creación
        if (i == 0 && (colName.contains('Nº') || colName.contains('N°') || colName.isEmpty)) {
          ctrl.text = (provider.currentTabRows.length + 1).toString();
        } else if (colName.contains('FECHA')) {
          ctrl.text = hoy;
        } else if (colName.contains('DEMANDANTE') && colName.contains('PROCURADUR')) {
          ctrl.text = 'PROCURADURIA GENERAL DEL ESTADO TRUJILLO';
        }

        if (_isAbogadoField(colName)) {
          if (!provider.isAdminMode && provider.abogadoSesion != null) {
            _selectedDropdownValues[i] = provider.abogadoSesion!.nombre;
            ctrl.text = provider.abogadoSesion!.nombre;
          } else if (provider.abogadosActivos.isNotEmpty) {
            _selectedDropdownValues[i] = provider.abogadosActivos.first.nombre;
            ctrl.text = provider.abogadosActivos.first.nombre;
          }
        }

        if (_isEstadoField(colName)) {
          _selectedDropdownValues[i] = 'ACTIVA';
          ctrl.text = 'ACTIVA';
        }
      }

      _controllers[i] = ctrl;
    }
  }

  @override
  void dispose() {
    for (final ctrl in _controllers.values) {
      ctrl.dispose();
    }
    super.dispose();
  }

  bool _isAbogadoField(String col) {
    return col.contains('ABG') || col.contains('RESPONSABLE');
  }

  bool _isEstadoField(String col) {
    return col.contains('ESTADO') && !col.contains('ADSCRITO');
  }

  bool _isMultilineField(String col) {
    return col.contains('ACTUACION') ||
        col.contains('OBSERVACION') ||
        col.contains('MOTIVO') ||
        col.contains('DELITO') ||
        col.contains('DESCRIPCION');
  }

  IconData _getIconForColumn(String col) {
    final c = col.toUpperCase();
    if (c.contains('Nº') || c.contains('N°') || c.contains('NUMERO')) return Icons.pin_outlined;
    if (c.contains('TRIBUNAL') || c.contains('JUZGADO') || c.contains('CORTE') || c.contains('SALA')) return Icons.gavel;
    if (c.contains('DEMANDANTE') || c.contains('QUERELLANTE') || c.contains('SOLICITANTE')) return Icons.account_balance;
    if (c.contains('DEMANDADO') || c.contains('QUERELLADO') || c.contains('IMPUTADO') || c.contains('VICTIMA') || c.contains('SOLICITADO')) return Icons.person_outline;
    if (c.contains('EXPEDIENTE') || c.contains('INVESTIGACION')) return Icons.folder_open;
    if (c.contains('ABG') || c.contains('RESPONSABLE')) return Icons.badge;
    if (c.contains('CEDULA')) return Icons.fingerprint;
    if (c.contains('FECHA')) return Icons.calendar_today;
    if (c.contains('ESTADO')) return Icons.check_circle_outline;
    if (c.contains('MONTO') || c.contains('PAGADO') || c.contains('BS.')) return Icons.attach_money;
    if (c.contains('CARGO')) return Icons.work_outline;
    return Icons.edit_note;
  }

  void _guardarFormulario() async {
    if (!_formKey.currentState!.validate()) return;

    final provider = context.read<AbogadosProvider>();
    final List<dynamic> valoresFila = [];

    for (int i = 0; i < _tab.columns.length; i++) {
      final val = _controllers[i]?.text.trim() ?? '';
      valoresFila.add(val);
    }

    bool exito = false;
    if (isEditing) {
      final rowIndex = widget.causaAEditar!.rowIndex ?? 1;
      exito = await provider.actualizarFilaCompleta(_tab, rowIndex, valoresFila);
    } else {
      exito = await provider.registrarFilaEnPestana(_tab, valoresFila);
    }

    if (mounted) {
      if (exito) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            backgroundColor: AppTheme.vinotinto,
            content: Row(
              children: [
                const Icon(Icons.check_circle, color: AppTheme.oro),
                const SizedBox(width: 10),
                Expanded(
                  child: Text(
                    isEditing
                        ? 'Causa actualizada exitosamente en Google Sheets'
                        : 'Causa guardada exitosamente en la pestaña "${_tab.title}"',
                    style: const TextStyle(fontWeight: FontWeight.bold),
                  ),
                ),
              ],
            ),
          ),
        );
        Navigator.pop(context);
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            backgroundColor: Colors.redAccent,
            content: Text('Error al guardar en Google Sheets: ${provider.errorMessage}'),
          ),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final provider = context.watch<AbogadosProvider>();

    return Scaffold(
      backgroundColor: AppTheme.fondoBlanco,
      appBar: AppBar(
        title: Text(isEditing ? 'Editar Expediente' : 'Nueva Causa Judicial'),
        bottom: const PreferredSize(
          preferredSize: Size.fromHeight(2),
          child: Divider(height: 2, color: AppTheme.oro, thickness: 2),
        ),
      ),
      body: Form(
        key: _formKey,
        child: ListView(
          padding: const EdgeInsets.all(16),
          children: [
            // Banner de la Materia / Instancia Seleccionada
            Container(
              padding: const EdgeInsets.all(14),
              decoration: BoxDecoration(
                color: AppTheme.vinotinto,
                borderRadius: BorderRadius.circular(16),
                border: Border.all(color: AppTheme.oro, width: 1.5),
                boxShadow: [
                  BoxShadow(
                    color: AppTheme.vinotinto.withOpacity(0.2),
                    blurRadius: 8,
                    offset: const Offset(0, 3),
                  ),
                ],
              ),
              child: Row(
                children: [
                  Container(
                    padding: const EdgeInsets.all(10),
                    decoration: BoxDecoration(
                      color: Colors.white,
                      shape: BoxShape.circle,
                      border: Border.all(color: AppTheme.oro, width: 1.5),
                    ),
                    child: Icon(_tab.icon, color: AppTheme.vinotinto, size: 22),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          _tab.category.toUpperCase(),
                          style: const TextStyle(
                            color: AppTheme.oro,
                            fontSize: 10.5,
                            fontWeight: FontWeight.w800,
                            letterSpacing: 0.6,
                          ),
                        ),
                        const SizedBox(height: 2),
                        Text(
                          _tab.title,
                          style: const TextStyle(
                            color: Colors.white,
                            fontSize: 15,
                            fontWeight: FontWeight.w900,
                          ),
                        ),
                        const SizedBox(height: 2),
                        Text(
                          'Formulario adaptado • ${_tab.columns.length} Columnas de Google Sheets',
                          style: const TextStyle(color: Colors.white70, fontSize: 11),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),

            const SizedBox(height: 18),

            // Campos generados dinámicamente según las columnas exactas de esta pestaña
            ...List.generate(_tab.columns.length, (index) {
              final colName = _tab.columns[index];
              final colUpper = colName.toUpperCase();
              final ctrl = _controllers[index]!;
              final icon = _getIconForColumn(colUpper);
              final isMultiline = _isMultilineField(colUpper);

              // Si es campo de selección de Abogado Responsable
              if (_isAbogadoField(colUpper)) {
                return Padding(
                  padding: const EdgeInsets.only(bottom: 14),
                  child: DropdownButtonFormField<String>(
                    value: _selectedDropdownValues[index],
                    decoration: InputDecoration(
                      labelText: '$colName *',
                      prefixIcon: Icon(icon, color: AppTheme.vinotinto),
                    ),
                    items: provider.abogadosActivos.map((a) {
                      return DropdownMenuItem(
                        value: a.nombre,
                        child: Text(
                          a.nombre,
                          style: const TextStyle(fontSize: 12, fontWeight: FontWeight.bold),
                        ),
                      );
                    }).toList(),
                    onChanged: (val) {
                      if (val != null) {
                        setState(() {
                          _selectedDropdownValues[index] = val;
                          ctrl.text = val;
                        });
                      }
                    },
                    validator: (v) => v == null || v.isEmpty ? 'Selecciona el abogado responsable' : null,
                  ),
                );
              }

              // Si es campo de Estado
              if (_isEstadoField(colUpper)) {
                return Padding(
                  padding: const EdgeInsets.only(bottom: 14),
                  child: DropdownButtonFormField<String>(
                    value: _selectedDropdownValues[index] ?? 'ACTIVA',
                    decoration: InputDecoration(
                      labelText: '$colName *',
                      prefixIcon: Icon(icon, color: AppTheme.vinotinto),
                    ),
                    items: const [
                      DropdownMenuItem(value: 'ACTIVA', child: Text('ACTIVA')),
                      DropdownMenuItem(value: 'CERRADA', child: Text('CERRADA')),
                      DropdownMenuItem(value: 'EN TRÁMITE', child: Text('EN TRÁMITE')),
                    ],
                    onChanged: (val) {
                      if (val != null) {
                        setState(() {
                          _selectedDropdownValues[index] = val;
                          ctrl.text = val;
                        });
                      }
                    },
                  ),
                );
              }

              // Campo de texto estándar o multilínea
              return Padding(
                padding: const EdgeInsets.only(bottom: 14),
                child: TextFormField(
                  controller: ctrl,
                  maxLines: isMultiline ? 3 : 1,
                  textCapitalization: TextCapitalization.sentences,
                  decoration: InputDecoration(
                    labelText: colName.isNotEmpty ? colName : 'Campo #${index + 1}',
                    prefixIcon: Icon(icon, color: AppTheme.vinotinto),
                    hintText: 'Ingresa $colName',
                  ),
                  validator: (val) {
                    if (index == 0) return null; // Correlativo opcional
                    if (colUpper.contains('EXPEDIENTE') || colUpper.contains('INVESTIGACION')) {
                      if (val == null || val.trim().isEmpty) {
                        return 'El Nº de Expediente es obligatorio';
                      }
                    }
                    return null;
                  },
                ),
              );
            }),

            const SizedBox(height: 24),

            // Botón de Enviar a Google Sheets
            ElevatedButton(
              onPressed: provider.isSaving ? null : _guardarFormulario,
              style: ElevatedButton.styleFrom(
                padding: const EdgeInsets.symmetric(vertical: 16),
              ),
              child: provider.isSaving
                  ? const Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        SizedBox(
                          width: 20,
                          height: 20,
                          child: CircularProgressIndicator(color: AppTheme.oro, strokeWidth: 2),
                        ),
                        SizedBox(width: 12),
                        Text('Sincronizando con Google Sheets...'),
                      ],
                    )
                  : Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        const Icon(Icons.cloud_upload, color: AppTheme.oro),
                        const SizedBox(width: 8),
                        Text(
                          isEditing ? 'Guardar Cambios en Google Sheets' : 'Enviar Causa a Google Sheets',
                          style: const TextStyle(fontSize: 14, fontWeight: FontWeight.bold),
                        ),
                      ],
                    ),
            ),
            const SizedBox(height: 30),
          ],
        ),
      ),
    );
  }
}
