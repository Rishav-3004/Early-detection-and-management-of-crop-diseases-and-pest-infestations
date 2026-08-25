'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/lib/auth';
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Leaf, Lock, Mail, AlertCircle, ArrowRight, UserCheck, Shield, Sprout } from 'lucide-react';

export default function LoginPage() {
  const router = useRouter();
  const { login, loginAsDemo } = useAuth();

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMsg(null);
    setIsLoading(true);
    try {
      await login(email, password);
      router.push('/dashboard');
    } catch (err: any) {
      setErrorMsg(err.message || 'Login failed. Please check your credentials.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleDemo = async (role: 'FARMER' | 'EXPERT' | 'ADMIN') => {
    setErrorMsg(null);
    setIsLoading(true);
    try {
      await loginAsDemo(role);
      router.push('/dashboard');
    } catch (err: any) {
      setErrorMsg(err.message || 'Demo login failed');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4 bg-gradient-to-br from-slate-950 via-slate-900 to-emerald-950">
      <div className="w-full max-w-md space-y-6">
        {/* Brand Header */}
        <div className="text-center space-y-2">
          <div className="w-12 h-12 rounded-2xl bg-emerald-500 text-slate-950 mx-auto flex items-center justify-center shadow-lg shadow-emerald-500/20">
            <Leaf className="w-7 h-7 fill-slate-950" />
          </div>
          <h1 className="text-2xl font-extrabold text-white tracking-tight">AgriShield AI</h1>
          <p className="text-xs text-emerald-400 font-medium">Early Detection & Agronomic Crop Protection Platform</p>
        </div>

        {/* Login Card */}
        <Card className="border border-slate-800 shadow-2xl bg-slate-900/90 backdrop-blur-md">
          <CardHeader className="border-b border-slate-800 pb-4">
            <CardTitle className="text-slate-100">Sign in to your account</CardTitle>
            <CardDescription className="text-slate-400">Access your farm diagnostics, risk monitors, and agronomic reports</CardDescription>
          </CardHeader>

          <CardContent className="pt-6 space-y-4">
            {errorMsg && (
              <div className="p-3 bg-red-950/60 border border-red-800/80 rounded-xl text-xs text-red-200 flex items-center gap-2">
                <AlertCircle className="w-4 h-4 shrink-0 text-red-400" />
                <span>{errorMsg}</span>
              </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="space-y-1.5">
                <label className="text-xs font-semibold text-slate-300">Email Address</label>
                <div className="relative">
                  <Mail className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" />
                  <input
                    type="email"
                    required
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="farmer@example.com"
                    className="w-full pl-9 pr-3 py-2 bg-slate-800/80 border border-slate-700 rounded-xl text-xs text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-emerald-500"
                  />
                </div>
              </div>

              <div className="space-y-1.5">
                <div className="flex items-center justify-between">
                  <label className="text-xs font-semibold text-slate-300">Password</label>
                  <span className="text-[11px] text-slate-500">Default: Password123!</span>
                </div>
                <div className="relative">
                  <Lock className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" />
                  <input
                    type="password"
                    required
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="••••••••"
                    className="w-full pl-9 pr-3 py-2 bg-slate-800/80 border border-slate-700 rounded-xl text-xs text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-emerald-500"
                  />
                </div>
              </div>

              <Button type="submit" className="w-full mt-2" isLoading={isLoading} rightIcon={<ArrowRight className="w-4 h-4" />}>
                Sign In
              </Button>
            </form>

            {/* Quick Demo Logins */}
            <div className="pt-4 border-t border-slate-800 space-y-2">
              <p className="text-[11px] font-semibold text-slate-400 text-center uppercase tracking-wider">
                Instant Demo Account Sign-In
              </p>
              <div className="grid grid-cols-3 gap-2">
                <button
                  type="button"
                  onClick={() => handleDemo('FARMER')}
                  className="p-2 rounded-xl bg-slate-800 hover:bg-slate-750 border border-slate-700 hover:border-emerald-500 text-left transition-all text-xs flex flex-col items-center gap-1 group"
                >
                  <Sprout className="w-4 h-4 text-emerald-400 group-hover:scale-110 transition-transform" />
                  <span className="font-bold text-slate-200 text-[11px]">Farmer</span>
                  <span className="text-[9px] text-slate-500">Scan & History</span>
                </button>

                <button
                  type="button"
                  onClick={() => handleDemo('EXPERT')}
                  className="p-2 rounded-xl bg-slate-800 hover:bg-slate-750 border border-slate-700 hover:border-blue-500 text-left transition-all text-xs flex flex-col items-center gap-1 group"
                >
                  <UserCheck className="w-4 h-4 text-blue-400 group-hover:scale-110 transition-transform" />
                  <span className="font-bold text-slate-200 text-[11px]">Agronomist</span>
                  <span className="text-[9px] text-slate-500">Review Cases</span>
                </button>

                <button
                  type="button"
                  onClick={() => handleDemo('ADMIN')}
                  className="p-2 rounded-xl bg-slate-800 hover:bg-slate-750 border border-slate-700 hover:border-purple-500 text-left transition-all text-xs flex flex-col items-center gap-1 group"
                >
                  <Shield className="w-4 h-4 text-purple-400 group-hover:scale-110 transition-transform" />
                  <span className="font-bold text-slate-200 text-[11px]">Admin</span>
                  <span className="text-[9px] text-slate-500">Analytics & ML</span>
                </button>
              </div>
            </div>
          </CardContent>

          <CardFooter className="bg-slate-950/60 border-t border-slate-800/80 justify-center">
            <p className="text-xs text-slate-400">
              Don't have an account?{' '}
              <Link href="/register" className="text-emerald-400 hover:underline font-semibold">
                Register here
              </Link>
            </p>
          </CardFooter>
        </Card>
      </div>
    </div>
  );
}
