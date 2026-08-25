import React from 'react';
import { Card } from '@/components/ui/Card';
import { Sprout, ShieldAlert, Bug, Activity, AlertTriangle, CheckCircle2 } from 'lucide-react';

interface KPICardsProps {
  totalFields: number;
  healthyFields: number;
  activeAlerts: number;
  totalScans: number;
  diseasesDetected: number;
  pestsDetected: number;
}

export function KPICards({
  totalFields = 0,
  healthyFields = 0,
  activeAlerts = 0,
  totalScans = 0,
  diseasesDetected = 0,
  pestsDetected = 0,
}: KPICardsProps) {
  const cards = [
    {
      title: "Total Fields",
      value: totalFields,
      sub: `${healthyFields} in healthy condition`,
      icon: Sprout,
      color: "text-emerald-600",
      bg: "bg-emerald-50",
      border: "border-emerald-100",
    },
    {
      title: "Total Scans",
      value: totalScans,
      sub: "AI diagnostic runs",
      icon: Activity,
      color: "text-blue-600",
      bg: "bg-blue-50",
      border: "border-blue-100",
    },
    {
      title: "Active Risk Alerts",
      value: activeAlerts,
      sub: activeAlerts > 0 ? "Requires field scout" : "All fields clear",
      icon: AlertTriangle,
      color: activeAlerts > 0 ? "text-amber-600" : "text-emerald-600",
      bg: activeAlerts > 0 ? "bg-amber-50" : "bg-emerald-50",
      border: activeAlerts > 0 ? "border-amber-100" : "border-emerald-100",
    },
    {
      title: "Diseases Detected",
      value: diseasesDetected,
      sub: "Targeted management active",
      icon: ShieldAlert,
      color: "text-red-600",
      bg: "bg-red-50",
      border: "border-red-100",
    },
    {
      title: "Pest Infestations",
      value: pestsDetected,
      sub: "Traps & bio-controls active",
      icon: Bug,
      color: "text-purple-600",
      bg: "bg-purple-50",
      border: "border-purple-100",
    },
  ];

  return (
    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
      {cards.map((c, i) => {
        const Icon = c.icon;
        return (
          <Card key={i} className={`p-4 border ${c.border} hover:border-slate-300 transition-all`}>
            <div className="flex items-center justify-between">
              <span className="text-xs font-semibold text-slate-500 tracking-tight">{c.title}</span>
              <div className={`p-2 rounded-xl ${c.bg} ${c.color}`}>
                <Icon className="w-4 h-4" />
              </div>
            </div>
            <div className="mt-3">
              <span className="text-2xl font-bold text-slate-900">{c.value}</span>
              <p className="text-[11px] text-slate-500 mt-0.5 truncate">{c.sub}</p>
            </div>
          </Card>
        );
      })}
    </div>
  );
}
