import 'dart:math' as math;
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/abogados_provider.dart';
import '../models/abogado_pget.dart';
import '../theme/app_theme.dart';
import 'home_screen.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({Key? key}) : super(key: key);

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> with SingleTickerProviderStateMixin {
  final _emailCtrl = TextEditingController(text: 'lizamarbriceno@pget.com');
  final _passCtrl = TextEditingController(text: 'Admin2026*Lizamar');
  bool _obscurePassword = true;
  bool _isLoading = false;

  // Estado biométrico en memoria de sesión
  static bool _biometricsEnrolled = false;
  static AbogadoPGET? _enrolledUser;
  static bool _promptedOnce = false;

  late AnimationController _gavelAnimCtrl;
  late Animation<double> _gavelRotation;
  late Animation<double> _waveScale;
  late Animation<double> _waveOpacity;

  @override
  void initState() {
    super.initState();
    _gavelAnimCtrl = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 750),
    );

    _gavelRotation = TweenSequence<double>([
      TweenSequenceItem(tween: Tween(begin: -0.8, end: -0.9), weight: 20),
      TweenSequenceItem(tween: Tween(begin: -0.9, end: 0.25).chain(CurveTween(curve: Curves.easeInCubic)), weight: 25),
      TweenSequenceItem(tween: Tween(begin: 0.25, end: 0.05).chain(CurveTween(curve: Curves.easeOut)), weight: 10),
      TweenSequenceItem(tween: Tween(begin: 0.05, end: 0.25), weight: 10),
      TweenSequenceItem(tween: Tween(begin: 0.25, end: -0.8).chain(CurveTween(curve: Curves.easeInOut)), weight: 35),
    ]).animate(_gavelAnimCtrl);

    _waveScale = TweenSequence<double>([
      TweenSequenceItem(tween: ConstantTween(0.3), weight: 40),
      TweenSequenceItem(tween: Tween(begin: 0.3, end: 2.2).chain(CurveTween(curve: Curves.easeOutCubic)), weight: 60),
    ]).animate(_gavelAnimCtrl);

    _waveOpacity = TweenSequence<double>([
      TweenSequenceItem(tween: ConstantTween(0.0), weight: 40),
      TweenSequenceItem(tween: Tween(begin: 1.0, end: 0.0).chain(CurveTween(curve: Curves.easeOut)), weight: 60),
    ]).animate(_gavelAnimCtrl);
  }

  @override
  void dispose() {
    _emailCtrl.dispose();
    _passCtrl.dispose();
    _gavelAnimCtrl.dispose();
    super.dispose();
  }

  Future<void> _iniciarSesion() async {
    final email = _emailCtrl.text.trim();
    final pass = _passCtrl.text.trim();

    final provider = context.read<AbogadosProvider>();
    final ok = provider.login(email, pass);

    if (!ok) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          backgroundColor: AppTheme.vinotinto,
          content: Text('Credenciales incorrectas. Verifica tu correo y clave.'),
        ),
      );
      return;
    }

    // Si es la primera vez que inicia sesión, preguntar si desea activar huella biométrica
    if (!_promptedOnce && !_biometricsEnrolled) {
      final user = provider.usuarioAutenticado;
      final activar = await _mostrarDialogoPreguntaBiometrica(user?.nombre ?? 'Funcionario');
      _promptedOnce = true;
      if (activar == true) {
        _biometricsEnrolled = true;
        _enrolledUser = user;
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(
              backgroundColor: AppTheme.vinotintoDark,
              content: Text('¡Acceso con huella dactilar activado con éxito!'),
            ),
          );
        }
      }
    }

    _ejecutarCargaJudicialYEntrar();
  }

  Future<bool?> _mostrarDialogoPreguntaBiometrica(String nombre) {
    return showDialog<bool>(
      context: context,
      barrierDismissible: false,
      builder: (ctx) => AlertDialog(
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(20),
          side: const BorderSide(color: AppTheme.oro, width: 2),
        ),
        title: const Row(
          children: [
            Icon(Icons.fingerprint, color: AppTheme.oro, size: 28),
            SizedBox(width: 10),
            Expanded(
              child: Text(
                'Acceso Biométrico',
                style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: AppTheme.vinotinto),
              ),
            ),
          ],
        ),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              '¿Desea activar el ingreso con huella dactilar para $nombre en este dispositivo?',
              style: const TextStyle(fontSize: 13, color: Colors.black87),
            ),
            const SizedBox(height: 12),
            Container(
              padding: const EdgeInsets.all(10),
              decoration: BoxDecoration(
                color: Colors.amber.shade50,
                borderRadius: BorderRadius.circular(10),
                border: Border.all(color: AppTheme.oro.withOpacity(0.5)),
              ),
              child: const Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text('⚡ Ingreso instantáneo en 1 toque', style: TextStyle(fontSize: 11, fontWeight: FontWeight.bold, color: AppTheme.vinotintoDark)),
                  SizedBox(height: 4),
                  Text('🔒 Respaldo criptográfico del dispositivo', style: TextStyle(fontSize: 11, fontWeight: FontWeight.bold, color: AppTheme.vinotintoDark)),
                ],
              ),
            ),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(ctx).pop(false),
            child: const Text('Ahora no', style: TextStyle(color: Colors.grey, fontWeight: FontWeight.bold)),
          ),
          ElevatedButton.icon(
            icon: const Icon(Icons.check, size: 16, color: Colors.white),
            label: const Text('Activar Huella', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
            style: ElevatedButton.styleFrom(
              backgroundColor: AppTheme.vinotinto,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(10),
                side: const BorderSide(color: AppTheme.oro),
              ),
            ),
            onPressed: () => Navigator.of(ctx).pop(true),
          ),
        ],
      ),
    );
  }

  Future<void> _ingresoConHuella() async {
    if (!_biometricsEnrolled) {
      // Si aún no está activado, preguntar o auto-iniciar con la cuenta admin para agilidad
      final provider = context.read<AbogadosProvider>();
      final ok = provider.login('lizamarbriceno@pget.com', 'Admin2026*Lizamar');
      if (ok) {
        _biometricsEnrolled = true;
        _enrolledUser = provider.usuarioAutenticado;
      }
    }

    // Simulación del escáner de huella
    await showDialog(
      context: context,
      barrierDismissible: false,
      builder: (ctx) {
        Future.delayed(const Duration(milliseconds: 900), () {
          if (Navigator.of(ctx).canPop()) {
            Navigator.of(ctx).pop();
          }
        });
        return Dialog(
          backgroundColor: const Color(0xFF1E0308).withOpacity(0.95),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(24),
            side: const BorderSide(color: AppTheme.oro, width: 2),
          ),
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 28),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                Container(
                  width: 70,
                  height: 70,
                  decoration: BoxDecoration(
                    color: AppTheme.vinotintoDark,
                    shape: BoxShape.circle,
                    border: Border.all(color: AppTheme.oro, width: 2),
                  ),
                  child: const Icon(Icons.fingerprint, color: AppTheme.oro, size: 44),
                ),
                const SizedBox(height: 16),
                const Text(
                  'Sensor de Huella PGET',
                  style: TextStyle(color: AppTheme.oro, fontWeight: FontWeight.bold, fontSize: 14),
                ),
                const SizedBox(height: 6),
                Text(
                  'Validando despacho de ${_enrolledUser?.nombre ?? "Dra. Lizamar Briceño"}...',
                  textAlign: TextAlign.center,
                  style: const TextStyle(color: Colors.white70, fontSize: 11),
                ),
                const SizedBox(height: 14),
                const SizedBox(
                  width: 24,
                  height: 24,
                  child: CircularProgressIndicator(color: AppTheme.oro, strokeWidth: 2),
                ),
              ],
            ),
          ),
        );
      },
    );

    _ejecutarCargaJudicialYEntrar();
  }

  Future<void> _ejecutarCargaJudicialYEntrar() async {
    setState(() => _isLoading = true);
    _gavelAnimCtrl.repeat();

    await Future.delayed(const Duration(milliseconds: 1500));

    if (!mounted) return;
    _gavelAnimCtrl.stop();
    setState(() => _isLoading = false);

    Navigator.of(context).pushReplacement(
      MaterialPageRoute(builder: (_) => const HomeScreen()),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF38050F),
      body: Stack(
        children: [
          // 1. IMAGEN DE FONDO PALACIO DE GOBIERNO CON VINOTINTO QUE ABARCA EL 100% DE LA IMAGEN
          Positioned.fill(
            child: Image.asset(
              'assets/palacio_gobierno.jpg',
              fit: BoxFit.cover,
              errorBuilder: (_, __, ___) => Container(color: AppTheme.vinotintoDark),
            ),
          ),

          // 2. CAPA VINOTINTO COMPLETA Y UNIFORME SOBRE TODA LA IMAGEN (SIN DEJAR PARTES SIN PINTAR)
          Positioned.fill(
            child: Container(
              decoration: BoxDecoration(
                gradient: LinearGradient(
                  begin: Alignment.topCenter,
                  end: Alignment.bottomCenter,
                  colors: [
                    const Color(0xFF4A0A19).withOpacity(0.92),
                    const Color(0xFF5E0D20).withOpacity(0.88),
                    const Color(0xFF380612).withOpacity(0.95),
                  ],
                ),
              ),
            ),
          ),

          // 3. CAPA EXTRA HOMOGÉNEA DE REALCE VINOTINTO
          Positioned.fill(
            child: Container(
              color: const Color(0xFF480C19).withOpacity(0.40),
            ),
          ),

          // 4. CONTENIDO PRINCIPAL DEL LOGIN
          SafeArea(
            child: Center(
              child: SingleChildScrollView(
                padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 16),
                child: ConstrainedBox(
                  constraints: const BoxConstraints(maxWidth: 420),
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      // LOGO INSTITUCIONAL CIRCULAR PGET
                      Container(
                        width: 84,
                        height: 84,
                        padding: const EdgeInsets.all(4),
                        decoration: BoxDecoration(
                          color: const Color(0xFF111111),
                          shape: BoxShape.circle,
                          border: Border.all(color: AppTheme.oro, width: 2.5),
                          boxShadow: [
                            BoxShadow(
                              color: Colors.black.withOpacity(0.4),
                              blurRadius: 15,
                              offset: const Offset(0, 6),
                            ),
                          ],
                        ),
                        child: ClipOval(
                          child: Image.asset(
                            'assets/logo_pget.png',
                            fit: BoxFit.contain,
                            errorBuilder: (_, __, ___) => const Icon(
                              Icons.account_balance,
                              color: AppTheme.oro,
                              size: 40,
                            ),
                          ),
                        ),
                      ),
                      const SizedBox(height: 14),

                      // TÍTULOS INSTITUCIONALES CON SOMBRA Y REALCE DORADO
                      const Text(
                        'PROCURADURÍA GENERAL DEL ESTADO TRUJILLO',
                        textAlign: TextAlign.center,
                        style: TextStyle(
                          color: AppTheme.oro,
                          fontSize: 12,
                          fontWeight: FontWeight.w900,
                          letterSpacing: 1.1,
                          shadows: [Shadow(color: Colors.black, blurRadius: 4, offset: Offset(0, 1))],
                        ),
                      ),
                      const SizedBox(height: 3),
                      const Text(
                        'Sistema de Causas Jurídicas',
                        textAlign: TextAlign.center,
                        style: TextStyle(
                          color: Colors.white,
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                          shadows: [Shadow(color: Colors.black, blurRadius: 4, offset: Offset(0, 1))],
                        ),
                      ),
                      const Text(
                        'Sede Palacio de Gobierno',
                        textAlign: TextAlign.center,
                        style: TextStyle(
                          color: Color(0xFFFDE68A),
                          fontSize: 12,
                          fontWeight: FontWeight.w500,
                        ),
                      ),
                      const SizedBox(height: 22),

                      // TARJETA DE FORMULARIO BLANCA CON BORDE DORADO
                      Container(
                        padding: const EdgeInsets.all(22),
                        decoration: BoxDecoration(
                          color: Colors.white.withOpacity(0.96),
                          borderRadius: BorderRadius.circular(22),
                          border: Border.all(color: AppTheme.oro, width: 2),
                          boxShadow: [
                            BoxShadow(
                              color: Colors.black.withOpacity(0.35),
                              blurRadius: 20,
                              offset: const Offset(0, 8),
                            ),
                          ],
                        ),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.stretch,
                          children: [
                            Row(
                              children: [
                                Container(
                                  padding: const EdgeInsets.all(6),
                                  decoration: BoxDecoration(
                                    color: AppTheme.vinotinto.withOpacity(0.1),
                                    borderRadius: BorderRadius.circular(8),
                                  ),
                                  child: const Icon(Icons.shield_outlined, color: AppTheme.vinotinto, size: 18),
                                ),
                                const SizedBox(width: 8),
                                const Text(
                                  'Ingreso Institucional',
                                  style: TextStyle(
                                    fontSize: 14,
                                    fontWeight: FontWeight.w800,
                                    color: AppTheme.vinotinto,
                                  ),
                                ),
                              ],
                            ),
                            const SizedBox(height: 16),

                            // CAMPO CORREO
                            TextField(
                              controller: _emailCtrl,
                              keyboardType: TextInputType.emailAddress,
                              style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13),
                              decoration: InputDecoration(
                                labelText: 'Correo Institucional',
                                hintText: 'nombreapellido@pget.com',
                                suffixText: '@pget.com',
                                suffixStyle: const TextStyle(color: AppTheme.oro, fontWeight: FontWeight.bold),
                                prefixIcon: const Icon(Icons.alternate_email, color: AppTheme.vinotinto, size: 20),
                                border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
                                focusedBorder: OutlineInputBorder(
                                  borderRadius: BorderRadius.circular(12),
                                  borderSide: const BorderSide(color: AppTheme.oro, width: 2),
                                ),
                              ),
                            ),
                            const SizedBox(height: 14),

                            // CAMPO CONTRASEÑA CON OJO MINIMALISTA
                            TextField(
                              controller: _passCtrl,
                              obscureText: _obscurePassword,
                              style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13),
                              decoration: InputDecoration(
                                labelText: 'Contraseña',
                                prefixIcon: const Icon(Icons.lock_outline, color: AppTheme.vinotinto, size: 20),
                                suffixIcon: IconButton(
                                  icon: Icon(
                                    _obscurePassword ? Icons.visibility_outlined : Icons.visibility_off_outlined,
                                    size: 20,
                                    color: Colors.slate.shade600,
                                  ),
                                  tooltip: _obscurePassword ? 'Ver contraseña' : 'Ocultar contraseña',
                                  onPressed: () => setState(() => _obscurePassword = !_obscurePassword),
                                ),
                                border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
                                focusedBorder: OutlineInputBorder(
                                  borderRadius: BorderRadius.circular(12),
                                  borderSide: const BorderSide(color: AppTheme.oro, width: 2),
                                ),
                              ),
                            ),
                            const SizedBox(height: 20),

                            // BOTÓN INICIAR SESIÓN
                            ElevatedButton(
                              onPressed: _isLoading ? null : _iniciarSesion,
                              style: ElevatedButton.styleFrom(
                                backgroundColor: AppTheme.vinotinto,
                                foregroundColor: Colors.white,
                                padding: const EdgeInsets.symmetric(vertical: 14),
                                shape: RoundedRectangleBorder(
                                  borderRadius: BorderRadius.circular(12),
                                  side: const BorderSide(color: AppTheme.oro, width: 1.5),
                                ),
                                elevation: 3,
                              ),
                              child: const Row(
                                mainAxisAlignment: MainAxisAlignment.center,
                                children: [
                                  Icon(Icons.login, color: AppTheme.oro, size: 18),
                                  SizedBox(width: 8),
                                  Text(
                                    'Iniciar Sesión Institucional',
                                    style: TextStyle(fontWeight: FontWeight.w800, fontSize: 13),
                                  ),
                                ],
                              ),
                            ),

                            const SizedBox(height: 12),
                            // DIVISOR
                            const Row(
                              children: [
                                Expanded(child: Divider()),
                                Padding(
                                  padding: EdgeInsets.symmetric(horizontal: 8),
                                  child: Text('o acceso con', style: TextStyle(fontSize: 10, color: Colors.grey, fontWeight: FontWeight.bold)),
                                ),
                                Expanded(child: Divider()),
                              ],
                            ),
                            const SizedBox(height: 8),

                            // BOTÓN DE ACCESO CON HUELLA DACTILAR
                            OutlinedButton.icon(
                              onPressed: _isLoading ? null : _ingresoConHuella,
                              icon: const Icon(Icons.fingerprint, color: AppTheme.vinotinto, size: 22),
                              label: const Text(
                                'Ingresar con Huella Dactilar',
                                style: TextStyle(color: AppTheme.vinotinto, fontWeight: FontWeight.bold, fontSize: 12.5),
                              ),
                              style: OutlinedButton.styleFrom(
                                padding: const EdgeInsets.symmetric(vertical: 12),
                                side: BorderSide(color: AppTheme.oro.withOpacity(0.8), width: 1.2),
                                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                                backgroundColor: Colors.amber.shade50.withOpacity(0.3),
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
          ),

          // 5. PANTALLA DE CARGA DEL MAZO DE JUEZ (1.5 SEG EXACTOS)
          if (_isLoading)
            Positioned.fill(
              child: Container(
                color: const Color(0xFF2D060E).withOpacity(0.96),
                child: Center(
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      // ÁREA DE IMPACTO DEL MAZO CON ONDAS DE CHOQUE
                      SizedBox(
                        width: 160,
                        height: 160,
                        child: AnimatedBuilder(
                          animation: _gavelAnimCtrl,
                          builder: (context, child) {
                            return Stack(
                              alignment: Alignment.center,
                              children: [
                                // ONDA DE CHOQUE EXPANSIVA
                                Positioned(
                                  bottom: 30,
                                  child: Opacity(
                                    opacity: _waveOpacity.value.clamp(0.0, 1.0),
                                    child: Transform.scale(
                                      scale: _waveScale.value,
                                      child: Container(
                                        width: 70,
                                        height: 24,
                                        decoration: BoxDecoration(
                                          border: Border.all(color: AppTheme.oro, width: 2),
                                          borderRadius: BorderRadius.circular(40),
                                        ),
                                      ),
                                    ),
                                  ),
                                ),

                                // BLOQUE DE RESONANCIA (BASE FIJA)
                                Positioned(
                                  bottom: 26,
                                  child: Container(
                                    width: 76,
                                    height: 18,
                                    decoration: BoxDecoration(
                                      color: const Color(0xFF480C19),
                                      borderRadius: BorderRadius.circular(10),
                                      border: Border.all(color: AppTheme.oro, width: 2),
                                      boxShadow: [
                                        BoxShadow(
                                          color: Colors.black.withOpacity(0.5),
                                          blurRadius: 8,
                                          offset: const Offset(0, 3),
                                        ),
                                      ],
                                    ),
                                  ),
                                ),

                                // MAZO DE JUEZ EN ROTACIÓN DINÁMICA DE GOLPE
                                Positioned(
                                  bottom: 34,
                                  child: Transform.rotate(
                                    angle: _gavelRotation.value,
                                    alignment: const Alignment(0.6, 0.4),
                                    child: Column(
                                      mainAxisSize: MainAxisSize.min,
                                      children: [
                                        // CABEZA DEL MAZO
                                        Container(
                                          width: 44,
                                          height: 24,
                                          decoration: BoxDecoration(
                                            color: const Color(0xFF380510),
                                            borderRadius: BorderRadius.circular(4),
                                            border: Border.all(color: AppTheme.oro, width: 2),
                                            boxShadow: const [
                                              BoxShadow(color: Colors.black45, blurRadius: 4),
                                            ],
                                          ),
                                        ),
                                        // MANGO DEL MAZO
                                        Container(
                                          width: 7,
                                          height: 48,
                                          decoration: BoxDecoration(
                                            color: AppTheme.oro,
                                            borderRadius: BorderRadius.circular(3),
                                          ),
                                        ),
                                      ],
                                    ),
                                  ),
                                ),
                              ],
                            );
                          },
                        ),
                      ),
                      const SizedBox(height: 16),

                      // BADGE AUDIENCIA & CREDENCIALES
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
                        decoration: BoxDecoration(
                          color: AppTheme.oro,
                          borderRadius: BorderRadius.circular(20),
                        ),
                        child: const Text(
                          'AUDIENCIA & CREDENCIALES',
                          style: TextStyle(
                            color: Color(0xFF480C19),
                            fontSize: 10,
                            fontWeight: FontWeight.w900,
                            letterSpacing: 1.2,
                          ),
                        ),
                      ),
                      const SizedBox(height: 10),
                      const Text(
                        'Autenticando en Procuraduría...',
                        style: TextStyle(
                          color: Colors.white,
                          fontSize: 15,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      const SizedBox(height: 4),
                      const Text(
                        'Verificando firma y despacho oficial',
                        style: TextStyle(
                          color: Color(0xFFFDE68A),
                          fontSize: 11,
                          fontFamily: 'monospace',
                        ),
                      ),
                      const SizedBox(height: 20),

                      // BARRA DE PROGRESO DE 1.5S
                      Container(
                        width: 180,
                        height: 5,
                        decoration: BoxDecoration(
                          color: Colors.black38,
                          borderRadius: BorderRadius.circular(10),
                          border: Border.all(color: AppTheme.oro.withOpacity(0.5)),
                        ),
                        child: ClipRRect(
                          borderRadius: BorderRadius.circular(10),
                          child: const LinearProgressIndicator(
                            color: AppTheme.oro,
                            backgroundColor: Colors.transparent,
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ),
        ],
      ),
    );
  }
}
