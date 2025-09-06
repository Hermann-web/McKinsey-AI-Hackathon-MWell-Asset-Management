#!/usr/bin/env python3
"""
Test script for the MCP server
Run this after port-forwarding the service: kubectl port-forward service/math-tools 8000:8000
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_tool(tool_name, input_data):
    """Test a specific tool"""
    url = f"{BASE_URL}/tools/{tool_name}"
    response = requests.post(url, json=input_data)
    
    print(f"\n🔧 Testing {tool_name}")
    print(f"Input: {input_data}")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    return response.json()

def main():
    print("🧪 Testing MCP Server Tools")
    print("=" * 50)
    
    # Test add tool
    test_tool("add", {"a": 15, "b": 25})
    
    # Test multiply tool
    test_tool("multiply", {"a": 40, "b": 3})
    
    # Test analyze_text tool
    test_tool("analyze_text", {"text": "This is amazing news about our project success"})
    
    # Test calculate_statistics tool
    test_tool("calculate_statistics", {"numbers": [10, 20, 30, 40, 50]})
    
    print("\n✅ All tests completed!")

if __name__ == "__main__":
    main()
