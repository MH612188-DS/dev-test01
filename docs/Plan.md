# Project Plan: Measure It Segmentation and Metric Measurement

## Context & Setup
* **Environment:** The object and reference will be placed flat on a small red table to ensure they lie in the exact same plane.
* **Hardware Strategy:** Local machine is a 4-core 7th Gen Intel Core i7 CPU with no local GPU. To accommodate this, model training will be offloaded to a cloud notebook (e.g., Google Colab/Kaggle), and weights will be exported for local CPU inference. 
* **Target Object:**  A mobile phone charging adapter - chosen for distinct edges against the red table and ease of manual measurement.
* **Reference Object:**  A plan white card - measured manually with a caliper.

## Order of Operations and Time Allocation (8 Hours Total)

**1. Setup and Initial Documentation (0.5 hours)**
* Create the repository and checkout branch `dev-test01`.
* Write and commit this `Plan.md` and the `Definition_of_Done.md` before any code is written.

**2. Camera Calibration (1.0 hours)**
* Lock phone camera focus, zoom, and resolution.
* Tape a printed checkerboard (at least 7x9 inner corners) completely flat and measure one square manually with a caliper.
* Capture 20+ calibration images.
* Write an OpenCV script to compute the camera matrix, distortion coefficients, and reprojection error, saving the parameters to a file.

**3. Data Collection and Splitting (1.5 hours)**
* Photograph the target object and reference object together on the red table, capturing 70+ images.
* Intentionally vary camera tilt during capture to create a degrading condition to test later.
* Run all images through the OpenCV calibration parameters to undistort them.
* Label segmentation masks (using CVAT or Label Studio).
* Define a 70/20/10 train/val/test split, create a file list of the test split, and commit this list before training begins.

**4. Model Training Setup (1.0 hours of active work)**
* Write training code for a lightweight segmentation model (e.g., MobileNetV3-UNet) that can run efficiently on a CPU. Ultralytics YOLO and Roboflow models will not be used.
* Evaluate the trained model strictly on the test split, recording mask IoU, mAP@0.5, mAP@0.5:0.95, precision, and recall.

**5. Inference and Measurement Pipeline (1.5 hours)**
* Write the main command-line script that ingests a single new image, undistorts it, runs segmentation, and locates the reference object.
* Implement the pixel-to-millimeter mathematical conversion using the reference object's known dimensions.
* Add error handling to cleanly report when the object or reference is not found.
* Set safety thresholds so the system refuses to output a measurement if mask confidence is low or the tilt is too severe.

**6. Accuracy Validation and Objectives (2.0 hours)**
* Measure 10 instances by hand using a caliper.
* Run the inference command on those same 10 instances and generate a table showing mean absolute error and mean percentage error.
* Run the command on the raw (distorted) images of those 10 instances to prove the mathematical necessity of undistortion.
* Measure how the error rate increases as the camera tilt (the chosen degrading condition) worsens.

**7. Final Polish and Submission (0.5 hours)**
* Finalize the `Objectives.md` and `README.md` (including hardware specs and dataset summary).
* Complete the Decision Record in this document.
* Record the 5-minute Loom video demonstrating the live measurement, tracing the code, and answering the four required questions.

## What is Being Skipped
* **Heavy Segmentation Architectures (e.g., SAM or large Vision Transformers):** Skipped to ensure the final inference command runs with low latency on a local CPU during the final Loom recording.
* **Automatic Focal Length Estimation:** Skipped in favor of strict, physical OpenCV checkerboard calibration to guarantee mathematical traceability.

## Decision Record
*(To be completed at the end of the project)*
* **The approach I took:** 
* **The approach I rejected:** 
* **What rejecting it cost:**
