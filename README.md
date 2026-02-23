# Final Team Project: Machine Learning IoT Application — Soil Moisture Sensor Network

AAI-530 Final Team Project. Design and implementation of an ML-enabled IoT application using the Soil Moisture Data from Field-Scale Sensor Network dataset.

## Repository Contents

| File / Folder | Description |
|---------------|-------------|
| `Soil Moisture Final notebook.ipynb` | Main Jupyter notebook: data load, cleaning, EDA, **two ML models** (LSTM for soil moisture, Linear Regression for soil temperature), and evaluation. |
| `Final_Report_APA7.md` | Final report content in APA 7 style (IoT system design, ML methods, dashboard design). Convert to PDF (10–15 pp, double-spaced) for submission. |
| `Assignment_2.2_Project_Proposal.md` | Project proposal (dataset and IoT application introduction). |
| `Final Project Instructions_SP23rev.pdf` | Course instructions for the final project. |
| `README.md` | This file — describes all files and how to run the code. |

## Dataset

- **Name:** Soil Moisture Data from Field-Scale Sensor Network  
- **Source:** [Kaggle](https://www.kaggle.com/datasets/sathyanarayanrao89/soil-moisture-data-from-field-scale-sensor-network/data)  
- **Contents:** Hourly and daily volumetric water content (VW) and soil temperature (T) at 30, 60, 90, 120, and 150 cm depth from 42 locations.  
- **Place data in:** An `archive` folder with `Hourly/` and `Daily/` subfolders containing `.txt` files (tab-separated), or set `dataset_path` in the notebook to your path.

## Python environment

**Option A — Use the project venv (recommended)**

The repo includes a virtual environment (Python 3.12) with all dependencies installed.

1. **Activate the environment**
   - **macOS/Linux:** `source venv/bin/activate`
   - **Windows:** `venv\Scripts\activate`

2. **Run the notebook**
   - In Cursor/VS Code: open `Soil Moisture Final notebook.ipynb`, click the kernel selector (top right), and choose **"Python (soil-moisture-env)"** if it appears.
   - Or from the terminal: `jupyter notebook` (after activating the venv), then open the notebook.

**Option B — Create the env from scratch**

TensorFlow requires Python 3.10–3.12 (not 3.14). If you don’t have the `venv` folder or want to recreate it:

```bash
python3.12 -m venv venv
source venv/bin/activate   # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python -m ipykernel install --user --name=soil-moisture-env --display-name="Python (soil-moisture-env)"
```

Then open the notebook and select the kernel **"Python (soil-moisture-env)"**.

## Running the Notebook

1. Clone the repo and place the dataset so the notebook can find it (e.g., `archive/Hourly/*.txt`).  
2. In the notebook, set `dataset_path` in the data-loading cells to your local or Kaggle path.  
3. Run cells in order. The notebook includes:
   - **Load & clean:** Load TXT files, normalize columns, handle missing values, datetime conversion.  
   - **EDA:** Time series, KDE, violin, correlation heatmaps, Sankey.  
   - **Model 1 — LSTM (soil moisture):** TensorFlow/Keras LSTM built from scratch; predicts next-step VW_30cm.  
   - **Model 2 — Linear Regression (soil temperature):** Lag/rolling features; predicts next-step T_30cm.

## Tableau Public dashboard

The project requires a **Tableau Public** dashboard (PDF + link) with at least **four visualizations**: one status, one summary, and one per ML insight.

1. **Export data for Tableau** (from project folder):
   ```bash
   source venv/bin/activate   # or use: ./venv/bin/python
   python export_tableau_data.py
   ```
   This creates the folder `tableau_export/` with four CSVs: status (latest per location), summary (weekly history), LR actual vs predicted (moisture), LSTM actual vs predicted (temperature).

2. **Build the dashboard in Tableau Public**  
   See **`Tableau_Dashboard_Spec.md`** for the exact four visualizations, field names, and design notes. Connect to the CSVs, build the sheets, then create one dashboard and publish to Tableau Public.

3. **Submit**  
   - Export the dashboard as **PDF** (File → Print to PDF or system print).  
   - Copy the **Tableau Public dashboard URL** after publishing.  
   - Submit both the PDF and the link with your final deliverables.

## Project Deliverables (Submission Checklist)

- [ ] **Report:** PDF of final report (APA 7, 10–15 pages, double-spaced) with IoT system diagram, ML methods, and dashboard design. Use `Final_Report_APA7.md` as content; add diagram figure and any tables/graphs, then export to PDF.  
- [ ] **Code:** PDF export of the notebook (or .py files) and **link to this GitHub repository** with all final code merged.  
- [ ] **Dashboard:** **PDF** of the Tableau dashboard and **link** to it on Tableau Public. At least four visualizations: one status, one summary, one for LR (moisture) insight, one for LSTM (temperature) insight.  
- [ ] Submit all PDFs and the GitHub and Tableau Public links via the course assignment link (one team member submits).

## License

For course use only.
