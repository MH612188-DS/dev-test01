import pandas as pd
import os

# --- Configuration ---
RESULTS_FILE = "measurement/results.csv"
REPORT_FILE = "measurement/statistical_summary.txt"

if not os.path.exists(RESULTS_FILE):
    raise FileNotFoundError(f"Could not find {RESULTS_FILE}. Run measure.py first.")

# Load the measurement data
df = pd.read_csv(RESULTS_FILE)

total_images = len(df)
if total_images == 0:
    raise ValueError("The CSV file is empty. No measurements to analyze.")

# Calculate Mean and Standard Deviation
mean_w = df["Target_Width_mm"].mean()
std_w = df["Target_Width_mm"].std()

mean_h = df["Target_Height_mm"].mean()
std_h = df["Target_Height_mm"].std()

# Format the report
report = (
    f"--- Statistical Summary of Charger Measurements ---\n"
    f"Total Valid Images Analyzed: {total_images}\n\n"
    f"Target Width:\n"
    f"  Mean: {mean_w:.2f} mm\n"
    f"  Standard Deviation: ±{std_w:.2f} mm\n\n"
    f"Target Height:\n"
    f"  Mean: {mean_h:.2f} mm\n"
    f"  Standard Deviation: ±{std_h:.2f} mm\n"
)

# Print to console and save to file
print(report)

with open(REPORT_FILE, "w") as f:
    f.write(report)

print(f"\nReport saved to: {REPORT_FILE}")