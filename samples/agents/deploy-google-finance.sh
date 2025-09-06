#!/bin/bash

# Deploy Google Finance Agent with SerpAPI integration
# This script deploys all necessary resources for the Google Finance trends agent

set -e

echo "🚀 Deploying Google Finance Agent with SerpAPI integration..."

# Check if SerpAPI secret exists
if ! kubectl get secret serpapi-secret >/dev/null 2>&1; then
    echo "❌ SerpAPI secret not found. Please create it first:"
    echo "   1. Edit samples/agents/serpapi-secret.yaml"
    echo "   2. Replace YOUR_SERPAPI_KEY_HERE with your actual SerpAPI key"
    echo "   3. Run: kubectl apply -f samples/agents/serpapi-secret.yaml"
    echo ""
    echo "   Get your SerpAPI key from: https://serpapi.com/"
    exit 1
fi

echo "✅ SerpAPI secret found"

# Deploy the tool
echo "📊 Deploying Google Finance tool..."
kubectl apply -f samples/agents/google-finance-tool.yaml

# Wait for tool to be ready
echo "⏳ Waiting for tool to be ready..."
kubectl wait --for=condition=Ready tool/google-finance-trends --timeout=60s

# Deploy the agent
echo "🤖 Deploying Google Finance agent..."
kubectl apply -f samples/agents/google-finance-agent.yaml

# Deploy the sample query
echo "📝 Deploying sample query..."
kubectl apply -f samples/queries/google-finance-query.yaml

echo ""
echo "✅ Google Finance Agent deployment complete!"
echo ""
echo "📋 Resources created:"
echo "   - Tool: google-finance-trends"
echo "   - Agent: google-finance-agent"
echo "   - Query: google-finance-trends-query"
echo ""
echo "🔍 Check status:"
echo "   kubectl get tool,agent,query | grep google-finance"
echo ""
echo "🧪 Test the agent:"
echo "   kubectl get query google-finance-trends-query -o yaml"
echo ""
echo "📊 Monitor query execution:"
echo "   kubectl logs -l app=ark-controller -f"
