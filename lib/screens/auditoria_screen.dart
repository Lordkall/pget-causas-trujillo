import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/abogados_provider.dart';
import '../theme/app_theme.dart';

class AuditoriaScreen extends StatelessWidget {
  const AuditoriaScreen({Key? key}) : super(key: key);

  Color _getBadgeColor(String accion) {
    if (accion.contains('CREACIÓN') || accion.contains('ALTA')) return AppTheme.estadoActiva;
    if (accion.contains('DESACTIVACIÓN') || accion.contains('ELIMIN')) return Colors.red.shade700;
    if (accion.contains('MODIFICACIÓN')) return AppTheme.estadoTramite;
    return AppTheme.vinotinto;
  }

  IconData _getIcon(String accion) {
    if (accion.contains('CREACIÓN') || accion.contains('ALTA')) return Icons.add_circle_outline;
    if (accion.contains('DESACTIVACIÓN')) return Icons.remove_circle_outline;
    if (accion.contains('MODIFICACIÓN')) return Icons.edit_note;
    return Icons.history_edu;
  }

  @override
  Widget build(BuildContext context) {
    final provider = context.watch<AbogadosProvider>();
    final logs = provider.auditoriaLogs;

    return Scaffold(
      backgroundColor: AppTheme.fondoBlanco,
      appBar: AppBar(
        title: const Text('Registro de Auditoría PGET'),
        bottom: const PreferredSize(
          preferredSize: Size.fromHeight(2),
          child: Divider(height: 2, color: AppTheme.oro, thickness: 2),
        ),
      ),
      body: Column(
        children: [
          // Banner Superior Auditoría
          Container(
            padding: const EdgeInsets.all(16),
            decoration: const BoxDecoration(
              color: AppTheme.vinotinto,
              border: Border(bottom: BorderSide(color: AppTheme.oro, width: 1.5)),
            ),
            child: Row(
              children: [
                Container(
                  padding: const EdgeInsets.all(10),
                  decoration: BoxDecoration(
                    color: Colors.white,
                    shape: BoxShape.circle,
                    border: Border.all(color: AppTheme.oro, width: 2),
                  ),
                  child: const Icon(Icons.security, color: AppTheme.vinotinto, size: 24),
                ),
                const SizedBox(width: 12),
                const Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'SUPERVISIÓN Y AUDITORÍA ADMIN',
                        style: TextStyle(color: AppTheme.oro, fontSize: 11, fontWeight: FontWeight.bold, letterSpacing: 0.6),
                      ),
                      SizedBox(height: 2),
                      Text(
                        'Historial de Creaciones, Cambios y Bajas',
                        style: TextStyle(color: Colors.white, fontSize: 15, fontWeight: FontWeight.bold),
                      ),
                      Text(
                        'Quién, cuándo y qué se modificó en causas y nómina',
                        style: TextStyle(color: Colors.white70, fontSize: 11),
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),

          // Lista Cronológica de Registros
          Expanded(
            child: logs.isEmpty
                ? const Center(
                    child: Text(
                      'No hay eventos registrados en auditoría todavía.',
                      style: TextStyle(color: AppTheme.textoSecundario),
                    ),
                  )
                : ListView.builder(
                    padding: const EdgeInsets.all(16),
                    itemCount: logs.length,
                    itemBuilder: (ctx, idx) {
                      final item = logs[idx];
                      final color = _getBadgeColor(item.accion);

                      return Container(
                        margin: const EdgeInsets.only(bottom: 12),
                        decoration: BoxDecoration(
                          color: Colors.white,
                          borderRadius: BorderRadius.circular(16),
                          border: Border.all(color: AppTheme.oroBorde, width: 1.3),
                          boxShadow: [
                            BoxShadow(
                              color: AppTheme.vinotinto.withOpacity(0.04),
                              offset: const Offset(0, 3),
                              blurRadius: 8,
                            ),
                          ],
                        ),
                        child: Padding(
                          padding: const EdgeInsets.all(14),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              // Cabecera: Acción + Fecha/Hora
                              Row(
                                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                children: [
                                  Row(
                                    children: [
                                      Icon(_getIcon(item.accion), size: 16, color: color),
                                      const SizedBox(width: 6),
                                      Text(
                                        item.accion,
                                        style: TextStyle(
                                          color: color,
                                          fontSize: 11,
                                          fontWeight: FontWeight.w800,
                                          letterSpacing: 0.4,
                                        ),
                                      ),
                                    ],
                                  ),
                                  Text(
                                    item.fechaFormateada,
                                    style: const TextStyle(
                                      color: AppTheme.textoSecundario,
                                      fontSize: 10.5,
                                      fontWeight: FontWeight.w600,
                                    ),
                                  ),
                                ],
                              ),
                              const SizedBox(height: 8),

                              // Quién lo realizó
                              Row(
                                children: [
                                  const Icon(Icons.person_pin, size: 15, color: AppTheme.vinotinto),
                                  const SizedBox(width: 6),
                                  Text(
                                    'Realizado por: ',
                                    style: const TextStyle(fontSize: 12, color: AppTheme.textoSecundario),
                                  ),
                                  Text(
                                    item.usuario,
                                    style: const TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: AppTheme.vinotinto),
                                  ),
                                ],
                              ),
                              const SizedBox(height: 4),

                              // Expediente y Materia
                              if (item.expediente.isNotEmpty)
                                Row(
                                  children: [
                                    const Icon(Icons.folder_shared_outlined, size: 15, color: AppTheme.oroDark),
                                    const SizedBox(width: 6),
                                    Text(
                                      'Exp: ${item.expediente}  •  ${item.pestana}',
                                      style: const TextStyle(fontSize: 11.5, fontWeight: FontWeight.w600, color: AppTheme.textoPrincipal),
                                    ),
                                  ],
                                ),

                              const SizedBox(height: 8),
                              const Divider(height: 1, color: AppTheme.bordeDivisor),
                              const SizedBox(height: 8),

                              // Detalle de la acción
                              Text(
                                item.detalle,
                                style: const TextStyle(
                                  fontSize: 12,
                                  color: AppTheme.textoPrincipal,
                                  height: 1.35,
                                ),
                              ),
                            ],
                          ),
                        ),
                      );
                    },
                  ),
          ),
        ],
      ),
    );
  }
}

