# RevenueLens AI

An AI revenue recovery copilot that helps merchants identify payment leakage and prioritize high-value recovery opportunities.

## Problem

Failed payments can leave merchants with hidden, recoverable revenue. Finding the important losses across transaction volume, payment methods, and peak hours is difficult.

## Solution

RevenueLens follows **Detect → Diagnose → Predict → Prioritize → Recover**. It measures revenue at risk, identifies payment and time-of-day risk signals, ranks failed transactions by expected recovery, and gives merchant teams a controlled recommendation.

## Features

- Revenue intelligence and revenue-at-risk detection
- Root-cause analysis
- ML recovery prediction and expected-recovery ranking
- AI Merchant Copilot
- Clearly labelled simulated recovery workflow
- Responsive merchant dashboard

## Architecture

```text
React → FastAPI → Python/Pandas → Revenue Investigation → ML Recovery Model → AI Copilot → Merchant Dashboard
```

## ML Approach

The recovery model uses `amount`, `retry_count`, `hour`, and `checkout_started` to predict recovery probability. Expected recovery is `amount × recovery probability`; failed transactions are ranked by that value.

## API Endpoints

- `GET /api/investigate`
- `GET /api/recovery`
- `POST /api/copilot`

## Demo

The prototype uses synthetic transaction data. The recovery queue is a simulation: it does not execute payment retries, contact customers, or integrate with Razorpay.

## Run locally

From the repository root, start the backend:

```bash
uvicorn backend.main:app --reload
```

Start the frontend:

```bash
cd frontend
npm run dev
```

## Future Scope

- Razorpay test-mode integration
- Automated, bounded recovery workflows
- Payment-method routing
- Real-time monitoring and merchant alerts
- Audit trail for review and recovery actions
