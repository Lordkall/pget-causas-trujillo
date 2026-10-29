import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../models/causa_judicial.dart';
import '../providers/abogados_provider.dart';
import '../theme/app_theme.dart';
import 'causa_form_screen.dart';

class CausaDetailScreen extends StatefulWidget {
  final CausaJudicial causa;

  const CausaDetailScreen({Key? key, required this.causa}) : super(key: key);

  @override
  State<CausaDetailScreen> createState() => _CausaDetailScreenState();
}

class _CausaDetailScreenState extends State<CausaDetailScreen> {
  late CausaJudicial _causa;

  @override
  void initState() {
    super.initState();
    _causa = widget.causa;
  }

  void _abrirModalNuevaActuacion(BuildContext context) {
    final actuacionCtrl = TextEditingController();
    String nuevoEstado = _causa.estadoActual;

    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.transparent,
      builder: (ctx) => StatefulBuilder(
        builder: (ctx, setModalState) => Container(
          padding: EdgeInsets.only(
            top: 20,
            left: 20,
            right: 20,
            bottom: MediaQuery.of(ctx).viewInsets.bottom + 20,
          ),
          decoration: const BoxDecoration(
            color: Colors.white,
            borderRadius: BorderRadius.vertical(top: Radius.circular(24)),
            border: Border(top: BorderSide(color: AppTheme.oro, width: 2.5)),
          ),
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
                        padding: const EdgeInsets.all(7),
                        decoration: BoxDecoration(
                          color: AppTheme.vinotinto,
                          borderRadius: BorderRadius.circular(8),
                          border: Border.all(color: AppTheme.oro),
                        ),
                        child: const Icon(Icons.edit_note, color: AppTheme.oro, size: 20),
                      ),
                      const SizedBox(width: 10),
                      const Text(
                        'Nueva Actuación Procesal',
                        style: TextStyle(
                          fontSize: 16,
                          fontWeight: FontWeight.bold,
                          color: AppTheme.vinotinto,
                        ),
                      ),
                    ],
                  ),
                  IconButton(
                    icon: const Icon(Icons.close),
                    onPressed: () => Navigator.pop(ctx),
                  ),
                ],
              ),
              const SizedBox(height: 6),
              Text(
                'Expediente Nº ${_causa.numeroExpediente}',
                style: const TextStyle(fontSize: 12, color: AppTheme.textoSecundario, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 14),

              TextField(
                controller: actuacionCtrl,
                maxLines: 4,
                textCapitalization: TextCapitalization.sentences,
                decoration: const InputDecoration(
                  labelText: 'Descripción de la Actuación Judicial *',
                  hintText: 'Ej. Se consignó escrito de contestación ante el tribunal...',
                  alignLabelWithHint: true,
                ),
              ),
              const SizedBox(height: 14),

              // Selector rápido de nuevo estado
              const Text(
                'Estado resultante:',
                style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: AppTheme.textoPrincipal),
              ),
              const SizedBox(height: 6),
              Wrap(
                spacing: 8,
                children: ['ACTIVA', 'CERRADA', 'EN TRÁMITE'].map((est) {
                  final isSel = nuevoEstado.toUpperCase().contains(est);
                  return ChoiceChip(
                    label: Text(est),
                    selected: isSel,
                    selectedColor: AppTheme.vinotinto,
                    labelStyle: TextStyle(
                      color: isSel ? Colors.white : AppTheme.textoPrincipal,
                      fontWeight: FontWeight.bold,
                      fontSize: 11,
                    ),
                    side: BorderSide(color: isSel ? AppTheme.oro : AppTheme.oroBordeSuave),
                    onSelected: (_) => setModalState(() => nuevoEstado = est),
                  );
                }).toList(),
              ),
              const SizedBox(height: 18),

              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  onPressed: () async {
                    if (actuacionCtrl.text.trim().isEmpty) return;

                    final provider = context.read<AbogadosProvider>();
                    Navigator.pop(ctx);

                    final exito = await provider.registrarNuevaActuacion(
                      causa: _causa,
                      nuevaActuacion: actuacionCtrl.text.trim(),
                      nuevoEstado: nuevoEstado,
                    );

                    if (mounted && exito) {
                      setState(() {
                        // Actualizar vista local
                        final idx = provider.causas.indexWhere((c) => c.numeroExpediente == _causa.numeroExpediente);
                        if (idx != -1) {
                          _causa = provider.causas[idx];
                        }
                      });

                      ScaffoldMessenger.of(context).showSnackBar(
                        const SnackBar(
                          backgroundColor: AppTheme.vinotinto,
                          content: Row(
                            children: [
                              Icon(Icons.check_circle, color: AppTheme.oro),
                              SizedBox(width: 10),
                              Text('Actuación enviada y registrada en Google Sheets'),
                            ],
                          ),
                        ),
                      );
                    }
                  },
                  child: const Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Icon(Icons.cloud_upload_outlined, color: AppTheme.oro),
                      SizedBox(width: 8),
                      Text('Guardar en Google Sheets'),
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

  void _confirmarEliminarCausa(BuildContext context) {
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(16),
          side: const BorderSide(color: AppTheme.oroBorde, width: 1.5),
        ),
        title: Row(
          children: [
            Container(
              padding: const EdgeInsets.all(6),
              decoration: BoxDecoration(
                color: Colors.red.shade50,
                borderRadius: BorderRadius.circular(8),
              ),
              child: const Icon(Icons.delete_forever, color: Colors.red, size: 22),
            ),
            const SizedBox(width: 10),
            const Text('Eliminar Causa', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
          ],
        ),
        content: Text(
          '¿Estás seguro de que deseas eliminar la causa del Expediente Nº ${_causa.numeroExpediente}?\n\nEsta acción quedará registrada en el Registro de Auditoría del Sistema.',
          style: const TextStyle(fontSize: 13, height: 1.4),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(ctx),
            child: const Text('Cancelar', style: TextStyle(color: AppTheme.textoSecundario)),
          ),
          ElevatedButton(
            style: ElevatedButton.styleFrom(backgroundColor: Colors.red.shade800),
            onPressed: () async {
              Navigator.pop(ctx);
              final provider = context.read<AbogadosProvider>();
              final exito = await provider.eliminarCausa(_causa);
              if (mounted) {
                if (exito) {
                  ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(
                      backgroundColor: AppTheme.vinotinto,
                      content: Text('Causa con Expediente ${_causa.numeroExpediente} eliminada del sistema.'),
                    ),
                  );
                  Navigator.pop(context); // Volver al home
                } else {
                  ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(
                      backgroundColor: Colors.redAccent,
                      content: Text('Error al eliminar la causa: ${provider.errorMessage}'),
                    ),
                  );
                }
              }
            },
            child: const Text('Sí, Eliminar', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
          ),
        ],
      ),
    );
  }

  Widget _buildCard({required String title, required IconData icon, required List<Widget> children}) {
    return Container(
      margin: const EdgeInsets.only(bottom: 14),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: AppTheme.oroBorde, width: 1.2),
        boxShadow: [
          BoxShadow(
            color: AppTheme.vinotinto.withOpacity(0.04),
            blurRadius: 8,
            offset: const Offset(0, 3),
          ),
        ],
      ),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(icon, color: AppTheme.vinotinto, size: 18),
                const SizedBox(width: 8),
                Text(
                  title,
                  style: const TextStyle(
                    fontSize: 14,
                    fontWeight: FontWeight.bold,
                    color: AppTheme.vinotinto,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 12),
            const Divider(height: 1, color: AppTheme.bordeDivisor),
            const SizedBox(height: 12),
            ...children,
          ],
        ),
      ),
    );
  }

  Widget _buildRowItem(String label, String value) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 8),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          SizedBox(
            width: 130,
            child: Text(
              label,
              style: const TextStyle(fontSize: 12, color: AppTheme.textoSecundario, fontWeight: FontWeight.w600),
            ),
          ),
          Expanded(
            child: Text(
              value.isNotEmpty ? value : 'No especificado',
              style: const TextStyle(fontSize: 13, color: AppTheme.textoPrincipal, fontWeight: FontWeight.bold),
            ),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppTheme.fondoBlanco,
      appBar: AppBar(
        title: Text('Expediente: ${_causa.numeroExpediente}'),
        actions: [
          IconButton(
            icon: const Icon(Icons.edit_outlined),
            tooltip: 'Editar causa completa',
            onPressed: () async {
              await Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (_) => CausaFormScreen(causaAEditar: _causa),
                ),
              );
              final provider = context.read<AbogadosProvider>();
              final idx = provider.causas.indexWhere((c) => c.numeroExpediente == _causa.numeroExpediente);
              if (idx != -1) {
                setState(() => _causa = provider.causas[idx]);
              }
            },
          ),
          IconButton(
            icon: const Icon(Icons.delete_outline, color: Colors.white),
            tooltip: 'Eliminar causa',
            onPressed: () => _confirmarEliminarCausa(context),
          ),
        ],
        bottom: const PreferredSize(
          preferredSize: Size.fromHeight(2),
          child: Divider(height: 2, color: AppTheme.oro, thickness: 2),
        ),
      ),
      bottomNavigationBar: Container(
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          color: Colors.white,
          border: const Border(top: BorderSide(color: AppTheme.oroBorde, width: 1.5)),
          boxShadow: [
            BoxShadow(
              color: AppTheme.vinotinto.withOpacity(0.08),
              blurRadius: 10,
              offset: const Offset(0, -3),
            ),
          ],
        ),
        child: ElevatedButton(
          style: ElevatedButton.styleFrom(
            backgroundColor: AppTheme.vinotinto,
            padding: const EdgeInsets.symmetric(vertical: 14),
          ),
          onPressed: () => _abrirModalNuevaActuacion(context),
          child: const Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(Icons.add_task, color: AppTheme.oro),
              SizedBox(width: 10),
              Text(
                'Registrar Nueva Actuación Procesal',
                style: TextStyle(fontWeight: FontWeight.bold, fontSize: 14),
              ),
            ],
          ),
        ),
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          // Banner Superior Causa
          Container(
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: AppTheme.vinotinto,
              borderRadius: BorderRadius.circular(16),
              border: Border.all(color: AppTheme.oro, width: 1.5),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Text(
                      'CAUSA Nº ${_causa.numero}',
                      style: const TextStyle(color: AppTheme.oro, fontSize: 12, fontWeight: FontWeight.bold),
                    ),
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 3),
                      decoration: BoxDecoration(
                        color: Colors.white,
                        borderRadius: BorderRadius.circular(12),
                        border: Border.all(color: AppTheme.oro, width: 1),
                      ),
                      child: Text(
                        _causa.estadoActual,
                        style: const TextStyle(color: AppTheme.vinotinto, fontWeight: FontWeight.bold, fontSize: 11),
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 8),
                Text(
                  _causa.motivo,
                  style: const TextStyle(color: Colors.white, fontSize: 17, fontWeight: FontWeight.bold),
                ),
              ],
            ),
          ),

          const SizedBox(height: 14),

          // Tarjeta: Partes y Juzgado
          _buildCard(
            title: 'Datos del Juzgado y las Partes',
            icon: Icons.account_balance,
            children: [
              _buildRowItem('Tribunal / Sede:', _causa.juzgadoMunicipio),
              _buildRowItem('N° Juzgado:', _causa.numeroJuzgado),
              _buildRowItem('Demandante:', _causa.demandante),
              _buildRowItem('Demandado:', _causa.demandado),
              _buildRowItem('Fecha Entrada:', _causa.fechaEntrada),
            ],
          ),

          // Tarjeta: Abogado Responsable
          _buildCard(
            title: 'Abogado(a) PGET Asignado',
            icon: Icons.badge,
            children: [
              _buildRowItem('Nombre:', _causa.abogadoResponsable),
              _buildRowItem('Cédula:', _causa.cedula),
              _buildRowItem('Cargo:', _causa.cargo),
              _buildRowItem('Adscripción:', _causa.adscrito),
            ],
          ),

          // Tarjeta: Historial Completo de Actuaciones Realizadas
          _buildCard(
            title: 'Historial de Actuaciones Procesales',
            icon: Icons.history_edu,
            children: [
              Container(
                width: double.infinity,
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: AppTheme.fondoBlanco,
                  borderRadius: BorderRadius.circular(10),
                  border: Border.all(color: AppTheme.oroBordeSuave),
                ),
                child: Text(
                  _causa.actuacionesRealizadas.isNotEmpty
                      ? _causa.actuacionesRealizadas
                      : 'No hay actuaciones registradas aún. Pulsa el botón inferior para añadir la primera actuación procesal.',
                  style: const TextStyle(
                    fontSize: 12.5,
                    color: AppTheme.textoPrincipal,
                    height: 1.45,
                  ),
                ),
              ),
            ],
          ),

          if (_causa.observaciones.isNotEmpty)
            _buildCard(
              title: 'Observaciones Adicionales',
              icon: Icons.notes,
              children: [
                Text(
                  _causa.observaciones,
                  style: const TextStyle(fontSize: 13, color: AppTheme.textoPrincipal),
                ),
              ],
            ),
        ],
      ),
    );
  }
}

