# Procuraduría General del Estado Trujillo (PGET) • Sistema de Causas Jurídicas

Aplicación móvil y multiplataforma oficial para la **Procuraduría General del Estado Trujillo (PGET)** diseñada en **Blanco, Vinotinto Institucional y Bordes Dorados**, con conexión en tiempo real a las **17 materias jurídicas en Google Sheets** (todas excepto `Gráfico1`), formularios adaptados automáticamente a cada columna, nómina activa de 13 abogados oficiales con Dra. Lizamar Briceño como Administradora, autenticación biométrica (Huella Dactilar), animación de mazo judicial al iniciar sesión, módulo de trazabilidad y auditoría, y compilación automática de APK mediante GitHub Actions.

---

## 🏛️ Identidad Visual & Funcionalidades Principales

- **Fondo Institucional**: Palacio de Gobierno del Estado Trujillo con cobertura 100% en Vinotinto institucional (`#4A0A19` / `#380612`).
- **Autenticación Biométrica**: Acceso instantáneo con **Huella Dactilar** vinculada al dispositivo, con pregunta de confirmación en el primer inicio de sesión.
- **Pantalla de Carga Judicial**: Al iniciar sesión se muestra una animación del **Mazo de Juez** golpeando el bloque de resonancia con ondas expansivas de 1,5 segundos.
- **Ícono de Cerrar Sesión Minimalista**: Botón blanco minimalista de trazo fino en la cabecera institucional.
- **Nómina Oficial Activa (13 Abogados A-Z)**:
  - 👑 **Dra. Lizamar Briceño** (`lizamarbriceno@pget.com`) - Administradora
  - ⚖️ 12 Abogados y Procuradora en nivel Abogado procesal.
- **Preservación Histórica (Soft-Delete)**: La edición o retiro de abogados nunca altera las causas históricas existentes en Google Sheets.
- **Módulo de Auditoría**: Trazabilidad completa (Quién, Cuándo, Qué, Expediente y Materia).

---

## 🚀 Compilación Automática del APK con GitHub Actions

El repositorio incluye un workflow de GitHub Actions en `.github/workflows/build_apk.yml` que compila automáticamente el archivo APK para Android cada vez que se hace un `git push` a la rama `main`.

### Pasos para vincular su repositorio y obtener el APK:

1. **Crear un nuevo repositorio en GitHub** (ejemplo: `pget-causas-trujillo`).
2. **Vincular y subir el proyecto desde la terminal**:
   ```bash
   git remote add origin https://github.com/SU_USUARIO/pget-causas-trujillo.git
   git branch -M main
   git push -u origin main
   ```
3. **Descargar el APK compilado**:
   - Vaya a la pestaña **Actions** en su repositorio de GitHub.
   - Seleccione la ejecución más reciente de **Build Android APK Release**.
   - En la sección **Artifacts**, descargue el archivo zip con el APK: `PGET-Causas-Juridicas-release.apk`.
   - ¡Instálelo directamente en cualquier teléfono o tablet Android!

---

## 👥 Nómina Institucional de Cuentas Activas

| Nº | Funcionario / Abogado | Cédula | Cargo | Correo Institucional | Clave Generada | Rol |
| :---: | :--- | :---: | :--- | :--- | :--- | :---: |
| 1 | BARRIOS JULIO ALEXANDER | 14.459.865 | ABOGADO I | `juliobarrios@pget.com` | `Pget2026*Julio` | Abogado |
| 2 | BARRIOS MARIA ALCIRA | 17.037.437 | ABOGADO I | `mariabarrios@pget.com` | `Pget2026*MariaB` | Abogado |
| 3 | BRICEÑO FERNANDEZ ARMANDO JOSE | 5.780.167 | ABOGADO | `armandobriceno@pget.com` | `Pget2026*Armando` | Abogado |
| 4 | BRICEÑO VALECILLOS LIZAMAR INDIRA | 20.400.747 | DIR. ASUNTOS JURÍDICOS | `lizamarbriceno@pget.com` | `Admin2026*Lizamar` | **ADMIN** 👑 |
| 5 | DE ABREU HERNANDEZ CARLOS EDUARDO | 10.446.852 | ABOGADO I | `carlosdeabreu@pget.com` | `Pget2026*Carlos` | Abogado |
| 6 | DORA ALICIA MATHEUS | 10.035.929 | PROCURADORA | `doramatheus@pget.com` | `Pget2026*Dora` | Abogado |
| 7 | MERCADO HIDALGO ROXANNA KAROLINA | 23.596.460 | ABOGADO I | `roxannamercado@pget.com` | `Pget2026*Roxanna` | Abogado |
| 8 | MOLINA UZCATEGUI HUMBERTO JOSE | 20.790.382 | ABOGADO | `humbertomolina@pget.com` | `Pget2026*Humberto` | Abogado |
| 9 | MORENO HERNANDEZ YONEXI CAROLINA | 16.738.909 | ABOGADO | `yoneximoreno@pget.com` | `Pget2026*Yonexi` | Abogado |
| 10 | OJEDA NUÑEZ MARIA DE LOS ANGELES | 26.046.163 | ABOGADO I | `mariaojeda@pget.com` | `Pget2026*MariaO` | Abogado |
| 11 | RAMIREZ OROPEZA TATIANA MARILIN | 15.315.709 | ABOGADO I | `tatianaramirez@pget.com` | `Pget2026*Tatiana` | Abogado |
| 12 | SANCHEZ MONSALVE LILIBETH DAYANA | 13.404.142 | ABOGADO I | `lilibethsanchez@pget.com` | `Pget2026*Lilibeth` | Abogado |
| 13 | VALE VALERA YULIANOVA PAOLA | 26.591.763 | ABOGADO I | `paolavale@pget.com` | `Pget2026*Paola` | Abogado |
