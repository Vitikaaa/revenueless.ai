import os
import numpy as np
import pandas as pd

np.random.seed(42)

N = 50000

data = pd.DataFrame({
    "transaction_id": [f"TXN{i:06d}" for i in range(N)],
    "merchant_id": np.random.choice(
        ["M001", "M002", "M003", "M004", "M005"], N
    ),
    "customer_id": [f"C{i:06d}" for i in np.random.randint(1, 10000, N)],
    "amount": np.round(np.random.lognormal(7.2, 0.8, N), 2),
    "payment_method": np.random.choice(
        ["UPI", "CARD", "NETBANKING", "WALLET"],
        N,
        p=[0.55, 0.25, 0.12, 0.08]
    ),
    "status": np.random.choice(
        ["captured", "failed"],
        N,
        p=[0.92, 0.08]
    ),
    "hour": np.random.randint(0, 24, N),
    "retry_count": np.random.choice(
        [0, 1, 2, 3],
        N,
        p=[0.65, 0.2, 0.1, 0.05]
    ),
    "checkout_started": np.random.choice(
        [0, 1], N, p=[0.15, 0.85]
    ),
})

# Checkout abandonment
data["checkout_completed"] = (
    (data["checkout_started"] == 1) &
    (data["status"] == "captured")
).astype(int)

# Revenue actually received
data["revenue"] = np.where(
    data["status"] == "captured",
    data["amount"],
    0
)

# Potential revenue lost from failed payments
data["revenue_lost"] = np.where(
    data["status"] == "failed",
    data["amount"],
    0
)

# Inject a realistic payment incident
incident = (
    (data["payment_method"] == "UPI") &
    (data["hour"].between(18, 21))
)

incident_indices = data[incident].sample(
    frac=0.25,
    random_state=42
).index

data.loc[incident_indices, "status"] = "failed"
data.loc[incident_indices, "revenue"] = 0
data.loc[incident_indices, "revenue_lost"] = (
    data.loc[incident_indices, "amount"]
)

# Create data folder if needed
os.makedirs("data", exist_ok=True)

output_path = "data/transactions.csv"
data.to_csv(output_path, index=False)

print(f"Generated {len(data):,} transactions")
print(f"Saved to: {output_path}")
print(f"Total revenue: ₹{data['revenue'].sum():,.2f}")
print(f"Revenue at risk: ₹{data['revenue_lost'].sum():,.2f}")