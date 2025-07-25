Perfect, got you! Here's the **final edited version** of your `README.md` reflecting:

✅ Title = **Healthcare Predictor**
✅ Data = **Synthetic data based on Lesotho**
✅ Everything clean, focused, and submission-ready.

---

# 🧠 Healthcare Predictor

A mobile-first machine learning project that predicts individual healthcare costs using **synthetic data** generated to reflect healthcare trends in **Lesotho**.

Built with:

* ⚙️ **FastAPI** backend
* 📱 **Flutter** mobile app
* ☁️ Deployed on **Render**

---

## 🎯 Mission & Problem

Predicting healthcare costs helps improve financial planning and access to medical services. This solution uses **synthetic data based on Lesotho** to simulate real-world health-related spending patterns and predict costs based on key factors like age, income, region, and more.

---

## 📊 Model Performance

| Model             | Train R² | Test R² | Test MAE | Test MSE   |
| ----------------- | -------- | ------- | -------- | ---------- |
| Linear Regression | 0.9447   | 0.9224  | 371.04   | 218,304.28 |
| Decision Tree     | 1.0000   | 0.9529  | 293.96   | 132,412.84 |
| Random Forest     | 0.9970   | 0.9764  | 210.45   | 66,469.49  |

✅ **Chosen Model:** *Linear Regression*

> Chosen for its simplicity, fast inference on mobile, interpretability, and low risk of overfitting—making it ideal for deployment in real-world, low-resource settings.

---

## 🔗 Public API (Hosted on Render)

* **Base URL:**
  [`https://healthcare-predictor-aelg.onrender.com`](https://healthcare-predictor-aelg.onrender.com)

* **Swagger Docs:**
  [`/docs`](https://healthcare-predictor-aelg.onrender.com/docs)

> 🧪 Test predictions, explore required fields, and validate inputs via Swagger UI.

---

## 📱 Running the Flutter Mobile App

### 1. Clone the Repo

``
git clone https://github.com/<your-username>/<repo-name>.git
cd linear_regression_model/summative/FlutterApp
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

## 🧪 Run the API Locally (Optional)

```
cd linear_regression_model/summative/API
pip install -r requirements.txt
uvicorn main:app --reload
```

---

## 🎥 Demo Video

📺 [Watch the Demo on YouTube](https://your-youtube-link.com)

---

## 📂 Project Structure

```
Healthcare_Predictor/
            ├── API/
            │   ├── best_model.pkl
            │   ├── feature_names.pkl
            │   ├── prediction.py
            │   ├── scaler.pkl
            │   ├── start.sh
            │   └── healthcare_app_flutter/     # Your mobile frontend
            ├── linear_regression/
            │   └── Multivariate.ipynb          # Model training notebook
            ├── lesotho_healthcare_costs.csv   # Synthetic dataset
            ├── main.py                         # FastAPI app
            ├── render.yaml                     # Render deployment config
            └── requirements.txt


---


