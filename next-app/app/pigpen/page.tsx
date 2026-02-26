"use client";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Accordion, AccordionItem, AccordionTrigger, AccordionContent } from "@/components/ui/accordion";

import { ChevronRight, Search } from "lucide-react";

import dynamic from "next/dynamic";
const DocumentHandler = dynamic(() => import("./document-handler"), { ssr: false });
const TracePanel = dynamic(() => import("./trace-panel"), { ssr: false });


import { useEffect, useState } from "react";

const [operatorData, setOperatorData] = useState([]);

useEffect(() => {
  fetch('/api/pigpen')
    .then(res => res.json())
    .then(data => setOperatorData(data));
}, []);

const clusters = [
  "Executive & Architecture",
  "Creative Engine"
];

const phaseColors = {
  SPARK: "bg-orange-500 text-black",
  BUILD: "bg-orange-600 text-black",
  LAUNCH: "bg-blue-600 text-white",
  EXPAND: "bg-blue-800 text-white",
  EVERGREEN: "bg-neutral-700 text-white"
};

export default function PigPenPage() {
  return (
    <div className="min-h-screen bg-black text-white flex">
      {/* Sidebar */}
      <aside className="hidden md:flex flex-col w-64 bg-neutral-950 border-r border-neutral-800 p-4 gap-8">
        <nav className="flex flex-col gap-1">
          <Button variant="ghost" className="justify-start">Dashboard</Button>
          <Button variant="ghost" className="justify-start">Documentation</Button>
          <Button variant="ghost" className="justify-start">Architecture</Button>
          <Button variant="ghost" className="justify-start text-orange-500 bg-neutral-900">Pig Pen</Button>
          <Button variant="ghost" className="justify-start">Brands</Button>
          <Button variant="ghost" className="justify-start">Garvis AI</Button>
          <Button variant="ghost" className="justify-start">Glossary</Button>
          <Button variant="ghost" className="justify-start">Audit Log</Button>
          <Button variant="ghost" className="justify-start">Settings</Button>
        </nav>
      </aside>
      {/* Main Content */}
      <main className="flex-1 flex flex-col px-4 py-8 overflow-y-auto">
        <div className="flex flex-col gap-4 max-w-6xl mx-auto w-full">
          {/* Header */}
          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-2 mb-4">
            <div className="flex items-center gap-4">
              <span className="text-2xl font-bold tracking-widest text-orange-500">GARVIS // PIG PEN</span>
              <span className="text-xs text-neutral-400">v1.0.0 | Authority: AKB</span>
              <Badge className="bg-orange-500 text-black">DRAFT</Badge>
              <Badge className="bg-teal-500 text-black">OPERATIONAL</Badge>
            </div>
            <div className="flex items-center gap-2">
              <Input className="bg-neutral-900 border-neutral-700 text-white placeholder:text-neutral-500 w-80" placeholder="SEARCH OPERATORS BY NAME, ID, TITLE..." />
              <Search className="w-5 h-5 text-neutral-400 -ml-8" />
            </div>
          </div>
          {/* Stats */}
          <div className="text-xs text-neutral-400 mb-2">SHOWING 42 OF 42 OPERATORS ACROSS 12 CLUSTERS</div>
          {/* Accordion for clusters */}
          <Accordion className="w-full">
            {clusters.map(cluster => (
              <AccordionItem key={cluster} className="border-b border-neutral-800">
                <AccordionTrigger className="text-lg text-orange-400">{cluster}</AccordionTrigger>
                <AccordionContent>
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {operatorData.filter(op => op.cluster === cluster).map(op => (
                      <Card key={op.id} className="bg-neutral-950 border border-neutral-800 flex flex-col justify-between">
                        <CardHeader className="flex flex-row items-center justify-between pb-2">
                          <div>
                            <CardTitle className="text-white text-lg">{op.name}</CardTitle>
                            <div className="text-xs text-neutral-400">{op.title}</div>
                          </div>
                          <Badge className="bg-orange-500 text-black text-sm px-2 py-1 rounded-md">{op.weight}</Badge>
                        </CardHeader>
                        <CardContent className="flex flex-col gap-2">
                          <div className="text-xs text-neutral-400">Traits: ...</div>
                          <div className="flex gap-2 flex-wrap">
                            {op.phases.map(phase => (
                              <Badge key={phase} className={phaseColors[phase as keyof typeof phaseColors] + " text-xs px-2 py-1 rounded-md"}>{phase}</Badge>
                            ))}
                          </div>
                        </CardContent>
                        <div className="flex justify-end p-2">
                          <ChevronRight className="w-5 h-5 text-orange-500" />
                        </div>
                      </Card>
                    ))}
                  </div>
                </AccordionContent>
              </AccordionItem>
            ))}
          </Accordion>

          {/* Document Handler Demo */}
          <DocumentHandler />

          {/* Routing Trace Visualization */}
          <TracePanel />
        </div>
      </main>
    </div>
  );
}
