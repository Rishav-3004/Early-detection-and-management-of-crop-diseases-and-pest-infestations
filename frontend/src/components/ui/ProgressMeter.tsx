import React from 'react';
import { cn } from '@/lib/utils';

interface ProgressMeterProps {
  value: number; // 0 to 1 or 0 to 100
  maxValue?: number;
  label?: string;
  subLabel?: string;
  showPercentage?: boolean;
  colorScheme?: 'green' | 'amber' | 'red' | 'blue' | 'gradient';
  className?: string;
  tooltipText?: string;
}

export function ProgressMeter({
  value,
  maxValue = 100,
  label,
  subLabel,
  showPercentage = true,
  colorScheme = 'gradient',
  className,
  tooltipText,
}: ProgressMeterProps) {
  // Normalize percentage
  const pct = maxValue === 1 ? Math.min(100, Math.max(0, value * 100)) : Math.min(100, Math.max(0, (value / maxValue) * 100));

  const colors = {
    green: 'bg-emerald-500',
    amber: 'bg-amber-500',
    red: 'bg-red-500',
    blue: 'bg-blue-500',
    gradient: pct >= 80 ? 'bg-emerald-500' : pct >= 60 ? 'bg-amber-500' : 'bg-red-500',
  };

  return (
    <div className={cn("w-full space-y-1.5", className)} title={tooltipText}>
      {(label || showPercentage) && (
        <div className="flex justify-between items-center text-xs">
          {label && <span className="font-semibold text-slate-700">{label}</span>}
          {showPercentage && (
            <span className="font-bold text-slate-900">
              {Math.round(pct)}%
            </span>
          )}
        </div>
      )}
      <div className="w-full h-2.5 bg-slate-100 rounded-full overflow-hidden p-0.5 border border-slate-200/50">
        <div
          className={cn("h-full rounded-full transition-all duration-700 ease-out", colors[colorScheme])}
          style={{ width: `${pct}%` }}
        />
      </div>
      {subLabel && <p className="text-[11px] text-slate-500 leading-tight">{subLabel}</p>}
    </div>
  );
}
