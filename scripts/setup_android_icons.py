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

        # Permisos requeridos
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

    # 8. Actualizar Gradle Wrapper a 8.7 (totalmente compatible con AGP 8.5.0 y Android 35)
    wrapper_props = 'android/gradle/wrapper/gradle-wrapper.properties'
    if os.path.exists(wrapper_props):
        with open(wrapper_props, 'r', encoding='utf-8') as f:
            w_content = f.read()
        w_content = re.sub(r'distributionUrl=.*', r'distributionUrl=https\\://services.gradle.org/distributions/gradle-8.7-all.zip', w_content)
        with open(wrapper_props, 'w', encoding='utf-8') as f:
            f.write(w_content)
        print("Updated gradle-wrapper.properties to gradle-8.7-all.zip")

    # 9. Actualizar android/settings.gradle: AGP 8.5.0 y Kotlin 1.9.24
    settings_gradle = 'android/settings.gradle'
    if os.path.exists(settings_gradle):
        with open(settings_gradle, 'r', encoding='utf-8') as f:
            s_content = f.read()
        s_content = re.sub(r'id "com\.android\.application" version "[^"]*"', 'id "com.android.application" version "8.5.0"', s_content)
        s_content = re.sub(r'id "org\.jetbrains\.kotlin\.android" version "[^"]*"', 'id "org.jetbrains.kotlin.android" version "1.9.24"', s_content)
        s_content = re.sub(r"id 'com\.android\.application' version '[^']*'", 'id "com.android.application" version "8.5.0"', s_content)
        s_content = re.sub(r"id 'org\.jetbrains\.kotlin\.android' version '[^']*'", 'id "org.jetbrains.kotlin.android" version "1.9.24"', s_content)
        with open(settings_gradle, 'w', encoding='utf-8') as f:
            f.write(s_content)
        print("Updated android/settings.gradle: AGP 8.5.0, Kotlin 1.9.24")

    # 10. Configurar android/gradle.properties
    gradle_props = 'android/gradle.properties'
    p_lines = []
    if os.path.exists(gradle_props):
        with open(gradle_props, 'r', encoding='utf-8') as f:
            p_lines = f.readlines()
    
    needed_props = {
        'org.gradle.jvmargs': '-Xmx4G -XX:+HeapDumpOnOutOfMemoryError',
        'android.useAndroidX': 'true',
        'android.enableJetifier': 'true',
        'kotlin.version': '1.9.24',
        'kotlin.jvm.target.validation.mode': 'IGNORE',
    }
    existing_keys = set()
    new_lines = []
    for line in p_lines:
        k = line.split('=')[0].strip() if '=' in line else ''
        if k in needed_props:
            new_lines.append(f"{k}={needed_props[k]}\n")
            existing_keys.add(k)
        else:
            new_lines.append(line)
    for k, v in needed_props.items():
        if k not in existing_keys:
            new_lines.append(f"{k}={v}\n")
    with open(gradle_props, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    print("Updated android/gradle.properties")

    # 11. Habilitar multidex y configurar compileSdk 35 y buildToolsVersion 35.0.0 en android/app/build.gradle
    app_gradle = 'android/app/build.gradle'
    if os.path.exists(app_gradle):
        with open(app_gradle, 'r', encoding='utf-8') as f:
            g_content = f.read()
        if 'multiDexEnabled' not in g_content:
            g_content = g_content.replace('defaultConfig {', 'defaultConfig {\n        multiDexEnabled true')
        
        # compileSdk 35 y buildToolsVersion 35.0.0 y ndkVersion 26.1.10909125
        g_content = re.sub(r'compileSdk\s*=\s*.*', 'compileSdk = 35\n    buildToolsVersion = "35.0.0"\n    ndkVersion = "26.1.10909125"', g_content)
        g_content = re.sub(r'compileSdkVersion\s+.*', 'compileSdkVersion 35\n    buildToolsVersion "35.0.0"\n    ndkVersion = "26.1.10909125"', g_content)
        g_content = re.sub(r'targetSdk\s*=\s*.*', 'targetSdk = 35', g_content)
        g_content = re.sub(r'targetSdkVersion\s+.*', 'targetSdkVersion 35', g_content)

        # JavaVersion 17
        g_content = re.sub(r'sourceCompatibility\s*=\s*JavaVersion\.[A-Za-z0-9_]+', 'sourceCompatibility = JavaVersion.VERSION_17', g_content)
        g_content = re.sub(r'targetCompatibility\s*=\s*JavaVersion\.[A-Za-z0-9_]+', 'targetCompatibility = JavaVersion.VERSION_17', g_content)

        # kotlinOptions jvmTarget 17
        if 'kotlinOptions {' in g_content:
            g_content = re.sub(r'jvmTarget\s*=\s*.*', "jvmTarget = '17'", g_content)
        else:
            g_content = g_content.replace('compileOptions {', "kotlinOptions {\n        jvmTarget = '17'\n    }\n    compileOptions {")

        with open(app_gradle, 'w', encoding='utf-8') as f:
            f.write(g_content)
        print("Updated android/app/build.gradle: multiDexEnabled true, compileSdk 35, ndkVersion 26.1.10909125, Java 17, Kotlin 17")

    # 12. Configurar android/build.gradle con buildscript, Kotlin 1.9.24 y subprojects compileSdk 35
    root_gradle = 'android/build.gradle'
    if os.path.exists(root_gradle):
        with open(root_gradle, 'r', encoding='utf-8') as f:
            r_content = f.read()
        
        # Asegurar buildscript con ext.kotlin_version y dependencies
        if 'ext.kotlin_version' not in r_content:
            buildscript_block = '''buildscript {
    ext.kotlin_version = '1.9.24'
    repositories {
        google()
        mavenCentral()
    }
    dependencies {
        classpath 'com.android.tools.build:gradle:8.5.0'
        classpath 'org.jetbrains.kotlin:kotlin-gradle-plugin:1.9.24'
    }
}

'''
            r_content = buildscript_block + r_content
        else:
            r_content = re.sub(r"ext\.kotlin_version\s*=\s*['\"][^'\"]*['\"]", "ext.kotlin_version = '1.9.24'", r_content)

        # Limpiar cualquier subprojects previo
        r_content = re.sub(r'subprojects\s*\{\s*project\s*->[\s\S]*?\}\s*\}', '', r_content)
        r_content = re.sub(r'subprojects\s*\{[\s\S]*?withId\("com\.android\.library"\)[\s\S]*?\}\s*\}', '', r_content)

        subproject_hook = '''
allprojects {
    tasks.withType(JavaCompile) {
        options.compilerArgs << "-Xlint:-deprecation"
    }
    tasks.withType(org.jetbrains.kotlin.gradle.tasks.KotlinCompile).configureEach {
        kotlinOptions {
            jvmTarget = "17"
        }
    }
}

subprojects { project ->
    project.plugins.withId("com.android.library") {
        if (project.android.hasProperty('namespace') && project.android.namespace == null) {
            project.android.namespace = project.group ?: "com.pget.plugin.${project.name.replace('-', '_')}"
        }
    }
}
'''
        r_content += subproject_hook
        with open(root_gradle, 'w', encoding='utf-8') as f:
            f.write(r_content)
        print("Updated android/build.gradle: buildscript, Kotlin 1.9.24, and subprojects compileSdkVersion 35 / buildToolsVersion 35.0.0")

if __name__ == '__main__':
    generate_icons()
