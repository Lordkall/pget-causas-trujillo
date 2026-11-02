import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'providers/abogados_provider.dart';
import 'screens/home_screen.dart';
import 'screens/login_screen.dart';
import 'theme/app_theme.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  final provider = AbogadosProvider();
  await provider.verificarSesionGuardada();
  runApp(PgetDataAbogadosApp(provider: provider));
}

class PgetDataAbogadosApp extends StatelessWidget {
  final AbogadosProvider provider;
  const PgetDataAbogadosApp({Key? key, required this.provider}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider.value(value: provider),
      ],
      child: Consumer<AbogadosProvider>(
        builder: (context, p, _) {
          return MaterialApp(
            title: 'Procuraduría General del Estado Trujillo • Causas Jurídicas',
            debugShowCheckedModeBanner: false,
            theme: AppTheme.lightTheme,
            home: p.isAuthenticated ? const HomeScreen() : const LoginScreen(),
          );
        },
      ),
    );
  }
}
