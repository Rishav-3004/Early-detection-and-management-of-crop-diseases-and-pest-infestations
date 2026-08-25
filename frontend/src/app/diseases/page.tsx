'use client';

import React, { useState, useEffect } from 'react';
import { knowledgeService } from '@/services/knowledge';
import { Disease, Crop } from '@/types';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { ShieldAlert, Search, Filter, Leaf, Info, AlertTriangle, CheckCircle2 } from 'lucide-react';

export default function DiseasesPage() {
  const [diseases, setDiseases] = useState<Disease[]>([]);
  const [crops, setCrops] = useState<Crop[]>([]);
  const [selectedCropId, setSelectedCropId] = useState<string>('');
  const [search, setSearch] = useState('');
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    knowledgeService.listCrops().then(setCrops).catch(() => {});
  }, []);

  useEffect(() => {
    setIsLoading(true);
    knowledgeService.listDiseases(selectedCropId || undefined)
      .then(setDiseases)
      .catch(() => setDiseases([]))
      .finally(() => setIsLoading(false));
  }, [selectedCropId]);

  const filtered = diseases.filter((d) =>
    d.name.toLowerCase().includes(search.toLowerCase()) ||
    (d.scientific_name && d.scientific_name.toLowerCase().includes(search.toLowerCase())) ||
    d.description.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="p-2 rounded-xl bg-red-100 text-red-800">
              <ShieldAlert className="w-5 h-5" />
            </span>
            <h1 className="text-xl md:text-2xl font-extrabold text-slate-900 tracking-tight">
              Foliar Disease Knowledge Catalog
            </h1>
          </div>
          <p className="text-xs text-slate-500 mt-1">
            Scientific reference database of crop pathogens, concentric lesions, chlorosis indicators, and biological management.
          </p>
        </div>
      </div>

      {/* Filter Bar */}
      <Card className="p-4">
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
          <div className="relative sm:col-span-2">
            <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search by disease name, pathogen, or symptoms..."
              className="w-full pl-9 pr-3 py-2 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-800 focus:outline-none focus:ring-2 focus:ring-emerald-500"
            />
          </div>

          <div>
            <select
              value={selectedCropId}
              onChange={(e) => setSelectedCropId(e.target.value)}
              className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-800 focus:outline-none focus:ring-2 focus:ring-emerald-500"
            >
              <option value="">All Crop Types</option>
              {crops.map((c) => (
                <option key={c.id} value={c.id}>
                  {c.name}
                </option>
              ))}
            </select>
          </div>
        </div>
      </Card>

      {/* Disease Cards Grid */}
      {isLoading ? (
        <div className="py-20 text-center text-slate-400">
          <div className="w-8 h-8 border-2 border-emerald-500 border-t-transparent rounded-full animate-spin mx-auto mb-2" />
          <p className="text-xs">Loading disease encyclopedias...</p>
        </div>
      ) : filtered.length === 0 ? (
        <Card className="p-12 text-center text-slate-400 text-xs">
          No disease records matched your filter.
        </Card>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {filtered.map((d) => (
            <Card key={d.id} className="border border-slate-200 space-y-4 p-5 flex flex-col justify-between">
              <div>
                <div className="flex items-start justify-between gap-2">
                  <div>
                    <h3 className="text-base font-bold text-slate-900">{d.name}</h3>
                    {d.scientific_name && (
                      <p className="text-xs text-slate-400 italic mt-0.5">Pathogen: {d.scientific_name}</p>
                    )}
                  </div>
                  <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase bg-red-100 text-red-800 border border-red-200">
                    Foliar Disease
                  </span>
                </div>

                <p className="text-xs text-slate-600 mt-3 leading-relaxed">{d.description}</p>

                {d.symptoms && d.symptoms.length > 0 && (
                  <div className="mt-4 space-y-1.5 bg-slate-50 p-3 rounded-xl border border-slate-100">
                    <span className="text-[11px] font-bold text-slate-700 uppercase tracking-wider flex items-center gap-1">
                      <AlertTriangle className="w-3.5 h-3.5 text-amber-500" /> Key Visual Symptoms
                    </span>
                    <ul className="text-xs text-slate-600 list-disc pl-4 space-y-1">
                      {d.symptoms.map((s, i) => (
                        <li key={i}>{s}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>

              {d.prevention && d.prevention.length > 0 && (
                <div className="pt-3 border-t border-slate-100 text-xs text-slate-600">
                  <span className="text-[11px] font-bold text-emerald-800 flex items-center gap-1 mb-1">
                    <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" /> Recommended Preventative Strategy
                  </span>
                  <p className="text-[11px] text-slate-600">{d.prevention[0]}</p>
                </div>
              )}
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
