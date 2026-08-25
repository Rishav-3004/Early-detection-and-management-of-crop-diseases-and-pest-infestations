import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card';
import { DetectionResultCandidate } from '@/types';
import { Layers } from 'lucide-react';

interface MultiRankCandidatesProps {
  candidates: DetectionResultCandidate[];
}

export function MultiRankCandidates({ candidates = [] }: MultiRankCandidatesProps) {
  if (candidates.length <= 1) return null;

  return (
    <Card className="border border-slate-200">
      <CardHeader className="py-3 px-4">
        <div className="flex items-center gap-2">
          <Layers className="w-4 h-4 text-emerald-600" />
          <CardTitle className="text-sm">Differential Diagnostic Candidates</CardTitle>
        </div>
        <span className="text-[10px] text-slate-400">Ranked by AI probability</span>
      </CardHeader>
      <CardContent className="p-4 space-y-3">
        {candidates.map((cand) => {
          const pct = Math.round(cand.confidence * 100);
          return (
            <div key={cand.id || cand.rank} className="space-y-1">
              <div className="flex items-center justify-between text-xs">
                <span className="font-semibold text-slate-800">
                  <span className="text-slate-400 font-mono mr-1.5">#{cand.rank}</span>
                  {cand.label}
                </span>
                <span className="font-bold text-slate-900">{pct}%</span>
              </div>
              <div className="w-full h-1.5 bg-slate-100 rounded-full overflow-hidden">
                <div
                  className={`h-full rounded-full ${cand.rank === 1 ? 'bg-emerald-500' : 'bg-slate-400'}`}
                  style={{ width: `${pct}%` }}
                />
              </div>
            </div>
          );
        })}
      </CardContent>
    </Card>
  );
}
