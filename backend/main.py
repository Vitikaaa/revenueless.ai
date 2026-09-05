from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
import os
import pandas as pd
import joblib

sys.path.append(os.path.abspath("."))

from ml.investigate import investigate_revenue

app = FastAPI(
    title="RevenueLens AI",
    description="AI-powered revenue intelligence for Razorpay merchants",
    version="0.2.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Load trained ML model
MODEL_PATH = "ml/models/recovery_model.pkl"
recovery_model = joblib.load(MODEL_PATH)


@app.get("/")
def home():
    return {
        "product": "RevenueLens AI",
        "status": "online",
        "message": "Revenue intelligence engine is running 🚀"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/api/investigate")
def investigate():
    result = investigate_revenue()

    return {
        "status": "success",
        "investigation": result
    }


@app.get("/api/recovery")
def recovery_prediction():
    df = pd.read_csv("data/transactions.csv")

    failed = df[df["status"] == "failed"].copy()

    features = [
        "amount",
        "retry_count",
        "hour",
        "checkout_started"
    ]

    # Predict probability of recovery
    failed["recovery_probability"] = (
        recovery_model.predict_proba(
            failed[features]
        )[:, 1]
    )

    # Expected recoverable revenue
    failed["expected_recovery"] = (
        failed["amount"] *
        failed["recovery_probability"]
    )

    # Highest-value opportunities
    opportunities = failed.sort_values(
        "expected_recovery",
        ascending=False
    ).head(10)

    return {
        "status": "success",
        "total_failed_transactions": len(failed),
        "potential_recovery": round(
            failed["expected_recovery"].sum(), 2
        ),
        "top_opportunities": opportunities[
            [
                "transaction_id",
                "amount",
                "payment_method",
                "retry_count",
                "recovery_probability",
                "expected_recovery"
            ]
        ].round(2).to_dict(orient="records")
    }
from pydantic import BaseModel


class CopilotQuestion(BaseModel):
    question: str


@app.post("/api/copilot")
def copilot(request: CopilotQuestion):

    question = request.question.lower()

    # Get the same intelligence already used by the dashboard
    investigation = investigate_revenue()

    total_revenue = investigation["total_revenue"]
    revenue_at_risk = investigation["revenue_at_risk"]
    estimated_recovery = investigation["estimated_recovery"]
    primary_method = investigation["primary_payment_method"]
    worst_hour = investigation["worst_hour"]
    evening_hotspot = investigation["evening_hotspot"]

    # Recovery data
    recovery_response = recovery_prediction()

    potential_recovery = recovery_response["potential_recovery"]
    opportunities = recovery_response["top_opportunities"]

    # Determine the merchant's intent
    if "why" in question and ("revenue" in question or "drop" in question):

        answer = (
            f"Your revenue leakage is concentrated around "
            f"{primary_method} payments, especially around {worst_hour}:00. "
            f"The analysis identifies ₹{revenue_at_risk:,.0f} of revenue at risk. "
            f"The strongest pattern is {evening_hotspot} payment activity "
            f"during the evening period."
        )

        action = (
            f"Prioritize investigation of {primary_method} payment degradation "
            f"around {worst_hour}:00 and recover high-probability failed payments."
        )

    elif "where" in question or "losing" in question:

        answer = (
            f"The largest leakage signal is associated with "
            f"{primary_method} transactions. "
            f"The worst observed hour is {worst_hour}:00."
        )

        action = (
            f"Focus your first intervention on {primary_method} transactions "
            f"during the evening window."
        )

    elif "recover" in question or "recovery" in question:

        answer = (
            f"I found ₹{potential_recovery:,.0f} in ML-ranked recovery "
            f"opportunities across failed transactions."
        )

        action = (
            f"Start with the highest expected-recovery transactions "
            f"rather than retrying every failed payment."
        )

    elif "fix" in question or "action" in question:

        answer = (
            f"The highest-impact issue is {primary_method} payment leakage "
            f"around {worst_hour}:00."
        )

        action = (
            f"Investigate payment degradation first, then prioritize "
            f"high-probability recovery opportunities."
        )

    else:

        answer = (
            f"RevenueLens analyzed your payment data and found "
            f"₹{revenue_at_risk:,.0f} of revenue at risk, with "
            f"₹{potential_recovery:,.0f} currently identified as "
            f"potential recovery."
        )

        action = (
            f"Start with {primary_method} payments around {worst_hour}:00 "
            f"and review the highest-value recovery opportunities."
        )

    return {
        "status": "success",
        "question": request.question,
        "answer": answer,
        "action": action,
        "metrics": {
            "total_revenue": total_revenue,
            "revenue_at_risk": revenue_at_risk,
            "estimated_recovery": estimated_recovery,
            "potential_recovery": potential_recovery,
        },
        "insight": {
            "primary_payment_method": primary_method,
            "worst_hour": worst_hour,
            "evening_hotspot": evening_hotspot,
        },
    }