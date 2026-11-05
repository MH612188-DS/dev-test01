# Definition of Done

## Phase 1: Setup & Git Compliance
- [x] Plan and Definition of Done committed to `dev-test01` branch before any code was written. (Commit link: )
- [ ] Git history shows progressive steps (calibration -> data -> training -> measurement), with no single monolithic commit.

## Phase 2: Camera Calibration
- [x] 20 or more calibration images captured with locked focus/zoom.
- [x] Reprojection error successfully reported. (Error value & image count: 1.0040 pixels)
- [x] Camera matrix and distortion coefficients saved to a file that the inference script loads. (File path: dev-test01\calibration\camera_params.npz )

## Phase 3: Dataset & Reproducibility
- [ ] 70 or more original images captured, undistorted, and manually labelled.
- [ ] Test split file list (70/20/10) committed before any model training began. (Commit link: )
- [ ] Random seeds, library versions, and training configurations pinned for reproducibility.

## Phase 4: Model & Evaluation
- [ ] Segmentation model trained on custom data (NOT an Ultralytics YOLO or Roboflow model). (Model architecture used: )
- [ ] Model evaluated strictly on the test split. (Mask IoU, mAP@0.5, mAP@0.5:0.95, precision, and recall reported here: )

## Phase 5: Inference Pipeline
- [ ] Single command successfully runs on a new image and prints width and height in mm alongside an overlay.
- [ ] System cleanly handles the "object not found" and "reference not found" cases.
- [ ] System accurately refuses to answer when confidence is low or the reference/plane is compromised. (Refusal threshold value/logic: )

## Phase 6: Validation & Objectives
- [ ] Accuracy table for 10 instances (measured by hand vs. system) is complete, reporting mean absolute error and mean percentage error. (Table location/file: )
- [ ] Undistortion proof complete: 10 instances measured on raw images vs undistorted images, with the numerical difference explained.
- [ ] **MO-1 (Measurement Accuracy):** Target set, measured, and reported. (Target met/missed and reason: )
- [ ] **MO-2 (Custom Objective):** Target set, measured, and reported. (Target met/missed and reason: )
- [ ] One breaking condition (e.g., camera tilt) tested, with error changes measured and reported.

## Phase 7: Final Submission
- [ ] `docs/Objectives.md` completed.
- [ ] `README.md` complete with setup, run instructions, hardware specs, and dataset summary.
- [ ] Model weights linked, with SHA-256 hash provided in README.
- [ ] Everything I did not finish within the 8 hours is explicitly listed here or in the Plan.
- [ ] 5-minute Loom video recorded, covering live measurement, code walkthrough, and the four K1-K4 questions answered verbally. (Loom link: )
- [ ] Pull request opened from `dev-test01` into `main`. (PR link: )
