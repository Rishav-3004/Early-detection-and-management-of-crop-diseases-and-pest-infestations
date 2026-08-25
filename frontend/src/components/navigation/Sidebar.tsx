'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useAuth } from '@/lib/auth';
import { translations } from '@/lib/i18n';
import { cn } from '@/lib/utils';
import {
  LayoutDashboard,
  Sprout,
  ScanLine,
  History,
  Bug,
  ShieldAlert,
  CloudSun,
  Bell,
  UserCheck,
  BarChart3,
  Settings,
  LogOut,
  MapPin,
  Leaf
} from 'lucide-react';

export function Sidebar() {
  const pathname = usePathname();
  const { user, logout, language } = useAuth();
  const t = translations[language] || translations.en;

  const farmerNavItems = [
    { label: t.dashboard, href: '/dashboard', icon: LayoutDashboard },
    { label: t.scanCrop, href: '/scan', icon: ScanLine, highlight: true },
    { label: t.farms, href: '/farms', icon: MapPin },
    { label: t.detections, href: '/detections', icon: History },
    { label: t.diseases, href: '/diseases', icon: ShieldAlert },
    { label: t.pests, href: '/pests', icon: Bug },
    { label: t.weather, href: '/weather', icon: CloudSun },
    { label: t.notifications, href: '/notifications', icon: Bell },
    { label: t.settings, href: '/settings', icon: Settings },
  ];

  const expertNavItems = [
    { label: t.dashboard, href: '/dashboard', icon: LayoutDashboard },
    { label: t.expertReview, href: '/expert', icon: UserCheck, highlight: true },
    { label: t.detections, href: '/detections', icon: History },
    { label: t.diseases, href: '/diseases', icon: ShieldAlert },
    { label: t.pests, href: '/pests', icon: Bug },
    { label: t.settings, href: '/settings', icon: Settings },
  ];

  const adminNavItems = [
    { label: t.dashboard, href: '/dashboard', icon: LayoutDashboard },
    { label: t.adminStudio, href: '/admin', icon: BarChart3, highlight: true },
    { label: t.expertReview, href: '/expert', icon: UserCheck },
    { label: t.detections, href: '/detections', icon: History },
    { label: t.farms, href: '/farms', icon: MapPin },
    { label: t.diseases, href: '/diseases', icon: ShieldAlert },
    { label: t.pests, href: '/pests', icon: Bug },
    { label: t.settings, href: '/settings', icon: Settings },
  ];

  let navItems = farmerNavItems;
  if (user?.role === 'EXPERT') navItems = expertNavItems;
  if (user?.role === 'ADMIN') navItems = adminNavItems;

  return (
    <aside className="w-64 bg-slate-900 text-slate-100 flex flex-col shrink-0 border-r border-slate-800 min-h-screen">
      {/* Brand Header */}
      <div className="px-6 py-5 flex items-center gap-3 border-b border-slate-800/80">
        <div className="w-9 h-9 rounded-xl bg-emerald-500 flex items-center justify-center text-slate-950 shadow-md shadow-emerald-500/20">
          <Leaf className="w-5 h-5 fill-slate-950" />
        </div>
        <div>
          <h1 className="font-bold text-sm text-white tracking-wide flex items-center gap-1.5">
            {t.appName}
          </h1>
          <p className="text-[10px] text-emerald-400 font-medium">Crop Health Intelligence</p>
        </div>
      </div>

      {/* User Role Pill */}
      {user && (
        <div className="px-5 py-3 mx-3 my-2 rounded-xl bg-slate-800/60 border border-slate-800 flex items-center justify-between">
          <div className="truncate pr-2">
            <p className="text-xs font-semibold text-slate-200 truncate">{user.name}</p>
            <p className="text-[10px] text-slate-400 truncate">{user.email}</p>
          </div>
          <span className="px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
            {user.role}
          </span>
        </div>
      )}

      {/* Navigation Links */}
      <nav className="flex-1 px-3 py-3 space-y-1 overflow-y-auto">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = pathname === item.href || pathname.startsWith(item.href + '/');

          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                "flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-xs font-medium transition-all duration-150 group",
                isActive
                  ? "bg-emerald-600 text-white shadow-sm font-semibold"
                  : item.highlight
                  ? "bg-emerald-950/40 text-emerald-300 hover:bg-emerald-900/50 border border-emerald-800/40"
                  : "text-slate-300 hover:bg-slate-800 hover:text-white"
              )}
            >
              <Icon className={cn("w-4 h-4 transition-transform group-hover:scale-110", isActive ? "text-white" : "text-slate-400 group-hover:text-emerald-400")} />
              <span>{item.label}</span>
              {item.highlight && !isActive && (
                <span className="ml-auto w-1.5 h-1.5 rounded-full bg-emerald-400 animate-ping" />
              )}
            </Link>
          );
        })}
      </nav>

      {/* Bottom Footer Action */}
      <div className="p-3 border-t border-slate-800 space-y-2">
        <button
          onClick={logout}
          className="w-full flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-xs font-medium text-slate-400 hover:bg-red-950/40 hover:text-red-300 transition-colors"
        >
          <LogOut className="w-4 h-4" />
          <span>{t.logout}</span>
        </button>
      </div>
    </aside>
  );
}
