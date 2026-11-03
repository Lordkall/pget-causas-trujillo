'use client';

import React, { useState, useEffect, useMemo } from 'react';
import Image from 'next/image';
import { PGET_TABS } from '@/lib/tabsData';
import { ABOGADOS_PGET } from '@/lib/abogadosData';
import { 
  Search, Plus, ShieldCheck, Scale, Calendar, Users, 
  FolderCheck, FolderClock, LogOut, Share, X, CheckCircle, 
  AlertCircle, ChevronDown, RefreshCw
} from 'lucide-react';

export default function HomePage() {
  const [currentUser, setCurrentUser] = useState(null);
  const [showLoginModal, setShowLoginModal] = useState(false);
  const [loginId, setLoginId] = useState('');
  const [loginPass, setLoginPass] = useState('');
  const [loginError, setLoginError] = useState('');

  const [currentTab, setCurrentTab] = useState(PGET_TABS[0]);
  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [estadoFilter, setEstadoFilter] = useState('TODAS');
  const [yearFilter, setYearFilter] = useState('TODOS');

  // Modal Crear Causa
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [formValues, setFormValues] = useState({});
  const [isSaving, setIsSaving] = useState(false);
  const [saveSuccess, setSaveSuccess] = useState('');
  const [saveError, setSaveError] = useState('');

  // Prompt PWA iPhone
  const [showIosPrompt, setShowIosPrompt] = useState(false);

  useEffect(() => {
    // Detectar si está en iPhone Safari y no en modo standalone
    const isIos = /iPad|iPhone|iPod/.test(navigator.userAgent) && !window.MSStream;
    const isStandalone = window.navigator.standalone || window.matchMedia('(display-mode: standalone)').matches;
    if (isIos && !isStandalone) {
      setShowIosPrompt(true);
    }

    // Cargar sesión previa si existe
    const saved = localStorage.getItem('pget_user');
    if (saved) {
      try {
        setCurrentUser(JSON.parse(saved));
      } catch (_) {}
    } else {
      // Default como Abogado oficial para navegación directa
      const def = ABOGADOS_PGET[0];
      setCurrentUser(def);
      localStorage.setItem('pget_user', JSON.stringify(def));
    }
  }, []);

  // Cargar filas cuando cambia la pestaña
  useEffect(() => {
    fetchTabRows(currentTab.title);
  }, [currentTab]);

  async function fetchTabRows(tabTitle) {
    setLoading(true);
    try {
      const res = await fetch(`/api/causas?tab=${encodeURIComponent(tabTitle)}`);
      const data = await res.json();
      if (data.success) {
        setRows(data.rows || []);
      } else {
        console.error(data.error);
      }
    } catch (e) {
      console.error('Error fetching tab rows:', e);
    } finally {
      setLoading(false);
    }
  }

  // Extraer año de una fila
  function extractYear(row) {
    if (!row) return '';
    for (const cell of row) {
      const str = String(cell);
      const match = str.match(/\b\d{1,2}[/-]\d{1,2}[/-](\d{4})\b/);
      if (match) return match[1];
    }
    for (const cell of row) {
      const str = String(cell);
      const match = str.match(/(?:19|20)\d{2}/g);
      if (match && match.length > 0) return match[match.length - 1];
    }
    return '';
  }

  // Años disponibles en la pestaña activa
  const availableYears = useMemo(() => {
    const set = new Set();
    rows.forEach(r => {
      const y = extractYear(r);
      if (y && y.length === 4) set.add(y);
    });
    const sorted = Array.from(set).sort((a, b) => b.localeCompare(a));
    return ['TODOS', ...sorted];
  }, [rows]);

  // Filtrado de causas
  const filteredRows = useMemo(() => {
    return rows.filter(row => {
      // 1. Descartar filas vacías o banners
      const joined = row.map(c => String(c)).join(' ').toUpperCase();
      if (joined.includes('CAUSAS') && (joined.includes('20') || joined.includes('19'))) return false;
      const nonBlank = row.filter(c => c && String(c).trim() !== '');
      if (nonBlank.length <= 1) return false;

      // 2. Filtro de búsqueda
      if (searchQuery.trim()) {
        const q = searchQuery.toUpperCase();
        if (!joined.includes(q)) return false;
      }

      // 3. Filtro por Año
      if (yearFilter !== 'TODOS') {
        const y = extractYear(row);
        if (y !== yearFilter) return false;
      }

      // 4. Filtro por Estado
      if (estadoFilter !== 'TODAS') {
        const estIdx = currentTab.columns.findIndex(c => c.toUpperCase().includes('ESTADO'));
        if (estIdx !== -1 && row[estIdx]) {
          const val = String(row[estIdx]).toUpperCase();
          if (estadoFilter === 'ACTIVA' && !val.includes('ACTIV')) return false;
          if (estadoFilter === 'CERRADA' && !val.includes('CERRAD')) return false;
          if (estadoFilter === 'EN TRÁMITE' && !(val.includes('TRAMITE') || val.includes('TRÁMITE'))) return false;
        }
      }

      return true;
    });
  }, [rows, searchQuery, yearFilter, estadoFilter, currentTab]);

  // Métricas
  const stats = useMemo(() => {
    let activas = 0;
    let cerradas = 0;
    const estIdx = currentTab.columns.findIndex(c => c.toUpperCase().includes('ESTADO'));

    filteredRows.forEach(r => {
      if (estIdx !== -1 && r[estIdx]) {
        const val = String(r[estIdx]).toUpperCase();
        if (val.includes('ACTIV')) activas++;
        else if (val.includes('CERRAD')) cerradas++;
      } else {
        activas++;
      }
    });

    return {
      total: filteredRows.length,
      activas,
      cerradas,
      nomina: ABOGADOS_PGET.filter(a => a.activo).length,
    };
  }, [filteredRows, currentTab]);

  // Manejo de Login
  function handleLogin(e) {
    e.preventDefault();
    setLoginError('');
    const cleanId = loginId.trim().toUpperCase().replace(/[.\s-]/g, '');
    const cleanPass = loginPass.trim();

    const user = ABOGADOS_PGET.find(a => {
      const matchCedula = a.cedula.replace(/[.\s-]/g, '').toUpperCase() === cleanId;
      const matchCorreo = a.correo.toUpperCase() === cleanId;
      const matchNombre = a.nombre.toUpperCase().includes(cleanId);
      return (matchCedula || matchCorreo || matchNombre);
    });

    if (!user || user.clave !== cleanPass) {
      setLoginError('Credenciales incorrectas');
      return;
    }

    setCurrentUser(user);
    localStorage.setItem('pget_user', JSON.stringify(user));
    setShowLoginModal(false);
    setLoginPass('');
  }

  function handleLogout() {
    localStorage.removeItem('pget_user');
    setCurrentUser(null);
    setShowLoginModal(true);
  }

  // Guardar nueva causa
  async function handleSaveCause(e) {
    e.preventDefault();
    setIsSaving(true);
    setSaveError('');
    setSaveSuccess('');

    try {
      const rowValues = currentTab.columns.map((col, idx) => {
        return formValues[idx] || '';
      });

      const res = await fetch('/api/causas', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          tabTitle: currentTab.title,
          rowValues,
          targetYear: 2026,
        }),
      });

      const data = await res.json();
      if (!data.success) {
        throw new Error(data.error || 'Error al guardar');
      }

      setSaveSuccess(`¡Causa registrada con éxito en ${currentTab.title}!`);
      // Refrescar filas
      await fetchTabRows(currentTab.title);
      setTimeout(() => {
        setShowCreateModal(false);
        setFormValues({});
        setSaveSuccess('');
      }, 1500);
    } catch (err) {
      setSaveError(err.message);
    } finally {
      setIsSaving(false);
    }
  }

  return (
    <div className="min-h-screen pb-24 bg-[#F8F9FA]">
      {/* HEADER INSTITUCIONAL */}
      <header className="sticky top-0 z-30 bg-[#6B1226] text-white shadow-md border-b-2 border-[#D4AF37]">
        <div className="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-full border border-[#D4AF37] overflow-hidden bg-white/10 flex items-center justify-center">
              <img src="/logo.png" alt="Escudo PGET" className="w-9 h-9 object-contain" />
            </div>
            <div>
              <h1 className="text-sm font-bold tracking-wider text-[#D4AF37] leading-tight">
                PROCURADURÍA GENERAL
              </h1>
              <p className="text-xs text-white/90 font-medium">
                ESTADO TRUJILLO • CAUSAS
              </p>
            </div>
          </div>

          <div className="flex items-center space-x-2">
            {currentUser ? (
              <div className="flex items-center space-x-2">
                <span className="text-xs bg-[#4A0C1A] text-[#D4AF37] font-semibold px-2.5 py-1 rounded-full border border-[#D4AF37]/50 max-w-[120px] truncate sm:max-w-none">
                  {currentUser.nombre.split(' ')[0]} {currentUser.rol === 'admin' ? '(ADMIN)' : ''}
                </span>
                <button 
                  onClick={handleLogout}
                  title="Cerrar sesión"
                  className="p-1.5 rounded-full hover:bg-white/10 text-white/80 hover:text-white transition"
                >
                  <LogOut className="w-4 h-4" />
                </button>
              </div>
            ) : (
              <button
                onClick={() => setShowLoginModal(true)}
                className="text-xs bg-[#D4AF37] text-[#6B1226] font-bold px-3 py-1.5 rounded-lg hover:bg-[#F4D068] transition"
              >
                Ingresar
              </button>
            )}
          </div>
        </div>

        {/* SUBHEADER: ABOGADO ACTIVO */}
        {currentUser && (
          <div className="bg-[#560D1E] px-4 py-1.5 text-xs text-white/90 flex items-center justify-between border-t border-white/10">
            <div className="flex items-center space-x-2 truncate">
              <Users className="w-3.5 h-3.5 text-[#D4AF37]" />
              <span className="text-white/70">Abogado:</span>
              <span className="font-semibold text-white truncate">{currentUser.nombre}</span>
            </div>
            <button
              onClick={() => fetchTabRows(currentTab.title)}
              className="flex items-center space-x-1 text-xs text-[#D4AF37] hover:underline"
            >
              <RefreshCw className={`w-3 h-3 ${loading ? 'animate-spin' : ''}`} />
              <span className="hidden sm:inline">Actualizar</span>
            </button>
          </div>
        )}
      </header>

      {/* BANNER INSTALACIÓN IPHONE (PWA) */}
      {showIosPrompt && (
        <div className="bg-amber-50 border-b border-amber-200 px-4 py-2.5 flex items-center justify-between text-xs text-amber-900 shadow-sm">
          <div className="flex items-center space-x-2">
            <Share className="w-4 h-4 text-[#6B1226] flex-shrink-0" />
            <span>
              Para usar en tu <strong>iPhone</strong> como App: toca el botón <strong>Compartir</strong> en Safari y selecciona <strong>"Agregar al inicio"</strong>.
            </span>
          </div>
          <button 
            onClick={() => setShowIosPrompt(false)}
            className="p-1 text-amber-700 hover:text-black"
          >
            <X className="w-4 h-4" />
          </button>
        </div>
      )}

      {/* CONTENIDO PRINCIPAL */}
      <main className="max-w-7xl mx-auto px-4 py-4 space-y-4">
        {/* SELECTOR DE PESTAÑA */}
        <div className="bg-white p-3 rounded-xl shadow-sm border border-slate-200">
          <label className="block text-xs font-bold text-[#6B1226] uppercase tracking-wider mb-1">
            Materia / Tribunal:
          </label>
          <div className="relative">
            <select
              value={currentTab.title}
              onChange={(e) => {
                const found = PGET_TABS.find(t => t.title === e.target.value);
                if (found) setCurrentTab(found);
              }}
              className="w-full bg-slate-50 border border-slate-300 rounded-lg px-3 py-2 text-sm font-semibold text-slate-800 appearance-none focus:outline-none focus:ring-2 focus:ring-[#6B1226]"
            >
              {PGET_TABS.map((t) => (
                <option key={t.gid} value={t.title}>
                  {t.title} ({t.category})
                </option>
              ))}
            </select>
            <ChevronDown className="w-4 h-4 text-slate-500 absolute right-3 top-3 pointer-events-none" />
          </div>
        </div>

        {/* MÉTRICAS RÁPIDAS */}
        <div className="grid grid-cols-4 gap-2 sm:gap-3">
          <div className="bg-white p-2.5 rounded-xl border border-slate-200 text-center shadow-sm">
            <span className="block text-lg font-black text-[#6B1226]">{stats.total}</span>
            <span className="text-[10px] sm:text-xs font-semibold text-slate-600">Causas</span>
          </div>
          <div className="bg-white p-2.5 rounded-xl border border-slate-200 text-center shadow-sm">
            <span className="block text-lg font-black text-emerald-600">{stats.activas}</span>
            <span className="text-[10px] sm:text-xs font-semibold text-slate-600">Activas</span>
          </div>
          <div className="bg-white p-2.5 rounded-xl border border-slate-200 text-center shadow-sm">
            <span className="block text-lg font-black text-slate-700">{stats.cerradas}</span>
            <span className="text-[10px] sm:text-xs font-semibold text-slate-600">Cerradas</span>
          </div>
          <div className="bg-white p-2.5 rounded-xl border border-slate-200 text-center shadow-sm">
            <span className="block text-lg font-black text-[#D4AF37]">{stats.nomina}</span>
            <span className="text-[10px] sm:text-xs font-semibold text-slate-600">Nómina</span>
          </div>
        </div>

        {/* BUSCADOR */}
        <div className="relative">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
          <input
            type="text"
            placeholder={`Buscar en ${currentTab.title}...`}
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full bg-white border border-slate-300 rounded-xl pl-9 pr-4 py-2 text-sm text-slate-800 placeholder-slate-400 shadow-sm focus:outline-none focus:ring-2 focus:ring-[#6B1226]"
          />
          {searchQuery && (
            <button 
              onClick={() => setSearchQuery('')}
              className="absolute right-3 top-2.5 text-slate-400 hover:text-slate-600"
            >
              <X className="w-4 h-4" />
            </button>
          )}
        </div>

        {/* FILTROS (ESTADO Y AÑO) */}
        <div className="space-y-2">
          {/* Estados */}
          <div className="flex space-x-1.5 overflow-x-auto pb-1 scrollbar-none">
            {['TODAS', 'ACTIVA', 'CERRADA', 'EN TRÁMITE'].map((est) => (
              <button
                key={est}
                onClick={() => setEstadoFilter(est)}
                className={`text-xs font-bold px-3 py-1.5 rounded-lg whitespace-nowrap transition ${
                  estadoFilter === est
                    ? 'bg-[#6B1226] text-white shadow-sm'
                    : 'bg-white text-slate-700 border border-slate-200 hover:bg-slate-100'
                }`}
              >
                {est}
              </button>
            ))}
          </div>

          {/* Selector de Años */}
          <div className="flex items-center space-x-2">
            <Calendar className="w-4 h-4 text-[#D4AF37]" />
            <span className="text-xs font-bold text-slate-600">Año:</span>
            <div className="flex space-x-1.5 overflow-x-auto pb-1 scrollbar-none flex-1">
              {availableYears.map((yr) => (
                <button
                  key={yr}
                  onClick={() => setYearFilter(yr)}
                  className={`text-[11px] font-bold px-2.5 py-1 rounded-md transition ${
                    yearFilter === yr
                      ? 'bg-[#D4AF37] text-[#4A0C1A]'
                      : 'bg-white text-slate-600 border border-slate-200 hover:bg-slate-50'
                  }`}
                >
                  {yr}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* LISTA DE CAUSAS */}
        <div className="space-y-2.5">
          {loading ? (
            <div className="bg-white rounded-xl p-8 text-center text-slate-500 border border-slate-200">
              <RefreshCw className="w-6 h-6 animate-spin mx-auto text-[#6B1226] mb-2" />
              <p className="text-xs font-semibold">Cargando causas desde Google Sheets...</p>
            </div>
          ) : filteredRows.length === 0 ? (
            <div className="bg-white rounded-xl p-8 text-center text-slate-500 border border-slate-200">
              <AlertCircle className="w-8 h-8 text-slate-300 mx-auto mb-2" />
              <p className="text-sm font-semibold">No se encontraron causas con los filtros aplicados</p>
              <p className="text-xs text-slate-400 mt-1">Prueba cambiando el año o la búsqueda</p>
            </div>
          ) : (
            filteredRows.map((row, index) => {
              const yr = extractYear(row) || 'Sin Año';
              const expIdx = currentTab.columns.findIndex(c => c.toUpperCase().includes('EXPEDIENTE'));
              const motivoIdx = currentTab.columns.findIndex(c => c.toUpperCase().includes('MOTIVO'));
              const demIdx = currentTab.columns.findIndex(c => c.toUpperCase().includes('DEMANDADO') || c.toUpperCase().includes('SOLICITADO') || c.toUpperCase().includes('QUERELLADO'));
              const abgIdx = currentTab.columns.findIndex(c => c.toUpperCase().includes('ABG') || c.toUpperCase().includes('RESPONSABLE'));
              const estIdx = currentTab.columns.findIndex(c => c.toUpperCase().includes('ESTADO'));

              const exp = (expIdx !== -1 && row[expIdx]) ? row[expIdx] : `Causa #${index + 1}`;
              const motivo = (motivoIdx !== -1 && row[motivoIdx]) ? row[motivoIdx] : 'Sin motivo especificado';
              const contra = (demIdx !== -1 && row[demIdx]) ? row[demIdx] : null;
              const abg = (abgIdx !== -1 && row[abgIdx]) ? row[abgIdx] : 'Sin asignar';
              const estado = (estIdx !== -1 && row[estIdx]) ? String(row[estIdx]).toUpperCase() : 'ACTIVA';

              return (
                <div 
                  key={index}
                  className="bg-white rounded-xl p-3.5 shadow-sm border border-slate-200 hover:border-[#D4AF37] transition"
                >
                  <div className="flex items-center justify-between mb-2">
                    <div className="flex items-center space-x-1.5 flex-wrap gap-y-1">
                      <span className="text-xs font-bold bg-[#6B1226] text-white px-2.5 py-0.5 rounded-md">
                        EXP. {exp}
                      </span>
                      <span className="text-xs font-semibold bg-amber-50 text-amber-900 border border-amber-200 px-2 py-0.5 rounded-md">
                        {yr}
                      </span>
                    </div>

                    <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                      estado.includes('ACTIV') 
                        ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' 
                        : estado.includes('CERRAD') 
                        ? 'bg-slate-100 text-slate-700 border border-slate-300' 
                        : 'bg-amber-50 text-amber-700 border border-amber-200'
                    }`}>
                      {estado}
                    </span>
                  </div>

                  <h3 className="text-sm font-bold text-slate-900 leading-snug mb-1">
                    {motivo}
                  </h3>

                  {contra && (
                    <p className="text-xs text-slate-600 mb-2">
                      <span className="font-semibold text-slate-500">Contra:</span> {contra}
                    </p>
                  )}

                  <div className="pt-2 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
                    <div className="flex items-center space-x-1 truncate max-w-[220px]">
                      <Users className="w-3.5 h-3.5 text-[#D4AF37]" />
                      <span className="truncate">{abg}</span>
                    </div>
                    <span className="text-[11px] text-slate-400">Fila {index + 1}</span>
                  </div>
                </div>
              );
            })
          )}
        </div>
      </main>

      {/* BOTÓN FLOTANTE CREAR CAUSA */}
      <div className="fixed bottom-5 right-5 z-20">
        <button
          onClick={() => {
            // Inicializar formulario con defaults
            const init = {};
            const fechaIdx = currentTab.columns.findIndex(c => c.toUpperCase().includes('FECHA'));
            const estadoIdx = currentTab.columns.findIndex(c => c.toUpperCase().includes('ESTADO'));
            const abgIdx = currentTab.columns.findIndex(c => c.toUpperCase().includes('ABG') || c.toUpperCase().includes('RESPONSABLE'));

            if (fechaIdx !== -1) init[fechaIdx] = '03/11/2026';
            if (estadoIdx !== -1) init[estadoIdx] = 'ACTIVA';
            if (abgIdx !== -1 && currentUser) init[abgIdx] = currentUser.nombre;

            setFormValues(init);
            setShowCreateModal(true);
          }}
          className="flex items-center space-x-2 bg-[#D4AF37] hover:bg-[#F4D068] text-[#4A0C1A] font-extrabold px-4 py-3 rounded-full shadow-lg border border-[#AA8822] transition transform active:scale-95"
        >
          <Plus className="w-5 h-5" />
          <span className="text-sm">Crear Causa PGET</span>
        </button>
      </div>

      {/* MODAL CREAR CAUSA */}
      {showCreateModal && (
        <div className="fixed inset-0 z-50 bg-black/60 flex items-end sm:items-center justify-center p-0 sm:p-4 animate-in fade-in">
          <div className="bg-white w-full sm:max-w-xl max-h-[90vh] rounded-t-2xl sm:rounded-2xl shadow-2xl flex flex-col overflow-hidden">
            <div className="bg-[#6B1226] text-white px-4 py-3 border-b-2 border-[#D4AF37] flex items-center justify-between">
              <div>
                <h3 className="text-sm font-bold text-[#D4AF37]">NUEVA CAUSA JUDICIAL</h3>
                <p className="text-xs text-white/80 truncate max-w-[260px] sm:max-w-md">{currentTab.title}</p>
              </div>
              <button 
                onClick={() => setShowCreateModal(false)}
                className="p-1 rounded-full text-white/80 hover:text-white"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <form onSubmit={handleSaveCause} className="flex-1 overflow-y-auto p-4 space-y-3">
              {saveSuccess && (
                <div className="bg-emerald-50 border border-emerald-300 text-emerald-800 text-xs font-semibold p-3 rounded-xl flex items-center space-x-2">
                  <CheckCircle className="w-4 h-4 text-emerald-600 flex-shrink-0" />
                  <span>{saveSuccess}</span>
                </div>
              )}

              {saveError && (
                <div className="bg-rose-50 border border-rose-300 text-rose-800 text-xs font-semibold p-3 rounded-xl flex items-center space-x-2">
                  <AlertCircle className="w-4 h-4 text-rose-600 flex-shrink-0" />
                  <span>{saveError}</span>
                </div>
              )}

              <p className="text-[11px] text-slate-500 font-medium">
                Diligencie los campos requeridos. Si la sección <strong>CAUSAS 2026</strong> no existe en Google Sheets, se creará automáticamente formateada y centrada.
              </p>

              {currentTab.columns.map((col, idx) => {
                const isEstado = col.toUpperCase().includes('ESTADO');
                const isAbogado = col.toUpperCase().includes('ABG') || col.toUpperCase().includes('RESPONSABLE');

                return (
                  <div key={idx} className="space-y-1">
                    <label className="block text-xs font-bold text-slate-700">
                      {col}
                    </label>

                    {isEstado ? (
                      <select
                        value={formValues[idx] || 'ACTIVA'}
                        onChange={(e) => setFormValues({ ...formValues, [idx]: e.target.value })}
                        className="w-full bg-slate-50 border border-slate-300 rounded-lg p-2.5 text-xs text-slate-800 font-semibold"
                      >
                        <option value="ACTIVA">ACTIVA</option>
                        <option value="CERRADA">CERRADA</option>
                        <option value="EN TRÁMITE">EN TRÁMITE</option>
                      </select>
                    ) : isAbogado ? (
                      <select
                        value={formValues[idx] || (currentUser?.nombre || '')}
                        onChange={(e) => setFormValues({ ...formValues, [idx]: e.target.value })}
                        className="w-full bg-slate-50 border border-slate-300 rounded-lg p-2.5 text-xs text-slate-800 font-semibold"
                      >
                        {ABOGADOS_PGET.filter(a => a.activo).map(a => (
                          <option key={a.id} value={a.nombre}>{a.nombre}</option>
                        ))}
                      </select>
                    ) : (
                      <input
                        type="text"
                        value={formValues[idx] || ''}
                        onChange={(e) => setFormValues({ ...formValues, [idx]: e.target.value })}
                        placeholder={`Ingresar ${col.toLowerCase()}...`}
                        className="w-full bg-slate-50 border border-slate-300 rounded-lg p-2.5 text-xs text-slate-800 focus:outline-none focus:ring-2 focus:ring-[#6B1226]"
                      />
                    )}
                  </div>
                );
              })}

              <div className="pt-3 border-t border-slate-200 flex space-x-2">
                <button
                  type="button"
                  onClick={() => setShowCreateModal(false)}
                  className="flex-1 bg-slate-200 text-slate-700 text-xs font-bold py-2.5 rounded-lg hover:bg-slate-300 transition"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  disabled={isSaving}
                  className="flex-1 bg-[#6B1226] text-white text-xs font-bold py-2.5 rounded-lg hover:bg-[#8B1832] transition disabled:opacity-50 flex items-center justify-center space-x-1"
                >
                  {isSaving ? (
                    <>
                      <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                      <span>Sincronizando con Google Sheets...</span>
                    </>
                  ) : (
                    <span>Guardar en Google Sheets</span>
                  )}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* MODAL INICIAR SESIÓN */}
      {showLoginModal && (
        <div className="fixed inset-0 z-50 bg-black/60 flex items-center justify-center p-4">
          <div className="bg-white w-full max-w-sm rounded-2xl shadow-2xl p-5 border border-slate-200">
            <div className="text-center mb-4">
              <div className="w-12 h-12 rounded-full border-2 border-[#D4AF37] mx-auto mb-2 overflow-hidden bg-[#6B1226] p-1 flex items-center justify-center">
                <img src="/logo.png" alt="PGET" className="w-full h-full object-contain" />
              </div>
              <h3 className="text-base font-bold text-[#6B1226]">Acceso de Abogados</h3>
              <p className="text-xs text-slate-500">Procuraduría General del Estado Trujillo</p>
            </div>

            <form onSubmit={handleLogin} className="space-y-3">
              {loginError && (
                <div className="bg-rose-50 text-rose-700 border border-rose-200 p-2.5 rounded-lg text-xs font-semibold">
                  {loginError}
                </div>
              )}

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">Cédula o Correo:</label>
                <input
                  type="text"
                  value={loginId}
                  onChange={(e) => setLoginId(e.target.value)}
                  placeholder="Ej: 14.459.865 o juliobarrios@pget.com"
                  className="w-full bg-slate-50 border border-slate-300 rounded-lg p-2.5 text-xs text-slate-800 focus:outline-none focus:ring-2 focus:ring-[#6B1226]"
                  required
                />
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">Contraseña:</label>
                <input
                  type="password"
                  value={loginPass}
                  onChange={(e) => setLoginPass(e.target.value)}
                  placeholder="••••••••"
                  className="w-full bg-slate-50 border border-slate-300 rounded-lg p-2.5 text-xs text-slate-800 focus:outline-none focus:ring-2 focus:ring-[#6B1226]"
                  required
                />
              </div>

              <button
                type="submit"
                className="w-full bg-[#6B1226] text-white text-xs font-bold py-2.5 rounded-lg hover:bg-[#8B1832] transition"
              >
                Iniciar Sesión
              </button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
