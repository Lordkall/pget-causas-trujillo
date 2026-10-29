import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'providers/abogados_provider.dart';
import 'screens/home_screen.dart';
import 'screens/login_screen.dart';
import 'theme/app_theme.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(const PgetDataAbogadosApp());
}

class PgetDataAbogadosApp extends StatelessWidget {
  const PgetDataAbogadosApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => AbogadosProvider()),
      ],
      child: Consumer<AbogadosProvider>(
        builder: (context, provider, _) {
          return MaterialApp(
            title: 'Procuraduría General del Estado Trujillo • Causas Jurídicas',
            debugShowCheckedModeBanner: false,
            theme: AppTheme.lightTheme,
            home: provider.isAuthenticated ? const HomeScreen() : const LoginScreen(),
          );
        },
      ),
    );
  }
}
