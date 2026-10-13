import os
import json
import joblib
import numpy as np
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load model and feature metadata
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model.joblib")
EVAL_PATH = os.path.join(BASE_DIR, "model_evaluation.json")

model = None
feature_importances = []
evaluation_metrics = {}

try:
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
        print("Scikit-learn model loaded successfully.")
    if os.path.exists(EVAL_PATH):
        with open(EVAL_PATH, "r") as f:
            eval_data = json.load(f)
            feature_importances = eval_data.get("feature_importances", [])
            evaluation_metrics = eval_data.get("metrics", {})
except Exception as e:
    print(f"Error loading model or metadata: {e}")

FEATURE_NAMES = [
    "income",
    "expenses",
    "total_emi",
    "debt_to_income",
    "outstanding_debt",
    "liquid_savings",
    "emergency_reserve",
    "reserve_coverage",
    "salary_reduction_pct",
    "emergency_expense",
    "interest_rate_change"
]

def extract_features(data):
    """
    Extracts and validates features from incoming request dict,
    calculating derived metrics if omitted.
    """
    income = float(data.get("income", 0.0))
    expenses = float(data.get("expenses", 0.0))
    total_emi = float(data.get("total_emi", 0.0))
    outstanding_debt = float(data.get("outstanding_debt", 0.0))
    emergency_reserve = float(data.get("emergency_reserve", 0.0))
    liquid_savings = float(data.get("liquid_savings", emergency_reserve))

    # Derived metrics with zero-division safety
    debt_to_income = float(data.get("debt_to_income", total_emi / max(income, 1.0)))
    reserve_coverage = float(data.get("reserve_coverage", emergency_reserve / max(expenses, 1.0)))

    # Stress inputs
    salary_reduction_pct = float(data.get("salary_reduction_pct", 0.0))
    emergency_expense = float(data.get("emergency_expense", 0.0))
    interest_rate_change = float(data.get("interest_rate_change", 0.0))

    vec = [
        income,
        expenses,
        total_emi,
        debt_to_income,
        outstanding_debt,
        liquid_savings,
        emergency_reserve,
        reserve_coverage,
        salary_reduction_pct,
        emergency_expense,
        interest_rate_change
    ]
    return vec, {
        "income": income,
        "expenses": expenses,
        "total_emi": total_emi,
        "debt_to_income": debt_to_income,
        "outstanding_debt": outstanding_debt,
        "liquid_savings": liquid_savings,
        "emergency_reserve": emergency_reserve,
        "reserve_coverage": reserve_coverage,
        "salary_reduction_pct": salary_reduction_pct,
        "emergency_expense": emergency_expense,
        "interest_rate_change": interest_rate_change
    }

def get_risk_category(prob):
    if prob < 0.25:
        return "Low Risk (Healthy & Resilient)"
    elif prob < 0.55:
        return "Moderate Risk (Manageable with Care)"
    elif prob < 0.80:
        return "High Risk (Vulnerable to Shocks)"
    else:
        return "Critical Risk (Severe Distress Warning)"

def generate_driver_explanations(f):
    drivers = []
    if f["reserve_coverage"] < 1.5:
        drivers.append(f"Emergency reserve is critically low ({f['reserve_coverage']:.1f} months of expenses), leaving no cushion against income shocks.")
    elif f["reserve_coverage"] < 3.0:
        drivers.append(f"Emergency buffer ({f['reserve_coverage']:.1f} months) is below the recommended 3-6 month safety threshold.")
    
    if f["debt_to_income"] > 0.45:
        drivers.append(f"EMI burden consumes {f['debt_to_income']*100:.1f}% of monthly take-home pay, well above safe banking limits (35-40%).")
    
    if f["salary_reduction_pct"] > 0:
        drivers.append(f"Hypothetical salary cut of {f['salary_reduction_pct']:.0f}% reduces monthly cash flow.")
    
    if f["emergency_expense"] > 0:
        drivers.append(f"One-time emergency expense of ₹{f['emergency_expense']:,.0f} directly drains liquid savings.")

    if f["interest_rate_change"] > 0:
        drivers.append(f"Interest rate increase of {f['interest_rate_change']:.2f}% raises monthly EMI obligations.")

    if not drivers:
        drivers.append("Strong reserve coverage and healthy debt-to-income ratio protect against immediate repayment distress.")
    return drivers

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "SmartLoan-ML-Engine",
        "model_loaded": model is not None,
        "model_type": "RandomForestClassifier",
        "n_features": len(FEATURE_NAMES),
        "metrics": evaluation_metrics
    })

@app.route("/predict-risk", methods=["POST"])
def predict_risk():
    if model is None:
        return jsonify({"status": "error", "message": "Model not loaded"}), 503

    try:
        data = request.get_json(force=True)
        if not data:
            return jsonify({"status": "error", "message": "Empty or invalid JSON body"}), 400

        vec, feature_dict = extract_features(data)
        X = np.array([vec])
        proba = float(model.predict_proba(X)[0][1])
        prediction = int(proba >= 0.5)
        category = get_risk_category(proba)
        drivers = generate_driver_explanations(feature_dict)

        return jsonify({
            "status": "success",
            "stress_probability": round(proba, 4),
            "stress_prediction": prediction,
            "risk_category": category,
            "features_used": feature_dict,
            "risk_drivers": drivers,
            "feature_importances": feature_importances[:6]
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/evaluate-strategy", methods=["POST"])
def evaluate_strategy():
    if model is None:
        return jsonify({"status": "error", "message": "Model not loaded"}), 503

    try:
        data = request.get_json(force=True)
        user_data = data.get("user", {})
        strategies = data.get("strategies", [])
        salary_cut = float(data.get("salary_reduction_pct", 0.0))
        emergency_exp = float(data.get("emergency_expense", 0.0))
        rate_change = float(data.get("interest_rate_change", 0.0))

        results = []
        for strat in strategies:
            strat_name = strat.get("name", "Unknown")
            post_emi = float(strat.get("post_total_emi", user_data.get("total_emi", 0.0)))
            post_debt = float(strat.get("post_total_debt", user_data.get("outstanding_debt", 0.0)))
            post_reserve = float(strat.get("post_emergency_reserve", user_data.get("emergency_reserve", 0.0)))

            strat_feature_data = {
                "income": user_data.get("income", 0.0),
                "expenses": user_data.get("expenses", 0.0),
                "total_emi": post_emi,
                "outstanding_debt": post_debt,
                "emergency_reserve": post_reserve,
                "liquid_savings": post_reserve,
                "salary_reduction_pct": salary_cut,
                "emergency_expense": emergency_exp,
                "interest_rate_change": rate_change
            }
            vec, _ = extract_features(strat_feature_data)
            proba = float(model.predict_proba(np.array([vec]))[0][1])

            results.append({
                "name": strat_name,
                "stress_probability": round(proba, 4),
                "risk_category": get_risk_category(proba),
                "interest_saved": strat.get("interest_saved", 0.0),
                "months_saved": strat.get("months_saved", 0),
                "description": strat.get("description", "")
            })

        # Rank strategies: lowest stress probability first, tie-break by highest interest saved
        results.sort(key=lambda x: (x["stress_probability"], -float(x.get("interest_saved", 0))))

        return jsonify({
            "status": "success",
            "evaluations": results,
            "recommended_strategy": results[0]["name"] if results else None
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    print(f"Starting Smart Loan ML Service on port {port}...")
    app.run(host="127.0.0.1", port=port, debug=False)
