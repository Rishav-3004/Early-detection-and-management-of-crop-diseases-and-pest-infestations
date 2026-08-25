import { apiClient } from '@/lib/api';
import { Crop, Disease, Pest } from '@/types';

export const knowledgeService = {
  async listCrops(): Promise<Crop[]> {
    return apiClient<Crop[]>('/crops');
  },

  async getCrop(cropId: string): Promise<Crop> {
    return apiClient<Crop>(`/crops/${cropId}`);
  },

  async listDiseases(cropId?: string): Promise<Disease[]> {
    const query = cropId ? `?crop_id=${cropId}` : '';
    return apiClient<Disease[]>(`/diseases${query}`);
  },

  async getDisease(diseaseId: string): Promise<Disease> {
    return apiClient<Disease>(`/diseases/${diseaseId}`);
  },

  async listPests(cropId?: string): Promise<Pest[]> {
    const query = cropId ? `?crop_id=${cropId}` : '';
    return apiClient<Pest[]>(`/pests${query}`);
  },

  async getPest(pestId: string): Promise<Pest> {
    return apiClient<Pest>(`/pests/${pestId}`);
  },
};
