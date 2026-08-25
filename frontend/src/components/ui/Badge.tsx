import React from 'react';
import { cn, getSeverityColor, getRiskBadge } from '@/lib/utils';

interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  variant?: 'default' | 'severity' | 'risk' | 'confidence' | 'outline' | 'demo';
  severity?: string;
  riskLevel?: string;
  confidence?: number;
}

export function Badge({
  className,
  variant = 'default',
  severity,
  riskLevel,
  confidence,
  children,
  ...props
}: BadgeProps) {
  if (variant === 'severity' && severity) {
    const sev = getSeverityColor(severity);
    return (
      <span
        className={cn(
          "inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-semibold border",
          sev.badge,
          className
        )}
        {...props}
      >
        <span className={cn("w-1.5 h-1.5 rounded-full", sev.dot)} />
        {severity}
      </span>
    );
  }

  if (variant === 'risk' && riskLevel) {
    const risk = getRiskBadge(riskLevel);
    return (
      <span
        className={cn(
          "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold shadow-xs",
          risk.style,
          className
        )}
        {...props}
      >
        {risk.label}
      </span>
    );
  }

  if (variant === 'confidence' && confidence !== undefined) {
    const isHigh = confidence >= 0.80;
    const isMed = confidence >= 0.60 && confidence < 0.80;
    const style = isHigh
      ? "bg-emerald-100 text-emerald-800 border-emerald-300"
      : isMed
      ? "bg-amber-100 text-amber-800 border-amber-300"
      : "bg-red-100 text-red-800 border-red-300";

    return (
      <span
        className={cn("inline-flex items-center px-2 py-0.5 rounded-md text-xs font-bold border", style, className)}
        {...props}
      >
        {Math.round(confidence * 100)}% Match
      </span>
    );
  }

  if (variant === 'demo') {
    return (
      <span
        className={cn(
          "inline-flex items-center px-2 py-0.5 rounded-md text-[10px] uppercase tracking-wider font-bold bg-purple-100 text-purple-700 border border-purple-200",
          className
        )}
        {...props}
      >
        DEMO MODE
      </span>
    );
  }

  return (
    <span
      className={cn(
        "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-slate-100 text-slate-800",
        className
      )}
      {...props}
    >
      {children}
    </span>
  );
}
