import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Configuration
CSV_FILE = "temp_entrega.csv"
RESULTS_PATH = "results.csv"
STUDENT_NAME = os.getenv("STUDENT_NAME", "Anonymous")

try:
    # 1. Process New Submission
    df_new = pd.read_csv(CSV_FILE)
    reference = df_new.iloc[:, 2].values / 100 
    velocity = df_new.iloc[:, 3].values / 100 

    # Calculate current RMSE
    rmse_val = np.sqrt(np.mean((reference - velocity)**2))

    # 2. Load Existing Leaderboard
    if os.path.exists(RESULTS_PATH):
        leaderboard = pd.read_csv(RESULTS_PATH)
    else:
        leaderboard = pd.DataFrame(columns=["Student", "RMSE", "Grade"])

    # 3. Update or Add Student (Handle duplicate submissions)
    # If student exists, remove the old record
    leaderboard = leaderboard[leaderboard["Student"] != STUDENT_NAME]
    
    # Add new result (Grade will be recalculated for everyone)
    new_entry = pd.DataFrame([{"Student": STUDENT_NAME, "RMSE": rmse_val, "Grade": 0.0}])
    leaderboard = pd.concat([leaderboard, new_entry], ignore_index=True)

    # 4. Recalculate Grades (Relative Scaling)
    if len(leaderboard) > 1:
        max_rmse = leaderboard["RMSE"].max()
        min_rmse = leaderboard["RMSE"].min()
        
        if max_rmse != min_rmse:
            # Linear mapping: Min RMSE -> 10, Max RMSE -> 7
            # Formula: Grade = 10 - ( (RMSE - Min) / (Max - Min) ) * (10 - 7)
            leaderboard["Grade"] = 10 - ((leaderboard["RMSE"] - min_rmse) / (max_rmse - min_rmse)) * 3
        else:
            # If all have the same error, everyone gets 10
            leaderboard["Grade"] = 10.0
    else:
        # First student always gets 10
        leaderboard["Grade"] = 10.0

    # 5. Save Updated Leaderboard
    leaderboard.to_csv(RESULTS_PATH, index=False)

    # 6. Generate Plot for the latest submission
    time = df_new.iloc[:, 1].values
    plt.figure(figsize=(10, 5))
    plt.plot(time, reference, 'r--', label='Reference', linewidth=2)
    plt.plot(time, velocity, 'b-', label='Measured Velocity', linewidth=2)
    plt.title(f"Latest Submission: {STUDENT_NAME} (RMSE: {rmse_val:.4f})")
    plt.xlabel("Time (s)")
    plt.ylabel("Velocity")
    plt.legend()
    plt.grid(True)
    plt.savefig("latest_result.png")
    plt.close()

    print(f"Leaderboard updated. {STUDENT_NAME} scored RMSE: {rmse_val:.4f}")

except Exception as e:
    print(f"Error: {e}")
