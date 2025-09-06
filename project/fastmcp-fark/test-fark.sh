#!/bin/bash

# Test script for Fark integration
# Make sure Fark is built and available in the PATH

set -e

echo "🚀 Testing Fark Integration with FastMCP"
echo "========================================"

# Check if fark is available
if ! command -v fark &> /dev/null; then
    echo "❌ Fark not found. Please build and install Fark first:"
    echo "   make fark-install"
    exit 1
fi

echo "✅ Fark found"

# Test 1: Basic math query
echo -e "\n🧮 Test 1: Basic Math Query"
echo "Query: Add 15 and 25, then multiply by 3"
fark agent math-agent "Add 15 and 25, then multiply by 3" --quiet

# Test 2: Text analysis
echo -e "\n📝 Test 2: Text Analysis"
echo "Query: Analyze the text 'This is amazing news'"
fark agent math-agent "Analyze the text 'This is amazing news'" --quiet

# Test 3: Statistics calculation
echo -e "\n📊 Test 3: Statistics Calculation"
echo "Query: Calculate statistics for [10, 20, 30, 40, 50]"
fark agent math-agent "Calculate statistics for the numbers 10, 20, 30, 40, 50" --quiet

# Test 4: Combined operations
echo -e "\n🔄 Test 4: Combined Operations"
echo "Query: Add 7 and 8, then analyze 'Great results'"
fark agent math-agent "Add 7 and 8, then analyze the text 'Great results'" --quiet

# Test 5: JSON output
echo -e "\n📋 Test 5: JSON Output"
echo "Query: What is 12 * 8?"
fark agent math-agent "What is 12 * 8?" --output json --quiet

# Test 6: Direct tool query
echo -e "\n🔧 Test 6: Direct Tool Query"
echo "Querying add-tool directly"
fark tool add-tool --parameters a=100,b=200 --quiet

echo -e "\n✅ All Fark tests completed!"
echo -e "\n💡 Try these additional queries:"
echo "   fark agent math-agent 'Calculate 5 + 3 * 2'"
echo "   fark agent math-agent 'Analyze the sentiment of this text: I love this product'"
echo "   fark agent math-agent 'Find statistics for [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]'"
