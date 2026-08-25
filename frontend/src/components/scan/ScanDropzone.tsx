'use client';

import React, { useState, useRef } from 'react';
import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { UploadCloud, Camera, Image as ImageIcon, X, AlertCircle } from 'lucide-react';

interface ScanDropzoneProps {
  onFileSelect: (file: File) => void;
  selectedFile: File | null;
  onClear: () => void;
  isLoading: boolean;
}

export function ScanDropzone({
  onFileSelect,
  selectedFile,
  onClear,
  isLoading,
}: ScanDropzoneProps) {
  const [isDragOver, setIsDragOver] = useState(false);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const cameraInputRef = useRef<HTMLInputElement>(null);

  const validateAndHandle = (file: File) => {
    setErrorMsg(null);
    const validExtensions = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp'];
    if (!validExtensions.includes(file.type)) {
      setErrorMsg("Please upload a valid image (JPG, PNG, or WEBP).");
      return;
    }
    if (file.size > 15 * 1024 * 1024) {
      setErrorMsg("Image size exceeds the 15MB limit.");
      return;
    }

    const url = URL.createObjectURL(file);
    setPreviewUrl(url);
    onFileSelect(file);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      validateAndHandle(e.dataTransfer.files[0]);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      validateAndHandle(e.target.files[0]);
    }
  };

  const handleRemove = () => {
    if (previewUrl) URL.revokeObjectURL(previewUrl);
    setPreviewUrl(null);
    setErrorMsg(null);
    onClear();
  };

  return (
    <div className="space-y-4">
      {errorMsg && (
        <div className="p-3 bg-red-50 border border-red-200 rounded-xl text-xs text-red-700 flex items-center gap-2">
          <AlertCircle className="w-4 h-4 shrink-0 text-red-500" />
          <span>{errorMsg}</span>
        </div>
      )}

      {selectedFile && previewUrl ? (
        <Card className="p-4 border-2 border-emerald-500/40 relative overflow-hidden bg-slate-900">
          <div className="relative aspect-video max-h-80 w-full rounded-xl overflow-hidden flex items-center justify-center bg-black">
            <img
              src={previewUrl}
              alt="Uploaded plant scan"
              className="max-h-full max-w-full object-contain"
            />
            <button
              onClick={handleRemove}
              disabled={isLoading}
              className="absolute top-3 right-3 p-1.5 rounded-full bg-slate-900/80 text-white hover:bg-red-600 transition-colors shadow-md"
              title="Remove image"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
          <div className="mt-3 flex items-center justify-between text-xs text-slate-300">
            <div className="flex items-center gap-2 truncate">
              <ImageIcon className="w-4 h-4 text-emerald-400 shrink-0" />
              <span className="truncate font-medium">{selectedFile.name}</span>
              <span className="text-slate-500">({(selectedFile.size / (1024 * 1024)).toFixed(2)} MB)</span>
            </div>
            <button
              onClick={() => fileInputRef.current?.click()}
              disabled={isLoading}
              className="text-emerald-400 hover:text-emerald-300 font-semibold underline text-xs"
            >
              Replace Photo
            </button>
          </div>
        </Card>
      ) : (
        <div
          onDragOver={(e) => { e.preventDefault(); setIsDragOver(true); }}
          onDragLeave={() => setIsDragOver(false)}
          onDrop={handleDrop}
          className={`border-2 border-dashed rounded-2xl p-8 text-center transition-all duration-200 cursor-pointer flex flex-col items-center justify-center ${
            isDragOver
              ? 'border-emerald-500 bg-emerald-50/50 scale-[1.01]'
              : 'border-slate-300 hover:border-emerald-400 bg-white hover:bg-slate-50/60'
          }`}
          onClick={() => fileInputRef.current?.click()}
        >
          <div className="w-16 h-16 rounded-2xl bg-emerald-100/80 text-emerald-700 flex items-center justify-center mb-4 shadow-xs">
            <UploadCloud className="w-8 h-8" />
          </div>
          <h3 className="text-sm font-bold text-slate-800">
            Drag & drop crop image here, or browse files
          </h3>
          <p className="text-xs text-slate-500 mt-1 max-w-sm">
            High-resolution JPG, PNG, or WEBP photos up to 15MB. Center affected plant foliage in frame.
          </p>

          <div className="mt-6 flex flex-wrap items-center justify-center gap-3" onClick={(e) => e.stopPropagation()}>
            <Button
              type="button"
              variant="outline"
              size="sm"
              leftIcon={<ImageIcon className="w-4 h-4 text-emerald-600" />}
              onClick={() => fileInputRef.current?.click()}
            >
              Select Photo
            </Button>
            <Button
              type="button"
              variant="secondary"
              size="sm"
              leftIcon={<Camera className="w-4 h-4 text-emerald-700" />}
              onClick={() => cameraInputRef.current?.click()}
            >
              Open Camera
            </Button>
          </div>
        </div>
      )}

      {/* Hidden Inputs */}
      <input
        ref={fileInputRef}
        type="file"
        accept="image/jpeg,image/png,image/webp"
        className="hidden"
        onChange={handleFileChange}
      />
      <input
        ref={cameraInputRef}
        type="file"
        accept="image/*"
        capture="environment"
        className="hidden"
        onChange={handleFileChange}
      />
    </div>
  );
}
