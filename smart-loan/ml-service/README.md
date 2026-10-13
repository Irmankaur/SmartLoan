# Smart Loan Machine Learning Service

This service provides real-time financial stress prediction and strategy evaluation using a trained **scikit-learn Random Forest Classifier**.

## Architecture & Integration
```
Browser (JSP/HTML/JS) 
   │
   ▼
Java Servlets (SimulatorServlet, RiskServlet, StrategyServlet)
   │
   ▼
Java Service Layer (MLClient.java / FinancialIntelligenceService.java)
   │
   ▼ HTTP (POST JSON to http://127.0.0.1:5001)
Python ML REST API (Flask, app.py)
   │
   ▼
Scikit-Learn Random Forest Model (model.joblib)
```

## Features Used by the Model
1. `income`: Monthly take-home income
2. `expenses`: Monthly living expenses
3. `total_emi`: Total monthly EMI obligations
4. `debt_to_income`: Total EMI / Monthly Income
5. `outstanding_debt`: Total principal outstanding across all loans
6. `liquid_savings`: Liquid cash & deposits available
7. `emergency_reserve`: Dedicated emergency fund
8. `reserve_coverage`: Emergency reserve / Monthly expenses (months of coverage)
9. `salary_reduction_pct`: Simulated salary reduction (0% - 100%)
10. `emergency_expense`: Simulated one-time medical or life emergency expense
11. `interest_rate_change`: Simulated interest rate hike across loans (0% - 15%)

## Target Label Definition: `repayment_stress_next_3_months`
Binary classification target ($1 =$ Repayment Distress within 3 months, $0 =$ Solvent and Resilient):
- True ($1$) if monthly cash flow under shock turns negative and remaining emergency reserves cannot sustain 3 months of burn, OR if the simulated EMI burden exceeds 60% with inadequate liquidity ($<1$ month).
- False ($0$) if the borrower maintains positive cash flow or sufficient emergency reserves to safely absorb the shock without missed payments.

## Model Evaluation Metrics
Reported on a 20% holdout test set (3,000 samples) in `model_evaluation.json`:
- **ROC-AUC:** 0.9487
- **F1-Score:** 0.8382
- **Accuracy:** 0.8933
- **Precision:** 0.7918
- **Recall:** 0.8904
- **Brier Score:** 0.0842 (indicates well-calibrated probabilities)

## How to Run on Windows
1. Open PowerShell or Command Prompt.
2. Navigate to `d:\godrej3\smart-loan\ml-service`.
3. Run:
   ```cmd
   run_ml_service.bat
   ```
   or directly:
   ```cmd
   python app.py
   ```
4. The service listens on `http://127.0.0.1:5001`.

## Endpoints
- `GET /health`: Healthcheck and model status
- `POST /predict-risk`: Predict repayment stress probability, risk category, and risk drivers for given financial profile and shock parameters.
- `POST /evaluate-strategy`: Evaluate candidate repayment strategies under stress scenarios and rank them.
