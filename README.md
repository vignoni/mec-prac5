# 🏆 Mobile Robot Control Competition: Trajectory tracking

Welcome to the **Real-Time Trajectory tracking Leaderboard**. This repository evaluates your trajectory performance using **RMSE (Root Mean Square Error)** in Practice 6, Mechatronics (11642) - Universitat Politècnica de València.

The goal is to achieve the best trayectory tracking with your mobile robot..

---

## 📊 Live Leaderboard & Plot
You can monitor the competition results and the latest submission plot here:
👉 **[[Competition Results]](https://vignoni.github.io/mec-prac5/)**

---

## 🚀 How to Participate

1. **Tune your controller:** Adjust your PID (or other control strategy) parameters on the mobile robot.
2. **Export your data:** Save your test results into a `.csv` file. 
   - **Important:** Your file must follow the standard export format (see below).
3. **Submit the Form:** Upload your file and enter your name in the official submission form: [[GOOGLE FORM]](https://forms.gle/TT6iaXa9LxJQQUvA9)

---

## 📋 CSV Data Format Requirements

To ensure the automated judge can read your results, your CSV file **must** have the following structure (Standard Robot Export):

| Column | Data Description | Units |
| :--- | :--- | :--- |
| **A** | Reference trajectory X | cm |
| **B** | Reference trajectory Y | cm |
| **C** | Real trajectory X | cm |
| **D** | Real trajectory Y | cm |

> [!CAUTION]
> **Do not change the order of the columns.** The evaluation script relies on these exact positions to calculate your score. 


---

## 📉 Evaluation Metric: RMSE

We use the **Root Mean Square Error** to rank your performance. 
- A **lower RMSE** means better tracking and higher precision.
- The **Grade** is automatically calculated based on your RMSE (Max: 10.00).

---

## 🛠️ Built With
- **Python**: Data processing and plotting (Pandas, Numpy, Matplotlib).
- **GitHub Actions**: Automated CI/CD pipeline for real-time assessment.
- **Google Forms & Apps Script**: Student submission bridge.
- **Tailwind CSS**: Live dashboard visualization.

**Good luck and may the best controller win!** 🤖🏎️
