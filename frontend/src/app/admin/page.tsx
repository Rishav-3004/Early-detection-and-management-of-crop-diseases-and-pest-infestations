'use client';

import React, { useState, useEffect } from 'react';
import { useAuth } from '@/lib/auth';
import { adminService } from '@/services/expert';
import { AdminAnalytics, User } from '@/types';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Badge } from '@/components/ui/Badge';
import { ProgressMeter } from '@/components/ui/ProgressMeter';
import { formatDate } from '@/lib/utils';
import {
  BarChart3,
  Users,
  Cpu,
  ShieldCheck,
  Download,
  CheckCircle2,
  AlertTriangle,
  Layers,
  Activity,
  UserCheck
} from 'lucide-react';

export default function AdminStudioPage() {
  const { user } = useAuth();

  const [analytics, setAnalytics] = useState<AdminAnalytics | null>(null);
  const [users, setUsers] = useState<User[]>([]);
  const [activeTab, setActiveTab] = useState<'analytics' | 'users' | 'model'>('analytics');
  const [isLoading, setIsLoading] = useState(true);

  const loadData = async () => {
    setIsLoading(true);
    try {
      const [an, usrs] = await Promise.all([
        adminService.getAnalytics().catch(() => null),
        adminService.listUsers().catch(() => []),
      ]);
      setAnalytics(an);
      setUsers(usrs);
    } catch (e) {
      console.error(e);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [user]);

  const handleToggleUser = async (userId: string, currentStatus: boolean) => {
    await adminService.toggleUserStatus(userId, !currentStatus);
    loadData();
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="p-2 rounded-xl bg-purple-100 text-purple-800">
              <BarChart3 className="w-5 h-5" />
            </span>
            <h1 className="text-xl md:text-2xl font-extrabold text-slate-900 tracking-tight">
              Administrative & Model Telemetry Studio
            </h1>
          </div>
          <p className="text-xs text-slate-500 mt-1">
            Global system KPIs, model confidence distribution metrics, agronomist agreement telemetry, and user management.
          </p>
        </div>

        {/* Tab Controls */}
        <div className="flex items-center gap-1 bg-slate-100 p-1 rounded-xl border border-slate-200 text-xs">
          <button
            onClick={() => setActiveTab('analytics')}
            className={`px-3 py-1.5 rounded-lg font-bold transition-all ${activeTab === 'analytics' ? 'bg-white text-purple-900 shadow-xs' : 'text-slate-600 hover:text-slate-900'}`}
          >
            System KPIs
          </button>
          <button
            onClick={() => setActiveTab('model')}
            className={`px-3 py-1.5 rounded-lg font-bold transition-all ${activeTab === 'model' ? 'bg-white text-purple-900 shadow-xs' : 'text-slate-600 hover:text-slate-900'}`}
          >
            Model Performance
          </button>
          <button
            onClick={() => setActiveTab('users')}
            className={`px-3 py-1.5 rounded-lg font-bold transition-all ${activeTab === 'users' ? 'bg-white text-purple-900 shadow-xs' : 'text-slate-600 hover:text-slate-900'}`}
          >
            Users ({users.length})
          </button>
        </div>
      </div>

      {isLoading ? (
        <div className="py-20 text-center text-slate-400">
          <div className="w-8 h-8 border-2 border-purple-500 border-t-transparent rounded-full animate-spin mx-auto mb-2" />
          <p className="text-xs">Computing platform telemetry...</p>
        </div>
      ) : activeTab === 'analytics' ? (
        <div className="space-y-6">
          {/* Top KPI Cards */}
          {analytics && (
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
              <Card className="p-4 border-slate-200">
                <span className="text-xs font-semibold text-slate-500">Total Registered Users</span>
                <h3 className="text-2xl font-bold text-slate-900 mt-1">{analytics.kpis.total_users}</h3>
                <p className="text-[10px] text-slate-400 mt-0.5">{analytics.kpis.total_farmers} Farmers • {analytics.kpis.total_experts} Agronomists</p>
              </Card>

              <Card className="p-4 border-slate-200">
                <span className="text-xs font-semibold text-slate-500">Total Farms & Fields</span>
                <h3 className="text-2xl font-bold text-slate-900 mt-1">{analytics.kpis.total_fields}</h3>
                <p className="text-[10px] text-slate-400 mt-0.5">Across {analytics.kpis.total_farms} farm properties</p>
              </Card>

              <Card className="p-4 border-slate-200">
                <span className="text-xs font-semibold text-slate-500">Diagnostic Scans</span>
                <h3 className="text-2xl font-bold text-slate-900 mt-1">{analytics.kpis.total_scans}</h3>
                <p className="text-[10px] text-slate-400 mt-0.5">{analytics.kpis.total_diseases_detected} Diseases • {analytics.kpis.total_pests_detected} Pests</p>
              </Card>

              <Card className="p-4 border-slate-200">
                <span className="text-xs font-semibold text-slate-500">Expert Reviews Completed</span>
                <h3 className="text-2xl font-bold text-emerald-700 mt-1">{analytics.kpis.completed_expert_reviews}</h3>
                <p className="text-[10px] text-slate-400 mt-0.5">{analytics.kpis.pending_expert_reviews} Pending in queue</p>
              </Card>
            </div>
          )}

          {/* Breakdown Distributions */}
          {analytics && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <Card className="p-5 space-y-4">
                <h3 className="text-xs font-bold text-slate-800 uppercase tracking-wider">Top Detected Crop Diseases</h3>
                {analytics.top_diseases.length === 0 ? (
                  <p className="text-xs text-slate-400">No disease distributions recorded yet.</p>
                ) : (
                  <div className="space-y-3">
                    {analytics.top_diseases.map((d, i) => (
                      <div key={i} className="space-y-1">
                        <div className="flex justify-between text-xs font-semibold text-slate-700">
                          <span>{d.name}</span>
                          <span>{d.count} ({d.percentage}%)</span>
                        </div>
                        <ProgressMeter value={d.percentage} showPercentage={false} colorScheme="red" />
                      </div>
                    ))}
                  </div>
                )}
              </Card>

              <Card className="p-5 space-y-4">
                <h3 className="text-xs font-bold text-slate-800 uppercase tracking-wider">Top Detected Insect Pests</h3>
                {analytics.top_pests.length === 0 ? (
                  <p className="text-xs text-slate-400">No pest distributions recorded yet.</p>
                ) : (
                  <div className="space-y-3">
                    {analytics.top_pests.map((p, i) => (
                      <div key={i} className="space-y-1">
                        <div className="flex justify-between text-xs font-semibold text-slate-700">
                          <span>{p.name}</span>
                          <span>{p.count} ({p.percentage}%)</span>
                        </div>
                        <ProgressMeter value={p.percentage} showPercentage={false} colorScheme="amber" />
                      </div>
                    ))}
                  </div>
                )}
              </Card>
            </div>
          )}
        </div>
      ) : activeTab === 'model' ? (
        /* Model Performance Tab */
        analytics && (
          <div className="space-y-6">
            <Card className="p-6 bg-slate-900 text-white border-slate-800 space-y-5">
              <div className="flex flex-wrap items-center justify-between gap-4">
                <div>
                  <span className="text-xs font-mono font-bold text-emerald-400 uppercase tracking-wider">
                    Model Version: {analytics.model_metrics.model_version}
                  </span>
                  <h2 className="text-2xl font-bold text-white mt-1">Computer Vision Model Performance</h2>
                  <p className="text-xs text-slate-400">Continuous telemetry derived from expert feedback loops</p>
                </div>
                <div className="p-3 rounded-2xl bg-slate-800 border border-slate-700 text-right">
                  <p className="text-[10px] text-slate-400 uppercase font-bold">Average Diagnostic Confidence</p>
                  <p className="text-xl font-bold text-emerald-400">{Math.round(analytics.model_metrics.average_confidence * 100)}%</p>
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 pt-3 border-t border-slate-800">
                <div className="p-3 bg-slate-800/80 rounded-xl border border-slate-700">
                  <p className="text-[10px] text-slate-400">High Confidence (&ge;80%)</p>
                  <h4 className="text-lg font-bold text-emerald-400">{analytics.model_metrics.high_confidence_count}</h4>
                </div>

                <div className="p-3 bg-slate-800/80 rounded-xl border border-slate-700">
                  <p className="text-[10px] text-slate-400">Medium Confidence (60-79%)</p>
                  <h4 className="text-lg font-bold text-amber-400">{analytics.model_metrics.medium_confidence_count}</h4>
                </div>

                <div className="p-3 bg-slate-800/80 rounded-xl border border-slate-700">
                  <p className="text-[10px] text-slate-400">Low Confidence (&lt;60%)</p>
                  <h4 className="text-lg font-bold text-red-400">{analytics.model_metrics.low_confidence_count}</h4>
                </div>
              </div>

              <div className="p-4 rounded-xl bg-slate-800/60 border border-slate-700 space-y-2">
                <div className="flex justify-between items-center text-xs">
                  <span className="text-slate-300 font-semibold">Expert Agronomist Agreement Rate:</span>
                  <span className="font-bold text-emerald-400">{analytics.model_metrics.expert_agreement_rate}%</span>
                </div>
                <div className="flex justify-between items-center text-xs">
                  <span className="text-slate-300 font-semibold">Expert Correction Rate:</span>
                  <span className="font-bold text-red-400">{analytics.model_metrics.expert_correction_rate}%</span>
                </div>
              </div>
            </Card>
          </div>
        )
      ) : (
        /* Users Management Tab */
        <Card className="overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse text-xs">
              <thead>
                <tr className="bg-slate-50/70 border-b border-slate-100 text-slate-500 font-semibold uppercase tracking-wider text-[10px]">
                  <th className="py-3 px-4">User</th>
                  <th className="py-3 px-4">Email</th>
                  <th className="py-3 px-4">Role</th>
                  <th className="py-3 px-4">Status</th>
                  <th className="py-3 px-4">Registered</th>
                  <th className="py-3 px-4 text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {users.map((u) => (
                  <tr key={u.id} className="hover:bg-slate-50/60 transition-colors">
                    <td className="py-3 px-4 font-bold text-slate-800">{u.name}</td>
                    <td className="py-3 px-4 text-slate-600">{u.email}</td>
                    <td className="py-3 px-4">
                      <span className="px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider bg-slate-100 text-slate-700 border border-slate-200">
                        {u.role}
                      </span>
                    </td>
                    <td className="py-3 px-4">
                      {u.is_active ? (
                        <span className="text-emerald-700 font-bold text-[11px]">Active</span>
                      ) : (
                        <span className="text-red-700 font-bold text-[11px]">Suspended</span>
                      )}
                    </td>
                    <td className="py-3 px-4 text-slate-500">{formatDate(u.created_at)}</td>
                    <td className="py-3 px-4 text-right">
                      <button
                        onClick={() => handleToggleUser(u.id, u.is_active)}
                        className={`text-xs font-semibold underline ${u.is_active ? 'text-red-600 hover:text-red-700' : 'text-emerald-600 hover:text-emerald-700'}`}
                      >
                        {u.is_active ? 'Deactivate' : 'Activate'}
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Card>
      )}
    </div>
  );
}
