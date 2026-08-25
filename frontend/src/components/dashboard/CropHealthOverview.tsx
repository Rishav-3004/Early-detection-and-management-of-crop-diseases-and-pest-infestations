import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card';
import { ProgressMeter } from '@/components/ui/ProgressMeter';
import { Badge } from '@/components/ui/Badge';
import { Field } from '@/types';
import Link from 'next/link';
import { ArrowRight, Sprout } from 'lucide-react';

interface CropHealthOverviewProps {
  fields: Field[];
}

export function CropHealthOverview({ fields = [] }: CropHealthOverviewProps) {
  return (
    <Card className="h-full flex flex-col">
      <CardHeader>
        <div className="flex items-center gap-2">
          <Sprout className="w-4 h-4 text-emerald-600" />
          <CardTitle>Field Crop Health Status</CardTitle>
        </div>
        <Link href="/farms" className="text-xs font-semibold text-emerald-600 hover:text-emerald-700 flex items-center gap-1">
          Manage Farms <ArrowRight className="w-3.5 h-3.5" />
        </Link>
      </CardHeader>
      <CardContent className="space-y-4 flex-1">
        {fields.length === 0 ? (
          <div className="text-center py-8 text-slate-400 text-xs">
            No fields created yet. Add your first farm & field to start crop monitoring.
          </div>
        ) : (
          fields.map((f) => {
            const riskLevel = f.health_score >= 80 ? 'LOW' : f.health_score >= 60 ? 'MEDIUM' : 'HIGH';
            return (
              <div
                key={f.id}
                className="p-3.5 rounded-xl border border-slate-100 bg-slate-50/50 hover:bg-slate-50 transition-colors space-y-2"
              >
                <div className="flex items-center justify-between">
                  <div>
                    <h4 className="text-xs font-bold text-slate-800">{f.name}</h4>
                    <p className="text-[11px] text-slate-500">
                      {f.crop?.name || 'Assigned Crop'} {f.variety ? `(${f.variety})` : ''} • {f.growth_stage || 'Vegetative'}
                    </p>
                  </div>
                  <Badge variant="risk" riskLevel={riskLevel} />
                </div>
                <ProgressMeter
                  value={f.health_score}
                  label="Health Index"
                  subLabel="Platform estimated vitality score based on recent scouting"
                  colorScheme={f.health_score >= 80 ? 'green' : f.health_score >= 60 ? 'amber' : 'red'}
                />
              </div>
            );
          })
        )}
      </CardContent>
    </Card>
  );
}
