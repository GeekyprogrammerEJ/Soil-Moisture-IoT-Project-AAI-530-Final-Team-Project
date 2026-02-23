# Assignment 2.2: Final Team Project Introduction and Proposal  
**AAI-530 Machine Learning IoT Application**  
**Due:** 20 Jan by 13:29

---

## 1. Team and Project Overview

Our team will design and implement a **machine learning IoT application** using a **soil moisture sensor network** dataset. We will produce a theoretical IoT system design, apply at least two machine learning methods (including one deep learning model and one time series prediction), and present insights on a Tableau Public dashboard. All code will be hosted and documented on **GitHub** with a README and in-code comments.

---

## 2. Dataset Introduction

### 2.1 Source and Eligibility

- **Dataset:** Soil Moisture Data from Field-Scale Sensor Network  
- **Source:** [Kaggle](https://www.kaggle.com/datasets/sathyanarayanrao89/soil-moisture-data-from-field-scale-sensor-network/data)  
- **Eligibility:**  
  - **Real IoT sensors:** Data comes from real field-scale sensor networks (not simulated).  
  - **Not restricted:** The dataset is not the Household Energy Consumption, Air Quality, or Continuous Glucose Monitoring datasets used in course assignments.  
  - **Time series:** The data includes multiple time series variables (volumetric water and temperature at multiple depths over time).

### 2.2 Data Description

- **Granularity:** Hourly and daily readings from multiple locations (42 sites, e.g., CAF095).  
- **Variables:**  
  - **Location** – sensor/site identifier  
  - **Date / Time** – temporal index  
  - **Volumetric water content (VW):** `VW_30cm`, `VW_60cm`, `VW_90cm`, `VW_120cm`, `VW_150cm` (soil moisture at 30–150 cm depth)  
  - **Soil temperature (T):** `T_30cm`, `T_60cm`, `T_90cm`, `T_120cm`, `T_150cm` (temperature at same depths)  
- **Scale:** Hourly dataset ~3.37M rows × 13 columns; daily dataset ~140K rows × 12 columns.  
- **Use case:** Irrigation planning, drought monitoring, and soil moisture / temperature forecasting for precision agriculture.

---

## 3. IoT Application and (Theoretical) System Design

### 3.1 Application

**Precision agriculture soil monitoring:**  
A system that collects soil moisture and temperature at multiple depths across fields, stores and processes the data in the cloud, runs machine learning models for short- and long-term predictions, and surfaces current status, historical summaries, and ML insights on a dashboard for farmers or agronomists.

### 3.2 System Components (to be detailed in the full report with diagram)

- **Sensors:** In-situ soil moisture and temperature probes at 30, 60, 90, 120, and 150 cm; deployed per location/site; limitations (e.g., calibration, depth representativeness, maintenance) will be documented.  
- **Edge processing:** Whether and where to do aggregation, validation, or lightweight alerts at the edge, and implications for edge device requirements.  
- **Networking:** How field devices connect (e.g., cellular, LoRa, gateway) and which messaging protocol (e.g., MQTT) is used to send data to the cloud.  
- **Data storage and processing:** Cloud storage (e.g., time-series DB or data lake), pipelines for cleaning and feature preparation, and where ML models (deep learning and time series) are trained and served. Scalability and deployment of insights will be addressed.

A full **system diagram** and **component documentation** will be included in the final submitted report.

---

## 4. Planned Machine Learning Methods

To meet the project requirements (at least **one deep learning** model and **one time series prediction**, predicting **different** variables):

1. **Deep learning time series model (e.g., LSTM):**  
   Built from scratch with TensorFlow/Keras (or similar). For example: predict **future soil moisture** (e.g., VW at 30 cm or aggregate moisture) using past sequences of moisture and temperature. This satisfies the “deep learning from scratch” and “time series prediction” requirements for one target.

2. **Second ML task (different target):**  
   Either a second time series predictor (e.g., **soil temperature** forecast using traditional ML or a second deep learning model) or a classifier (e.g., wet/dry or risk-level classification). The two models will predict **different** variables.

Exploratory analysis and cleaning (e.g., handling missing values, datetime handling, aggregation) will be documented in the code and report, consistent with the existing Soil Moisture notebook.

---

## 5. Planned Tableau Dashboard

The Tableau Public dashboard will include at least:

- **One status visualization:** e.g., current or latest soil moisture / temperature by location or depth.  
- **One summary visualization:** e.g., historical averages, trends, or counts over a chosen period.  
- **One visualization per ML insight:** one for the deep learning (e.g., moisture) predictions and one for the second model (e.g., temperature or classification).  

Design will follow course best practices: pre-attentive attributes, consistent color scheme, logical layout, and clear titles and labels.

---

## 6. Next Steps and Timeline

- **Module 2 (by end of Week 2):** Submit this proposal (Assignment 2.2).  
- **Module 4 (by end of Week 4):** Submit status report (PDF) describing chosen ML methods.  
- **Module 7 (by end of Week 7):** Submit final report (PDF), code (PDF/notebook + GitHub link), and dashboard (PDF + Tableau Public link).

We will use **GitHub** for version control and collaboration, with a README describing all repository files and comments throughout the code.

---

*This proposal introduces our dataset, IoT application, and high-level plan for the Final Team Project. The full system design diagram and detailed documentation will be included in the final report.*
