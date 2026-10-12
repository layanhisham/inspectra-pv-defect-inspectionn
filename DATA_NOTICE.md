# Data notice

## What is not in this repository

| Not published | Why |
|---|---|
| EL images, annotations and crops from the industrial partner | Proprietary; shared for academic use under confidentiality |
| Trained weights (`.pt`, `.pth`, `.onnx`, …) | Trained on that data; weights can leak training data |
| The partner's inspection standard, acceptance thresholds and recommendation texts | Internal, manufacturer-specific rules |
| Notebook outputs | They embedded dataset images and file identifiers |
| Web-application source, `.env` files, database dumps, uploaded images | Contain credentials, rules and real inspection data |

## How the notebooks were prepared

- All outputs, execution counts and Colab metadata removed.
- Google Drive and local paths replaced by the generic root `/content/drive/MyDrive/inspectra/…`.
- Arabic comments translated; stale assistant citation markers removed.
- No change to the code logic apart from small fixes noted in the notebook headers (03: run-folder lookup and predict path; 04: duplicate early classifier removed; 01: path variable renamed to `DATA_DIR`).

## Reproducing the work

Use your own YOLO-format EL dataset and adjust the class names in the notebooks. Reported private-data results cannot be reproduced without access to the partner dataset.

## Rules for contributors

1. Never commit data, crops, predictions, weights or outputs. `.gitignore` blocks the common cases.
2. Colab's *Save a copy in GitHub* embeds outputs. Clear them first (*Edit → Clear all outputs*) or use the `nbstripout` pre-commit hook (`pip install pre-commit && pre-commit install`).
3. Run `python scripts/check_repo.py` before pushing. CI runs it too.
4. Anything showing partner data, logos or names needs the partner's written approval first.

## Takedown

If you believe something here should not be public, open an issue or contact the repository owner and it will be removed promptly.
