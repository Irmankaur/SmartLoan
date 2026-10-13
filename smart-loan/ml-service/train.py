import json
import os
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, brier_score_loss, confusion_matrix, classification_report
)

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

def generate_synthetic_data(num_samples=15000, random_seed=42):
    """
    Generates a realistic synthetic financial dataset of personal loan profiles
    across diverse economic segments in India (tier 1/2/3 earners, varied debt ratios,
    emergency reserves, and realistic macroeconomic/personal shock simulations).
    """
    np.random.seed(random_seed)

    # 1. Base Monthly Income: Log-normal distribution skewed towards median incomes (₹25,000 - ₹250,000)
    income = np.random.lognormal(mean=11.0, sigma=0.65, size=num_samples)
    income = np.clip(income, 20000.0, 400000.0)

    # 2. Monthly Expenses: 35% - 75% of income with noise
    expense_ratio = np.random.uniform(0.35, 0.75, size=num_samples)
    expenses = income * expense_ratio

    # 3. Existing Total EMI: 10% - 65% of income
    emi_ratio = np.random.uniform(0.10, 0.65, size=num_samples)
    total_emi = income * emi_ratio

    # 4. Debt to Income ratio (EMI burden)
    debt_to_income = total_emi / np.maximum(income, 1.0)

    # 5. Outstanding Debt: roughly 12 to 84 months of EMI with realistic tenure spreads
    tenure_months = np.random.uniform(12.0, 84.0, size=num_samples)
    outstanding_debt = total_emi * tenure_months * np.random.uniform(0.7, 0.95, size=num_samples)

    # 6. Emergency Reserve: 0.5 to 10 months of expenses
    reserve_months = np.random.exponential(scale=3.0, size=num_samples)
    reserve_months = np.clip(reserve_months, 0.1, 12.0)
    emergency_reserve = expenses * reserve_months

    # 7. Liquid Savings: emergency reserve + discretionary liquidity (0 - 3x monthly income)
    liquid_savings = emergency_reserve + (income * np.random.uniform(0.0, 3.0, size=num_samples))

    # 8. Reserve Coverage (months of expenses covered)
    reserve_coverage = emergency_reserve / np.maximum(expenses, 1.0)

    # 9. Simulated Shock Parameters (What-If stress test conditions)
    # Salary reduction (0% to 50%)
    salary_reduction_pct = np.random.choice([0.0, 10.0, 20.0, 30.0, 40.0, 50.0], size=num_samples, p=[0.35, 0.20, 0.20, 0.15, 0.05, 0.05])

    # Emergency Expense (₹0 to ₹250,000)
    emergency_expense = np.random.choice([0.0, 20000.0, 50000.0, 100000.0, 200000.0], size=num_samples, p=[0.40, 0.25, 0.20, 0.10, 0.05])

    # Interest rate hike across loans (0% to 5%)
    interest_rate_change = np.random.choice([0.0, 0.5, 1.0, 2.0, 3.0, 5.0], size=num_samples, p=[0.40, 0.25, 0.20, 0.10, 0.03, 0.02])

    # -------------------------------------------------------------
    # Explicit, Defensible Target Definition: `repayment_stress_next_3_months`
    # -------------------------------------------------------------
    # Simulate post-shock financial state over a 3-month forward horizon:
    simulated_income = income * (1.0 - salary_reduction_pct / 100.0)

    # Interest rate increase raises EMI proportionally
    # Approx EMI multiplier for small rate hikes: (1 + delta_r * 0.04)
    emi_hike_factor = 1.0 + (interest_rate_change * 0.045)
    simulated_total_emi = total_emi * emi_hike_factor

    # Monthly cash surplus / deficit after shock
    simulated_free_cash_flow = simulated_income - expenses - simulated_total_emi

    # Remaining emergency reserve after initial emergency expense
    post_shock_reserve = np.maximum(0.0, emergency_reserve - emergency_expense)

    # Cumulative 3-month cash position
    # If cash flow is negative, 3 months of deficit drains the reserve
    three_month_cash_burn = np.where(simulated_free_cash_flow < 0, np.abs(simulated_free_cash_flow) * 3.0, 0.0)
    reserve_depleted = post_shock_reserve < three_month_cash_burn

    # EMI to Income ratio under stress
    simulated_dti = simulated_total_emi / np.maximum(simulated_income, 1.0)

    # Target Label: 1 if user cannot sustain repayments without severe distress in the next 3 months:
    # Condition A: Negative monthly cash flow AND remaining reserve exhausted within 3 months.
    # Condition B: Simulated EMI burden > 60% of income AND post-shock reserve covers < 1 month of expenses.
    # Condition C: Severe cash flow deficit (> ₹15,000/mo) with reserve coverage < 1.5 months.
    condition_a = (simulated_free_cash_flow < 0) & reserve_depleted
    condition_b = (simulated_dti > 0.60) & (post_shock_reserve < expenses * 1.0)
    condition_c = (simulated_free_cash_flow < -15000.0) & (reserve_coverage < 1.5)

    target = (condition_a | condition_b | condition_c).astype(int)

    # Introduce realistic 2% real-world noise/unobserved variance
    noise_idx = np.random.choice(num_samples, size=int(num_samples * 0.02), replace=False)
    target[noise_idx] = 1 - target[noise_idx]

    df = pd.DataFrame({
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
        "interest_rate_change": interest_rate_change,
        "repayment_stress_next_3_months": target
    })

    return df

def train_and_evaluate():
    print("=" * 60)
    print("Generating synthetic financial dataset (15,000 samples)...")
    df = generate_synthetic_data(num_samples=15000, random_seed=42)

    X = df[FEATURE_NAMES]
    y = df["repayment_stress_next_3_months"]

    stress_rate = y.mean()
    print(f"Dataset generated. Target prevalence (Stress rate): {stress_rate * 100:.2f}%")

    # Stratified Train / Test split (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    print(f"Training set: {len(X_train)} samples, Test set: {len(X_test)} samples")
    print("Training scikit-learn RandomForestClassifier...")

    # Train Random Forest with calibrated hyperparameters for credit risk scoring
    model = RandomForestClassifier(
        n_estimators=120,
        max_depth=9,
        min_samples_split=6,
        min_samples_leaf=4,
        max_features="sqrt",
        random_state=42,
        class_weight="balanced",
        n_jobs=-1
    )
    model.fit(X_train, y_train)

    # Predictions
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    # Metrics
    acc = float(accuracy_score(y_test, y_pred))
    prec = float(precision_score(y_test, y_pred))
    rec = float(recall_score(y_test, y_pred))
    f1 = float(f1_score(y_test, y_pred))
    roc_auc = float(roc_auc_score(y_test, y_proba))
    brier = float(brier_score_loss(y_test, y_proba))
    cm = confusion_matrix(y_test, y_pred).tolist()

    print("\n--- MODEL EVALUATION METRICS ---")
    print(f"Accuracy:         {acc:.4f}")
    print(f"Precision:        {prec:.4f}")
    print(f"Recall:           {rec:.4f}")
    print(f"F1-Score:         {f1:.4f}")
    print(f"ROC-AUC:          {roc_auc:.4f}")
    print(f"Brier Score:      {brier:.4f} (lower is better, <0.10 is well-calibrated)")
    print(f"Confusion Matrix: TN={cm[0][0]}, FP={cm[0][1]}, FN={cm[1][0]}, TP={cm[1][1]}")

    # Feature Importances
    importances = model.feature_importances_
    feat_imp = []
    for name, imp in zip(FEATURE_NAMES, importances):
        feat_imp.append({"feature": name, "importance": round(float(imp), 4)})
    feat_imp.sort(key=lambda x: x["importance"], reverse=True)

    print("\n--- TOP FEATURE IMPORTANCES ---")
    for fi in feat_imp:
        print(f"  {fi['feature']:<22} : {fi['importance'] * 100:.2f}%")

    # Save artifacts
    script_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(script_dir, "model.joblib")
    eval_path = os.path.join(script_dir, "model_evaluation.json")
    features_path = os.path.join(script_dir, "features.json")

    joblib.dump(model, model_path)
    print(f"\nModel saved to: {model_path}")

    evaluation_report = {
        "model_type": "RandomForestClassifier",
        "n_estimators": 120,
        "max_depth": 9,
        "dataset_size": len(df),
        "test_size": len(X_test),
        "target": "repayment_stress_next_3_months",
        "metrics": {
            "accuracy": round(acc, 4),
            "precision": round(prec, 4),
            "recall": round(rec, 4),
            "f1_score": round(f1, 4),
            "roc_auc": round(roc_auc, 4),
            "brier_score": round(brier, 4),
            "confusion_matrix": {
                "true_negative": cm[0][0],
                "false_positive": cm[0][1],
                "false_negative": cm[1][0],
                "true_positive": cm[1][1]
            }
        },
        "feature_importances": feat_imp
    }

    with open(eval_path, "w") as f:
        json.dump(evaluation_report, f, indent=2)
    print(f"Evaluation report saved to: {eval_path}")

    with open(features_path, "w") as f:
        json.dump({"features": FEATURE_NAMES}, f, indent=2)
    print(f"Feature list saved to: {features_path}")
    print("=" * 60)

if __name__ == "__main__":
    train_and_evaluate()
