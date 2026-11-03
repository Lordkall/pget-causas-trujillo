import { NextResponse } from 'next/server';
import { PGET_TABS } from '@/lib/tabsData';

export async function GET() {
  return NextResponse.json({
    success: true,
    tabs: PGET_TABS.map(t => ({
      title: t.title,
      gid: t.gid,
      category: t.category,
      columnsCount: t.columns.length,
    })),
  });
}

