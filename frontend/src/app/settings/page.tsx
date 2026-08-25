'use client';

import React, { useState } from 'react';
import { useAuth } from '@/lib/auth';
import { translations, SupportedLanguage } from '@/lib/i18n';
import { apiClient } from '@/lib/api';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import {
  Settings as SettingsIcon,
  Globe,
  User,
  Lock,
  CheckCircle2,
  AlertCircle
} from 'lucide-react';

export default function SettingsPage() {
  const { user, language, setLanguage, refreshUser } = useAuth();
  const t = translations[language] || translations.en;

  const [name, setName] = useState(user?.name || '');
  const [phone, setPhone] = useState(user?.phone || '');
  const [profileSuccess, setProfileSuccess] = useState(false);
  const [profileLoading, setProfileLoading] = useState(false);

  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [pwdSuccess, setPwdSuccess] = useState(false);
  const [pwdError, setPwdError] = useState<string | null>(null);
  const [pwdLoading, setPwdLoading] = useState(false);

  const handleUpdateProfile = async (e: React.FormEvent) => {
    e.preventDefault();
    setProfileLoading(true);
    setProfileSuccess(false);
    try {
      await apiClient('/auth/me', {
        method: 'PATCH',
        body: JSON.stringify({ name, phone }),
      });
      await refreshUser();
      setProfileSuccess(true);
    } catch (err) {
      console.error(err);
    } finally {
      setProfileLoading(false);
    }
  };

  const handleChangePassword = async (e: React.FormEvent) => {
    e.preventDefault();
    setPwdLoading(true);
    setPwdError(null);
    setPwdSuccess(false);
    try {
      await apiClient('/auth/change-password', {
        method: 'POST',
        body: JSON.stringify({ current_password: currentPassword, new_password: newPassword }),
      });
      setPwdSuccess(true);
      setCurrentPassword('');
      setNewPassword('');
    } catch (err: any) {
      setPwdError(err.message || 'Password update failed.');
    } finally {
      setPwdLoading(false);
    }
  };

  return (
    <div className="space-y-6 max-w-3xl mx-auto">
      {/* Header */}
      <div>
        <div className="flex items-center gap-2">
          <span className="p-2 rounded-xl bg-slate-100 text-slate-800">
            <SettingsIcon className="w-5 h-5" />
          </span>
          <h1 className="text-xl md:text-2xl font-extrabold text-slate-900 tracking-tight">
            Account & System Settings
          </h1>
        </div>
        <p className="text-xs text-slate-500 mt-1">
          Manage user profile information, interface language, and account security.
        </p>
      </div>

      {/* Language Preferences */}
      <Card className="p-5 space-y-4">
        <h3 className="text-xs font-bold text-slate-800 uppercase tracking-wider flex items-center gap-2">
          <Globe className="w-4 h-4 text-emerald-600" /> Interface Language & Regionalization
        </h3>
        <div className="grid grid-cols-3 gap-3">
          <button
            type="button"
            onClick={() => setLanguage('en')}
            className={`p-3 rounded-xl border text-center transition-all text-xs font-bold ${
              language === 'en'
                ? 'border-emerald-600 bg-emerald-50/60 text-emerald-900 shadow-xs'
                : 'border-slate-200 bg-white hover:bg-slate-50 text-slate-700'
            }`}
          >
            English
          </button>
          <button
            type="button"
            onClick={() => setLanguage('hi')}
            className={`p-3 rounded-xl border text-center transition-all text-xs font-bold ${
              language === 'hi'
                ? 'border-emerald-600 bg-emerald-50/60 text-emerald-900 shadow-xs'
                : 'border-slate-200 bg-white hover:bg-slate-50 text-slate-700'
            }`}
          >
            हिन्दी (Hindi)
          </button>
          <button
            type="button"
            onClick={() => setLanguage('pa')}
            className={`p-3 rounded-xl border text-center transition-all text-xs font-bold ${
              language === 'pa'
                ? 'border-emerald-600 bg-emerald-50/60 text-emerald-900 shadow-xs'
                : 'border-slate-200 bg-white hover:bg-slate-50 text-slate-700'
            }`}
          >
            ਪੰਜਾਬੀ (Punjabi)
          </button>
        </div>
      </Card>

      {/* Profile Info */}
      <Card className="p-5 space-y-4">
        <h3 className="text-xs font-bold text-slate-800 uppercase tracking-wider flex items-center gap-2">
          <User className="w-4 h-4 text-emerald-600" /> Profile Information
        </h3>

        {profileSuccess && (
          <div className="p-3 bg-emerald-50 border border-emerald-200 rounded-xl text-xs text-emerald-800 flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
            <span>Profile details updated successfully.</span>
          </div>
        )}

        <form onSubmit={handleUpdateProfile} className="space-y-3 text-xs">
          <div className="space-y-1">
            <label className="font-semibold text-slate-700">Full Name</label>
            <input
              type="text"
              required
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-800 focus:outline-none focus:ring-2 focus:ring-emerald-500"
            />
          </div>

          <div className="space-y-1">
            <label className="font-semibold text-slate-700">Contact Phone Number</label>
            <input
              type="text"
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
              placeholder="+91 98765 43210"
              className="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-800 focus:outline-none focus:ring-2 focus:ring-emerald-500"
            />
          </div>

          <Button type="submit" size="sm" isLoading={profileLoading}>
            Save Changes
          </Button>
        </form>
      </Card>

      {/* Password Management */}
      <Card className="p-5 space-y-4">
        <h3 className="text-xs font-bold text-slate-800 uppercase tracking-wider flex items-center gap-2">
          <Lock className="w-4 h-4 text-emerald-600" /> Security & Password
        </h3>

        {pwdSuccess && (
          <div className="p-3 bg-emerald-50 border border-emerald-200 rounded-xl text-xs text-emerald-800 flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
            <span>Password updated successfully.</span>
          </div>
        )}

        {pwdError && (
          <div className="p-3 bg-red-50 border border-red-200 rounded-xl text-xs text-red-800 flex items-center gap-2">
            <AlertCircle className="w-4 h-4 text-red-600 shrink-0" />
            <span>{pwdError}</span>
          </div>
        )}

        <form onSubmit={handleChangePassword} className="space-y-3 text-xs">
          <div className="space-y-1">
            <label className="font-semibold text-slate-700">Current Password</label>
            <input
              type="password"
              required
              value={currentPassword}
              onChange={(e) => setCurrentPassword(e.target.value)}
              className="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-800 focus:outline-none focus:ring-2 focus:ring-emerald-500"
            />
          </div>

          <div className="space-y-1">
            <label className="font-semibold text-slate-700">New Password</label>
            <input
              type="password"
              required
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
              placeholder="Minimum 6 characters"
              className="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-800 focus:outline-none focus:ring-2 focus:ring-emerald-500"
            />
          </div>

          <Button type="submit" size="sm" isLoading={pwdLoading}>
            Update Password
          </Button>
        </form>
      </Card>
    </div>
  );
}
