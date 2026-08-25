'use client';

import React, { useState, useEffect } from 'react';
import { Card } from '@/components/ui/Card';
import { Loader2, CheckCircle2, Search, Sparkles, Bug, ShieldAlert, Cpu } from 'lucide-react';

interface AnalysisProgressProps {
  isAnalyzing: boolean;
}

const STAGES = [
  { id: 1, label: "Uploading image to secure storage...", icon: UploadProgressIcon },
  { id: 2, label: "Analyzing cellular image textures & pigmentation...", icon: Cpu },
  { id: 3, label: "Identifying botanical crop species...", icon: Search },
  { id: 4, label: "Scanning pathogen spore & lesion patterns...", icon: ShieldAlert },
  { id: 5, label: "Checking pest colony & insect damage markers...", icon: Bug },
  { id: 6, label: "Estimating affected leaf surface area & severity...", icon: Sparkles },
  { id: 7, label: "Synthesizing agronomic management prescriptions...", icon: CheckCircle2 },
];

function UploadProgressIcon(props: any) {
  return <Loader2 className="w-4 h-4 animate-spin text-emerald-500" {...props} />;
}

export function AnalysisProgress({ isAnalyzing }: AnalysisProgressProps) {
  const [activeStage, setActiveStage] = useState(0);

  useEffect(() => {
    if (!isAnalyzing) {
      setActiveStage(0);
      return;
    }

    // Step through deterministic states
    const interval = setInterval(() => {
      setActiveStage((prev) => {
        if (prev < STAGES.length - 1) return prev + 1;
        return prev;
      });
    }, 450);

    return () => clearInterval(interval);
  }, [isAnalyzing]);

  if (!isAnalyzing) return null;

  return (
    <Card className="p-6 bg-slate-900 text-white border border-slate-800 shadow-xl space-y-5 animate-in fade-in">
      <div className="flex items-center justify-between border-b border-slate-800 pb-3">
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-lg bg-emerald-500/20 text-emerald-400 flex items-center justify-center">
            <Cpu className="w-5 h-5 animate-pulse" />
          </div>
          <div>
            <h4 className="text-sm font-bold text-slate-100">AI Diagnostic Engine Active</h4>
            <p className="text-[11px] text-slate-400">Deterministic vision & agronomic pipeline</p>
          </div>
        </div>
        <span className="text-xs font-mono font-bold text-emerald-400">
          Step {activeStage + 1} of {STAGES.length}
        </span>
      </div>

      <div className="space-y-2.5">
        {STAGES.map((s, idx) => {
          const isDone = idx < activeStage;
          const isCurrent = idx === activeStage;
          const isPending = idx > activeStage;

          return (
            <div
              key={s.id}
              className={`flex items-center gap-3 px-3 py-2 rounded-xl text-xs transition-all duration-300 ${
                isCurrent
                  ? 'bg-emerald-950/60 border border-emerald-500/40 text-emerald-300 font-semibold shadow-inner'
                  : isDone
                  ? 'text-slate-400 opacity-80'
                  : 'text-slate-600 opacity-40'
              }`}
            >
              <div className="shrink-0">
                {isDone ? (
                  <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                ) : isCurrent ? (
                  <Loader2 className="w-4 h-4 animate-spin text-emerald-400" />
                ) : (
                  <div className="w-4 h-4 rounded-full border border-slate-700" />
                )}
              </div>
              <span className="truncate">{s.label}</span>
            </div>
          );
        })}
      </div>
    </Card>
  );
}
