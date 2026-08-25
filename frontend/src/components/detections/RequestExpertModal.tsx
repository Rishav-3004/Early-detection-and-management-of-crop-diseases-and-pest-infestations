'use client';

import React, { useState } from 'react';
import { Modal } from '@/components/ui/Modal';
import { Button } from '@/components/ui/Button';
import { CheckCircle2, UserCheck, AlertCircle } from 'lucide-react';

interface RequestExpertModalProps {
  isOpen: boolean;
  onClose: () => void;
  detectionId: string;
  diseaseLabel: string;
}

export function RequestExpertModal({
  isOpen,
  onClose,
  detectionId,
  diseaseLabel,
}: RequestExpertModalProps) {
  const [notes, setNotes] = useState('');
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    // Simulate submission to review queue
    setTimeout(() => {
      setIsLoading(false);
      setIsSubmitted(true);
    }, 600);
  };

  const handleClose = () => {
    setIsSubmitted(false);
    setNotes('');
    onClose();
  };

  return (
    <Modal
      isOpen={isOpen}
      onClose={handleClose}
      title="Request Agronomist Case Review"
      description={`Submit scan (${diseaseLabel}) for human expert diagnosis and tailored treatment plan.`}
    >
      {isSubmitted ? (
        <div className="text-center py-6 space-y-3">
          <div className="w-12 h-12 rounded-full bg-emerald-100 text-emerald-600 mx-auto flex items-center justify-center">
            <CheckCircle2 className="w-7 h-7" />
          </div>
          <h4 className="text-sm font-bold text-slate-800">Case Submitted Successfully</h4>
          <p className="text-xs text-slate-500 max-w-xs mx-auto">
            Our certified agricultural extension officers will review this case and provide tailored advice. You will receive an in-app notification once verified.
          </p>
          <Button onClick={handleClose} size="sm" className="mt-3">
            Done
          </Button>
        </div>
      ) : (
        <form onSubmit={handleSubmit} className="space-y-4 text-xs">
          <div className="p-3 bg-emerald-50 rounded-xl border border-emerald-200 text-emerald-900 flex items-start gap-2">
            <UserCheck className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
            <p>
              An assigned agronomist will inspect the original leaf image, cross-reference local climate alerts, and either confirm or correct the diagnosis.
            </p>
          </div>

          <div className="space-y-1.5">
            <label className="font-semibold text-slate-700">Additional Field Observations (Optional)</label>
            <textarea
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              placeholder="e.g. Symptoms started 3 days after heavy rainfall; lower leaves turning yellow first..."
              rows={3}
              className="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-800 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-emerald-500"
            />
          </div>

          <div className="flex items-center justify-end gap-2 pt-2 border-t border-slate-100">
            <Button type="button" variant="ghost" size="sm" onClick={handleClose}>
              Cancel
            </Button>
            <Button type="submit" size="sm" isLoading={isLoading}>
              Submit Case for Review
            </Button>
          </div>
        </form>
      )}
    </Modal>
  );
}
