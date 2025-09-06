# FastMCP + Fark Example

This example demonstrates how to use FastMCP with Fark to create and query agents with custom tools.

## What This Example Shows

1. **FastMCP Server**: A Python server with mathematical and text analysis tools
2. **Kubernetes Deployment**: Complete K8s resources for the MCP server
3. **Tool Resources**: ARK Tool resources that connect to the MCP server
4. **Agent Integration**: An agent that uses the custom tools
5. **Fark Queries**: How to query the agent using Fark CLI and HTTP API

## Quick Start

### 1. Deploy the MCP Server

```bash
# Deploy the MCP server and related resources
kubectl apply -f mcp-server.yaml

# Wait for the server to be ready
kubectl wait --for=condition=Ready mcpserver/math-tools --timeout=60s
```

### 2. Deploy the Tools

```bash
# Deploy the tool resources
kubectl apply -f tools.yaml

# Verify tools are ready
kubectl get tools
```

### 3. Deploy the Agent

```bash
# Deploy the agent
kubectl apply -f agent.yaml

# Verify agent is ready
kubectl get agents
```

### 4. Query with Fark

#### Using Fark CLI

```bash
# Basic math query
./fark agent math-agent "Add 15 and 25, then multiply the result by 2"

# Text analysis
./fark agent math-agent "Analyze the text 'The quick brown fox jumps over the lazy dog'"

# Combined operations
./fark agent math-agent "Add 10 and 5, then analyze the text 'This is amazing news'"

# JSON output
./fark agent math-agent "What is 7 * 8?" --output json --quiet
```

#### Using Fark HTTP API

```bash
# Start Fark server
./fark server &

# Query via HTTP
curl -X POST http://localhost:8080/agent/math-agent \
  -H "Content-Type: application/json" \
  -d '{"input": "Calculate 12 + 18 and analyze the text"}'

# Query specific tool
curl -X POST http://localhost:8080/tool/add-tool \
  -H "Content-Type: application/json" \
  -d '{"input": "{\"a\": 20, \"b\": 30}"}'
```

## Files in This Example

- `mcp-server.yaml` - Kubernetes resources for the MCP server
- `tools.yaml` - ARK Tool resources
- `agent.yaml` - Agent that uses the tools
- `query.yaml` - Sample query
- `test-mcp.py` - Script to test MCP server directly
- `test-fark.sh` - Script to test Fark integration

## Testing the MCP Server Directly

```bash
# Port forward to access the server
kubectl port-forward service/math-tools 8000:8000

# Test in another terminal
python test-mcp.py
```

## Expected Output

When you run the queries, you should see:

1. **Math operations**: Correct calculations
2. **Text analysis**: Word counts, character counts, and sentiment analysis
3. **Combined operations**: Both math and text analysis in sequence
4. **Tool calls**: Fark will show which tools are being called

## Troubleshooting

### Check MCP Server Status
```bash
kubectl get mcpserver math-tools -o yaml
kubectl logs -l app=math-tools
```

### Check Tool Status
```bash
kubectl get tools
kubectl describe tool add-tool
```

### Check Agent Status
```bash
kubectl get agents
kubectl describe agent math-agent
```

### Check Query Execution
```bash
kubectl get queries
kubectl logs -l app=ark-controller
```

## Customization

### Adding New Tools

1. Add new functions to the MCP server
2. Create corresponding Tool resources
3. Update the agent to reference new tools
4. Test with Fark

### Modifying Existing Tools

1. Update the Python functions
2. Rebuild and redeploy the MCP server
3. Test with Fark

### Adding Parameters

1. Update function signatures with `Annotated` types
2. Update Tool input schemas if needed
3. Test parameter passing with Fark
