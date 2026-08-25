'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { useAuth } from '@/lib/auth';
import { translations, SupportedLanguage } from '@/lib/i18n';
import { notificationService, weatherService } from '@/services/expert';
import { WeatherCurrent, NotificationItem } from '@/types';
import {
  Bell,
  CloudSun,
  Globe,
  PlusCircle,
  ScanLine,
  Search,
  CheckCircle2,
  AlertTriangle
} from 'lucide-react';
import { NotificationDrawer } from './NotificationDrawer';

export function TopNavbar() {
  const { user, language, setLanguage } = useAuth();
  const [weather, setWeather] = useState<WeatherCurrent | null>(null);
  const [notifications, setNotifications] = useState<NotificationItem[]>([]);
  const [isDrawerOpen, setIsDrawerOpen] = useState(false);

  const t = translations[language] || translations.en;

  useEffect(() => {
    weatherService.getCurrentWeather().then(setWeather).catch(() => {});
    if (user) {
      notificationService.listNotifications().then(setNotifications).catch(() => {});
    }
  }, [user]);

  const unreadCount = notifications.filter(n => !n.is_read).length;

  return (
    <header className="h-16 bg-white border-b border-slate-200/80 px-6 flex items-center justify-between z-20 sticky top-0">
      {/* Search / Context */}
      <div className="flex items-center gap-4 flex-1 max-w-md">
        <div className="relative w-full">
          <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
          <input
            type="text"
            placeholder="Search crops, diseases, fields or scans..."
            className="w-full pl-9 pr-4 py-1.5 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-700 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 transition-all"
          />
        </div>
      </div>

      {/* Right Controls */}
      <div className="flex items-center gap-4">
        {/* Weather Indicator */}
        {weather && (
          <Link
            href="/weather"
            className="hidden md:flex items-center gap-2 px-3 py-1.5 bg-emerald-50 border border-emerald-200/70 rounded-xl text-xs text-emerald-900 hover:bg-emerald-100/70 transition-colors"
          >
            <CloudSun className="w-4 h-4 text-emerald-600" />
            <span className="font-semibold">{Math.round(weather.temperature)}°C</span>
            <span className="text-emerald-700 text-[11px]">• {weather.humidity}% RH</span>
            {weather.high_disease_risk_warning && (
              <span className="w-2 h-2 rounded-full bg-amber-500 animate-pulse" title="High Fungal Risk Alert" />
            )}
          </Link>
        )}

        {/* Language Selector */}
        <div className="relative flex items-center gap-1 bg-slate-100 p-1 rounded-xl border border-slate-200 text-xs">
          <Globe className="w-3.5 h-3.5 text-slate-500 ml-1.5" />
          <button
            onClick={() => setLanguage('en')}
            className={`px-2 py-0.5 rounded-lg font-semibold transition-colors ${language === 'en' ? 'bg-white shadow-xs text-emerald-700' : 'text-slate-600 hover:text-slate-900'}`}
          >
            EN
          </button>
          <button
            onClick={() => setLanguage('hi')}
            className={`px-2 py-0.5 rounded-lg font-semibold transition-colors ${language === 'hi' ? 'bg-white shadow-xs text-emerald-700' : 'text-slate-600 hover:text-slate-900'}`}
          >
            हिन्दी
          </button>
          <button
            onClick={() => setLanguage('pa')}
            className={`px-2 py-0.5 rounded-lg font-semibold transition-colors ${language === 'pa' ? 'bg-white shadow-xs text-emerald-700' : 'text-slate-600 hover:text-slate-900'}`}
          >
            ਪੰਜਾਬੀ
          </button>
        </div>

        {/* Quick Scan Action */}
        <Link
          href="/scan"
          className="hidden sm:inline-flex items-center gap-1.5 px-3.5 py-1.5 bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl text-xs font-semibold shadow-xs hover:shadow transition-all"
        >
          <ScanLine className="w-4 h-4" />
          <span>{t.scanCrop}</span>
        </Link>

        {/* Notification Bell */}
        <button
          onClick={() => setIsDrawerOpen(true)}
          className="relative p-2 rounded-xl text-slate-600 hover:bg-slate-100 hover:text-slate-900 transition-colors"
          title="View Notifications"
        >
          <Bell className="w-5 h-5" />
          {unreadCount > 0 && (
            <span className="absolute top-1.5 right-1.5 min-w-[16px] h-4 px-1 rounded-full bg-red-500 text-[10px] font-bold text-white flex items-center justify-center animate-bounce">
              {unreadCount}
            </span>
          )}
        </button>
      </div>

      {/* Notification Drawer Component */}
      <NotificationDrawer
        isOpen={isDrawerOpen}
        onClose={() => setIsDrawerOpen(false)}
        notifications={notifications}
        onRefresh={() => notificationService.listNotifications().then(setNotifications)}
      />
    </header>
  );
}
