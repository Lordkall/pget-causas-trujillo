'use client';

import React, { useState, useEffect, useMemo } from 'react';
import Image from 'next/image';
import { PGET_TABS } from '@/lib/tabsData';
import { ABOGADOS_PGET } from '@/lib/abogadosData';
import { 
  Search, Plus, ShieldCheck, Scale, Calendar, Users, 
  FolderCheck, FolderClock, LogOut, Share, X, CheckCircle, 
  AlertCircle, ChevronDown, RefreshCw, Trash2, Edit3,
  Lock, Eye, EyeOff
} from 'lucide-react';

export default function HomePage() {
  const [currentUser, setCurrentUser] = useState(null);
  const [authChecked, setAuthChecked] = useState(false);
  const [loginId, setLoginId] = useState('');
  const [loginPass, setLoginPass] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [rememberMe, setRememberMe] = useState(true);
  const [loginError, setLoginError] = useState('');

  const [currentTab, setCurrentTab] = useState(PGET_TABS[0]);
  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [estadoFilter, setEstadoFilter] = useState('TODAS');
  const [yearFilter, setYearFilter] = useState('TODOS');

  // Modal Crear/Editar Causa
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [editingCause, setEditingCause] = useState(null);
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
    try {
      const saved = localStorage.getItem('pget_user');
      if (saved) {
        const parsed = JSON.parse(saved);
        if (parsed && (parsed.cedula || parsed.correo)) {
          setCurrentUser(parsed);
        }
      }
    } catch (_) {}
    setAuthChecked(true);
  }, []);

  // Cargar filas únicamente cuando el usuario esté autenticado
  useEffect(() => {
    if (currentUser) {
      fetchTabRows(currentTab.title);
    }
  }, [currentTab, currentUser]);

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
    const rawInput = loginId.trim();
    if (!rawInput) {
      setLoginError('Por favor ingrese su Cédula o Correo');
      return;
    }
    if (!loginPass.trim()) {
      setLoginError('Por favor ingrese su Contraseña');
      return;
    }

    const cleanId = rawInput.toUpperCase().replace(/^V-?/, '').replace(/[.\s-]/g, '');
    const cleanPass = loginPass.trim();

    const user = ABOGADOS_PGET.find(a => {
      const matchCedula = a.cedula.replace(/[.\s-]/g, '').toUpperCase() === cleanId;
      const matchCorreo = a.correo.trim().toUpperCase() === rawInput.toUpperCase();
      const matchNombre = a.nombre.toUpperCase().includes(cleanId);
      return (matchCedula || matchCorreo || matchNombre);
    });

    if (!user) {
      setLoginError('Cédula o correo no registrado.');
      return;
    }

    // Permitir clave oficial y alias intuitivos (ej: Maria Barrios acepta tanto Pget2026*Maria como Pget2026*MariaB)
    const isPassValid = (user.clave === cleanPass) ||
      (user.correo === 'mariabarrios@pget.com' && (cleanPass === 'Pget2026*Maria' || cleanPass === 'Pget2026*MariaB')) ||
      (user.correo === 'mariaojeda@pget.com' && (cleanPass === 'Pget2026*MariaO' || cleanPass === 'Pget2026*Maria'));

    if (!isPassValid) {
      setLoginError('Contraseña incorrecta. Verifique sus datos.');
      return;
    }

    setCurrentUser(user);
    if (rememberMe) {
      localStorage.setItem('pget_user', JSON.stringify(user));
    } else {
      localStorage.removeItem('pget_user');
    }
    setLoginPass('');
    setLoginError('');
  }

  function handleLogout() {
    localStorage.removeItem('pget_user');
    setCurrentUser(null);
    setLoginPass('');
    setLoginError('');
  }

  // Guardar o Actualizar causa
  async function handleSaveCause(e) {
    e.preventDefault();
    setIsSaving(true);
    setSaveError('');
    setSaveSuccess('');

    try {
      const rowValues = currentTab.columns.map((col, idx) => {
        return formValues[idx] !== undefined ? String(formValues[idx]) : '';
      });

      if (editingCause) {
        // Actualizar causa existente
        const res = await fetch('/api/causas', {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            tabTitle: currentTab.title,
            rowIndex: currentTab.headerRow + 1 + editingCause.index,
            expediente: editingCause.originalExp,
            rowValues,
          }),
        });

        const data = await res.json();
        if (!data.success) throw new Error(data.error || 'Error al actualizar');
        setSaveSuccess('¡Causa actualizada con éxito en Google Sheets!');
      } else {
        // Crear nueva causa
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
        if (!data.success) throw new Error(data.error || 'Error al guardar');
        setSaveSuccess(`¡Causa registrada con éxito en ${currentTab.title}!`);
      }

      await fetchTabRows(currentTab.title);
      setTimeout(() => {
        setShowCreateModal(false);
        setEditingCause(null);
        setFormValues({});
        setSaveSuccess('');
      }, 1200);
    } catch (err) {
      setSaveError(err.message);
    } finally {
      setIsSaving(false);
    }
  }

  function handleOpenEdit(row, index, exp) {
    const init = {};
    currentTab.columns.forEach((col, cIdx) => {
      init[cIdx] = row[cIdx] || '';
    });
    setFormValues(init);
    setEditingCause({ row, index, originalExp: exp });
    setShowCreateModal(true);
  }

  // Eliminar causa físicamente
  async function handleDeleteCause() {
    if (!editingCause) return;
    const expText = editingCause.originalExp ? `del expediente ${editingCause.originalExp}` : 'seleccionada';
    if (!window.confirm(`¿Estás seguro de que deseas eliminar permanentemente de Google Sheets la causa ${expText}?`)) {
      return;
    }

    setIsSaving(true);
    setSaveError('');
    try {
      const exp = encodeURIComponent(editingCause.originalExp || '');
      const res = await fetch(`/api/causas?tab=${encodeURIComponent(currentTab.title)}&expediente=${exp}`, {
        method: 'DELETE',
      });
      const data = await res.json();
      if (!data.success) throw new Error(data.error || 'Error al eliminar');

      setSaveSuccess('¡Causa eliminada físicamente de Google Sheets!');
      await fetchTabRows(currentTab.title);
      setTimeout(() => {
        setShowCreateModal(false);
        setEditingCause(null);
        setFormValues({});
        setSaveSuccess('');
      }, 1000);
    } catch (err) {
      setSaveError(err.message);
    } finally {
      setIsSaving(false);
    }
  }

  // Eliminar causa directamente desde la tarjeta principal
  async function handleDirectDelete(row, index, exp) {
    const expText = exp ? `con Expediente "${exp}"` : `de la fila #${index + 1}`;
    if (!window.confirm(`¿Estás seguro de que deseas eliminar permanentemente de Google Sheets la causa ${expText}?\n\nEsta acción eliminará la fila directamente en la hoja de cálculo.`)) {
      return;
    }

    setLoading(true);
    try {
      const expParam = encodeURIComponent(exp || '');
      const res = await fetch(`/api/causas?tab=${encodeURIComponent(currentTab.title)}&expediente=${expParam}`, {
        method: 'DELETE',
      });
      const data = await res.json();
      if (!data.success) throw new Error(data.error || 'Error al eliminar');

      await fetchTabRows(currentTab.title);
      alert(`¡Causa ${expText} eliminada exitosamente de Google Sheets!`);
    } catch (err) {
      alert(`Error al eliminar: ${err.message}`);
    } finally {
      setLoading(false);
    }
  }

  // 1. Pantalla de carga mientras se verifica el estado de sesión local
  if (!authChecked) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-[#4A0C1A] via-[#6B1226] to-[#2B0710] flex flex-col items-center justify-center p-4 text-white">
        <div className="relative mb-4">
          <div className="w-20 h-20 rounded-full border-2 border-[#D4AF37] p-2 bg-white/10 backdrop-blur shadow-2xl flex items-center justify-center animate-pulse">
            <img src="/logo.png" alt="Escudo PGET" className="w-16 h-16 object-contain drop-shadow" />
          </div>
        </div>
        <div className="text-center">
          <h2 className="text-sm font-bold tracking-widest text-[#D4AF37] uppercase">
            Procuraduría General del Estado Trujillo
          </h2>
          <p className="text-xs text-white/70 mt-1">Verificando acceso institucional...</p>
        </div>
      </div>
    );
  }

  // 2. Pantalla de LOGIN OBLIGATORIO (si no hay sesión activa)
  if (!currentUser) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-[#3D0A15] via-[#6B1226] to-[#26050C] flex flex-col justify-between p-4 sm:p-6 text-white selection:bg-[#D4AF37] selection:text-[#6B1226]">
        {/* Banner instalación iPhone si aplica */}
        {showIosPrompt && (
          <div className="max-w-md mx-auto w-full mb-3 bg-amber-400 text-amber-950 px-3.5 py-2 rounded-xl text-xs flex items-center justify-between shadow-lg">
            <div className="flex items-center space-x-2">
              <Share className="w-4 h-4 flex-shrink-0" />
              <span>
                <strong>iPhone:</strong> Toca Compartir y luego <strong>"Agregar al inicio"</strong>.
              </span>
            </div>
            <button onClick={() => setShowIosPrompt(false)} className="p-1 hover:opacity-70">
              <X className="w-4 h-4" />
            </button>
          </div>
        )}

        <div className="flex-1 flex items-center justify-center py-6">
          <div className="w-full max-w-md bg-white text-slate-900 rounded-3xl shadow-2xl border border-[#D4AF37]/40 overflow-hidden">
            {/* Cabecera de la tarjeta con estilo Vinotinto Institucional */}
            <div className="bg-gradient-to-b from-[#6B1226] to-[#4A0C1A] text-white px-6 pt-7 pb-6 text-center border-b-2 border-[#D4AF37] relative">
              <div className="w-20 h-20 rounded-full border-2 border-[#D4AF37] mx-auto mb-3 bg-white/10 p-2 shadow-lg flex items-center justify-center">
                <img src="/logo.png" alt="Escudo PGET" className="w-16 h-16 object-contain drop-shadow" />
              </div>
              <p className="text-[10px] tracking-widest uppercase font-semibold text-[#D4AF37]/90 mb-0.5">
                República Bolivariana de Venezuela
              </p>
              <h1 className="text-base font-extrabold tracking-wide text-white leading-tight">
                PROCURADURÍA GENERAL
              </h1>
              <p className="text-xs font-semibold text-[#D4AF37] tracking-wider uppercase">
                Estado Trujillo
              </p>
              <div className="mt-2 inline-block bg-[#2E0710]/80 border border-[#D4AF37]/40 text-[#F4D068] text-[11px] font-medium px-3 py-0.5 rounded-full">
                Control de Causas Judiciales
              </div>
            </div>

            {/* Formulario de Login */}
            <div className="p-6 sm:p-7">
              <div className="mb-5 text-center">
                <h2 className="text-base font-bold text-[#6B1226]">Acceso de Abogados</h2>
                <p className="text-xs text-slate-500 mt-0.5">
                  Ingrese sus credenciales oficiales para gestionar expedientes
                </p>
              </div>

              {loginError && (
                <div className="mb-4 bg-red-50 border border-red-200 text-red-800 p-3 rounded-xl text-xs font-medium flex items-start space-x-2">
                  <AlertCircle className="w-4 h-4 text-red-600 flex-shrink-0 mt-0.5" />
                  <span>{loginError}</span>
                </div>
              )}

              <form onSubmit={handleLogin} className="space-y-4">
                <div>
                  <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">
                    Cédula o Correo Institucional
                  </label>
                  <div className="relative">
                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-400">
                      <Users className="w-4 h-4" />
                    </div>
                    <input
                      type="text"
                      value={loginId}
                      onChange={(e) => setLoginId(e.target.value)}
                      placeholder="Ej: 14.459.865 o juliobarrios@pget.com"
                      autoComplete="username"
                      required
                      className="w-full pl-9 pr-3 py-2.5 bg-slate-50 border border-slate-300 rounded-xl text-xs text-slate-900 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-[#6B1226] focus:border-[#6B1226] transition font-medium"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">
                    Contraseña
                  </label>
                  <div className="relative">
                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-400">
                      <Lock className="w-4 h-4" />
                    </div>
                    <input
                      type={showPassword ? 'text' : 'password'}
                      value={loginPass}
                      onChange={(e) => setLoginPass(e.target.value)}
                      placeholder="••••••••"
                      autoComplete="current-password"
                      required
                      className="w-full pl-9 pr-10 py-2.5 bg-slate-50 border border-slate-300 rounded-xl text-xs text-slate-900 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-[#6B1226] focus:border-[#6B1226] transition font-medium"
                    />
                    <button
                      type="button"
                      onClick={() => setShowPassword(!showPassword)}
                      className="absolute inset-y-0 right-0 pr-3 flex items-center text-slate-400 hover:text-slate-600 transition"
                      tabIndex={-1}
                    >
                      {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                    </button>
                  </div>
                </div>

                <div className="flex items-center justify-between text-xs pt-1">
                  <label className="flex items-center space-x-2 text-slate-600 cursor-pointer select-none">
                    <input
                      type="checkbox"
                      checked={rememberMe}
                      onChange={(e) => setRememberMe(e.target.checked)}
                      className="w-4 h-4 rounded text-[#6B1226] focus:ring-[#6B1226] border-slate-300 cursor-pointer"
                    />
                    <span>Recordar sesión</span>
                  </label>
                  <span className="text-[11px] text-slate-400">
                    PGET v2.0
                  </span>
                </div>

                <button
                  type="submit"
                  className="w-full mt-2 bg-gradient-to-r from-[#6B1226] to-[#8B1832] hover:from-[#540D1E] hover:to-[#6B1226] text-white text-xs font-bold py-3 rounded-xl shadow-lg shadow-[#6B1226]/30 border border-[#D4AF37]/50 hover:border-[#D4AF37] transition flex items-center justify-center space-x-2 cursor-pointer"
                >
                  <ShieldCheck className="w-4 h-4 text-[#D4AF37]" />
                  <span>INGRESAR AL SISTEMA</span>
                </button>
              </form>

              <div className="mt-6 pt-4 border-t border-slate-100 text-center">
                <p className="text-[11px] text-slate-400 leading-relaxed">
                  🔒 Acceso exclusivo para el personal letrado adscrito a la Procuraduría General del Estado Trujillo.
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Footer institucional */}
        <div className="text-center text-[11px] text-white/60 py-2">
          © {new Date().getFullYear()} Procuraduría General del Estado Trujillo • Plataforma Oficial de Control Judicial
        </div>
      </div>
    );
  }

  // 3. Panel Principal de Causas (Únicamente accesible tras autenticación exitosa)
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
            <div className="flex items-center space-x-2">
              <span className="text-xs bg-[#4A0C1A] text-[#D4AF37] font-semibold px-2.5 py-1 rounded-full border border-[#D4AF37]/50 max-w-[140px] truncate sm:max-w-none">
                {currentUser.nombre.split(' ')[0]} {currentUser.rol === 'admin' ? '(ADMIN)' : ''}
              </span>
              <button 
                onClick={handleLogout}
                title="Cerrar sesión"
                className="flex items-center space-x-1 text-xs bg-black/20 hover:bg-black/40 text-white/90 px-2.5 py-1 rounded-lg border border-white/10 transition"
              >
                <LogOut className="w-3.5 h-3.5" />
                <span className="hidden sm:inline">Cerrar Sesión</span>
              </button>
            </div>
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
                  onClick={() => handleOpenEdit(row, index, exp)}
                  className="bg-white rounded-xl p-3.5 shadow-sm border border-slate-200 hover:border-[#D4AF37] cursor-pointer hover:shadow-md transition group"
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

                    <div className="flex items-center space-x-1.5">
                      <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                        estado.includes('ACTIV') 
                          ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' 
                          : estado.includes('CERRAD') 
                          ? 'bg-slate-100 text-slate-700 border border-slate-300' 
                          : 'bg-amber-50 text-amber-700 border border-amber-200'
                      }`}>
                        {estado}
                      </span>
                      <span className="p-1 rounded-md text-slate-400 group-hover:text-[#6B1226] group-hover:bg-amber-50 transition">
                        <Edit3 className="w-3.5 h-3.5" />
                      </span>
                    </div>
                  </div>

                  <h3 className="text-sm font-bold text-slate-900 leading-snug mb-1">
                    {motivo}
                  </h3>

                  {contra && (
                    <p className="text-xs text-slate-600 mb-2">
                      <span className="font-semibold text-slate-500">Contra:</span> {contra}
                    </p>
                  )}

                  <div className="pt-2.5 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500 gap-2">
                    <div className="flex items-center space-x-1 truncate max-w-[180px] sm:max-w-[260px]">
                      <Users className="w-3.5 h-3.5 text-[#D4AF37] flex-shrink-0" />
                      <span className="truncate">{abg}</span>
                    </div>
                    <div className="flex items-center space-x-1.5 flex-shrink-0">
                      <button
                        type="button"
                        onClick={(e) => {
                          e.stopPropagation();
                          handleOpenEdit(row, index, exp);
                        }}
                        className="text-[11px] font-bold text-[#6B1226] bg-[#6B1226]/5 hover:bg-[#6B1226]/15 px-2.5 py-1 rounded-lg border border-[#6B1226]/20 flex items-center space-x-1 transition"
                      >
                        <Edit3 className="w-3.5 h-3.5" />
                        <span>Editar</span>
                      </button>
                      <button
                        type="button"
                        onClick={(e) => {
                          e.stopPropagation();
                          handleDirectDelete(row, index, exp);
                        }}
                        className="text-[11px] font-bold text-red-600 bg-red-50 hover:bg-red-600 hover:text-white px-2.5 py-1 rounded-lg border border-red-200 hover:border-red-600 flex items-center space-x-1 transition shadow-xs"
                      >
                        <Trash2 className="w-3.5 h-3.5" />
                        <span>Eliminar</span>
                      </button>
                    </div>
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
                <h3 className="text-sm font-bold text-[#D4AF37]">
                  {editingCause ? `EDITAR EXPEDIENTE ${editingCause.originalExp || ''}` : 'NUEVA CAUSA JUDICIAL'}
                </h3>
                <p className="text-xs text-white/80 truncate max-w-[260px] sm:max-w-md">{currentTab.title}</p>
              </div>
              <button 
                onClick={() => {
                  setShowCreateModal(false);
                  setEditingCause(null);
                }}
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

              <div className="pt-3 border-t border-slate-200 flex items-center justify-between gap-2">
                {editingCause && (
                  <button
                    type="button"
                    onClick={handleDeleteCause}
                    disabled={isSaving}
                    title="Eliminar causa permanentemente de Google Sheets"
                    className="bg-red-50 hover:bg-red-600 text-red-700 hover:text-white border border-red-200 hover:border-red-600 text-xs font-bold py-2.5 px-3.5 rounded-lg transition flex items-center space-x-1.5 disabled:opacity-50 flex-shrink-0"
                  >
                    <Trash2 className="w-4 h-4" />
                    <span>Eliminar</span>
                  </button>
                )}
                <div className="flex items-center space-x-2 flex-1 justify-end">
                  <button
                    type="button"
                    onClick={() => {
                      setShowCreateModal(false);
                      setEditingCause(null);
                    }}
                    className="bg-slate-200 text-slate-700 text-xs font-bold py-2.5 px-4 rounded-lg hover:bg-slate-300 transition"
                  >
                    Cancelar
                  </button>
                  <button
                    type="submit"
                    disabled={isSaving}
                    className="flex-1 max-w-[220px] bg-[#6B1226] text-white text-xs font-bold py-2.5 px-4 rounded-lg hover:bg-[#8B1832] transition disabled:opacity-50 flex items-center justify-center space-x-1"
                  >
                    {isSaving ? (
                      <>
                        <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                        <span>Guardando...</span>
                      </>
                    ) : (
                      <span>{editingCause ? 'Guardar Cambios' : 'Guardar en Sheets'}</span>
                    )}
                  </button>
                </div>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

