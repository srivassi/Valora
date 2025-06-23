import requests

print("🔄 Sending request to FastAPI...")

try:
    response = requests.post("http://127.0.0.1:8000/chat", json={
        "prompt_type": "stock_trend",  # Try "ratios", "anomaly", or "enhanced_hypothesis"
        "company_name": "Apple"
    })

    print("✅ Response received!")
    print("Status code:", response.status_code)
    print("Response JSON:", response.json())

except Exception as e:
    print("❌ Error while sending request:", e)

