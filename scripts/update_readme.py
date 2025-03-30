import pandas as pd

results = pd.read_csv("results.csv", names=["Student", "Index", "Grade"])

with open("README.md", "r") as f:
    lines = f.readlines()

start = lines.index("<!-- RESULTS_TABLE_START -->\n")
end = lines.index("<!-- RESULTS_TABLE_END -->\n")

table = "| Student | Performance Index | Grade |\n|---------|-------------------|-------|\n"
for _, row in results.iterrows():
    table += f"| {row['Student']} | {row['Index']:.4f} | {row['Grade']:.2f} |\n"

table += "\n### 📈 Latest Submission Plot\n"
table += "![Latest Result](latest_result.png)\n"

new_readme = lines[:start+1] + [table] + lines[end:]
with open("README.md", "w") as f:
    f.writelines(new_readme)
