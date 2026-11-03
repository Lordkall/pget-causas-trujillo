import { NextResponse } from 'next/server';
import { ABOGADOS_PGET } from '@/lib/abogadosData';

export async function GET() {
  const publicList = ABOGADOS_PGET.map(a => ({
    id: a.id,
    nombre: a.nombre,
    cedula: a.cedula,
    cargo: a.cargo,
    adscrito: a.adscrito,
    correo: a.correo,
    rol: a.rol,
    activo: a.activo,
  }));
  return NextResponse.json({ success: true, abogados: publicList });
}

export async function POST(request) {
  try {
    const { identificador, clave } = await request.json();
    if (!identificador || !clave) {
      return NextResponse.json({ success: false, error: 'Credenciales incompletas' }, { status: 400 });
    }

    const cleanId = String(identificador).trim().toUpperCase().replace(/[.\s-]/g, '');
    const cleanClave = String(clave).trim();

    const user = ABOGADOS_PGET.find(a => {
      const matchCedula = a.cedula.replace(/[.\s-]/g, '').toUpperCase() === cleanId;
      const matchCorreo = a.correo.toUpperCase() === cleanId;
      const matchNombre = a.nombre.toUpperCase().includes(cleanId);
      return (matchCedula || matchCorreo || matchNombre);
    });

    if (!user || user.clave !== cleanClave) {
      return NextResponse.json({ success: false, error: 'Cédula/correo o contraseña incorrectos' }, { status: 401 });
    }

    return NextResponse.json({
      success: true,
      user: {
        id: user.id,
        nombre: user.nombre,
        cedula: user.cedula,
        cargo: user.cargo,
        adscrito: user.adscrito,
        correo: user.correo,
        rol: user.rol,
      },
    });
  } catch (e) {
    return NextResponse.json({ success: false, error: e.message }, { status: 500 });
  }
}
