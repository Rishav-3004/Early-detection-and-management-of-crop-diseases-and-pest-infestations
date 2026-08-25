'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Button } from '@/components/ui/Button';
import { ConfidenceVisualizer } from './ConfidenceVisualizer';
import { MultiRankCandidates } from './MultiRankCandidates';
import { Detection } from '@/types';
import {
  ShieldAlert,
  AlertTriangle,
  CheckCircle2,
  Printer,
  UserCheck,
  Leaf,
  Info,
  ChevronDown,
  ChevronUp,
  Sparkles,
  ExternalLink
} from 'lucide-react';
import { RequestExpertModal } from '@/components/detections/RequestExpertModal';

interface DiagnosisResultCardProps {
  detection: Detection;
}

export function DiagnosisResultCard({ detection }: DiagnosisResultCardProps) {
  const [isExpertModalOpen, setIsExpertModalOpen] = useState(false);
  const [showAllRecs, setShowAllRecs] = useState(true);

  const isHealthy = detection.detection_type === 'HEALTHY';
  const recs = detection.recommendations;

  return (
    <div className="space-y-6">
      {/* Primary Result Banner */}
      <Card className="border-2 border-emerald-600/30 overflow-hidden shadow-md">
        <div className="bg-gradient-to-r from-slate-900 to-slate-800 text-white p-6">
          <div className="flex flex-wrap items-start justify-between gap-4">
            <div>
              <div className="flex items-center gap-2 mb-2">
                <span className="px-2.5 py-0.5 rounded-full text-[10px] font-extrabold uppercase tracking-wider bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
                  AI PREDICTION
                </span>
                {detection.is_demo && <Badge variant="demo" />}
                {detection.expert_verified && (
                  <span className="px-2.5 py-0.5 rounded-full text-[10px] font-extrabold uppercase tracking-wider bg-blue-500/20 text-blue-300 border border-blue-500/30">
                    EXPERT VERIFIED
                  </span>
                )}
              </div>
              <h2 className="text-2xl font-bold tracking-tight text-white">
                {detection.predicted_label}
              </h2>
              {detection.scientific_name && (
                <p className="text-xs text-slate-400 italic mt-0.5">
                  Taxonomy: {detection.scientific_name}
                </p>
              )}
            </div>

            <div className="flex flex-wrap items-center gap-2">
              <Badge variant="severity" severity={detection.severity} />
              <Badge variant="risk" riskLevel={detection.risk_level} />
            </div>
          </div>

          <div className="mt-4 pt-4 border-t border-slate-700/60 flex items-center gap-2 text-xs text-slate-300">
            <Info className="w-4 h-4 text-emerald-400 shrink-0" />
            <span>
              The AI model indicates that this image is likely to show symptoms of <strong>{detection.predicted_label}</strong>.
            </span>
          </div>
        </div>

        <CardContent className="p-6 space-y-6">
          {/* Key Metrics Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <ConfidenceVisualizer
              confidence={detection.confidence}
              modelVersion={detection.model_version}
              isDemo={detection.is_demo}
            />

            <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200/80 space-y-3 flex flex-col justify-between">
              <div>
                <span className="text-xs font-bold text-slate-800">AFFECTED TISSUE & RISK ASSESSMENT</span>
                <div className="mt-2 flex items-center justify-between text-xs">
                  <span className="text-slate-600">Estimated Canopy Area:</span>
                  <span className="font-bold text-slate-900">{detection.affected_area_percentage ?? 25}%</span>
                </div>
                <div className="mt-1 flex items-center justify-between text-xs">
                  <span className="text-slate-600">Multi-Factor Risk Score:</span>
                  <span className="font-bold text-slate-900">{detection.risk_score} / 100</span>
                </div>
              </div>

              {detection.risk_reasons && detection.risk_reasons.length > 0 && (
                <div className="pt-2 border-t border-slate-200 text-xs space-y-1">
                  <span className="text-[11px] font-semibold text-slate-500">Risk Drivers:</span>
                  <ul className="text-[11px] text-slate-700 list-disc pl-4 space-y-0.5">
                    {detection.risk_reasons.slice(0, 2).map((r, i) => (
                      <li key={i}>{r}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>

          {/* Differential Diagnostic Candidates */}
          {detection.results && detection.results.length > 1 && (
            <MultiRankCandidates candidates={detection.results} />
          )}

          {/* Actionable Recommendations Accordion */}
          {recs && (
            <div className="space-y-4 pt-2">
              <div className="flex items-center justify-between">
                <h3 className="text-sm font-bold text-slate-800 flex items-center gap-2">
                  <Sparkles className="w-4 h-4 text-emerald-600" />
                  Tailored Agronomic Recommendations
                </h3>
                <button
                  onClick={() => setShowAllRecs(!showAllRecs)}
                  className="text-xs text-slate-500 hover:text-slate-700 flex items-center gap-1 font-medium"
                >
                  {showAllRecs ? 'Collapse' : 'Expand All'}
                  {showAllRecs ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
                </button>
              </div>

              {showAllRecs && (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {/* Immediate Action */}
                  <div className="p-4 rounded-xl bg-red-50/60 border border-red-200/80 space-y-2">
                    <h4 className="text-xs font-bold text-red-900 uppercase tracking-wider flex items-center gap-1.5">
                      <AlertTriangle className="w-3.5 h-3.5 text-red-600" /> Immediate Actions
                    </h4>
                    <ul className="text-xs text-slate-700 space-y-1.5 list-disc pl-4">
                      {recs.immediate_actions.map((act, i) => (
                        <li key={i} className="leading-snug">{act}</li>
                      ))}
                    </ul>
                  </div>

                  {/* Management */}
                  <div className="p-4 rounded-xl bg-emerald-50/60 border border-emerald-200/80 space-y-2">
                    <h4 className="text-xs font-bold text-emerald-900 uppercase tracking-wider flex items-center gap-1.5">
                      <Leaf className="w-3.5 h-3.5 text-emerald-600" /> Cultural & Biological Management
                    </h4>
                    <ul className="text-xs text-slate-700 space-y-1.5 list-disc pl-4">
                      {recs.management.map((m, i) => (
                        <li key={i} className="leading-snug">{m}</li>
                      ))}
                    </ul>
                  </div>

                  {/* Prevention */}
                  <div className="p-4 rounded-xl bg-blue-50/60 border border-blue-200/80 space-y-2">
                    <h4 className="text-xs font-bold text-blue-900 uppercase tracking-wider flex items-center gap-1.5">
                      <CheckCircle2 className="w-3.5 h-3.5 text-blue-600" /> Future Prevention
                    </h4>
                    <ul className="text-xs text-slate-700 space-y-1.5 list-disc pl-4">
                      {recs.prevention.map((p, i) => (
                        <li key={i} className="leading-snug">{p}</li>
                      ))}
                    </ul>
                  </div>

                  {/* Monitoring */}
                  <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 space-y-2">
                    <h4 className="text-xs font-bold text-slate-900 uppercase tracking-wider flex items-center gap-1.5">
                      <Info className="w-3.5 h-3.5 text-slate-600" /> Monitoring & Expert Advice
                    </h4>
                    <ul className="text-xs text-slate-700 space-y-1.5 list-disc pl-4">
                      {recs.monitoring.map((mon, i) => (
                        <li key={i} className="leading-snug">{mon}</li>
                      ))}
                    </ul>
                    {recs.expert_review_advice && (
                      <p className="text-[11px] text-emerald-800 font-semibold mt-2 pt-2 border-t border-slate-200">
                        Agronomist Note: {recs.expert_review_advice}
                      </p>
                    )}
                  </div>
                </div>
              )}

              {/* Legal / Chemical Safety Disclaimer */}
              <div className="p-3 bg-slate-100 rounded-xl text-[11px] text-slate-600 border border-slate-200 flex items-start gap-2">
                <Info className="w-4 h-4 text-slate-500 shrink-0 mt-0.5" />
                <p>{recs.disclaimer}</p>
              </div>
            </div>
          )}

          {/* Action Bar */}
          <div className="flex flex-wrap items-center justify-between gap-3 pt-4 border-t border-slate-100">
            <div className="flex items-center gap-2">
              <Button
                variant="outline"
                size="sm"
                leftIcon={<Printer className="w-4 h-4" />}
                onClick={() => window.print()}
              >
                Print Report
              </Button>
              <Link href={`/detections/${detection.id}`}>
                <Button variant="ghost" size="sm" rightIcon={<ExternalLink className="w-3.5 h-3.5" />}>
                  Open Full File
                </Button>
              </Link>
            </div>

            {!detection.expert_verified && (
              <Button
                variant="secondary"
                size="sm"
                leftIcon={<UserCheck className="w-4 h-4 text-emerald-700" />}
                onClick={() => setIsExpertModalOpen(true)}
              >
                Request Agronomist Review
              </Button>
            )}
          </div>
        </CardContent>
      </Card>

      <RequestExpertModal
        isOpen={isExpertModalOpen}
        onClose={() => setIsExpertModalOpen(false)}
        detectionId={detection.id}
        diseaseLabel={detection.predicted_label}
      />
    </div>
  );
}
