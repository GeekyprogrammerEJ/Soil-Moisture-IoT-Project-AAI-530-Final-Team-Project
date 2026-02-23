# Tableau Public — Detailed Step-by-Step Guide

**AAI-530 Final Team Project — Soil Moisture IoT Dashboard**

Use this guide after you have run `export_tableau_data.py` and have the four CSV files in the `tableau_export` folder.

---

## Part 1: Get Tableau Public and the data

### Step 1.1 — Install Tableau Public (if needed)

1. Go to **https://www.tableau.com/products/public**.
2. Click **Download the Free App** and install Tableau Public.
3. Open Tableau Public and sign in (or create a free account).

### Step 1.2 — Confirm your data files

In your project folder, open the **tableau_export** folder. You should see:

| File | Columns (after connection) |
|------|----------------------------|
| `tableau_status_current.csv` | Location, Latest_DateTime, VW_30cm, T_30cm |
| `tableau_summary_history.csv` | Week, Avg_VW_30cm, Avg_T_30cm, Record_Count |
| `tableau_ml_lr_moisture.csv` | Time_Index, Actual_VW_30cm, Predicted_VW_30cm |
| `tableau_ml_lstm_temperature.csv` | Time_Index, Actual_T_30cm, Predicted_T_30cm |

---

## Part 2: Connect to the data

### Step 2.1 — Connect to the first CSV (Status)

1. On the start screen, under **Connect**, click **Text file** (or **Microsoft Excel** if you prefer; CSVs open as text).
2. Browse to your **tableau_export** folder and select **tableau_status_current.csv**.
3. In the data preview, check that you see: **Location**, **Latest_DateTime**, **VW_30cm**, **T_30cm**.
4. If **Latest_DateTime** is not recognized as a date/time, click the icon next to it and choose **Date** or **Date & Time**.
5. Click **Sheet 1** at the bottom to go to the worksheet (you will rename it later).

### Step 2.2 — Add the other three data sources

1. In the top menu, click **Data** → **New Data Source** (or the **New Data Source** icon in the left data pane).
2. Connect to **tableau_summary_history.csv** from **tableau_export**. Check: **Week**, **Avg_VW_30cm**, **Avg_T_30cm**, **Record_Count**. Set **Week** to a date type if needed. Click **Sheet 2** (or add a new sheet).
3. Repeat: **Data** → **New Data Source** → **tableau_ml_lr_moisture.csv**. Check: **Time_Index**, **Actual_VW_30cm**, **Predicted_VW_30cm**. Use **Sheet 3**.
4. Repeat: **Data** → **New Data Source** → **tableau_ml_lstm_temperature.csv**. Check: **Time_Index**, **Actual_T_30cm**, **Predicted_T_30cm**. Use **Sheet 4**.

You should now have four data sources and at least four sheets. Rename each sheet (double-click the sheet tab at the bottom) to: **Status**, **Summary**, **LR Actual vs Predicted**, **LSTM Actual vs Predicted**.

---

## Part 3: Build each of the four sheets

### Sheet 1 — Status (current sensor status)

**Data source:** tableau_status_current.csv  
**Goal:** Show latest moisture and temperature by location (current status).

1. At the bottom, select the sheet that uses **tableau_status_current** (e.g. **Status**).
2. In the **Data** pane (left), confirm you see: Location, Latest_DateTime, VW_30cm, T_30cm.
3. **Build the view:**
   - Drag **Location** to **Rows** (or **Columns** if you prefer horizontal bars).
   - Drag **T_30cm** to **Columns** (or **Rows**). You should see a bar chart by location.
   - To add moisture on the same sheet: drag **VW_30cm** to the opposite axis (e.g. **Rows** if T_30cm is on Columns), or use **Dual Axis** (right-click the second measure → **Dual Axis**) so both measures show. Alternatively, create two separate bar charts stacked (e.g. one for T_30cm, one for VW_30cm) and place them on the dashboard.
4. **Important:** Ensure the axis shows **T_30cm** and **VW_30cm** values (e.g. 0–30 for temperature, 0–0.5 for moisture), **not** “Number of Records” or counts (e.g. 0–200K). If you see huge numbers, remove any **CNT(Number of Records)** from Rows/Columns and use only the measure **T_30cm** / **VW_30cm**.
5. **Title:** Double-click the title at the top and set it to: **Current Sensor Status — Latest Moisture & Temperature by Location**.
6. **Axis labels:** Right-click axes → **Edit Axis** and set clear names (e.g. “Temperature (°C)”, “Volumetric water (VW_30cm)”).

---

### Sheet 2 — Summary (historical)

**Data source:** tableau_summary_history.csv  
**Goal:** Line chart of average moisture and temperature over time (weekly).

1. Select the sheet that uses **tableau_summary_history** (e.g. **Summary**).
2. **Build the view:**
   - Drag **Week** to **Columns**.
   - Drag **Avg_T_30cm** to **Rows**. You should see one line (average temperature by week).
   - To add average moisture: drag **Avg_VW_30cm** to the **Rows** shelf. Tableau may add it to the same axis or create a second axis. If both measures are on the same axis and scales differ a lot, use **Dual Axis** (right-click the second measure in the view → **Dual Axis**) and format the second axis (e.g. 0–0.5 for VW).
3. **Important:** Use **Avg_T_30cm** and **Avg_VW_30cm** (measures from the CSV), not “Number of Records.”
4. **Title:** **Historical Summary — Average Soil Moisture & Temperature by Week**.
5. **Axis labels:** e.g. “Week”, “Avg temperature (°C)” / “Avg moisture (VW_30cm)”.

---

### Sheet 3 — LR actual vs predicted (soil moisture)

**Data source:** tableau_ml_lr_moisture.csv  
**Goal:** Show Linear Regression performance (actual vs predicted VW_30cm).

**Option A — Scatter (recommended)**

1. Select the sheet that uses **tableau_ml_lr_moisture** (e.g. **LR Actual vs Predicted**).
2. Drag **Actual_VW_30cm** to **Columns**.
3. Drag **Predicted_VW_30cm** to **Rows**.
4. **If you only see one point:** Tableau is aggregating all rows into a single mark. Fix it:
   - Go to the top menu **Analysis** → **Aggregate Measures** and **uncheck** it (turn it OFF).  
   - You should now see one point per row (a full scatter).  
   - **Alternative:** Drag **Time_Index** from the Data pane into the **Detail** box in the **Marks** card (so each time index is one mark). Then you can turn **Aggregate Measures** back on if you prefer.
5. You get a scatter: points near the diagonal mean good predictions. Optionally add a **Reference Line** (Analytics → Reference Line → Line) with slope 1 and intercept 0.
6. **Important:** Axes must show **Actual_VW_30cm** and **Predicted_VW_30cm** (typically 0.1–0.4), not “Number of Records” or Time_Index unless you intend a time-series view.

**Option B — Line over time**

1. Drag **Time_Index** to **Columns**.
2. Drag **Actual_VW_30cm** to **Rows** (one line).
3. Drag **Predicted_VW_30cm** to **Rows** (second line). Use different colors (e.g. Actual = blue, Predicted = orange) via **Color** in the Marks card.
4. **Important:** Use the measure pills **Actual_VW_30cm** and **Predicted_VW_30cm**, not counts.

**Title:** **Model 1 — Linear Regression: Actual vs Predicted Soil Moisture (VW_30cm)**.

---

### Sheet 4 — LSTM actual vs predicted (soil temperature)

**Data source:** tableau_ml_lstm_temperature.csv  
**Goal:** Show LSTM performance (actual vs predicted T_30cm).

**Option A — Scatter (recommended)**

1. Select the sheet that uses **tableau_ml_lstm_temperature** (e.g. **LSTM Actual vs Predicted**).
2. Drag **Actual_T_30cm** to **Columns**.
3. Drag **Predicted_T_30cm** to **Rows**.
4. **If you only see one point:** Go to **Analysis** → **Aggregate Measures** and **uncheck** it so Tableau shows one point per row. Or drag **Time_Index** to the **Detail** box in the Marks card.
5. Axes should show temperature values (e.g. 0–30 °C), **not** row counts (e.g. 0–180K). If you see 0K–180K, remove **CNT(Number of Records)** and use only **Actual_T_30cm** and **Predicted_T_30cm**.

**Option B — Line over time**

1. Drag **Time_Index** to **Columns**.
2. Drag **Actual_T_30cm** and **Predicted_T_30cm** to **Rows**; use **Color** to distinguish them.

**Title:** **Model 2 — LSTM: Actual vs Predicted Soil Temperature (T_30cm), 6h Ahead**.

---

## Part 4: Create the dashboard

1. At the bottom, click **New Dashboard** (dashboard icon) or **Dashboard** → **New Dashboard**.
2. Name the dashboard (e.g. **Soil Moisture IoT — AAI-530 Final Project**).
3. In the left panel under **Sheets**, you should see: Status, Summary, LR Actual vs Predicted, LSTM Actual vs Predicted.
4. **Add sheets to the dashboard:**
   - Drag **Status** onto the canvas (e.g. bottom-right or top-left).
   - Drag **Summary** next to it.
   - Drag **LR Actual vs Predicted** and **LSTM Actual vs Predicted** so all four are visible.
5. **Layout:** Use a 2×2 grid (e.g. Status | Summary on top, LR | LSTM on bottom) or: Status and Summary on top, both ML sheets on bottom. Resize by dragging sheet borders.
6. **Consistent colors (optional):** For LR and LSTM sheets, use the same color for “Actual” (e.g. blue) and “Predicted” (e.g. orange) so the rubric’s “consistent color scheme” is met.
7. **Dashboard title:** At the top, enable **Show dashboard title** and set a clear title (e.g. **Soil Moisture IoT — Status, Summary & ML Insights**).

---

## Part 5: Publish to Tableau Public and get the link

1. **File** → **Save to Tableau Public** (or the cloud icon).
2. Sign in to Tableau Public if prompted.
3. Enter a **Workbook name** (e.g. *Soil Moisture IoT Dashboard*) and optionally a **Project**.
4. Click **Save**. Tableau uploads the workbook.
5. When it finishes, the workbook opens in your browser. Copy the **URL** from the address bar (e.g. `https://public.tableau.com/views/...`). This is the **dashboard link** you will submit.

---

## Part 6: Export the dashboard as PDF

1. In Tableau Public (desktop), open your dashboard tab.
2. **File** → **Print to PDF** (or **Export as PDF** if your version has it).  
   - If you don’t see that, use **File** → **Print** and choose **Save as PDF** or **Microsoft Print to PDF** as the printer.
3. Choose the **tableau_export** folder (or your project folder) and save as **Soil_Moisture_Tableau_Dashboard.pdf**.
4. This PDF is what you submit along with the Tableau Public link.

---

## Quick checklist before submission

- [ ] All **four** sheets are on the dashboard: Status, Summary, LR, LSTM.
- [ ] **Status** uses **VW_30cm** and **T_30cm** (latest by location), not record counts.
- [ ] **Summary** uses **Avg_VW_30cm** and **Avg_T_30cm** over **Week**.
- [ ] **LR** and **LSTM** charts use **actual and predicted measure fields**; axes show realistic ranges (e.g. moisture 0.1–0.4, temperature 0–30), not 0K–180K.
- [ ] Titles and axis labels are clear on every sheet.
- [ ] Dashboard is saved to Tableau Public and the **link** is copied.
- [ ] **PDF** of the dashboard is exported and saved for submission.

---

## If axes show wrong scale (e.g. 0K–180K)

- In the view, look at **Rows** and **Columns**. Remove any **CNT(Number of Records)** or **SUM(Time_Index)** if you wanted measures.
- For scatter/line charts, **Columns** and **Rows** should be the **measure** fields: e.g. **Actual_T_30cm**, **Predicted_T_30cm**, **Actual_VW_30cm**, **Predicted_VW_30cm**.
- If you have both measures on one axis, ensure they are **SUM(Actual_T_30cm)** and **SUM(Predicted_T_30cm)** (or **AVG**), not count of rows.
