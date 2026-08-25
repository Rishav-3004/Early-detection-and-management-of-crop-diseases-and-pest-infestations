'use client';

import React, { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import { detectionService } from '@/services/detections';
import { Detection } from '@/types';
import { DiagnosisResultCard } from '@/components/scan/DiagnosisResultCard';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Badge } from '@/components/ui/Badge';
import { formatDate } from '@/lib/utils';
import {
  ArrowLeft,
  Calendar,
  MapPin,
  Sprout,
  ShieldCheck,
  UserCheck,
  Printer,
  FileText,
  AlertTriangle,
  Leaf
} from 'lucide-react';

export default function DetectionDetailPage() {
  const params = useParams();
  const router = useRouter();
  const detectionId = params.id as string;

  const [detection, setDetection] = useState<Detection | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  useEffect(() => {
    if (!detectionId) return;
    setIsLoading(true);
    detectionService.getDetectionDetail(detectionId)
      .then(setDetection)
      .catch((e) => setErrorMsg(e.message || "Failed to load detection report"))
      .finally(() => setIsLoading(false));
  }, [detectionId]);

  if (isLoading) {
    return (
      <div className="py-20 text-center text-slate-400">
        <div className="w-8 h-8 border-2 border-emerald-500 border-t-transparent rounded-full animate-spin mx-auto mb-3" />
        <p className="text-xs font-semibold">Loading diagnostic case file #{detectionId?.slice(0, 8)}...</p>
      </div>
    );
  }

  if (errorMsg || !detection) {
    return (
      <div className="py-16 text-center space-y-4">
        <AlertTriangle className="w-10 h-10 text-red-500 mx-auto" />
        <h2 className="text-base font-bold text-slate-800">Diagnostic Record Not Found</h2>
        <p className="text-xs text-slate-500 max-w-sm mx-auto">{errorMsg || "The requested detection record does not exist or you do not have permission."}</p>
        <Link href="/detections">
          <Button variant="outline" size="sm" leftIcon={<ArrowLeft className="w-4 h-4" />}>
            Back to Scan History
          </Button>
        </Link>
      </div>
    );
  }

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      {/* Top Breadcrumb & Actions */}
      <div className="flex flex-wrap items-center justify-between gap-4">
        <Link href="/detections" className="text-xs font-semibold text-emerald-600 hover:text-emerald-700 flex items-center gap-1.5">
          <ArrowLeft className="w-4 h-4" /> Back to Scan Registry
        </Link>

        <div className="flex items-center gap-2">
          <Button
            variant="outline"
            size="sm"
            onClick={() => window.print()}
            leftIcon={<Printer className="w-4 h-4" />}
          >
            Print Case File
          </Button>
        </div>
      </div>

      {/* Case Header Card */}
      <Card className="p-6 bg-slate-900 text-white border-slate-800 space-y-4">
        <div className="flex flex-wrap items-start justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 mb-1.5">
              <span className="text-xs font-mono font-bold text-emerald-400">
                CASE #{detection.id.slice(0, 8).toUpperCase()}
              </span>
              <Badge variant="severity" severity={detection.severity} />
              <Badge variant="risk" riskLevel={detection.risk_level} />
            </div>
            <h1 className="text-2xl font-bold text-white tracking-tight">
              {detection.predicted_label}
            </h1>
            {detection.scientific_name && (
              <p className="text-xs text-slate-400 italic mt-0.5">
                Taxonomic Classification: {detection.scientific_name}
              </p>
            )}
          </div>

          <div className="text-right text-xs text-slate-400 space-y-1">
            <div className="flex items-center gap-1.5 justify-end">
              <Calendar className="w-3.5 h-3.5" />
              <span>{formatDate(detection.created_at)}</span>
            </div>
            {detection.farm_name && (
              <div className="flex items-center gap-1.5 justify-end text-slate-300">
                <MapPin className="w-3.5 h-3.5 text-emerald-400" />
                <span>{detection.farm_name} {detection.field_name ? `• ${detection.field_name}` : ''}</span>
              </div>
            )}
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pt-4 border-t border-slate-800">
          {/* Sample Image Preview */}
          <div className="aspect-video max-h-72 rounded-2xl overflow-hidden bg-black flex items-center justify-center border border-slate-800">
            {detection.image_url ? (
              <img
                src={detection.image_url}
                alt={detection.predicted_label}
                className="w-full h-full object-contain"
              />
            ) : (
              <Leaf className="w-12 h-12 text-emerald-600" />
            )}
          </div>

          {/* Expert Review Card if present */}
          {detection.expert_review ? (
            <div className="p-4 rounded-2xl bg-slate-800/80 border border-emerald-500/40 space-y-3 flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-emerald-400 flex items-center gap-1.5">
                    <UserCheck className="w-4 h-4" /> Certified Agronomist Review
                  </span>
                  <span className="text-[10px] text-slate-400">{formatDate(detection.expert_review.created_at)}</span>
                </div>
                <div className="mt-2">
                  <p className="text-xs text-slate-300">Verified Diagnosis: <strong className="text-white">{detection.expert_review.verified_label}</strong></p>
                  <p className="text-xs text-slate-300 mt-0.5">Verified Severity: <strong className="text-white">{detection.expert_review.severity}</strong></p>
                </div>
                <div className="mt-2 text-xs text-slate-200 bg-slate-900/60 p-2.5 rounded-xl border border-slate-700">
                  <p className="text-[10px] text-slate-400 font-semibold mb-1">Agronomist Clinical Notes:</p>
                  <p>{detection.expert_review.notes}</p>
                </div>
              </div>
              <div className="text-xs text-emerald-300 bg-emerald-950/40 p-2.5 rounded-xl border border-emerald-800/50">
                <p className="text-[10px] text-emerald-400 font-semibold mb-1">Prescribed Action:</p>
                <p>{detection.expert_review.recommendation}</p>
              </div>
            </div>
          ) : (
            <div className="p-4 rounded-2xl bg-slate-800/50 border border-slate-800 flex flex-col items-center justify-center text-center space-y-2">
              <ShieldCheck className="w-8 h-8 text-slate-600" />
              <h4 className="text-xs font-bold text-slate-300">No Expert Verification Submitted</h4>
              <p className="text-[11px] text-slate-500 max-w-xs">
                This diagnosis is currently based on the AI vision model. You can request a certified agronomist review below.
              </p>
            </div>
          )}
        </div>
      </Card>

      {/* Main Diagnosis & Action Component */}
      <DiagnosisResultCard detection={detection} />
    </div>
  );
}
