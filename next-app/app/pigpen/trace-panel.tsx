"use client";
import { useEffect, useState } from "react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";

export default function TracePanel() {
  const [traces, setTraces] = useState([]);

  useEffect(() => {
    fetch("/api/invocations/recent")
      .then(res => res.json())
      .then(data => setTraces(data));
  }, []);

  return (
    <Card className="bg-neutral-950 border border-neutral-800 mt-8">
      <CardHeader>
        <CardTitle>Routing Trace Visualization</CardTitle>
      </CardHeader>
      <CardContent className="flex flex-col gap-4">
        {traces.length === 0 ? (
          <div className="text-neutral-400">No traces found.</div>
        ) : (
          traces.map((trace, idx) => (
            <div key={idx} className="bg-neutral-900 rounded p-4 mb-2">
              <div className="text-orange-400 font-bold">Domain: {trace.domain}</div>
              <div className="text-neutral-300">Trigger: {trace.trigger}</div>
              <div className="text-neutral-300">Provider: {trace.provider}</div>
              <div className="text-neutral-300">Operator Scores:</div>
              <ul className="ml-4">
                {Object.entries(trace.operator_scores).map(([op, score]) => (
                  <li key={op} className="text-neutral-200">{op}: {score}</li>
                ))}
              </ul>
              <div className="text-neutral-300">Timeline:</div>
              <ul className="ml-4">
                {trace.timeline.map((event, i) => (
                  <li key={i} className="text-neutral-400">{event.event} @ {event.timestamp}</li>
                ))}
              </ul>
            </div>
          ))
        )}
      </CardContent>
    </Card>
  );
}
