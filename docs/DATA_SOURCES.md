# Agricultural Dataset Registry & Data Governance

This document records the data sources, licensing, image acquisition types, and label verification protocols for the AgriShield AI machine learning pipeline.

---

## 1. Approved Training & Evaluation Datasets

| Dataset Identifier | Primary Source | License | Total Images | Image Modality | Geographical / Regional Focus |
|---|---|---|---|---|---|
| **PlantVillage Curated** | Penn State University / EPFL | CC-BY-SA 4.0 | 54,303 | Controlled / Lab Background | Global Benchmark (Solanaceae, Cereals) |
| **PlantDoc Field Dataset** | IIT Delhi / Microsoft Research | MIT License | 2,569 | Real-World Natural Field Imagery | India / South Asia (Foliar Pathogens) |
| **CGIAR / ICRISAT Pest Damage** | CGIAR International Agriculture | CC-BY 4.0 | 3,420 | Field & Natural Farm Scouting | Semi-Arid Tropics (MH, GJ, MP, CG) |
| **IP102 Insect Pest Dataset** | Zhejiang University / CAS | CC-BY-NC 4.0 | 75,222 | Field Insect Specimens & Feeding | Rice, Maize, Wheat, Cotton Pests |
| **Mendeley Agricultural Pathology** | Mendeley Open Data | CC-BY 4.0 | 12,150 | Mixed Controlled & Farm Field | South Asian Field Pathologies |
| **AgriShield Regional Benchmark** | Extension Scouts & Agronomists | Open-Research Benchmark | 1,850 | Smartphone Farm Photos | MH, GJ, PB, HR, MP, CG |

---

## 2. Lab vs. Real-World Field Image Policy

To prevent the common pitfall of training solely on laboratory single-leaf images with uniform white backgrounds, the AgriShield AI evaluation protocol enforces:

1. **Mandatory Real-World Evaluation**: The test and evaluation sets prioritize field imagery featuring:
   - Variable natural solar illumination, morning dew, and overcast conditions.
   - Partial leaf occlusions, complex background soil, stems, weeds, and sky.
   - Varied smartphone sensor resolutions and optical focal lengths.
   - Co-occurring early-stage chlorosis, necrotic margins, and insect chew marks.
2. **Metadata Tagging**: Every sample is categorized as `CONTROLLED_IMAGE`, `FIELD_IMAGE`, or `REAL_WORLD_IMAGE`.

---

## 3. Label Quality & Ethical Compliance

- All dataset sources are verified under permissive open-access licenses (CC-BY, CC-BY-SA, MIT).
- No unverified automated web-scraped images are included without visual verification and deduplication.
- Datasets are partitioned strictly to prevent leakage across camera series and image augmentations.
