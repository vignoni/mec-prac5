import os
import pandas as pd
import numpy as np

# Configuration for real-time evaluation
CSV_FILE = "temp_entrega.csv"
STUDENT_NAME = os.getenv("STUDENT_NAME", "Anonymous")

try:
    # Read the student CSV file
    # Expected format: Col 1: Timestamp, Col 2: Reference, Col 3: Velocity
    df = pd.read_csv(CSV_FILE)
    
    # Extract data using column indices for robustness
    # Reference and Velocity are normalized (divided by 100)
    reference = df.iloc[:, 2].values / 100 
    velocity = df.iloc[:, 3].values / 100 

    # --- RMSE CALCULATION ---
    # Formula: sqrt(mean((reference - velocity)^2))
    mse = np.mean((reference - velocity)**2)
    rmse = np.sqrt(mse)

    # --- GRADING LOGIC ---
    # Higher precision (lower RMSE) results in a better grade.
    # Base grade is 10.0, minus a penalty proportional to the error.
    grade = max(0, 10 - (rmse * 50)) 

    # Update the central leaderboard file
    # Format: Student Name, RMSE, Grade
    with open("results.csv", "a") as f:
        f.write(f"{STUDENT_NAME},{rmse:.4f},{grade:.2f}\n")

    print(f"Evaluation finished for {STUDENT_NAME}. RMSE: {rmse:.4f}")

except Exception as e:
    print(f"CRITICAL ERROR during assessment: {e}")
