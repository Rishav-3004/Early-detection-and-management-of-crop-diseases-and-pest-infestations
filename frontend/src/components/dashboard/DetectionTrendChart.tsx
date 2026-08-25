'use client';

import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card';
import { ResponsiveContainer, AreaChart, Area, XAxis, YAxis, Tooltip, Legend } from 'recharts';
import { TrendDataPoint } from '@/types';

interface DetectionTrendChartProps {
  data: TrendDataPoint[];
}

export function DetectionTrendChart({ data = [] }: DetectionTrendChartProps) {
  // Provide sample fallback trend if empty
  const chartData = data.length > 0 ? data : [
    { date: 'Aug 12', scans: 4, diseases: 2, pests: 1, healthy: 1 },
    { date: 'Aug 14', scans: 6, diseases: 3, pests: 2, healthy: 1 },
    { date: 'Aug 16', scans: 8, diseases: 4, pests: 1, healthy: 3 },
    { date: 'Aug 18', scans: 5, diseases: 2, pests: 1, healthy: 2 },
    { date: 'Aug 20', scans: 9, diseases: 5, pests: 2, healthy: 2 },
    { date: 'Aug 22', scans: 11, diseases: 4, pests: 3, healthy: 4 },
    { date: 'Aug 24', scans: 7, diseases: 2, pests: 2, healthy: 3 },
  ];

  return (
    <Card className="h-full flex flex-col">
      <CardHeader>
        <div>
          <CardTitle>Crop Detections & Diagnostics Trend</CardTitle>
          <p className="text-xs text-slate-500 mt-0.5">14-day chronological tracking of disease, pest, and healthy plant observations</p>
        </div>
      </CardHeader>
      <CardContent className="flex-1 min-h-[260px] pt-4">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={chartData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
            <defs>
              <linearGradient id="diseaseGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#ef4444" stopOpacity={0.4}/>
                <stop offset="95%" stopColor="#ef4444" stopOpacity={0.0}/>
              </linearGradient>
              <linearGradient id="pestGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#a855f7" stopOpacity={0.4}/>
                <stop offset="95%" stopColor="#a855f7" stopOpacity={0.0}/>
              </linearGradient>
              <linearGradient id="healthyGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#22c55e" stopOpacity={0.4}/>
                <stop offset="95%" stopColor="#22c55e" stopOpacity={0.0}/>
              </linearGradient>
            </defs>
            <XAxis dataKey="date" tick={{ fontSize: 11, fill: '#64748b' }} axisLine={false} tickLine={false} />
            <YAxis tick={{ fontSize: 11, fill: '#64748b' }} axisLine={false} tickLine={false} />
            <Tooltip
              contentStyle={{ backgroundColor: '#0f172a', borderRadius: '12px', border: 'none', color: '#fff', fontSize: '12px' }}
              itemStyle={{ color: '#fff' }}
            />
            <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '10px' }} />
            <Area type="monotone" dataKey="diseases" name="Diseases" stroke="#ef4444" strokeWidth={2} fillOpacity={1} fill="url(#diseaseGrad)" />
            <Area type="monotone" dataKey="pests" name="Pests" stroke="#a855f7" strokeWidth={2} fillOpacity={1} fill="url(#pestGrad)" />
            <Area type="monotone" dataKey="healthy" name="Healthy" stroke="#22c55e" strokeWidth={2} fillOpacity={1} fill="url(#healthyGrad)" />
          </AreaChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}
