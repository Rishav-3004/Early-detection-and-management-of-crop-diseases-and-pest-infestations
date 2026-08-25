'use client';

import React, { useState, useEffect } from 'react';
import { useAuth } from '@/lib/auth';
import { translations } from '@/lib/i18n';
import { farmService } from '@/services/farms';
import { knowledgeService } from '@/services/knowledge';
import { detectionService } from '@/services/detections';
import { Farm, Field, Crop, Detection } from '@/types';
import { ScanDropzone } from '@/components/scan/ScanDropzone';
import { AnalysisProgress } from '@/components/scan/AnalysisProgress';
import { DiagnosisResultCard } from '@/components/scan/DiagnosisResultCard';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import {
  ScanLine,
  Sprout,
  MapPin,
  CheckCircle2,
  AlertCircle,
  Sparkles,
  HelpCircle,
  Camera,
  RotateCcw
} from 'lucide-react';

export default function ScanPage() {
  const { user, language } = useAuth();
  const t = translations[language] || translations.en;

  const [farms, setFarms] = useState<Farm[]>([]);
  const [crops, setCrops] = useState<Crop[]>([]);
  const [selectedFarmId, setSelectedFarmId] = useState<string>('');
  const [selectedFieldId, setSelectedFieldId] = useState<string>('');
  const [selectedCropId, setSelectedCropId] = useState<string>('');

  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [detectionResult, setDetectionResult] = useState<Detection | null>(null);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  useEffect(() => {
    farmService.listFarms().then((f) => {
      setFarms(f);
      if (f.length > 0) {
        setSelectedFarmId(f[0].id);
        if (f[0].fields && f[0].fields.length > 0) {
          setSelectedFieldId(f[0].fields[0].id);
          if (f[0].fields[0].crop_id) {
            setSelectedCropId(f[0].fields[0].crop_id);
          }
        }
      }
    }).catch(() => {});

    knowledgeService.listCrops().then(setCrops).catch(() => {});
  }, [user]);

  const handleFarmChange = (farmId: string) => {
    setSelectedFarmId(farmId);
    const farm = farms.find((f) => f.id === farmId);
    if (farm && farm.fields && farm.fields.length > 0) {
      setSelectedFieldId(farm.fields[0].id);
      if (farm.fields[0].crop_id) {
        setSelectedCropId(farm.fields[0].crop_id);
      }
    } else {
      setSelectedFieldId('');
    }
  };

  const handleFieldChange = (fieldId: string) => {
    setSelectedFieldId(fieldId);
    const farm = farms.find((f) => f.id === selectedFarmId);
    const field = farm?.fields.find((fld) => fld.id === fieldId);
    if (field && field.crop_id) {
      setSelectedCropId(field.crop_id);
    }
  };

  const handleRunScan = async () => {
    if (!selectedFile) {
      setErrorMsg("Please upload or take a leaf photo first.");
      return;
    }

    setErrorMsg(null);
    setIsAnalyzing(true);
    setDetectionResult(null);

    try {
      const result = await detectionService.scanCrop(selectedFile, {
        farm_id: selectedFarmId || undefined,
        field_id: selectedFieldId || undefined,
        crop_id: selectedCropId || undefined,
      });

      setDetectionResult(result);
    } catch (err: any) {
      setErrorMsg(err.message || "Diagnostic analysis failed. Please try again with a clearer image.");
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleReset = () => {
    setSelectedFile(null);
    setDetectionResult(null);
    setErrorMsg(null);
  };

  const activeFarm = farms.find((f) => f.id === selectedFarmId);
  const fieldsOfFarm = activeFarm?.fields || [];

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      {/* Header Banner */}
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="p-2 rounded-xl bg-emerald-100 text-emerald-800">
              <ScanLine className="w-5 h-5" />
            </span>
            <h1 className="text-xl md:text-2xl font-extrabold text-slate-900 tracking-tight">
              {t.scanTitle}
            </h1>
          </div>
          <p className="text-xs text-slate-500 mt-1 max-w-2xl">
            {t.scanSubtitle}
          </p>
        </div>

        {detectionResult && (
          <Button
            variant="outline"
            size="sm"
            onClick={handleReset}
            leftIcon={<RotateCcw className="w-4 h-4 text-emerald-600" />}
          >
            New Scan
          </Button>
        )}
      </div>

      {errorMsg && (
        <div className="p-4 bg-red-50 border border-red-200 rounded-2xl text-xs text-red-800 flex items-center gap-3">
          <AlertCircle className="w-5 h-5 text-red-600 shrink-0" />
          <span className="font-medium">{errorMsg}</span>
        </div>
      )}

      {/* Main Scan Workflow */}
      {!detectionResult ? (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left 2 Cols: Dropzone & Action */}
          <div className="lg:col-span-2 space-y-6">
            <Card className="p-6 space-y-5">
              {/* Optional Field Assignment */}
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 p-3 bg-slate-50 border border-slate-200/70 rounded-2xl">
                <div className="space-y-1">
                  <label className="text-[11px] font-bold text-slate-600 uppercase tracking-wider flex items-center gap-1">
                    <MapPin className="w-3.5 h-3.5 text-emerald-600" /> {t.selectFarm}
                  </label>
                  <select
                    value={selectedFarmId}
                    onChange={(e) => handleFarmChange(e.target.value)}
                    className="w-full px-2.5 py-1.5 bg-white border border-slate-200 rounded-xl text-xs text-slate-800 focus:outline-none focus:ring-2 focus:ring-emerald-500"
                  >
                    <option value="">-- General Scan --</option>
                    {farms.map((f) => (
                      <option key={f.id} value={f.id}>
                        {f.name}
                      </option>
                    ))}
                  </select>
                </div>

                <div className="space-y-1">
                  <label className="text-[11px] font-bold text-slate-600 uppercase tracking-wider flex items-center gap-1">
                    <Sprout className="w-3.5 h-3.5 text-emerald-600" /> {t.selectField}
                  </label>
                  <select
                    value={selectedFieldId}
                    onChange={(e) => handleFieldChange(e.target.value)}
                    className="w-full px-2.5 py-1.5 bg-white border border-slate-200 rounded-xl text-xs text-slate-800 focus:outline-none focus:ring-2 focus:ring-emerald-500"
                  >
                    <option value="">-- None / Select Field --</option>
                    {fieldsOfFarm.map((fld) => (
                      <option key={fld.id} value={fld.id}>
                        {fld.name}
                      </option>
                    ))}
                  </select>
                </div>

                <div className="space-y-1">
                  <label className="text-[11px] font-bold text-slate-600 uppercase tracking-wider flex items-center gap-1">
                    <Sparkles className="w-3.5 h-3.5 text-emerald-600" /> {t.selectCrop}
                  </label>
                  <select
                    value={selectedCropId}
                    onChange={(e) => setSelectedCropId(e.target.value)}
                    className="w-full px-2.5 py-1.5 bg-white border border-slate-200 rounded-xl text-xs text-slate-800 focus:outline-none focus:ring-2 focus:ring-emerald-500"
                  >
                    <option value="">Auto-Detect Crop</option>
                    {crops.map((c) => (
                      <option key={c.id} value={c.id}>
                        {c.name}
                      </option>
                    ))}
                  </select>
                </div>
              </div>

              {/* Upload Dropzone */}
              <ScanDropzone
                selectedFile={selectedFile}
                onFileSelect={(f) => {
                  setSelectedFile(f);
                  setErrorMsg(null);
                }}
                onClear={() => setSelectedFile(null)}
                isLoading={isAnalyzing}
              />

              {/* Run Scan Button */}
              <Button
                type="button"
                variant="primary"
                size="lg"
                className="w-full text-base font-bold shadow-md hover:shadow-lg"
                disabled={!selectedFile || isAnalyzing}
                isLoading={isAnalyzing}
                onClick={handleRunScan}
                leftIcon={<ScanLine className="w-5 h-5" />}
              >
                {isAnalyzing ? "Analyzing Plant Foliage..." : t.startScan}
              </Button>
            </Card>

            {/* Analysis Progress Stepper Animation */}
            {isAnalyzing && <AnalysisProgress isAnalyzing={isAnalyzing} />}
          </div>

          {/* Right Col: Guidelines & Instructions */}
          <div className="space-y-6">
            <Card className="p-5 border border-slate-200 space-y-4">
              <h3 className="text-xs font-bold text-slate-800 uppercase tracking-wider flex items-center gap-1.5">
                <HelpCircle className="w-4 h-4 text-emerald-600" /> Best Practices for Best Results
              </h3>
              <ul className="text-xs text-slate-600 space-y-2.5">
                <li className="flex items-start gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0 mt-0.5" />
                  <span><strong>Close-up framing:</strong> Keep the affected leaf centered and fill at least 70% of the image.</span>
                </li>
                <li className="flex items-start gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0 mt-0.5" />
                  <span><strong>Natural diffuse light:</strong> Avoid deep shadows, flash glare, or direct blinding sunlight.</span>
                </li>
                <li className="flex items-start gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0 mt-0.5" />
                  <span><strong>Sharp focus:</strong> Avoid blurry or shaking camera motion; ensure lesion margins are sharp.</span>
                </li>
                <li className="flex items-start gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0 mt-0.5" />
                  <span><strong>Capture active symptoms:</strong> Include visible discoloration, fungal dust, concentric rings, or insect bore holes.</span>
                </li>
              </ul>
            </Card>

            <Card className="p-5 border border-slate-200 bg-slate-50/60 space-y-2 text-xs text-slate-600">
              <h4 className="font-bold text-slate-800">Supported Crops</h4>
              <p className="text-[11px] text-slate-500">
                Tomato, Potato, Wheat, Rice, Maize, Cotton, Soybean, Apple, Grape, Chili, Mustard, and more.
              </p>
            </Card>
          </div>
        </div>
      ) : (
        /* Result View */
        <DiagnosisResultCard detection={detectionResult} />
      )}
    </div>
  );
}
