import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Configuration
CSV_FILE = "temp_entrega.csv"
STUDENT_NAME = os.getenv("STUDENT_NAME", "Anonymous")

try:
    # Load student data
    df = pd.read_csv(CSV_FILE)
    
    # Extracting data: Col 1=Time, Col 2=Ref, Col 3=Vel
    time = df.iloc[:, 1].values
    reference = df.iloc[:, 2].values / 100 
    velocity = df.iloc[:, 3].values / 100 

    # RMSE Calculation
    rmse = np.sqrt(np.mean((reference - velocity)**2))
    grade = max(0, 10 - (rmse * 50)) 

    # Update global results file
    with open("results.csv", "a") as f:
        f.write(f"{STUDENT_NAME},{rmse:.4f},{grade:.2f}\n")

    # --- GENERATE PLOT ---
    plt.figure(figsize=(10, 5))
    plt.plot(time, reference, 'r--', label='Reference', linewidth=2)
    plt.plot(time, velocity, 'b-', label='Student Velocity', linewidth=2)
    plt.title(f"Latest Submission: {STUDENT_NAME} (RMSE: {rmse:.4f})")
    plt.xlabel("Time (s)")
    plt.ylabel("Normalized Velocity")
    plt.legend()
    plt.grid(True)
    
    # Save as fixed filename for the web display
    plt.savefig("latest_result.png")
    plt.close()

    print(f"Success: Result and plot updated for {STUDENT_NAME}")

except Exception as e:
    print(f"Error: {e}")
