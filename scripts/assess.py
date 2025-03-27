import os
import pandas as pd

csv_file = os.getenv("CSV_FILE")
student_name = os.getenv("STUDENT_NAME")

df = pd.read_csv(csv_file)
df["Ref"] /= 100
df["Vel"] /= 100

mse = ((df["Ref"] - df["Vel"])**2).mean()
grade = 10 - 20 * min(mse, 0.1)

with open("results.csv", "a") as f:
    f.write(f"{student_name},{mse:.4f},{grade:.2f}\n")

print(f"Student: {student_name}")
print(f"MSE: {mse:.4f}")
print(f"Grade: {grade:.2f}")
