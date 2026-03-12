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
    # El archivo del robot no lleva cabecera y tiene 5 columnas:
    # 0: xref, 1: yref, 2: x, 3: y, 4: errorcua
    df_new = pd.read_csv(CSV_FILE, header=None)

    if df_new.shape[1] < 5:
        raise ValueError(
            f"El archivo debe tener al menos 5 columnas y tiene {df_new.shape[1]}"
        )

    xref = pd.to_numeric(df_new.iloc[:, 0], errors="raise").values
    yref = pd.to_numeric(df_new.iloc[:, 1], errors="raise").values
    x = pd.to_numeric(df_new.iloc[:, 2], errors="raise").values
    y = pd.to_numeric(df_new.iloc[:, 3], errors="raise").values
    errorcua_logged = pd.to_numeric(df_new.iloc[:, 4], errors="raise").values

    # Recalcular el error cuadrático por robustez
    errorcua_calc = (xref - x) ** 2 + (yref - y) ** 2

    # Métrica principal
    rmse_val = np.sqrt(np.mean(errorcua_calc))

    # Comprobación opcional frente a la columna registrada por el robot
    mse_logged = np.mean(errorcua_logged)
    mse_calc = np.mean(errorcua_calc)
    mse_diff = abs(mse_logged - mse_calc)

    # 2. Load Existing Leaderboard
    if os.path.exists(RESULTS_PATH):
        leaderboard = pd.read_csv(RESULTS_PATH)
    else:
        leaderboard = pd.DataFrame(columns=["Student", "RMSE", "Grade"])

    # 3. Update or Add Student
    leaderboard = leaderboard[leaderboard["Student"] != STUDENT_NAME]

    new_entry = pd.DataFrame([{
        "Student": STUDENT_NAME,
        "RMSE": rmse_val,
        "Grade": 0.0
    }])
    leaderboard = pd.concat([leaderboard, new_entry], ignore_index=True)

    # 4. Recalculate Grades (Relative Scaling)
    if len(leaderboard) > 1:
        max_rmse = leaderboard["RMSE"].max()
        min_rmse = leaderboard["RMSE"].min()

        if max_rmse != min_rmse:
            # Min RMSE -> 10, Max RMSE -> 7
            leaderboard["Grade"] = 10 - (
                (leaderboard["RMSE"] - min_rmse) / (max_rmse - min_rmse)
            ) * 3
        else:
            leaderboard["Grade"] = 10.0
    else:
        leaderboard["Grade"] = 10.0

    # 5. Save Updated Leaderboard
    leaderboard.to_csv(RESULTS_PATH, index=False)

    # 6. Generate Plot for the latest submission
    sample_idx = np.arange(len(xref))

    plt.figure(figsize=(10, 5))
    plt.plot(xref, yref, "r--", label="Reference trajectory", linewidth=2)
    plt.plot(x, y, "b-", label="Measured trajectory", linewidth=2)
    plt.title(f"Latest Submission: {STUDENT_NAME} (RMSE: {rmse_val:.4f})")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.grid(True)
    plt.axis("equal")
    plt.tight_layout()
    plt.savefig("latest_result.png")
    plt.close()

    print(f"Leaderboard updated. {STUDENT_NAME} scored RMSE: {rmse_val:.4f}")
    print(f"MSE calculated: {mse_calc:.6f}")
    print(f"MSE logged: {mse_logged:.6f}")
    print(f"MSE difference: {mse_diff:.6f}")

except Exception as e:
    print(f"Error: {e}")
    raise
