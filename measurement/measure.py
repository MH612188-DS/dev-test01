import cv2
import numpy as np
import glob
import os
import csv

# --- Configuration ---
REF_WIDTH_MM = 85.6   
REF_HEIGHT_MM = 53.9  

PROC_DIR = "dataset/processed"
RESULTS_FILE = "measurement/results.csv"

os.makedirs("measurement", exist_ok=True)

# Gather unique processed images
image_extensions = ('*.jpg', '*.jpeg', '*.png')
images = set()
for ext in image_extensions:
    for file in glob.glob(os.path.join(PROC_DIR, ext)):
        images.add(file)
images = list(images)

print(f"Starting measurement pipeline on {len(images)} images...")

# Open CSV for logging
with open(RESULTS_FILE, mode='w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["Filename", "Ref_Px_W", "Ref_Px_H", "Scale_X", "Scale_Y", "Target_Width_mm", "Target_Height_mm"])

    success_count = 0

    for fname in images:
        base_name = os.path.basename(fname)
        img = cv2.imread(fname)
        if img is None:
            continue
        
        # 1. Color Masking (Isolate objects from the Red Table)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        
        # Red HSV ranges (wraps around 180)
        mask1 = cv2.inRange(hsv, np.array([0, 120, 70]), np.array([10, 255, 255]))
        mask2 = cv2.inRange(hsv, np.array([170, 120, 70]), np.array([180, 255, 255]))
        red_mask = cv2.bitwise_or(mask1, mask2)
        
        # Invert to get the objects
        object_mask = cv2.bitwise_not(red_mask)
        
        # Morphological cleanup
        kernel = np.ones((5, 5), np.uint8)
        object_mask = cv2.morphologyEx(object_mask, cv2.MORPH_OPEN, kernel)
        object_mask = cv2.morphologyEx(object_mask, cv2.MORPH_CLOSE, kernel)
        
        # 2. Extract Contours
        contours, _ = cv2.findContours(object_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Filter tiny noise contours and sort by area descending
        valid_contours = [c for c in contours if cv2.contourArea(c) > 1000]
        valid_contours = sorted(valid_contours, key=cv2.contourArea, reverse=True)
        
        if len(valid_contours) < 2:
            print(f"[WARNING] {base_name}: Could not isolate both objects. Skipping.")
            continue
            
        # 3. Identify Objects (Assuming the reference card is the larger contour)
        # If your charger is larger, swap index 0 and 1.
        ref_contour = valid_contours[0] 
        target_contour = valid_contours[1]
        
        # 4. Get Minimum Area Bounding Boxes
        ref_rect = cv2.minAreaRect(ref_contour) 
        target_rect = cv2.minAreaRect(target_contour)
        
        ref_box_w = max(ref_rect[1])
        ref_box_h = min(ref_rect[1])
        
        target_box_w = max(target_rect[1])
        target_box_h = min(target_rect[1])
        
        # 5. Calculate Scale and Dimensions
        scale_x = REF_WIDTH_MM / ref_box_w
        scale_y = REF_HEIGHT_MM / ref_box_h
        
        target_width_mm = target_box_w * scale_x
        target_height_mm = target_box_h * scale_y
        
        # Log to CSV
        csv_writer.writerow([
            base_name, 
            round(ref_box_w, 2), round(ref_box_h, 2), 
            round(scale_x, 4), round(scale_y, 4), 
            round(target_width_mm, 2), round(target_height_mm, 2)
        ])
        success_count += 1

print(f"\nPipeline complete! Successfully measured {success_count}/{len(images)} images.")
print(f"Results saved to: {RESULTS_FILE}")