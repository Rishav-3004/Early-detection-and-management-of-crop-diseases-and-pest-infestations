import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card';
import { ProgressMeter } from '@/components/ui/ProgressMeter';
import { ShieldAlert, Bug, CloudSun, CheckCircle2, AlertTriangle } from 'lucide-react';

interface RiskOverviewProps {
  diseaseRiskScore?: number;
  pestRiskScore?: number;
  weatherRiskScore?: number;
  overallCropRiskScore?: number;
}

export function RiskOverview({
  diseaseRiskScore = 42,
  pestRiskScore = 28,
  weatherRiskScore = 65,
  overallCropRiskScore = 45,
}: RiskOverviewProps) {
  return (
    <Card className="h-full flex flex-col">
      <CardHeader>
        <div className="flex items-center gap-2">
          <ShieldAlert className="w-4 h-4 text-emerald-600" />
          <CardTitle>Multi-Factor Risk Assessment</CardTitle>
        </div>
        <span className="text-[11px] text-slate-400 font-medium">Real-time Calibrated</span>
      </CardHeader>
      <CardContent className="space-y-4 flex-1 flex flex-col justify-between">
        <div className="p-4 rounded-xl bg-slate-900 text-white flex items-center justify-between">
          <div>
            <p className="text-xs text-slate-400 font-medium">Overall Farm Risk Score</p>
            <h3 className="text-2xl font-bold mt-0.5">{overallCropRiskScore} / 100</h3>
            <p className="text-[10px] text-slate-300 mt-1">
              {overallCropRiskScore >= 70 ? 'High probability of foliar pathogen spread' : 'Moderate ambient risk; maintain scouting'}
            </p>
          </div>
          <div className="p-3 rounded-xl bg-slate-800 text-emerald-400">
            <AlertTriangle className="w-6 h-6 text-amber-400" />
          </div>
        </div>

        <div className="space-y-3">
          <div className="space-y-1">
            <div className="flex justify-between items-center text-xs font-semibold text-slate-700">
              <span className="flex items-center gap-1.5"><ShieldAlert className="w-3.5 h-3.5 text-red-500" /> Foliar Disease Index</span>
              <span>{diseaseRiskScore}%</span>
            </div>
            <ProgressMeter value={diseaseRiskScore} showPercentage={false} colorScheme={diseaseRiskScore > 60 ? 'red' : 'amber'} />
          </div>

          <div className="space-y-1">
            <div className="flex justify-between items-center text-xs font-semibold text-slate-700">
              <span className="flex items-center gap-1.5"><Bug className="w-3.5 h-3.5 text-purple-500" /> Pest Population Risk</span>
              <span>{pestRiskScore}%</span>
            </div>
            <ProgressMeter value={pestRiskScore} showPercentage={false} colorScheme={pestRiskScore > 60 ? 'red' : 'green'} />
          </div>

          <div className="space-y-1">
            <div className="flex justify-between items-center text-xs font-semibold text-slate-700">
              <span className="flex items-center gap-1.5"><CloudSun className="w-3.5 h-3.5 text-blue-500" /> Meteorological Microclimate Risk</span>
              <span>{weatherRiskScore}%</span>
            </div>
            <ProgressMeter value={weatherRiskScore} showPercentage={false} colorScheme={weatherRiskScore > 60 ? 'amber' : 'green'} />
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
