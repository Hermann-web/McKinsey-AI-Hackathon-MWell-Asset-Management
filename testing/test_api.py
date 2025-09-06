import pytest
import requests
import json

BASE_URL = "https://11aa3fbb424c.ngrok-free.app/agent"

# Payloads for each agent
economic_payload = {
    "input": "evaluate new values of inflation (0.5 update 10%), exchange rate (0.6 update 20%)"
}

risk_payload = {
    "input": "Analyze risks: inflation 3.2%, interest rate 4.5%, exchange rate 1.15"
}

finance_payload = {
    "input": "what are the trends in morocco"
}

orchestrator_payload = {
    "input": "Aggregate all results"
}

# Helper function to call agent
def call_agent(agent_name, payload):
    url = f"{BASE_URL}/{agent_name}"
    response = requests.post(url, headers={"Content-Type": "application/json"}, data=json.dumps(payload))
    try:
        return response.json()
    except json.JSONDecodeError:
        return response.text

# =========================
# Pytest Test Cases
# =========================

def test_economic_evaluator_agent():
    result = call_agent("economic-evaluator-agent", economic_payload)
    assert "inflation" in result
    assert "exchange_rate" in result
    assert "interest_rate" in result
    print("\nEconomic Evaluator Result:", json.dumps(result, indent=2))

def test_smart_risk_detector_agent():
    result = call_agent("smart-risk-detector-agent", risk_payload)
    assert "inflation" in result
    assert "interest_rate" in result
    assert "exchange_rate" in result
    print("\nSmart Risk Detector Result:", json.dumps(result, indent=2))

def test_google_finance_agent():
    result = call_agent("smart-risk-detector-agent/agent/google-finance-agent", finance_payload)
    assert "region" in result or "trend_summary" in result
    print("\nGoogle Finance Result:", json.dumps(result, indent=2))

def test_app_orchestrator_agent():
    result = call_agent("app-orchestrator-agent", orchestrator_payload)
    # Check that combined structure exists
    assert "economic_update" in result
    assert "risk_analysis" in result
    assert "finance_trends" in result
    print("\nApp Orchestrator Result:", json.dumps(result, indent=2))

# To run the tests, use: pytest -s test_agents.py
