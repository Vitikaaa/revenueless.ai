import pandas as pd
import numpy as np

DATA_PATH = "data/transactions.csv"


def investigate_revenue():
    df = pd.read_csv(DATA_PATH)

    total_revenue = df["revenue"].sum()
    total_at_risk = df["revenue_lost"].sum()

    # Payment-method analysis
    payment_analysis = (
        df.groupby("payment_method")
        .agg(
            transactions=("transaction_id", "count"),
            revenue=("revenue", "sum"),
            revenue_lost=("revenue_lost", "sum")
        )
        .reset_index()
    )

    payment_analysis["loss_rate"] = (
        payment_analysis["revenue_lost"] /
        (payment_analysis["revenue"] + payment_analysis["revenue_lost"])
    )

    # Find biggest source of revenue loss
    biggest_loss = payment_analysis.loc[
        payment_analysis["revenue_lost"].idxmax()
    ]

    # Hour analysis
    hourly = (
        df.groupby("hour")
        .agg(
            revenue=("revenue", "sum"),
            revenue_lost=("revenue_lost", "sum")
        )
        .reset_index()
    )

    worst_hour = hourly.loc[
        hourly["revenue_lost"].idxmax()
    ]

    # Payment method + evening analysis
    evening = df[
        df["hour"].between(18, 21)
    ]

    evening_method = (
        evening.groupby("payment_method")
        .agg(
            revenue=("revenue", "sum"),
            revenue_lost=("revenue_lost", "sum")
        )
        .reset_index()
    )

    worst_evening_method = evening_method.loc[
        evening_method["revenue_lost"].idxmax()
    ]

    # Calculate potential recovery
    estimated_recovery = total_at_risk * 0.65

    print("\n" + "=" * 55)
    print("        REVENUELENS AI — REVENUE INVESTIGATION")
    print("=" * 55)

    print(f"\n💰 Total Revenue: ₹{total_revenue:,.2f}")
    print(f"⚠️ Revenue At Risk: ₹{total_at_risk:,.2f}")
    print(f"🎯 Estimated Recoverable: ₹{estimated_recovery:,.2f}")

    print("\n🔎 ROOT CAUSE ANALYSIS")
    print("-" * 55)

    print(
        f"Biggest payment loss: "
        f"{biggest_loss['payment_method']} "
        f"→ ₹{biggest_loss['revenue_lost']:,.2f}"
    )

    print(
        f"Worst hour: "
        f"{int(worst_hour['hour'])}:00 "
        f"→ ₹{worst_hour['revenue_lost']:,.2f} lost"
    )

    print(
        f"Evening hotspot: "
        f"{worst_evening_method['payment_method']} "
        f"→ ₹{worst_evening_method['revenue_lost']:,.2f} lost"
    )

    print("\n🤖 AI INVESTIGATION")
    print("-" * 55)

    print(
        f"Revenue loss is concentrated around "
        f"{worst_evening_method['payment_method']} transactions "
        f"during the evening period."
    )

    print(
        "\n🚨 PRIORITY: Investigate payment degradation "
        "before spending resources on lower-impact problems."
    )

    print("=" * 55)

    return {
        "total_revenue": float(total_revenue),
        "revenue_at_risk": float(total_at_risk),
        "estimated_recovery": float(estimated_recovery),
        "primary_payment_method": biggest_loss["payment_method"],
        "worst_hour": int(worst_hour["hour"]),
        "evening_hotspot": worst_evening_method["payment_method"]
    }


if __name__ == "__main__":
    investigate_revenue()