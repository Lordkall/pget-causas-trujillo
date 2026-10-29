import 'package:flutter/material.dart';
import '../models/causa_judicial.dart';
import '../theme/app_theme.dart';
import '../screens/causa_detail_screen.dart';

class CausaCard extends StatelessWidget {
  final CausaJudicial causa;

  const CausaCard({Key? key, required this.causa}) : super(key: key);

  Color _getEstadoColor(String estado) {
    final est = estado.toUpperCase();
    if (est.contains('ACTIV')) return AppTheme.estadoActiva;
    if (est.contains('CERRAD')) return AppTheme.estadoCerrada;
    return AppTheme.estadoTramite;
  }

  @override
  Widget build(BuildContext context) {
    final estadoColor = _getEstadoColor(causa.estadoActual);

    return Container(
      margin: const EdgeInsets.only(bottom: 14),
      decoration: BoxDecoration(
        color: AppTheme.tarjetaBlanca,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: AppTheme.oroBorde, width: 1.4), // Bordes dorados pedidos
        boxShadow: [
          BoxShadow(
            color: AppTheme.vinotinto.withOpacity(0.06),
            offset: const Offset(0, 4),
            blurRadius: 10,
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
                builder: (_) => CausaDetailScreen(causa: causa),
              ),
            );
          },
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // Cabecera: N° Expediente + Estado
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Row(
                      children: [
                        Container(
                          padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                          decoration: BoxDecoration(
                            color: AppTheme.vinotinto,
                            borderRadius: BorderRadius.circular(6),
                            border: Border.all(color: AppTheme.oro, width: 1),
                          ),
                          child: Text(
                            'EXP. ${causa.numeroExpediente.isNotEmpty ? causa.numeroExpediente : causa.numero}',
                            style: const TextStyle(
                              color: Colors.white,
                              fontSize: 12,
                              fontWeight: FontWeight.w800,
                              letterSpacing: 0.5,
                            ),
                          ),
                        ),
                        const SizedBox(width: 8),
                        Text(
                          'Causa #${causa.numero}',
                          style: const TextStyle(
                            fontSize: 12,
                            color: AppTheme.textoSecundario,
                            fontWeight: FontWeight.w600,
                          ),
                        ),
                      ],
                    ),
                    // Badge Estado
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                      decoration: BoxDecoration(
                        color: estadoColor.withOpacity(0.12),
                        borderRadius: BorderRadius.circular(20),
                        border: Border.all(color: estadoColor, width: 1),
                      ),
                      child: Row(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          Container(
                            width: 6,
                            height: 6,
                            decoration: BoxDecoration(color: estadoColor, shape: BoxShape.circle),
                          ),
                          const SizedBox(width: 5),
                          Text(
                            causa.estadoActual,
                            style: TextStyle(
                              color: estadoColor,
                              fontSize: 11,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                        ],
                      ),
                    ),
                  ],
                ),

                const SizedBox(height: 12),

                // Motivo de la Causa
                Text(
                  causa.motivo.isNotEmpty ? causa.motivo : 'Sin motivo especificado',
                  style: const TextStyle(
                    fontSize: 15,
                    fontWeight: FontWeight.w700,
                    color: AppTheme.vinotinto,
                    height: 1.25,
                  ),
                  maxLines: 2,
                  overflow: TextOverflow.ellipsis,
                ),

                const SizedBox(height: 10),
                const Divider(height: 1, color: AppTheme.bordeDivisor),
                const SizedBox(height: 10),

                // Partes Judiciales: Demandante y Demandado
                Row(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Icon(Icons.compare_arrows_rounded, size: 16, color: AppTheme.oroDark),
                    const SizedBox(width: 6),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          RichText(
                            text: TextSpan(
                              style: const TextStyle(fontSize: 12, color: AppTheme.textoPrincipal),
                              children: [
                                const TextSpan(text: 'Demandante: ', style: TextStyle(fontWeight: FontWeight.bold, color: AppTheme.textoSecundario)),
                                TextSpan(text: causa.demandante.isNotEmpty ? causa.demandante : 'N/A', style: const TextStyle(fontWeight: FontWeight.w600)),
                              ],
                            ),
                            maxLines: 1,
                            overflow: TextOverflow.ellipsis,
                          ),
                          const SizedBox(height: 3),
                          RichText(
                            text: TextSpan(
                              style: const TextStyle(fontSize: 12, color: AppTheme.textoPrincipal),
                              children: [
                                const TextSpan(text: 'Demandado: ', style: TextStyle(fontWeight: FontWeight.bold, color: AppTheme.textoSecundario)),
                                TextSpan(text: causa.demandado.isNotEmpty ? causa.demandado : 'N/A', style: const TextStyle(fontWeight: FontWeight.w600)),
                              ],
                            ),
                            maxLines: 1,
                            overflow: TextOverflow.ellipsis,
                          ),
                        ],
                      ),
                    ),
                  ],
                ),

                const SizedBox(height: 10),

                // Pie de Tarjeta: Abogado Responsable + Tribunal
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 8),
                  decoration: BoxDecoration(
                    color: AppTheme.vinotintoTint,
                    borderRadius: BorderRadius.circular(10),
                    border: Border.all(color: AppTheme.oroBordeSuave, width: 1),
                  ),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Row(
                        children: [
                          const Icon(Icons.badge_outlined, size: 15, color: AppTheme.vinotinto),
                          const SizedBox(width: 6),
                          Text(
                            causa.abogadoResponsable.isNotEmpty ? causa.abogadoResponsable : 'Sin Asignar',
                            style: const TextStyle(
                              fontSize: 12,
                              fontWeight: FontWeight.bold,
                              color: AppTheme.vinotinto,
                            ),
                          ),
                        ],
                      ),
                      if (causa.fechaEntrada.isNotEmpty)
                        Text(
                          causa.fechaEntrada,
                          style: const TextStyle(
                            fontSize: 11,
                            color: AppTheme.textoSecundario,
                            fontWeight: FontWeight.w500,
                          ),
                        ),
                    ],
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

