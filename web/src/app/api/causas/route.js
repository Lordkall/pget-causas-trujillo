import { NextResponse } from 'next/server';
import { PGET_TABS } from '@/lib/tabsData';
import { getRowsForTab, insertRowForTab } from '@/lib/sheets';

export async function GET(request) {
  try {
    const { searchParams } = new URL(request.url);
    const tabTitle = searchParams.get('tab') || 'JUZGADOS DE MUNICIPIOS ORDINARI';
    
    const tab = PGET_TABS.find(t => t.title.toUpperCase() === tabTitle.toUpperCase()) || PGET_TABS[0];
    const rows = await getRowsForTab(tab.title, tab.headerRow);

    return NextResponse.json({
      success: true,
      tab: tab.title,
      headerRow: tab.headerRow,
      columns: tab.columns,
      total: rows.length,
      rows,
    });
  } catch (error) {
    console.error('Error fetching tab rows:', error);
    return NextResponse.json(
      { success: false, error: error.message || 'Error al obtener causas de Google Sheets' },
      { status: 500 }
    );
  }
}

export async function POST(request) {
  try {
    const body = await request.json();
    const { tabTitle, rowValues, targetYear } = body;

    if (!tabTitle || !rowValues || !Array.isArray(rowValues)) {
      return NextResponse.json(
        { success: false, error: 'Parámetros inválidos (tabTitle y rowValues requeridos)' },
        { status: 400 }
      );
    }

    const tab = PGET_TABS.find(t => t.title.toUpperCase() === tabTitle.toUpperCase());
    if (!tab) {
      return NextResponse.json(
        { success: false, error: `Pestaña "${tabTitle}" no encontrada` },
        { status: 404 }
      );
    }

    const year = targetYear || 2026;
    const result = await insertRowForTab(tab, rowValues, year);

    return NextResponse.json({
      success: true,
      message: `Causa registrada exitosamente en ${tab.title}`,
      result,
    });
  } catch (error) {
    console.error('Error inserting row:', error);
    return NextResponse.json(
      { success: false, error: error.message || 'Error al guardar causa en Google Sheets' },
      { status: 500 }
    );
  }
}
