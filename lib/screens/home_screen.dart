import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../models/pget_tab.dart';
import '../providers/abogados_provider.dart';
import '../theme/app_theme.dart';
import '../widgets/pget_header.dart';
import 'abogados_admin_screen.dart';
import 'auditoria_screen.dart';
import 'select_tab_modal.dart';
import 'causa_detail_screen.dart';
import 'causa_form_screen.dart';
import '../models/causa_judicial.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({Key? key}) : super(key: key);

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final TextEditingController _searchCtrl = TextEditingController();
  final List<String> _estadosFiltro = ['TODAS', 'ACTIVA', 'CERRADA', 'EN TRÁMITE'];

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      context.read<AbogadosProvider>().cargarFilasPestana();
    });
  }

  @override
  void dispose() {
    _searchCtrl.dispose();
    super.dispose();
  }

  void _abrirSelectorPestanas(BuildContext context) {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.transparent,
      builder: (_) => const SelectTabModal(),
    );
  }

  void _mostrarDialogoEliminar(BuildContext context, CausaJudicial causa) {
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
          '¿Estás seguro de que deseas eliminar la causa del Expediente Nº ${causa.numeroExpediente}?\\n\\nEsta acción quedará registrada en el Registro de Auditoría del Sistema.',
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
              final exito = await provider.eliminarCausa(causa);
              if (mounted) {
                if (exito) {
                  ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(
                      backgroundColor: AppTheme.vinotinto,
                      content: Text('Causa con Expediente ${causa.numeroExpediente} eliminada del sistema.'),
                    ),
                  );
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

  Widget _buildMetricCard({
    required String title,
    required String value,
    required IconData icon,
    required Color color,
    VoidCallback? onTap,
  }) {
    return Expanded(
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(14),
        child: Container(
          padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 10),
          decoration: BoxDecoration(
            color: Colors.white,
            borderRadius: BorderRadius.circular(14),
            border: Border.all(color: AppTheme.oroBorde, width: 1.2),
            boxShadow: [
              BoxShadow(
                color: AppTheme.vinotinto.withOpacity(0.04),
                blurRadius: 6,
                offset: const Offset(0, 2),
              ),
            ],
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text(
                    value,
                    style: TextStyle(
                      fontSize: 17,
                      fontWeight: FontWeight.w900,
                      color: color,
                    ),
                  ),
                  Icon(icon, color: color, size: 16),
                ],
              ),
              const SizedBox(height: 3),
              Text(
                title,
                style: const TextStyle(
                  fontSize: 10.5,
                  fontWeight: FontWeight.w600,
                  color: AppTheme.textoSecundario,
                ),
                maxLines: 1,
                overflow: TextOverflow.ellipsis,
              ),
            ],
          ),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final provider = context.watch<AbogadosProvider>();
    final isAdmin = provider.isAdminMode;
    final currentTab = provider.currentTab;
    final years = provider.availableYears;

    return Scaffold(
      backgroundColor: AppTheme.fondoBlanco,
      body: Column(
        children: [
          // Cabecera Oficial PGET (Limpia, sin botones desordenados, clic lleva a Home)
          const PgetAppHeader(),

          // Selector de Pestaña Activa y Filtro de Año
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
            decoration: const BoxDecoration(
              color: Colors.white,
              border: Border(bottom: BorderSide(color: AppTheme.oroBorde, width: 1)),
            ),
            child: Row(
              children: [
                // Selector Pestaña
                Expanded(
                  flex: 3,
                  child: Row(
                    children: [
                      const Icon(Icons.table_chart_outlined, color: AppTheme.vinotinto, size: 16),
                      const SizedBox(width: 6),
                      Expanded(
                        child: DropdownButtonHideUnderline(
                          child: DropdownButton<PgetTab>(
                            value: currentTab,
                            isDense: true,
                            isExpanded: true,
                            icon: const Icon(Icons.arrow_drop_down, color: AppTheme.vinotinto, size: 18),
                            style: const TextStyle(color: AppTheme.vinotinto, fontSize: 12, fontWeight: FontWeight.bold),
                            items: provider.tabs.map((tab) {
                              return DropdownMenuItem<PgetTab>(
                                value: tab,
                                child: Text(tab.title, overflow: TextOverflow.ellipsis),
                              );
                            }).toList(),
                            onChanged: (newTab) {
                              if (newTab != null) {
                                provider.setCurrentTab(newTab);
                              }
                            },
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
                const SizedBox(width: 8),

                // FILTRO DE AÑO
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                  decoration: BoxDecoration(
                    color: AppTheme.vinotintoTint,
                    borderRadius: BorderRadius.circular(8),
                    border: Border.all(color: AppTheme.oroBorde),
                  ),
                  child: Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      const Icon(Icons.calendar_today, size: 12, color: AppTheme.vinotinto),
                      const SizedBox(width: 4),
                      DropdownButtonHideUnderline(
                        child: DropdownButton<String>(
                          value: provider.selectedYearFilter,
                          isDense: true,
                          icon: const Icon(Icons.arrow_drop_down, color: AppTheme.vinotinto, size: 16),
                          style: const TextStyle(color: AppTheme.vinotinto, fontSize: 11, fontWeight: FontWeight.bold),
                          items: years.map((y) {
                            return DropdownMenuItem<String>(
                              value: y,
                              child: Text(y == 'TODOS' ? 'Año: Todos' : 'Año: $y'),
                            );
                          }).toList(),
                          onChanged: (y) {
                            if (y != null) {
                              provider.setYearFilter(y);
                            }
                          },
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),

          // Cuerpo de la pantalla con Pull to Refresh
          Expanded(
            child: RefreshIndicator(
              color: AppTheme.vinotinto,
              onRefresh: () => provider.cargarFilasPestana(),
              child: CustomScrollView(
                physics: const AlwaysScrollableScrollPhysics(),
                slivers: [
                  // Métricas
                  SliverToBoxAdapter(
                    child: Padding(
                      padding: const EdgeInsets.fromLTRB(16, 12, 16, 6),
                      child: Row(
                        children: [
                          _buildMetricCard(
                            title: 'Causas',
                            value: '${provider.totalCausasTab}',
                            icon: Icons.folder_special,
                            color: AppTheme.vinotinto,
                          ),
                          const SizedBox(width: 8),
                          _buildMetricCard(
                            title: 'Activas',
                            value: '${provider.causasActivasTab}',
                            icon: Icons.check_circle_outline,
                            color: AppTheme.estadoActiva,
                          ),
                          const SizedBox(width: 8),
                          _buildMetricCard(
                            title: 'Cerradas',
                            value: '${provider.causasCerradasTab}',
                            icon: Icons.archive_outlined,
                            color: AppTheme.estadoCerrada,
                          ),
                          const SizedBox(width: 8),
                          _buildMetricCard(
                            title: 'Nómina',
                            value: '${provider.abogadosActivos.length}',
                            icon: Icons.people_outline,
                            color: AppTheme.oroDark,
                            onTap: isAdmin
                                ? () {
                                    Navigator.push(
                                      context,
                                      MaterialPageRoute(builder: (_) => const AbogadosAdminScreen()),
                                    );
                                  }
                                : null,
                          ),
                        ],
                      ),
                    ),
                  ),

                  // Buscador en tiempo real
                  SliverToBoxAdapter(
                    child: Padding(
                      padding: const EdgeInsets.fromLTRB(16, 6, 16, 6),
                      child: TextField(
                        controller: _searchCtrl,
                        onChanged: (val) => provider.setSearchQuery(val),
                        decoration: InputDecoration(
                          hintText: 'Buscar en ${currentTab.title}...',
                          prefixIcon: const Icon(Icons.search, color: AppTheme.vinotinto, size: 20),
                          suffixIcon: _searchCtrl.text.isNotEmpty
                              ? IconButton(
                                  icon: const Icon(Icons.clear, size: 16),
                                  onPressed: () {
                                    _searchCtrl.clear();
                                    provider.setSearchQuery('');
                                  },
                                )
                              : null,
                        ),
                      ),
                    ),
                  ),

                  // Filtros por Estado
                  SliverToBoxAdapter(
                    child: Container(
                      height: 38,
                      margin: const EdgeInsets.symmetric(vertical: 4),
                      child: ListView.separated(
                        padding: const EdgeInsets.symmetric(horizontal: 16),
                        scrollDirection: Axis.horizontal,
                        itemCount: _estadosFiltro.length,
                        separatorBuilder: (_, __) => const SizedBox(width: 8),
                        itemBuilder: (ctx, i) {
                          final est = _estadosFiltro[i];
                          final isSel = provider.selectedEstadoFilter == est;

                          return ChoiceChip(
                            label: Text(est),
                            selected: isSel,
                            selectedColor: AppTheme.vinotinto,
                            backgroundColor: Colors.white,
                            labelStyle: TextStyle(
                              color: isSel ? Colors.white : AppTheme.textoPrincipal,
                              fontWeight: isSel ? FontWeight.bold : FontWeight.w500,
                              fontSize: 11,
                            ),
                            side: BorderSide(
                              color: isSel ? AppTheme.oro : AppTheme.oroBordeSuave,
                              width: 1.2,
                            ),
                            showCheckmark: false,
                            onSelected: (_) => provider.setEstadoFilter(est),
                          );
                        },
                      ),
                    ),
                  ),

                  // Listado dinámico de filas cargadas de esta pestaña
                  provider.isLoading
                      ? const SliverFillRemaining(
                          child: Center(
                            child: CircularProgressIndicator(color: AppTheme.vinotinto),
                          ),
                        )
                      : provider.filteredRows.isEmpty
                          ? SliverFillRemaining(
                              hasScrollBody: false,
                              child: Center(
                                child: Column(
                                  mainAxisAlignment: MainAxisAlignment.center,
                                  children: [
                                    Container(
                                      padding: const EdgeInsets.all(20),
                                      decoration: BoxDecoration(
                                        color: AppTheme.vinotintoTint,
                                        shape: BoxShape.circle,
                                        border: Border.all(color: AppTheme.oroBordeSuave),
                                      ),
                                      child: const Icon(Icons.folder_off_outlined, size: 48, color: AppTheme.vinotinto),
                                    ),
                                    const SizedBox(height: 12),
                                    Text(
                                      'No se encontraron causas en "${currentTab.title}"',
                                      style: const TextStyle(fontSize: 15, fontWeight: FontWeight.bold, color: AppTheme.vinotinto),
                                      textAlign: TextAlign.center,
                                    ),
                                    const SizedBox(height: 4),
                                    const Text(
                                      'Prueba cambiando el filtro de año o busca otro término.',
                                      style: TextStyle(fontSize: 12, color: AppTheme.textoSecundario),
                                    ),
                                  ],
                                ),
                              ),
                            )
                          : SliverPadding(
                              padding: const EdgeInsets.fromLTRB(16, 8, 16, 80),
                              sliver: SliverList(
                                delegate: SliverChildBuilderDelegate(
                                  (ctx, index) {
                                    final row = provider.filteredRows[index];
                                    return _buildRowCard(context, row, index + 1, currentTab);
                                  },
                                  childCount: provider.filteredRows.length,
                                ),
                              ),
                            ),
                ],
              ),
            ),
          ),
        ],
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () => _abrirSelectorPestanas(context),
        backgroundColor: AppTheme.oro,
        icon: const Icon(Icons.add_circle, color: AppTheme.vinotintoDark),
        label: const Text(
          'Crear Causa PGET',
          style: TextStyle(
            color: AppTheme.vinotintoDark,
            fontWeight: FontWeight.w900,
            letterSpacing: 0.3,
          ),
        ),
      ),
    );
  }

  Widget _buildRowCard(BuildContext context, List<dynamic> row, int index, PgetTab tab) {
    String getVal(int i) {
      if (i < row.length && row[i] != null) return row[i].toString().trim();
      return '';
    }

    final expIdx = tab.columns.indexWhere((c) => c.toUpperCase().contains('EXPEDIENTE') || c.toUpperCase().contains('INVESTIGACION'));
    final motivoIdx = tab.columns.indexWhere((c) => c.toUpperCase().contains('MOTIVO') || c.toUpperCase().contains('DELITO'));
    final demandadoIdx = tab.columns.indexWhere((c) => c.toUpperCase().contains('DEMANDADO') || c.toUpperCase().contains('QUERELLADO') || c.toUpperCase().contains('IMPUTADO'));
    final abgIdx = tab.columns.indexWhere((c) => c.toUpperCase().contains('ABG') || c.toUpperCase().contains('RESPONSABLE'));
    final estadoIdx = tab.columns.indexWhere((c) => c.toUpperCase().contains('ESTADO'));

    final expediente = expIdx != -1 ? getVal(expIdx) : 'Fila $index';
    final motivo = motivoIdx != -1 ? getVal(motivoIdx) : 'Asunto registrado';
    final demandado = demandadoIdx != -1 ? getVal(demandadoIdx) : '';
    final abogado = abgIdx != -1 ? getVal(abgIdx) : '';
    final estado = estadoIdx != -1 ? getVal(estadoIdx) : 'ACTIVA';

    final isActiva = estado.toUpperCase().contains('ACTIV');
    final estadoColor = isActiva ? AppTheme.estadoActiva : AppTheme.estadoCerrada;

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
      child: Material(
        color: Colors.transparent,
        borderRadius: BorderRadius.circular(16),
        child: InkWell(
          borderRadius: BorderRadius.circular(16),
          onTap: () {
            final causa = CausaJudicial.fromTabRow(tab, row, rowIndex: index);
            Navigator.push(
              context,
              MaterialPageRoute(builder: (_) => CausaDetailScreen(causa: causa)),
            );
          },
          child: Padding(
            padding: const EdgeInsets.all(14),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                      decoration: BoxDecoration(
                        color: AppTheme.vinotinto,
                        borderRadius: BorderRadius.circular(6),
                        border: Border.all(color: AppTheme.oro),
                      ),
                      child: Text(
                        expediente.isNotEmpty ? 'EXP. $expediente' : 'REGISTRO #$index',
                        style: const TextStyle(color: Colors.white, fontSize: 11, fontWeight: FontWeight.bold),
                      ),
                    ),
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                      decoration: BoxDecoration(
                        color: estadoColor.withOpacity(0.12),
                        borderRadius: BorderRadius.circular(12),
                        border: Border.all(color: estadoColor, width: 1),
                      ),
                      child: Text(
                        estado.isNotEmpty ? estado : 'ACTIVA',
                        style: TextStyle(color: estadoColor, fontSize: 10, fontWeight: FontWeight.bold),
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 8),
                Text(
                  motivo.isNotEmpty ? motivo : 'Sin motivo registrado',
                  style: const TextStyle(fontSize: 14, fontWeight: FontWeight.bold, color: AppTheme.vinotinto),
                  maxLines: 2,
                  overflow: TextOverflow.ellipsis,
                ),
                if (demandado.isNotEmpty) ...[
                  const SizedBox(height: 4),
                  Text(
                    'Contra: $demandado',
                    style: const TextStyle(fontSize: 12, color: AppTheme.textoSecundario),
                    maxLines: 1,
                    overflow: TextOverflow.ellipsis,
                  ),
                ],
                const SizedBox(height: 10),
                const Divider(height: 1, color: AppTheme.bordeDivisor),
                const SizedBox(height: 8),
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Expanded(
                      child: Row(
                        children: [
                          const Icon(Icons.badge_outlined, size: 14, color: AppTheme.oroDark),
                          const SizedBox(width: 4),
                          Expanded(
                            child: Text(
                              abogado.isNotEmpty ? abogado : 'Sin asignar',
                              style: const TextStyle(fontSize: 11, fontWeight: FontWeight.bold, color: AppTheme.vinotinto),
                              overflow: TextOverflow.ellipsis,
                            ),
                          ),
                        ],
                      ),
                    ),
                    const SizedBox(width: 8),
                    Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        InkWell(
                          onTap: () {
                            final causa = CausaJudicial.fromTabRow(tab, row, rowIndex: index);
                            Navigator.push(
                              context,
                              MaterialPageRoute(builder: (_) => CausaFormScreen(causaAEditar: causa)),
                            );
                          },
                          child: Container(
                            padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 3),
                            decoration: BoxDecoration(
                              color: AppTheme.vinotintoTint,
                              borderRadius: BorderRadius.circular(6),
                              border: Border.all(color: AppTheme.oroBordeSuave),
                            ),
                            child: const Row(
                              children: [
                                Icon(Icons.edit, size: 11, color: AppTheme.vinotinto),
                                SizedBox(width: 3),
                                Text('Editar', style: TextStyle(fontSize: 10, fontWeight: FontWeight.bold, color: AppTheme.vinotinto)),
                              ],
                            ),
                          ),
                        ),
                        const SizedBox(width: 6),
                        InkWell(
                          onTap: () {
                            final causa = CausaJudicial.fromTabRow(tab, row, rowIndex: index);
                            _mostrarDialogoEliminar(context, causa);
                          },
                          child: Container(
                            padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 3),
                            decoration: BoxDecoration(
                              color: Colors.red.shade50,
                              borderRadius: BorderRadius.circular(6),
                              border: Border.all(color: Colors.red.shade200),
                            ),
                            child: const Row(
                              children: [
                                Icon(Icons.delete_outline, size: 11, color: Colors.red),
                                SizedBox(width: 3),
                                Text('Eliminar', style: TextStyle(fontSize: 10, fontWeight: FontWeight.bold, color: Colors.red)),
                              ],
                            ),
                          ),
                        ),
                      ],
                    ),
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
