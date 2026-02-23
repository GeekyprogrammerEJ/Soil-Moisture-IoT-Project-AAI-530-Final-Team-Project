# Machine Learning IoT Application: Soil Moisture Sensor Network Design and Implementation

**AAI-530 Final Team Project**

---

*Note: Format this document in APA 7 style (double-spaced, 10–15 pages) in Word or Google Docs, then export to PDF for submission. Include the IoT system diagram as a figure and any selected tables/graphs from the notebook.*

---

## Title Page (APA 7)

**Machine Learning IoT Application: Design and Implementation of a Soil Moisture Sensor Network System**

[Author names]

[University name]

AAI-530: [Course title]

[Instructor name]

[Date]

---

## Abstract

This project designs and implements a machine learning–enabled IoT application for precision agriculture using a real-world soil moisture sensor network dataset. We present a theoretical end-to-end IoT system design (sensors, edge, networking, storage, and ML), implement two machine learning tasks—an LSTM deep learning model for soil moisture time series prediction and a linear regression model for soil temperature time series prediction—and describe dashboard design choices for communicating status, historical summaries, and ML insights. The dataset comprises hourly and daily volumetric water content and soil temperature at multiple depths from 42 field locations. The report is structured around the IoT system design, the two ML methods, and the Tableau dashboard visualizations required for the course deliverables.

*Keywords:* IoT, soil moisture, precision agriculture, LSTM, time series prediction, TensorFlow, Tableau

---

## Introduction

The Final Team Project for AAI-530 requires designing and implementing a machine learning IoT application using an existing IoT dataset, a complete (theoretical) IoT system design, at least two machine learning methods (including one deep learning model built from scratch and one time series prediction), and a Tableau Public dashboard with at least four visualizations (status, summary, and one per ML insight). This report documents our team’s work on a **soil moisture sensor network** application for precision agriculture.

We selected the **Soil Moisture Data from Field-Scale Sensor Network** dataset (Kaggle), which meets the course requirements: it comes from real IoT sensors, is not among the restricted datasets (Household Energy, Air Quality, Continuous Glucose Monitoring), and includes time series variables (volumetric water content and soil temperature at 30, 60, 90, 120, and 150 cm depth across 42 locations). The application supports irrigation planning, drought monitoring, and forecasting of soil moisture and temperature.

The remainder of the report is organized as follows: IoT system design (with diagram and component documentation), data processing and exploratory analysis, the two machine learning methods (LSTM for moisture, linear regression for temperature), dashboard design choices, and a brief conclusion.

---

## IoT System Design

We designed a theoretical end-to-end IoT system for a precision agriculture soil monitoring application that could collect, transmit, store, and analyze the same types of data as in our dataset. The design does not replicate the exact system that produced the dataset but reflects a realistic architecture using course concepts.

### Diagram Overview

The system consists of five main layers:

1. **Sensing layer** – In-situ soil moisture and temperature probes at multiple depths (30–150 cm) per monitoring location.
2. **Edge layer** – Optional gateways or edge devices for aggregation, validation, and local alerts.
3. **Networking layer** – Connectivity from field to cloud (e.g., cellular, LoRa, or gateway to backhaul).
4. **Data storage and ingestion** – Cloud-based time-series or relational storage and ingestion pipelines.
5. **Analytics and ML** – Training and serving of time series and deep learning models; generation of insights for the dashboard.

*Insert here a single figure (IoT System Diagram) showing: Sensors → Edge/Gateway → Network (e.g., MQTT/HTTP) → Cloud Storage & Processing → ML Models → Dashboard. Label each component. You can draw this in draw.io, Lucidchart, PowerPoint, or similar and paste into the report.*

### Component Documentation

**Sensors.** Soil moisture is measured using volumetric water content (VWC) sensors (e.g., capacitance or TDR), and soil temperature using thermistors or RTDs at 30, 60, 90, 120, and 150 cm depth at each location. Sensors are deployed in the field at multiple sites (e.g., 42 locations as in the dataset). Limitations include calibration drift, representativeness of a single probe per depth, and maintenance (e.g., damage, cable degradation). Location and depth are recorded with each reading.

**Edge processing.** The system may perform light edge computation on gateways or edge nodes: aggregating raw readings to hourly/daily to reduce bandwidth, validating ranges (e.g., VWC 0–1, temperature within plausible bounds), and raising local alerts for out-of-range or missing data. This affects edge device requirements: sufficient compute and memory for buffering and simple rules, and reliable power (e.g., solar or line power).

**Networking.** Field devices connect to the network via cellular modems, LoRa, or local gateways that backhaul to the internet. A messaging protocol such as MQTT or HTTP is used to send batches of sensor data to a cloud endpoint. MQTT is suitable for low-bandwidth, publish–subscribe telemetry; TLS is used for confidentiality and integrity.

**Data storage and processing.** Incoming device data is ingested into a cloud pipeline (e.g., message queue or serverless ingestion) and stored in a time-series database or data lake. Scalability is addressed by partitioning by location and time, and by using scalable compute (e.g., Spark or cloud ML) for cleaning and feature preparation. Machine learning models (LSTM and linear regression in our case) are trained on historical data in the cloud; insights can be produced in batch (e.g., daily predictions) or via an on-demand inference API, and are written to a store that the dashboard (Tableau) or another front end can consume.

---

## Data Processing and Exploratory Analysis

Our code (see submitted notebook and GitHub repository) includes loading of hourly and daily TXT files from the dataset, column normalization (lowercase, trimmed), and handling of missing values (e.g., forward-fill where appropriate). We combine files from all locations and convert date/time columns to datetime for time-based filtering and splitting.

Exploratory analysis includes: time series plots of moisture and temperature (hourly vs. daily) for representative locations; KDE and violin plots by season and wet/dry periods; correlation heatmaps across depths and between moisture and temperature; and Sankey-style flows of moisture state across seasons. Key findings used in modeling include: strong correlation among moisture at different depths and among temperatures at different depths (with temperature more redundant); negative correlation between moisture and temperature; and clear seasonality, supporting the use of lag and rolling features and sequence-based models (LSTM).

---

## Machine Learning Methods

The project requires at least one deep learning model built from scratch and at least one time series prediction, with the two models predicting **different** variables. We implemented:

### Method 1: LSTM Deep Learning (Soil Moisture Time Series Prediction)

We built a **Long Short-Term Memory (LSTM)** recurrent network from scratch using **TensorFlow/Keras**. No pre-built application-specific architectures or pre-trained models were used; we defined and trained the model ourselves.

- **Target variable:** Volumetric water content at 30 cm (VW_30cm)—i.e., soil moisture.
- **Inputs:** Sequences of past 24 hours of VW_30cm and T_30cm (min-max scaled).
- **Architecture:** Two LSTM layers (64 and 32 units) with Dropout (0.2), then Dense(16, ReLU) and Dense(1) for regression. Trained with Adam optimizer and MSE loss; early stopping on validation loss.
- **Train/test split:** Time-based (e.g., 80/20) to avoid leakage.
- **Output:** Next-step (1-hour-ahead) soil moisture prediction. Metrics (e.g., RMSE, MAE, R²) are reported on the test set after inverse-scaling predictions.

This satisfies the requirement for a deep learning method built from scratch and for a time series prediction (future value from past data).

### Method 2: Linear Regression (Soil Temperature Time Series Prediction)

We implemented a **linear regression** model for time series prediction of a **different** variable: soil temperature at 30 cm (T_30cm).

- **Target variable:** T_30cm (soil temperature).
- **Features:** Lagged values of T_30cm (e.g., lag_1–lag_6) and a rolling mean (e.g., 6-step) shifted by one step to avoid leakage. No future or current target in the feature set.
- **Train/test split:** Time-based.
- **Output:** Next-step soil temperature prediction. Metrics (RMSE, MAE, R²) are reported on the test set.

This ensures we have two distinct ML tasks predicting different variables: LSTM → moisture; linear regression → temperature. Both are time series predictions; one is deep learning, one is traditional ML.

---

## Dashboard Design Choices

The Tableau Public dashboard must include at least four visualizations: one status, one summary, and one for each of the two ML insights. Our design choices align with course best practices (Module 5).

**Status visualization.** We include a view that communicates the “current” (or most recent) state of the IoT application—e.g., latest soil moisture and/or temperature by location or by depth, or number of locations reporting. This gives the user an immediate snapshot of field status.

**Summary visualization.** We include a view of historical data—e.g., average moisture or temperature over the last week or month by location, or distribution of readings. This supports trend and variability assessment.

**ML insight visualizations.** One visualization communicates LSTM soil moisture predictions—e.g., time series of actual vs. predicted moisture, or a scatter of predicted vs. actual. A second visualization communicates linear regression temperature predictions—e.g., actual vs. predicted temperature over time or by location. Both use clear titles, axes labels, and a consistent color scheme (e.g., actual in one color, predicted in another).

**Design principles.** We use pre-attentive attributes (e.g., color and position) to highlight the most important information; a consistent color palette across the dashboard; logical layout (e.g., status first, then summary, then ML insights); and clean, descriptive titles and labels so that each chart is self-explanatory.

---

## Conclusion

This project delivered a complete machine learning IoT application design and implementation for a soil moisture sensor network: an APA-style report with IoT system design and diagram, two machine learning methods (LSTM for moisture and linear regression for temperature) with code in the submitted notebook and GitHub repository, and a Tableau Public dashboard with at least four visualizations (status, summary, and one per ML insight). The work aligns with the course requirements for dataset eligibility, deep learning from scratch, time series prediction, different prediction targets, and documented code and repository.

---

## References

*List any sources used (dataset, TensorFlow/Keras documentation, course materials). Example:*

Kaggle. (n.d.). *Soil moisture data from field-scale sensor network*. https://www.kaggle.com/datasets/sathyanarayanrao89/soil-moisture-data-from-field-scale-sensor-network/data

TensorFlow. (n.d.). *Keras API*. https://www.tensorflow.org/api_docs/python/tf/keras

*Add course textbook or instructor materials if cited.*

---

*End of report. Add the IoT system diagram as a figure in the body and any selected tables or graphs from the notebook before exporting to PDF.*
