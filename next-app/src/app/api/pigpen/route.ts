import clientPromise from '@/lib/mongodb';
import { NextResponse } from 'next/server';

export async function GET() {
  try {
    const client = await clientPromise;
    const db = client.db('garvisdb');
    const operators = await db.collection('pigpen_operators')
      .find({ is_active: true })
      .toArray();
    return NextResponse.json(operators);
  } catch (e) {
    console.error(e);
    return NextResponse.json({ error: 'Failed to fetch operators' }, { status: 500 });
  }
}
