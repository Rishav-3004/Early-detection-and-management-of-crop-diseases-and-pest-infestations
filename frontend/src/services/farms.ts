import { apiClient } from '@/lib/api';
import { Farm, Field } from '@/types';

export const farmService = {
  async listFarms(): Promise<Farm[]> {
    return apiClient<Farm[]>('/farms');
  },

  async createFarm(data: {
    name: string;
    location: string;
    area: number;
    latitude?: number;
    longitude?: number;
    soil_type?: string;
    irrigation_type?: string;
  }): Promise<Farm> {
    return apiClient<Farm>('/farms', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  async getFarm(farmId: string): Promise<Farm> {
    return apiClient<Farm>(`/farms/${farmId}`);
  },

  async updateFarm(farmId: string, data: Partial<Farm>): Promise<Farm> {
    return apiClient<Farm>(`/farms/${farmId}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  },

  async deleteFarm(farmId: string): Promise<void> {
    return apiClient(`/farms/${farmId}`, { method: 'DELETE' });
  },

  async createField(data: {
    farm_id: string;
    name: string;
    area: number;
    crop_id?: string;
    variety?: string;
    growth_stage?: string;
  }): Promise<Field> {
    return apiClient<Field>('/fields', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  async updateField(fieldId: string, data: Partial<Field>): Promise<Field> {
    return apiClient<Field>(`/fields/${fieldId}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  },

  async deleteField(fieldId: string): Promise<void> {
    return apiClient(`/fields/${fieldId}`, { method: 'DELETE' });
  },
};
