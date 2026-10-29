import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';
import '../models/abogado.dart';
import '../theme/app_theme.dart';
import '../screens/abogado_detail_screen.dart';

class LawyerCard extends StatelessWidget {
  final Abogado abogado;

  const LawyerCard({Key? key, required this.abogado}) : super(key: key);

  Color _getStatusColor(String estado) {
    switch (estado.toLowerCase()) {
      case 'activo':
        return AppTheme.statusActive;
      case 'en trámite':
      case 'en tramite':
        return AppTheme.statusPending;
      case 'suspendido':
        return AppTheme.statusSuspended;
      default:
        return AppTheme.statusInactive;
    }
  }

  String _getInitials(String name) {
    final cleaned = name.replaceAll(RegExp(r'^(Dr\.|Dra\.|Lic\.)\s*', caseSensitive: false), '').trim();
    final parts = cleaned.split(' ');
    if (parts.length >= 2) {
      return '${parts[0][0]}${parts[1][0]}'.toUpperCase();
    } else if (parts.isNotEmpty && parts[0].isNotEmpty) {
      return parts[0].substring(0, parts[0].length >= 2 ? 2 : 1).toUpperCase();
    }
    return 'AB';
  }

  void _launchUrl(String url) async {
    final uri = Uri.parse(url);
    if (await canLaunchUrl(uri)) {
      await launchUrl(uri);
    }
  }

  @override
  Widget build(BuildContext context) {
    final statusColor = _getStatusColor(abogado.estado);

    return Container(
      margin: const EdgeInsets.only(bottom: 14),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: AppTheme.borderSubtle, width: 1.2),
        boxShadow: [
          BoxShadow(
            color: AppTheme.primaryNavy.withOpacity(0.04),
            offset: const Offset(0, 4),
            blurRadius: 12,
          ),
        ],
      ),
      child: Material(
        color: Colors.transparent,
        borderRadius: BorderRadius.circular(16),
        child: InkWell(
          borderRadius: BorderRadius.circular(16),
          onTap: () {
            Navigator.push(
              context,
              MaterialPageRoute(
                builder: (_) => AbogadoDetailScreen(abogado: abogado),
              ),
            );
          },
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // Fila Superior: Avatar + Nombre + Estado
                Row(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    // Avatar Ejecutivo
                    Container(
                      width: 50,
                      height: 50,
                      decoration: BoxDecoration(
                        gradient: const LinearGradient(
                          colors: [AppTheme.primaryNavy, AppTheme.secondaryNavy],
                          begin: Alignment.topLeft,
                          end: Alignment.bottomRight,
                        ),
                        borderRadius: BorderRadius.circular(14),
                        boxShadow: [
                          BoxShadow(
                            color: AppTheme.primaryNavy.withOpacity(0.2),
                            blurRadius: 6,
                            offset: const Offset(0, 2),
                          ),
                        ],
                      ),
                      child: Center(
                        child: Text(
                          _getInitials(abogado.nombre),
                          style: const TextStyle(
                            color: AppTheme.accentGold,
                            fontWeight: FontWeight.bold,
                            fontSize: 17,
                          ),
                        ),
                      ),
                    ),
                    const SizedBox(width: 14),
                    // Información Principal
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            abogado.nombre,
                            style: const TextStyle(
                              fontSize: 16,
                              fontWeight: FontWeight.w700,
                              color: AppTheme.primaryNavy,
                            ),
                            maxLines: 1,
                            overflow: TextOverflow.ellipsis,
                          ),
                          const SizedBox(height: 3),
                          Text(
                            '${abogado.colegiatura}  •  ${abogado.id}',
                            style: const TextStyle(
                              fontSize: 12,
                              fontWeight: FontWeight.w500,
                              color: AppTheme.textMuted,
                            ),
                          ),
                        ],
                      ),
                    ),
                    // Badge Estado
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                      decoration: BoxDecoration(
                        color: statusColor.withOpacity(0.12),
                        borderRadius: BorderRadius.circular(20),
                        border: Border.all(color: statusColor.withOpacity(0.3), width: 1),
                      ),
                      child: Row(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          Container(
                            width: 6,
                            height: 6,
                            decoration: BoxDecoration(
                              color: statusColor,
                              shape: BoxShape.circle,
                            ),
                          ),
                          const SizedBox(width: 5),
                          Text(
                            abogado.estado,
                            style: TextStyle(
                              color: statusColor,
                              fontSize: 11,
                              fontWeight: FontWeight.w700,
                            ),
                          ),
                        ],
                      ),
                    ),
                  ],
                ),

                const SizedBox(height: 14),
                const Divider(height: 1, color: AppTheme.borderSubtle),
                const SizedBox(height: 12),

                // Tags de Especialidad y Despacho
                Row(
                  children: [
                    // Especialidad Chip
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                      decoration: BoxDecoration(
                        color: AppTheme.lightGold,
                        borderRadius: BorderRadius.circular(8),
                        border: Border.all(color: AppTheme.accentGold.withOpacity(0.4)),
                      ),
                      child: Row(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          const Icon(Icons.gavel, size: 13, color: AppTheme.darkGold),
                          const SizedBox(width: 5),
                          Text(
                            abogado.especialidad,
                            style: const TextStyle(
                              color: AppTheme.primaryNavy,
                              fontSize: 12,
                              fontWeight: FontWeight.w600,
                            ),
                          ),
                        ],
                      ),
                    ),
                    const SizedBox(width: 8),
                    // Despacho o Ciudad
                    if (abogado.ciudad.isNotEmpty || abogado.despacho.isNotEmpty)
                      Expanded(
                        child: Row(
                          children: [
                            const Icon(Icons.location_on_outlined, size: 14, color: AppTheme.textMuted),
                            const SizedBox(width: 3),
                            Expanded(
                              child: Text(
                                abogado.despacho.isNotEmpty
                                    ? abogado.despacho
                                    : abogado.ciudad,
                                style: const TextStyle(
                                  fontSize: 12,
                                  color: AppTheme.textMuted,
                                ),
                                maxLines: 1,
                                overflow: TextOverflow.ellipsis,
                              ),
                            ),
                          ],
                        ),
                      ),
                  ],
                ),

                const SizedBox(height: 12),

                // Botones rápidos de contacto (Teléfono / WhatsApp / Email)
                Row(
                  mainAxisAlignment: MainAxisAlignment.end,
                  children: [
                    if (abogado.telefono.isNotEmpty) ...[
                      InkWell(
                        onTap: () => _launchUrl('tel:${abogado.telefono}'),
                        borderRadius: BorderRadius.circular(8),
                        child: Container(
                          padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
                          decoration: BoxDecoration(
                            color: AppTheme.backgroundLight,
                            borderRadius: BorderRadius.circular(8),
                            border: Border.all(color: AppTheme.borderSubtle),
                          ),
                          child: const Row(
                            children: [
                              Icon(Icons.phone_outlined, size: 14, color: AppTheme.secondaryNavy),
                              SizedBox(width: 4),
                              Text('Llamar', style: TextStyle(fontSize: 11, fontWeight: FontWeight.w600, color: AppTheme.secondaryNavy)),
                            ],
                          ),
                        ),
                      ),
                      const SizedBox(width: 8),
                      InkWell(
                        onTap: () => _launchUrl('https://wa.me/${abogado.telefono.replaceAll(RegExp(r'[^0-9]'), '')}'),
                        borderRadius: BorderRadius.circular(8),
                        child: Container(
                          padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
                          decoration: BoxDecoration(
                            color: const Color(0xFF25D366).withOpacity(0.1),
                            borderRadius: BorderRadius.circular(8),
                            border: Border.all(color: const Color(0xFF25D366).withOpacity(0.3)),
                          ),
                          child: const Row(
                            children: [
                              Icon(Icons.chat_bubble_outline, size: 14, color: Color(0xFF1E7E34)),
                              SizedBox(width: 4),
                              Text('WhatsApp', style: TextStyle(fontSize: 11, fontWeight: FontWeight.w600, color: Color(0xFF1E7E34))),
                            ],
                          ),
                        ),
                      ),
                      const SizedBox(width: 8),
                    ],
                    if (abogado.correo.isNotEmpty) ...[
                      InkWell(
                        onTap: () => _launchUrl('mailto:${abogado.correo}'),
                        borderRadius: BorderRadius.circular(8),
                        child: Container(
                          padding: const EdgeInsets.all(6),
                          decoration: BoxDecoration(
                            color: AppTheme.backgroundLight,
                            borderRadius: BorderRadius.circular(8),
                            border: Border.all(color: AppTheme.borderSubtle),
                          ),
                          child: const Icon(Icons.mail_outline, size: 16, color: AppTheme.primaryNavy),
                        ),
                      ),
                    ],
                  ],
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

