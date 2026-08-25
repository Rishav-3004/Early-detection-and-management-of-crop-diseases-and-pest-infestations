import React from 'react';
import { ProgressMeter } from '@/components/ui/ProgressMeter';
import { HelpCircle, ShieldCheck, AlertCircle } from 'lucide-react';

interface ConfidenceVisualizerProps {
  confidence: number;
  modelVersion?: string;
  isDemo?: boolean;
}

export function ConfidenceVisualizer({
  confidence,
  modelVersion,
  isDemo,
}: ConfidenceVisualizerProps) {
  const isHigh = confidence >= 0.80;
  const isMed = confidence >= 0.60 && confidence < 0.80;

  const statusText = isHigh
    ? "HIGH CONFIDENCE RESULT"
    : isMed
    ? "MEDIUM CONFIDENCE"
    : "LOW CONFIDENCE RESULT";

  const color = isHigh ? "green" : isMed ? "amber" : "red";

  return (
    <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200/80 space-y-3">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-1.5">
          <span className="text-xs font-bold text-slate-800 tracking-tight">{statusText}</span>
          <div className="group relative cursor-pointer">
            <HelpCircle className="w-3.5 h-3.5 text-slate-400 hover:text-slate-600" />
            <div className="absolute left-0 bottom-full mb-1.5 hidden group-hover:block w-64 p-2 bg-slate-900 text-white text-[10px] rounded-lg shadow-lg z-30 leading-tight">
              Confidence represents the model's estimated statistical similarity to trained foliar patterns. It does not guarantee a laboratory diagnosis.
            </div>
          </div>
        </div>
        <span className="text-sm font-extrabold text-slate-900">
          {Math.round(confidence * 100)}% Match
        </span>
      </div>

      <ProgressMeter
        value={confidence}
        maxValue={1}
        showPercentage={false}
        colorScheme={color}
      />

      <div className="flex items-center justify-between text-[10px] text-slate-500 pt-1">
        <span>Model Version: <strong className="text-slate-700">{modelVersion || 'v1.2.0-agrishield'}</strong></span>
        {isDemo && (
          <span className="font-semibold text-purple-700 bg-purple-100 px-1.5 py-0.5 rounded">
            DEMO CALIBRATED
          </span>
        )}
      </div>

      {!isHigh && (
        <div className="p-2.5 bg-amber-50 border border-amber-200 rounded-xl text-xs text-amber-800 flex items-start gap-2">
          <AlertCircle className="w-4 h-4 shrink-0 text-amber-600 mt-0.5" />
          <p className="text-[11px] leading-tight">
            Confidence is below 80%. Consider uploading a closer, well-lit photo of the symptoms or request expert agronomist verification.
          </p>
        </div>
      )}
    </div>
  );
}
