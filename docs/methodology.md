# Methodology

Settings as used in the notebooks and the project report. Metrics: see the README.

## Datasets

| | Public | Private (not published) |
|---|---|---|
| Source | EL-Images, Roboflow Universe, CC BY 4.0 | Desert Technologies (Saudi PV manufacturer), manually annotated by the team in Roboflow |
| Size | ≈ 420 EL images | 462 raw images (Pass/Fail); 362 annotated images reported on the project poster |
| Classes | Branch crack, isolation area, micro-crack | Black spot, cell scratch, cells class difference, micro-crack |

Nine fine-grained defect types were first annotated on the private data; the four classes with enough instances were kept to avoid skewed training. Annotation follows the partner's internal EL standard, which is not reproduced here.

## Preprocessing

| Step | Setting |
|---|---|
| Panel crop (border removal) | Gaussian blur (7,7) → Otsu threshold → closing (15,15) → erosion (5,5), 1 iter → largest contour, 5 px padding |
| Contrast | CLAHE, clipLimit 2.0, tiles (8,8) |
| Class balancing (detection) | Micro-crack images repeated ×4 (YOLO11s) / ×2 (RT-DETR-X), train split only |
| ROI crops (classification) | Notebook 04: tight bounding-box crops per annotation; `smart_solar_preprocess` previews ×1.5 context margin, bicubic 224×224, CLAHE 1.2 |
| Classifier input | 224×224, grayscale → 3 channels, ImageNet normalisation |
| Classifier augmentation | Horizontal flip, rotation ±10°, ColorJitter (brightness/contrast 0.1) |

## Training

| | YOLO11s | RT-DETR-X |
|---|---|---|
| Image size | 1280 | 1280 |
| Epochs | 100 (patience 30) | 120 |
| Batch | 6 | 4, then 8 in the recovery run |
| Optimiser | auto | AdamW; recovery run lr0 = 1e-4 |
| AMP | on | off (NaN divergence with AMP) |
| GPU | Tesla T4 | A100 80 GB |

| | ResNet50 | EfficientNet-B0 |
|---|---|---|
| Epochs / batch | 15 / 32 | 15 / 32 |
| Optimiser | Adam, lr 5e-4, StepLR(7, 0.1) | same |
| Head | Linear(2048→4) | Dropout(0.4) + Linear(→4) |
| Class balance | WeightedRandomSampler | WeightedRandomSampler |
| Loss | Cross-entropy | Cross-entropy |

Frameworks: Ultralytics 8.4.47–8.4.48, PyTorch 2.10, CUDA 12.8, torchvision, scikit-learn, OpenCV.

## Evaluation

- Detection: mAP@50, precision, recall (Ultralytics validation).
- Classification: accuracy and weighted precision / recall / F1 (scikit-learn), last-epoch validation metrics.
