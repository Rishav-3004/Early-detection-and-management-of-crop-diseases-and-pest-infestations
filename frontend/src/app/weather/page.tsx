'use client';

import React, { useState, useEffect } from 'react';
import { weatherService } from '@/services/expert';
import { WeatherForecast } from '@/types';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import {
  CloudSun,
  Droplets,
  Wind,
  CloudRain,
  ShieldAlert,
  CheckCircle2,
  AlertTriangle,
  MapPin
} from 'lucide-react';

export default function WeatherPage() {
  const [forecast, setForecast] = useState<WeatherForecast | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    weatherService.getForecast()
      .then(setForecast)
      .catch(() => setForecast(null))
      .finally(() => setIsLoading(false));
  }, []);

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="p-2 rounded-xl bg-blue-100 text-blue-800">
              <CloudSun className="w-5 h-5" />
            </span>
            <h1 className="text-xl md:text-2xl font-extrabold text-slate-900 tracking-tight">
              Agricultural Weather & Disease Risk Telemetry
            </h1>
          </div>
          <p className="text-xs text-slate-500 mt-1">
            Meteorological microclimate tracking calibrated for fungal sporulation and bacterial pathogen proliferation.
          </p>
        </div>
      </div>

      {isLoading ? (
        <div className="py-20 text-center text-slate-400">
          <div className="w-8 h-8 border-2 border-emerald-500 border-t-transparent rounded-full animate-spin mx-auto mb-2" />
          <p className="text-xs">Fetching meteorological telemetry from Open-Meteo...</p>
        </div>
      ) : !forecast ? (
        <Card className="p-12 text-center text-slate-400 text-xs">
          Weather telemetry currently unavailable.
        </Card>
      ) : (
        <div className="space-y-6">
          {/* Current Weather Banner */}
          <Card className="p-6 bg-gradient-to-br from-slate-900 via-slate-850 to-emerald-950 text-white border-slate-800 space-y-5 shadow-lg">
            <div className="flex flex-wrap items-center justify-between gap-4">
              <div>
                <span className="text-xs font-mono font-bold text-emerald-400 uppercase tracking-wider flex items-center gap-1">
                  <MapPin className="w-3.5 h-3.5" /> Regional Microclimate Station
                </span>
                <h2 className="text-3xl font-extrabold text-white mt-1">
                  {Math.round(forecast.current.temperature)}°C
                </h2>
                <p className="text-xs text-slate-300 font-medium">{forecast.current.weather_condition}</p>
              </div>

              <div className="flex flex-wrap items-center gap-3">
                <div className="px-4 py-2.5 rounded-xl bg-slate-800/80 border border-slate-700 flex items-center gap-2">
                  <Droplets className="w-5 h-5 text-blue-400" />
                  <div>
                    <p className="text-[10px] text-slate-400 uppercase font-bold">Relative Humidity</p>
                    <p className="text-sm font-bold text-white">{forecast.current.humidity}%</p>
                  </div>
                </div>

                <div className="px-4 py-2.5 rounded-xl bg-slate-800/80 border border-slate-700 flex items-center gap-2">
                  <CloudRain className="w-5 h-5 text-indigo-400" />
                  <div>
                    <p className="text-[10px] text-slate-400 uppercase font-bold">Precipitation</p>
                    <p className="text-sm font-bold text-white">{forecast.current.rainfall} mm</p>
                  </div>
                </div>

                <div className="px-4 py-2.5 rounded-xl bg-slate-800/80 border border-slate-700 flex items-center gap-2">
                  <Wind className="w-5 h-5 text-slate-300" />
                  <div>
                    <p className="text-[10px] text-slate-400 uppercase font-bold">Wind Velocity</p>
                    <p className="text-sm font-bold text-white">{forecast.current.wind_speed} km/h</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Agronomic Risk Advisory */}
            <div className={`p-4 rounded-xl border flex items-start gap-3 ${
              forecast.current.high_disease_risk_warning
                ? 'bg-amber-950/60 border-amber-500/40 text-amber-200'
                : 'bg-emerald-950/60 border-emerald-500/40 text-emerald-200'
            }`}>
              {forecast.current.high_disease_risk_warning ? (
                <AlertTriangle className="w-5 h-5 text-amber-400 shrink-0 mt-0.5" />
              ) : (
                <CheckCircle2 className="w-5 h-5 text-emerald-400 shrink-0 mt-0.5" />
              )}
              <div className="text-xs space-y-1">
                <h4 className="font-bold">Agronomic Environmental Advisory</h4>
                <p className="leading-relaxed">{forecast.current.risk_assessment}</p>
              </div>
            </div>
          </Card>

          {/* 5-Day Forecast Grid */}
          <div className="space-y-3">
            <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
              <CloudSun className="w-4 h-4 text-emerald-600" />
              5-Day Agronomic Risk Outlook
            </h3>

            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-5 gap-3">
              {forecast.forecast.map((day, i) => (
                <Card key={i} className="p-4 border border-slate-200 text-center space-y-3 hover:border-emerald-400 transition-colors">
                  <p className="text-xs font-bold text-slate-800">{day.date}</p>
                  <div className="w-10 h-10 rounded-2xl bg-slate-100 text-slate-700 mx-auto flex items-center justify-center">
                    <CloudSun className="w-5 h-5 text-emerald-600" />
                  </div>
                  <div>
                    <span className="text-base font-extrabold text-slate-900">{day.temp_max}°</span>
                    <span className="text-xs text-slate-400 ml-1">/ {day.temp_min}°</span>
                    <p className="text-[11px] text-slate-500 mt-0.5">{day.condition}</p>
                  </div>
                  <div className="text-[10px] text-slate-600 space-y-0.5 pt-2 border-t border-slate-100">
                    <p>RH: {day.humidity}%</p>
                    <p>Rain: {day.rainfall}mm</p>
                  </div>
                  <div>
                    {day.disease_favorable ? (
                      <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-100 text-amber-800">
                        ⚠ Fungal Risk
                      </span>
                    ) : (
                      <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-100 text-emerald-800">
                        ✓ Low Risk
                      </span>
                    )}
                  </div>
                </Card>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
