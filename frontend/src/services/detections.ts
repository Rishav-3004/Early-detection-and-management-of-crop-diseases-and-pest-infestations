import { apiClient } from '@/lib/api';
import { Detection } from '@/types';

export interface DetectionListResponse {
  items: Detection[];
  meta: {
    total: number;
    page: number;
    page_size: number;
    total_pages: number;
  };
}

export const detectionService = {
  async scanCrop(
    file: File,
    options?: { farm_id?: string; field_id?: string; crop_id?: string }
  ): Promise<Detection> {
    const formData = new FormData();
    formData.append('file', file);
    if (options?.farm_id) formData.append('farm_id', options.farm_id);
    if (options?.field_id) formData.append('field_id', options.field_id);
    if (options?.crop_id) formData.append('crop_id', options.crop_id);

    return apiClient<Detection>('/detections/scan', {
      method: 'POST',
      body: formData,
    });
  },

  async listDetections(params: {
    page?: number;
    page_size?: number;
    crop_id?: string;
    farm_id?: string;
    field_id?: string;
    detection_type?: string;
    severity?: string;
    risk_level?: string;
    expert_verified?: boolean;
    search?: string;
    sort_by?: string;
  } = {}): Promise<DetectionListResponse> {
    const query = new URLSearchParams();
    if (params.page) query.append('page', params.page.toString());
    if (params.page_size) query.append('page_size', params.page_size.toString());
    if (params.crop_id) query.append('crop_id', params.crop_id);
    if (params.farm_id) query.append('farm_id', params.farm_id);
    if (params.field_id) query.append('field_id', params.field_id);
    if (params.detection_type) query.append('detection_type', params.detection_type);
    if (params.severity) query.append('severity', params.severity);
    if (params.risk_level) query.append('risk_level', params.risk_level);
    if (params.expert_verified !== undefined) query.append('expert_verified', params.expert_verified.toString());
    if (params.search) query.append('search', params.search);
    if (params.sort_by) query.append('sort_by', params.sort_by);

    return apiClient<DetectionListResponse>(`/detections?${query.toString()}`);
  },

  async getDetectionDetail(detectionId: string): Promise<Detection> {
    return apiClient<Detection>(`/detections/${detectionId}`);
  },
};
