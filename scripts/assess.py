import os
import pandas as pd
import matplotlib.pyplot as plt

csv_file = os.getenv("CSV_FILE")
student_name = os.getenv("STUDENT_NAME")

df = pd.read_csv(csv_file)
df["Ref"] /= 100
df["Vel"] /= 100

mse = ((df["Ref"] - df["Vel"])**2).mean()
grade = 10 - 20 * min(mse, 0.1)

with open("results.csv", "a") as f:
    f.write(f"{student_name},{mse:.4f},{grade:.2f}\n")

plt.figure(figsize=(6, 4))
plt.plot(df["Timestamp"], df["Ref"], label="Reference", linewidth=2)
plt.plot(df["Timestamp"], df["Vel"], label="Velocity", linewidth=2)
plt.title(f"{student_name} | MSE: {mse:.4f} | Grade: {grade:.2f}")
plt.xlabel("Time (s)")
plt.ylabel("Reference, Velocity")
plt.legend()
plt.tight_layout()
plt.savefig("latest_result.png")
plt.close()
