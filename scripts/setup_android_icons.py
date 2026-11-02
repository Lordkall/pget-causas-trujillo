import os
import re
from PIL import Image

def generate_icons():
    logo_path = 'assets/circular_logo_pget.png'
    if not os.path.exists(logo_path):
        logo_path = 'assets/logo_pget.png'

    print(f"Using logo from: {logo_path}")
    base_img = Image.open(logo_path).convert('RGBA')

    res_dir = 'android/app/src/main/res'
    if not os.path.exists(res_dir):
        print(f"Warning: {res_dir} does not exist yet. It will be created.")
        os.makedirs(res_dir, exist_ok=True)

    # 1. Definir tamaños estándar de mipmap Android
    mipmap_sizes = {
        'mipmap-mdpi': 48,
        'mipmap-hdpi': 72,
        'mipmap-xhdpi': 96,
        'mipmap-xxhdpi': 144,
        'mipmap-xxxhdpi': 192,
    }

    for folder, size in mipmap_sizes.items():
        folder_path = os.path.join(res_dir, folder)
        os.makedirs(folder_path, exist_ok=True)

        resized = base_img.resize((size, size), Image.Resampling.LANCZOS)
        
        # Guardar ic_launcher.png y ic_launcher_round.png
        icon_path = os.path.join(folder_path, 'ic_launcher.png')
        round_icon_path = os.path.join(folder_path, 'ic_launcher_round.png')
        resized.save(icon_path, 'PNG')
        resized.save(round_icon_path, 'PNG')
        print(f"Generated {size}x{size} icon in {folder_path}")

    # 2. Adaptive Icon Foreground (432x432 con logo centrado en zona segura 288x288)
    drawable_dir = os.path.join(res_dir, 'drawable')
    os.makedirs(drawable_dir, exist_ok=True)

    foreground = Image.new('RGBA', (432, 432), (0, 0, 0, 0))
    logo_adaptive = base_img.resize((288, 288), Image.Resampling.LANCZOS)
    foreground.paste(logo_adaptive, (72, 72), logo_adaptive)
    foreground.save(os.path.join(drawable_dir, 'ic_launcher_foreground.png'), 'PNG')
    print("Generated adaptive ic_launcher_foreground.png (432x432)")

    # 3. Colores institucionales PGET para background
    values_dir = os.path.join(res_dir, 'values')
    os.makedirs(values_dir, exist_ok=True)
    colors_xml = os.path.join(values_dir, 'colors.xml')
    with open(colors_xml, 'w', encoding='utf-8') as f:
        f.write('''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="ic_launcher_background">#6B1226</color>
    <color name="vinotinto_pget">#6B1226</color>
    <color name="oro_pget">#D4AF37</color>
</resources>
''')
    print("Generated colors.xml with #6B1226 vinotinto background")

    # 4. XMLs de Adaptive Icon (Android 8.0+)
    anydpi_dir = os.path.join(res_dir, 'mipmap-anydpi-v26')
    os.makedirs(anydpi_dir, exist_ok=True)

    adaptive_xml_content = '''<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@color/ic_launcher_background"/>
    <foreground android:drawable="@drawable/ic_launcher_foreground"/>
</adaptive-icon>
'''
    with open(os.path.join(anydpi_dir, 'ic_launcher.xml'), 'w', encoding='utf-8') as f:
        f.write(adaptive_xml_content)
    with open(os.path.join(anydpi_dir, 'ic_launcher_round.xml'), 'w', encoding='utf-8') as f:
        f.write(adaptive_xml_content)
    print("Generated adaptive ic_launcher.xml and ic_launcher_round.xml")

    # 5. Splash Screen con Fondo Vinotinto y Logo PGET Centrado
    launch_bg_path = os.path.join(drawable_dir, 'launch_background.xml')
    with open(launch_bg_path, 'w', encoding='utf-8') as f:
        f.write('''<?xml version="1.0" encoding="utf-8"?>
<layer-list xmlns:android="http://schemas.android.com/apk/res/android">
    <item android:drawable="@color/ic_launcher_background" />
    <item>
        <bitmap
            android:gravity="center"
            android:src="@drawable/ic_launcher_foreground" />
    </item>
</layer-list>
''')
    print("Updated launch_background.xml for institutional splash screen")

    # 6. Actualizar AndroidManifest.xml con Título 'PGET Causas' y Logo
    manifest_path = 'android/app/src/main/AndroidManifest.xml'
    if os.path.exists(manifest_path):
        with open(manifest_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Cambiar label
        content = re.sub(r'android:label="[^"]*"', 'android:label="PGET Causas"', content)
        # Asegurar icono
        if 'android:icon=' not in content:
            content = content.replace('<application', '<application\n        android:icon="@mipmap/ic_launcher"')
        else:
            content = re.sub(r'android:icon="[^"]*"', 'android:icon="@mipmap/ic_launcher"', content)
        
        if 'android:roundIcon=' not in content:
            content = content.replace('<application', '<application\n        android:roundIcon="@mipmap/ic_launcher_round"')
        else:
            content = re.sub(r'android:roundIcon="[^"]*"', 'android:roundIcon="@mipmap/ic_launcher_round"', content)

        # Asegurar permisos de Internet, red y biometría en AndroidManifest.xml
        permissions = '''
    <uses-permission android:name="android.permission.INTERNET"/>
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE"/>
    <uses-permission android:name="android.permission.USE_BIOMETRIC"/>
    <uses-permission android:name="android.permission.USE_FINGERPRINT"/>
'''
        if 'android.permission.INTERNET' not in content:
            content = content.replace('<application', permissions + '    <application')

        with open(manifest_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Updated AndroidManifest.xml: label='PGET Causas', icon='@mipmap/ic_launcher', Internet and Biometric permissions added")

    # 7. Actualizar MainActivity para soporte biométrico con FlutterFragmentActivity
    for root, dirs, files in os.walk('android/app/src/main'):
        for file in files:
            if file.startswith('MainActivity'):
                act_path = os.path.join(root, file)
                if file.endswith('.kt'):
                    with open(act_path, 'w', encoding='utf-8') as f:
                        f.write('''package com.pget.trujillo.data_abogados

import io.flutter.embedding.android.FlutterFragmentActivity

class MainActivity: FlutterFragmentActivity()
''')
                    print(f"Set {act_path} to use FlutterFragmentActivity")
                elif file.endswith('.java'):
                    with open(act_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    content = content.replace('import io.flutter.embedding.android.FlutterActivity;', 'import io.flutter.embedding.android.FlutterFragmentActivity;')
                    content = content.replace('extends FlutterActivity', 'extends FlutterFragmentActivity')
                    with open(act_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"Updated {act_path} with FlutterFragmentActivity")

    # 8. Habilitar multidex y configurar compileSdkVersion 34 en android/app/build.gradle
    app_gradle = 'android/app/build.gradle'
    if os.path.exists(app_gradle):
        with open(app_gradle, 'r', encoding='utf-8') as f:
            g_content = f.read()
        if 'multiDexEnabled' not in g_content:
            g_content = g_content.replace('defaultConfig {', 'defaultConfig {\n        multiDexEnabled true')
        
        # Asegurar compileSdkVersion 34 (evita bug de android-35 en AAPT2)
        g_content = re.sub(r'compileSdk\s*=\s*.*', 'compileSdk = 34', g_content)
        g_content = re.sub(r'compileSdkVersion\s+.*', 'compileSdkVersion 34', g_content)
        g_content = re.sub(r'targetSdk\s*=\s*.*', 'targetSdk = 34', g_content)
        g_content = re.sub(r'targetSdkVersion\s+.*', 'targetSdkVersion 34', g_content)

        with open(app_gradle, 'w', encoding='utf-8') as f:
            f.write(g_content)
        print("Updated android/app/build.gradle: multiDexEnabled true, compileSdk 34")

    # 9. Configurar compileSdkVersion 34 en todos los subproyectos (plugins)
    root_gradle = 'android/build.gradle'
    if os.path.exists(root_gradle):
        with open(root_gradle, 'r', encoding='utf-8') as f:
            r_content = f.read()
        
        # Eliminar cualquier hook previo que haya usado afterEvaluate
        if 'afterEvaluate' in r_content:
            r_content = re.sub(r'subprojects\s*\{[\s\S]*?afterEvaluate[\s\S]*?\}\s*\}', '', r_content)
        
        subproject_hook = '''
subprojects {
    project.plugins.withId("com.android.library") {
        project.android {
            compileSdkVersion 34
            buildToolsVersion "34.0.0"
        }
    }
}
'''
        if 'withId("com.android.library")' not in r_content:
            r_content += subproject_hook
            with open(root_gradle, 'w', encoding='utf-8') as f:
                f.write(r_content)
            print("Configured android/build.gradle with subprojects plugins.withId('com.android.library') compileSdkVersion 34")

if __name__ == '__main__':
    generate_icons()

