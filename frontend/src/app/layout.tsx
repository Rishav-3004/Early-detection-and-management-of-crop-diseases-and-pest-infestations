'use client';

import React from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { AuthProvider, useAuth } from '@/lib/auth';
import { Sidebar } from '@/components/navigation/Sidebar';
import { TopNavbar } from '@/components/navigation/TopNavbar';
import { usePathname } from 'next/navigation';
import './globals.css';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const isAuthPage = pathname.startsWith('/login') || pathname.startsWith('/register');

  if (isAuthPage) {
    return <main className="min-h-screen bg-slate-950 flex flex-col">{children}</main>;
  }

  return (
    <div className="flex min-h-screen bg-[#f8faf8]">
      <Sidebar />
      <div className="flex-1 flex flex-col min-w-0">
        <TopNavbar />
        <main className="flex-1 p-6 md:p-8 max-w-7xl w-full mx-auto">{children}</main>
      </div>
    </div>
  );
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <head>
        <title>AgriShield AI - Early Detection of Crop Diseases & Pest Infestations</title>
        <meta
          name="description"
          content="Early detection and actionable agronomic management of crop diseases and pest infestations with multi-factor risk assessment."
        />
      </head>
      <body>
        <QueryClientProvider client={queryClient}>
          <AuthProvider>
            <AppShell>{children}</AppShell>
          </AuthProvider>
        </QueryClientProvider>
      </body>
    </html>
  );
}
