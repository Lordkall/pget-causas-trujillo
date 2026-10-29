import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../models/pget_tab.dart';
import '../providers/abogados_provider.dart';
import '../theme/app_theme.dart';
import 'causa_form_screen.dart';

class SelectTabModal extends StatelessWidget {
  const SelectTabModal({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final provider = context.read<AbogadosProvider>();
    final tabs = provider.tabs;

    // Agrupar por categoría
    final Map<String, List<PgetTab>> categorias = {};
    for (final t in tabs) {
      if (!categorias.containsKey(t.category)) {
        categorias[t.category] = [];
      }
      categorias[t.category]!.add(t);
    }

    return Container(
      height: MediaQuery.of(context).size.height * 0.85,
      decoration: const BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.vertical(top: Radius.circular(24)),
        border: Border(top: BorderSide(color: AppTheme.oro, width: 2.5)),
      ),
      child: Column(
        children: [
          // Cabecera Modal
          Container(
            padding: const EdgeInsets.fromLTRB(20, 16, 16, 12),
            decoration: const BoxDecoration(
              color: AppTheme.vinotinto,
              borderRadius: BorderRadius.vertical(top: Radius.circular(21)),
              border: Border(bottom: BorderSide(color: AppTheme.oro, width: 1.5)),
            ),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                const Row(
                  children: [
                    Icon(Icons.dashboard_customize_outlined, color: AppTheme.oro, size: 22),
                    SizedBox(width: 10),
                    Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          'Selecciona la Materia / Instancia',
                          style: TextStyle(color: Colors.white, fontSize: 15, fontWeight: FontWeight.bold),
                        ),
                        Text(
                          'Pestañas oficiales de Google Sheets (PGET)',
                          style: TextStyle(color: AppTheme.oro, fontSize: 11),
                        ),
                      ],
                    ),
                  ],
                ),
                IconButton(
                  icon: const Icon(Icons.close, color: Colors.white),
                  onPressed: () => Navigator.pop(context),
                ),
              ],
            ),
          ),

          // Lista de categorías y pestañas
          Expanded(
            child: ListView.builder(
              padding: const EdgeInsets.all(16),
              itemCount: categorias.keys.length,
              itemBuilder: (ctx, idx) {
                final categoriaNombre = categorias.keys.elementAt(idx);
                final tabsDeCategoria = categorias[categoriaNombre]!;

                return Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Padding(
                      padding: const EdgeInsets.only(top: 8, bottom: 8),
                      child: Row(
                        children: [
                          Container(width: 4, height: 16, color: AppTheme.oro),
                          const SizedBox(width: 8),
                          Text(
                            categoriaNombre.toUpperCase(),
                            style: const TextStyle(
                              fontSize: 12,
                              fontWeight: FontWeight.w800,
                              color: AppTheme.vinotinto,
                              letterSpacing: 0.5,
                            ),
                          ),
                        ],
                      ),
                    ),
                    ...tabsDeCategoria.map((tab) {
                      return Container(
                        margin: const EdgeInsets.only(bottom: 8),
                        decoration: BoxDecoration(
                          color: AppTheme.fondoBlanco,
                          borderRadius: BorderRadius.circular(12),
                          border: Border.all(color: AppTheme.oroBorde, width: 1.2), // Bordes dorados
                        ),
                        child: ListTile(
                          contentPadding: const EdgeInsets.symmetric(horizontal: 14, vertical: 2),
                          leading: Container(
                            padding: const EdgeInsets.all(8),
                            decoration: BoxDecoration(
                              color: AppTheme.vinotinto,
                              borderRadius: BorderRadius.circular(10),
                              border: Border.all(color: AppTheme.oro, width: 1),
                            ),
                            child: Icon(tab.icon, color: AppTheme.oro, size: 18),
                          ),
                          title: Text(
                            tab.title,
                            style: const TextStyle(
                              fontSize: 13,
                              fontWeight: FontWeight.bold,
                              color: AppTheme.vinotinto,
                            ),
                          ),
                          subtitle: Text(
                            '${tab.columns.length} columnas configuradas',
                            style: const TextStyle(fontSize: 11, color: AppTheme.textoSecundario),
                          ),
                          trailing: const Icon(Icons.arrow_forward_ios, size: 14, color: AppTheme.oro),
                          onTap: () {
                            Navigator.pop(context);
                            Navigator.push(
                              context,
                              MaterialPageRoute(
                                builder: (_) => CausaFormScreen(tab: tab),
                              ),
                            );
                          },
                        ),
                      );
                    }).toList(),
                    const SizedBox(height: 6),
                  ],
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}

