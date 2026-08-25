'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function FieldsPage() {
  const router = useRouter();
  useEffect(() => {
    router.replace('/farms');
  }, [router]);

  return null;
}
