import Link from 'next/link';

export default function DashboardPage() {
  return (
    <main className="flex flex-col gap-8 p-8">
      <h1 className="text-3xl font-bold text-accent">Pig Pen Dashboard</h1>
      <div className="space-y-4">
        <p className="text-lg text-gray-300">Welcome! This is your Pig Pen operator overview.</p>
        <Link href="/pigpen" className="underline text-orange-400 hover:text-orange-300">
          View all operators
        </Link>
      </div>
    </main>
  );
}
