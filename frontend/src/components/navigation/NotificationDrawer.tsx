'use client';

import React from 'react';
import Link from 'next/link';
import { NotificationItem } from '@/types';
import { notificationService } from '@/services/expert';
import { formatDate } from '@/lib/utils';
import { X, CheckCheck, Bell, ShieldAlert, UserCheck, CloudRain } from 'lucide-react';

interface NotificationDrawerProps {
  isOpen: boolean;
  onClose: () => void;
  notifications: NotificationItem[];
  onRefresh: () => void;
}

export function NotificationDrawer({
  isOpen,
  onClose,
  notifications,
  onRefresh,
}: NotificationDrawerProps) {
  if (!isOpen) return null;

  const handleMarkAsRead = async (id: string) => {
    await notificationService.markAsRead(id);
    onRefresh();
  };

  const handleMarkAll = async () => {
    await notificationService.markAllAsRead();
    onRefresh();
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
    <div className="fixed inset-0 z-50 overflow-hidden">
      <div className="absolute inset-0 bg-slate-900/30 backdrop-blur-xs" onClick={onClose} />
      <div className="fixed inset-y-0 right-0 max-w-sm w-full bg-white shadow-2xl flex flex-col z-10 border-l border-slate-200">
        {/* Header */}
        <div className="p-4 border-b border-slate-100 flex items-center justify-between bg-slate-50/70">
          <div className="flex items-center gap-2">
            <Bell className="w-4 h-4 text-emerald-600" />
            <h3 className="font-semibold text-sm text-slate-800">Alerts & Notifications</h3>
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={handleMarkAll}
              className="text-xs text-emerald-700 hover:text-emerald-800 font-medium flex items-center gap-1"
              title="Mark all as read"
            >
              <CheckCheck className="w-3.5 h-3.5" />
              Mark all
            </button>
            <button onClick={onClose} className="p-1 rounded-lg hover:bg-slate-200 text-slate-500">
              <X className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Notifications List */}
        <div className="flex-1 overflow-y-auto p-4 space-y-3">
          {notifications.length === 0 ? (
            <div className="text-center py-12 text-slate-400 text-xs">
              <Bell className="w-8 h-8 mx-auto mb-2 opacity-30" />
              No notifications yet. You will be alerted when new scans or expert reviews arrive.
            </div>
          ) : (
            notifications.map((n) => (
              <div
                key={n.id}
                className={`p-3 rounded-xl border transition-all ${
                  n.is_read ? 'bg-slate-50/50 border-slate-200/60 opacity-80' : 'bg-emerald-50/30 border-emerald-200/80 shadow-xs'
                }`}
              >
                <div className="flex items-start gap-3">
                  {getIcon(n.type)}
                  <div className="flex-1 min-w-0">
                    <h4 className="text-xs font-semibold text-slate-800 leading-tight">{n.title}</h4>
                    <p className="text-xs text-slate-600 mt-1 leading-normal">{n.message}</p>
                    <div className="flex items-center justify-between mt-2 pt-2 border-t border-slate-100">
                      <span className="text-[10px] text-slate-400">{formatDate(n.created_at)}</span>
                      <div className="flex items-center gap-2">
                        {n.link && (
                          <Link
                            href={n.link}
                            onClick={onClose}
                            className="text-[11px] font-semibold text-emerald-600 hover:underline"
                          >
                            View →
                          </Link>
                        )}
                        {!n.is_read && (
                          <button
                            onClick={() => handleMarkAsRead(n.id)}
                            className="text-[10px] text-slate-400 hover:text-slate-600"
                          >
                            Mark read
                          </button>
                        )}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
