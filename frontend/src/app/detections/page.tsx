'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { useAuth } from '@/lib/auth';
import { detectionService } from '@/services/detections';
import { farmService } from '@/services/farms';
import { knowledgeService } from '@/services/knowledge';
import { adminService } from '@/services/expert';
import { Detection, Farm, Crop } from '@/types';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Button } from '@/components/ui/Button';
import { formatDate } from '@/lib/utils';
import {
  History,
  Search,
  Filter,
  Download,
  ShieldCheck,
  ExternalLink,
  ChevronLeft,
  ChevronRight,
  Leaf,
  ScanLine
} from 'lucide-react';

export default function DetectionsHistoryPage() {
  const { user } = useAuth();

  const [detections, setDetections] = useState<Detection[]>([]);
  const [total, setTotal] = useState(0);
  const [totalPages, setTotalPages] = useState(1);
  const [page, setPage] = useState(1);
  const [pageSize] = useState(15);
  const [isLoading, setIsLoading] = useState(true);

  // Filters
  const [search, setSearch] = useState('');
  const [detectionType, setDetectionType] = useState('');
  const [severity, setSeverity] = useState('');
  const [riskLevel, setRiskLevel] = useState('');
  const [sortBy, setSortBy] = useState('newest');

  const [farms, setFarms] = useState<Farm[]>([]);
  const [crops, setCrops] = useState<Crop[]>([]);

  useEffect(() => {
    farmService.listFarms().then(setFarms).catch(() => {});
    knowledgeService.listCrops().then(setCrops).catch(() => {});
  }, []);

  const loadDetections = async () => {
    setIsLoading(true);
    try {
      const res = await detectionService.listDetections({
        page,
        page_size: pageSize,
        detection_type: detectionType || undefined,
        severity: severity || undefined,
        risk_level: riskLevel || undefined,
        search: search || undefined,
        sort_by: sortBy,
      });
      setDetections(res.items || []);
      setTotal(res.meta.total);
      setTotalPages(res.meta.total_pages);
    } catch (e) {
      console.error(e);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadDetections();
  }, [page, detectionType, severity, riskLevel, sortBy]);

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setPage(1);
    loadDetections();
  };

  const handleExportCSV = async () => {
    await adminService.downloadCSV();
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="p-2 rounded-xl bg-emerald-100 text-emerald-800">
              <History className="w-5 h-5" />
            </span>
            <h1 className="text-xl md:text-2xl font-extrabold text-slate-900 tracking-tight">
              Crop Scan History & Diagnostics Log
            </h1>
          </div>
          <p className="text-xs text-slate-500 mt-1">
            Historical registry of AI and expert-verified foliar diagnoses ({total} total records)
          </p>
        </div>

        <div className="flex items-center gap-3">
          <Button
            variant="outline"
            size="sm"
            onClick={handleExportCSV}
            leftIcon={<Download className="w-4 h-4" />}
          >
            Export CSV
          </Button>
          <Link href="/scan">
            <Button variant="primary" size="sm" leftIcon={<ScanLine className="w-4 h-4" />}>
              Scan New Leaf
            </Button>
          </Link>
        </div>
      </div>

      {/* Search & Filter Bar */}
      <Card className="p-4 space-y-3">
        <form onSubmit={handleSearchSubmit} className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-6 gap-3">
          <div className="relative sm:col-span-2">
            <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search diagnosis or pathogen..."
              className="w-full pl-9 pr-3 py-2 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-800 focus:outline-none focus:ring-2 focus:ring-emerald-500"
            />
          </div>

          <div>
            <select
              value={detectionType}
              onChange={(e) => { setDetectionType(e.target.value); setPage(1); }}
              className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-800 focus:outline-none focus:ring-2 focus:ring-emerald-500"
            >
              <option value="">All Types</option>
              <option value="DISEASE">Foliar Diseases</option>
              <option value="PEST">Pest Infestations</option>
              <option value="HEALTHY">Healthy Plants</option>
            </select>
          </div>

          <div>
            <select
              value={severity}
              onChange={(e) => { setSeverity(e.target.value); setPage(1); }}
              className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-800 focus:outline-none focus:ring-2 focus:ring-emerald-500"
            >
              <option value="">All Severities</option>
              <option value="NONE">None</option>
              <option value="LOW">Low</option>
              <option value="MODERATE">Moderate</option>
              <option value="HIGH">High</option>
              <option value="CRITICAL">Critical</option>
            </select>
          </div>

          <div>
            <select
              value={riskLevel}
              onChange={(e) => { setRiskLevel(e.target.value); setPage(1); }}
              className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-800 focus:outline-none focus:ring-2 focus:ring-emerald-500"
            >
              <option value="">All Risk Levels</option>
              <option value="LOW">Low Risk</option>
              <option value="MEDIUM">Medium Risk</option>
              <option value="HIGH">High Risk</option>
              <option value="CRITICAL">Critical Risk</option>
            </select>
          </div>

          <div>
            <select
              value={sortBy}
              onChange={(e) => { setSortBy(e.target.value); setPage(1); }}
              className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-800 focus:outline-none focus:ring-2 focus:ring-emerald-500"
            >
              <option value="newest">Newest First</option>
              <option value="oldest">Oldest First</option>
              <option value="highest_confidence">Highest Confidence</option>
              <option value="highest_severity">Highest Risk Score</option>
            </select>
          </div>
        </form>
      </Card>

      {/* Detections List */}
      <Card className="overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse text-xs">
            <thead>
              <tr className="bg-slate-50/70 border-b border-slate-100 text-slate-500 font-semibold uppercase tracking-wider text-[10px]">
                <th className="py-3 px-4">Sample Image</th>
                <th className="py-3 px-4">Diagnosis / Condition</th>
                <th className="py-3 px-4">Confidence</th>
                <th className="py-3 px-4">Severity</th>
                <th className="py-3 px-4">Risk Level</th>
                <th className="py-3 px-4">Status</th>
                <th className="py-3 px-4">Date</th>
                <th className="py-3 px-4 text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {isLoading ? (
                <tr>
                  <td colSpan={8} className="py-12 text-center text-slate-400">
                    <div className="w-6 h-6 border-2 border-emerald-500 border-t-transparent rounded-full animate-spin mx-auto mb-2" />
                    Loading scan records...
                  </td>
                </tr>
              ) : detections.length === 0 ? (
                <tr>
                  <td colSpan={8} className="py-12 text-center text-slate-400">
                    No detections match your query. Try clearing filters.
                  </td>
                </tr>
              ) : (
                detections.map((d) => (
                  <tr key={d.id} className="hover:bg-slate-50/60 transition-colors">
                    <td className="py-3 px-4">
                      <div className="w-10 h-10 rounded-xl bg-slate-100 overflow-hidden shrink-0 flex items-center justify-center border border-slate-200">
                        {d.image_url ? (
                          <img src={d.image_url} alt={d.predicted_label} className="w-full h-full object-cover" />
                        ) : (
                          <Leaf className="w-5 h-5 text-emerald-600" />
                        )}
                      </div>
                    </td>
                    <td className="py-3 px-4">
                      <p className="font-bold text-slate-800 text-xs">{d.predicted_label}</p>
                      <p className="text-[10px] text-slate-400 italic">{d.scientific_name || d.detection_type}</p>
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
                        Details <ExternalLink className="w-3 h-3" />
                      </Link>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>

        {/* Pagination Controls */}
        {totalPages > 1 && (
          <div className="p-4 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
            <span>Page {page} of {totalPages} ({total} total scans)</span>
            <div className="flex items-center gap-2">
              <Button
                variant="outline"
                size="sm"
                disabled={page <= 1}
                onClick={() => setPage(p => Math.max(1, p - 1))}
                leftIcon={<ChevronLeft className="w-3.5 h-3.5" />}
              >
                Previous
              </Button>
              <Button
                variant="outline"
                size="sm"
                disabled={page >= totalPages}
                onClick={() => setPage(p => Math.min(totalPages, p + 1))}
                rightIcon={<ChevronRight className="w-3.5 h-3.5" />}
              >
                Next
              </Button>
            </div>
          </div>
        )}
      </Card>
    </div>
  );
}
