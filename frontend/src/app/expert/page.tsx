'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { useAuth } from '@/lib/auth';
import { expertService } from '@/services/expert';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Modal } from '@/components/ui/Modal';
import { Badge } from '@/components/ui/Badge';
import { formatDate } from '@/lib/utils';
import {
  UserCheck,
  CheckCircle2,
  AlertTriangle,
  FileCheck,
  ShieldAlert,
  Search,
  ExternalLink,
  Leaf
} from 'lucide-react';

export default function ExpertPortalPage() {
  const { user } = useAuth();

  const [pendingCases, setPendingCases] = useState<any[]>([]);
  const [historyCases, setHistoryCases] = useState<any[]>([]);
  const [activeTab, setActiveTab] = useState<'pending' | 'history'>('pending');
  const [isLoading, setIsLoading] = useState(true);

  // Review Modal
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [activeCase, setActiveCase] = useState<any | null>(null);
  const [verifiedLabel, setVerifiedLabel] = useState('');
  const [correctedConfidence, setCorrectedConfidence] = useState('0.95');
  const [severity, setSeverity] = useState('MODERATE');
  const [isCorrect, setIsCorrect] = useState(true);
  const [notes, setNotes] = useState('');
  const [recommendation, setRecommendation] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const loadCases = async () => {
    setIsLoading(true);
    try {
      const [pending, hist] = await Promise.all([
        expertService.listPendingCases().catch(() => []),
        expertService.listCaseHistory().catch(() => []),
      ]);
      setPendingCases(pending);
      setHistoryCases(hist);
    } catch (e) {
      console.error(e);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadCases();
  }, [user]);

  const handleOpenReview = (c: any) => {
    setActiveCase(c);
    setVerifiedLabel(c.predicted_label);
    setSeverity(c.severity || 'MODERATE');
    setIsCorrect(true);
    setNotes('');
    setRecommendation('');
    setIsModalOpen(true);
  };

  const handleSubmitReview = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!activeCase) return;

    setIsSubmitting(true);
    try {
      await expertService.submitReview({
        detection_id: activeCase.id,
        verified_label: verifiedLabel,
        corrected_confidence: parseFloat(correctedConfidence) || 0.95,
        severity: severity,
        is_correct_prediction: isCorrect,
        notes: notes,
        recommendation: recommendation,
      });

      setIsModalOpen(false);
      setActiveCase(null);
      loadCases();
    } catch (e) {
      console.error(e);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="p-2 rounded-xl bg-blue-100 text-blue-800">
              <UserCheck className="w-5 h-5" />
            </span>
            <h1 className="text-xl md:text-2xl font-extrabold text-slate-900 tracking-tight">
              Agronomist Case Review Workbench
            </h1>
          </div>
          <p className="text-xs text-slate-500 mt-1">
            Review farmer diagnostic scans, verify AI prediction accuracy, and issue certified agronomic prescriptions.
          </p>
        </div>

        {/* Tab Controls */}
        <div className="flex items-center gap-1 bg-slate-100 p-1 rounded-xl border border-slate-200 text-xs">
          <button
            onClick={() => setActiveTab('pending')}
            className={`px-3 py-1.5 rounded-lg font-bold transition-all ${activeTab === 'pending' ? 'bg-white text-emerald-800 shadow-xs' : 'text-slate-600 hover:text-slate-900'}`}
          >
            Pending Reviews ({pendingCases.length})
          </button>
          <button
            onClick={() => setActiveTab('history')}
            className={`px-3 py-1.5 rounded-lg font-bold transition-all ${activeTab === 'history' ? 'bg-white text-emerald-800 shadow-xs' : 'text-slate-600 hover:text-slate-900'}`}
          >
            Completed Archive ({historyCases.length})
          </button>
        </div>
      </div>

      {/* Content Table */}
      <Card className="overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse text-xs">
            <thead>
              <tr className="bg-slate-50/70 border-b border-slate-100 text-slate-500 font-semibold uppercase tracking-wider text-[10px]">
                <th className="py-3 px-4">Sample Image</th>
                <th className="py-3 px-4">Farmer / Farm</th>
                <th className="py-3 px-4">AI Prediction</th>
                <th className="py-3 px-4">AI Confidence</th>
                <th className="py-3 px-4">Risk Level</th>
                <th className="py-3 px-4">Date</th>
                <th className="py-3 px-4 text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {isLoading ? (
                <tr>
                  <td colSpan={7} className="py-12 text-center text-slate-400">
                    <div className="w-6 h-6 border-2 border-emerald-500 border-t-transparent rounded-full animate-spin mx-auto mb-2" />
                    Loading cases...
                  </td>
                </tr>
              ) : activeTab === 'pending' ? (
                pendingCases.length === 0 ? (
                  <tr>
                    <td colSpan={7} className="py-12 text-center text-slate-400">
                      All farmer diagnostic scans are currently reviewed and up to date!
                    </td>
                  </tr>
                ) : (
                  pendingCases.map((c) => (
                    <tr key={c.id} className="hover:bg-slate-50/60 transition-colors">
                      <td className="py-3 px-4">
                        <div className="w-10 h-10 rounded-xl bg-slate-100 overflow-hidden shrink-0 flex items-center justify-center border border-slate-200">
                          {c.image_url ? (
                            <img src={c.image_url} alt={c.predicted_label} className="w-full h-full object-cover" />
                          ) : (
                            <Leaf className="w-5 h-5 text-emerald-600" />
                          )}
                        </div>
                      </td>
                      <td className="py-3 px-4">
                        <p className="font-bold text-slate-800">{c.user_name || 'Farmer'}</p>
                        <p className="text-[10px] text-slate-400">{c.farm_name || 'Farm Plot'}</p>
                      </td>
                      <td className="py-3 px-4 font-bold text-slate-800">
                        {c.predicted_label}
                      </td>
                      <td className="py-3 px-4">
                        <Badge variant="confidence" confidence={c.confidence} />
                      </td>
                      <td className="py-3 px-4">
                        <Badge variant="risk" riskLevel={c.risk_level} />
                      </td>
                      <td className="py-3 px-4 text-slate-500">
                        {formatDate(c.created_at)}
                      </td>
                      <td className="py-3 px-4 text-right">
                        <Button
                          variant="primary"
                          size="sm"
                          onClick={() => handleOpenReview(c)}
                        >
                          Review & Verify
                        </Button>
                      </td>
                    </tr>
                  ))
                )
              ) : (
                historyCases.length === 0 ? (
                  <tr>
                    <td colSpan={7} className="py-12 text-center text-slate-400">
                      No archived expert reviews yet.
                    </td>
                  </tr>
                ) : (
                  historyCases.map((h) => (
                    <tr key={h.id} className="hover:bg-slate-50/60 transition-colors">
                      <td className="py-3 px-4">
                        <div className="w-10 h-10 rounded-xl bg-slate-100 overflow-hidden shrink-0 flex items-center justify-center border border-slate-200">
                          {h.image_url ? (
                            <img src={h.image_url} alt={h.verified_label} className="w-full h-full object-cover" />
                          ) : (
                            <Leaf className="w-5 h-5 text-emerald-600" />
                          )}
                        </div>
                      </td>
                      <td className="py-3 px-4">
                        <p className="font-bold text-slate-800">{h.expert_name}</p>
                        <p className="text-[10px] text-slate-400">Verified Case</p>
                      </td>
                      <td className="py-3 px-4">
                        <p className="font-bold text-emerald-800">{h.verified_label}</p>
                        <p className="text-[10px] text-slate-400 line-through">Original: {h.original_label}</p>
                      </td>
                      <td className="py-3 px-4">
                        <Badge variant="severity" severity={h.severity} />
                      </td>
                      <td className="py-3 px-4">
                        <span className="text-[11px] font-bold text-emerald-700">✓ Resolved</span>
                      </td>
                      <td className="py-3 px-4 text-slate-500">
                        {formatDate(h.created_at)}
                      </td>
                      <td className="py-3 px-4 text-right">
                        <Link href={`/detections/${h.detection_id}`}>
                          <Button variant="ghost" size="sm">
                            Open Case
                          </Button>
                        </Link>
                      </td>
                    </tr>
                  ))
                )
              )}
            </tbody>
          </table>
        </div>
      </Card>

      {/* Expert Review Modal */}
      {activeCase && (
        <Modal
          isOpen={isModalOpen}
          onClose={() => setIsModalOpen(false)}
          title="Clinical Agronomic Verification"
          description={`Case ID: ${activeCase.id.slice(0, 8)} • AI Initial: ${activeCase.predicted_label}`}
          maxWidth="lg"
        >
          <form onSubmit={handleSubmitReview} className="space-y-4 text-xs">
            {/* Image Preview Thumbnail */}
            <div className="flex items-center gap-3 p-3 bg-slate-900 text-white rounded-xl">
              <div className="w-16 h-16 rounded-lg bg-black overflow-hidden shrink-0">
                <img src={activeCase.image_url} alt="Scan specimen" className="w-full h-full object-cover" />
              </div>
              <div>
                <p className="text-xs font-bold">{activeCase.predicted_label}</p>
                <p className="text-[10px] text-slate-400">AI Confidence: {Math.round(activeCase.confidence * 100)}% • Severity: {activeCase.severity}</p>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div className="space-y-1">
                <label className="font-semibold text-slate-700">Verified Diagnosis Label</label>
                <input
                  type="text"
                  required
                  value={verifiedLabel}
                  onChange={(e) => setVerifiedLabel(e.target.value)}
                  className="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-800 focus:outline-none focus:ring-2 focus:ring-emerald-500"
                />
              </div>

              <div className="space-y-1">
                <label className="font-semibold text-slate-700">Confirmed Severity</label>
                <select
                  value={severity}
                  onChange={(e) => setSeverity(e.target.value)}
                  className="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-800 focus:outline-none focus:ring-2 focus:ring-emerald-500"
                >
                  <option value="NONE">None</option>
                  <option value="LOW">Low</option>
                  <option value="MODERATE">Moderate</option>
                  <option value="HIGH">High</option>
                  <option value="CRITICAL">Critical</option>
                </select>
              </div>
            </div>

            <div className="space-y-1">
              <label className="font-semibold text-slate-700">Agronomist Clinical Notes</label>
              <textarea
                required
                value={notes}
                onChange={(e) => setNotes(e.target.value)}
                placeholder="Detail microscopic/visual observations confirming or correcting the AI prediction..."
                rows={3}
                className="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-800 focus:outline-none focus:ring-2 focus:ring-emerald-500"
              />
            </div>

            <div className="space-y-1">
              <label className="font-semibold text-slate-700">Custom Management Prescription for Farmer</label>
              <textarea
                required
                value={recommendation}
                onChange={(e) => setRecommendation(e.target.value)}
                placeholder="Prescribe biological spray schedules, pruning, or cultural isolation steps..."
                rows={3}
                className="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-800 focus:outline-none focus:ring-2 focus:ring-emerald-500"
              />
            </div>

            <div className="flex items-center justify-end gap-2 pt-3 border-t border-slate-100">
              <Button type="button" variant="ghost" size="sm" onClick={() => setIsModalOpen(false)}>
                Cancel
              </Button>
              <Button type="submit" size="sm" isLoading={isSubmitting}>
                Publish Agronomic Prescription
              </Button>
            </div>
          </form>
        </Modal>
      )}
    </div>
  );
}
