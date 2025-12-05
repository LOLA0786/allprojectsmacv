import React, { useState } from "react";

export default function PaymentPanel() {
  const [currency, setCurrency] = useState("AUD");
  const [amount, setAmount] = useState("5");

  const razorpayLink = "https://razorpay.me/@pentaprimesolutionsllp";

  const presets = {
    AUD: 5,
    NZD: 5,
    USD: 5,
    INR: 100
  };

  const openPayment = () => {
    let finalLink = razorpayLink;

    // Razorpay sometimes supports ?amount=XXX (in base currency units)
    // But to avoid breaking the link, we open plain link + let user edit amount on Razorpay page.
    
    window.open(finalLink, "_blank");
  };

  return (
    <div>
      <h2 className="text-2xl font-bold mb-4">💳 Payments & Support</h2>

      <div className="bg-white rounded-lg shadow p-6 space-y-6 max-w-xl">

        <p className="text-slate-600">
          Support development of <strong>AuditPilot</strong> or activate premium features.
        </p>

        <div>
          <label className="font-semibold">Choose Your Country</label>
          <select
            value={currency}
            onChange={(e) => {
              setCurrency(e.target.value);
              setAmount(presets[e.target.value]);
            }}
            className="w-full border p-2 rounded-md mt-1"
          >
            <option value="AUD">🇦🇺 Australia (AUD)</option>
            <option value="NZD">🇳🇿 New Zealand (NZD)</option>
            <option value="USD">🇺🇸 United States (USD)</option>
            <option value="INR">🇮🇳 India (INR)</option>
          </select>
        </div>

        <div>
          <label className="font-semibold">Amount ({currency})</label>
          <input
            type="number"
            className="w-full border p-2 rounded-md mt-1"
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
            min="1"
          />
        </div>

        <button
          onClick={openPayment}
          className="bg-emerald-600 text-white px-4 py-2 rounded-md hover:bg-emerald-700 w-full text-center font-semibold"
        >
          Pay with Razorpay
        </button>

        <div className="text-xs text-slate-400 mt-4">
          *You will be redirected to a secure Razorpay.me checkout page.
        </div>

      </div>
    </div>
  );
}
