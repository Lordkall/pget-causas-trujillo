import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import 'package:provider/provider.dart';
import 'package:url_launcher/url_launcher.dart';
import '../models/abogado.dart';
import '../providers/abogados_provider.dart';
import '../theme/app_theme.dart';
import 'abogado_form_screen.dart';

class AbogadoDetailScreen extends StatelessWidget {
  final Abogado abogado;

  const AbogadoDetailScreen({Key? key, required this.abogado}) : super(key: key);

  void _launchUrl(String url) async {
    final uri = Uri.parse(url);
    if (await canLaunchUrl(uri)) {
      await launchUrl(uri);
    }
  }

  void _confirmarEliminacion(BuildContext context) {
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
        title: const Text('¿Eliminar abogado?'),
        content: Text('¿Deseas eliminar a ${abogado.nombre} de Google Sheets y del sistema?'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(ctx),
            child: const Text('Cancelar', style: TextStyle(color: AppTheme.textMuted)),
          ),
          ElevatedButton(
            style: ElevatedButton.styleFrom(backgroundColor: AppTheme.statusInactive),
            onPressed: () async {
              Navigator.pop(ctx);
              await context.read<AbogadosProvider>().eliminarAbogado(abogado.id);
              if (context.mounted) {
                Navigator.pop(context);
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(
                    content: Text('Registro eliminado de Google Sheets'),
                    backgroundColor: AppTheme.statusInactive,
                  ),
                );
              }
            },
            child: const Text('Eliminar', style: TextStyle(color: Colors.white)),
          ),
        ],
      ),
    );
  }

  Widget _buildInfoTile(IconData icon, String label, String value) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 14),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Container(
            padding: const EdgeInsets.all(8),
            decoration: BoxDecoration(
              color: AppTheme.primaryNavy.withOpacity(0.06),
              borderRadius: BorderRadius.circular(10),
            ),
            child: Icon(icon, size: 18, color: AppTheme.primaryNavy),
          ),
          const SizedBox(width: 14),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  label,
                  style: const TextStyle(
                    fontSize: 12,
                    fontWeight: FontWeight.w500,
                    color: AppTheme.textMuted,
                  ),
                ),
                const SizedBox(height: 2),
                Text(
                  value.isNotEmpty ? value : 'No especificado',
                  style: const TextStyle(
                    fontSize: 15,
                    fontWeight: FontWeight.w600,
                    color: AppTheme.textDark,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final dateFormat = DateFormat('dd ' 'MMMM ' 'yyyy, hh:mm a');

    return Scaffold(
      backgroundColor: AppTheme.backgroundLight,
      appBar: AppBar(
        title: const Text('Ficha del Abogado'),
        actions: [
          IconButton(
            icon: const Icon(Icons.edit_outlined),
            tooltip: 'Editar',
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (_) => AbogadoFormScreen(abogadoAEditar: abogado),
                ),
              );
            },
          ),
          IconButton(
            icon: const Icon(Icons.delete_outline, color: Color(0xFFFCA5A5)),
            tooltip: 'Eliminar',
            onPressed: () => _confirmarEliminacion(context),
          ),
        ],
      ),
      body: ListView(
        padding: const EdgeInsets.all(20),
        children: [
          // Tarjeta Principal Ejecutiva
          Container(
            padding: const EdgeInsets.all(20),
            decoration: BoxDecoration(
              gradient: const LinearGradient(
                colors: [AppTheme.primaryNavy, AppTheme.secondaryNavy],
                begin: Alignment.topLeft,
                end: Alignment.bottomRight,
              ),
              borderRadius: BorderRadius.circular(20),
              boxShadow: [
                BoxShadow(
                  color: AppTheme.primaryNavy.withOpacity(0.2),
                  blurRadius: 12,
                  offset: const Offset(0, 5),
                ),
              ],
            ),
            child: Column(
              children: [
                // Avatar e iniciales
                Container(
                  width: 70,
                  height: 70,
                  decoration: BoxDecoration(
                    color: Colors.white.withOpacity(0.15),
                    shape: BoxShape.circle,
                    border: Border.all(color: AppTheme.accentGold, width: 2),
                  ),
                  child: Center(
                    child: Text(
                      abogado.nombre.isNotEmpty ? abogado.nombre.substring(0, 1) : 'A',
                      style: const TextStyle(
                        fontSize: 28,
                        fontWeight: FontWeight.bold,
                        color: AppTheme.accentGold,
                      ),
                    ),
                  ),
                ),
                const SizedBox(height: 14),
                Text(
                  abogado.nombre,
                  textAlign: TextAlign.center,
                  style: const TextStyle(
                    fontSize: 20,
                    fontWeight: FontWeight.bold,
                    color: Colors.white,
                  ),
                ),
                const SizedBox(height: 6),
                Text(
                  '${abogado.especialidad}  •  ${abogado.id}',
                  style: const TextStyle(
                    fontSize: 13,
                    color: AppTheme.accentGold,
                    fontWeight: FontWeight.w600,
                  ),
                ),
                const SizedBox(height: 16),

                // Acciones Directas (Llamar, WhatsApp, Email)
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    if (abogado.telefono.isNotEmpty) ...[
                      IconButton.filled(
                        style: IconButton.styleFrom(backgroundColor: Colors.white.withOpacity(0.2)),
                        icon: const Icon(Icons.phone, color: Colors.white),
                        tooltip: 'Llamar',
                        onPressed: () => _launchUrl('tel:${abogado.telefono}'),
                      ),
                      const SizedBox(width: 14),
                      IconButton.filled(
                        style: IconButton.styleFrom(backgroundColor: const Color(0xFF25D366)),
                        icon: const Icon(Icons.chat, color: Colors.white),
                        tooltip: 'WhatsApp',
                        onPressed: () => _launchUrl('https://wa.me/${abogado.telefono.replaceAll(RegExp(r'[^0-9]'), '')}'),
                      ),
                      const SizedBox(width: 14),
                    ],
                    if (abogado.correo.isNotEmpty) ...[
                      IconButton.filled(
                        style: IconButton.styleFrom(backgroundColor: Colors.white.withOpacity(0.2)),
                        icon: const Icon(Icons.email, color: Colors.white),
                        tooltip: 'Enviar Correo',
                        onPressed: () => _launchUrl('mailto:${abogado.correo}'),
                      ),
                    ],
                  ],
                ),
              ],
            ),
          ),

          const SizedBox(height: 20),

          // Tarjeta: Datos Jurídicos
          Card(
            child: Padding(
              padding: const EdgeInsets.all(18),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text(
                    'Información Profesional',
                    style: TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                      color: AppTheme.primaryNavy,
                    ),
                  ),
                  const SizedBox(height: 16),
                  _buildInfoTile(Icons.fingerprint, 'Cédula / Documento de Identidad', abogado.identificacion),
                  _buildInfoTile(Icons.verified_outlined, 'N° Matrícula / Colegiatura', abogado.colegiatura),
                  _buildInfoTile(Icons.gavel, 'Especialidad Jurídica', abogado.especialidad),
                  _buildInfoTile(Icons.business_outlined, 'Despacho / Bufete', abogado.despacho),
                  _buildInfoTile(Icons.location_on_outlined, 'Ciudad / Jurisdicción', abogado.ciudad),
                ],
              ),
            ),
          ),

          const SizedBox(height: 14),

          // Tarjeta: Contacto & Sistema
          Card(
            child: Padding(
              padding: const EdgeInsets.all(18),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text(
                    'Contacto y Auditoría',
                    style: TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                      color: AppTheme.primaryNavy,
                    ),
                  ),
                  const SizedBox(height: 16),
                  _buildInfoTile(Icons.phone, 'Teléfono / Móvil', abogado.telefono),
                  _buildInfoTile(Icons.email, 'Correo Electrónico', abogado.correo),
                  _buildInfoTile(Icons.check_circle_outline, 'Estado en el Sistema', abogado.estado),
                  _buildInfoTile(Icons.access_time, 'Fecha de Registro en Sheets', dateFormat.format(abogado.fechaRegistro)),
                ],
              ),
            ),
          ),

          if (abogado.observaciones.isNotEmpty) ...[
            const SizedBox(height: 14),
            Card(
              child: Padding(
                padding: const EdgeInsets.all(18),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text(
                      'Observaciones / Casos',
                      style: TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.bold,
                        color: AppTheme.primaryNavy,
                      ),
                    ),
                    const SizedBox(height: 12),
                    Text(
                      abogado.observaciones,
                      style: const TextStyle(
                        fontSize: 14,
                        color: AppTheme.textDark,
                        height: 1.5,
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ],
        ],
      ),
    );
  }
}

