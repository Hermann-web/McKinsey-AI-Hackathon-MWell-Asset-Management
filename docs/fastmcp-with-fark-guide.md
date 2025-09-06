# Using FastMCP with Fark

This guide shows you how to create FastMCP servers and integrate them with Fark for querying agents and tools.

## Overview

FastMCP + Fark workflow:
1. **FastMCP Server**: Create a Python server with `@mcp.tool` decorated functions
2. **Kubernetes Resources**: Deploy the server with Deployment, Service, and MCPServer resources
3. **Tool Resources**: Create Tool resources that reference the MCP server
4. **Agent Integration**: Reference tools in Agent resources
5. **Fark Queries**: Use Fark CLI or HTTP API to query agents

## Quick Start

### 1. Create a FastMCP Server

Create a Python file with your tools:

```python
# src/main.py
from typing import Annotated
from fastmcp import FastMCP

mcp = FastMCP("My Tools 🚀")

@mcp.tool
def add(
    a: Annotated[int, "First number to add"], 
    b: Annotated[int, "Second number to add"]
) -> int:
    """Add two integers and return the sum"""
    return a + b

@mcp.tool
def analyze_text(
    text: Annotated[str, "Text to analyze"]
) -> dict:
    """Analyze text and return word count and sentiment"""
    words = text.split()
    return {
        "word_count": len(words),
        "char_count": len(text),
        "sentiment": "positive" if "good" in text.lower() else "neutral"
    }

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000, path="/")
```

### 2. Deploy MCP Server

Create Kubernetes resources:

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-tools
spec:
  replicas: 1
  selector:
    matchLabels:
      app: my-tools
  template:
    metadata:
      labels:
        app: my-tools
    spec:
      containers:
      - name: my-tools
        image: my-tools:latest
        ports:
        - containerPort: 8000
---
apiVersion: v1
kind: Service
metadata:
  name: my-tools
spec:
  ports:
  - port: 8000
    targetPort: 8000
  selector:
    app: my-tools
---
apiVersion: ark.mckinsey.com/v1alpha1
kind: MCPServer
metadata:
  name: my-tools
spec:
  address:
    valueFrom:
      serviceRef:
        name: my-tools
  transport: http
  timeout: 30s
  description: "My custom tools MCP server"
```

### 3. Create Tool Resources

Create Tool resources for each MCP function:

```yaml
# tools.yaml
apiVersion: ark.mckinsey.com/v1alpha1
kind: Tool
metadata:
  name: add-tool
spec:
  type: mcp
  description: "Add two numbers"
  mcp:
    mcpServerRef:
      name: my-tools
      namespace: default
    toolName: add
---
apiVersion: ark.mckinsey.com/v1alpha1
kind: Tool
metadata:
  name: analyze-text-tool
spec:
  type: mcp
  description: "Analyze text content"
  mcp:
    mcpServerRef:
      name: my-tools
      namespace: default
    toolName: analyze_text
```

### 4. Create Agent

```yaml
# agent.yaml
apiVersion: ark.mckinsey.com/v1alpha1
kind: Agent
metadata:
  name: math-agent
spec:
  prompt: |
    You are a helpful math assistant. You can add numbers and analyze text.
    Use the available tools to help users with calculations and text analysis.
  tools:
    - type: custom
      name: add-tool
    - type: custom
      name: analyze-text-tool
```

### 5. Deploy Everything

```bash
# Deploy the MCP server
kubectl apply -f deployment.yaml

# Wait for server to be ready
kubectl wait --for=condition=Ready mcpserver/my-tools --timeout=60s

# Deploy the tools
kubectl apply -f tools.yaml

# Deploy the agent
kubectl apply -f agent.yaml
```

### 6. Query with Fark

#### CLI Usage

```bash
# Query the agent
./fark agent math-agent "Add 5 and 3, then analyze the text 'This is good news'"

# Query a specific tool directly
./fark tool add-tool --parameters a=10,b=20

# JSON output
./fark agent math-agent "What is 15 + 25?" --output json --quiet
```

#### HTTP API Usage

```bash
# Start Fark server
./fark server

# Query agent via HTTP
curl -X POST http://localhost:8080/agent/math-agent \
  -H "Content-Type: application/json" \
  -d '{"input": "Add 7 and 9, then analyze the text"}'

# Query tool directly
curl -X POST http://localhost:8080/tool/add-tool \
  -H "Content-Type: application/json" \
  -d '{"input": "{\"a\": 15, \"b\": 25}"}'
```

## Advanced Examples

### Financial Analysis Tool

```python
# financial_tools.py
from typing import Annotated, List
from fastmcp import FastMCP
import requests

mcp = FastMCP("Financial Tools 💰")

@mcp.tool
def get_stock_price(
    symbol: Annotated[str, "Stock symbol (e.g., AAPL, GOOGL)"]
) -> dict:
    """Get current stock price for a symbol"""
    # Mock implementation - replace with real API
    return {
        "symbol": symbol,
        "price": 150.25,
        "change": 2.15,
        "change_percent": 1.45
    }

@mcp.tool
def analyze_portfolio(
    symbols: Annotated[List[str], "List of stock symbols"]
) -> dict:
    """Analyze a portfolio of stocks"""
    total_value = 0
    for symbol in symbols:
        # Mock calculation
        total_value += 150.25
    
    return {
        "symbols": symbols,
        "total_value": total_value,
        "count": len(symbols),
        "average_value": total_value / len(symbols) if symbols else 0
    }
```

### Data Processing Tool

```python
# data_tools.py
from typing import Annotated, List, Dict, Any
from fastmcp import FastMCP
import json

mcp = FastMCP("Data Tools 📊")

@mcp.tool
def process_csv_data(
    csv_content: Annotated[str, "CSV content as string"],
    operation: Annotated[str, "Operation: sum, average, count, max, min"]
) -> dict:
    """Process CSV data with various operations"""
    lines = csv_content.strip().split('\n')
    if not lines:
        return {"error": "Empty CSV content"}
    
    # Simple CSV parsing (use pandas for production)
    headers = lines[0].split(',')
    data = []
    
    for line in lines[1:]:
        values = line.split(',')
        data.append([float(v) if v.replace('.', '').isdigit() else v for v in values])
    
    if operation == "count":
        return {"count": len(data)}
    elif operation == "sum" and data:
        numeric_cols = [i for i, col in enumerate(headers) if isinstance(data[0][i], (int, float))]
        sums = [sum(row[i] for row in data) for i in numeric_cols]
        return {"sums": dict(zip([headers[i] for i in numeric_cols], sums))}
    
    return {"message": f"Operation {operation} completed", "rows": len(data)}

@mcp.tool
def filter_data(
    data: Annotated[List[Dict[str, Any]], "List of data objects"],
    filter_key: Annotated[str, "Key to filter on"],
    filter_value: Annotated[str, "Value to match"]
) -> List[Dict[str, Any]]:
    """Filter data based on key-value criteria"""
    return [item for item in data if item.get(filter_key) == filter_value]
```

## Testing Your MCP Server

### Local Testing

```python
# test_mcp.py
import requests

# Test the MCP server directly
response = requests.post("http://localhost:8000/tools/add", 
                        json={"a": 5, "b": 3})
print(response.json())  # {"result": 8}

response = requests.post("http://localhost:8000/tools/analyze_text",
                        json={"text": "This is good news"})
print(response.json())  # {"result": {"word_count": 4, "char_count": 17, "sentiment": "positive"}}
```

### Kubernetes Testing

```bash
# Port forward to test locally
kubectl port-forward service/my-tools 8000:8000

# Test the tools
curl -X POST http://localhost:8000/tools/add \
  -H "Content-Type: application/json" \
  -d '{"a": 10, "b": 20}'
```

## Best Practices

### 1. Error Handling

```python
@mcp.tool
def safe_divide(
    a: Annotated[float, "Numerator"],
    b: Annotated[float, "Denominator"]
) -> dict:
    """Safely divide two numbers"""
    try:
        if b == 0:
            return {"error": "Division by zero", "result": None}
        return {"result": a / b, "error": None}
    except Exception as e:
        return {"error": str(e), "result": None}
```

### 2. Input Validation

```python
from pydantic import BaseModel, validator

class StockQuery(BaseModel):
    symbol: str
    timeframe: str = "1d"
    
    @validator('symbol')
    def symbol_must_be_uppercase(cls, v):
        return v.upper()
    
    @validator('timeframe')
    def timeframe_must_be_valid(cls, v):
        valid_timeframes = ['1d', '5d', '1mo', '3mo', '6mo', '1y']
        if v not in valid_timeframes:
            raise ValueError(f'Timeframe must be one of {valid_timeframes}')
        return v

@mcp.tool
def get_stock_data(query: Annotated[StockQuery, "Stock query parameters"]) -> dict:
    """Get stock data with validation"""
    # Implementation here
    pass
```

### 3. Resource Management

```python
import asyncio
from contextlib import asynccontextmanager

# Use async for I/O operations
@mcp.tool
async def fetch_data_async(
    url: Annotated[str, "URL to fetch data from"]
) -> dict:
    """Fetch data asynchronously"""
    import aiohttp
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()
```

## Troubleshooting

### Common Issues

1. **MCP Server Not Ready**
   ```bash
   kubectl describe mcpserver my-tools
   kubectl logs -l app=my-tools
   ```

2. **Tool Not Found**
   ```bash
   kubectl describe tool add-tool
   kubectl get mcpserver my-tools -o yaml
   ```

3. **Agent Query Fails**
   ```bash
   kubectl describe agent math-agent
   kubectl logs -l app=ark-controller
   ```

### Debugging Tips

- Use `kubectl logs` to check server logs
- Test MCP server directly with curl
- Verify tool names match exactly
- Check network connectivity between components

## Next Steps

- Explore the [ARK MCP Server examples](../../services/ark-mcp/)
- Learn about [Tool resource configuration](../../docs/content/reference/resources/tools.mdx)
- Check out [Agent configuration options](../../docs/content/reference/resources/agents.mdx)
- See [Fark CLI documentation](../../tools/fark/docs/)
