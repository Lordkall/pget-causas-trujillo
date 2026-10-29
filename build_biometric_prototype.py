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

html_content = f"""<!DOCTYPE html>
<html lang="es" class="h-full">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>PGET Trujillo • Sistema Multimateria de Causas Jurídicas</title>
  
  <!-- Tailwind CSS Oficial Permitido por CSP -->
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>

  <style>
    :root {{
      --color-vinotinto: #6B1226;
      --color-vinotinto-dark: #480C19;
      --color-oro: #D4AF37;
      --color-oro-borde: #C5A059;
    }}
    .bg-vinotinto {{ background-color: #6B1226 !important; }}
    .bg-vinotinto-dark {{ background-color: #480C19 !important; }}
    .text-vinotinto {{ color: #6B1226 !important; }}
    .text-oro {{ color: #D4AF37 !important; }}
    .border-oro {{ border-color: #D4AF37 !important; }}
    .border-oro-borde {{ border-color: #C5A059 !important; }}
    
    ::-webkit-scrollbar {{ width: 4px; height: 4px; }}
    ::-webkit-scrollbar-track {{ background: rgba(0,0,0,0.05); }}
    ::-webkit-scrollbar-thumb {{ background: #D4AF37; border-radius: 4px; }}

    .toast-anim {{
      transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }}

    /* ANIMACIÓN DEL MAZO JUDICIAL GOLPEANDO */
    @keyframes gavel-strike {{
      0% {{ transform: rotate(-45deg); }}
      22% {{ transform: rotate(-58deg); }}
      42% {{ transform: rotate(14deg); }} /* ¡GOLPE SECO EN EL BLOQUE! */
      48% {{ transform: rotate(2deg); }} /* Rebote */
      56% {{ transform: rotate(14deg); }} /* Segundo impacto */
      72% {{ transform: rotate(-45deg); }} /* Retorno */
      100% {{ transform: rotate(-45deg); }}
    }}

    @keyframes impact-wave {{
      0%, 40% {{ opacity: 0; transform: scale(0.4); }}
      44% {{ opacity: 1; transform: scale(0.85); }}
      70% {{ opacity: 0; transform: scale(1.6); }}
      100% {{ opacity: 0; transform: scale(1.6); }}
    }}

    @keyframes impact-wave-2 {{
      0%, 43% {{ opacity: 0; transform: scale(0.4); }}
      49% {{ opacity: 0.8; transform: scale(0.95); }}
      75% {{ opacity: 0; transform: scale(2.0); }}
      100% {{ opacity: 0; transform: scale(2.0); }}
    }}

    .gavel-anim {{
      animation: gavel-strike 0.75s cubic-bezier(0.2, 0.8, 0.2, 1) infinite;
      transform-origin: 86px 64px;
    }}

    .impact-wave {{
      animation: impact-wave 0.75s ease-out infinite;
    }}

    
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

    .impact-wave-2 {{
      animation: impact-wave-2 0.75s ease-out infinite;
    }}
  </style>
</head>
<body class="bg-slate-100 text-slate-800 antialiased p-2 md:p-5 flex flex-col items-center min-h-screen">

  <!-- Header Banner Principal Superior -->
  <div class="max-w-4xl w-full mb-3 flex flex-col md:flex-row items-start md:items-center justify-between gap-3 bg-white border-2 border-[#D4AF37] rounded-2xl p-3.5 shadow-md">
    <div class="flex items-center gap-3 cursor-pointer" onclick="switchView('list')" title="Toca para ir a Inicio">
      <div class="w-13 h-13 rounded-full bg-[#111111] border-2 border-[#D4AF37] p-1 overflow-hidden shrink-0 shadow flex items-center justify-center hover:scale-105 transition-transform" style="width: 54px; height: 54px;">
        <img src="data:image/png;base64,{logo_b64}" alt="PGET Logo" class="w-full h-full object-contain">
      </div>
      <div>
        <div class="text-[11px] font-black tracking-widest text-[#D4AF37] uppercase">Procuraduría General del Estado Trujillo</div>
        <h1 class="text-base font-extrabold text-slate-900 leading-tight">
          Sistema de Causas Jurídicas • Palacio de Gobierno
        </h1>
        <p class="text-xs text-slate-500">Autenticación Institucional • Pantalla de Carga Judicial (Mazo de Juez) • Dra. Lizamar Briceño (Admin)</p>
      </div>
    </div>
    
    <div class="flex items-center gap-2 bg-emerald-50 border border-emerald-300 px-3 py-1 rounded-lg text-emerald-800 text-xs font-bold">
      <span class="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse"></span>
      13 Cuentas Activas
    </div>
  </div>

  <!-- Contenedor: Smartphone Simulator y Panel Explicativo -->
  <div class="max-w-4xl w-full grid grid-cols-1 lg:grid-cols-12 gap-5 items-start">
    
    <!-- FRAME SMARTPHONE (Cols 7) -->
    <div class="lg:col-span-7 flex justify-center">
      <div class="w-[365px] h-[750px] bg-slate-900 rounded-[44px] p-3 shadow-2xl border-4 border-slate-700 relative flex flex-col">
        
        <!-- Notch -->
        <div class="w-full flex justify-center items-center py-1 absolute top-3 left-0 z-50">
          <div class="w-24 h-4 bg-black rounded-full flex items-center justify-center">
            <div class="w-2 h-2 rounded-full bg-slate-900 mr-2"></div>
            <div class="w-1 h-1 rounded-full bg-amber-600"></div>
          </div>
        </div>

        <!-- Pantalla Móvil -->
        <div class="w-full h-full bg-[#FCFCFD] text-slate-800 rounded-[34px] overflow-hidden flex flex-col relative pt-7">
          
          <!-- TOAST NOTIFICATION CONTAINER (In-App) -->
          <div id="appToast" class="toast-anim fixed top-10 left-1/2 -translate-x-1/2 z-[100] max-w-[320px] w-11/12 opacity-0 pointer-events-none -translate-y-3">
            <div id="appToastInner" class="bg-slate-900 text-white text-xs font-bold px-3 py-2 rounded-xl border border-[#D4AF37] shadow-xl flex items-center gap-2">
              <span id="toastIcon">✅</span>
              <span id="toastMsg" class="flex-1 leading-tight">Acción completada</span>
            </div>
          </div>

          <!-- PANTALLA DE CARGA JUDICIAL CON MAZO DE JUEZ (1.5 SEG) -->
          <div id="gavelLoadingOverlay" class="hidden absolute inset-0 bg-[#2D060E]/94 backdrop-blur-md z-[90] flex flex-col items-center justify-center p-6 text-center text-white">
            
            <!-- Animación del Mazo Golpeando el Bloque de Resonancia -->
            <div class="relative w-36 h-36 flex items-center justify-center mb-3">
              <!-- Ondas de choque del golpe -->
              <div class="impact-wave absolute bottom-6 w-24 h-10 border-2 border-[#D4AF37] rounded-full pointer-events-none"></div>
              <div class="impact-wave-2 absolute bottom-6 w-24 h-10 border border-amber-300 rounded-full pointer-events-none"></div>

              <!-- Gráfico Vectorial SVG del Mazo y Base -->
              <svg class="w-32 h-32 overflow-visible" viewBox="0 0 120 120">
                <!-- Base de resonancia (Fija en el fondo) -->
                <g class="soundblock">
                  <ellipse cx="48" cy="94" rx="34" ry="10" fill="#1A0307" stroke="#D4AF37" stroke-width="2"/>
                  <ellipse cx="48" cy="91" rx="30" ry="8" fill="#480C19" stroke="#C5A059" stroke-width="1.5"/>
                  <ellipse cx="48" cy="89" rx="22" ry="5" fill="#6B1226"/>
                </g>

                <!-- Mazo de Juez Animado -->
                <g class="gavel-anim">
                  <!-- Mango -->
                  <line x1="86" y1="64" x2="48" y2="44" stroke="#D4AF37" stroke-width="6" stroke-linecap="round"/>
                  <line x1="86" y1="64" x2="48" y2="44" stroke="#480C19" stroke-width="3.5" stroke-linecap="round"/>
                  <circle cx="88" cy="65" r="4.5" fill="#D4AF37"/>

                  <!-- Cabeza del Mazo -->
                  <g transform="translate(48, 44) rotate(26)">
                    <rect x="-14" y="-12" width="28" height="24" rx="4" fill="#380510" stroke="#D4AF37" stroke-width="2"/>
                    <line x1="-6" y1="-12" x2="-6" y2="12" stroke="#D4AF37" stroke-width="2"/>
                    <line x1="6" y1="-12" x2="6" y2="12" stroke="#D4AF37" stroke-width="2"/>
                    <rect x="-20" y="-14" width="6" height="28" rx="2" fill="#500B1A" stroke="#D4AF37" stroke-width="1.5"/>
                    <rect x="14" y="-14" width="6" height="28" rx="2" fill="#500B1A" stroke="#D4AF37" stroke-width="1.5"/>
                  </g>
                </g>
              </svg>
            </div>

            <div class="space-y-1.5">
              <span class="inline-block bg-[#D4AF37] text-[#480C19] text-[10px] font-black px-2.5 py-0.5 rounded-full uppercase tracking-wider shadow">
                Audiencia & Credenciales
              </span>
              <h4 class="text-sm font-extrabold text-white tracking-wide">Autenticando en Procuraduría...</h4>
              <p class="text-[11px] text-amber-200/90 font-mono">Verificando firma y despacho oficial</p>
            </div>

            <!-- Barra de progreso de 1.5s -->
            <div class="w-48 bg-black/40 h-1.5 rounded-full mt-4 overflow-hidden border border-[#D4AF37]/50">
              <div class="bg-gradient-to-r from-amber-400 to-[#D4AF37] h-full rounded-full animate-[pulse_1.5s_ease-in-out]"></div>
            </div>
          </div>

          <!-- MODAL BACKDROP (In-DOM) -->
          <div id="modalBackdrop" onclick="closeModals()" class="hidden absolute inset-0 bg-black/60 z-40 backdrop-blur-sm transition-opacity"></div>

          <!-- MODAL 1: EDIT LAWYER (In-DOM) -->
          <div id="modalEditLawyer" class="hidden absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[310px] bg-white rounded-2xl border-2 border-[#D4AF37] shadow-2xl p-4 space-y-2.5 z-50">
            <div class="flex items-center justify-between border-b pb-2">
              <h4 class="font-extrabold text-xs text-[#6B1226] flex items-center gap-1.5">
                <span>✏️</span> Editar Abogado de Nómina
              </h4>
              <button onclick="closeModals()" class="text-slate-400 hover:text-slate-600 text-sm font-bold">✕</button>
            </div>
            <input type="hidden" id="editLawyerId">
            <div>
              <label class="text-[10px] font-bold text-slate-500 uppercase">Nombre y Apellido</label>
              <input type="text" id="editLawyerName" class="w-full bg-slate-50 border border-slate-300 rounded-lg p-1.5 text-xs font-bold text-slate-800 focus:outline-none focus:border-[#D4AF37]">
            </div>
            <div>
              <label class="text-[10px] font-bold text-slate-500 uppercase">Cédula de Identidad</label>
              <input type="text" id="editLawyerCI" class="w-full bg-slate-50 border border-slate-300 rounded-lg p-1.5 text-xs text-slate-800 focus:outline-none focus:border-[#D4AF37]">
            </div>
            <div>
              <label class="text-[10px] font-bold text-slate-500 uppercase">Cargo Institucional</label>
              <input type="text" id="editLawyerCargo" class="w-full bg-slate-50 border border-slate-300 rounded-lg p-1.5 text-xs text-slate-800 focus:outline-none focus:border-[#D4AF37]">
            </div>
            <div>
              <label class="text-[10px] font-bold text-slate-500 uppercase">Adscripción / Materia</label>
              <input type="text" id="editLawyerAdscrito" class="w-full bg-slate-50 border border-slate-300 rounded-lg p-1.5 text-xs text-slate-800 focus:outline-none focus:border-[#D4AF37]">
            </div>
            <div class="flex gap-2 pt-1">
              <button onclick="saveLawyerEditAction()" class="flex-1 bg-[#6B1226] text-white py-1.5 rounded-lg text-xs font-extrabold border border-[#D4AF37] hover:bg-[#520d1d] shadow">
                Guardar Cambios
              </button>
              <button onclick="closeModals()" class="px-3 py-1.5 bg-slate-100 text-slate-600 rounded-lg text-xs font-bold border border-slate-300 hover:bg-slate-200">
                Cancelar
              </button>
            </div>
          </div>

          <!-- MODAL 2: DEACTIVATE LAWYER (In-DOM) -->
          <div id="modalDeactivateLawyer" class="hidden absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[310px] bg-white rounded-2xl border-2 border-rose-500 shadow-2xl p-4 space-y-2.5 z-50">
            <div class="flex items-center gap-2 text-rose-700 font-extrabold text-xs border-b pb-2">
              <span>🚫</span> Desactivar Abogado
            </div>
            <input type="hidden" id="deactLawyerId">
            <p class="text-xs text-slate-700">
              ¿Desactivar a <strong id="deactLawyerName" class="text-[#6B1226]"></strong> de la nómina activa?
            </p>
            <div class="bg-amber-50 border border-amber-300 rounded-xl p-2.5 text-[10.5px] text-amber-900 leading-tight">
              <strong>🛡️ Garantía de Integridad:</strong> Todas sus causas y expedientes en Google Sheets <u>SE CONSERVAN AL 100%</u> con su nombre. Solo dejará de estar disponible para nuevas asignaciones.
            </div>
            <div class="flex gap-2 pt-1">
              <button onclick="confirmDeactivateLawyerAction()" class="flex-1 bg-rose-600 text-white py-1.5 rounded-lg text-xs font-extrabold hover:bg-rose-700 shadow">
                Sí, Desactivar
              </button>
              <button onclick="closeModals()" class="px-3 py-1.5 bg-slate-100 text-slate-600 rounded-lg text-xs font-bold border border-slate-300 hover:bg-slate-200">
                Cancelar
              </button>
            </div>
          </div>

          <!-- MODAL 3: REACTIVATE LAWYER (In-DOM) -->
          <div id="modalReactivateLawyer" class="hidden absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[310px] bg-white rounded-2xl border-2 border-emerald-500 shadow-2xl p-4 space-y-2.5 z-50">
            <div class="flex items-center gap-2 text-emerald-800 font-extrabold text-xs border-b pb-2">
              <span>✅</span> Reactivar Abogado
            </div>
            <input type="hidden" id="reactLawyerId">
            <p class="text-xs text-slate-700">
              ¿Reactivar a <strong id="reactLawyerName" class="text-[#6B1226]"></strong> en la nómina activa para asignarle nuevas causas?
            </p>
            <div class="flex gap-2 pt-1">
              <button onclick="confirmReactivateLawyerAction()" class="flex-1 bg-emerald-700 text-white py-1.5 rounded-lg text-xs font-extrabold hover:bg-emerald-800 shadow">
                Sí, Reactivar
              </button>
              <button onclick="closeModals()" class="px-3 py-1.5 bg-slate-100 text-slate-600 rounded-lg text-xs font-bold border border-slate-300 hover:bg-slate-200">
                Cancelar
              </button>
            </div>
          </div>

          <!-- MODAL 4: ADD LAWYER (In-DOM) -->
          <div id="modalAddLawyer" class="hidden absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[310px] bg-white rounded-2xl border-2 border-[#D4AF37] shadow-2xl p-4 space-y-2.5 z-50">
            <div class="flex items-center justify-between border-b pb-2">
              <h4 class="font-extrabold text-xs text-[#6B1226] flex items-center gap-1.5">
                <span>➕</span> Nuevo Abogado PGET
              </h4>
              <button onclick="closeModals()" class="text-slate-400 hover:text-slate-600 text-sm font-bold">✕</button>
            </div>
            <div>
              <label class="text-[10px] font-bold text-slate-500 uppercase">Nombre y Apellido</label>
              <input type="text" id="newLawyerName" placeholder="Ej: DRA. CARMEN MONTILLA" class="w-full bg-slate-50 border border-slate-300 rounded-lg p-1.5 text-xs font-bold text-slate-800 focus:outline-none focus:border-[#D4AF37]">
            </div>
            <div>
              <label class="text-[10px] font-bold text-slate-500 uppercase">Cédula de Identidad</label>
              <input type="text" id="newLawyerCI" placeholder="Ej: V-15.789.012" class="w-full bg-slate-50 border border-slate-300 rounded-lg p-1.5 text-xs text-slate-800 focus:outline-none focus:border-[#D4AF37]">
            </div>
            <div>
              <label class="text-[10px] font-bold text-slate-500 uppercase">Cargo Institucional</label>
              <input type="text" id="newLawyerCargo" placeholder="Ej: Abogada Litigante" class="w-full bg-slate-50 border border-slate-300 rounded-lg p-1.5 text-xs text-slate-800 focus:outline-none focus:border-[#D4AF37]">
            </div>
            <div>
              <label class="text-[10px] font-bold text-slate-500 uppercase">Adscripción / Materia</label>
              <input type="text" id="newLawyerAdscrito" placeholder="Ej: CONTENCIOSO ADMINISTRATIVO" class="w-full bg-slate-50 border border-slate-300 rounded-lg p-1.5 text-xs text-slate-800 focus:outline-none focus:border-[#D4AF37]">
            </div>
            <div class="flex gap-2 pt-1">
              <button onclick="saveNewLawyerAction()" class="flex-1 bg-[#6B1226] text-white py-1.5 rounded-lg text-xs font-extrabold border border-[#D4AF37] hover:bg-[#520d1d] shadow">
                Registrar en Nómina
              </button>
              <button onclick="closeModals()" class="px-3 py-1.5 bg-slate-100 text-slate-600 rounded-lg text-xs font-bold border border-slate-300 hover:bg-slate-200">
                Cancelar
              </button>
            </div>
          </div>

          <!-- MODAL 5: EDIT CAUSA (In-DOM) -->
          <div id="modalEditCausa" class="hidden absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[310px] bg-white rounded-2xl border-2 border-[#D4AF37] shadow-2xl p-4 space-y-2.5 z-50">
            <div class="flex items-center justify-between border-b pb-2">
              <h4 class="font-extrabold text-xs text-[#6B1226] flex items-center gap-1.5">
                <span>✏️</span> Editar Causa Judicial
              </h4>
              <button onclick="closeModals()" class="text-slate-400 hover:text-slate-600 text-sm font-bold">✕</button>
            </div>
            <input type="hidden" id="editCausaRowIndex">
            <div>
              <label class="text-[10px] font-bold text-slate-500 uppercase">Nº de Expediente</label>
              <input type="text" id="editCausaExp" class="w-full bg-slate-50 border border-slate-300 rounded-lg p-1.5 text-xs font-bold text-slate-800 focus:outline-none focus:border-[#D4AF37]">
            </div>
            <div>
              <label class="text-[10px] font-bold text-slate-500 uppercase">Motivo / Asunto Judicial</label>
              <textarea id="editCausaMot" rows="2" class="w-full bg-slate-50 border border-slate-300 rounded-lg p-1.5 text-xs text-slate-800 focus:outline-none focus:border-[#D4AF37]"></textarea>
            </div>
            <div>
              <label class="text-[10px] font-bold text-slate-500 uppercase">Demandado / Contraparte</label>
              <input type="text" id="editCausaDmd" class="w-full bg-slate-50 border border-slate-300 rounded-lg p-1.5 text-xs text-slate-800 focus:outline-none focus:border-[#D4AF37]">
            </div>
            <div>
              <label class="text-[10px] font-bold text-slate-500 uppercase">Abogado Responsable</label>
              <select id="editCausaAbg" class="w-full bg-slate-50 border border-slate-300 rounded-lg p-1.5 text-xs font-semibold text-slate-800 focus:outline-none focus:border-[#D4AF37]">
              </select>
            </div>
            <div>
              <label class="text-[10px] font-bold text-slate-500 uppercase">Estado Actual</label>
              <select id="editCausaEst" class="w-full bg-slate-50 border border-slate-300 rounded-lg p-1.5 text-xs font-bold text-slate-800 focus:outline-none focus:border-[#D4AF37]">
                <option value="ACTIVA">ACTIVA</option>
                <option value="CERRADA">CERRADA</option>
                <option value="EN TRÁMITE">EN TRÁMITE</option>
                <option value="SENTENCIADA">SENTENCIADA</option>
              </select>
            </div>
            <div class="flex gap-2 pt-1">
              <button onclick="saveCausaEditAction()" class="flex-1 bg-[#6B1226] text-white py-1.5 rounded-lg text-xs font-extrabold border border-[#D4AF37] hover:bg-[#520d1d] shadow">
                Guardar Cambios
              </button>
              <button onclick="closeModals()" class="px-3 py-1.5 bg-slate-100 text-slate-600 rounded-lg text-xs font-bold border border-slate-300 hover:bg-slate-200">
                Cancelar
              </button>
            </div>
          </div>

          <!-- MODAL 6: DELETE CAUSA (In-DOM) -->
          <div id="modalDeleteCausa" class="hidden absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[310px] bg-white rounded-2xl border-2 border-rose-500 shadow-2xl p-4 space-y-2.5 z-50">
            <div class="flex items-center gap-2 text-rose-700 font-extrabold text-xs border-b pb-2">
              <span>🗑️</span> Eliminar Causa Judicial
            </div>
            <input type="hidden" id="delCausaRowIndex">
            <p class="text-xs text-slate-700">
              ¿Eliminar la causa del Expediente <strong id="delCausaExp" class="text-[#6B1226]"></strong>?
            </p>
            <p id="delCausaMot" class="text-[10.5px] text-slate-600 italic bg-slate-50 p-2 rounded border border-slate-200 line-clamp-2"></p>
            <div class="bg-rose-50 border border-rose-200 rounded-xl p-2 text-[10px] text-rose-800 leading-tight">
              <strong>⚠️ Registro de Auditoría:</strong> Esta acción quedará grabada con usuario (<span id="delCausaUser" class="font-bold"></span>), fecha y hora exacta.
            </div>
            <div class="flex gap-2 pt-1">
              <button onclick="confirmDeleteCausaAction()" class="flex-1 bg-rose-600 text-white py-1.5 rounded-lg text-xs font-extrabold hover:bg-rose-700 shadow">
                Sí, Eliminar
              </button>
              <button onclick="closeModals()" class="px-3 py-1.5 bg-slate-100 text-slate-600 rounded-lg text-xs font-bold border border-slate-300 hover:bg-slate-200">
                Cancelar
              </button>
            </div>
          </div>

          
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

          <!-- VISTA 0: LOGIN SCREEN CON FONDO PALACIO DE GOBIERNO + CAPA VINOTINTO TRANSPARENTE -->
          <div id="view-login" class="flex-1 overflow-y-auto p-3 flex flex-col justify-center items-center relative" style="background-color: #38050F;">
            
            <!-- 1. IMAGEN DE FONDO PALACIO DE GOBIERNO CON VINOTINTO QUE ABARCA EL 100% DE LA IMAGEN -->
            <div class="absolute inset-0 bg-cover bg-center pointer-events-none" style="background-image: linear-gradient(180deg, rgba(78, 10, 25, 0.90) 0%, rgba(98, 14, 34, 0.88) 50%, rgba(56, 7, 18, 0.94) 100%), url('data:image/jpeg;base64,{palacio_b64}');"></div>
            
            <!-- 2. CAPA HOMOGÉNEA VINOTINTO ADICIONAL (Para que toda la calle, piso y fachada tengan el tono uniforme) -->
            <div class="absolute inset-0 bg-[#480C19]/45 backdrop-blur-[0.3px] pointer-events-none"></div>

            <!-- 3. CONTENIDO DEL LOGIN -->
            <div class="relative z-10 w-full max-w-[315px] space-y-3.5 my-auto">
              
              <!-- Logo PGET + Títulos Institucionales -->
              <div class="text-center space-y-1.5 flex flex-col items-center">
                <div class="w-16 h-16 rounded-full bg-[#111111] border-2 border-[#D4AF37] p-1 shadow-2xl flex items-center justify-center">
                  <img src="data:image/png;base64,{logo_b64}" alt="PGET Logo" class="w-full h-full object-contain">
                </div>
                <div>
                  <h2 class="text-[10px] font-black tracking-widest text-[#D4AF37] uppercase drop-shadow">PROCURADURÍA GENERAL DEL ESTADO TRUJILLO</h2>
                  <h3 class="text-sm font-extrabold text-white leading-tight drop-shadow">Sistema de Causas Jurídicas</h3>
                  <p class="text-[10.5px] text-amber-100/80">Sede Palacio de Gobierno</p>
                </div>
              </div>

              <!-- Tarjeta de Formulario de Login -->
              <div class="bg-white/95 backdrop-blur-md p-3.5 rounded-2xl border-2 border-[#D4AF37] shadow-2xl space-y-2.5">
                <div>
                  <label class="text-[10px] font-bold text-slate-700 uppercase flex items-center justify-between">
                    <span>Correo Institucional</span>
                    <span class="text-[9.5px] text-[#D4AF37] font-mono font-bold">@pget.com</span>
                  </label>
                  <input type="email" id="loginEmail" placeholder="nombreapellido@pget.com" value="lizamarbriceno@pget.com" class="w-full bg-slate-50 border border-slate-300 rounded-xl p-2 text-xs font-bold text-slate-800 focus:outline-none focus:border-[#D4AF37]">
                </div>

                <div>
                  <label class="text-[10px] font-bold text-slate-700 uppercase">Contraseña</label>
                  <div class="relative">
                    <input type="password" id="loginPassword" placeholder="••••••••" value="Admin2026*Lizamar" class="w-full bg-slate-50 border border-slate-300 rounded-xl p-2 pr-9 text-xs font-bold text-slate-800 focus:outline-none focus:border-[#D4AF37]">
                    
                    <!-- ICONO MINIMALISTA DEL OJO PARA VER/OCULTAR CONTRASEÑA -->
                    <button type="button" onclick="togglePasswordVisibility()" title="Ver/ocultar contraseña" class="absolute right-2.5 top-1/2 -translate-y-1/2 text-slate-400 hover:text-[#6B1226] transition-colors p-1 flex items-center justify-center">
                      <!-- Ojo Abierto Minimalista -->
                      <svg id="eyeIconOpen" class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M2.036 12.322a1.012 1.012 0 010-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.964-7.178z" />
                        <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                      </svg>
                      <!-- Ojo Oculto Minimalista con Tachado -->
                      <svg id="eyeIconClosed" class="w-4 h-4 hidden" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M3.98 8.223A10.477 10.477 0 001.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.45 10.45 0 0112 4.5c4.756 0 8.773 3.162 10.065 7.498a10.523 10.523 0 01-4.293 5.774M6.228 6.228L3 3m3.228 3.228l3.65 3.65m7.894 7.894L21 21m-3.228-3.228l-3.65-3.65m0 0a3 3 0 10-4.243-4.243m4.242 4.242L9.88 9.88" />
                      </svg>
                    </button>
                  </div>
                </div>

                <!-- Botón Iniciar Sesión (Desencadena el Mazo de Juez de 1,5s) -->
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
              </div>

              

            </div>
          </div>

          <!-- HEADER VINOTINTO PGET (Visible al iniciar sesión) -->
          <div id="mainAppHeader" class="hidden bg-[#6B1226] text-white px-3.5 py-2.5 border-b-2 border-[#D4AF37] shadow">
            
            <!-- Fila 1: Logo + Título (Home) + Usuario Activo + Botón Salir -->
            <div class="flex items-center justify-between">
              
              <!-- Clic en Logo o Título -> Va a Home -->
              <div class="flex items-center gap-2 cursor-pointer" onclick="switchView('list')" title="Toca el logo para regresar a Inicio">
                <div class="rounded-full bg-[#111111] border-2 border-[#D4AF37] p-0.5 overflow-hidden shrink-0 shadow flex items-center justify-center" style="width: 38px; height: 38px;">
                  <img src="data:image/png;base64,{logo_b64}" alt="Escudo PGET" class="w-full h-full object-contain">
                </div>
                <div>
                  <div class="text-[9.5px] font-black text-[#D4AF37] tracking-wider uppercase leading-none">PGET • TRUJILLO</div>
                  <div class="text-[11px] font-extrabold text-white leading-tight">Causas Jurídicas</div>
                </div>
              </div>

              <!-- Usuario Conectado + Botón Cerrar Sesión -->
              <div class="flex items-center gap-1.5">
                <div class="bg-[#480C19] px-2 py-1 rounded-lg border border-[#D4AF37]/50 flex flex-col items-end">
                  <span id="headerUserName" class="text-[10px] font-extrabold text-[#D4AF37] truncate max-w-[120px]">Lizamar Briceño</span>
                  <span id="headerUserRole" class="text-[8.5px] text-white/80 font-mono">ADMIN</span>
                </div>
                <button onclick="handleLogout()" title="Cerrar Sesión" class="p-1.5 rounded-lg hover:bg-white/10 text-white transition-colors flex items-center justify-center border border-white/20">
                  <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                  </svg>
                </button>
              </div>
            </div>

            <!-- Fila 2 (Solo para Admin): Accesos a Nómina y Auditoría -->
            <div id="admin-subbar" class="mt-2 grid grid-cols-2 gap-1.5 text-[10.5px]">
              <button onclick="switchView('lawyers-admin')" class="py-1 px-2 rounded-lg bg-white/10 hover:bg-white/20 border border-[#D4AF37]/40 text-white font-bold flex items-center justify-center gap-1.5">
                <svg class="w-3.5 h-3.5 text-[#D4AF37]" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"/></svg>
                Nómina Abogados
              </button>
              <button onclick="switchView('audit-admin')" class="py-1 px-2 rounded-lg bg-white/10 hover:bg-white/20 border border-[#D4AF37]/40 text-white font-bold flex items-center justify-center gap-1.5">
                <svg class="w-3.5 h-3.5 text-[#D4AF37]" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                Auditoría Admin
              </button>
            </div>

            <!-- Banner informativo para modo Abogado -->
            <div id="lawyer-badge" class="mt-2 hidden bg-white/10 px-2 py-1 rounded-lg border border-[#D4AF37]/30 text-[10px] text-white flex items-center justify-between">
              <span class="text-white/90">⚖️ <strong>Nivel Abogado:</strong> Consulta, creación, edición y eliminación de causas con registro de auditoría.</span>
            </div>

            <!-- Fila Filtros de Navegación: Pestaña (17 Pestañas) + FILTRO DE AÑO -->
            <div class="mt-2 pt-2 border-t border-white/15 flex items-center gap-1.5 text-[11px]">
              <!-- Selector Pestaña (17 Pestañas) -->
              <div class="flex-1 min-w-0">
                <select id="sheetTabSelect" onchange="onTabChanged()" class="w-full bg-[#480C19] text-white font-bold border border-[#D4AF37] rounded px-1.5 py-1 text-[11px] truncate focus:outline-none">
                </select>
              </div>

              <!-- FILTRO POR AÑO (Sin obligar a seleccionar abogado) -->
              <div class="shrink-0">
                <select id="yearFilterSelect" onchange="renderCausas()" class="bg-[#480C19] text-[#D4AF37] font-extrabold border border-[#D4AF37] rounded px-2 py-1 text-[11px] focus:outline-none">
                  <option value="TODOS">Año: Todos</option>
                </select>
              </div>
            </div>
          </div>

          <!-- VISTA 1: HOME / DASHBOARD DE CAUSAS -->
          <div id="view-list" class="hidden flex-1 overflow-y-auto p-3 space-y-2.5">
            
            <!-- Métricas -->
            <div class="grid grid-cols-3 gap-1.5">
              <div class="bg-white p-2 rounded-xl border border-[#D4AF37] shadow-sm flex flex-col items-center">
                <span class="text-[9.5px] text-slate-400 font-bold uppercase">Causas</span>
                <span id="stat-total" class="text-sm font-black text-[#6B1226]">0</span>
              </div>
              <div class="bg-white p-2 rounded-xl border border-[#D4AF37] shadow-sm flex flex-col items-center">
                <span class="text-[9.5px] text-emerald-600 font-bold uppercase">Activas</span>
                <span id="stat-active" class="text-sm font-black text-emerald-700">0</span>
              </div>
              <div class="bg-white p-2 rounded-xl border border-[#D4AF37] shadow-sm flex flex-col items-center">
                <span class="text-[9.5px] text-slate-500 font-bold uppercase">Cerradas</span>
                <span id="stat-closed" class="text-sm font-black text-slate-600">0</span>
              </div>
            </div>

            <!-- Búsqueda Rápida de Expediente / Causa -->
            <div class="relative">
              <input type="text" id="searchInput" oninput="renderCausas()" placeholder="Buscar por expediente, motivo, abogado..." class="w-full bg-white border border-[#D4AF37] rounded-xl pl-8 pr-3 py-1.5 text-xs focus:outline-none focus:ring-1 focus:ring-[#D4AF37]">
              <span class="absolute left-2.5 top-2 text-slate-400 text-xs">🔍</span>
            </div>

            <!-- Chips de Filtro Estado -->
            <div class="flex items-center gap-1.5 overflow-x-auto pb-1 text-[10px]">
              <button onclick="setEstadoFilter('ALL', this)" class="chip-estado bg-[#6B1226] text-white px-2.5 py-0.5 rounded-full font-bold shrink-0 border border-[#D4AF37]">Todos</button>
              <button onclick="setEstadoFilter('ACT', this)" class="chip-estado bg-white text-slate-700 px-2.5 py-0.5 rounded-full font-semibold shrink-0 border border-[#C5A059]">Solo Activas</button>
              <button onclick="setEstadoFilter('CERR', this)" class="chip-estado bg-white text-slate-700 px-2.5 py-0.5 rounded-full font-semibold shrink-0 border border-[#C5A059]">Solo Cerradas</button>
            </div>

            <!-- Lista de Causas Reales de Google Sheets -->
            <div id="causasContainer" class="space-y-2">
            </div>
          </div>

          <!-- VISTA 2: NÓMINA DE ABOGADOS (ADMIN) -->
          <div id="view-lawyers-admin" class="hidden flex-1 overflow-y-auto p-3 space-y-2.5">
            <div class="flex items-center justify-between">
              <div>
                <h3 class="font-extrabold text-sm text-[#6B1226]">Nómina Institucional</h3>
                <p class="text-[10px] text-slate-500">13 Abogados Activos Oficiales (A-Z)</p>
              </div>
              <button onclick="openAddLawyerModal()" class="px-2.5 py-1 rounded-lg bg-[#6B1226] text-white text-xs font-bold border border-[#D4AF37] flex items-center gap-1 shadow">
                <span>➕</span> Nuevo Abogado
              </button>
            </div>

            <div class="bg-amber-50 border border-amber-300 rounded-xl p-2 text-[10.5px] text-amber-900 leading-snug">
              <strong>🛡️ Política de Conservación Histórica:</strong> Al desactivar un abogado, jamás se borra su nombre de los expedientes previos ni de Google Sheets. Solo se inhabilita para nuevos casos.
            </div>

            <!-- Lista de Abogados -->
            <div id="lawyersListContainer" class="space-y-2">
            </div>
          </div>

          <!-- VISTA 3: AUDITORÍA (ADMIN) -->
          <div id="view-audit-admin" class="hidden flex-1 overflow-y-auto p-3 space-y-2.5">
            <div class="flex items-center justify-between">
              <div>
                <h3 class="font-extrabold text-sm text-[#6B1226]">Registro de Auditoría</h3>
                <p class="text-[10px] text-slate-500">Historial inmutable de creaciones, ediciones y bajas</p>
              </div>
              <span class="text-[10px] bg-slate-200 text-slate-700 px-2 py-0.5 rounded-full font-mono font-bold">Admin Only</span>
            </div>

            <div id="auditListContainer" class="space-y-2">
            </div>
          </div>

          <!-- VISTA 4: FORMULARIO DINÁMICO CREAR CAUSA -->
          <div id="view-form" class="hidden flex-1 overflow-y-auto p-3 space-y-3">
            <div class="bg-white p-3 rounded-2xl border border-[#D4AF37] shadow-sm">
              <div class="flex items-center justify-between border-b pb-2 mb-2">
                <div>
                  <span class="text-[10px] font-black text-[#D4AF37] uppercase">Nueva Causa Judicial</span>
                  <h3 id="form-tab-title" class="font-extrabold text-xs text-[#6B1226]">CONTENCIOSO TRUJILLO</h3>
                </div>
                <button onclick="openTabSelectorModal()" class="px-2 py-1 bg-amber-50 hover:bg-amber-100 text-[#6B1226] border border-[#D4AF37] rounded-lg text-[10px] font-bold">
                  Cambiar Materia ▾
                </button>
              </div>

              <!-- Campos dinámicos adaptados a la materia seleccionada -->
              <div id="dynamicFormFields" class="space-y-2 text-xs">
              </div>

              <div class="mt-4 pt-2 border-t flex items-center justify-between gap-2">
                <button onclick="switchView('list')" class="w-1/3 py-2 rounded-xl border border-slate-300 text-slate-600 text-xs font-bold hover:bg-slate-50">
                  Cancelar
                </button>
                <button onclick="submitNewCausa()" class="w-2/3 py-2 rounded-xl bg-[#6B1226] text-white text-xs font-extrabold border border-[#D4AF37] shadow hover:bg-[#520d1d] flex items-center justify-center gap-1.5">
                  <span>💾</span> Guardar en Google Sheets
                </button>
              </div>
            </div>
          </div>

          <!-- MODAL SELECTOR DE PESTAÑAS (Para Formulario) -->
          <div id="modalTabsSelector" class="hidden absolute inset-0 bg-white z-50 p-4 flex flex-col">
            <div class="flex items-center justify-between border-b pb-2 mb-2">
              <div>
                <h3 class="font-extrabold text-sm text-[#6B1226]">Selecciona la Materia</h3>
                <p class="text-[10.5px] text-slate-500">17 pestañas jurídicas oficiales</p>
              </div>
              <button onclick="closeTabSelectorModal()" class="text-slate-400 hover:text-slate-600 text-lg font-bold">✕</button>
            </div>
            <div id="modalTabsList" class="flex-1 overflow-y-auto space-y-1.5 pr-1">
            </div>
          </div>

          <!-- BARRA INFERIOR / BOTÓN FLOTANTE CREAR CAUSA (Solo visible logueado) -->
          <div id="mainAppBottomBar" class="hidden bg-white border-t border-[#D4AF37] p-2.5 flex items-center justify-between shrink-0 shadow-lg">
            <button onclick="switchView('list')" class="flex flex-col items-center gap-0.5 text-[#6B1226] px-3 py-1">
              <span class="text-base">🏠</span>
              <span class="text-[9.5px] font-black uppercase tracking-wider">Causas</span>
            </button>

            <!-- Botón Central Crear Causa -->
            <button onclick="switchView('form')" class="bg-[#6B1226] hover:bg-[#520d1d] text-white px-4 py-2 rounded-xl border border-[#D4AF37] shadow font-extrabold text-xs flex items-center gap-1.5 active:scale-95 transition-transform">
              <span class="text-sm">➕</span> Crear Causa PGET
            </button>

            <button onclick="switchView('lawyers-admin')" class="flex flex-col items-center gap-0.5 text-slate-500 hover:text-[#6B1226] px-3 py-1">
              <span class="text-base">👥</span>
              <span class="text-[9.5px] font-bold uppercase tracking-wider">Nómina</span>
            </button>
          </div>

        </div>
      </div>
    </div>

    <!-- PANEL EXPLICATIVO DERECHA (Cols 5) -->
    <div class="lg:col-span-5 space-y-3">
      
      <!-- Tarjeta 1: Credenciales Oficiales de Acceso -->
      <div class="bg-white border-2 border-[#D4AF37] rounded-2xl p-4 shadow-sm">
        <div class="flex items-center justify-between mb-2">
          <div class="flex items-center gap-2 text-[#6B1226]">
            <span class="text-lg">⚖️</span>
            <h2 class="font-extrabold text-sm">Credenciales Oficiales PGET</h2>
          </div>
          <span class="text-[10px] bg-[#6B1226] text-[#D4AF37] px-2 py-0.5 rounded font-bold font-mono">Palacio de Gobierno</span>
        </div>
        <p class="text-xs text-slate-600 mb-2 leading-relaxed">
          Fondo institucional del Palacio de Gobierno con velo vinotinto transparente y pantalla de carga con <strong>mazo judicial golpeando (1,5 segundos)</strong>.
        </p>

        <!-- Cuadro Destacado: Administradora Institucional -->
        <div class="bg-amber-50 border-2 border-[#D4AF37] rounded-xl p-2.5 mb-2.5">
          <div class="flex items-center justify-between text-xs">
            <span class="font-extrabold text-[#6B1226] flex items-center gap-1">👑 DRA. LIZAMAR BRICEÑO</span>
            <span class="bg-[#6B1226] text-white text-[9.5px] font-black px-2 py-0.5 rounded">ADMINISTRADORA</span>
          </div>
          <div class="text-[11px] text-slate-700 mt-1 font-mono flex items-center justify-between">
            <span>Correo: <strong>lizamarbriceno@pget.com</strong></span>
            <span>Clave: <strong class="text-[#6B1226]">Admin2026*Lizamar</strong></span>
          </div>
          <div class="text-[10px] text-slate-500 mt-0.5">Control total de nómina institucional y auditoría del sistema.</div>
        </div>

        <!-- Lista de los 12 Abogados Adscritos -->
        <h4 class="text-[11px] font-black text-slate-700 uppercase tracking-wider mb-1.5">Abogados de Nómina (Nivel Abogado):</h4>
        <div class="space-y-1.5 text-xs max-h-60 overflow-y-auto pr-1">
          
          <div class="p-1.5 rounded-lg bg-slate-50 border border-slate-200">
            <div class="flex items-center justify-between font-bold text-slate-800">
              <span>1. BARRIOS JULIO ALEXANDER</span>
              <span class="text-[10px] text-slate-500 font-mono">ABOGADO I</span>
            </div>
            <div class="text-[10px] text-slate-600 font-mono flex items-center justify-between mt-0.5">
              <span>juliobarrios@pget.com</span>
              <span class="font-bold text-[#6B1226]">Pget2026*Julio</span>
            </div>
          </div>

          <div class="p-1.5 rounded-lg bg-slate-50 border border-slate-200">
            <div class="flex items-center justify-between font-bold text-slate-800">
              <span>2. BARRIOS MARIA ALCIRA</span>
              <span class="text-[10px] text-slate-500 font-mono">ABOGADO I</span>
            </div>
            <div class="text-[10px] text-slate-600 font-mono flex items-center justify-between mt-0.5">
              <span>mariabarrios@pget.com</span>
              <span class="font-bold text-[#6B1226]">Pget2026*Maria</span>
            </div>
          </div>

          <div class="p-1.5 rounded-lg bg-slate-50 border border-slate-200">
            <div class="flex items-center justify-between font-bold text-slate-800">
              <span>3. BRICEÑO FERNANDEZ ARMANDO JOSE</span>
              <span class="text-[10px] text-slate-500 font-mono">ABOGADO</span>
            </div>
            <div class="text-[10px] text-slate-600 font-mono flex items-center justify-between mt-0.5">
              <span>armandobriceno@pget.com</span>
              <span class="font-bold text-[#6B1226]">Pget2026*Armando</span>
            </div>
          </div>

          <div class="p-1.5 rounded-lg bg-slate-50 border border-slate-200">
            <div class="flex items-center justify-between font-bold text-slate-800">
              <span>4. DE ABREU HERNANDEZ CARLOS EDUARDO</span>
              <span class="text-[10px] text-slate-500 font-mono">ABOGADO I</span>
            </div>
            <div class="text-[10px] text-slate-600 font-mono flex items-center justify-between mt-0.5">
              <span>carlosdeabreu@pget.com</span>
              <span class="font-bold text-[#6B1226]">Pget2026*Carlos</span>
            </div>
          </div>

          <div class="p-1.5 rounded-lg bg-slate-50 border border-slate-200">
            <div class="flex items-center justify-between font-bold text-slate-800">
              <span>5. DORA ALICIA MATHEUS</span>
              <span class="text-[10px] text-[#D4AF37] bg-[#6B1226] px-1.5 rounded font-bold">PROCURADORA</span>
            </div>
            <div class="text-[10px] text-slate-600 font-mono flex items-center justify-between mt-0.5">
              <span>doramatheus@pget.com</span>
              <span class="font-bold text-[#6B1226]">Pget2026*Dora</span>
            </div>
          </div>

          <div class="p-1.5 rounded-lg bg-slate-50 border border-slate-200">
            <div class="flex items-center justify-between font-bold text-slate-800">
              <span>6. MERCADO HIDALGO ROXANNA KAROLINA</span>
              <span class="text-[10px] text-slate-500 font-mono">ABOGADO I</span>
            </div>
            <div class="text-[10px] text-slate-600 font-mono flex items-center justify-between mt-0.5">
              <span>roxannamercado@pget.com</span>
              <span class="font-bold text-[#6B1226]">Pget2026*Roxanna</span>
            </div>
          </div>

          <div class="p-1.5 rounded-lg bg-slate-50 border border-slate-200">
            <div class="flex items-center justify-between font-bold text-slate-800">
              <span>7. MOLINA UZCATEGUI HUMBERTO JOSE</span>
              <span class="text-[10px] text-slate-500 font-mono">ABOGADO</span>
            </div>
            <div class="text-[10px] text-slate-600 font-mono flex items-center justify-between mt-0.5">
              <span>humbertomolina@pget.com</span>
              <span class="font-bold text-[#6B1226]">Pget2026*Humberto</span>
            </div>
          </div>

          <div class="p-1.5 rounded-lg bg-slate-50 border border-slate-200">
            <div class="flex items-center justify-between font-bold text-slate-800">
              <span>8. MORENO HERNANDEZ YONEXI CAROLINA</span>
              <span class="text-[10px] text-slate-500 font-mono">ABOGADO</span>
            </div>
            <div class="text-[10px] text-slate-600 font-mono flex items-center justify-between mt-0.5">
              <span>yoneximoreno@pget.com</span>
              <span class="font-bold text-[#6B1226]">Pget2026*Yonexi</span>
            </div>
          </div>

          <div class="p-1.5 rounded-lg bg-slate-50 border border-slate-200">
            <div class="flex items-center justify-between font-bold text-slate-800">
              <span>9. OJEDA NUÑEZ MARIA DE LOS ANGELES</span>
              <span class="text-[10px] text-slate-500 font-mono">ABOGADO I</span>
            </div>
            <div class="text-[10px] text-slate-600 font-mono flex items-center justify-between mt-0.5">
              <span>mariaojeda@pget.com</span>
              <span class="font-bold text-[#6B1226]">Pget2026*MariaO</span>
            </div>
          </div>

          <div class="p-1.5 rounded-lg bg-slate-50 border border-slate-200">
            <div class="flex items-center justify-between font-bold text-slate-800">
              <span>10. RAMIREZ OROPEZA TATIANA MARILIN</span>
              <span class="text-[10px] text-slate-500 font-mono">ABOGADO I</span>
            </div>
            <div class="text-[10px] text-slate-600 font-mono flex items-center justify-between mt-0.5">
              <span>tatianaramirez@pget.com</span>
              <span class="font-bold text-[#6B1226]">Pget2026*Tatiana</span>
            </div>
          </div>

          <div class="p-1.5 rounded-lg bg-slate-50 border border-slate-200">
            <div class="flex items-center justify-between font-bold text-slate-800">
              <span>11. SANCHEZ MONSALVE LILIBETH DAYANA</span>
              <span class="text-[10px] text-slate-500 font-mono">ABOGADO I</span>
            </div>
            <div class="text-[10px] text-slate-600 font-mono flex items-center justify-between mt-0.5">
              <span>lilibethsanchez@pget.com</span>
              <span class="font-bold text-[#6B1226]">Pget2026*Lilibeth</span>
            </div>
          </div>

          <div class="p-1.5 rounded-lg bg-slate-50 border border-slate-200">
            <div class="flex items-center justify-between font-bold text-slate-800">
              <span>12. VALE VALERA YULIANOVA PAOLA</span>
              <span class="text-[10px] text-slate-500 font-mono">ABOGADO I</span>
            </div>
            <div class="text-[10px] text-slate-600 font-mono flex items-center justify-between mt-0.5">
              <span>paolavale@pget.com</span>
              <span class="font-bold text-[#6B1226]">Pget2026*Paola</span>
            </div>
          </div>

        </div>
      </div>

      <!-- Tarjeta 2: Animación Judicial -->
      <div class="bg-slate-50 border border-slate-200 rounded-2xl p-3.5 text-xs text-slate-600 space-y-1.5">
        <div class="font-extrabold text-slate-800 text-[11px] uppercase tracking-wide">Efectos Implementados:</div>
        <div>✔ <strong>Fondo:</strong> Fachada real del Palacio de Gobierno con velo vinotinto institucional.</div>
        <div>✔ <strong>Ojo Minimalista:</strong> Icono de trazo vectorial para ver/ocultar contraseña.</div>
        <div>✔ <strong>Mazo de Juez:</strong> Al presionar "Iniciar Sesión", un mazo judicial impacta la base durante <strong>1,5 segundos exactos</strong> antes de abrir la aplicación.</div>
      </div>

    </div>

  </div>

  <script>
    // Base de Datos Institucional de Usuarios y Credenciales
    const usersDatabase = [
      {{ id: "4", nombre: "BRICEÑO VALECILLOS LIZAMAR INDIRA", correo: "lizamarbriceno@pget.com", clave: "Admin2026*Lizamar", rol: "admin", cargo: "DIRECTOR DE ASUNTOS JURIDICOS", cedula: "20.400.747", shortName: "Dra. Lizamar Briceño" }},
      {{ id: "1", nombre: "BARRIOS JULIO ALEXANDER", correo: "juliobarrios@pget.com", clave: "Pget2026*Julio", rol: "lawyer", cargo: "ABOGADO I", cedula: "14.459.865", shortName: "Abg. Julio Barrios" }},
      {{ id: "2", nombre: "BARRIOS MARIA ALCIRA", correo: "mariabarrios@pget.com", clave: "Pget2026*Maria", rol: "lawyer", cargo: "ABOGADO I", cedula: "17.037.437", shortName: "Abg. María Barrios" }},
      {{ id: "3", nombre: "BRICEÑO FERNANDEZ ARMANDO JOSE", correo: "armandobriceno@pget.com", clave: "Pget2026*Armando", rol: "lawyer", cargo: "ABOGADO", cedula: "5.780.167", shortName: "Abg. Armando Briceño" }},
      {{ id: "5", nombre: "DE ABREU HERNANDEZ CARLOS EDUARDO", correo: "carlosdeabreu@pget.com", clave: "Pget2026*Carlos", rol: "lawyer", cargo: "ABOGADO I", cedula: "10.446.852", shortName: "Abg. Carlos De Abreu" }},
      {{ id: "6", nombre: "DORA ALICIA MATHEUS", correo: "doramatheus@pget.com", clave: "Pget2026*Dora", rol: "lawyer", cargo: "PROCURADORA", cedula: "10.035.929", shortName: "Dra. Dora Matheus" }},
      {{ id: "7", nombre: "MERCADO HIDALGO ROXANNA KAROLINA", correo: "roxannamercado@pget.com", clave: "Pget2026*Roxanna", rol: "lawyer", cargo: "ABOGADO I", cedula: "23.596.460", shortName: "Dra. Roxanna Mercado" }},
      {{ id: "8", nombre: "MOLINA UZCATEGUI HUMBERTO JOSE", correo: "humbertomolina@pget.com", clave: "Pget2026*Humberto", rol: "lawyer", cargo: "ABOGADO", cedula: "20.790.382", shortName: "Abg. Humberto Molina" }},
      {{ id: "9", nombre: "MORENO HERNANDEZ YONEXI CAROLINA", correo: "yoneximoreno@pget.com", clave: "Pget2026*Yonexi", rol: "lawyer", cargo: "ABOGADO", cedula: "16.738.909", shortName: "Abg. Yonexi Moreno" }},
      {{ id: "10", nombre: "OJEDA NUÑEZ MARIA DE LOS ANGELES", correo: "mariaojeda@pget.com", clave: "Pget2026*MariaO", rol: "lawyer", cargo: "ABOGADO I", cedula: "26.046.163", shortName: "Dra. María de los Ángeles Ojeda" }},
      {{ id: "11", nombre: "RAMIREZ OROPEZA TATIANA MARILIN", correo: "tatianaramirez@pget.com", clave: "Pget2026*Tatiana", rol: "lawyer", cargo: "ABOGADO I", cedula: "15.315.709", shortName: "Abg. Tatiana Ramírez" }},
      {{ id: "12", nombre: "SANCHEZ MONSALVE LILIBETH DAYANA", correo: "lilibethsanchez@pget.com", clave: "Pget2026*Lilibeth", rol: "lawyer", cargo: "ABOGADO I", cedula: "13.404.142", shortName: "Abg. Lilibeth Sánchez" }},
      {{ id: "13", nombre: "VALE VALERA YULIANOVA PAOLA", correo: "paolavale@pget.com", clave: "Pget2026*Paola", rol: "lawyer", cargo: "ABOGADO I", cedula: "26.591.763", shortName: "Abg. Paola Vale" }}
    ];

    let currentUser = null;
    let currentRole = 'admin'; // 'admin' | 'lawyer'

    // Definición de las 17 Pestañas Jurídicas Reales
    const tabsData = [
      {{ id: "juzgados", title: "JUZGADOS Y TRIBUNALES", category: "Juzgados", icon: "⚖️", columns: ["N° EXPEDIENTE", "FECHA INGRESO", "ASUNTO / MOTIVO", "DEMANDANTE", "DEMANDADO", "TRIBUNAL", "ABOGADO RESPONSABLE", "ESTADO"] }},
      {{ id: "contencioso_admon", title: "CONTENCIOSO ADMINISTRATIVO", category: "Contencioso", icon: "🏛️", columns: ["N° EXP.", "FECHA", "ACCIONANTE", "ACCIONADO", "MOTIVO DE LA ACCIÓN", "TRIBUNAL DE ORIGEN", "ABOGADO DESIGNADO", "ESTATUS ACTUAL"] }},
      {{ id: "contencioso_trujillo", title: "CONTENCIOSO TRUJILLO", category: "Contencioso", icon: "🏛️", columns: ["N° EXPEDIENTE", "FECHA INGRESO", "PARTES", "OBJETO DEL LITIGIO", "JUZGADO", "ABOGADO RESPONSABLE", "ESTADO"] }},
      {{ id: "laboral", title: "LABORAL", category: "Laboral", icon: "👷", columns: ["N°", "FECHA", "TRABAJADOR / ACCIONANTE", "ORGANISMO / ENTE DEMANDADO", "MOTIVO DE DEMANDA", "TRIBUNAL LABORAL", "ABOGADO RESPONSABLE", "FASE PROCESAL"] }},
      {{ id: "inspectorias", title: "INSPECTORÍAS DEL TRABAJO", category: "Laboral", icon: "📑", columns: ["N° RECLAMO", "FECHA", "TRABAJADOR", "PATRONO", "PROCEDIMIENTO", "INSPECTORÍA", "ABOGADO", "ESTADO"] }},
      {{ id: "inspectoria_trujillo", title: "INSPECTORIA TRUJILLO", category: "Laboral", icon: "📑", columns: ["EXPEDIENTE", "FECHA", "RECLAMANTE", "RECLAMADO", "CAUSA", "ABOGADO", "ESTATUS"] }},
      {{ id: "inspectoria_bocono", title: "INSPECTORIA BOCONO", category: "Laboral", icon: "📑", columns: ["N° EXP.", "FECHA", "TRABAJADOR", "ENTE", "ASUNTO", "ABOGADO ASIGNADO", "ESTADO"] }},
      {{ id: "inspectoria_sabana_mendoza", title: "INSPECTORIA SABANA DE MENDOZA", category: "Laboral", icon: "📑", columns: ["EXPEDIENTE", "FECHA", "PARTES", "MOTIVO", "ABOGADO", "ESTATUS"] }},
      {{ id: "civil", title: "CIVIL", category: "Civil y Bienes", icon: "📜", columns: ["N° EXPEDIENTE", "FECHA", "DEMANDANTE", "DEMANDADO", "ACCION CIVIL", "JUZGADO CIVIL", "ABOGADO PGET", "ESTADO"] }},
      {{ id: "amparos", title: "AMPAROS CONSTITUCIONALES", category: "Constitucional", icon: "🛡️", columns: ["N° ACCION", "FECHA", "ACCIONANTE", "AGRAVIANTE", "DERECHO VULNERADO", "SALA / JUZGADO", "ABOGADO DEFENSOR", "ESTADO"] }},
      {{ id: "penal", title: "PENAL", category: "Penal", icon: "⚖️", columns: ["N° CAUSA", "FECHA", "IMPUTADO / VICTIMA", "DELITO IMPUTADO", "FISCALIA / TRIBUNAL", "ABOGADO ASIGNADO", "FASE ACTUAL"] }},
      {{ id: "tierras", title: "TIERRAS", category: "Agrario", icon: "🌱", columns: ["N° PROCEDIMIENTO", "FECHA", "SOLICITANTE", "PREDIO / POLIGONAL", "TRIBUNAL AGRARIO", "ABOGADO ASIGNADO", "ESTADO"] }},
      {{ id: "mercantil", title: "MERCANTIL", category: "Civil y Bienes", icon: "💼", columns: ["N° EXP.", "FECHA", "ACTOR", "DEMANDADO", "NATURALEZA MERCANTIL", "JUZGADO", "ABOGADO", "ESTADO"] }},
      {{ id: "tributario", title: "TRIBUTARIO", category: "Fiscal", icon: "💰", columns: ["N° EXPEDIENTE", "FECHA", "CONTRIBUYENTE", "TRIBUTO / REPARO", "TRIBUNAL FISCAL", "ABOGADO", "ESTADO"] }},
      {{ id: "proteccion", title: "PROTECCIÓN NIÑOS Y ADOLESCENTES", category: "Especial", icon: "👶", columns: ["N° EXP.", "FECHA", "SOLICITANTE", "MEDIDA SOLICITADA", "TRIBUNAL PROTECCIÓN", "ABOGADO", "ESTADO"] }},
      {{ id: "transito", title: "TRÁNSITO", category: "Especial", icon: "🚗", columns: ["N° CAUSA", "FECHA", "INVOLUCRADOS", "TRIBUNAL DE TRÁNSITO", "ABOGADO", "ESTADO"] }},
      {{ id: "casacion", title: "CASACIÓN", category: "Tribunal Supremo", icon: "🏛️", columns: ["N° EXPEDIENTE TSJ", "FECHA RECURSO", "RECURRENTE", "SALA TSJ", "MOTIVO CASACIÓN", "ABOGADO PGET", "ESTADO"] }}
    ];

    // Nómina Oficial PGET: 13 Abogados Activos (Ordenados Alfabéticamente) + Históricos
    let lawyers = [
      // --- 13 ABOGADOS ACTIVOS OFICIALES (Ordenados Alfabéticamente A-Z) ---
      {{ id: "1", nombre: "BARRIOS JULIO ALEXANDER", cedula: "14.459.865", cargo: "ABOGADO I", adscrito: "PROCURADURÍA GENERAL", activo: true }},
      {{ id: "2", nombre: "BARRIOS MARIA ALCIRA", cedula: "17.037.437", cargo: "ABOGADO I", adscrito: "PROCURADURÍA GENERAL", activo: true }},
      {{ id: "3", nombre: "BRICEÑO FERNANDEZ ARMANDO JOSE", cedula: "5.780.167", cargo: "ABOGADO", adscrito: "CONTENCIOSO ADMINISTRATIVO", activo: true }},
      {{ id: "4", nombre: "BRICEÑO VALECILLOS LIZAMAR INDIRA", cedula: "20.400.747", cargo: "DIRECTOR DE ASUNTOS JURIDICOS", adscrito: "DIRECCIÓN DE ASUNTOS JURÍDICOS", activo: true }},
      {{ id: "5", nombre: "DE ABREU HERNANDEZ CARLOS EDUARDO", cedula: "10.446.852", cargo: "ABOGADO I", adscrito: "PROCURADURÍA GENERAL", activo: true }},
      {{ id: "6", nombre: "DORA ALICIA MATHEUS", cedula: "10.035.929", cargo: "PROCURADORA", adscrito: "DESPACHO DE LA PROCURADORA", activo: true }},
      {{ id: "7", nombre: "MERCADO HIDALGO ROXANNA KAROLINA", cedula: "23.596.460", cargo: "ABOGADO I", adscrito: "JUZGADOS Y TRIBUNALES", activo: true }},
      {{ id: "8", nombre: "MOLINA UZCATEGUI HUMBERTO JOSE", cedula: "20.790.382", cargo: "ABOGADO", adscrito: "PROCURADURÍA GENERAL", activo: true }},
      {{ id: "9", nombre: "MORENO HERNANDEZ YONEXI CAROLINA", cedula: "16.738.909", cargo: "ABOGADO", adscrito: "PROCURADURÍA GENERAL", activo: true }},
      {{ id: "10", nombre: "OJEDA NUÑEZ MARIA DE LOS ANGELES", cedula: "26.046.163", cargo: "ABOGADO I", adscrito: "CONTENCIOSO TRUJILLO", activo: true }},
      {{ id: "11", nombre: "RAMIREZ OROPEZA TATIANA MARILIN", cedula: "15.315.709", cargo: "ABOGADO I", adscrito: "PROCURADURÍA GENERAL", activo: true }},
      {{ id: "12", nombre: "SANCHEZ MONSALVE LILIBETH DAYANA", cedula: "13.404.142", cargo: "ABOGADO I", adscrito: "PROCURADURÍA GENERAL", activo: true }},
      {{ id: "13", nombre: "VALE VALERA YULIANOVA PAOLA", cedula: "26.591.763", cargo: "ABOGADO I", adscrito: "PROCURADURÍA GENERAL", activo: true }},

      // --- ABOGADOS HISTÓRICOS (Preservados en causas y expedientes anteriores de Google Sheets) ---
      {{ id: "14", nombre: "SAMANTHA POLANCO", cedula: "5.493.478", cargo: "Apoderada Judicial", adscrito: "CORPOTURISMO / PGET", activo: false, historico: true }},
      {{ id: "15", nombre: "ANAIS PERDOMO", cedula: "19.876.543", cargo: "Especialista Laboral", adscrito: "LABORAL E INSPECTORÍAS", activo: false, historico: true }},
      {{ id: "16", nombre: "EDGARDO BASTIDAS", cedula: "16.234.567", cargo: "Abogado Litigante", adscrito: "PENAL Y AMPAROS", activo: false, historico: true }},
      {{ id: "17", nombre: "MARIA FERNANDA PEÑA", cedula: "21.345.678", cargo: "Consultora Jurídica", adscrito: "TRIBUTARIO Y MERCANTIL", activo: false, historico: true }},
      {{ id: "18", nombre: "YELITZA VÁSQUEZ", cedula: "15.432.109", cargo: "Abogada de Sustanciación", adscrito: "CIVIL Y BIENES", activo: false, historico: true }},
      {{ id: "19", nombre: "JESÚS ROJAS", cedula: "14.567.890", cargo: "Abogado Asistente", adscrito: "CONTENCIOSO TRUJILLO", activo: false, historico: true }},
      {{ id: "20", nombre: "MARÍA VALERA", cedula: "22.345.671", cargo: "Abogada Litigante", adscrito: "LABORAL", activo: false, historico: true }},
      {{ id: "21", nombre: "YURAIMA ALDANA", cedula: "13.987.654", cargo: "Abogada de Sustanciación", adscrito: "TIERRAS Y AGRARIO", activo: false, historico: true }},
      {{ id: "22", nombre: "FRANCISCO MORENO", cedula: "11.234.567", cargo: "Abogado Asesor", adscrito: "CASACIÓN Y TSJ", activo: false, historico: true }},
      {{ id: "23", nombre: "ZULAY CARRILLO", cedula: "17.890.123", cargo: "Abogada Litigante", adscrito: "JUZGADOS Y TRIBUNALES", activo: false, historico: true }},
      {{ id: "24", nombre: "CARLOS MARÍN", cedula: "18.901.234", cargo: "Abogado Asistente", adscrito: "PROTECCIÓN NIÑOS", activo: false, historico: true }},
      {{ id: "25", nombre: "GREGORIO DELGADO", cedula: "15.678.901", cargo: "Abogado Litigante", adscrito: "TRÁNSITO", activo: false, historico: true }},
      {{ id: "26", nombre: "ADOLFO SÁNCHEZ", cedula: "16.789.012", cargo: "Abogado Litigante", adscrito: "CONTENCIOSO ADMINISTRATIVO", activo: false, historico: true }},
      {{ id: "27", nombre: "RAFAEL VILORIA", cedula: "14.890.123", cargo: "Abogado Adscrito", adscrito: "AMPAROS", activo: false, historico: true }},
      {{ id: "28", nombre: "MIRYAM MONTERO", cedula: "12.901.234", cargo: "Consultora Adjunta", adscrito: "ADMINISTRACIÓN", activo: false, historico: true }},
      {{ id: "29", nombre: "JOSÉ LUIS BRICEÑO", cedula: "13.012.345", cargo: "Abogado Litigante", adscrito: "LABORAL", activo: false, historico: true }},
      {{ id: "30", nombre: "ANDREINA SEGOVIA", cedula: "19.345.678", cargo: "Abogada Asistente", adscrito: "CONTENCIOSO TRUJILLO", activo: false, historico: true }},
      {{ id: "31", nombre: "VERÓNICA MARKAN", cedula: "14.234.567", cargo: "Abogada de Sustanciación", adscrito: "JUZGADOS Y TRIBUNALES", activo: false, historico: true }}
    ];

    // Registro de Auditoría
    let auditLogs = [
      {{ id: "1", fecha: "29/10/2026, 01:30 PM", usuario: "Lizamar Briceño (Admin)", accion: "LOGIN", expediente: "SISTEMA", pestana: "SEGURIDAD", detalle: "Autenticación concedida con firma judicial (Palacio de Gobierno)." }},
      {{ id: "2", fecha: "29/10/2026, 12:45 PM", usuario: "Admin PGET", accion: "MODIFICACIÓN NÓMINA", expediente: "NÓMINA", pestana: "ADMINISTRACIÓN", detalle: "Actualización de nómina oficial activa: 13 abogados (A-Z)." }},
      {{ id: "3", fecha: "29/10/2026, 11:35 AM", usuario: "Roxanna Mercado", accion: "MODIFICACIÓN CAUSA", expediente: "TP11-G-2022-000006", pestana: "CONTENCIOSO TRUJILLO", detalle: "Actualización de auto y estado de sustanciación." }}
    ];

    const causasPorPestana = {causes_by_tab_json};
    const availableYears = {years_json};

    let currentSelectedTab = tabsData[2]; // Default a CONTENCIOSO TRUJILLO
    let formSelectedTab = tabsData[2];
    let currentEstadoFilter = 'ALL';
    let toastTimeout = null;

    function init() {{
      populateTabsDropdown();
      populateYearsDropdown();
      populateModalTabs();
      populateEditLawyerSelect();
      renderLawyers();
      renderAuditLogs();
      renderCausas();
    }}

    // TOGGLE MINIMALISTA DE CONTRASEÑA
    function togglePasswordVisibility() {{
      const p = document.getElementById('loginPassword');
      const eyeOpen = document.getElementById('eyeIconOpen');
      const eyeClosed = document.getElementById('eyeIconClosed');

      if (p.type === 'password') {{
        p.type = 'text';
        eyeOpen.classList.add('hidden');
        eyeClosed.classList.remove('hidden');
      }} else {{
        p.type = 'password';
        eyeOpen.classList.remove('hidden');
        eyeClosed.classList.add('hidden');
      }}
    }}

    function applyQuickLogin() {{
      const selEmail = document.getElementById('quickLoginSelect').value;
      const user = usersDatabase.find(u => u.correo === selEmail);
      if (user) {{
        document.getElementById('loginEmail').value = user.correo;
        document.getElementById('loginPassword').value = user.clave;
      }}
    }}

    // INICIAR SESIÓN CON PANTALLA DE CARGA DEL MAZO DE JUEZ (1,5 SEG)
    function handleLogin() {{
      const email = document.getElementById('loginEmail').value.trim().toLowerCase();
      const pass = document.getElementById('loginPassword').value.trim();

      const user = usersDatabase.find(u => u.correo.toLowerCase() === email && u.clave === pass);

      if (!user) {{
        showToast("Credenciales incorrectas. Verifica tu correo y clave.", "error");
        return;
      }}

      // 1. Mostrar pantalla de carga con el Mazo de Juez golpeando
      const loading = document.getElementById('gavelLoadingOverlay');
      loading.classList.remove('hidden');

      // 2. Duración exacta de 1,5 segundos (1500 ms)
      setTimeout(() => {{
        loading.classList.add('hidden');

        currentUser = user;
        currentRole = user.rol; // 'admin' | 'lawyer'

        // Actualizar Header
        document.getElementById('headerUserName').innerText = user.shortName || user.nombre;
        document.getElementById('headerUserRole').innerText = user.rol === 'admin' ? 'ADMIN' : 'ABOGADO';

        const adminSubbar = document.getElementById('admin-subbar');
        const lawyerBadge = document.getElementById('lawyer-badge');

        if (user.rol === 'admin') {{
          adminSubbar.classList.remove('hidden');
          lawyerBadge.classList.add('hidden');
        }} else {{
          adminSubbar.classList.add('hidden');
          lawyerBadge.classList.remove('hidden');
        }}

        // Mostrar interfaz principal
        document.getElementById('view-login').classList.add('hidden');
        document.getElementById('mainAppHeader').classList.remove('hidden');
        document.getElementById('mainAppBottomBar').classList.remove('hidden');
        document.getElementById('view-list').classList.remove('hidden');

        addAuditLog("LOGIN", "AUTENTICACIÓN", "SEGURIDAD", `Inicio de sesión exitoso: ${{user.nombre}} (${{user.cargo}}).`);
        showToast(`¡Audiencia abierta! Bienvenido(a), ${{user.shortName}}`, "success");
        renderCausas();
      }}, 1500);
    }}

    function handleLogout() {{
      currentUser = null;
      document.getElementById('view-list').classList.add('hidden');
      document.getElementById('view-lawyers-admin').classList.add('hidden');
      document.getElementById('view-audit-admin').classList.add('hidden');
      document.getElementById('view-form').classList.add('hidden');
      document.getElementById('mainAppHeader').classList.add('hidden');
      document.getElementById('mainAppBottomBar').classList.add('hidden');

      document.getElementById('view-login').classList.remove('hidden');
      showToast("Sesión cerrada correctamente", "info");
    }}

    // In-App Toast System
    function showToast(message, type = 'success') {{
      const toast = document.getElementById('appToast');
      const inner = document.getElementById('appToastInner');
      const icon = document.getElementById('toastIcon');
      const msg = document.getElementById('toastMsg');

      msg.innerText = message;
      if (type === 'success') {{
        icon.innerText = '✅';
        inner.className = 'bg-emerald-950 text-emerald-100 text-xs font-bold px-3 py-2 rounded-xl border border-emerald-400 shadow-xl flex items-center gap-2';
      }} else if (type === 'error' || type === 'danger') {{
        icon.innerText = '❌';
        inner.className = 'bg-rose-950 text-rose-100 text-xs font-bold px-3 py-2 rounded-xl border border-rose-400 shadow-xl flex items-center gap-2';
      }} else if (type === 'warning') {{
        icon.innerText = '⚠️';
        inner.className = 'bg-amber-950 text-amber-100 text-xs font-bold px-3 py-2 rounded-xl border border-amber-400 shadow-xl flex items-center gap-2';
      }} else {{
        icon.innerText = 'ℹ️';
        inner.className = 'bg-slate-900 text-white text-xs font-bold px-3 py-2 rounded-xl border border-[#D4AF37] shadow-xl flex items-center gap-2';
      }}

      toast.classList.remove('opacity-0', '-translate-y-3', 'pointer-events-none');
      toast.classList.add('opacity-100', 'translate-y-0');

      if (toastTimeout) clearTimeout(toastTimeout);
      toastTimeout = setTimeout(() => {{
        toast.classList.remove('opacity-100', 'translate-y-0');
        toast.classList.add('opacity-0', '-translate-y-3', 'pointer-events-none');
      }}, 3000);
    }}

    // In-DOM Modal Helpers
    function closeModals() {{
      document.getElementById('modalBackdrop').classList.add('hidden');
      document.getElementById('modalEditLawyer').classList.add('hidden');
      document.getElementById('modalDeactivateLawyer').classList.add('hidden');
      document.getElementById('modalReactivateLawyer').classList.add('hidden');
      document.getElementById('modalAddLawyer').classList.add('hidden');
      document.getElementById('modalEditCausa').classList.add('hidden');
      document.getElementById('modalDeleteCausa').classList.add('hidden');
    }}

    function openModal(modalId) {{
      closeModals();
      document.getElementById('modalBackdrop').classList.remove('hidden');
      document.getElementById(modalId).classList.remove('hidden');
    }}

    function populateTabsDropdown() {{
      const select = document.getElementById('sheetTabSelect');
      select.innerHTML = tabsData.map(t => 
        `<option value="${{t.title}}" ${{t.title === currentSelectedTab.title ? 'selected' : ''}}>${{t.title}}</option>`
      ).join('');
    }}

    function populateYearsDropdown() {{
      const select = document.getElementById('yearFilterSelect');
      let options = '<option value="TODOS">Año: Todos</option>';
      availableYears.forEach(y => {{
        options += `<option value="${{y}}">Año: ${{y}}</option>`;
      }});
      select.innerHTML = options;
    }}

    function populateEditLawyerSelect() {{
      const select = document.getElementById('editCausaAbg');
      if (!select) return;
      select.innerHTML = lawyers.filter(l => l.activo).map(l => 
        `<option value="${{l.nombre}}">${{l.nombre}}</option>`
      ).join('');
    }}

    function populateModalTabs() {{
      const container = document.getElementById('modalTabsList');
      container.innerHTML = tabsData.map(t => `
        <div onclick="selectTabForForm('${{t.title}}')" class="p-2.5 rounded-xl border border-[#D4AF37]/50 bg-slate-50 hover:bg-amber-50 hover:border-[#D4AF37] cursor-pointer flex items-center justify-between transition-all">
          <div class="flex items-center gap-2.5">
            <div class="w-8 h-8 rounded-lg bg-[#6B1226] text-[#D4AF37] flex items-center justify-center shrink-0 border border-[#D4AF37] text-sm">
              ${{t.icon}}
            </div>
            <div>
              <div class="font-extrabold text-xs text-[#6B1226] leading-tight">${{t.title}}</div>
              <div class="text-[10px] text-slate-500">${{t.category}} • ${{t.columns.length}} Columnas</div>
            </div>
          </div>
          <span class="text-[#D4AF37] font-bold">›</span>
        </div>
      `).join('');
    }}

    function onTabChanged() {{
      const val = document.getElementById('sheetTabSelect').value;
      currentSelectedTab = tabsData.find(t => t.title === val) || tabsData[0];
      renderCausas();
    }}

    function renderCausas() {{
      const container = document.getElementById('causasContainer');
      const search = document.getElementById('searchInput').value.toLowerCase();
      const yrFilter = document.getElementById('yearFilterSelect').value;

      const rawList = causasPorPestana[currentSelectedTab.title] || [];

      const filtered = rawList.filter(c => {{
        if (currentEstadoFilter === 'ACT' && !c.estado.toUpperCase().includes('ACT')) return false;
        if (currentEstadoFilter === 'CERR' && !c.estado.toUpperCase().includes('CERR')) return false;

        if (yrFilter !== 'TODOS' && c.year !== yrFilter && !c.fecha.includes(yrFilter) && !c.expediente.includes(yrFilter)) {{
          return false;
        }}

        if (search) {{
          const str = (c.expediente + ' ' + c.motivo + ' ' + c.demandado + ' ' + c.abogado).toLowerCase();
          if (!str.includes(search)) return false;
        }}

        return true;
      }});

      document.getElementById('stat-total').innerText = rawList.length;
      document.getElementById('stat-active').innerText = rawList.filter(c => c.estado.toUpperCase().includes('ACT')).length;
      document.getElementById('stat-closed').innerText = rawList.filter(c => c.estado.toUpperCase().includes('CERR')).length;

      if (filtered.length === 0) {{
        container.innerHTML = `
          <div class="text-center py-8 text-slate-400">
            <div class="text-2xl mb-1 text-[#6B1226]">📂</div>
            <p class="text-xs font-bold text-[#6B1226]">Sin resultados en "${{currentSelectedTab.title}}"</p>
            <p class="text-[11px] text-slate-400">Total en esta materia: ${{rawList.length}} causas registradas.</p>
            <p class="text-[10px] text-slate-400">Prueba cambiando el filtro de año (${{yrFilter}}) o búsqueda.</p>
          </div>
        `;
        return;
      }}

      container.innerHTML = filtered.map(c => {{
        const isAct = c.estado.toUpperCase().includes('ACT');
        return `
          <div class="bg-white p-2.5 rounded-xl border border-[#D4AF37] shadow-sm">
            <div class="flex items-center justify-between mb-1">
              <span class="bg-[#6B1226] text-white text-[10px] font-extrabold px-2 py-0.5 rounded border border-[#D4AF37]">
                EXP. ${{c.expediente}}
              </span>
              <div class="flex items-center gap-1">
                ${{c.year ? `<span class="text-[9.5px] bg-amber-50 text-amber-900 border border-amber-300 font-bold px-1.5 py-0.2 rounded">${{c.year}}</span>` : ''}}
                <span class="text-[10px] font-bold px-2 py-0.5 rounded-full ${{isAct ? 'bg-emerald-100 text-emerald-800 border border-emerald-300' : 'bg-slate-100 text-slate-600 border border-slate-300'}}">
                  ${{c.estado}}
                </span>
              </div>
            </div>

            <h4 class="font-bold text-xs text-[#6B1226] leading-snug line-clamp-2 my-1">${{c.motivo}}</h4>
            ${{c.demandado ? `<p class="text-[11px] text-slate-600 truncate"><strong class="text-slate-400">Contra:</strong> ${{c.demandado}}</p>` : ''}}

            <div class="mt-2 pt-1 border-t border-slate-100 flex items-center justify-between text-[10.5px]">
              <span class="text-[#6B1226] font-bold truncate max-w-[140px]" title="${{c.abogado}}">
                ⚖️ ${{c.abogado}}
              </span>
              
              <div class="flex items-center gap-1.5">
                <button onclick="openEditCausaModal(${{c.row_index}})" title="Editar Causa" class="px-2 py-0.5 rounded bg-amber-50 hover:bg-amber-100 text-amber-800 border border-amber-300 font-bold text-[9.5px] flex items-center gap-1">
                  ✏️ Editar
                </button>
                <button onclick="openDeleteCausaModal(${{c.row_index}})" title="Eliminar Causa" class="px-2 py-0.5 rounded bg-rose-50 hover:bg-rose-100 text-rose-700 border border-rose-300 font-bold text-[9.5px] flex items-center gap-1">
                  🗑️ Eliminar
                </button>
              </div>
            </div>
          </div>
        `;
      }}).join('');
    }}

    function setEstadoFilter(est, btn) {{
      currentEstadoFilter = est;
      document.querySelectorAll('.chip-estado').forEach(b => {{
        b.className = "chip-estado bg-white text-slate-700 px-2.5 py-0.5 rounded-full font-semibold shrink-0 border border-[#C5A059]";
      }});
      btn.className = "chip-estado bg-[#6B1226] text-white px-2.5 py-0.5 rounded-full font-bold shrink-0 border border-[#D4AF37]";
      renderCausas();
    }}

    // CAUSA EDIT MODAL LOGIC (IN-DOM)
    function openEditCausaModal(rowIndex) {{
      const tabTitle = currentSelectedTab.title;
      const list = causasPorPestana[tabTitle] || [];
      const causa = list.find(c => c.row_index === rowIndex);
      if (!causa) return;

      document.getElementById('editCausaRowIndex').value = rowIndex;
      document.getElementById('editCausaExp').value = causa.expediente;
      document.getElementById('editCausaMot').value = causa.motivo;
      document.getElementById('editCausaDmd').value = causa.demandado || '';
      
      populateEditLawyerSelect();
      const abgSelect = document.getElementById('editCausaAbg');
      if (abgSelect) {{
        abgSelect.value = causa.abogado;
        if (!abgSelect.value) {{
          const opt = document.createElement('option');
          opt.value = causa.abogado;
          opt.innerText = causa.abogado + ' (Histórico)';
          opt.selected = true;
          abgSelect.appendChild(opt);
        }}
      }}

      const estSelect = document.getElementById('editCausaEst');
      if (estSelect) {{
        estSelect.value = causa.estado.includes('CERR') ? 'CERRADA' : 'ACTIVA';
      }}

      openModal('modalEditCausa');
    }}

    function saveCausaEditAction() {{
      const rowIndex = parseInt(document.getElementById('editCausaRowIndex').value);
      const tabTitle = currentSelectedTab.title;
      const list = causasPorPestana[tabTitle] || [];
      const causa = list.find(c => c.row_index === rowIndex);
      if (!causa) return;

      const exp = document.getElementById('editCausaExp').value.trim();
      const mot = document.getElementById('editCausaMot').value.trim();
      const dmd = document.getElementById('editCausaDmd').value.trim();
      const abg = document.getElementById('editCausaAbg').value;
      const est = document.getElementById('editCausaEst').value;

      if (!exp || !mot) {{
        showToast("El expediente y motivo son requeridos", "warning");
        return;
      }}

      causa.expediente = exp;
      causa.motivo = mot;
      causa.demandado = dmd;
      causa.abogado = abg;
      causa.estado = est;

      const actor = currentUser ? currentUser.nombre : (currentRole === 'admin' ? 'Lizamar Briceño (Admin)' : 'Abogado PGET');
      addAuditLog("MODIFICACIÓN CAUSA", causa.expediente, tabTitle, `Expediente editado por ${{actor}}. Asignado a: ${{causa.abogado}}.`);
      
      closeModals();
      renderCausas();
      showToast(`Causa EXP. ${{causa.expediente}} actualizada exitosamente`, "success");
    }}

    // CAUSA DELETE MODAL LOGIC (IN-DOM)
    function openDeleteCausaModal(rowIndex) {{
      const tabTitle = currentSelectedTab.title;
      const list = causasPorPestana[tabTitle] || [];
      const causa = list.find(c => c.row_index === rowIndex);
      if (!causa) return;

      document.getElementById('delCausaRowIndex').value = rowIndex;
      document.getElementById('delCausaExp').innerText = causa.expediente;
      document.getElementById('delCausaMot').innerText = causa.motivo;
      document.getElementById('delCausaUser').innerText = currentUser ? currentUser.shortName : (currentRole === 'admin' ? 'Lizamar Briceño (Admin)' : 'Abogado PGET');

      openModal('modalDeleteCausa');
    }}

    function confirmDeleteCausaAction() {{
      const rowIndex = parseInt(document.getElementById('delCausaRowIndex').value);
      const tabTitle = currentSelectedTab.title;
      const list = causasPorPestana[tabTitle] || [];
      const idx = list.findIndex(c => c.row_index === rowIndex);
      if (idx === -1) return;
      const causa = list[idx];

      const actor = currentUser ? currentUser.nombre : (currentRole === 'admin' ? 'Lizamar Briceño (Admin)' : 'Abogado PGET');
      addAuditLog("ELIMINACIÓN CAUSA", causa.expediente, tabTitle, `Causa judicial eliminada del sistema por ${{actor}}.`);

      list.splice(idx, 1);
      closeModals();
      renderCausas();
      showToast(`Causa EXP. ${{causa.expediente}} eliminada y grabada en auditoría`, "success");
    }}

    // LAWYERS ADMIN RENDERING & LOGIC
    function renderLawyers() {{
      const container = document.getElementById('lawyersListContainer');
      const activos = lawyers.filter(l => l.activo);
      const inactivos = lawyers.filter(l => !l.activo);

      let html = `
        <div class="flex items-center justify-between bg-emerald-50 border border-emerald-300 rounded-xl px-3 py-1.5 text-xs text-emerald-900 font-bold mb-2">
          <span>⚖️ Nómina Activa Oficial (${{activos.length}})</span>
          <span class="text-[10px] bg-emerald-200 px-2 py-0.5 rounded-full">Disponibles en Nuevos Casos</span>
        </div>
      `;

      html += activos.map(l => `
        <div class="p-2.5 bg-white rounded-xl border border-[#D4AF37] shadow-sm hover:border-[#6B1226] transition-colors">
          <div class="flex items-start justify-between">
            <div class="flex items-center gap-2">
              <div class="w-8 h-8 rounded-full bg-[#6B1226] text-[#D4AF37] font-bold flex items-center justify-center text-xs shrink-0 border border-[#D4AF37]">
                ${{l.nombre[0]}}
              </div>
              <div>
                <h5 class="font-bold text-xs text-[#6B1226] flex items-center gap-1.5">
                  ${{l.nombre}}
                  ${{l.nombre.includes('LIZAMAR') ? '<span class="text-[9px] bg-amber-100 text-amber-900 px-1.5 py-0.2 rounded font-bold border border-amber-300">ADMIN</span>' : ''}}
                </h5>
                <p class="text-[10px] text-slate-500">C.I. ${{l.cedula}} • <strong class="text-slate-700">${{l.cargo}}</strong></p>
                <p class="text-[10px] text-slate-600 font-semibold">${{l.adscrito}}</p>
              </div>
            </div>

            <!-- Botones Exclusivos del Admin -->
            <div class="flex items-center gap-1">
              <button onclick="openEditLawyerModal('${{l.id}}')" title="Editar Abogado" class="w-6 h-6 rounded bg-amber-100 hover:bg-amber-200 text-amber-800 text-[11px] flex items-center justify-center border border-amber-300">
                ✏️
              </button>
              <button onclick="openDeactivateLawyerModal('${{l.id}}')" title="Desactivar (Mantiene su historial en expedientes)" class="w-6 h-6 rounded bg-rose-100 hover:bg-rose-200 text-rose-700 text-[11px] flex items-center justify-center border border-rose-300">
                🚫
              </button>
            </div>
          </div>
        </div>
      `).join('');

      if (inactivos.length > 0) {{
        html += `
          <div class="pt-3 pb-1 border-t mt-3 flex items-center justify-between text-xs font-bold text-slate-500">
            <span>Abogados Históricos (${{inactivos.length}})</span>
            <span class="text-[9.5px] font-normal text-slate-400">Preservados en causas previas</span>
          </div>
        `;
        html += inactivos.map(l => `
          <div class="p-2 bg-slate-50 rounded-xl border border-slate-200 opacity-60">
            <div class="flex items-center justify-between">
              <div>
                <div class="font-bold text-xs text-slate-600">${{l.nombre}}</div>
                <div class="text-[10px] text-slate-400">C.I. ${{l.cedula}} • ${{l.cargo}}</div>
              </div>
              <button onclick="openReactivateLawyerModal('${{l.id}}')" title="Reactivar Abogado" class="px-2 py-0.5 rounded bg-emerald-100 hover:bg-emerald-200 text-emerald-800 text-[10px] font-bold border border-emerald-300 flex items-center gap-1">
                ✅ Reactivar
              </button>
            </div>
          </div>
        `).join('');
      }}

      container.innerHTML = html;
    }}

    function openEditLawyerModal(id) {{
      if (currentRole !== 'admin') {{
        showToast("Acceso Restringido: Solo el Administrador puede modificar la nómina institucional.", "warning");
        return;
      }}
      const l = lawyers.find(item => item.id === id);
      if (!l) return;

      document.getElementById('editLawyerId').value = l.id;
      document.getElementById('editLawyerName').value = l.nombre;
      document.getElementById('editLawyerCI').value = l.cedula;
      document.getElementById('editLawyerCargo').value = l.cargo;
      document.getElementById('editLawyerAdscrito').value = l.adscrito;

      openModal('modalEditLawyer');
    }}

    function saveLawyerEditAction() {{
      const id = document.getElementById('editLawyerId').value;
      const l = lawyers.find(item => item.id === id);
      if (!l) return;

      const nom = document.getElementById('editLawyerName').value.trim();
      const ci = document.getElementById('editLawyerCI').value.trim();
      const cargo = document.getElementById('editLawyerCargo').value.trim();
      const adsc = document.getElementById('editLawyerAdscrito').value.trim();

      if (!nom) {{
        showToast("El nombre del abogado es obligatorio", "warning");
        return;
      }}

      l.nombre = nom.toUpperCase();
      l.cedula = ci;
      l.cargo = cargo;
      l.adscrito = adsc;

      addAuditLog("MODIFICACIÓN NÓMINA", "NÓMINA", "ADMINISTRACIÓN", `Se actualizaron datos de ${{l.nombre}} (C.I. ${{l.cedula}}).`);
      closeModals();
      renderLawyers();
      showToast(`Abogado ${{l.nombre}} actualizado con éxito`, "success");
    }}

    function openDeactivateLawyerModal(id) {{
      if (currentRole !== 'admin') {{
        showToast("Acceso Restringido: Solo el Administrador puede dar de baja en nómina.", "warning");
        return;
      }}
      const l = lawyers.find(item => item.id === id);
      if (!l) return;

      document.getElementById('deactLawyerId').value = l.id;
      document.getElementById('deactLawyerName').innerText = l.nombre;
      openModal('modalDeactivateLawyer');
    }}

    function confirmDeactivateLawyerAction() {{
      const id = document.getElementById('deactLawyerId').value;
      const l = lawyers.find(item => item.id === id);
      if (!l) return;

      l.activo = false;
      addAuditLog("DESACTIVACIÓN ABOGADO", "NÓMINA", "ADMINISTRACIÓN", `Se desactivó de nómina a ${{l.nombre}} (Se preserva su historial en expedientes al 100%).`);
      closeModals();
      renderLawyers();
      showToast(`Abogado ${{l.nombre}} desactivado. Historial protegido al 100%`, "success");
    }}

    function openReactivateLawyerModal(id) {{
      if (currentRole !== 'admin') return;
      const l = lawyers.find(item => item.id === id);
      if (!l) return;

      document.getElementById('reactLawyerId').value = l.id;
      document.getElementById('reactLawyerName').innerText = l.nombre;
      openModal('modalReactivateLawyer');
    }}

    function confirmReactivateLawyerAction() {{
      const id = document.getElementById('reactLawyerId').value;
      const l = lawyers.find(item => item.id === id);
      if (!l) return;

      l.activo = true;
      addAuditLog("REACTIVACIÓN ABOGADO", "NÓMINA", "ADMINISTRACIÓN", `Se reactivó a ${{l.nombre}} en nómina activa.`);
      closeModals();
      renderLawyers();
      showToast(`Abogado ${{l.nombre}} reactivado exitosamente`, "success");
    }}

    function openAddLawyerModal() {{
      if (currentRole !== 'admin') {{
        showToast("Acceso Restringido: Solo el Administrador puede agregar nuevos abogados.", "warning");
        return;
      }}
      document.getElementById('newLawyerName').value = '';
      document.getElementById('newLawyerCI').value = '';
      document.getElementById('newLawyerCargo').value = '';
      document.getElementById('newLawyerAdscrito').value = '';
      openModal('modalAddLawyer');
    }}

    function saveNewLawyerAction() {{
      const nom = document.getElementById('newLawyerName').value.trim();
      const ci = document.getElementById('newLawyerCI').value.trim();
      const cargo = document.getElementById('newLawyerCargo').value.trim() || 'Abogado Adscrito';
      const adsc = document.getElementById('newLawyerAdscrito').value.trim() || 'Procuraduría General del Estado Trujillo';

      if (!nom) {{
        showToast("Por favor ingresa el nombre del abogado", "warning");
        return;
      }}

      const nuevo = {{
        id: (lawyers.length + 1).toString(),
        nombre: nom.toUpperCase(),
        cedula: ci,
        cargo: cargo,
        adscrito: adsc,
        activo: true
      }};

      lawyers.push(nuevo);
      addAuditLog("ALTA ABOGADO", "NÓMINA", "ADMINISTRACIÓN", `Alta de ${{nuevo.nombre}} (C.I. ${{nuevo.cedula}}).`);
      closeModals();
      renderLawyers();
      showToast(`Abogado ${{nuevo.nombre}} registrado en nómina`, "success");
    }}

    function renderAuditLogs() {{
      const container = document.getElementById('auditListContainer');
      container.innerHTML = auditLogs.map(item => `
        <div class="bg-white p-2.5 rounded-xl border border-[#D4AF37] shadow-sm">
          <div class="flex items-center justify-between text-[10px] text-slate-400 mb-1">
            <span class="font-bold text-[#6B1226]">📅 ${{item.fecha}}</span>
            <span class="bg-slate-100 text-slate-600 px-1.5 py-0.2 rounded font-mono font-bold">${{item.usuario}}</span>
          </div>
          <div class="flex items-center gap-1.5 mb-1">
            <span class="text-[9.5px] font-black uppercase px-2 py-0.5 rounded ${{item.accion.includes('ELIMIN') ? 'bg-rose-100 text-rose-800 border border-rose-300' : item.accion.includes('MODIF') ? 'bg-amber-100 text-amber-800 border border-amber-300' : 'bg-emerald-100 text-emerald-800 border border-emerald-300'}}">
              ${{item.accion}}
            </span>
            <span class="text-[10px] font-extrabold text-[#6B1226] truncate">EXP: ${{item.expediente}}</span>
          </div>
          <p class="text-[11px] text-slate-700 leading-tight">${{item.detalle}}</p>
          <div class="mt-1 text-[9.5px] text-slate-400">Materia: <strong class="text-slate-600">${{item.pestana}}</strong></div>
        </div>
      `).join('');
    }}

    function addAuditLog(accion, expediente, pestana, detalle) {{
      const d = new Date();
      const fechaStr = d.toLocaleDateString('es-ES') + ', ' + d.toLocaleTimeString('es-ES', {{ hour: '2-digit', minute: '2-digit' }});
      const usuario = currentUser ? currentUser.shortName : (currentRole === 'admin' ? 'Lizamar Briceño (Admin)' : 'Abogado PGET');
      auditLogs.unshift({{
        id: (auditLogs.length + 1).toString(),
        fecha: fechaStr,
        usuario: usuario,
        accion: accion,
        expediente: expediente,
        pestana: pestana,
        detalle: detalle
      }});
      renderAuditLogs();
    }}

    // Switch de Vistas Móviles
    function switchView(viewName) {{
      if (!currentUser) {{
        document.getElementById('view-login').classList.remove('hidden');
        return;
      }}

      document.getElementById('view-list').classList.add('hidden');
      document.getElementById('view-lawyers-admin').classList.add('hidden');
      document.getElementById('view-audit-admin').classList.add('hidden');
      document.getElementById('view-form').classList.add('hidden');

      if (viewName === 'list') {{
        document.getElementById('view-list').classList.remove('hidden');
      }} else if (viewName === 'lawyers-admin') {{
        if (currentRole !== 'admin') {{
          showToast("Acceso Restringido: Los abogados no pueden gestionar la nómina institucional.", "warning");
          document.getElementById('view-list').classList.remove('hidden');
          return;
        }}
        document.getElementById('view-lawyers-admin').classList.remove('hidden');
      }} else if (viewName === 'audit-admin') {{
        if (currentRole !== 'admin') {{
          showToast("Acceso Restringido: El registro de auditoría es de uso exclusivo del Administrador.", "warning");
          document.getElementById('view-list').classList.remove('hidden');
          return;
        }}
        document.getElementById('view-audit-admin').classList.remove('hidden');
      }} else if (viewName === 'form') {{
        buildDynamicForm();
        document.getElementById('view-form').classList.remove('hidden');
      }}
    }}

    // Construcción Dinámica del Formulario según la Materia
    function buildDynamicForm() {{
      const container = document.getElementById('dynamicFormFields');
      document.getElementById('form-tab-title').innerText = formSelectedTab.title;

      let html = '';
      formSelectedTab.columns.forEach((col, idx) => {{
        const isAbog = col.toUpperCase().includes('ABOGAD');
        const isFecha = col.toUpperCase().includes('FECHA');
        const isEstado = col.toUpperCase().includes('ESTAD') || col.toUpperCase().includes('ESTATUS');

        if (isAbog) {{
          html += `
            <div>
              <label class="block font-bold text-slate-700 uppercase text-[10px] mb-0.5">${{col}} *</label>
              <select id="form-field-${{idx}}" class="w-full bg-slate-50 border border-[#D4AF37] rounded-lg p-2 font-semibold text-slate-800 focus:outline-none">
                ${{lawyers.filter(l => l.activo).map(l => {{
                  const isCur = currentUser && l.nombre === currentUser.nombre;
                  return `<option value="${{l.nombre}}" ${{isCur ? 'selected' : ''}}>${{l.nombre}} (${{l.cargo}})</option>`;
                }}).join('')}}
              </select>
            </div>
          `;
        }} else if (isEstado) {{
          html += `
            <div>
              <label class="block font-bold text-slate-700 uppercase text-[10px] mb-0.5">${{col}} *</label>
              <select id="form-field-${{idx}}" class="w-full bg-slate-50 border border-slate-300 rounded-lg p-2 text-slate-800 focus:outline-none focus:border-[#D4AF37]">
                <option value="ACTIVA">ACTIVA / EN TRÁMITE</option>
                <option value="EN SUSTANCIACIÓN">EN SUSTANCIACIÓN</option>
                <option value="SENTENCIADA">SENTENCIADA</option>
                <option value="CERRADA">CERRADA / ARCHIVADA</option>
              </select>
            </div>
          `;
        }} else if (isFecha) {{
          html += `
            <div>
              <label class="block font-bold text-slate-700 uppercase text-[10px] mb-0.5">${{col}}</label>
              <input type="date" id="form-field-${{idx}}" value="2026-10-29" class="w-full bg-slate-50 border border-slate-300 rounded-lg p-1.5 text-slate-800 focus:outline-none focus:border-[#D4AF37]">
            </div>
          `;
        }} else {{
          html += `
            <div>
              <label class="block font-bold text-slate-700 uppercase text-[10px] mb-0.5">${{col}}</label>
              <input type="text" id="form-field-${{idx}}" placeholder="Ingresar ${{col.toLowerCase()}}..." class="w-full bg-slate-50 border border-slate-300 rounded-lg p-1.5 text-slate-800 focus:outline-none focus:border-[#D4AF37]">
            </div>
          `;
        }}
      }});

      container.innerHTML = html;
    }}

    function openTabSelectorModal() {{
      document.getElementById('modalTabsSelector').classList.remove('hidden');
    }}

    function closeTabSelectorModal() {{
      document.getElementById('modalTabsSelector').classList.add('hidden');
    }}

    function selectTabForForm(tabTitle) {{
      formSelectedTab = tabsData.find(t => t.title === tabTitle) || tabsData[0];
      closeTabSelectorModal();
      buildDynamicForm();
    }}

    function submitNewCausa() {{
      let expediente = "EXP-2026-" + Math.floor(1000 + Math.random() * 9000);
      let motivo = "Causa Judicial PGET";
      let demandado = "";
      let abogado = currentUser ? currentUser.nombre : lawyers.find(l => l.activo).nombre;

      formSelectedTab.columns.forEach((col, idx) => {{
        const el = document.getElementById(`form-field-${{idx}}`);
        if (el && el.value) {{
          const val = el.value.trim();
          if (col.toUpperCase().includes('EXP')) expediente = val;
          if (col.toUpperCase().includes('MOTIVO') || col.toUpperCase().includes('ASUNTO') || col.toUpperCase().includes('OBJETO')) motivo = val;
          if (col.toUpperCase().includes('DEMANDADO') || col.toUpperCase().includes('ACCIONADO')) demandado = val;
          if (col.toUpperCase().includes('ABOGAD')) abogado = val;
        }}
      }});

      const nuevaCausa = {{
        row_index: 9999 + Math.floor(Math.random() * 1000),
        expediente: expediente,
        motivo: motivo,
        demandado: demandado,
        abogado: abogado,
        estado: "ACTIVA",
        year: "2026",
        fecha: "29/10/2026"
      }};

      if (!causasPorPestana[formSelectedTab.title]) {{
        causasPorPestana[formSelectedTab.title] = [];
      }}
      causasPorPestana[formSelectedTab.title].unshift(nuevaCausa);

      currentSelectedTab = formSelectedTab;
      document.getElementById('sheetTabSelect').value = currentSelectedTab.title;

      const actor = currentUser ? currentUser.nombre : (currentRole === 'admin' ? 'Lizamar Briceño (Admin)' : 'Abogado PGET');
      addAuditLog("CREACIÓN CAUSA", expediente, formSelectedTab.title, `Nueva causa registrada en materia "${{formSelectedTab.title}}" por ${{actor}}. Asignada a: ${{abogado}}.`);

      switchView('list');
      renderCausas();
      showToast(`¡Causa ${{expediente}} guardada con éxito en Google Sheets!`, "success");
    }}

    // Iniciar al cargar
    window.onload = init;
  </script>
</body>
</html>
"""

# Escribir en prototype.html en la raíz y en el directorio de artefactos
with open('prototype.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

artifact_path = 'C:/Users/PC/.gemini/antigravity/brain/098ba3de-2780-4abe-8d88-54767a85600a/prototype.html'
with open(artifact_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Successfully generated prototype.html with Palacio de Gobierno background + Gavel Strike Loader (1.5s)!")
