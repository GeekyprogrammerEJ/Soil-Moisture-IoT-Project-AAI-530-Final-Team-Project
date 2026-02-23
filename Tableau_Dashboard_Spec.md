# Tableau Public Dashboard — Specification & Instructions

**AAI-530 Final Team Project — Soil Moisture IoT Application**

You must submit:
1. **A PDF** of your dashboard (export or screenshot from Tableau Public).
2. **A link** to your dashboard on Tableau Public.

The dashboard must include **at least four visualizations** as follows.

---

## Required Visualizations (4 minimum)

### 1. Status visualization (current status)

**Purpose:** Tell the user something about the **current** status of the IoT system.

**Suggested content:**
- **Latest soil moisture (VW_30cm) and/or temperature (T_30cm) by sensor location**  
  Use the file: `tableau_status_current.csv`  
- **Chart type:** Horizontal bar chart or symbol map (if you have lat/long), or a table/card showing “most recent reading per location.”
- **Fields:** Location, Latest Date/Time, VW_30cm, T_30cm (or one of them).
- **Title example:** “Current sensor status — latest moisture & temperature by location.”

---

### 2. Summary visualization (historical)

**Purpose:** Tell the user something about **historical** data from the devices.

**Suggested content:**
- **Average soil moisture (VW_30cm) and/or temperature (T_30cm) over time** (e.g. by week or month).  
  Use: `tableau_summary_history.csv`
- **Chart type:** Line chart — X: date (week or month), Y: average VW_30cm and/or T_30cm; optionally break by Location.
- **Title example:** “Historical summary — average soil moisture (and temperature) by week.”

---

### 3. ML insight 1 — Linear Regression (soil moisture)

**Purpose:** Communicate the **machine learning insight** from Model 1 (LR predicting VW_30cm).

**Suggested content:**
- **Actual vs predicted soil moisture** over the test period.  
  Use: `tableau_ml_lr_moisture.csv`
- **Chart type:** Line chart (Actual vs Predicted over time index) or scatter (Actual on X, Predicted on Y).
- **Title example:** “Model 1 — Linear Regression: actual vs predicted soil moisture (VW_30cm).”

---

### 4. ML insight 2 — LSTM (soil temperature)

**Purpose:** Communicate the **machine learning insight** from Model 2 (LSTM predicting T_30cm).

**Suggested content:**
- **Actual vs predicted soil temperature** over the test period.  
  Use: `tableau_ml_lstm_temperature.csv`
- **Chart type:** Line chart or scatter (same idea as above).
- **Title example:** “Model 2 — LSTM: actual vs predicted soil temperature (T_30cm), 6h ahead.”

---

## Design (Module 5 best practices)

- **Pre-attentive attributes:** Use color/size to highlight what matters (e.g. one color for actual, another for predicted).
- **Consistent color scheme:** Same palette across all sheets (e.g. blue for actual, orange for predicted).
- **Logical order:** e.g. Status (top/left) → Summary → ML insight 1 → ML insight 2.
- **Clear titles and axis labels:** Every sheet has a descriptive title and labeled axes.

---

## Steps to build the dashboard

1. **Export the data**  
   Run the script `export_tableau_data.py` (see below). It creates CSVs in the `tableau_export` folder.

2. **Open Tableau Public**  
   Go to [https://www.tableau.com/products/public](https://www.tableau.com/products/public) and download Tableau Public (free), or use the web version if available.

3. **Connect to the CSVs**  
   Connect to each CSV (or connect once to a folder and use multiple sheets). Drag the CSVs into the data pane.

4. **Build the four sheets**  
   - Sheet 1: Status (current by location).  
   - Sheet 2: Summary (historical averages).  
   - Sheet 3: LR actual vs predicted (moisture).  
   - Sheet 4: LSTM actual vs predicted (temperature).

5. **Create a dashboard**  
   Drag the four sheets onto one dashboard. Resize and label so the layout is clear.

6. **Publish**  
   Save to Tableau Public. Sign in and choose “Save to Tableau Public.” Note the **dashboard URL**.

7. **Export PDF**  
   In Tableau Public: **File → Print to PDF** (or use your OS print dialog and “Save as PDF”). Submit this PDF with the assignment.

8. **Submit**  
   Submit the **PDF** and the **Tableau Public dashboard link** via the assignment instructions.

---

## Data files (created by `export_tableau_data.py`)

| File | Purpose |
|------|--------|
| `tableau_status_current.csv` | Latest reading per location (status viz). |
| `tableau_summary_history.csv` | Aggregated history by week (summary viz). |
| `tableau_ml_lr_moisture.csv` | Actual vs predicted VW_30cm (LR insight). |
| `tableau_ml_lstm_temperature.csv` | Actual vs predicted T_30cm (LSTM insight). |

Run the export script **after** your notebook has loaded and (if needed) run the model cells so the script can reuse the same data and model outputs, or the script can load data and run a minimal pipeline to generate the CSVs.

---

## Scoring rubric alignment (Tableau Dashboard — 20% / 46 pts)

The grading criterion is: *"All four required visualizations are present and organized in an effective way to communicate the major data insights."*

### Required visualizations (assignment instructions)

| # | Rubric / assignment requirement | This dashboard |
|---|----------------------------------|-----------------|
| 1 | **At least one status visualization** — “current” status of the IoT device (e.g. number of devices online, current level) | **Status** sheet: latest moisture (VW_30cm) and temperature (T_30cm) by sensor **Location** → “current” status by location. |
| 2 | **At least one summary visualization** — historical data (e.g. averages over time) | **Summary** sheet: **Avg_VW_30cm** and **Avg_T_30cm** by **Week** → historical summary. |
| 3 | **At least one visualization for ML insight 1** | **LR Actual vs Predicted** sheet: actual vs predicted soil moisture (VW_30cm) from Linear Regression. |
| 4 | **At least one visualization for ML insight 2** | **LSTM Actual vs Predicted** sheet: actual vs predicted soil temperature (T_30cm) from LSTM. |

**Total: four visualizations** → meets “at least four” and “all four required.”

### “Organized in an effective way to communicate major data insights”

Module 5 and the instructions say visualizations should:

| Requirement | How to meet it in your dashboard |
|-------------|-----------------------------------|
| **Pre-attentive attributes** (color/size to highlight what matters) | Use color to distinguish Actual vs Predicted in LR and LSTM sheets; use color or length in Status/Summary to show values. |
| **Consistent color scheme** | Use the same palette across sheets (e.g. blue for actual, orange for predicted in both ML sheets). |
| **Logical order** | Arrange sheets in a clear order, e.g. Status → Summary → LR insight → LSTM insight (e.g. top-left to bottom-right). |
| **Clean and clear titles and labels** | Give each sheet a descriptive title and label axes (e.g. “Temperature (°C)”, “Volumetric water (VW_30cm)”). |

### Rubric levels (quick check)

- **Meets or exceeds (46 pts):** All four required visualizations present **and** layout/design support clear communication (titles, labels, order, consistent colors).
- **Approaches (41.4 pts):** All four present but layout/design not clearly aimed at communication.
- **Below (37.72 pts):** Only two or three visualizations, even if well organized.
- **Inadequate (32.2 pts):** Two or three visualizations and not well organized.
- **Non-performance (0 pts):** Dashboard missing or only one visualization.

**Conclusion:** If your published dashboard has the four sheets above, with clear titles, labeled axes, sensible order, and consistent colors, it **aligns with the scoring rubric** for the Tableau Dashboard criterion.
