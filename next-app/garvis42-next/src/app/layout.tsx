import './globals.css';
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import Link from 'next/link';
import { useState } from 'react';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'Garvis Command Center',
  description: 'Pig Pen Dashboard',
};

const navLinks = [
  { href: '/dashboard', label: 'Dashboard' },
  { href: '/pigpen', label: 'Pig Pen' },
  { href: '/traces', label: 'Traces' },
];

export default function RootLayout({ children }: { children: React.ReactNode }) {
  // Simple dark mode toggle (client-side only)
  // For now, just toggles a class on <body>
  // In production, consider using next-themes or similar
  return (
    <html lang="en" className="dark">
      <body className={`${inter.className} bg-black text-white min-h-screen flex`}>
        <aside className="w-56 bg-zinc-950 border-r border-zinc-800 flex flex-col justify-between min-h-screen p-6">
          <div>
            <h1 className="text-2xl font-bold text-accent mb-8">Garvis CC</h1>
            <nav className="flex flex-col gap-2">
              {navLinks.map((link) => (
                <Link
                  key={link.href}
                  href={link.href}
                  className="rounded px-3 py-2 text-white/90 hover:bg-zinc-900 hover:text-accent transition-colors font-medium"
                >
                  {link.label}
                </Link>
              ))}
            </nav>
          </div>
          <DarkModeToggle />
        </aside>
        <main className="flex-1 min-h-screen bg-black/95">{children}</main>
      </body>
    </html>
  );
}

// Simple dark mode toggle (client component)
function DarkModeToggle() {
  'use client';
  const [dark, setDark] = useState(true);
  return (
    <button
      className="mt-8 px-3 py-2 rounded bg-zinc-900 text-orange-400 hover:bg-orange-500 hover:text-white transition-colors font-semibold"
      onClick={() => {
        setDark((d) => {
          document.documentElement.classList.toggle('dark', !d);
          return !d;
        });
      }}
    >
      {dark ? '🌙 Dark Mode' : '☀️ Light Mode'}
    </button>
  );
}
