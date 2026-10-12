<div align="center">

<img src="docs/assets/logo.png" alt="InSpectra" width="420">

**Seeing beyond the obvious.**

A hybrid deep-learning pipeline that detects and classifies defects in photovoltaic (PV) panels from electroluminescence (EL) images.

![Python](https://img.shields.io/badge/Python-3.10--3.12-3776AB?logo=python&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-2.x-EE4C2C?logo=pytorch&logoColor=white)
![Ultralytics](https://img.shields.io/badge/Ultralytics-111F68)
![YOLO11s](https://img.shields.io/badge/Detector-YOLO11s-00A3E0)
![RT-DETR-X](https://img.shields.io/badge/Detector-RT--DETR--X-7B2FF7)
![ResNet50](https://img.shields.io/badge/Classifier-ResNet50-EE4C2C)
![EfficientNet-B0](https://img.shields.io/badge/Classifier-EfficientNet--B0-2E7D32)
![React](https://img.shields.io/badge/React-Vite-61DAFB?logo=react&logoColor=black)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

[**Demo videos**](https://drive.google.com/drive/folders/1bsAReEUwmxozrBx8bYj9a-N0-e6rPsRl)

</div>

<!-- Enable after written approval from the data owner and the university (see DATA_NOTICE.md):
<p align="center"><img src="docs/assets/poster.png" width="420" alt="Graduation showcase poster"></p>
-->

## Overview

EL imaging reveals cracks and dead areas inside solar cells that are invisible to the eye, but in production lines the images are still inspected manually: slow, subjective and hard to scale. **InSpectra** automates this step.

It is a two-stage pipeline, evaluated on a **public** EL dataset and on a **private industrial** dataset from a Saudi PV manufacturer:

1. **Localisation** – an object detector (RT-DETR-X or YOLO11s) finds defects on the full panel image.
2. **Classification** – each detected region is cropped and classified (ResNet50 or EfficientNet-B0) into one of four defect types.

The selected models (**RT-DETR-X + EfficientNet-B0**) are integrated into a web application used by inspectors and administrators.

> Graduation project, B.Sc. Computer Science, Imam Abdulrahman Bin Faisal University (IAU), 2025–2026, supervised by **Dr. Dhiaa A. Musleh**, in collaboration with **Desert Technologies**. The project belongs to the supervisor and the university.

## Pipeline

### Methodology

```mermaid
flowchart LR
    A[(Data<br/>Desert Technologies)] --> B[Manual annotation<br/>Roboflow]
    B --> C[Preprocessing<br/>denoising · CLAHE · sharpening<br/>normalisation · augmentation]
    C --> D[Split<br/>70 / 15 / 15]
    D --> E[Detection<br/>YOLO11s vs RT-DETR-X]
    E --> F[ROI extraction<br/>& preprocessing<br/>224 × 224]
    F --> G[Classification<br/>ResNet50 vs EfficientNet-B0]
    G --> H[Software architecture<br/>React · FastAPI · PostgreSQL]
```

Selected models: **RT-DETR-X + EfficientNet-B0**. The same flow was run on the public dataset (Roboflow EL-Images) and the private one.

### Inference flow in the web application

```mermaid
flowchart LR
    A[Uploaded EL image] --> B[RT-DETR-X]
    B --> C{Any boxes?}
    C -->|No| H[Healthy]
    C -->|Yes| D[Crop each region]
    D --> E[EfficientNet-B0]
    E --> F[Assessment engine<br/>severity · recommendation]
    F --> G[(PostgreSQL)]
    F --> R[Results · history · PDF report]
    H --> G
```

**Defect classes:** Black spot · Cell scratch · Cells class difference · Micro-crack

## Results

Metrics are measured on the **validation split** of each dataset. Final selections are marked ✅.

### Defect localisation

| Dataset | Model | mAP@50 | Precision | Recall | |
|---|---|---:|---:|---:|:-:|
| Public | YOLO11s | 41.68 % | 54.25 % | 45.19 % | |
| Public | RT-DETR-X | 49.61 % | 77.00 % | 48.94 % | ✅ |
| Private | YOLO11s | 48.14 % | 52.83 % | 48.30 % | |
| Private | RT-DETR-X | 49.05 % | 48.24 % | 52.73 % | ✅ |

Per-class mAP@50 of RT-DETR-X on the private validation set: Micro-crack **83.2 %** · Cells class difference 44.1 % · Black spot 38.6 % · Cell scratch 30.3 %.

### Defect classification

| Dataset | Model | Accuracy | Precision | Recall | F1 | |
|---|---|---:|---:|---:|---:|:-:|
| Public | ResNet50 | 83.05 % | 83.74 % | 83.05 % | 82.50 % | ✅ |
| Public | EfficientNet-B0 | 79.66 % | 80.40 % | 79.66 % | 79.70 % | |
| Private | ResNet50 | 87.14 % | 87.34 % | 87.14 % | 87.16 % | |
| Private | EfficientNet-B0 | 87.46 % | 87.45 % | 87.46 % | 87.45 % | ✅ |

### How to read these numbers

- The validation sets are small (private: 29 images / 311 annotated defects). Single runs, no confidence intervals.
- On the private data, EfficientNet-B0 vs ResNet50 differs by **one validation crop** (272 vs 271 of 311), so the two are statistically indistinguishable; EfficientNet-B0 was kept for its efficiency.
- Detection mAP@50 of about 49 % is a baseline: micro-cracks are found reliably, scratches and black spots much less so. Better and larger data is the main lever.
- Images come from controlled indoor EL setups; outdoor / drone imagery is future work.

## Web application

React + Vite + Tailwind front end, FastAPI back end, PostgreSQL storage, PDF reports. Role-based access (admin / inspector), JWT in an HTTP-only cookie, bcrypt-hashed passwords.

| Inspector home | Admin home | PDF report |
|:-:|:-:|:-:|
| <img src="docs/assets/ui-inspector-home.png" width="300"> | <img src="docs/assets/ui-admin-home.png" width="300"> | <img src="docs/assets/ui-pdf-report.png" width="300"> |

| Home | New inspection | Processing |
|:-:|:-:|:-:|
| <img src="docs/assets/ui-home.png" width="300"> | <img src="docs/assets/ui-new-inspection.png" width="300"> | <img src="docs/assets/ui-processing.png" width="300"> |

**Architecture:** React client → FastAPI back end (JWT auth) → PostgreSQL (Supabase) for metadata and a storage folder for inspection images.

<p align="center"><img src="docs/assets/arch-system.png" width="420" alt="System architecture"></p>

Full walkthrough: [**demo videos (Drive)**](https://drive.google.com/drive/folders/1bsAReEUwmxozrBx8bYj9a-N0-e6rPsRl).

- **Inspector:** upload EL images → annotated result with defect types, locations, severity and recommendation → history, dashboard, PDF report.
- **Admin:** user management and system logs.
- A rule-based assessment engine turns detections into a panel-level verdict. The rules are manufacturer-specific and **are not part of this repository**.

This repository contains the machine-learning pipeline. The web-application source is not included.

## Repository structure

```
.
├── notebooks/
│   ├── 01_data_preprocessing.ipynb                       # EL preprocessing pipeline
│   ├── 02_detection_yolo11s.ipynb                        # YOLO11s training & evaluation
│   ├── 03_detection_rtdetr.ipynb                         # RT-DETR-X training & evaluation
│   ├── 04_roi_extraction.ipynb                           # detection labels -> classification crops
│   └── 05_classification_resnet50_efficientnetb0.ipynb   # classifier training & evaluation
├── configs/data.example.yaml                             # dataset config template
├── docs/methodology.md                                   # preprocessing & training settings
├── scripts/check_repo.py                                 # guards against leaking data/outputs
├── DATA_NOTICE.md                                        # what is (not) published, and why
└── requirements.txt
```

## Getting started

The notebooks are written for **Google Colab** (GPU). The datasets are **not** included, so bring a YOLO-format EL dataset with this layout:

```
inspectra/
├── detection_dataset_raw/          # train|valid|test / images|labels  + data.yaml
├── detection_dataset_processed/    # same, after preprocessing
├── classification_dataset/         # train|valid|test / <class> / *.jpg   (notebook 04)
└── runs/                           # training outputs
```

1. Copy `configs/data.example.yaml` to your dataset root as `data.yaml`.
2. Run the notebooks in order `01 → 05` and adjust the paths in each *Configuration* cell.
3. For the public alternative use [EL-Images (Roboflow Universe)](https://universe.roboflow.com/venkata-prasanth/el-images-p2ove) – 3 classes, so update `CLASS_NAMES` and the oversampled class id.

Local setup: `pip install -r requirements.txt`.

## Data and confidentiality

The private dataset (provided by Desert Technologies), annotations, trained weights and the manufacturer's inspection rules are proprietary and are **not** published. Notebook outputs were removed because they contained images from that dataset. Details and contributor rules: [`DATA_NOTICE.md`](DATA_NOTICE.md). Before committing, run `python scripts/check_repo.py` (also runs in CI).

## Future work

Drone-based inspection with InGaAs cameras, fine-tuning on new EL data, and larger, more diverse datasets for better scalability.

## Team

Rahaf J. Alghamdi · Ghada F. Alhafs · Raghad S. Jathmi · Alanood A. Alshabibi · **Layan H. Almohawish**
Supervisor: **Dr. Dhiaa A. Musleh** — College of Computer Science and Information Technology, Imam Abdulrahman Bin Faisal University (IAU).

<!-- Add your own role, e.g.: "My contribution: ..." -->

## Acknowledgements

- **Desert Technologies** for the collaboration and for providing the industrial EL dataset for academic use.
- **Dr. Dhiaa A. Musleh** and **Imam Abdulrahman Bin Faisal University** for supervision and support.
- Public dataset: *EL-Images* by Venkata Prasanth, Roboflow Universe, CC BY 4.0.
- [Ultralytics](https://github.com/ultralytics/ultralytics) (AGPL-3.0) for YOLO11 and RT-DETR; [PyTorch](https://pytorch.org/) / torchvision for the classifiers.

## License

The project was developed at, and belongs to, the supervisor Dr. Dhiaa A. Musleh and Imam Abdulrahman Bin Faisal University (IAU). Code and documentation: [MIT](LICENSE). Datasets and trained models are not covered. Note that Ultralytics is AGPL-3.0, which matters if you deploy a service built on it.
