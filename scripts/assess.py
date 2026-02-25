import os
import pandas as pd
import numpy as np

# File path for the downloaded student data
csv_file = "temp_entrega.csv"
student_name = os.getenv("STUDENT_NAME", "Unknown_Student")

try:
    # Load the CSV. Based on provided samples: 
    # Col 1: Timestamp, Col 2: Reference, Col 3: Velocity
    df = pd.read_csv(csv_file)
    
    # Extracting data by index to be robust against header name changes
    time = df.iloc[:, 1].values
    # Normalizing values as per existing implementation
    reference = df.iloc[:, 2].values / 100 
    velocity = df.iloc[:, 3].values / 100 

    # --- ITAE CALCULATION ---
    # Formula: Integral of (time * |error|) dt
    error = np.abs(reference - velocity)
    dt = np.diff(time, prepend=time[0])
    itae = np.sum(time * error * dt)

    # --- GRADING LOGIC ---
    # Lower ITAE is better. 10 is max grade, penalized by error magnitude.
    grade = max(0, 10 - (itae * 2)) 

    # Append to the global leaderboard file
    with open("results.csv", "a") as f:
        # Format: Name, ITAE, Grade
        f.write(f"{student_name},{itae:.4f},{grade:.2f}\n")

    print(f"Success: {student_name} evaluated. ITAE: {itae:.4f}")

except Exception as e:
    print(f"Error processing submission for {student_name}: {e}")
