import json
import base64

with open('compact_causes_by_tab.json', 'r', encoding='utf-8') as f:
    compact_data = json.load(f)

causes_by_tab_json = json.dumps(compact_data['causes_by_tab'], ensure_ascii=False)
years_json = json.dumps(compact_data['years'], ensure_ascii=False)

with open('assets/logo_pget.png', 'rb') as f:
    logo_b64 = base64.b64encode(f.read()).decode('utf-8')

html_content = f"""<!DOCTYPE html>
<html lang="es" class="h-full">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>PGET Trujillo • Sistema Multimateria de Causas Jurídicas</title>
  
  <!-- Tailwind CSS Oficial Permitido por CSP -->
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>

  <style>
    /* Estilos base con tokens institucionales PGET */
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
  </style>
</head>
<body class="bg-slate-100 text-slate-800 antialiased p-2 md:p-5 flex flex-col items-center min-h-screen">

  <!-- Header Banner Principal Superior -->
  <div class="max-w-4xl w-full mb-3 flex flex-col md:flex-row items-start md:items-center justify-between gap-3 bg-white border-2 border-[#D4AF37] rounded-2xl p-3.5 shadow-md">
    <div class="flex items-center gap-3 cursor-pointer" onclick="switchView('list')">
      <!-- Logo PGET en Base64 sobre disco vinotinto oscuro con aro dorado (Cero fallos de carga o CSP) -->
      <div class="w-13 h-13 rounded-full bg-[#480C19] border-2 border-[#D4AF37] p-1 overflow-hidden shrink-0 shadow flex items-center justify-center hover:scale-105 transition-transform" style="width: 52px; height: 52px;">
        <img src="data:image/png;base64,{logo_b64}" alt="PGET Logo" class="w-full h-full object-contain">
      </div>
      <div>
        <div class="text-[11px] font-black tracking-widest text-[#D4AF37] uppercase">Procuraduría General del Estado Trujillo</div>
        <h1 class="text-base font-extrabold text-slate-900 leading-tight">
          Sistema de Causas Jurídicas • 17 Materias
        </h1>
        <p class="text-xs text-slate-500">Datos reales de Google Sheets • Filtro por Año • Edición y Eliminación Activa</p>
      </div>
    </div>
    
    <div class="flex items-center gap-2 bg-emerald-50 border border-emerald-300 px-3 py-1 rounded-lg text-emerald-800 text-xs font-bold">
      <span class="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse"></span>
      17 Materias Conectadas
    </div>
  </div>

  <!-- Contenedor: Smartphone Simulator y Panel Explicativo -->
  <div class="max-w-4xl w-full grid grid-cols-1 lg:grid-cols-12 gap-5 items-start">
    
    <!-- FRAME SMARTPHONE (Cols 7) -->
    <div class="lg:col-span-7 flex justify-center">
      <div class="w-[365px] h-[730px] bg-slate-900 rounded-[44px] p-3 shadow-2xl border-4 border-slate-700 relative flex flex-col">
        
        <!-- Notch -->
        <div class="w-full flex justify-center items-center py-1 absolute top-3 left-0 z-50">
          <div class="w-24 h-4 bg-black rounded-full flex items-center justify-center">
            <div class="w-2 h-2 rounded-full bg-slate-900 mr-2"></div>
            <div class="w-1 h-1 rounded-full bg-amber-600"></div>
          </div>
        </div>

        <!-- Pantalla Móvil -->
        <div class="w-full h-full bg-[#FCFCFD] text-slate-800 rounded-[34px] overflow-hidden flex flex-col relative pt-7">
          
          <!-- Header Vinotinto PGET -->
          <div class="bg-[#6B1226] text-white px-3.5 py-2.5 border-b-2 border-[#D4AF37] shadow">
            
            <!-- Fila 1: Logo + Título (Home) + Switch Admin/Abogado -->
            <div class="flex items-center justify-between">
              
              <!-- Clic en Logo o Título -> Va a Home -->
              <div class="flex items-center gap-2.5 cursor-pointer" onclick="switchView('list')" title="Toca para regresar a Home">
                <div class="rounded-full bg-[#480C19] border-2 border-[#D4AF37] p-0.5 overflow-hidden shrink-0 shadow flex items-center justify-center" style="width: 44px; height: 44px;">
                  <img src="data:image/png;base64,{logo_b64}" alt="Escudo PGET" class="w-full h-full object-contain">
                </div>
                <div>
                  <div class="text-[10px] font-black text-[#D4AF37] tracking-wider uppercase">PGET • ESTADO TRUJILLO</div>
                  <div class="text-xs font-extrabold text-white">Gestor de Causas</div>
                </div>
              </div>

              <!-- Switch de Rol -->
              <div class="bg-[#480C19] px-1.5 py-0.5 rounded-full border border-[#D4AF37]/50 flex text-[10.5px]">
                <button id="btn-admin" onclick="setRole('admin')" class="px-2.5 py-0.5 rounded-full font-bold bg-white text-[#6B1226]">Admin</button>
                <button id="btn-lawyer" onclick="setRole('lawyer')" class="px-2.5 py-0.5 rounded-full font-bold text-white/80">Abogado</button>
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
              <span class="text-white/90">⚖️ <strong>Modo Abogado:</strong> Consulta libre, creación, edición y eliminación de causas.</span>
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
          <div id="view-list" class="flex-1 overflow-y-auto p-3 space-y-2.5">
            
            <!-- Métricas -->
            <div class="grid grid-cols-3 gap-1.5">
              <div class="bg-white p-2 rounded-xl border border-[#D4AF37] shadow-sm flex flex-col items-center">
                <span class="text-[9.5px] text-slate-400 font-bold uppercase">Causas</span>
                <span id="stat-total" class="text-sm font-black text-[#6B1226]">0</span>
              </div>
              <div class="bg-white p-2 rounded-xl border border-[#D4AF37] shadow-sm flex flex-col items-center">
                <span class="text-[9.5px] text-emerald-600 font-bold uppercase">Activas</span>
                <span id="stat-active" class="text-sm font-black text-emerald-600">0</span>
              </div>
              <div class="bg-white p-2 rounded-xl border border-[#D4AF37] shadow-sm flex flex-col items-center">
                <span class="text-[9.5px] text-slate-500 font-bold uppercase">Cerradas</span>
                <span id="stat-closed" class="text-sm font-black text-slate-600">0</span>
              </div>
            </div>

            <!-- Buscador en tiempo real -->
            <div class="relative">
              <span class="absolute left-3 top-2 text-[#6B1226]">🔍</span>
              <input id="searchInput" oninput="renderCausas()" type="text" placeholder="Buscar por expediente, abogado, parte o motivo..." class="w-full bg-white border border-[#D4AF37] rounded-xl pl-8 pr-3 py-1.5 text-xs focus:outline-none focus:ring-2 focus:ring-[#D4AF37]">
            </div>

            <!-- Filtros de Estado -->
            <div class="flex gap-1 overflow-x-auto text-[10.5px] pb-0.5">
              <button onclick="setEstadoFilter('ALL', this)" class="chip-estado bg-[#6B1226] text-white px-2.5 py-0.5 rounded-full font-bold shrink-0 border border-[#D4AF37]">TODAS</button>
              <button onclick="setEstadoFilter('ACT', this)" class="chip-estado bg-white text-slate-700 px-2.5 py-0.5 rounded-full font-semibold shrink-0 border border-[#C5A059]">ACTIVAS</button>
              <button onclick="setEstadoFilter('CERR', this)" class="chip-estado bg-white text-slate-700 px-2.5 py-0.5 rounded-full font-semibold shrink-0 border border-[#C5A059]">CERRADAS</button>
            </div>

            <!-- Lista de Tarjetas de Causas -->
            <div id="causasContainer" class="space-y-2 pb-16">
            </div>
          </div>

          <!-- VISTA 2: NÓMINA DE ABOGADOS (SOLO ADMIN: EDITAR Y DESACTIVAR CON PRESERVACIÓN HISTÓRICA) -->
          <div id="view-lawyers-admin" class="flex-1 overflow-y-auto p-3 space-y-2.5 hidden">
            <div class="flex items-center justify-between border-b border-[#D4AF37]/40 pb-2">
              <div class="flex items-center gap-2">
                <button onclick="switchView('list')" class="w-7 h-7 rounded-full bg-[#6B1226] text-[#D4AF37] flex items-center justify-center text-xs font-bold">
                  ←
                </button>
                <div>
                  <h4 class="font-black text-sm text-[#6B1226]">Nómina de Abogados PGET</h4>
                  <p class="text-[10px] text-slate-500">Gestión Exclusiva de Administrador</p>
                </div>
              </div>
              <button onclick="openAddLawyerPrompt()" class="bg-[#6B1226] text-white text-[11px] font-bold px-2.5 py-1 rounded-lg border border-[#D4AF37] flex items-center gap-1 shadow-sm hover:scale-105">
                + Añadir
              </button>
            </div>

            <!-- Aviso Institucional de Soft-Delete -->
            <div class="p-2 bg-amber-50 border border-amber-300 rounded-xl text-[10.5px] text-amber-900 flex items-start gap-1.5">
              <span>🛡️</span>
              <span><strong>Garantía Histórica:</strong> Al dar de baja a un abogado, su nombre y actuaciones en expedientes judiciales de Google Sheets permanecen 100% intactos.</span>
            </div>

            <!-- Lista de Abogados -->
            <div id="lawyersListContainer" class="space-y-2 pt-1 pb-16">
            </div>
          </div>

          <!-- VISTA 3: AUDITORÍA ADMIN -->
          <div id="view-audit-admin" class="flex-1 overflow-y-auto p-3 space-y-2.5 hidden">
            <div class="flex items-center gap-2 border-b border-[#D4AF37]/40 pb-2">
              <button onclick="switchView('list')" class="w-7 h-7 rounded-full bg-[#6B1226] text-[#D4AF37] flex items-center justify-center text-xs font-bold">
                ←
              </button>
              <div>
                <h4 class="font-black text-sm text-[#6B1226]">Registro de Auditoría PGET</h4>
                <p class="text-[10px] text-slate-500">Trazabilidad en Tiempo Real (Quién, Cuándo y Qué)</p>
              </div>
            </div>

            <div id="auditListContainer" class="space-y-2 pb-16">
            </div>
          </div>

          <!-- VISTA 4: FORMULARIO DINÁMICO DE CAUSA -->
          <div id="view-form" class="flex-1 overflow-y-auto p-3 space-y-3 hidden">
            <div class="flex items-center gap-2 border-b border-[#D4AF37]/40 pb-2">
              <button onclick="switchView('list')" class="w-7 h-7 rounded-full bg-[#6B1226] text-[#D4AF37] flex items-center justify-center text-xs font-bold">
                ←
              </button>
              <div>
                <h4 id="formHeaderTitle" class="font-black text-sm text-[#6B1226]">Nueva Causa Judicial</h4>
                <p id="formHeaderSubtitle" class="text-[10px] text-slate-500">Formulario adaptado dinámicamente</p>
              </div>
            </div>

            <!-- Form Container -->
            <form id="dynamicCausaForm" onsubmit="saveDynamicCausa(event)" class="space-y-2.5 pb-16">
              <div id="formInputsContainer" class="space-y-2"></div>
              
              <button type="submit" id="btnSaveCausa" class="w-full py-2.5 bg-[#6B1226] text-white rounded-xl font-black text-xs border-2 border-[#D4AF37] shadow-md flex items-center justify-center gap-2 hover:bg-[#480C19] transition-all">
                <span>☁️ Guardar en Google Sheets</span>
              </button>
            </form>
          </div>

          <!-- BOTÓN FLOTANTE INFERIOR: CREAR CAUSA PGET -->
          <div class="absolute bottom-3 left-0 w-full px-4 pointer-events-none z-30">
            <button onclick="openSelectTabModal()" class="w-full py-2.5 rounded-full bg-[#6B1226] text-white font-extrabold text-xs shadow-xl border-2 border-[#D4AF37] flex items-center justify-center gap-2 pointer-events-auto hover:scale-102 transition-transform">
              <span class="text-[#D4AF37] text-sm">➕</span>
              <span>Crear Causa PGET (Elegir Materia)</span>
            </button>
          </div>

          <!-- MODAL: PASO 1 - ELEGIR ENTRE LAS 17 MATERIAS -->
          <div id="modalSelectTab" class="absolute inset-0 bg-black/60 z-50 backdrop-blur-sm hidden flex flex-col justify-end">
            <div class="bg-white rounded-t-3xl max-h-[85%] flex flex-col border-t-4 border-[#D4AF37] shadow-2xl">
              <div class="p-3.5 bg-[#6B1226] text-white rounded-t-2xl flex items-center justify-between border-b border-[#D4AF37]">
                <div class="flex items-center gap-2">
                  <span class="text-[#D4AF37]">📂</span>
                  <div>
                    <h4 class="font-extrabold text-xs">Selecciona la Materia Judicial</h4>
                    <p class="text-[9px] text-[#D4AF37]">Pestañas oficiales de Google Sheets (PGET)</p>
                  </div>
                </div>
                <button onclick="closeSelectTabModal()" class="text-white hover:text-[#D4AF37] font-bold text-sm">
                  ✕
                </button>
              </div>

              <div id="modalTabsList" class="p-3 overflow-y-auto space-y-1.5 flex-1 text-xs">
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>

    <!-- PANEL DERECHO DE EXPLICACIÓN (Cols 5) -->
    <div class="lg:col-span-5 space-y-4">
      
      <!-- Card: Control de Roles y Permisos -->
      <div class="bg-white border-2 border-[#D4AF37] rounded-2xl p-4 shadow-sm">
        <h3 class="font-black text-sm text-[#6B1226] flex items-center gap-2 mb-2">
          <span>🔒</span> Permisos por Rol
        </h3>
        <ul class="text-xs space-y-2 text-slate-700">
          <li class="flex items-start gap-2">
            <span class="text-emerald-600 font-bold">✓</span>
            <span><strong>Abogados:</strong> Pueden consultar libremente todas las causas, crear nuevos expedientes, <strong>editar causas creadas</strong> y <strong>eliminar causas</strong>. Los abogados tienen bloqueada la gestión de nómina.</span>
          </li>
          <li class="flex items-start gap-2">
            <span class="text-[#6B1226] font-bold">✓</span>
            <span><strong>Administrador PGET:</strong> Control total de la nómina (altas, edición, bajas con histórico protegido) y auditoría.</span>
          </li>
          <li class="flex items-start gap-2">
            <span class="text-amber-600 font-bold">✓</span>
            <span><strong>Consulta Libre:</strong> No se requiere seleccionar ningún abogado para ver expedientes.</span>
          </li>
        </ul>
      </div>

      <!-- Card: Auditoría Activa -->
      <div class="bg-white border-2 border-[#D4AF37] rounded-2xl p-4 shadow-sm">
        <h3 class="font-black text-sm text-[#6B1226] flex items-center gap-2 mb-2">
          <span>⏱️</span> Trazabilidad y Auditoría
        </h3>
        <p class="text-xs text-slate-600 mb-2.5">
          Toda creación, edición o eliminación de causas ejecutada por un abogado o administrador queda registrada con fecha, hora exacta y causa afectada.
        </p>
        <button onclick="setRole('admin'); switchView('audit-admin')" class="w-full py-1.5 bg-[#6B1226]/10 hover:bg-[#6B1226]/20 text-[#6B1226] font-bold rounded-lg text-xs border border-[#D4AF37]">
          Ver Registro de Auditoría
        </button>
      </div>

      <!-- Card: Abogados Destacados -->
      <div class="bg-white border-2 border-[#D4AF37] rounded-2xl p-4 shadow-sm">
        <h3 class="font-black text-sm text-[#6B1226] flex items-center gap-2 mb-2">
          <span>⚖️</span> Abogados Identificados en Google Sheets
        </h3>
        <p class="text-xs text-slate-600">
          Registradas e indexadas: <strong>María de los Ángeles Ojeda</strong> (en el documento escrita como <em>María de los Ángeles</em> y <em>María Ojeda</em>) y <strong>Roxanna Mercado</strong> (escrita como <em>Roxanna Mercado</em> y <em>Roxana Mercado</em>).
        </p>
      </div>

    </div>

  </div>

  <script>
    // Catálogo de las 17 Pestañas
    const tabsData = [
      {{ title: "JUZGADOS DE MUNICIPIOS ORDINARI", category: "Juzgados Municipales", icon: "🏛️", columns: ["Nº", "Juzgado de Municipio", "Nº de Juzgado", "Demandante", "Demandado", "Motivo", "Nº de Expediente", "Abg. Responsable", "Cédula", "Cargo", "Adscrito a la Direcc.", "Fecha de Entrada", "Estado Actual", "Actuaciones Realizadas", "Monto Pagado", "Corte", "Nº de la Corte", "Observaciones"] }},
      {{ title: "CORTE CONTENCIOSO ADMIN.", category: "Contencioso Administrativo", icon: "⚖️", columns: ["Nº", "Juzgado de Municipio", "Nº de Juzgado", "Demandante", "Demandado", "Motivo", "Nº de Expediente", "Abg. Responsable", "Cédula", "Cargo", "Adscrito a la Direcc.", "Fecha de Entrada", "Estado Actual", "Actuaciones Realizadas", "Monto Pagado", "Corte", "Nº de la Corte", "Observaciones"] }},
      {{ title: "CONTENCIOSO TRUJILLO", category: "Contencioso Administrativo", icon: "🏢", columns: ["Nº", "Tribunal", "Querellante", "Querellado", "Motivo", "Nº de Expediente", "Abg. Responsable", "Cédula", "Cargo", "Adscripción", "Fecha de Entrada", "Estado", "Actuaciones Realizadas", "Monto Pagado", "Juzgado Superior Barquisimeto", "Corte", "Juzgado Nacional Maracaibo", "Actuaciones Realizadas 2", "Observaciones"] }},
      {{ title: "CONTENCIOSO", category: "Contencioso Administrativo", icon: "🏢", columns: ["Nº", "Tribunal", "Demandante", "Demandado", "Motivo", "Nº de Expediente", "Abg. Responsable", "Cédula", "Cargo", "Adscrito a la Direcc.", "Fecha de Entrada", "Estado Actual", "Actuaciones Realizadas", "Monto Pagado", "Corte", "Nº de la Corte", "Observaciones"] }},
      {{ title: "LABORAL", category: "Laboral Ordinario", icon: "💼", columns: ["Nº", "Tribunal", "Demandante", "Demandado", "Motivo", "Nº de Expediente", "Abg. Responsable", "Cédula", "Cargo", "Adscrito a la Direcc.", "Fecha de Entrada", "Estado Actual", "Actuaciones Realizadas", "Monto Pagado", "Corte", "Nº de la Corte", "Observaciones"] }},
      {{ title: "INSPECTORÍA-TRUJILO", category: "Laboral e Inspectorías", icon: "📜", columns: ["Nº", "Tribunal", "Demandante", "Demandado", "Motivo", "Nº de Expediente", "Abg. Responsable", "Cédula", "Cargo", "Adscrito a la Direcc.", "Fecha de Entrada", "Estado Actual", "Actuaciones Realizadas", "Procedimiento de Multa", "Solicitud Reenganche", "Reclamo Prestaciones", "Monto Pagado", "Nº Providencia", "Observaciones"] }},
      {{ title: "INSPECTORÍA-VALERA", category: "Laboral e Inspectorías", icon: "📜", columns: ["Nº", "Tribunal", "Demandante", "Demandado", "Motivo", "Nº de Expediente", "Abg. Responsable", "Cédula", "Cargo", "Adscrito a la Direcc.", "Fecha de Entrada", "Estado Actual", "Actuaciones Realizadas", "Procedimiento de Multa", "Solicitud Reenganche", "Reclamo Prestaciones", "Monto Pagado", "Nº Providencia", "Observaciones"] }},
      {{ title: "SUB-INSPECTORÍA-BOCONÓ", category: "Laboral e Inspectorías", icon: "📜", columns: ["Nº", "Tribunal", "Demandante", "Demandado", "Motivo", "Nº de Expediente", "Abg. Responsable", "Cédula", "Direcc. Adscrita", "Cargo", "Fecha de Entrada", "Estado Actual", "Actuaciones Realizadas", "Procedimiento Multa", "Solicitud Reenganche", "Reclamos Prestaciones", "Monto Pagado", "Fecha Culminación", "Observaciones"] }},
      {{ title: "CALIFICACIONES NO PROCESADAS", category: "Laboral e Inspectorías", icon: "📑", columns: ["Tribunal", "Demandante", "Demandado", "Motivo", "Nº de Expediente", "Abg. Responsable", "Cédula de Identidad", "Cargo", "Adscrito a la Direcc.", "Fecha de Entrada", "Estado Actual", "Actuaciones Realizadas", "Bs. Cancelados", "Nº Providencia", "Observaciones"] }},
      {{ title: "CIRCUITO PENAL", category: "Circuito Penal", icon: "🔒", columns: ["Nº", "Tribunal", "Imputado(s)", "Víctima", "Delito", "Nº de Expediente", "Abg. Responsable", "Fecha de Entrada", "Estado Actual", "Nº de Investigación Fiscalía", "Observaciones"] }},
      {{ title: "FISCALÍAS ORD.-ESP", category: "Fiscalías", icon: "🛡️", columns: ["Nº", "Tribunal / Fiscalía", "Imputado", "Víctima", "Delito", "Nº de Expediente", "Abg. Responsable", "Fecha de Entrada", "Estado Actual", "Actuaciones Realizadas", "Observaciones"] }},
      {{ title: "SOLICITUDES - VEHÍCULOS Y OTROS", category: "Fiscalías y Vehículos", icon: "🚗", columns: ["Nº", "Fiscalía", "Nº de Investigación", "Motivo", "Fecha de Solicitud", "Nº de Oficio", "Estado Actual", "Abg. Responsable", "Observaciones"] }},
      {{ title: "CIVIL", category: "Materia Civil", icon: "🏛️", columns: ["Tribunal", "Demandante", "Demandado", "Motivo", "Nº de Expediente", "Abg. Responsable", "Fecha de Entrada", "Estado Actual", "Actuaciones Realizadas", "Monto Pagado", "Observaciones"] }},
      {{ title: "AGRARIO", category: "Materia Agraria y Tierras", icon: "🌾", columns: ["Nº", "Tribunal", "Demandante", "Demandado", "Motivo", "Nº de Expediente", "Abg. Responsable", "Cédula de Identidad", "Cargo", "Adscrito a la Direcc.", "Fecha de Entrada", "Estado Actual", "Actuaciones Realizadas", "Monto Pagado", "Observaciones"] }},
      {{ title: "PROTECCION DE NIÑOS, NIÑAS Y AD", category: "Protección LOPNNA", icon: "👨‍👩‍👧", columns: ["Nº", "Tribunal", "Demandante", "Demandado", "Motivo", "Nº de Expediente", "Abg. Responsable", "Cédula", "Cargo", "Adscrito a la Direcc.", "Fecha de Entrada", "Estado Actual", "Actuaciones Realizadas", "Monto Pagado", "Corte", "Nº de la Corte", "Observaciones"] }},
      {{ title: "CONSEJOS DE PROTECCION DE NIÑ@S", category: "Protección LOPNNA", icon: "🧒", columns: ["Nº", "Consejo de Protección", "Solicitante", "Solicitado", "Motivo", "Nº Expediente Administrativo", "Abg. Responsable", "Cédula", "Cargo", "Adscrito a la Direcc.", "Fecha de Entrada", "Estado Actual", "Actuaciones Realizadas", "Monto Pagado", "Corte", "Nº de la Corte", "Observaciones"] }},
      {{ title: "TRIBUNAL SUPREMO-JUZGADOS", category: "Tribunal Supremo (TSJ)", icon: "⚖️", columns: ["Nº", "Sala", "Demandante", "Demandado", "Motivo", "Nº de Expediente", "Abg. Responsable", "Cédula", "Cargo", "Adscrito a la Direcc.", "Estado Actual", "Actuaciones Realizadas", "Monto Pagado", "Observaciones"] }}
    ];

    // Nómina Oficial Completa
    let lawyers = [
      {{ id: "1", nombre: "SAMANTHA POLANCO", cedula: "5.493.478", cargo: "Apoderada Judicial PGET", adscrito: "CORPOTURISMO / PGET", activo: true }},
      {{ id: "2", nombre: "DIANA FARIA", cedula: "16.724.586", cargo: "Abogada Adscrita", adscrito: "ASUNTOS JURÍDICOS", activo: true }},
      {{ id: "3", nombre: "GIUSEPPE ANGRISANO", cedula: "4.659.953", cargo: "Abogado Litigante", adscrito: "PROCURADURÍA GENERAL", activo: true }},
      {{ id: "4", nombre: "VIRGINIA ROJAS", cedula: "14.929.335", cargo: "Consultora Jurídica", adscrito: "DINFRA / PGET", activo: true }},
      {{ id: "5", nombre: "LIZAMAR BRICEÑO", cedula: "9.170.221", cargo: "Abogada Adjunta", adscrito: "ASUNTOS JURÍDICOS", activo: true }},
      {{ id: "6", nombre: "SILVANA GODOY", cedula: "18.441.902", cargo: "Abogada Adscrita", adscrito: "CONTENCIOSO ADMINISTRATIVO", activo: true }},
      {{ id: "7", nombre: "ANA JULIA PADILLA", cedula: "12.890.345", cargo: "Apoderada Especial", adscrito: "PROCURADURÍA GENERAL", activo: true }},
      {{ id: "8", nombre: "ANA BEATRIZ MATERÁN", cedula: "10.450.812", cargo: "Abogada Especialista", adscrito: "DIRECCIÓN DE EDUCACIÓN", activo: true }},
      {{ id: "9", nombre: "ANALÍ UZCÁTEGUI", cedula: "15.678.901", cargo: "Consultora Laboral", adscrito: "INSPECTORÍA TRUJILLO", activo: true }},
      {{ id: "10", nombre: "LUZ MARINA CABRERA", cedula: "8.991.234", cargo: "Abogada Litigante", adscrito: "CIRCUITO PENAL", activo: true }},
      {{ id: "11", nombre: "LISBETH GIL", cedula: "17.234.567", cargo: "Abogada de Sustanciación", adscrito: "CONTENCIOSO TRUJILLO", activo: true }},
      {{ id: "12", nombre: "JOAN TESTA", cedula: "13.456.789", cargo: "Apoderado Judicial", adscrito: "FISCALÍAS ESPECIALES", activo: true }},
      {{ id: "13", nombre: "LUIS GODOY", cedula: "7.890.123", cargo: "Consultor Agrario", adscrito: "MATERIA AGRARIA Y TIERRAS", activo: true }},
      {{ id: "14", nombre: "SARA BASTIDAS", cedula: "3.905.748", cargo: "Representante TSJ", adscrito: "TRIBUNAL SUPREMO", activo: true }},
      {{ id: "15", nombre: "YONEXI MORENO", cedula: "19.876.543", cargo: "Abogada Asistente", adscrito: "PROTECCIÓN LOPNNA", activo: true }},
      {{ id: "16", nombre: "MARIANGELA GÓMEZ", cedula: "16.554.321", cargo: "Abogada Adjunta", adscrito: "SUB-INSPECTORÍA BOCONÓ", activo: true }},
      {{ id: "17", nombre: "KLEIVER BRICEÑO", cedula: "20.123.456", cargo: "Abogado Litigante", adscrito: "CONTENCIOSO ADMINISTRATIVO", activo: true }},
      {{ id: "18", nombre: "ILIANA SAAVEDRA", cedula: "11.234.567", cargo: "Apoderada Judicial", adscrito: "PROCURADURÍA GENERAL", activo: true }},
      {{ id: "19", nombre: "FRANCISCO MAZZ", cedula: "6.789.012", cargo: "Consultor Civil", adscrito: "TRIBUNALES CIVILES", activo: true }},
      {{ id: "20", nombre: "HÉCTOR PEÑA", cedula: "8.123.456", cargo: "Abogado Litigante", adscrito: "CIRCUITO PENAL", activo: true }},
      {{ id: "21", nombre: "VICTOR VALECILLOS", cedula: "14.567.890", cargo: "Abogado Adscrito", adscrito: "JUZGADOS MUNICIPALES", activo: true }},
      {{ id: "22", nombre: "LILIBETH SÁNCHEZ", cedula: "17.890.123", cargo: "Abogada Adscrita", adscrito: "MATERIA LABORAL / PGET", activo: true }},
      {{ id: "23", nombre: "LUIS DANIEL VALERO", cedula: "15.345.678", cargo: "Abogado Litigante", adscrito: "CONTENCIOSO ADMINISTRATIVO", activo: true }},
      {{ id: "24", nombre: "PAOLA VALE", cedula: "18.234.567", cargo: "Abogada Asistente", adscrito: "PROCURADURÍA GENERAL", activo: true }},
      {{ id: "25", nombre: "MARÍA DE LOS ÁNGELES OJEDA", cedula: "16.123.456", cargo: "Abogada Adscrita", adscrito: "ASUNTOS JURÍDICOS / CONTENCIOSO", activo: true }},
      {{ id: "26", nombre: "ROXANNA MERCADO", cedula: "17.654.321", cargo: "Abogada Litigante", adscrito: "CONTENCIOSO / LABORAL / INSPECTORÍA", activo: true }},
      {{ id: "27", nombre: "ANDREINA SEGOVIA", cedula: "19.345.678", cargo: "Abogada Asistente", adscrito: "CONTENCIOSO TRUJILLO", activo: true }},
      {{ id: "28", nombre: "ARMANDO BRICEÑO", cedula: "12.345.678", cargo: "Abogado Litigante", adscrito: "CONTENCIOSO ADMINISTRATIVO", activo: true }},
      {{ id: "29", nombre: "VERÓNICA MARKAN", cedula: "14.234.567", cargo: "Abogada de Sustanciación", adscrito: "JUZGADOS Y TRIBUNALES", activo: true }}
    ];

    // Registro de Auditoría
    let auditLogs = [
      {{ id: "1", fecha: "29/10/2026, 11:35 AM", usuario: "Roxanna Mercado", accion: "MODIFICACIÓN CAUSA", expediente: "TP11-G-2022-000006", pestana: "CONTENCIOSO TRUJILLO", detalle: "Actualización de auto y estado de sustanciación." }},
      {{ id: "2", fecha: "29/10/2026, 11:05 AM", usuario: "María de los Ángeles Ojeda", accion: "NUEVA ACTUACIÓN", expediente: "TP11-G-2021-000009", pestana: "CONTENCIOSO TRUJILLO", detalle: "Se consignó escrito de contestación ante el tribunal." }},
      {{ id: "3", fecha: "29/10/2026, 10:45 AM", usuario: "Admin PGET", accion: "MODIFICACIÓN NÓMINA", expediente: "NÓMINA", pestana: "ADMINISTRACIÓN", detalle: "Se incorporó a Roxanna Mercado y María de los Ángeles a la nómina oficial." }}
    ];

    const causasPorPestana = {causes_by_tab_json};
    const availableYears = {years_json};

    let currentSelectedTab = tabsData[2]; // Default a CONTENCIOSO TRUJILLO
    let formSelectedTab = tabsData[2];
    let currentRole = 'admin'; // 'admin' | 'lawyer'
    let currentEstadoFilter = 'ALL';

    function init() {{
      populateTabsDropdown();
      populateYearsDropdown();
      populateModalTabs();
      renderLawyers();
      renderAuditLogs();
      renderCausas();
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

    // Renderizar causas sin obligar a filtrar por abogado
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
                <button onclick="openEditCausa(${{c.row_index}})" title="Editar Causa" class="px-2 py-0.5 rounded bg-amber-50 hover:bg-amber-100 text-amber-800 border border-amber-300 font-bold text-[9.5px] flex items-center gap-1">
                  ✏️ Editar
                </button>
                <button onclick="confirmDeleteCausa(${{c.row_index}})" title="Eliminar Causa" class="px-2 py-0.5 rounded bg-rose-50 hover:bg-rose-100 text-rose-700 border border-rose-300 font-bold text-[9.5px] flex items-center gap-1">
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

    function openEditCausa(rowIndex) {{
      const tabTitle = currentSelectedTab.title;
      const list = causasPorPestana[tabTitle] || [];
      const causa = list.find(c => c.row_index === rowIndex);
      if (!causa) return;

      const nuevoExp = prompt("Editar Nº de Expediente:", causa.expediente);
      if (nuevoExp === null) return;
      const nuevoMot = prompt("Editar Motivo / Asunto Judicial:", causa.motivo);
      if (nuevoMot === null) return;
      const nuevoDmd = prompt("Editar Demandado / Parte Contraria:", causa.demandado);
      if (nuevoDmd === null) return;
      const nuevoAbg = prompt("Editar Abogado Responsable:", causa.abogado);
      if (nuevoAbg === null) return;
      const nuevoEst = prompt("Editar Estado Actual (ACTIVA / CERRADA / EN TRÁMITE):", causa.estado) || causa.estado;

      causa.expediente = nuevoExp.trim() || causa.expediente;
      causa.motivo = nuevoMot.trim() || causa.motivo;
      causa.demandado = nuevoDmd.trim() || causa.demandado;
      causa.abogado = nuevoAbg.trim() || causa.abogado;
      causa.estado = nuevoEst.trim().toUpperCase() || causa.estado;

      const actor = currentRole === 'admin' ? 'Administrador PGET' : 'Abogado PGET';
      addAuditLog("MODIFICACIÓN CAUSA", causa.expediente, tabTitle, `Expediente editado por ${{actor}}. Asignado a: ${{causa.abogado}}.`);
      renderCausas();
      alert(`¡Causa EXP. ${{causa.expediente}} actualizada exitosamente en Google Sheets!`);
    }}

    function confirmDeleteCausa(rowIndex) {{
      const tabTitle = currentSelectedTab.title;
      const list = causasPorPestana[tabTitle] || [];
      const idx = list.findIndex(c => c.row_index === rowIndex);
      if (idx === -1) return;
      const causa = list[idx];

      const ok = confirm(`¿Estás seguro de que deseas eliminar la causa del Expediente Nº ${{causa.expediente}} (${{causa.motivo}}) de la materia "${{tabTitle}}"?\\n\\nEsta acción quedará registrada en el Registro de Auditoría del Sistema.`);
      if (ok) {{
        list.splice(idx, 1);
        const actor = currentRole === 'admin' ? 'Administrador PGET' : 'Abogado PGET';
        addAuditLog("ELIMINACIÓN CAUSA", causa.expediente, tabTitle, `Causa judicial eliminada del sistema por ${{actor}}.`);
        renderCausas();
        alert(`Causa con Expediente ${{causa.expediente}} eliminada con éxito y registrada en auditoría.`);
      }}
    }}

    function renderLawyers() {{
      const container = document.getElementById('lawyersListContainer');
      container.innerHTML = lawyers.map(l => `
        <div class="p-2.5 bg-slate-50 rounded-xl border border-[#D4AF37] shadow-sm ${{!l.activo ? 'opacity-60 bg-slate-100' : ''}}">
          <div class="flex items-start justify-between">
            <div class="flex items-center gap-2">
              <div class="w-8 h-8 rounded-full bg-[#6B1226] text-[#D4AF37] font-bold flex items-center justify-center text-xs shrink-0 border border-[#D4AF37]">
                ${{l.nombre[0]}}
              </div>
              <div>
                <h5 class="font-bold text-xs text-[#6B1226] flex items-center gap-1.5">
                  ${{l.nombre}}
                  ${{!l.activo ? '<span class="text-[9px] bg-red-100 text-red-700 px-1 py-0.2 rounded font-mono">Desactivado (Histórico)</span>' : ''}}
                </h5>
                <p class="text-[10px] text-slate-500">C.I. ${{l.cedula || 'S/C'}} • ${{l.cargo}}</p>
                <p class="text-[10px] text-slate-600 font-semibold">${{l.adscrito}}</p>
              </div>
            </div>

            <!-- Botones Exclusivos del Admin -->
            <div class="flex items-center gap-1">
              <button onclick="editLawyerPrompt('${{l.id}}')" title="Editar Abogado" class="w-6 h-6 rounded bg-amber-100 hover:bg-amber-200 text-amber-800 text-[11px] flex items-center justify-center border border-amber-300">
                ✏️
              </button>
              ${{l.activo ? `
                <button onclick="deactivateLawyerPrompt('${{l.id}}')" title="Desactivar (Mantiene su historial en expedientes)" class="w-6 h-6 rounded bg-rose-100 hover:bg-rose-200 text-rose-700 text-[11px] flex items-center justify-center border border-rose-300">
                  🚫
                </button>
              ` : `
                <button onclick="reactivateLawyerPrompt('${{l.id}}')" title="Reactivar Abogado" class="w-6 h-6 rounded bg-emerald-100 hover:bg-emerald-200 text-emerald-800 text-[11px] flex items-center justify-center border border-emerald-300">
                  ✅
                </button>
              `}}
            </div>
          </div>
        </div>
      `).join('');
    }}

    function editLawyerPrompt(id) {{
      if (currentRole !== 'admin') {{
        alert("Acceso Restringido: Los abogados no pueden editar la nómina institucional.");
        return;
      }}
      const l = lawyers.find(item => item.id === id);
      if (!l) return;

      const nom = prompt("Editar Nombre del Abogado:", l.nombre);
      if (nom === null) return;
      const ci = prompt("Editar Cédula de Identidad:", l.cedula);
      if (ci === null) return;
      const cargo = prompt("Editar Cargo Institucional:", l.cargo);
      if (cargo === null) return;

      l.nombre = nom.trim().toUpperCase() || l.nombre;
      l.cedula = ci.trim() || l.cedula;
      l.cargo = cargo.trim() || l.cargo;

      addAuditLog("MODIFICACIÓN NÓMINA", "NÓMINA", "ADMINISTRACIÓN", `Se actualizaron datos de ${{l.nombre}} (C.I. ${{l.cedula}}).`);
      renderLawyers();
      alert(`Abogado ${{l.nombre}} actualizado con éxito.`);
    }}

    function deactivateLawyerPrompt(id) {{
      if (currentRole !== 'admin') {{
        alert("Acceso Restringido: Los abogados no pueden dar de baja a miembros de la nómina.");
        return;
      }}
      const l = lawyers.find(item => item.id === id);
      if (!l) return;

      const ok = confirm(`¿Desactivar a ${{l.nombre}} de la nómina activa?\\n\\nNOTA DE SEGURIDAD: Toda su información y actuaciones en expedientes judiciales previos SE CONSERVARÁ INTACTA al 100%.`);
      if (ok) {{
        l.activo = false;
        addAuditLog("DESACTIVACIÓN ABOGADO", "NÓMINA", "ADMINISTRACIÓN", `Se desactivó de nómina a ${{l.nombre}} (Se preserva su historial en expedientes).`);
        renderLawyers();
        alert(`Abogado ${{l.nombre}} desactivado. Su información en expedientes previos se conserva intacta.`);
      }}
    }}

    function reactivateLawyerPrompt(id) {{
      if (currentRole !== 'admin') return;
      const l = lawyers.find(item => item.id === id);
      if (!l) return;
      l.activo = true;
      addAuditLog("REACTIVACIÓN ABOGADO", "NÓMINA", "ADMINISTRACIÓN", `Se reactivó a ${{l.nombre}} en nómina activa.`);
      renderLawyers();
      alert(`Abogado ${{l.nombre}} reactivado exitosamente.`);
    }}

    function openAddLawyerPrompt() {{
      if (currentRole !== 'admin') {{
        alert("Acceso Restringido: Los abogados no pueden registrar nuevos abogados.");
        return;
      }}
      const nom = prompt("Nombre y Apellido del nuevo abogado PGET:");
      if (!nom || !nom.trim()) return;
      const ci = prompt("Cédula de Identidad:") || "";
      const cargo = prompt("Cargo Institucional:") || "Abogado Adscrito";

      const nuevo = {{
        id: (lawyers.length + 1).toString(),
        nombre: nom.trim().toUpperCase(),
        cedula: ci.trim(),
        cargo: cargo.trim(),
        adscrito: "Procuraduría General del Estado Trujillo",
        activo: true
      }};

      lawyers.push(nuevo);
      addAuditLog("ALTA ABOGADO", "NÓMINA", "ADMINISTRACIÓN", `Alta de ${{nuevo.nombre}} (C.I. ${{nuevo.cedula}}).`);
      renderLawyers();
      alert(`Abogado ${{nuevo.nombre}} registrado en nómina.`);
    }}

    function renderAuditLogs() {{
      const container = document.getElementById('auditListContainer');
      container.innerHTML = auditLogs.map(item => `
        <div class="bg-white p-2.5 rounded-xl border border-[#D4AF37] shadow-sm">
          <div class="flex items-center justify-between text-[10px] text-slate-400 mb-1">
            <span class="font-bold text-[#6B1226] flex items-center gap-1">
              ⏱️ ${{item.fecha}}
            </span>
            <span class="font-extrabold text-[9px] px-1.5 py-0.5 rounded bg-[#6B1226]/10 text-[#6B1226] border border-[#6B1226]/30">
              ${{item.accion}}
            </span>
          </div>
          <div class="font-bold text-xs text-slate-800">
            <span class="text-[#D4AF37]">👤 ${{item.usuario}}:</span> ${{item.detalle}}
          </div>
          <div class="mt-1 text-[10px] text-slate-500">
            <strong>Expediente:</strong> ${{item.expediente}} • <strong>Materia:</strong> ${{item.pestana}}
          </div>
        </div>
      `).join('');
    }}

    function addAuditLog(accion, expediente, pestana, detalle) {{
      const nuevo = {{
        id: (auditLogs.length + 1).toString(),
        fecha: new Date().toLocaleDateString('es-ES') + ', ' + new Date().toLocaleTimeString('es-ES', {{hour: '2-digit', minute:'2-digit'}}),
        usuario: currentRole === 'admin' ? 'Admin PGET' : 'Abogado PGET',
        accion: accion,
        expediente: expediente,
        pestana: pestana,
        detalle: detalle
      }};
      auditLogs.unshift(nuevo);
      renderAuditLogs();
    }}

    function openSelectTabModal() {{
      document.getElementById('modalSelectTab').classList.remove('hidden');
    }}

    function closeSelectTabModal() {{
      document.getElementById('modalSelectTab').classList.add('hidden');
    }}

    function selectTabForForm(tabTitle) {{
      formSelectedTab = tabsData.find(t => t.title === tabTitle) || tabsData[0];
      closeSelectTabModal();
      buildFormForTab(formSelectedTab);
      switchView('form');
    }}

    function buildFormForTab(tab) {{
      document.getElementById('formHeaderTitle').innerText = tab.title;
      document.getElementById('formHeaderSubtitle').innerText = `${{tab.category}} • ${{tab.columns.length}} Columnas`;

      const container = document.getElementById('formInputsContainer');
      const today = new Date().toLocaleDateString('es-ES');

      container.innerHTML = tab.columns.map((col, idx) => {{
        const cUp = col.toUpperCase();
        const isAbg = cUp.includes('ABG') || cUp.includes('RESPONSABLE');
        const isEst = cUp.includes('ESTADO') && !cUp.includes('ADSCRITO');
        const isMulti = cUp.includes('ACTUACION') || cUp.includes('OBSERVACION') || cUp.includes('MOTIVO') || cUp.includes('DELITO');

        if (isAbg) {{
          return `
            <div>
              <label class="block text-[10px] font-extrabold text-[#6B1226] uppercase mb-0.5">${{col}} *</label>
              <select name="col_${{idx}}" class="w-full bg-white border border-[#D4AF37] rounded-lg px-2 py-1.5 text-xs font-bold text-[#6B1226] focus:outline-none">
                ${{lawyers.filter(l => l.activo).map(l => `<option value="${{l.nombre}}">${{l.nombre}}</option>`).join('')}}
              </select>
            </div>
          `;
        }}

        if (isEst) {{
          return `
            <div>
              <label class="block text-[10px] font-extrabold text-[#6B1226] uppercase mb-0.5">${{col}} *</label>
              <select name="col_${{idx}}" class="w-full bg-white border border-[#D4AF37] rounded-lg px-2 py-1.5 text-xs font-bold text-slate-800 focus:outline-none">
                <option value="ACTIVA">ACTIVA</option>
                <option value="CERRADA">CERRADA</option>
                <option value="EN TRÁMITE">EN TRÁMITE</option>
              </select>
            </div>
          `;
        }}

        let defaultVal = '';
        if (idx === 0 && (cUp.includes('Nº') || cUp.includes('N°'))) defaultVal = (causasPorPestana[tab.title]?.length + 1) || '1';
        if (cUp.includes('FECHA')) defaultVal = today;
        if (cUp.includes('DEMANDANTE') && cUp.includes('PROCURADUR')) defaultVal = 'PROCURADURÍA GENERAL DEL ESTADO TRUJILLO';

        if (isMulti) {{
          return `
            <div>
              <label class="block text-[10px] font-extrabold text-[#6B1226] uppercase mb-0.5">${{col}}</label>
              <textarea name="col_${{idx}}" rows="2" class="w-full bg-white border border-[#D4AF37] rounded-lg px-2 py-1 text-xs text-slate-800 focus:outline-none">${{defaultVal}}</textarea>
            </div>
          `;
        }}

        return `
          <div>
            <label class="block text-[10px] font-extrabold text-[#6B1226] uppercase mb-0.5">${{col}} ${{cUp.includes('EXPEDIENTE') ? '*' : ''}}</label>
            <input type="text" name="col_${{idx}}" value="${{defaultVal}}" class="w-full bg-white border border-[#D4AF37] rounded-lg px-2 py-1 text-xs text-slate-800 focus:outline-none" ${{cUp.includes('EXPEDIENTE') ? 'required' : ''}}>
          </div>
        `;
      }}).join('');
    }}

    function switchView(viewName) {{
      if (viewName === 'lawyers-admin' && currentRole !== 'admin') {{
        alert("Acceso Restringido: Los abogados no tienen permisos para añadir, editar o dar de baja abogados de la nómina. Esta función es de uso exclusivo del Administrador PGET.");
        return;
      }}

      document.getElementById('view-list').classList.add('hidden');
      document.getElementById('view-lawyers-admin').classList.add('hidden');
      document.getElementById('view-audit-admin').classList.add('hidden');
      document.getElementById('view-form').classList.add('hidden');

      if (viewName === 'list') {{
        document.getElementById('view-list').classList.remove('hidden');
        renderCausas();
      }} else if (viewName === 'lawyers-admin') {{
        document.getElementById('view-lawyers-admin').classList.remove('hidden');
        renderLawyers();
      }} else if (viewName === 'audit-admin') {{
        document.getElementById('view-audit-admin').classList.remove('hidden');
        renderAuditLogs();
      }} else if (viewName === 'form') {{
        document.getElementById('view-form').classList.remove('hidden');
      }}
    }}

    function saveDynamicCausa(e) {{
      e.preventDefault();
      const btn = document.getElementById('btnSaveCausa');
      btn.innerHTML = '<span>⏳ Guardando en Sheets...</span>';
      btn.disabled = true;

      const formData = new FormData(e.target);
      const exp = formData.get('col_5') || formData.get('col_6') || formData.get('col_4') || ('EXP-' + Date.now().toString().slice(-4));
      const mot = formData.get('col_4') || formData.get('col_3') || formData.get('col_2') || 'Nueva causa';
      const dmd = formData.get('col_3') || formData.get('col_2') || '';
      const abg = formData.get('col_6') || formData.get('col_7') || (lawyers[0]?.nombre || 'Samantha Polanco');

      setTimeout(() => {{
        const newCausa = {{
          row_index: (causasPorPestana[formSelectedTab.title]?.length || 0) + 1,
          expediente: exp,
          motivo: mot,
          demandado: dmd,
          abogado: abg,
          estado: 'ACTIVA',
          year: new Date().getFullYear().toString(),
          fecha: new Date().toLocaleDateString('es-ES')
        }};

        causasPorPestana[formSelectedTab.title].unshift(newCausa);
        
        addAuditLog("CREACIÓN CAUSA", exp, formSelectedTab.title, `Se creó causa "${{mot}}" asignada a ${{abg}}.`);

        document.getElementById('sheetTabSelect').value = formSelectedTab.title;
        currentSelectedTab = formSelectedTab;

        btn.innerHTML = '<span>☁️ Guardar en Google Sheets</span>';
        btn.disabled = false;
        
        switchView('list');
        renderCausas();
        alert(`¡Causa registrada y sincronizada en Google Sheets dentro de "${{formSelectedTab.title}}"!`);
      }}, 500);
    }}

    function setRole(role) {{
      currentRole = role;
      document.getElementById('btn-admin').className = role === 'admin' ? 'px-2.5 py-0.5 rounded-full font-bold bg-white text-[#6B1226]' : 'px-2.5 py-0.5 rounded-full font-bold text-white/80';
      document.getElementById('btn-lawyer').className = role === 'lawyer' ? 'px-2.5 py-0.5 rounded-full font-bold bg-white text-[#6B1226]' : 'px-2.5 py-0.5 rounded-full font-bold text-white/80';
      document.getElementById('admin-subbar').classList.toggle('hidden', role !== 'admin');
      document.getElementById('lawyer-badge').classList.toggle('hidden', role === 'admin');
      
      if (role === 'lawyer' && !document.getElementById('view-lawyers-admin').classList.contains('hidden')) {{
        switchView('list');
      }}
      renderCausas();
    }}

    init();
  </script>
</body>
</html>
"""

with open('C:/Users/PC/.gemini/antigravity/brain/098ba3de-2780-4abe-8d88-54767a85600a/prototype.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Self-contained CSP-compliant prototype.html created successfully!")

