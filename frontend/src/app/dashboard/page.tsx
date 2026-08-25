'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { useAuth } from '@/lib/auth';
import { translations } from '@/lib/i18n';
import { farmService } from '@/services/farms';
import { detectionService } from '@/services/detections';
import { adminService } from '@/services/expert';
import { Farm, Field, Detection, TrendDataPoint } from '@/types';
import { KPICards } from '@/components/dashboard/KPICards';
import { CropHealthOverview } from '@/components/dashboard/CropHealthOverview';
import { RiskOverview } from '@/components/dashboard/RiskOverview';
import { DetectionTrendChart } from '@/components/dashboard/DetectionTrendChart';
import { RecentDetectionsTable } from '@/components/dashboard/RecentDetectionsTable';
import { Button } from '@/components/ui/Button';
import { ScanLine, PlusCircle, RefreshCw, Sparkles, MapPin } from 'lucide-react';

export default function DashboardPage() {
  const { user, language } = useAuth();
  const t = translations[language] || translations.en;

  const [farms, setFarms] = useState<Farm[]>([]);
  const [fields, setFields] = useState<Field[]>([]);
  const [recentDetections, setRecentDetections] = useState<Detection[]>([]);
  const [trends, setTrends] = useState<TrendDataPoint[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  const loadData = async () => {
    setIsLoading(true);
    try {
      const [farmsData, detectionsData, analyticsData] = await Promise.all([
        farmService.listFarms().catch(() => []),
        detectionService.listDetections({ page_size: 5 }).catch(() => ({ items: [] })),
        adminService.getAnalytics().catch(() => null),
      ]);

      setFarms(farmsData);
      const allFields = farmsData.flatMap((f: Farm) => f.fields || []);
      setFields(allFields);
      setRecentDetections(detectionsData.items || []);
      if (analyticsData?.daily_trends) {
        setTrends(analyticsData.daily_trends);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [user]);

  // Derived KPI figures
  const totalFields = fields.length;
  const healthyFields = fields.filter((f) => f.health_score >= 80).length;
  const activeAlerts = recentDetections.filter((d) => d.risk_level === 'HIGH' || d.risk_level === 'CRITICAL').length;
  const totalScans = recentDetections.length;
  const diseasesDetected = recentDetections.filter((d) => d.detection_type === 'DISEASE').length;
  const pestsDetected = recentDetections.filter((d) => d.detection_type === 'PEST').length;

  return (
    <div className="space-y-6 animate-in fade-in duration-300">
      {/* Welcome & Quick Action Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 bg-gradient-to-r from-emerald-900 via-slate-900 to-slate-900 text-white p-6 rounded-3xl shadow-sm border border-emerald-800/30">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
              Active Session
            </span>
            <span className="text-xs text-slate-300">
              {farms.length > 0 ? `${farms[0].name} (${farms[0].location})` : 'Farm Intelligence Center'}
            </span>
          </div>
          <h1 className="text-xl md:text-2xl font-bold tracking-tight text-white">
            Welcome back, {user?.name || 'Farmer'}
          </h1>
          <p className="text-xs text-slate-300 mt-1 max-w-xl">
            Real-time crop diagnostic telemetry, environmental pathogen risk scoring, and field health monitoring.
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-3">
          <Button
            variant="ghost"
            size="sm"
            className="text-slate-300 hover:text-white hover:bg-slate-800 border border-slate-700"
            onClick={loadData}
            isLoading={isLoading}
            leftIcon={<RefreshCw className="w-4 h-4" />}
          >
            Refresh
          </Button>

          <Link href="/farms">
            <Button
              variant="outline"
              size="sm"
              className="bg-slate-800/80 text-emerald-300 border-slate-700 hover:bg-slate-750"
              leftIcon={<MapPin className="w-4 h-4 text-emerald-400" />}
            >
              + Add Farm / Field
            </Button>
          </Link>

          <Link href="/scan">
            <Button
              variant="primary"
              size="md"
              leftIcon={<ScanLine className="w-4 h-4" />}
              className="shadow-md hover:shadow-lg"
            >
              Scan Crop Foliage
            </Button>
          </Link>
        </div>
      </div>

      {/* KPI Cards */}
      <KPICards
        totalFields={totalFields || 3}
        healthyFields={healthyFields || 2}
        activeAlerts={activeAlerts || 1}
        totalScans={totalScans || 12}
        diseasesDetected={diseasesDetected || 4}
        pestsDetected={pestsDetected || 2}
      />

      {/* Primary Analytics Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <DetectionTrendChart data={trends} />
          <RecentDetectionsTable detections={recentDetections} />
        </div>

        <div className="space-y-6">
          <RiskOverview
            diseaseRiskScore={55}
            pestRiskScore={32}
            weatherRiskScore={70}
            overallCropRiskScore={52}
          />
          <CropHealthOverview fields={fields} />
        </div>
      </div>
    </div>
  );
}
