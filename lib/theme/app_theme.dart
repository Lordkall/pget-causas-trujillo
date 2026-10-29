import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class AppTheme {
  // Paleta Institucional Procuraduría General del Estado Trujillo
  static const Color vinotinto = Color(0xFF6B1226);       // Vinotinto Principal
  static const Color vinotintoDark = Color(0xFF480C19);   // Vinotinto Oscuro
  static const Color vinotintoLight = Color(0xFF8B1E38);  // Vinotinto Medio
  static const Color vinotintoTint = Color(0xFFFDF2F4);   // Tinte suave de fondo

  // Acentos y Bordes Dorados
  static const Color oro = Color(0xFFD4AF37);             // Oro Clásico
  static const Color oroBright = Color(0xFFFFD700);       // Oro Brillante
  static const Color oroDark = Color(0xFFA6801E);         // Oro Envejecido
  static const Color oroBorde = Color(0xFFC5A059);        // Oro para bordes
  static const Color oroBordeSuave = Color(0xFFEADBBE);   // Borde dorado suave

  // Superficies y Textos
  static const Color fondoBlanco = Color(0xFFFDFDFE);     // Blanco puro / institucional
  static const Color tarjetaBlanca = Colors.white;
  static const Color textoPrincipal = Color(0xFF1E293B);  // Gris carbón ejecutivo
  static const Color textoSecundario = Color(0xFF64748B); // Gris medio
  static const Color bordeDivisor = Color(0xFFE2E8F0);

  // Estados de Causas
  static const Color estadoActiva = Color(0xFF15803D);    // Verde Esmeralda
  static const Color estadoCerrada = Color(0xFF475569);   // Gris pizarra
  static const Color estadoTramite = Color(0xFFD97706);   // Ámbar

  static ThemeData get lightTheme {
    return ThemeData(
      useMaterial3: true,
      colorScheme: ColorScheme.fromSeed(
        seedColor: vinotinto,
        primary: vinotinto,
        secondary: oro,
        surface: tarjetaBlanca,
        background: fondoBlanco,
      ),
      scaffoldBackgroundColor: fondoBlanco,
      textTheme: GoogleFonts.outfitTextTheme().copyWith(
        headlineMedium: GoogleFonts.outfit(
          fontSize: 22,
          fontWeight: FontWeight.w700,
          color: vinotinto,
          letterSpacing: 0.2,
        ),
        titleLarge: GoogleFonts.outfit(
          fontSize: 17,
          fontWeight: FontWeight.w600,
          color: vinotinto,
        ),
        bodyLarge: GoogleFonts.outfit(
          fontSize: 15,
          color: textoPrincipal,
        ),
        bodyMedium: GoogleFonts.outfit(
          fontSize: 13,
          color: textoSecundario,
        ),
      ),
      appBarTheme: AppBarTheme(
        backgroundColor: vinotinto,
        foregroundColor: Colors.white,
        elevation: 0,
        centerTitle: false,
        titleTextStyle: GoogleFonts.outfit(
          fontSize: 18,
          fontWeight: FontWeight.w700,
          color: Colors.white,
          letterSpacing: 0.3,
        ),
      ),
      cardTheme: CardTheme(
        color: tarjetaBlanca,
        elevation: 1.5,
        shadowColor: vinotinto.withOpacity(0.08),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(16),
          side: const BorderSide(color: oroBorde, width: 1.2),
        ),
      ),
      inputDecorationTheme: InputDecorationTheme(
        filled: true,
        fillColor: Colors.white,
        contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(12),
          borderSide: const BorderSide(color: oroBordeSuave, width: 1),
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(12),
          borderSide: const BorderSide(color: oroBordeSuave, width: 1),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(12),
          borderSide: const BorderSide(color: oro, width: 1.8),
        ),
        errorBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(12),
          borderSide: const BorderSide(color: Colors.redAccent, width: 1.2),
        ),
        labelStyle: const TextStyle(color: textoSecundario, fontSize: 13),
        hintStyle: const TextStyle(color: Color(0xFF94A3B8), fontSize: 13),
        prefixIconColor: vinotinto,
      ),
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          backgroundColor: vinotinto,
          foregroundColor: Colors.white,
          elevation: 2,
          padding: const EdgeInsets.symmetric(horizontal: 22, vertical: 14),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(12),
            side: const BorderSide(color: oro, width: 1),
          ),
          textStyle: GoogleFonts.outfit(
            fontSize: 15,
            fontWeight: FontWeight.w600,
            letterSpacing: 0.4,
          ),
        ),
      ),
      floatingActionButtonTheme: FloatingActionButtonThemeData(
        backgroundColor: oro,
        foregroundColor: vinotintoDark,
        elevation: 4,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(16),
          side: const BorderSide(color: vinotinto, width: 1),
        ),
      ),
    );
  }
}
