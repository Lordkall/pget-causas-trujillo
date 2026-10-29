import json
import base64
import os

with open('compact_causes_by_tab.json', 'r', encoding='utf-8') as f:
    compact_data = json.load(f)

causes_by_tab_json = json.dumps(compact_data['causes_by_tab'], ensure_ascii=False)
years_json = json.dumps(compact_data['years'], ensure_ascii=False)

with open('assets/logo_pget.png', 'rb') as f:
    logo_b64 = base64.b64encode(f.read()).decode('utf-8')

with open('assets/palacio_gobierno.jpg', 'rb') as f:
    palacio_b64 = base64.b64encode(f.read()).decode('utf-8')

# Read build_gavel_login_prototype.py
with open('build_gavel_login_prototype.py', 'r', encoding='utf-8') as f:
    orig = f.read()

# 1. Add CSS for fingerprint scan and laser
css_addition = """
    /* ANIMACIÓN ESCÁNER DE HUELLA DACTILAR */
    @keyframes fingerprint-scan {{
      0% {{ top: 4px; opacity: 0; }}
      20% {{ opacity: 1; }}
      80% {{ opacity: 1; }}
      100% {{ top: calc(100% - 6px); opacity: 0; }}
    }}
    .fingerprint-laser {{
      animation: fingerprint-scan 1.2s ease-in-out infinite;
    }}
    @keyframes pulse-ring {{
      0% {{ transform: scale(0.9); opacity: 0.8; }}
      50% {{ transform: scale(1.15); opacity: 0.3; }}
      100% {{ transform: scale(0.9); opacity: 0.8; }}
    }}
    .pulse-ring {{
      animation: pulse-ring 1.8s ease-in-out infinite;
    }}
"""

orig = orig.replace('.impact-wave-2 {', css_addition + '\n    .impact-wave-2 {')

# 2. Add Biometric Modals (Enrollment Prompt and Scanner) before view-login
biometric_modals = """
          <!-- MODAL: BIOMETRIC ENROLLMENT PROMPT (In-DOM) -->
          <div id="modalBiometricPrompt" class="hidden absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[310px] bg-white rounded-3xl border-2 border-[#D4AF37] shadow-2xl p-5 space-y-3 z-50 text-center">
            <div class="w-14 h-14 mx-auto rounded-full bg-[#6B1226]/10 border-2 border-[#D4AF37] flex items-center justify-center text-[#6B1226]">
              <svg class="w-8 h-8 text-[#D4AF37]" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 11c0 3.517-1.009 6.799-2.753 9.571m-3.44-2.04l.054-.09A13.916 13.916 0 008 11a4 4 0 118 0c0 1.017-.07 2.019-.203 3m-2.118 6.844A21.88 21.88 0 0015.171 17m3.839 1.132c.645-2.266.99-4.659.99-7.132A8 8 0 004 11m0 0a8.003 8.003 0 0015.357 2m-1.084 4.887A14.07 14.07 0 0112 21" />
              </svg>
            </div>
            <div>
              <div class="inline-block bg-[#D4AF37]/20 text-[#6B1226] text-[9.5px] font-black px-2 py-0.5 rounded-full uppercase tracking-wider mb-1">
                Seguridad Institucional
              </div>
              <h4 class="text-xs font-black text-slate-900">¿Activar Acceso con Huella?</h4>
              <p class="text-[11px] text-slate-600 mt-1 leading-tight">
                Inicie sesión en futuros accesos con un solo toque utilizando el sensor biométrico para la cuenta de <strong id="bioPromptUserName" class="text-[#6B1226]"></strong>.
              </p>
            </div>
            <div class="bg-amber-50 border border-[#D4AF37]/50 rounded-xl p-2.5 text-[10.5px] text-amber-900 text-left space-y-1">
              <div class="flex items-center gap-1.5 font-bold">⚡ Acceso instantáneo en 1 toque</div>
              <div class="flex items-center gap-1.5 font-bold">🔒 Respaldo criptográfico del dispositivo</div>
            </div>
            <div class="flex flex-col gap-1.5 pt-1">
              <button onclick="confirmActivateBiometrics()" class="w-full bg-[#6B1226] text-white py-2 rounded-xl text-xs font-extrabold border border-[#D4AF37] hover:bg-[#520d1d] shadow flex items-center justify-center gap-1.5">
                <svg class="w-3.5 h-3.5 text-[#D4AF37]" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/></svg>
                <span>Activar Huella Dactilar</span>
              </button>
              <button onclick="skipBiometrics()" class="w-full py-1.5 text-slate-500 hover:text-slate-800 text-[11px] font-bold">
                Ahora no, ingresar directamente
              </button>
            </div>
          </div>

          <!-- MODAL: BIOMETRIC SCANNING SIMULATOR (In-DOM) -->
          <div id="modalBiometricScan" class="hidden absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[290px] bg-slate-900/95 backdrop-blur-md rounded-3xl border-2 border-[#D4AF37] shadow-2xl p-5 space-y-3 z-50 text-center text-white">
            <div class="relative w-20 h-20 mx-auto flex items-center justify-center">
              <div class="pulse-ring absolute inset-0 rounded-full border-2 border-[#D4AF37]/50 pointer-events-none"></div>
              <div id="fingerprintIconBox" class="relative w-16 h-16 rounded-2xl bg-[#3D0612] border border-[#D4AF37] flex items-center justify-center overflow-hidden">
                <!-- Laser scan bar -->
                <div class="fingerprint-laser absolute left-0 right-0 h-1 bg-gradient-to-r from-transparent via-[#D4AF37] to-transparent shadow-[0_0_8px_#D4AF37]"></div>
                <svg id="fpSvg" class="w-10 h-10 text-[#D4AF37]" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M12 11c0 3.517-1.009 6.799-2.753 9.571m-3.44-2.04l.054-.09A13.916 13.916 0 008 11a4 4 0 118 0c0 1.017-.07 2.019-.203 3m-2.118 6.844A21.88 21.88 0 0015.171 17m3.839 1.132c.645-2.266.99-4.659.99-7.132A8 8 0 004 11m0 0a8.003 8.003 0 0015.357 2m-1.084 4.887A14.07 14.07 0 0112 21" />
                </svg>
                <svg id="fpCheckSvg" class="w-10 h-10 text-emerald-400 hidden" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                </svg>
              </div>
            </div>
            <div>
              <h4 id="bioScanTitle" class="text-xs font-black text-[#D4AF37] uppercase tracking-wide">Sensor de Huella PGET</h4>
              <p id="bioScanDesc" class="text-[11.5px] text-slate-200 mt-1">Coloque su huella en el sensor...</p>
              <p id="bioScanUser" class="text-[10px] text-amber-200/80 font-mono mt-0.5">Identificando despacho oficial...</p>
            </div>
            <button onclick="closeModals()" class="text-[10px] text-slate-400 hover:text-white underline pt-1">
              Cancelar y usar contraseña
            </button>
          </div>
"""

orig = orig.replace('<!-- VISTA 0: LOGIN SCREEN CON FONDO PALACIO DE GOBIERNO', biometric_modals + '\n          <!-- VISTA 0: LOGIN SCREEN CON FONDO PALACIO DE GOBIERNO')

# 3. Replace view-login background and overlay to ensure 100% full vinotinto coverage!
old_bg_block = """          <div id="view-login" class="flex-1 overflow-y-auto p-3 flex flex-col justify-center items-center relative">
            
            <!-- 1. IMAGEN DE FONDO: PALACIO DE GOBIERNO DEL ESTADO TRUJILLO -->
            <div class="absolute inset-0 bg-cover bg-center" style="background-image: url('data:image/jpeg;base64,{palacio_b64}');"></div>
            
            <!-- 2. CAPA VINOTINTO TRANSPARENTOSA ENCIMA (OVERLAY) -->
            <div class="absolute inset-0 bg-gradient-to-b from-[#3D0612]/90 via-[#5A0C1E]/82 to-[#220208]/94 backdrop-blur-[0.5px]"></div>"""

new_bg_block = """          <div id="view-login" class="flex-1 overflow-y-auto p-3 flex flex-col justify-center items-center relative" style="background-color: #38050F;">
            
            <!-- 1. IMAGEN DE FONDO PALACIO DE GOBIERNO CON VINOTINTO QUE ABARCA EL 100% DE LA IMAGEN -->
            <div class="absolute inset-0 bg-cover bg-center pointer-events-none" style="background-image: linear-gradient(180deg, rgba(78, 10, 25, 0.90) 0%, rgba(98, 14, 34, 0.88) 50%, rgba(56, 7, 18, 0.94) 100%), url('data:image/jpeg;base64,{palacio_b64}');"></div>
            
            <!-- 2. CAPA HOMOGÉNEA VINOTINTO ADICIONAL (Para que toda la calle, piso y fachada tengan el tono uniforme) -->
            <div class="absolute inset-0 bg-[#480C19]/45 backdrop-blur-[0.3px] pointer-events-none"></div>"""

assert old_bg_block in orig, "old_bg_block not found in orig"
orig = orig.replace(old_bg_block, new_bg_block)

# 4. In login card, add the Biometric fingerprint button below login button
old_login_btn = """                <!-- Botón Iniciar Sesión (Desencadena el Mazo de Juez de 1,5s) -->
                <button onclick="handleLogin()" class="w-full bg-[#6B1226] text-white py-2.5 rounded-xl text-xs font-extrabold border border-[#D4AF37] shadow-lg hover:bg-[#520d1d] active:scale-95 transition-all flex items-center justify-center gap-1.5">
                  <svg class="w-4 h-4 text-[#D4AF37]" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/></svg>
                  <span>Iniciar Sesión Institucional</span>
                </button>
              </div>"""

new_login_btn = """                <!-- Botón Iniciar Sesión (Desencadena el Mazo de Juez de 1,5s) -->
                <button onclick="handleLogin()" class="w-full bg-[#6B1226] text-white py-2.5 rounded-xl text-xs font-extrabold border border-[#D4AF37] shadow-lg hover:bg-[#520d1d] active:scale-95 transition-all flex items-center justify-center gap-1.5">
                  <svg class="w-4 h-4 text-[#D4AF37]" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/></svg>
                  <span>Iniciar Sesión Institucional</span>
                </button>

                <!-- DIVISOR DISCRETO -->
                <div class="relative flex py-1 items-center">
                  <div class="flex-grow border-t border-slate-200"></div>
                  <span class="flex-shrink mx-2 text-[9.5px] text-slate-400 font-bold uppercase">o acceso con</span>
                  <div class="flex-grow border-t border-slate-200"></div>
                </div>

                <!-- BOTÓN INGRESO CON HUELLA DACTILAR -->
                <button type="button" onclick="handleBiometricScanClick()" class="w-full bg-slate-50 hover:bg-amber-50/50 text-slate-800 py-2 px-3 rounded-xl border border-slate-200 hover:border-[#D4AF37] shadow-sm flex items-center justify-center gap-2 transition-all">
                  <div class="w-6 h-6 rounded-full bg-[#6B1226]/10 flex items-center justify-center text-[#6B1226]">
                    <svg class="w-4 h-4 text-[#6B1226]" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M12 11c0 3.517-1.009 6.799-2.753 9.571m-3.44-2.04l.054-.09A13.916 13.916 0 008 11a4 4 0 118 0c0 1.017-.07 2.019-.203 3m-2.118 6.844A21.88 21.88 0 0015.171 17m3.839 1.132c.645-2.266.99-4.659.99-7.132A8 8 0 004 11m0 0a8.003 8.003 0 0015.357 2m-1.084 4.887A14.07 14.07 0 0112 21" />
                    </svg>
                  </div>
                  <span class="text-xs font-bold text-slate-700">Ingresar con Huella Dactilar</span>
                </button>
              </div>"""

assert old_login_btn in orig, "old_login_btn not found"
orig = orig.replace(old_login_btn, new_login_btn)

# 5. Remove "Acceso Rápido de Prueba" completely!
# Find from <!-- Selector Rápido para Pruebas to </select>\s*</div>
start_quick = orig.find('<!-- Selector Rápido para Pruebas')
end_quick = orig.find('</select>\n              </div>', start_quick) + len('</select>\n              </div>')
assert start_quick != -1 and end_quick != -1, "quick login block not found"
orig = orig[:start_quick] + orig[end_quick:]

# 6. Change logout button to minimalist white icon
old_logout = """                <button onclick="handleLogout()" title="Cerrar Sesión" class="p-1 rounded-lg bg-red-950/60 hover:bg-red-900 border border-red-500/50 text-white text-[11px]">
                  🚪
                </button>"""

new_logout = """                <button onclick="handleLogout()" title="Cerrar Sesión" class="p-1.5 rounded-lg hover:bg-white/10 text-white transition-colors flex items-center justify-center border border-white/20">
                  <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                  </svg>
                </button>"""

assert old_logout in orig, "old_logout not found"
orig = orig.replace(old_logout, new_logout)

# 7. Update JavaScript for handleLogin, biometrics, etc.
old_js_login = """    // INICIAR SESIÓN CON PANTALLA DE CARGA DEL MAZO DE JUEZ (1,5 SEG)
    function handleLogin() {
      const email = document.getElementById('loginEmail').value.trim().toLowerCase();
      const pass = document.getElementById('loginPassword').value.trim();

      const user = usersDatabase.find(u => u.correo.toLowerCase() === email && u.clave === pass);

      if (!user) {
        showToast("Credenciales incorrectas. Verifica tu correo y clave.", "error");
        return;
      }

      // 1. Mostrar pantalla de carga con el Mazo de Juez golpeando
      const loading = document.getElementById('gavelLoadingOverlay');
      loading.classList.remove('hidden');

      // 2. Duración exacta de 1,5 segundos (1500 ms)
      setTimeout(() => {
        loading.classList.add('hidden');

        currentUser = user;
        currentRole = user.rol; // 'admin' | 'lawyer'

        // Actualizar Header
        document.getElementById('headerUserName').innerText = user.shortName || user.nombre;
        document.getElementById('headerUserRole').innerText = user.rol === 'admin' ? 'ADMIN' : 'ABOGADO';

        const adminSubbar = document.getElementById('admin-subbar');
        const lawyerBadge = document.getElementById('lawyer-badge');

        if (user.rol === 'admin') {
          adminSubbar.classList.remove('hidden');
          lawyerBadge.classList.add('hidden');
        } else {
          adminSubbar.classList.add('hidden');
          lawyerBadge.classList.remove('hidden');
        }

        // Mostrar interfaz principal
        document.getElementById('view-login').classList.add('hidden');
        document.getElementById('mainAppHeader').classList.remove('hidden');
        document.getElementById('mainAppBottomBar').classList.remove('hidden');
        document.getElementById('view-list').classList.remove('hidden');

        addAuditLog("LOGIN", "AUTENTICACIÓN", "SEGURIDAD", `Inicio de sesión exitoso: ${user.nombre} (${user.cargo}).`);
        showToast(`¡Audiencia abierta! Bienvenido(a), ${user.shortName}`, "success");
      }, 1500);
    }"""

new_js_login = """    let pendingLoginUser = null;

    // INICIAR SESIÓN: PREGUNTA POR HUELLA BIOMÉTRICA SI ES LA PRIMERA VEZ
    function handleLogin() {
      const email = document.getElementById('loginEmail').value.trim().toLowerCase();
      const pass = document.getElementById('loginPassword').value.trim();

      const user = usersDatabase.find(u => u.correo.toLowerCase() === email && u.clave === pass);

      if (!user) {
        showToast("Credenciales incorrectas. Verifica tu correo y clave.", "error");
        return;
      }

      // Comprobar si ya se le ha preguntado por el acceso biométrico
      const bioConfigured = localStorage.getItem('pget_bio_configured_' + user.correo);

      if (!bioConfigured) {
        // Primera vez que inicia sesión este usuario: preguntar si desea activar huella
        pendingLoginUser = user;
        document.getElementById('bioPromptUserName').innerText = user.shortName || user.nombre;
        document.getElementById('modalBackdrop').classList.remove('hidden');
        document.getElementById('modalBiometricPrompt').classList.remove('hidden');
        return;
      }

      // Si ya fue configurado (o ya respondió previamente), proceder con la carga judicial
      executeGavelLogin(user);
    }

    // CONFIRMAR ACTIVACIÓN DE HUELLA DACTILAR
    function confirmActivateBiometrics() {
      if (!pendingLoginUser) return;
      localStorage.setItem('pget_bio_configured_' + pendingLoginUser.correo, 'true');
      localStorage.setItem('pget_bio_active_user', JSON.stringify(pendingLoginUser));
      closeModals();
      showToast(`¡Huella activada para ${pendingLoginUser.shortName || pendingLoginUser.nombre}!`, "success");
      executeGavelLogin(pendingLoginUser);
      pendingLoginUser = null;
    }

    // OMITIR ACTIVACIÓN DE HUELLA
    function skipBiometrics() {
      if (!pendingLoginUser) return;
      localStorage.setItem('pget_bio_configured_' + pendingLoginUser.correo, 'true');
      closeModals();
      executeGavelLogin(pendingLoginUser);
      pendingLoginUser = null;
    }

    // EJECUCIÓN DE CARGA JUDICIAL CON EL MAZO DE JUEZ (1,5 SEG)
    function executeGavelLogin(user) {
      const loading = document.getElementById('gavelLoadingOverlay');
      loading.classList.remove('hidden');

      setTimeout(() => {
        loading.classList.add('hidden');

        currentUser = user;
        currentRole = user.rol; // 'admin' | 'lawyer'

        // Actualizar Header
        document.getElementById('headerUserName').innerText = user.shortName || user.nombre;
        document.getElementById('headerUserRole').innerText = user.rol === 'admin' ? 'ADMIN' : 'ABOGADO';

        const adminSubbar = document.getElementById('admin-subbar');
        const lawyerBadge = document.getElementById('lawyer-badge');

        if (user.rol === 'admin') {
          adminSubbar.classList.remove('hidden');
          lawyerBadge.classList.add('hidden');
        } else {
          adminSubbar.classList.add('hidden');
          lawyerBadge.classList.remove('hidden');
        }

        // Mostrar interfaz principal
        document.getElementById('view-login').classList.add('hidden');
        document.getElementById('mainAppHeader').classList.remove('hidden');
        document.getElementById('mainAppBottomBar').classList.remove('hidden');
        document.getElementById('view-list').classList.remove('hidden');

        addAuditLog("LOGIN", "AUTENTICACIÓN", "SEGURIDAD", `Inicio de sesión exitoso: ${user.nombre} (${user.cargo}).`);
        showToast(`¡Audiencia abierta! Bienvenido(a), ${user.shortName}`, "success");
      }, 1500);
    }

    // ACCESO CON HUELLA DACTILAR
    function handleBiometricScanClick() {
      const savedBio = localStorage.getItem('pget_bio_active_user');

      if (!savedBio) {
        showToast("Primero ingresa con tu correo y clave una vez para registrar tu huella.", "warning");
        return;
      }

      const bioUser = JSON.parse(savedBio);

      // Mostrar modal de escaneo de huella
      const scanModal = document.getElementById('modalBiometricScan');
      const backdrop = document.getElementById('modalBackdrop');
      const fpLaser = document.querySelector('.fingerprint-laser');
      const fpSvg = document.getElementById('fpSvg');
      const fpCheckSvg = document.getElementById('fpCheckSvg');
      const bioScanTitle = document.getElementById('bioScanTitle');
      const bioScanDesc = document.getElementById('bioScanDesc');
      const bioScanUser = document.getElementById('bioScanUser');

      fpLaser.classList.remove('hidden');
      fpSvg.classList.remove('hidden');
      fpCheckSvg.classList.add('hidden');
      bioScanTitle.innerText = "Sensor de Huella PGET";
      bioScanDesc.innerText = "Verificando huella dactilar...";
      bioScanUser.innerText = "Despacho: " + (bioUser.shortName || bioUser.nombre);

      backdrop.classList.remove('hidden');
      scanModal.classList.remove('hidden');

      // Simulación de lectura biométrica de sensor
      setTimeout(() => {
        fpLaser.classList.add('hidden');
        fpSvg.classList.add('hidden');
        fpCheckSvg.classList.remove('hidden');
        bioScanTitle.innerText = "¡HUELLA VERIFICADA!";
        bioScanTitle.classList.add('text-emerald-400');
        bioScanDesc.innerText = "Identidad validada con éxito";

        setTimeout(() => {
          closeModals();
          bioScanTitle.classList.remove('text-emerald-400');
          // Desencadenar el mazo de juez de 1.5s
          executeGavelLogin(bioUser);
        }, 500);
      }, 800);
    }"""

# In orig, handleLogin appears with double braces in f-string
# Let's inspect how handleLogin was formatted in orig
if 'function handleLogin() {' in orig:
    orig = orig.replace(old_js_login, new_js_login)
elif 'function handleLogin() {{' in orig:
    old_js_login_braces = old_js_login.replace('{', '{{').replace('}', '}}')
    new_js_login_braces = new_js_login.replace('{', '{{').replace('}', '}}')
    assert old_js_login_braces in orig, "old_js_login_braces not found"
    orig = orig.replace(old_js_login_braces, new_js_login_braces)
else:
    raise Exception("handleLogin pattern not matched")

# Also update build_biometric_prototype.py to save the file
with open('build_biometric_prototype.py', 'w', encoding='utf-8') as f:
    f.write(orig)

print("Updated build_biometric_prototype.py successfully!")
