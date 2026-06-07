
---

#  Healthcare Predictor

A mobile machine learning project that predicts individual healthcare costs using **synthetic data** generated to reflect healthcare trends in **Lesotho**.

Built with:

*  **FastAPI** backend
*  **Flutter** mobile app
*  Deployed on **Render**

---

##  Mission & Problem

This project offers a predictive tool to help individuals—especially low-income or uninsured—estimate healthcare costs.
It enables better financial planning and supports informed decision-making in low-access settings.
The model is built on synthetic data representing Lesotho’s healthcare landscape.
It simulates a real-world solution for tackling cost-related barriers to care.

---

##  Model Performance

| Model                           | Test MSE      | Test R²    | Test MAE   |
| ------------------------------- | ------------- | ---------- | ---------- |
| **Linear Regression (GD)**      | 191,449.03    | 0.9284     | 340.82     |
| **Linear Regression (Sklearn)** | 192,898.68    | 0.9279     | 341.52     |
| **Decision Tree**               | 170,737.14    | 0.9362     | 314.74     |
| **Random Forest**               | **66,985.90** | **0.9750** | **202.69** |


 **Chosen Model:** *Linear Regression*

> Chosen for its simplicity, fast inference on mobile, interpretability, and low risk of overfitting—making it ideal for deployment in real-world, low-resource settings.

---

## 🔗 Public API (Hosted on Render)

* **Base URL:**
  [`https://healthcare-predictor-aelg.onrender.com`](https://healthcare-predictor-aelg.onrender.com)

* **Swagger Docs:**
  [`/docs`](https://healthcare-predictor-aelg.onrender.com/docs)

>  Test predictions, explore required fields, and validate inputs via Swagger UI.

---

## 📱 Running the Flutter Mobile App

### 1. Clone the Repo


```
git clone https://github.com/<your-username>/<repo-name>.git

cd Healthcare_Prediction/healthcare_app_flutter
```
### 2. Update API Endpoint in Dart

Edit `api_service.dart`:

```dart
static const String baseUrl = 'https://healthcare-predictor-aelg.onrender.com';
```

### 3. Install Dependencies

```
flutter pub get
```

### 4. Run the App

```
flutter run
```

---

##  Run the API Locally (Optional)

```
cd Healthcare_Predictor/API
pip install -r requirements.txt
uvicorn main:app --reload
```

---

## Demo Video 
🔗 [**Watch the Video**](https://youtu.be/VMmscT9nAo0?si=be-fjM3RQ0YUlgUW)

---

##  Project Structure

```
Healthcare_Predictor/
            ├── API/
            │   ├── best_model.pkl
            │   ├── feature_names.pkl
            │   ├── prediction.py
            │   ├── scaler.pkl
            │   ├── start.sh
            │   └── healthcare_app_flutter/     # The mobile frontend
            ├── linear_regression/
            │   └── Multivariate.ipynb          # Model training notebook
            ├── lesotho_healthcare_costs.csv   # Synthetic dataset
            ├── main.py                         # FastAPI app
            ├── render.yaml                     # Render deployment config
            └── requirements.txt


---


