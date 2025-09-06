#!/bin/bash

# Deploy Smart Risk Detector Agent
# Advanced AI agent for financial risk and opportunity analysis

set -e

echo "🎯 Deploying Smart Risk Detector Agent"
echo "====================================="

# Check prerequisites
if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl not found. Please install kubectl first."
    exit 1
fi

if ! kubectl cluster-info &> /dev/null; then
    echo "❌ Cannot connect to Kubernetes cluster. Please check your kubeconfig."
    exit 1
fi

echo "✅ Kubernetes cluster accessible"

# Deploy MCP server
echo -e "\n📦 Deploying Smart Risk Detector MCP Server..."
kubectl apply -f smart-risk-detector-mcp.yaml

# Wait for MCP server to be ready
echo "⏳ Waiting for MCP server to be ready..."
kubectl wait --for=condition=Ready mcpserver/smart-risk-detector --timeout=120s

# Deploy tools
echo -e "\n🔧 Deploying Risk Detection Tools..."
kubectl apply -f smart-risk-detector-tools.yaml

# Wait for tools to be ready
echo "⏳ Waiting for tools to be ready..."
kubectl wait --for=condition=Ready tool/compute-metric-updates-tool --timeout=60s
kubectl wait --for=condition=Ready tool/detect-risks-opportunities-tool --timeout=60s
kubectl wait --for=condition=Ready tool/smart-risk-analysis-tool --timeout=60s

# Deploy agent
echo -e "\n🤖 Deploying Smart Risk Detector Agent..."
kubectl apply -f smart-risk-detector-agent.yaml

# Deploy sample queries
echo -e "\n📝 Deploying Sample Queries..."
kubectl apply -f ../queries/smart-risk-detector-queries.yaml

echo -e "\n✅ Smart Risk Detector Deployment Complete!"
echo "============================================="

echo -e "\n📋 Resources Created:"
echo "   - MCP Server: smart-risk-detector"
echo "   - Tools: compute-metric-updates-tool, detect-risks-opportunities-tool, smart-risk-analysis-tool"
echo "   - Agent: smart-risk-detector-agent"
echo "   - Queries: smart-risk-analysis-query, high-risk-scenario-query, opportunity-focused-query"

echo -e "\n🔍 Check Status:"
echo "   kubectl get mcpserver,tool,agent,query | grep smart-risk"

echo -e "\n🧪 Test the Agent:"
echo "   # Basic risk analysis"
echo "   fark agent smart-risk-detector-agent 'Analyze risks for inflation 4.5%, interest rate 5.2%, exchange rate 1.15'"
echo ""
echo "   # Comprehensive analysis"
echo "   fark agent smart-risk-detector-agent 'Perform smart risk analysis for TechCorp with inflation 3.2%, rates 4.5%, FX 1.15'"
echo ""
echo "   # Test specific tools"
echo "   fark tool smart-risk-analysis-tool --parameters '{\"data\": {\"summaries\": [\"Market shows strong growth\"], \"metrics\": {\"inflation\": 3.2, \"exchange_rate\": 1.15, \"interest_rate\": 4.5}, \"firm\": \"TechCorp\"}}'"

echo -e "\n📊 Monitor Query Execution:"
echo "   kubectl logs -l app=ark-controller -f"

echo -e "\n📚 Example Use Cases:"
echo "   1. Financial Risk Assessment"
echo "   2. Market Opportunity Analysis"
echo "   3. Strategic Planning Support"
echo "   4. Investment Decision Making"
echo "   5. Crisis Management Planning"

echo -e "\n🎉 Smart Risk Detector is ready for advanced financial analysis!"
