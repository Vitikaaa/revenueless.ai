import { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [data, setData] = useState(null);
  const [recovery, setRecovery] = useState(null);
  const [loading, setLoading] = useState(true);
  const [question, setQuestion] = useState("");
  const [copilot, setCopilot] = useState(null);
  const [asking, setAsking] = useState(false);

  useEffect(() => {
    Promise.all([
      fetch("http://127.0.0.1:8000/api/investigate"),
      fetch("http://127.0.0.1:8000/api/recovery"),
    ])
      .then(async ([investigateResponse, recoveryResponse]) => {
        const investigateData = await investigateResponse.json();
        const recoveryData = await recoveryResponse.json();

        setData(investigateData.investigation);
        setRecovery(recoveryData);
        setLoading(false);
      })
      .catch((error) => {
        console.error("API error:", error);
        setLoading(false);
      });
  }, []);
const askCopilot = async () => {
  if (!question.trim()) return;

  setAsking(true);

  try {
    const response = await fetch(
      "http://127.0.0.1:8000/api/copilot",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: question,
        }),
      }
    );

    const result = await response.json();

    setCopilot(result);
  } catch (error) {
    console.error("Copilot error:", error);
  }

  setAsking(false);
};
  const formatINR = (value) =>
    new Intl.NumberFormat("en-IN", {
      style: "currency",
      currency: "INR",
      maximumFractionDigits: 0,
    }).format(value);

  if (loading) {
    return <div className="loading">Loading RevenueLens AI...</div>;
  }

  if (!data || !recovery) {
    return (
      <div className="loading">
        Unable to connect to RevenueLens API.
      </div>
    );
  }

  const healthScore = Math.max(
    0,
    Math.round(
      100 - (data.revenue_at_risk / data.total_revenue) * 100
    )
  );

  return (
    <div className="app">

      {/* HEADER */}
      <header className="topbar">
        <div>
          <h1>
            RevenueLens <span>AI</span>
          </h1>
          <p>AI Revenue Copilot for Merchants</p>
        </div>

        <div className="live">
          <div className="dot"></div>
          Live Intelligence
        </div>
      </header>

      <main>

        {/* HERO */}
        <section className="hero">
          <div>
            <p className="eyebrow">REVENUE INTELLIGENCE</p>

            <h2>
              Know where your money is leaking.
            </h2>

            <p className="subtitle">
              RevenueLens continuously analyzes payment behavior,
              detects revenue loss and identifies recovery
              opportunities.
            </p>
          </div>

          <button className="investigate-btn">
            Investigate Revenue →
          </button>
        </section>

        {/* METRICS */}
        <section className="metrics">

          <div className="metric">
            <p>Total Revenue</p>

            <h3>
              {formatINR(data.total_revenue)}
            </h3>

            <span>Processed revenue</span>
          </div>

          <div className="metric danger">
            <p>Revenue At Risk</p>

            <h3>
              {formatINR(data.revenue_at_risk)}
            </h3>

            <span>Potentially lost</span>
          </div>

          <div className="metric success">
            <p>Estimated Recovery</p>

            <h3>
              {formatINR(data.estimated_recovery)}
            </h3>

            <span>Recoverable opportunity</span>
          </div>

        </section>

        {/* AI DETECTION + HEALTH */}
        <section className="grid">

          <div className="card alert-card">

            <div className="card-title">

              <span className="alert-icon">
                !
              </span>

              <div>
                <p className="eyebrow">
                  AI DETECTION
                </p>

                <h3>
                  Revenue Leakage Detected
                </h3>
              </div>

            </div>

            <p className="alert-text">
              Revenue loss is concentrated around{" "}
              <strong>
                {data.evening_hotspot}
              </strong>{" "}
              payments during the evening period.
            </p>

            <div className="finding">

              <div>
                <span>
                  Primary payment method
                </span>

                <strong>
                  {data.primary_payment_method}
                </strong>
              </div>

              <div>
                <span>
                  Worst hour
                </span>

                <strong>
                  {data.worst_hour}:00
                </strong>
              </div>

            </div>

            <div className="recommendation">

              <strong>
                🤖 AI Recommendation
              </strong>

              <p>
                Investigate payment degradation during
                peak evening traffic and prioritize
                eligible failed transactions for recovery.
              </p>

            </div>

          </div>


          <div className="card score-card">

            <p className="eyebrow">
              REVENUE HEALTH
            </p>

            <div className="score">

              <strong>
                {healthScore}
              </strong>

              <span>
                /100
              </span>

            </div>

            <h3>
              Revenue Health Score
            </h3>

            <div className="progress">

              <div
                style={{
                  width: `${healthScore}%`,
                }}
              ></div>

            </div>

            <p>
              Your revenue engine is operating,
              but there are recoverable payment
              opportunities.
            </p>

          </div>

        </section>


        {/* RECOVERY OPPORTUNITIES */}
        <section className="card recovery-card">

          <div className="section-heading">

            <div>
              <p className="eyebrow">
                ML-POWERED RECOVERY
              </p>

              <h3>
                Top Recovery Opportunities
              </h3>

              <p>
                RevenueLens prioritizes failed payments
                based on their predicted recovery value.
              </p>
            </div>

            <div className="recovery-total">
              {formatINR(recovery.potential_recovery)}
              <span>potential recovery</span>
            </div>

          </div>


          <div className="table-container">

            <table>

              <thead>
                <tr>
                  <th>Transaction</th>
                  <th>Amount</th>
                  <th>Payment</th>
                  <th>Retries</th>
                  <th>Recovery</th>
                  <th>Expected ₹</th>
                </tr>
              </thead>

              <tbody>

                {recovery.top_opportunities.map(
                  (transaction) => (

                    <tr
                      key={transaction.transaction_id}
                    >

                      <td>
                        <strong>
                          {transaction.transaction_id}
                        </strong>
                      </td>

                      <td>
                        {formatINR(transaction.amount)}
                      </td>

                      <td>
                        <span className="payment-badge">
                          {transaction.payment_method}
                        </span>
                      </td>

                      <td>
                        {transaction.retry_count}
                      </td>

                      <td>
                        <strong className="recovery-percent">
                          {Math.round(
                            transaction.recovery_probability * 100
                          )}
                          %
                        </strong>
                      </td>

                      <td>
                        <strong>
                          {formatINR(
                            transaction.expected_recovery
                          )}
                        </strong>
                      </td>

                    </tr>

                  )
                )}

              </tbody>

            </table>

          </div>

        </section>
{/* AI COPILOT */}
<section className="card copilot-card">

  <div className="copilot-header">
    <div>
      <p className="eyebrow">AI MERCHANT COPILOT</p>

      <h3>Ask RevenueLens 🤖</h3>

      <p>
        Ask questions about your revenue, payment failures
        and recovery opportunities.
      </p>
    </div>
  </div>

  <div className="copilot-input">

    <input
      type="text"
      value={question}
      onChange={(e) => setQuestion(e.target.value)}
      onKeyDown={(e) => {
        if (e.key === "Enter") {
          askCopilot();
        }
      }}
      placeholder="Why am I losing revenue?"
    />

    <button onClick={askCopilot}>
      {asking ? "Analyzing..." : "Ask"}
    </button>

  </div>

  <div className="suggestions">

    <button
      onClick={() => {
        setQuestion("Why am I losing revenue?");
      }}
    >
      Why am I losing revenue?
    </button>

    <button
      onClick={() => {
        setQuestion("Where am I losing money?");
      }}
    >
      Where am I losing money?
    </button>

    <button
      onClick={() => {
        setQuestion("What should I fix first?");
      }}
    >
      What should I fix first?
    </button>

    <button
      onClick={() => {
        setQuestion("Which payments should I recover?");
      }}
    >
      Which payments should I recover?
    </button>

  </div>


  {copilot && (
    <div className="copilot-response">

      <div className="response-label">
        🤖 REVENUELENS ANALYSIS
      </div>

      <p className="copilot-answer">
        {copilot.answer}
      </p>

      <div className="copilot-action">

        <strong>
          NEXT BEST ACTION
        </strong>

        <p>
          {copilot.action}
        </p>

      </div>

      <div className="copilot-impact">

        <div>
          <span>Revenue at risk</span>
          <strong>
            {formatINR(copilot.metrics.revenue_at_risk)}
          </strong>
        </div>

        <div>
          <span>Potential recovery</span>
          <strong>
            {formatINR(copilot.metrics.potential_recovery)}
          </strong>
        </div>

      </div>

    </div>
  )}

</section>

        {/* NEXT ACTION */}
        <section className="card action-card">

          <div>

            <p className="eyebrow">
              NEXT BEST ACTION
            </p>

            <h3>
              Recover lost revenue before acquiring new customers.
            </h3>

            <p>
              RevenueLens has identified failed transactions
              with potential recovery value.
            </p>

          </div>

          <button>
            Recover Revenue →
          </button>

        </section>

      </main>

    </div>
  );
}

export default App;