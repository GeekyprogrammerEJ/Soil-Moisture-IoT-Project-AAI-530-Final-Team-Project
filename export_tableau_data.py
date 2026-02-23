"""
Export CSV files for Tableau Public dashboard.
AAI-530 Final Team Project — Soil Moisture IoT Application.

Run this script after placing your data in archive/Hourly and archive/Daily.
It creates the folder tableau_export/ and writes:
  - tableau_status_current.csv   (status viz: latest per location)
  - tableau_summary_history.csv (summary viz: weekly averages)
  - tableau_ml_lr_moisture.csv  (ML viz 1: LR actual vs predicted)
  - tableau_ml_lstm_temperature.csv (ML viz 2: LSTM actual vs predicted)

Then connect these in Tableau Public and build your 4+ visualizations.
"""

import os
import glob
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error

# Optional: TensorFlow for LSTM (skip LSTM export if not installed)
try:
    import tensorflow as tf
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import LSTM, Dense, Dropout
    from tensorflow.keras.callbacks import EarlyStopping
    HAS_TF = True
except ImportError:
    HAS_TF = False

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
dataset_path = os.path.join(os.getcwd(), "archive")
out_dir = os.path.join(os.getcwd(), "tableau_export")
os.makedirs(out_dir, exist_ok=True)
print("Output directory:", out_dir)

# ---------------------------------------------------------------------------
# 1. Load data
# ---------------------------------------------------------------------------
hourly_files = glob.glob(os.path.join(dataset_path, "Hourly", "*.txt"))
daily_files = glob.glob(os.path.join(dataset_path, "Daily", "*.txt"))
if not hourly_files:
    raise FileNotFoundError(f"No hourly files in {dataset_path}/Hourly")

hourly_df = pd.concat(
    [pd.read_csv(f, sep="\t") for f in hourly_files],
    ignore_index=True
)
hourly_df.columns = hourly_df.columns.str.strip().str.lower()
time_col = "date" if "date" in hourly_df.columns else [c for c in hourly_df.columns if "time" in c or "date" in c][0]
hourly_df[time_col] = pd.to_datetime(hourly_df[time_col], errors="coerce")
hourly_df = hourly_df.sort_values(time_col).ffill().bfill()

# ---------------------------------------------------------------------------
# 2. STATUS: Latest reading per location (current status)
# ---------------------------------------------------------------------------
# For each location, take the row with the most recent date/time
idx_latest = hourly_df.groupby("location")[time_col].idxmax()
status_df = hourly_df.loc[idx_latest][["location", time_col, "vw_30cm", "t_30cm"]].copy()
status_df.columns = ["Location", "Latest_DateTime", "VW_30cm", "T_30cm"]
status_path = os.path.join(out_dir, "tableau_status_current.csv")
status_df.to_csv(status_path, index=False)
print("Saved:", status_path)

# ---------------------------------------------------------------------------
# 3. SUMMARY: Historical weekly averages
# ---------------------------------------------------------------------------
ts = pd.to_datetime(hourly_df[time_col])
# Week start (Monday) for Tableau date axis
hourly_df["Week_Start"] = ts - pd.to_timedelta(ts.dt.dayofweek, unit="D")
hourly_df["Week_Start"] = hourly_df["Week_Start"].dt.normalize()
summary_df = hourly_df.groupby("Week_Start").agg(
    Avg_VW_30cm=("vw_30cm", "mean"),
    Avg_T_30cm=("t_30cm", "mean"),
    Record_Count=("vw_30cm", "count"),
).reset_index()
summary_df = summary_df.rename(columns={"Week_Start": "Week"})
summary_path = os.path.join(out_dir, "tableau_summary_history.csv")
summary_df.to_csv(summary_path, index=False)
print("Saved:", summary_path)

# ---------------------------------------------------------------------------
# 4. ML 1: Linear Regression — actual vs predicted moisture (one location)
# ---------------------------------------------------------------------------
loc = hourly_df["location"].value_counts().index[0]
df = hourly_df[hourly_df["location"] == loc].copy().dropna(subset=["vw_30cm"])
df = df.sort_values(time_col)

target = "vw_30cm"
for i in range(1, 7):
    df[f"lag_{i}"] = df[target].shift(i)
df["roll_mean_6"] = df[target].rolling(6).mean().shift(1)
df = df.dropna()

feat_cols = [c for c in df.columns if c.startswith("lag_") or c == "roll_mean_6"]
train_size = int(0.8 * len(df))
train, test = df.iloc[:train_size], df.iloc[train_size:]
X_train, y_train = train[feat_cols], train[target]
X_test, y_test = test[feat_cols], test[target]

lr = LinearRegression()
lr.fit(X_train, y_train)
pred = lr.predict(X_test)

lr_export = pd.DataFrame({
    "Time_Index": range(len(y_test)),
    "Actual_VW_30cm": y_test.values,
    "Predicted_VW_30cm": pred,
})
lr_path = os.path.join(out_dir, "tableau_ml_lr_moisture.csv")
lr_export.to_csv(lr_path, index=False)
print("Saved:", lr_path)

# ---------------------------------------------------------------------------
# 5. ML 2: LSTM — actual vs predicted temperature (one location)
# ---------------------------------------------------------------------------
if HAS_TF:
    np.random.seed(42)
    tf.random.set_seed(42)

    path_hourly = os.path.join(dataset_path, "Hourly")
    files = glob.glob(os.path.join(path_hourly, "*.txt"))
    df_lstm = pd.concat([pd.read_csv(f, sep="\t") for f in files], ignore_index=True)
    df_lstm.columns = df_lstm.columns.str.strip().str.lower()
    tc = [c for c in df_lstm.columns if "time" in c or "date" in c][0]
    df_lstm[tc] = pd.to_datetime(df_lstm[tc], errors="coerce")
    df_lstm = df_lstm.sort_values(tc).ffill().bfill().dropna()

    loc = df_lstm["location"].value_counts().index[0]
    df_loc = df_lstm[df_lstm["location"] == loc].copy()
    target_col = "t_30cm"
    feat_cols = [c for c in df_loc.columns if c.startswith("vw_") or c.startswith("t_")]

    HORIZON = 6
    df_loc["y"] = df_loc[target_col].shift(-HORIZON)
    df_loc = df_loc.dropna(subset=["y"])

    X_raw = df_loc[feat_cols].values.astype(np.float32)
    y_raw = df_loc["y"].values.astype(np.float32)

    scaler_x = MinMaxScaler()
    scaler_y = MinMaxScaler()
    X_scaled = scaler_x.fit_transform(X_raw)
    y_scaled = scaler_y.fit_transform(y_raw.reshape(-1, 1)).flatten()

    LOOKBACK = 24
    X_seq, y_seq = [], []
    for i in range(LOOKBACK, len(X_scaled)):
        X_seq.append(X_scaled[i - LOOKBACK:i])
        y_seq.append(y_scaled[i])
    X_seq = np.array(X_seq)
    y_seq = np.array(y_seq)

    split = int(0.8 * len(X_seq))
    X_train_lstm, X_test_lstm = X_seq[:split], X_seq[split:]
    y_train_lstm, y_test_lstm = y_seq[:split], y_seq[split:]

    model = Sequential([
        LSTM(64, return_sequences=True, input_shape=(LOOKBACK, len(feat_cols))),
        Dropout(0.2),
        LSTM(32, return_sequences=False),
        Dropout(0.2),
        Dense(1),
    ])
    model.compile(optimizer="adam", loss="mse", metrics=["mae"])
    early = EarlyStopping(monitor="val_loss", patience=3, restore_best_weights=True)
    model.fit(
        X_train_lstm, y_train_lstm,
        validation_split=0.1, epochs=15, batch_size=64,
        callbacks=[early], verbose=0
    )

    y_pred_s = model.predict(X_test_lstm, verbose=0).flatten()
    y_pred = scaler_y.inverse_transform(y_pred_s.reshape(-1, 1)).flatten()
    y_actual = scaler_y.inverse_transform(y_test_lstm.reshape(-1, 1)).flatten()

    lstm_export = pd.DataFrame({
        "Time_Index": range(len(y_actual)),
        "Actual_T_30cm": y_actual,
        "Predicted_T_30cm": y_pred,
    })
    lstm_path = os.path.join(out_dir, "tableau_ml_lstm_temperature.csv")
    lstm_export.to_csv(lstm_path, index=False)
    print("Saved:", lstm_path)
else:
    # No TensorFlow: create a placeholder so Tableau still has a file
    lstm_export = pd.DataFrame({
        "Time_Index": [0],
        "Actual_T_30cm": [0.0],
        "Predicted_T_30cm": [0.0],
    })
    lstm_path = os.path.join(out_dir, "tableau_ml_lstm_temperature.csv")
    lstm_export.to_csv(lstm_path, index=False)
    print("Saved (placeholder; install TensorFlow for real LSTM):", lstm_path)

print("\nDone. Use the CSV files in tableau_export/ in Tableau Public to build your dashboard.")
