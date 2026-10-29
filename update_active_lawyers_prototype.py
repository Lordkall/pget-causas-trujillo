import re

with open('create_complete_prototype.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Reemplazar la lista de abogados
old_lawyers_pattern = r'// Nómina Oficial Completa de 29 Abogados Extraídos del Documento\s+let lawyers = \[[\s\S]*?\];'

new_lawyers_code = """// Nómina Oficial PGET: 13 Abogados Activos (Ordenados Alfabéticamente) + Históricos
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
    ];"""

code = re.sub(old_lawyers_pattern, new_lawyers_code, code)

# 2. Actualizar el encabezado de nómina en la vista del móvil
code = code.replace(
    '<p class="text-[10px] text-slate-500">29 Abogados oficiales (Google Sheets)</p>',
    '<p class="text-[10px] text-slate-500">13 Abogados Activos Oficiales (A-Z)</p>'
)

# 3. Actualizar la tarjeta lateral de abogados clave
old_tarjeta_2 = """      <!-- Tarjeta 2: Abogados Clave Confirmados -->
      <div class="bg-amber-50/70 border border-[#D4AF37] rounded-2xl p-4 shadow-sm">
        <h3 class="text-xs font-black text-[#6B1226] uppercase tracking-wider mb-2">Abogadas Clave en Nómina</h3>
        <div class="space-y-2 text-xs">
          <div class="bg-white p-2 rounded-xl border border-amber-300">
            <strong class="text-slate-800">MARÍA DE LOS ÁNGELES OJEDA</strong>
            <p class="text-[11px] text-slate-500">C.I. 18.456.789 • Contencioso Trujillo & Laboral</p>
          </div>
          <div class="bg-white p-2 rounded-xl border border-amber-300">
            <strong class="text-slate-800">ROXANNA MERCADO</strong>
            <p class="text-[11px] text-slate-500">C.I. 17.654.321 • Juzgados, Tribunales & Contencioso</p>
          </div>
        </div>
      </div>"""

new_tarjeta_2 = """      <!-- Tarjeta 2: Nómina Activa Oficial PGET (Orden Alfabético) -->
      <div class="bg-white border border-[#D4AF37] rounded-2xl p-4 shadow-sm">
        <div class="flex items-center justify-between mb-2">
          <h3 class="text-xs font-black text-[#6B1226] uppercase tracking-wider">Nómina Activa (13 Abogados A-Z)</h3>
          <span class="text-[10px] bg-emerald-100 text-emerald-800 px-2 py-0.5 rounded-full font-bold">Oficiales PGET</span>
        </div>
        <p class="text-[11px] text-slate-600 mb-2">
          Únicos habilitados en el selector para la creación de nuevos expedientes:
        </p>
        <div class="space-y-1.5 text-xs max-h-60 overflow-y-auto pr-1">
          <div class="p-1.5 rounded-lg bg-slate-50 border border-slate-200 flex items-center justify-between">
            <span class="font-bold text-slate-800">1. BARRIOS JULIO ALEXANDER</span>
            <span class="text-[10px] text-slate-500 font-mono">14.459.865</span>
          </div>
          <div class="p-1.5 rounded-lg bg-slate-50 border border-slate-200 flex items-center justify-between">
            <span class="font-bold text-slate-800">2. BARRIOS MARIA ALCIRA</span>
            <span class="text-[10px] text-slate-500 font-mono">17.037.437</span>
          </div>
          <div class="p-1.5 rounded-lg bg-slate-50 border border-slate-200 flex items-center justify-between">
            <span class="font-bold text-slate-800">3. BRICEÑO F. ARMANDO JOSE</span>
            <span class="text-[10px] text-slate-500 font-mono">5.780.167</span>
          </div>
          <div class="p-1.5 rounded-lg bg-slate-50 border border-slate-200 flex items-center justify-between">
            <span class="font-bold text-slate-800">4. BRICEÑO V. LIZAMAR INDIRA</span>
            <span class="text-[10px] text-[#6B1226] font-bold">DIR. ASUNTOS JUR.</span>
          </div>
          <div class="p-1.5 rounded-lg bg-slate-50 border border-slate-200 flex items-center justify-between">
            <span class="font-bold text-slate-800">5. DE ABREU H. CARLOS EDUARDO</span>
            <span class="text-[10px] text-slate-500 font-mono">10.446.852</span>
          </div>
          <div class="p-1.5 rounded-lg bg-slate-50 border border-slate-200 flex items-center justify-between">
            <span class="font-bold text-[#6B1226]">6. DORA ALICIA MATHEUS</span>
            <span class="text-[10px] text-[#D4AF37] bg-[#6B1226] px-1.5 py-0.2 rounded font-bold">PROCURADORA</span>
          </div>
          <div class="p-1.5 rounded-lg bg-slate-50 border border-slate-200 flex items-center justify-between">
            <span class="font-bold text-slate-800">7. MERCADO H. ROXANNA KAROLINA</span>
            <span class="text-[10px] text-slate-500 font-mono">23.596.460</span>
          </div>
          <div class="p-1.5 rounded-lg bg-slate-50 border border-slate-200 flex items-center justify-between">
            <span class="font-bold text-slate-800">8. MOLINA U. HUMBERTO JOSE</span>
            <span class="text-[10px] text-slate-500 font-mono">20.790.382</span>
          </div>
          <div class="p-1.5 rounded-lg bg-slate-50 border border-slate-200 flex items-center justify-between">
            <span class="font-bold text-slate-800">9. MORENO H. YONEXI CAROLINA</span>
            <span class="text-[10px] text-slate-500 font-mono">16.738.909</span>
          </div>
          <div class="p-1.5 rounded-lg bg-slate-50 border border-slate-200 flex items-center justify-between">
            <span class="font-bold text-slate-800">10. OJEDA N. MARIA DE LOS ANGELES</span>
            <span class="text-[10px] text-slate-500 font-mono">26.046.163</span>
          </div>
          <div class="p-1.5 rounded-lg bg-slate-50 border border-slate-200 flex items-center justify-between">
            <span class="font-bold text-slate-800">11. RAMIREZ O. TATIANA MARILIN</span>
            <span class="text-[10px] text-slate-500 font-mono">15.315.709</span>
          </div>
          <div class="p-1.5 rounded-lg bg-slate-50 border border-slate-200 flex items-center justify-between">
            <span class="font-bold text-slate-800">12. SANCHEZ M. LILIBETH DAYANA</span>
            <span class="text-[10px] text-slate-500 font-mono">13.404.142</span>
          </div>
          <div class="p-1.5 rounded-lg bg-slate-50 border border-slate-200 flex items-center justify-between">
            <span class="font-bold text-slate-800">13. VALE V. YULIANOVA PAOLA</span>
            <span class="text-[10px] text-slate-500 font-mono">26.591.763</span>
          </div>
        </div>
      </div>"""

code = code.replace(old_tarjeta_2, new_tarjeta_2)

with open('create_complete_prototype.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("create_complete_prototype.py updated successfully!")

