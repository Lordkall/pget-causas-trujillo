import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/abogados_provider.dart';
import '../theme/app_theme.dart';
import '../screens/abogados_admin_screen.dart';
import '../screens/auditoria_screen.dart';

class PgetAppHeader extends StatelessWidget {
  const PgetAppHeader({Key? key}) : super(key: key);

  void _irAHome(BuildContext context) {
    Navigator.of(context).popUntil((route) => route.isFirst);
  }

  @override
  Widget build(BuildContext context) {
    final provider = context.watch<AbogadosProvider>();
    final isAdmin = provider.isAdminMode;

    return Container(
      decoration: BoxDecoration(
        color: AppTheme.vinotinto,
        border: const Border(
          bottom: BorderSide(color: AppTheme.oro, width: 2.5),
        ),
        boxShadow: [
          BoxShadow(
            color: AppTheme.vinotintoDark.withOpacity(0.3),
            blurRadius: 10,
            offset: const Offset(0, 4),
          ),
        ],
      ),
      child: SafeArea(
        bottom: false,
        child: Padding(
          padding: const EdgeInsets.fromLTRB(16, 12, 16, 12),
          child: Column(
            children: [
              // FILA PRINCIPAL: LOGO + TÍTULO + SWITCH ROL
              Row(
                crossAxisAlignment: CrossAxisAlignment.center,
                children: [
                  // LOGO OFICIAL PGET: Clic lleva a Home
                  InkWell(
                    onTap: () => _irAHome(context),
                    borderRadius: BorderRadius.circular(28),
                    child: Container(
                      width: 52,
                      height: 52,
                      padding: const EdgeInsets.all(3),
                      decoration: BoxDecoration(
                        color: AppTheme.vinotintoDark,
                        shape: BoxShape.circle,
                        border: Border.all(color: AppTheme.oro, width: 2.2),
                        boxShadow: [
                          BoxShadow(
                            color: Colors.black.withOpacity(0.3),
                            blurRadius: 8,
                            offset: const Offset(0, 3),
                          ),
                        ],
                      ),
                      child: ClipOval(
                        child: Image.asset(
                          'assets/logo_pget.png',
                          fit: BoxFit.contain,
                          filterQuality: FilterQuality.high,
                          errorBuilder: (_, __, ___) => const Icon(
                            Icons.account_balance,
                            color: AppTheme.oro,
                            size: 28,
                          ),
                        ),
                      ),
                    ),
                  ),
                  const SizedBox(width: 12),

                  // TÍTULO: Clic lleva a Home
                  Expanded(
                    child: InkWell(
                      onTap: () => _irAHome(context),
                      child: const Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            'PROCURADURÍA GENERAL',
                            style: TextStyle(
                              color: AppTheme.oro,
                              fontSize: 13.5,
                              fontWeight: FontWeight.w900,
                              letterSpacing: 0.8,
                            ),
                          ),
                          Text(
                            'ESTADO TRUJILLO • CAUSAS',
                            style: TextStyle(
                              color: Colors.white,
                              fontSize: 11,
                              fontWeight: FontWeight.w600,
                              letterSpacing: 0.5,
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),

                  // USUARIO LOGUEADO + BOTÓN CERRAR SESIÓN
                  Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                        decoration: BoxDecoration(
                          color: AppTheme.vinotintoDark,
                          borderRadius: BorderRadius.circular(12),
                          border: Border.all(color: AppTheme.oroBorde, width: 1),
                        ),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.end,
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            Text(
                              provider.usuarioAutenticado?.nombre.split(' ').first ?? (isAdmin ? 'Admin' : 'Abogado'),
                              style: const TextStyle(
                                fontSize: 10,
                                fontWeight: FontWeight.bold,
                                color: AppTheme.oro,
                              ),
                            ),
                            Text(
                              isAdmin ? 'ADMIN' : 'ABOGADO',
                              style: const TextStyle(fontSize: 8.5, color: Colors.white70),
                            ),
                          ],
                        ),
                      ),
                      const SizedBox(width: 6),
                      IconButton(
                        icon: const Icon(Icons.logout, color: Colors.white, size: 19),
                        tooltip: 'Cerrar Sesión',
                        onPressed: () {
                          provider.logout();
                        },
                      ),
                    ],
                  ),
                ],
              ),

              // SUB-BARRA: Si es Admin, accesos directos a Nómina y Auditoría
              if (isAdmin) ...[
                const SizedBox(height: 10),
                Row(
                  children: [
                    Expanded(
                      child: InkWell(
                        onTap: () {
                          Navigator.push(
                            context,
                            MaterialPageRoute(builder: (_) => const AbogadosAdminScreen()),
                          );
                        },
                        borderRadius: BorderRadius.circular(10),
                        child: Container(
                          padding: const EdgeInsets.symmetric(vertical: 6, horizontal: 10),
                          decoration: BoxDecoration(
                            color: Colors.white.withOpacity(0.12),
                            borderRadius: BorderRadius.circular(10),
                            border: Border.all(color: AppTheme.oro.withOpacity(0.5)),
                          ),
                          child: const Row(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Icon(Icons.people_outline, color: AppTheme.oro, size: 15),
                              SizedBox(width: 6),
                              Text(
                                'Nómina de Abogados',
                                style: TextStyle(color: Colors.white, fontSize: 11, fontWeight: FontWeight.bold),
                              ),
                            ],
                          ),
                        ),
                      ),
                    ),
                    const SizedBox(width: 8),
                    Expanded(
                      child: InkWell(
                        onTap: () {
                          Navigator.push(
                            context,
                            MaterialPageRoute(builder: (_) => const AuditoriaScreen()),
                          );
                        },
                        borderRadius: BorderRadius.circular(10),
                        child: Container(
                          padding: const EdgeInsets.symmetric(vertical: 6, horizontal: 10),
                          decoration: BoxDecoration(
                            color: Colors.white.withOpacity(0.12),
                            borderRadius: BorderRadius.circular(10),
                            border: Border.all(color: AppTheme.oro.withOpacity(0.5)),
                          ),
                          child: const Row(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Icon(Icons.security, color: AppTheme.oro, size: 15),
                              SizedBox(width: 6),
                              Text(
                                'Auditoría Admin',
                                style: TextStyle(color: Colors.white, fontSize: 11, fontWeight: FontWeight.bold),
                              ),
                            ],
                          ),
                        ),
                      ),
                    ),
                  ],
                ),
              ],

              // Si es Abogado: Selector del abogado activo en sesión
              if (!isAdmin) ...[
                const SizedBox(height: 8),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
                  decoration: BoxDecoration(
                    color: Colors.white.withOpacity(0.12),
                    borderRadius: BorderRadius.circular(10),
                    border: Border.all(color: AppTheme.oro.withOpacity(0.5)),
                  ),
                  child: Row(
                    children: [
                      const Icon(Icons.person, color: AppTheme.oro, size: 16),
                      const SizedBox(width: 8),
                      const Text('Abogado Activo: ', style: TextStyle(color: Colors.white70, fontSize: 11)),
                      Expanded(
                        child: DropdownButtonHideUnderline(
                          child: DropdownButton<String>(
                            value: provider.abogadoSesion?.nombre,
                            dropdownColor: AppTheme.vinotintoDark,
                            isDense: true,
                            icon: const Icon(Icons.arrow_drop_down, color: AppTheme.oro, size: 18),
                            style: const TextStyle(color: Colors.white, fontSize: 11.5, fontWeight: FontWeight.bold),
                            items: provider.abogadosActivos.map((a) {
                              return DropdownMenuItem<String>(
                                value: a.nombre,
                                child: Text(a.nombre, style: const TextStyle(color: Colors.white)),
                              );
                            }).toList(),
                            onChanged: (nombre) {
                              if (nombre != null) {
                                final sel = provider.abogados.firstWhere((a) => a.nombre == nombre);
                                provider.setAbogadoSesion(sel);
                              }
                            },
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ],
          ),
        ),
      ),
    );
  }
}
