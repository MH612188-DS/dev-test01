import cv2
import numpy as np
import glob
import os

# Configuration matching your physical setup
SQUARE_SIZE_MM = 21.0  # 2.1 cm square size
CHECKERBOARD = (10, 7)   # 11x8 squares = 10x7 inner corners
CALIB_DIR = os.path.dirname(os.path.abspath(__file__))

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Prepare 3D object points in physical world units (mm)
objp = np.zeros((CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)
objp *= SQUARE_SIZE_MM

objpoints = [] # 3D points in real-world space
imgpoints = [] # 2D points in image plane

# Gather all images in calibration folder without duplicates
image_extensions = ('*.jpg', '*.jpeg', '*.png')
images = set() # Use a set to automatically drop duplicates
for ext in image_extensions:
    for file in glob.glob(os.path.join(CALIB_DIR, ext)):
        # Convert to lower case just for checking, but keep original file path
        images.add(file)
images = list(images)

print(f"Found {len(images)} unique images in {CALIB_DIR}")

successful_count = 0
img_shape = None

for fname in sorted(images):
    img = cv2.imread(fname)
    if img is None:
        continue
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_shape = gray.shape[::-1]

    # Find checkerboard corners
    ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, None)

    if ret:
        objpoints.append(objp)
        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners2)
        successful_count += 1
        print(f"[OK] {os.path.basename(fname)}")
    else:
        print(f"[FAILED] Could not detect corners in {os.path.basename(fname)}")

print(f"\nDetected grid corners in {successful_count} out of {len(images)} images.")

if successful_count >= 10:
    # Calibrate camera
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(
        objpoints, imgpoints, img_shape, None, None
    )

    # Compute mean reprojection error
    total_error = 0
    for i in range(len(objpoints)):
        imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
        error = cv2.norm(imgpoints[i], imgpoints2, cv2.NORM_L2) / len(imgpoints2)
        total_error += error

    reprojection_error = total_error / len(objpoints)
    print(f"\n==========================================")
    print(f"REPROJECTION ERROR: {reprojection_error:.4f} pixels")
    print(f"==========================================")

    # Save output parameters
    out_file = os.path.join(CALIB_DIR, 'camera_params.npz')
    np.savez(out_file, mtx=mtx, dist=dist)
    print(f"Saved parameters to: {out_file}")
else:
    print("\nCalibration failed: Too few valid images detected. Check lighting or blur.")