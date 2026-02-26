import { NextResponse } from 'next/server';
import clientPromise from '@/lib/mongodb';
import { v4 as uuidv4 } from 'uuid';
import { completion } from 'litellm';

export async function POST(request: Request) {
  const body = await request.json();
  const { parent_operator_id, task_description, max_subagents = 5, max_depth = 3, current_depth = 0 } = body;

  try {
    const client = await clientPromise;
    const db = client.db('garvisdb');

    // Fetch parent operator
    const parent = await db.collection('pigpen_operators').findOne({ tai_d: parent_operator_id });
    if (!parent || !parent.can_spawn) {
      return NextResponse.json({ error: 'Parent operator not found or cannot spawn' }, { status: 403 });
    }

    // LLM decomposition
    const response = await completion({
      model: 'anthropic/claude-3-5-sonnet-20241022',
      messages: [
        { role: 'system', content: `You are ${parent.name}. Decompose task: "${task_description}" into subagents from registry.` },
        { role: 'user', content: task_description }
      ],
    });

    const decomposition = JSON.parse(response.choices[0].message.content);
    const subagents = decomposition.subagents || [];

    // Queue task
    const taskId = uuidv4();
    const task = {
      task_id: taskId,
      parent_operator_id,
      task_description,
      subagents,
      status: subagents.some((s: any) => s.requires_approval) ? 'pending_approval' : 'queued',
      current_depth: current_depth + 1,
      created_at: new Date().toISOString(),
    };

    await db.collection('tasks').insertOne(task);

    // Audit log
    await db.collection('audit_log').insertOne({
      event_type: 'subagent_spawn',
      task_id: taskId,
      timestamp: new Date().toISOString(),
      details: { subagent_count: subagents.length },
    });

    return NextResponse.json({
      task_id: taskId,
      parent_operator_id,
      subagents,
      status: task.status,
    });
  } catch (e) {
    console.error(e);
    return NextResponse.json({ error: 'Spawn failed' }, { status: 500 });
  }
}
