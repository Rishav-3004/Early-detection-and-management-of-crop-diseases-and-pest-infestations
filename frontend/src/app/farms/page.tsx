'use client';

import React, { useState, useEffect } from 'react';
import { useAuth } from '@/lib/auth';
import { farmService } from '@/services/farms';
import { knowledgeService } from '@/services/knowledge';
import { Farm, Field, Crop } from '@/types';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Modal } from '@/components/ui/Modal';
import { ProgressMeter } from '@/components/ui/ProgressMeter';
import { Badge } from '@/components/ui/Badge';
import {
  MapPin,
  PlusCircle,
  Sprout,
  Droplets,
  Layers,
  Trash2,
  Edit2,
  Calendar,
  AlertCircle
} from 'lucide-react';

export default function FarmsPage() {
  const { user } = useAuth();

  const [farms, setFarms] = useState<Farm[]>([]);
  const [crops, setCrops] = useState<Crop[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  // Farm modal
  const [isFarmModalOpen, setIsFarmModalOpen] = useState(false);
  const [farmName, setFarmName] = useState('');
  const [farmLocation, setFarmLocation] = useState('');
  const [farmArea, setFarmArea] = useState('5.0');
  const [soilType, setSoilType] = useState('Loamy');
  const [irrigationType, setIrrigationType] = useState('Drip');

  // Field modal
  const [isFieldModalOpen, setIsFieldModalOpen] = useState(false);
  const [targetFarmId, setTargetFarmId] = useState('');
  const [fieldName, setFieldName] = useState('');
  const [fieldArea, setFieldArea] = useState('1.5');
  const [selectedCropId, setSelectedCropId] = useState('');
  const [variety, setVariety] = useState('');
  const [growthStage, setGrowthStage] = useState('Vegetative');

  const loadData = async () => {
    setIsLoading(true);
    try {
      const [farmsList, cropsList] = await Promise.all([
        farmService.listFarms(),
        knowledgeService.listCrops()
      ]);
      setFarms(farmsList);
      setCrops(cropsList);
    } catch (e) {
      console.error(e);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [user]);

  const handleCreateFarm = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await farmService.createFarm({
        name: farmName,
        location: farmLocation,
        area: parseFloat(farmArea) || 1.0,
        soil_type: soilType,
        irrigation_type: irrigationType,
      });
      setIsFarmModalOpen(false);
      setFarmName('');
      setFarmLocation('');
      loadData();
    } catch (e) {
      console.error(e);
    }
  };

  const handleCreateField = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await farmService.createField({
        farm_id: targetFarmId,
        name: fieldName,
        area: parseFloat(fieldArea) || 0.5,
        crop_id: selectedCropId || undefined,
        variety: variety || undefined,
        growth_stage: growthStage,
      });
      setIsFieldModalOpen(false);
      setFieldName('');
      setVariety('');
      loadData();
    } catch (e) {
      console.error(e);
    }
  };

  const handleDeleteFarm = async (id: string) => {
    if (confirm("Are you sure you want to delete this farm and all its associated fields?")) {
      await farmService.deleteFarm(id);
      loadData();
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="p-2 rounded-xl bg-emerald-100 text-emerald-800">
              <MapPin className="w-5 h-5" />
            </span>
            <h1 className="text-xl md:text-2xl font-extrabold text-slate-900 tracking-tight">
              Farm & Field Management
            </h1>
          </div>
          <p className="text-xs text-slate-500 mt-1">
            Organize agricultural plots, soil profiles, crop cultivars, and continuous vitality scores.
          </p>
        </div>

        <Button
          variant="primary"
          size="sm"
          onClick={() => setIsFarmModalOpen(true)}
          leftIcon={<PlusCircle className="w-4 h-4" />}
        >
          Add New Farm
        </Button>
      </div>

      {/* Farms List */}
      {isLoading ? (
        <div className="py-20 text-center text-slate-400">
          <div className="w-8 h-8 border-2 border-emerald-500 border-t-transparent rounded-full animate-spin mx-auto mb-2" />
          <p className="text-xs">Loading farm registries...</p>
        </div>
      ) : farms.length === 0 ? (
        <Card className="p-12 text-center space-y-4">
          <div className="w-16 h-16 rounded-2xl bg-emerald-50 text-emerald-600 mx-auto flex items-center justify-center">
            <MapPin className="w-8 h-8" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-slate-800">No Farms Registered</h3>
            <p className="text-xs text-slate-500 mt-1 max-w-sm mx-auto">
              Create your primary cultivation farm to map fields, assign crop varieties, and track plant health indices.
            </p>
          </div>
          <Button onClick={() => setIsFarmModalOpen(true)} size="sm">
            Create First Farm
          </Button>
        </Card>
      ) : (
        <div className="space-y-6">
          {farms.map((farm) => (
            <Card key={farm.id} className="overflow-hidden border border-slate-200">
              {/* Farm Header */}
              <div className="p-5 bg-slate-900 text-white flex flex-wrap items-center justify-between gap-4">
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <MapPin className="w-4 h-4 text-emerald-400" />
                    <h3 className="text-base font-bold text-white">{farm.name}</h3>
                    <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-slate-800 text-slate-300 border border-slate-700">
                      {farm.area} Hectares
                    </span>
                  </div>
                  <p className="text-xs text-slate-400">{farm.location}</p>
                </div>

                <div className="flex items-center gap-3">
                  <div className="hidden sm:flex items-center gap-4 text-xs text-slate-300 mr-2">
                    <span className="flex items-center gap-1"><Layers className="w-3.5 h-3.5 text-amber-400" /> Soil: {farm.soil_type}</span>
                    <span className="flex items-center gap-1"><Droplets className="w-3.5 h-3.5 text-blue-400" /> Irrigation: {farm.irrigation_type}</span>
                  </div>
                  <Button
                    variant="secondary"
                    size="sm"
                    onClick={() => {
                      setTargetFarmId(farm.id);
                      setIsFieldModalOpen(true);
                    }}
                    leftIcon={<PlusCircle className="w-3.5 h-3.5" />}
                  >
                    Add Field
                  </Button>
                  <button
                    onClick={() => handleDeleteFarm(farm.id)}
                    className="p-2 text-slate-400 hover:text-red-400 transition-colors rounded-lg hover:bg-slate-800"
                    title="Delete Farm"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </div>

              {/* Fields Grid */}
              <CardContent className="p-5">
                {farm.fields && farm.fields.length > 0 ? (
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {farm.fields.map((field) => {
                      const risk = field.health_score >= 80 ? 'LOW' : field.health_score >= 60 ? 'MEDIUM' : 'HIGH';
                      return (
                        <div
                          key={field.id}
                          className="p-4 rounded-xl border border-slate-200 bg-slate-50/50 hover:bg-slate-50 transition-colors space-y-3"
                        >
                          <div className="flex items-start justify-between">
                            <div>
                              <h4 className="text-xs font-bold text-slate-900">{field.name}</h4>
                              <p className="text-[11px] text-slate-500 mt-0.5">
                                {field.crop?.name || 'Crop'} {field.variety ? `• ${field.variety}` : ''}
                              </p>
                            </div>
                            <Badge variant="risk" riskLevel={risk} />
                          </div>

                          <div className="text-[11px] text-slate-600 space-y-1">
                            <div className="flex justify-between">
                              <span>Area:</span>
                              <strong className="text-slate-800">{field.area} ha</strong>
                            </div>
                            <div className="flex justify-between">
                              <span>Growth Stage:</span>
                              <strong className="text-slate-800">{field.growth_stage}</strong>
                            </div>
                          </div>

                          <div className="pt-2 border-t border-slate-200">
                            <ProgressMeter
                              value={field.health_score}
                              label="Vitality Index"
                              colorScheme={field.health_score >= 80 ? 'green' : field.health_score >= 60 ? 'amber' : 'red'}
                            />
                          </div>
                        </div>
                      );
                    })}
                  </div>
                ) : (
                  <div className="py-6 text-center text-slate-400 text-xs">
                    No fields configured for this farm yet. Click "Add Field" to register crop sectors.
                  </div>
                )}
              </CardContent>
            </Card>
          ))}
        </div>
      )}

      {/* Modal: Create Farm */}
      <Modal
        isOpen={isFarmModalOpen}
        onClose={() => setIsFarmModalOpen(false)}
        title="Register New Farm"
        description="Add a cultivation property to group your fields and weather telemetry."
      >
        <form onSubmit={handleCreateFarm} className="space-y-4 text-xs">
          <div className="space-y-1">
            <label className="font-semibold text-slate-700">Farm Name</label>
            <input
              type="text"
              required
              value={farmName}
              onChange={(e) => setFarmName(e.target.value)}
              placeholder="e.g. Sunrise Organic Orchards"
              className="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-800 focus:outline-none focus:ring-2 focus:ring-emerald-500"
            />
          </div>

          <div className="space-y-1">
            <label className="font-semibold text-slate-700">Location / Agricultural Zone</label>
            <input
              type="text"
              required
              value={farmLocation}
              onChange={(e) => setFarmLocation(e.target.value)}
              placeholder="e.g. Punjab Agri Zone, Sector 4"
              className="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-800 focus:outline-none focus:ring-2 focus:ring-emerald-500"
            />
          </div>

          <div className="grid grid-cols-3 gap-3">
            <div className="space-y-1">
              <label className="font-semibold text-slate-700">Area (Hectares)</label>
              <input
                type="number"
                step="0.1"
                required
                value={farmArea}
                onChange={(e) => setFarmArea(e.target.value)}
                className="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-800 focus:outline-none focus:ring-2 focus:ring-emerald-500"
              />
            </div>

            <div className="space-y-1">
              <label className="font-semibold text-slate-700">Soil Type</label>
              <select
                value={soilType}
                onChange={(e) => setSoilType(e.target.value)}
                className="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-800 focus:outline-none focus:ring-2 focus:ring-emerald-500"
              >
                <option value="Loamy">Loamy</option>
                <option value="Clay Loam">Clay Loam</option>
                <option value="Sandy Loam">Sandy Loam</option>
                <option value="Black Soil">Black Soil</option>
                <option value="Alluvial">Alluvial</option>
              </select>
            </div>

            <div className="space-y-1">
              <label className="font-semibold text-slate-700">Irrigation</label>
              <select
                value={irrigationType}
                onChange={(e) => setIrrigationType(e.target.value)}
                className="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-800 focus:outline-none focus:ring-2 focus:ring-emerald-500"
              >
                <option value="Drip">Drip Irrigation</option>
                <option value="Sprinkler">Sprinkler</option>
                <option value="Furrow">Furrow</option>
                <option value="Rainfed">Rainfed</option>
              </select>
            </div>
          </div>

          <div className="flex items-center justify-end gap-2 pt-3 border-t border-slate-100">
            <Button type="button" variant="ghost" size="sm" onClick={() => setIsFarmModalOpen(false)}>
              Cancel
            </Button>
            <Button type="submit" size="sm">
              Save Farm
            </Button>
          </div>
        </form>
      </Modal>

      {/* Modal: Create Field */}
      <Modal
        isOpen={isFieldModalOpen}
        onClose={() => setIsFieldModalOpen(false)}
        title="Add Field to Farm"
        description="Register a specific plot with crop type, variety, and growth stage."
      >
        <form onSubmit={handleCreateField} className="space-y-4 text-xs">
          <div className="space-y-1">
            <label className="font-semibold text-slate-700">Field / Plot Name</label>
            <input
              type="text"
              required
              value={fieldName}
              onChange={(e) => setFieldName(e.target.value)}
              placeholder="e.g. North Plot - Tomato Sector A"
              className="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-800 focus:outline-none focus:ring-2 focus:ring-emerald-500"
            />
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div className="space-y-1">
              <label className="font-semibold text-slate-700">Crop Cultivated</label>
              <select
                value={selectedCropId}
                onChange={(e) => setSelectedCropId(e.target.value)}
                className="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-800 focus:outline-none focus:ring-2 focus:ring-emerald-500"
              >
                <option value="">Select Crop</option>
                {crops.map((c) => (
                  <option key={c.id} value={c.id}>
                    {c.name}
                  </option>
                ))}
              </select>
            </div>

            <div className="space-y-1">
              <label className="font-semibold text-slate-700">Variety / Cultivar</label>
              <input
                type="text"
                value={variety}
                onChange={(e) => setVariety(e.target.value)}
                placeholder="e.g. Arka Rakshak"
                className="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-800 focus:outline-none focus:ring-2 focus:ring-emerald-500"
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div className="space-y-1">
              <label className="font-semibold text-slate-700">Area (Hectares)</label>
              <input
                type="number"
                step="0.1"
                required
                value={fieldArea}
                onChange={(e) => setFieldArea(e.target.value)}
                className="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-800 focus:outline-none focus:ring-2 focus:ring-emerald-500"
              />
            </div>

            <div className="space-y-1">
              <label className="font-semibold text-slate-700">Growth Stage</label>
              <select
                value={growthStage}
                onChange={(e) => setGrowthStage(e.target.value)}
                className="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-800 focus:outline-none focus:ring-2 focus:ring-emerald-500"
              >
                <option value="Seedling">Seedling</option>
                <option value="Vegetative">Vegetative</option>
                <option value="Flowering & Fruit Set">Flowering & Fruit Set</option>
                <option value="Grain Filling / Bulking">Grain Filling / Bulking</option>
                <option value="Maturity">Maturity / Harvest</option>
              </select>
            </div>
          </div>

          <div className="flex items-center justify-end gap-2 pt-3 border-t border-slate-100">
            <Button type="button" variant="ghost" size="sm" onClick={() => setIsFieldModalOpen(false)}>
              Cancel
            </Button>
            <Button type="submit" size="sm">
              Save Field
            </Button>
          </div>
        </form>
      </Modal>
    </div>
  );
}
