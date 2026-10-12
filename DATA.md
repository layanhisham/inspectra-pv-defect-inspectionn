# Data availability

The private industrial dataset used in this project was provided by **Desert Technologies** for academic use and cannot be redistributed. The following are therefore not part of this repository:

| Not included | Reason |
|---|---|
| EL images, annotations and ROI crops from Desert Technologies | Proprietary; shared for academic use |
| Trained model weights | Trained on the proprietary data |
| The partner's inspection standard, acceptance thresholds and recommendation texts | Internal, manufacturer-specific rules |
| System application source (front end and back end), credentials, database dumps and uploaded inspection images | Contain credentials, rules and real inspection data |

Notebook outputs are cleared so that no dataset images are embedded in them.

## Reproducing the work

Use your own YOLO-format EL dataset (see `configs/data.example.yaml`) and adjust the class names in the notebooks. The reported private-data results cannot be reproduced without access to the partner dataset.

## Contact

For questions about data access, or to request the removal of anything published here, please open an issue.
