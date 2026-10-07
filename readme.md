# 🧠 Student Mental Health Score Prediction

A machine learning project that predicts a student's **Mental Health Score** based on their social media usage, lifestyle habits, and personal attributes. Includes end-to-end ML pipeline, model comparison with GridSearchCV, Streamlit app, and a custom FastAPI + HTML/CSS/JS frontend.

---

## 📌 Problem Statement

Social media usage has become an integral part of student life, but its impact on mental health is a growing concern. The goal of this project is to build a regression model that can **predict a student's mental health score** based on factors like:

- Daily social media usage hours
- Sleep patterns
- Study hours
- Physical activity
- Stress level
- Academic level

This model can help educators, counsellors, and students themselves **identify risk factors** and take proactive measures to improve mental well-being.

---

## 📊 Dataset

- **Source:** [Student Social Media and Mental Health Impact — Kaggle](https://www.kaggle.com/datasets/shivasingh4945/student-social-media-and-mental-health-impact)
- **Size:** 4,998 rows × 13 columns
- **Target:** `Mental_Health_Score` (continuous numeric value)
- **Problem Type:** Regression

### Feature Description

| Feature | Type | Description |
|---------|------|-------------|
| `Age` | Numeric | Student's age |
| `Gender` | Categorical | Male / Female / Other |
| `Country` | Categorical | Country of residence |
| `Academic_Level` | Categorical | High School / Bachelor's / Master's / PhD |
| `Most_Used_Platform` | Categorical | Instagram, Facebook, TikTok, etc. |
| `Purpose_Of_Use` | Categorical | Education, Entertainment, Socializing, etc. |
| `Avg_Daily_Usage_Hours` | Numeric | Average hours spent on social media daily |
| `Daily_Unlocks` | Numeric | Number of phone unlocks per day |
| `Study_Hours` | Numeric | Daily study hours |
| `Physical_Activity_Hours` | Numeric | Daily physical activity hours |
| `Sleep_Hours_Per_Night` | Numeric | Average sleep hours per night |
| `Stress_Level` | Categorical | Low / Medium / High / Very High |
| **`Mental_Health_Score`** | **Target** | **Mental health score (continuous)** |

---

## 🔬 Project Workflow

### 1. Exploratory Data Analysis (EDA)
- Checked target distribution (`Mental_Health_Score`)
- Analyzed numeric feature correlations with target
- Computed mean target per categorical category
- Examined relationships: sleep, usage hours, stress → mental health
- Identified key predictors: `Stress_Level`, `Avg_Daily_Usage_Hours`, `Sleep_Hours_Per_Night`

### 2. Preprocessing Pipeline
- **Numeric features:** Median imputation → Standard Scaling
- **Ordinal feature (`Stress_Level`):** Ordinal Encoding (Low < Medium < High < Very High)
- **Categorical features:** Most-frequent imputation → One-Hot Encoding

### 3. Models Compared with GridSearchCV

Each model was tuned using `GridSearchCV` with `scoring='r2'` and `cv=5`:

| Algorithm | Parameters Tuned |
|-----------|------------------|
| **Linear Regression** | (No hyperparameters) |
| **Decision Tree Regressor** | `criterion`, `max_depth`, `min_samples_split`, `min_samples_leaf`, `max_features` |
| **Random Forest Regressor** | `n_estimators`, `max_depth`, `min_samples_split`, `min_samples_leaf`, `max_features` |
| **Gradient Boosting Regressor** | `n_estimators`, `learning_rate`, `max_depth`, `subsample` |

---

## 📈 Results

### Model Comparison (Test Set)

| Model | R² | RMSE | MAE |
|-------|-----|------|-----|
| Linear Regression | 0.744 | 0.677 | 0.532 |
| Decision Tree Regressor | 0.770 | 0.641 | 0.411 |
| Gradient Boosting Regressor | 0.806 | 0.589 | 0.457 |
| **Random Forest Regressor** | **0.889** | **0.445** | **0.328** |
| Best RF (Tuned via GridSearchCV) | 0.881 | 0.460 | 0.346 |

### 🏆 Best Model: **Random Forest Regressor**

**Best Hyperparameters (GridSearchCV):**
```python
{
    'n_estimators': 100,
    'max_depth': 10,
    'max_features': 'sqrt',
    'min_samples_split': 2,
    'min_samples_leaf': 2
}
```
---
Test Set Performance:

R² Score: 0.881 → Model explains 88.1% of variance

RMSE: 0.460

MAE: 0.346

---

### 📊 Why Random Forest Won

- Captures non-linear patterns	
- Handles mixed features	
- Ensemble effect	Reduces variance of individual decision trees
- Robust to outliers	

---

## 🖥️ Applications
1. Streamlit App
An interactive web app where users can input their habits and get a predicted mental health score.

2. FastAPI + Custom Frontend
A production-ready API with a custom HTML/CSS/JS frontend for a modern UI.

---

## 🛠️ Project Structure

student_mental_health/
│
├── data/
│   └── student_social_media_mental_health.csv
│
├── notebooks/
│   ├── 01_eda.ipynb
│   ├── 02_preprocessing.ipynb
│   └── 03_model_training.ipynb
│
├── fastapi/
│   ├── main.py
│   ├── modling/
│   │   └── predict.py
│   └── schema/
│       └── user_input.py
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── models/
│   ├── best_random_forest.pkl
│
├── streamlit_app/
│   └── app.py
│
├── .gitignore
├── README.md
└── requirements.txt

---

## 🚀 How to Run

1. Installation
```bash
git clone https://github.com/yourusername/student-mental-health.git
cd student-mental-health

python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

pip install -r requirements.txt

```
2. Run Streamlit App

```bash
  streamlit run streamlit/app.py
```
3. Run FastAPI

```bash
cd fastapi
uvicorn main:app --reload
```

## Author
Majid Mehmood

---


📄 License
- This project is licensed under the MIT License.


---
### if you see this project help full  give it a star ⭐.  


