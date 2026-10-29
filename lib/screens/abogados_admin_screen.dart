import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:url_launcher/url_launcher.dart';
import '../models/abogado_pget.dart';
import '../providers/abogados_provider.dart';
import '../theme/app_theme.dart';
import '../widgets/abogados_admin_modal.dart';

class AbogadosAdminScreen extends StatefulWidget {
  const AbogadosAdminScreen({Key? key}) : super(key: key);

  @override
  State<AbogadosAdminScreen> createState() => _AbogadosAdminScreenState();
}

class _AbogadosAdminScreenState extends State<AbogadosAdminScreen> {
  final TextEditingController _searchCtrl = TextEditingController();
  String _filtroEstado = 'TODOS'; // 'TODOS', 'ACTIVOS', 'INACTIVOS'

  @override
  void dispose() {
    _searchCtrl.dispose();
    super.dispose();
  }

  void _abrirModalEditar(BuildContext context, AbogadoPGET abogado) {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.transparent,
      builder: (_) => AbogadosAdminModal(abogadoAEditar: abogado),
    );
  }

  void _confirmarDesactivar(BuildContext context, AbogadoPGET abogado) {
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
                color: Colors.amber.shade50,
                borderRadius: BorderRadius.circular(8),
              ),
              child: Icon(Icons.person_off_outlined, color: Colors.amber.shade900, size: 22),
            ),
            const SizedBox(width: 10),
            const Expanded(
              child: Text(
                'Dar de Baja a Abogado',
                style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
              ),
            ),
          ],
        ),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              '¿Deseas dar de baja a ${abogado.nombre} (C.I. ${abogado.cedula}) de la nómina activa?',
              style: const TextStyle(fontSize: 13, height: 1.4),
            ),
            const SizedBox(height: 12),
            Container(
              padding: const EdgeInsets.all(10),
              decoration: BoxDecoration(
                color: Colors.amber.shade50,
                borderRadius: BorderRadius.circular(8),
                border: Border.all(color: Colors.amber.shade300),
              ),
              child: Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Icon(Icons.shield_outlined, color: Colors.amber.shade900, size: 18),
                  const SizedBox(width: 8),
                  const Expanded(
                    child: Text(
                      'GARANTÍA HISTÓRICA: Sus actuaciones, causas asignadas y registros en Google Sheets permanecerán 100% intactos.',
                      style: TextStyle(fontSize: 11, fontWeight: FontWeight.bold, color: Colors.brown),
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(ctx),
            child: const Text('Cancelar', style: TextStyle(color: AppTheme.textoSecundario)),
          ),
          ElevatedButton(
            style: ElevatedButton.styleFrom(backgroundColor: Colors.amber.shade900),
            onPressed: () {
              Navigator.pop(ctx);
              context.read<AbogadosProvider>().eliminarAbogado(abogado.id);
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(
                  backgroundColor: AppTheme.vinotinto,
                  content: Text('Abogado ${abogado.nombre} retirado de la nómina activa (Historial preservado).'),
                ),
              );
            },
            child: const Text('Sí, Desactivar', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
          ),
        ],
      ),
    );
  }

  void _confirmarReactivar(BuildContext context, AbogadoPGET abogado) {
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
                color: Colors.green.shade50,
                borderRadius: BorderRadius.circular(8),
              ),
              child: const Icon(Icons.check_circle_outline, color: Colors.green, size: 22),
            ),
            const SizedBox(width: 10),
            const Expanded(
              child: Text(
                'Reactivar en Nómina',
                style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
              ),
            ),
          ],
        ),
        content: Text(
          '¿Deseas reactivar a ${abogado.nombre} (C.I. ${abogado.cedula}) en la nómina activa para asignarle nuevas causas?',
          style: const TextStyle(fontSize: 13, height: 1.4),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(ctx),
            child: const Text('Cancelar', style: TextStyle(color: AppTheme.textoSecundario)),
          ),
          ElevatedButton(
            style: ElevatedButton.styleFrom(backgroundColor: AppTheme.vinotinto),
            onPressed: () {
              Navigator.pop(ctx);
              context.read<AbogadosProvider>().reactivarAbogado(abogado.id);
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(
                  backgroundColor: AppTheme.vinotinto,
                  content: Text('Abogado ${abogado.nombre} reactivado en nómina activa.'),
                ),
              );
            },
            child: const Text('Sí, Reactivar', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
          ),
        ],
      ),
    );
  }

  void _launchUrl(String url) async {
    final uri = Uri.parse(url);
    if (await canLaunchUrl(uri)) {
      await launchUrl(uri);
    }
  }

  @override
  Widget build(BuildContext context) {
    final provider = context.watch<AbogadosProvider>();
    final query = _searchCtrl.text.toLowerCase();

    final listaFiltrada = provider.abogados.where((a) {
      if (_filtroEstado == 'ACTIVOS' && !a.activo) return false;
      if (_filtroEstado == 'INACTIVOS' && a.activo) return false;

      if (query.isEmpty) return true;
      return a.nombre.toLowerCase().contains(query) ||
          a.cedula.toLowerCase().contains(query) ||
          a.cargo.toLowerCase().contains(query) ||
          a.adscrito.toLowerCase().contains(query);
    }).toList();

    final totalActivos = provider.abogados.where((a) => a.activo).length;
    final totalInactivos = provider.abogados.where((a) => !a.activo).length;

    return Scaffold(
      backgroundColor: AppTheme.fondoBlanco,
      appBar: AppBar(
        title: const Text('Nómina de Abogados PGET'),
        bottom: const PreferredSize(
          preferredSize: Size.fromHeight(2),
          child: Divider(height: 2, color: AppTheme.oro, thickness: 2),
        ),
      ),
      floatingActionButton: FloatingActionButton.extended(
        backgroundColor: AppTheme.oro,
        icon: const Icon(Icons.person_add_alt_1, color: AppTheme.vinotintoDark),
        label: const Text(
          'Añadir Abogado',
          style: TextStyle(color: AppTheme.vinotintoDark, fontWeight: FontWeight.bold),
        ),
        onPressed: () {
          showModalBottomSheet(
            context: context,
            isScrollControlled: true,
            backgroundColor: Colors.transparent,
            builder: (_) => const AbogadosAdminModal(),
          );
        },
      ),
      body: Column(
        children: [
          // Banner Superior Nómina
          Container(
            padding: const EdgeInsets.all(16),
            decoration: const BoxDecoration(
              color: AppTheme.vinotinto,
              border: Border(bottom: BorderSide(color: AppTheme.oro, width: 1.5)),
            ),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text(
                      'DIRECCIÓN DE ASUNTOS JURÍDICOS',
                      style: TextStyle(color: AppTheme.oro, fontSize: 11, fontWeight: FontWeight.bold, letterSpacing: 0.6),
                    ),
                    const SizedBox(height: 2),
                    Text(
                      '${provider.abogados.length} Abogados Registrados',
                      style: const TextStyle(color: Colors.white, fontSize: 17, fontWeight: FontWeight.bold),
                    ),
                    Text(
                      '$totalActivos Activos • $totalInactivos Históricos',
                      style: const TextStyle(color: Colors.white70, fontSize: 11),
                    ),
                  ],
                ),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                  decoration: BoxDecoration(
                    color: Colors.white.withOpacity(0.15),
                    borderRadius: BorderRadius.circular(16),
                    border: Border.all(color: AppTheme.oro),
                  ),
                  child: const Row(
                    children: [
                      Icon(Icons.shield_outlined, color: AppTheme.oro, size: 14),
                      SizedBox(width: 5),
                      Text('Admin PGET', style: TextStyle(color: Colors.white, fontSize: 11, fontWeight: FontWeight.bold)),
                    ],
                  ),
                ),
              ],
            ),
          ),

          // Aviso institucional de preservación de histórico
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
            color: Colors.amber.shade50,
            child: Row(
              children: [
                Icon(Icons.info_outline, color: Colors.amber.shade900, size: 16),
                const SizedBox(width: 8),
                const Expanded(
                  child: Text(
                    'Si das de baja a un abogado, su historial en causas de Google Sheets se conserva intacto.',
                    style: TextStyle(fontSize: 11, color: Colors.brown, fontWeight: FontWeight.w600),
                  ),
                ),
              ],
            ),
          ),

          // Selector de filtro Activos / Inactivos / Todos
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 6),
            color: Colors.white,
            child: Row(
              children: [
                Wrap(
                  spacing: 6,
                  children: [
                    ChoiceChip(
                      label: Text('Todos (${provider.abogados.length})'),
                      selected: _filtroEstado == 'TODOS',
                      selectedColor: AppTheme.vinotinto,
                      labelStyle: TextStyle(
                        fontSize: 11,
                        fontWeight: FontWeight.bold,
                        color: _filtroEstado == 'TODOS' ? Colors.white : AppTheme.textoPrincipal,
                      ),
                      onSelected: (_) => setState(() => _filtroEstado = 'TODOS'),
                    ),
                    ChoiceChip(
                      label: Text('Activos ($totalActivos)'),
                      selected: _filtroEstado == 'ACTIVOS',
                      selectedColor: AppTheme.vinotinto,
                      labelStyle: TextStyle(
                        fontSize: 11,
                        fontWeight: FontWeight.bold,
                        color: _filtroEstado == 'ACTIVOS' ? Colors.white : AppTheme.textoPrincipal,
                      ),
                      onSelected: (_) => setState(() => _filtroEstado = 'ACTIVOS'),
                    ),
                    ChoiceChip(
                      label: Text('Histórico ($totalInactivos)'),
                      selected: _filtroEstado == 'INACTIVOS',
                      selectedColor: AppTheme.vinotinto,
                      labelStyle: TextStyle(
                        fontSize: 11,
                        fontWeight: FontWeight.bold,
                        color: _filtroEstado == 'INACTIVOS' ? Colors.white : AppTheme.textoPrincipal,
                      ),
                      onSelected: (_) => setState(() => _filtroEstado = 'INACTIVOS'),
                    ),
                  ],
                ),
              ],
            ),
          ),

          // Buscador
          Padding(
            padding: const EdgeInsets.fromLTRB(16, 6, 16, 6),
            child: TextField(
              controller: _searchCtrl,
              onChanged: (_) => setState(() {}),
              decoration: InputDecoration(
                hintText: 'Buscar por nombre, cédula o cargo...',
                prefixIcon: const Icon(Icons.search, color: AppTheme.vinotinto, size: 20),
                suffixIcon: _searchCtrl.text.isNotEmpty
                    ? IconButton(
                        icon: const Icon(Icons.clear, size: 16),
                        onPressed: () {
                          _searchCtrl.clear();
                          setState(() {});
                        },
                      )
                    : null,
              ),
            ),
          ),

          // Lista de Abogados
          Expanded(
            child: listaFiltrada.isEmpty
                ? Center(
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        const Icon(Icons.person_off_outlined, size: 48, color: AppTheme.textoSecundario),
                        const SizedBox(height: 10),
                        const Text(
                          'No se encontraron abogados',
                          style: TextStyle(fontSize: 15, fontWeight: FontWeight.bold, color: AppTheme.vinotinto),
                        ),
                      ],
                    ),
                  )
                : ListView.builder(
                    padding: const EdgeInsets.fromLTRB(16, 4, 16, 80),
                    itemCount: listaFiltrada.length,
                    itemBuilder: (ctx, idx) {
                      final abg = listaFiltrada[idx];

                      return Container(
                        margin: const EdgeInsets.only(bottom: 12),
                        decoration: BoxDecoration(
                          color: Colors.white,
                          borderRadius: BorderRadius.circular(16),
                          border: Border.all(
                            color: abg.activo ? AppTheme.oroBorde : Colors.grey.shade300,
                            width: 1.3,
                          ),
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
                              // Fila 1: Avatar + Nombre + Estado + Acciones
                              Row(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Container(
                                    width: 44,
                                    height: 44,
                                    decoration: BoxDecoration(
                                      color: abg.activo ? AppTheme.vinotinto : Colors.grey.shade400,
                                      shape: BoxShape.circle,
                                      border: Border.all(color: abg.activo ? AppTheme.oro : Colors.grey.shade500, width: 1.5),
                                    ),
                                    child: Center(
                                      child: Text(
                                        abg.nombre.isNotEmpty ? abg.nombre[0] : 'A',
                                        style: TextStyle(
                                          color: abg.activo ? AppTheme.oro : Colors.white,
                                          fontWeight: FontWeight.bold,
                                          fontSize: 18,
                                        ),
                                      ),
                                    ),
                                  ),
                                  const SizedBox(width: 12),
                                  Expanded(
                                    child: Column(
                                      crossAxisAlignment: CrossAxisAlignment.start,
                                      children: [
                                        Row(
                                          children: [
                                            Expanded(
                                              child: Text(
                                                abg.nombre,
                                                style: TextStyle(
                                                  fontSize: 14,
                                                  fontWeight: FontWeight.bold,
                                                  color: abg.activo ? AppTheme.vinotinto : Colors.grey.shade700,
                                                ),
                                              ),
                                            ),
                                            // Badge de Estado
                                            Container(
                                              padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                                              decoration: BoxDecoration(
                                                color: abg.activo ? Colors.green.withOpacity(0.12) : Colors.amber.withOpacity(0.15),
                                                borderRadius: BorderRadius.circular(4),
                                                border: Border.all(
                                                  color: abg.activo ? Colors.green : Colors.amber.shade800,
                                                  width: 0.8,
                                                ),
                                              ),
                                              child: Text(
                                                abg.activo ? 'ACTIVO' : 'HISTÓRICO',
                                                style: TextStyle(
                                                  fontSize: 9,
                                                  fontWeight: FontWeight.bold,
                                                  color: abg.activo ? Colors.green.shade800 : Colors.amber.shade900,
                                                ),
                                              ),
                                            ),
                                          ],
                                        ),
                                        const SizedBox(height: 2),
                                        Text(
                                          'C.I. ${abg.cedula.isNotEmpty ? abg.cedula : "Sin Cédula"} • ${abg.cargo}',
                                          style: const TextStyle(fontSize: 11, color: AppTheme.textoSecundario),
                                        ),
                                      ],
                                    ),
                                  ),

                                  // Acciones Admin: Editar y Desactivar / Reactivar
                                  Row(
                                    mainAxisSize: MainAxisSize.min,
                                    children: [
                                      IconButton(
                                        icon: const Icon(Icons.edit_outlined, color: AppTheme.vinotinto, size: 20),
                                        tooltip: 'Editar datos del abogado',
                                        onPressed: () => _abrirModalEditar(context, abg),
                                      ),
                                      if (abg.activo)
                                        IconButton(
                                          icon: const Icon(Icons.person_off_outlined, color: Colors.amber, size: 20),
                                          tooltip: 'Dar de baja (Preserva historial)',
                                          onPressed: () => _confirmarDesactivar(context, abg),
                                        )
                                      else
                                        IconButton(
                                          icon: const Icon(Icons.check_circle_outline, color: Colors.green, size: 20),
                                          tooltip: 'Reactivar en nómina activa',
                                          onPressed: () => _confirmarReactivar(context, abg),
                                        ),
                                    ],
                                  ),
                                ],
                              ),

                              const SizedBox(height: 8),
                              const Divider(height: 1, color: AppTheme.bordeDivisor),
                              const SizedBox(height: 8),

                              // Fila 2: Adscripción
                              Row(
                                children: [
                                  const Icon(Icons.account_balance_outlined, size: 14, color: AppTheme.oroDark),
                                  const SizedBox(width: 6),
                                  Expanded(
                                    child: Text(
                                      abg.adscrito.isNotEmpty ? abg.adscrito : 'Procuraduría General',
                                      style: const TextStyle(fontSize: 11, color: AppTheme.textoPrincipal, fontWeight: FontWeight.w600),
                                    ),
                                  ),
                                ],
                              ),

                              // Fila 3: Botones de Contacto Rápido
                              if (abg.telefono.isNotEmpty || abg.correo.isNotEmpty) ...[
                                const SizedBox(height: 10),
                                Row(
                                  mainAxisAlignment: MainAxisAlignment.end,
                                  children: [
                                    if (abg.telefono.isNotEmpty) ...[
                                      InkWell(
                                        onTap: () => _launchUrl('tel:${abg.telefono}'),
                                        child: Container(
                                          padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                                          decoration: BoxDecoration(
                                            color: AppTheme.vinotintoTint,
                                            borderRadius: BorderRadius.circular(6),
                                            border: Border.all(color: AppTheme.oroBordeSuave),
                                          ),
                                          child: const Row(
                                            children: [
                                              Icon(Icons.phone, size: 12, color: AppTheme.vinotinto),
                                              SizedBox(width: 4),
                                              Text('Llamar', style: TextStyle(fontSize: 10, fontWeight: FontWeight.bold, color: AppTheme.vinotinto)),
                                            ],
                                          ),
                                        ),
                                      ),
                                      const SizedBox(width: 6),
                                      InkWell(
                                        onTap: () => _launchUrl('https://wa.me/${abg.telefono.replaceAll(RegExp(r'[^0-9]'), '')}'),
                                        child: Container(
                                          padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                                          decoration: BoxDecoration(
                                            color: const Color(0xFF25D366).withOpacity(0.12),
                                            borderRadius: BorderRadius.circular(6),
                                            border: Border.all(color: const Color(0xFF25D366).withOpacity(0.4)),
                                          ),
                                          child: const Row(
                                            children: [
                                              Icon(Icons.chat_bubble_outline, size: 12, color: Color(0xFF1E7E34)),
                                              SizedBox(width: 4),
                                              Text('WhatsApp', style: TextStyle(fontSize: 10, fontWeight: FontWeight.bold, color: Color(0xFF1E7E34))),
                                            ],
                                          ),
                                        ),
                                      ),
                                    ],
                                  ],
                                ),
                              ],
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
