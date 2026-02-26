"use client";
import { Card, CardHeader, CardTitle, CardContent } from "@/src/components/ui/card";
import { Button } from "@/src/components/ui/button";
import { Badge } from "@/src/components/ui/badge";
import { Progress } from "@/src/components/ui/progress";
import { Home, User, FileText, Plus, RefreshCw } from "lucide-react";

export default function HomePage() {
  return (
    <div className="min-h-screen bg-black text-white flex flex-col">
      {/* Top Bar */}
      <header className="flex items-center justify-between px-6 py-4 border-b border-neutral-800 bg-black">
        <div className="flex items-center gap-4">
          <span className="text-2xl font-bold tracking-widest text-orange-500">GARVIS</span>
        </div>
        <div className="flex items-center gap-2">
          <Badge className="bg-green-600 text-white px-3 py-1 rounded-full">AKB 100%</Badge>
          <Button variant="ghost" className="text-orange-500">AKB Builder</Button>
          <Button variant="ghost">Profile</Button>
          <Button variant="ghost">Artifacts</Button>
        </div>
      </header>
      <div className="flex flex-1 overflow-hidden">
        {/* Sidebar */}
        <aside className="hidden md:flex flex-col w-64 bg-neutral-950 border-r border-neutral-800 p-4 gap-8">
          <div>
            <div className="text-xs text-neutral-400 mb-2">PROJECTS</div>
            <nav className="flex flex-col gap-1">
              <Button variant="ghost" className="justify-start text-orange-500 bg-neutral-900">Home Canonical</Button>
              <Button variant="ghost" className="justify-start">My Business</Button>
              <Button variant="ghost" className="justify-start text-orange-500"><Plus className="w-4 h-4 mr-2" /> New Project</Button>
            </nav>
          </div>
          <div>
            <div className="text-xs text-neutral-400 mb-2">SESSIONS</div>
            <nav className="flex flex-col gap-1">
              <Button variant="ghost" className="justify-start text-orange-500"><Plus className="w-4 h-4 mr-2" /> New Session</Button>
              <Button variant="ghost" className="justify-start">goGarvis: Build mode...</Button>
              <Button variant="ghost" className="justify-start">goGarvis: Review mode...</Button>
            </nav>
          </div>
        </aside>
        {/* Main Content */}
        <main className="flex-1 flex flex-col items-center justify-center px-4 py-8 overflow-y-auto">
          <div className="flex flex-col items-center gap-6 w-full max-w-xl">
            <h1 className="text-5xl font-extrabold tracking-tight text-orange-500 mb-2">goGARVIS</h1>
            <p className="text-lg text-neutral-300 mb-4">Project in progress. Keep building momentum.</p>
            <Button className="bg-orange-500 text-black text-lg px-8 py-4 rounded-xl font-bold hover:bg-orange-600 transition">▶ Advance Active Project</Button>
            {/* Recent Uploads Card */}
            <Card className="w-full bg-neutral-900 border border-neutral-800 mt-8">
              <CardHeader>
                <CardTitle className="text-orange-500">Recent uploads</CardTitle>
              </CardHeader>
              <CardContent className="flex flex-col items-center gap-2 py-8">
                <div className="text-neutral-400 mb-2">No uploads yet.</div>
                <Button variant="outline" className="border-orange-500 text-orange-500 hover:bg-orange-500 hover:text-black"><RefreshCw className="w-4 h-4 mr-2" />Refresh</Button>
              </CardContent>
            </Card>
            {/* Bottom Buttons */}
            <div className="flex gap-4 mt-8">
              <Button className="bg-orange-500 text-black font-bold">Create Artifact</Button>
              <Button variant="outline" className="border-orange-500 text-orange-500 hover:bg-orange-500 hover:text-black">Upload More</Button>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
