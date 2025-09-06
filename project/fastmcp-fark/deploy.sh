#!/bin/bash

# Deploy FastMCP + Fark example
# This script deploys all necessary resources for the example

set -e

echo "🚀 Deploying FastMCP + Fark Example"
echo "===================================="

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl not found. Please install kubectl first."
    exit 1
fi

# Check if cluster is accessible
if ! kubectl cluster-info &> /dev/null; then
    echo "❌ Cannot connect to Kubernetes cluster. Please check your kubeconfig."
    exit 1
fi

echo "✅ Kubernetes cluster accessible"

# Deploy MCP server
echo -e "\n📦 Deploying MCP Server..."
kubectl apply -f mcp-server.yaml

# Wait for MCP server to be ready
echo "⏳ Waiting for MCP server to be ready..."
kubectl wait --for=condition=Ready mcpserver/math-tools --timeout=120s

# Deploy tools
echo -e "\n🔧 Deploying Tools..."
kubectl apply -f tools.yaml

# Wait for tools to be ready
echo "⏳ Waiting for tools to be ready..."
kubectl wait --for=condition=Ready tool/add-tool --timeout=60s
kubectl wait --for=condition=Ready tool/multiply-tool --timeout=60s
kubectl wait --for=condition=Ready tool/analyze-text-tool --timeout=60s
kubectl wait --for=condition=Ready tool/calculate-statistics-tool --timeout=60s

# Deploy agent
echo -e "\n🤖 Deploying Agent..."
kubectl apply -f agent.yaml

# Deploy sample query
echo -e "\n📝 Deploying Sample Query..."
kubectl apply -f query.yaml

echo -e "\n✅ Deployment Complete!"
echo "========================"

echo -e "\n📋 Resources Created:"
echo "   - MCP Server: math-tools"
echo "   - Tools: add-tool, multiply-tool, analyze-text-tool, calculate-statistics-tool"
echo "   - Agent: math-agent"
echo "   - Query: math-analysis-query"

echo -e "\n🔍 Check Status:"
echo "   kubectl get mcpserver,tool,agent,query | grep math"

echo -e "\n🧪 Test the Setup:"
echo "   # Test MCP server directly (in another terminal):"
echo "   kubectl port-forward service/math-tools 8000:8000"
echo "   python test-mcp.py"
echo ""
echo "   # Test with Fark:"
echo "   ./test-fark.sh"
echo ""
echo "   # Or test individual queries:"
echo "   fark agent math-agent 'Add 10 and 20'"
echo "   fark agent math-agent 'Analyze the text: Hello world'"

echo -e "\n📊 Monitor Query Execution:"
echo "   kubectl logs -l app=ark-controller -f"

echo -e "\n🎉 Ready to use FastMCP with Fark!"
