import React from 'react';
import Link from 'next/link';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Detection } from '@/types';
import { formatDate } from '@/lib/utils';
import { History, ArrowRight, ShieldCheck, ExternalLink, Leaf } from 'lucide-react';

interface RecentDetectionsTableProps {
  detections: Detection[];
}

export function RecentDetectionsTable({ detections = [] }: RecentDetectionsTableProps) {
  return (
    <Card>
      <CardHeader>
        <div className="flex items-center gap-2">
          <History className="w-4 h-4 text-emerald-600" />
          <CardTitle>Recent Crop Scans & Detections</CardTitle>
        </div>
        <Link href="/detections" className="text-xs font-semibold text-emerald-600 hover:text-emerald-700 flex items-center gap-1">
          Full Scan History <ArrowRight className="w-3.5 h-3.5" />
        </Link>
      </CardHeader>
      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse text-xs">
          <thead>
            <tr className="bg-slate-50/70 border-b border-slate-100 text-slate-500 font-semibold uppercase tracking-wider text-[10px]">
              <th className="py-3 px-4">Diagnosis</th>
              <th className="py-3 px-4">Confidence</th>
              <th className="py-3 px-4">Severity</th>
              <th className="py-3 px-4">Risk Level</th>
              <th className="py-3 px-4">Status</th>
              <th className="py-3 px-4">Date</th>
              <th className="py-3 px-4 text-right">Action</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {detections.length === 0 ? (
              <tr>
                <td colSpan={7} className="py-8 text-center text-slate-400">
                  No scan records found. Use the Scan Crop tool to analyze leaf symptoms.
                </td>
              </tr>
            ) : (
              detections.map((d) => (
                <tr key={d.id} className="hover:bg-slate-50/60 transition-colors">
                  <td className="py-3 px-4">
                    <div className="flex items-center gap-2.5">
                      <div className="w-8 h-8 rounded-lg bg-slate-100 overflow-hidden shrink-0 flex items-center justify-center border border-slate-200">
                        {d.image_url ? (
                          <img src={d.image_url} alt={d.predicted_label} className="w-full h-full object-cover" />
                        ) : (
                          <Leaf className="w-4 h-4 text-emerald-600" />
                        )}
                      </div>
                      <div>
                        <p className="font-bold text-slate-800">{d.predicted_label}</p>
                        <p className="text-[10px] text-slate-400 italic">{d.scientific_name || d.detection_type}</p>
                      </div>
                    </div>
                  </td>
                  <td className="py-3 px-4">
                    <Badge variant="confidence" confidence={d.confidence} />
                  </td>
                  <td className="py-3 px-4">
                    <Badge variant="severity" severity={d.severity} />
                  </td>
                  <td className="py-3 px-4">
                    <Badge variant="risk" riskLevel={d.risk_level} />
                  </td>
                  <td className="py-3 px-4">
                    {d.expert_verified ? (
                      <span className="inline-flex items-center gap-1 text-[11px] font-bold text-emerald-700">
                        <ShieldCheck className="w-3.5 h-3.5" /> Verified
                      </span>
                    ) : (
                      <span className="text-[11px] text-slate-500 font-medium">AI Estimate</span>
                    )}
                  </td>
                  <td className="py-3 px-4 text-slate-500">
                    {formatDate(d.created_at)}
                  </td>
                  <td className="py-3 px-4 text-right">
                    <Link
                      href={`/detections/${d.id}`}
                      className="inline-flex items-center gap-1 font-semibold text-emerald-600 hover:text-emerald-700"
                    >
                      Report <ExternalLink className="w-3 h-3" />
                    </Link>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </Card>
  );
}
