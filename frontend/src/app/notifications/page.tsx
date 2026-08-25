'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { useAuth } from '@/lib/auth';
import { notificationService } from '@/services/expert';
import { NotificationItem } from '@/types';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { formatDate } from '@/lib/utils';
import { Bell, CheckCheck, ShieldAlert, UserCheck, CloudRain, ExternalLink } from 'lucide-react';

export default function NotificationsPage() {
  const { user } = useAuth();
  const [notifications, setNotifications] = useState<NotificationItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  const loadNotifs = async () => {
    setIsLoading(true);
    try {
      const list = await notificationService.listNotifications();
      setNotifications(list);
    } catch (e) {
      console.error(e);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadNotifs();
  }, [user]);

  const handleMarkAsRead = async (id: string) => {
    await notificationService.markAsRead(id);
    loadNotifs();
  };

  const handleMarkAll = async () => {
    await notificationService.markAllAsRead();
    loadNotifs();
  };

  const getIcon = (type: string) => {
    switch (type) {
      case 'HIGH_RISK':
        return <ShieldAlert className="w-5 h-5 text-red-500 shrink-0" />;
      case 'EXPERT_REVIEW':
        return <UserCheck className="w-5 h-5 text-emerald-600 shrink-0" />;
      case 'WEATHER_ALERT':
        return <CloudRain className="w-5 h-5 text-blue-500 shrink-0" />;
      default:
        return <Bell className="w-5 h-5 text-slate-500 shrink-0" />;
    }
  };

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="p-2 rounded-xl bg-amber-100 text-amber-800">
              <Bell className="w-5 h-5" />
            </span>
            <h1 className="text-xl md:text-2xl font-extrabold text-slate-900 tracking-tight">
              Crop Health Alerts & Notifications
            </h1>
          </div>
          <p className="text-xs text-slate-500 mt-1">
            Real-time critical alerts, agronomist verification notices, and microclimate risk updates.
          </p>
        </div>

        <Button
          variant="outline"
          size="sm"
          onClick={handleMarkAll}
          leftIcon={<CheckCheck className="w-4 h-4 text-emerald-600" />}
        >
          Mark All Read
        </Button>
      </div>

      <Card className="divide-y divide-slate-100 overflow-hidden">
        {isLoading ? (
          <div className="py-16 text-center text-slate-400 text-xs">
            <div className="w-6 h-6 border-2 border-emerald-500 border-t-transparent rounded-full animate-spin mx-auto mb-2" />
            Loading alerts...
          </div>
        ) : notifications.length === 0 ? (
          <div className="py-16 text-center text-slate-400 text-xs space-y-2">
            <Bell className="w-8 h-8 mx-auto opacity-30" />
            <p>No notifications at this time.</p>
          </div>
        ) : (
          notifications.map((n) => (
            <div
              key={n.id}
              className={`p-4 flex items-start gap-4 transition-colors ${
                n.is_read ? 'bg-white hover:bg-slate-50/60' : 'bg-emerald-50/40 hover:bg-emerald-50/70'
              }`}
            >
              <div className="mt-0.5">{getIcon(n.type)}</div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center justify-between gap-2">
                  <h4 className="text-xs font-bold text-slate-900">{n.title}</h4>
                  <span className="text-[10px] text-slate-400 shrink-0">{formatDate(n.created_at)}</span>
                </div>
                <p className="text-xs text-slate-600 mt-1 leading-relaxed">{n.message}</p>
                <div className="flex items-center gap-3 mt-2.5">
                  {n.link && (
                    <Link
                      href={n.link}
                      className="text-xs font-bold text-emerald-600 hover:text-emerald-700 inline-flex items-center gap-1"
                    >
                      Open Case <ExternalLink className="w-3 h-3" />
                    </Link>
                  )}
                  {!n.is_read && (
                    <button
                      onClick={() => handleMarkAsRead(n.id)}
                      className="text-[11px] text-slate-400 hover:text-slate-700 underline"
                    >
                      Mark as read
                    </button>
                  )}
                </div>
              </div>
            </div>
          ))
        )}
      </Card>
    </div>
  );
}
