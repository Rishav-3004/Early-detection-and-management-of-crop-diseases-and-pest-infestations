'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/lib/auth';
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Leaf, Lock, Mail, User as UserIcon, Phone, AlertCircle, ArrowRight } from 'lucide-react';

export default function RegisterPage() {
  const router = useRouter();
  const { register } = useAuth();

  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [phone, setPhone] = useState('');
  const [role, setRole] = useState('FARMER');
  const [language, setLanguage] = useState('en');
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMsg(null);
    setIsLoading(true);
    try {
      await register(name, email, password, role, phone, language);
      router.push('/dashboard');
    } catch (err: any) {
      setErrorMsg(err.message || 'Registration failed.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4 bg-gradient-to-br from-slate-950 via-slate-900 to-emerald-950">
      <div className="w-full max-w-md space-y-6">
        <div className="text-center space-y-2">
          <div className="w-12 h-12 rounded-2xl bg-emerald-500 text-slate-950 mx-auto flex items-center justify-center shadow-lg shadow-emerald-500/20">
            <Leaf className="w-7 h-7 fill-slate-950" />
          </div>
          <h1 className="text-2xl font-extrabold text-white tracking-tight">Create an Account</h1>
          <p className="text-xs text-emerald-400 font-medium">Join the AgriShield AI Crop Health Network</p>
        </div>

        <Card className="border border-slate-800 shadow-2xl bg-slate-900/90 backdrop-blur-md">
          <CardHeader className="border-b border-slate-800 pb-4">
            <CardTitle className="text-slate-100">Farmer & Expert Registration</CardTitle>
            <CardDescription className="text-slate-400">Set up your agricultural profile and begin diagnostic monitoring</CardDescription>
          </CardHeader>

          <CardContent className="pt-6 space-y-4">
            {errorMsg && (
              <div className="p-3 bg-red-950/60 border border-red-800/80 rounded-xl text-xs text-red-200 flex items-center gap-2">
                <AlertCircle className="w-4 h-4 shrink-0 text-red-400" />
                <span>{errorMsg}</span>
              </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-3.5">
              <div className="space-y-1">
                <label className="text-xs font-semibold text-slate-300">Full Name</label>
                <div className="relative">
                  <UserIcon className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" />
                  <input
                    type="text"
                    required
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    placeholder="Rohan Patel"
                    className="w-full pl-9 pr-3 py-2 bg-slate-800/80 border border-slate-700 rounded-xl text-xs text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-emerald-500"
                  />
                </div>
              </div>

              <div className="space-y-1">
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

              <div className="space-y-1">
                <label className="text-xs font-semibold text-slate-300">Password</label>
                <div className="relative">
                  <Lock className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" />
                  <input
                    type="password"
                    required
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="At least 6 characters"
                    className="w-full pl-9 pr-3 py-2 bg-slate-800/80 border border-slate-700 rounded-xl text-xs text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-emerald-500"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div className="space-y-1">
                  <label className="text-xs font-semibold text-slate-300">Primary Role</label>
                  <select
                    value={role}
                    onChange={(e) => setRole(e.target.value)}
                    className="w-full px-3 py-2 bg-slate-800/80 border border-slate-700 rounded-xl text-xs text-slate-100 focus:outline-none focus:ring-2 focus:ring-emerald-500"
                  >
                    <option value="FARMER">Farmer / Cultivator</option>
                    <option value="EXPERT">Agronomist / Expert</option>
                  </select>
                </div>

                <div className="space-y-1">
                  <label className="text-xs font-semibold text-slate-300">Language</label>
                  <select
                    value={language}
                    onChange={(e) => setLanguage(e.target.value)}
                    className="w-full px-3 py-2 bg-slate-800/80 border border-slate-700 rounded-xl text-xs text-slate-100 focus:outline-none focus:ring-2 focus:ring-emerald-500"
                  >
                    <option value="en">English</option>
                    <option value="hi">हिन्दी (Hindi)</option>
                    <option value="pa">ਪੰਜਾਬੀ (Punjabi)</option>
                  </select>
                </div>
              </div>

              <Button type="submit" className="w-full mt-3" isLoading={isLoading} rightIcon={<ArrowRight className="w-4 h-4" />}>
                Create Account
              </Button>
            </form>
          </CardContent>

          <CardFooter className="bg-slate-950/60 border-t border-slate-800/80 justify-center">
            <p className="text-xs text-slate-400">
              Already have an account?{' '}
              <Link href="/login" className="text-emerald-400 hover:underline font-semibold">
                Sign in
              </Link>
            </p>
          </CardFooter>
        </Card>
      </div>
    </div>
  );
}
