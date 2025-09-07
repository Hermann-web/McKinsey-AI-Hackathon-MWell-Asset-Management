import streamlit as st
import requests
import json
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import time
from datetime import datetime
import asyncio
from typing import Dict, Any, List

# Page config
st.set_page_config(
    page_title="ARK Agentic Risk Analysis",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem 0;
        margin: -1rem -1rem 2rem -1rem;
        border-radius: 10px;
        text-align: center;
        color: white;
    }
    
    .agent-card {
        background: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: transform 0.2s ease;
    }
    
    .agent-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    
    .metric-card {
        background: white;
        border: 1px solid #e9ecef;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    .status-running {
        color: #fd7e14;
        font-weight: bold;
    }
    
    .status-complete {
        color: #28a745;
        font-weight: bold;
    }
    
    .status-error {
        color: #dc3545;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'base_url' not in st.session_state:
    st.session_state.base_url = "http://localhost:8080"
if 'query_history' not in st.session_state:
    st.session_state.query_history = []

class AgentClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
    
    def query_agent(self, agent_name: str, input_text: str) -> Dict[str, Any]:
        """Send a query to an ARK agent"""
        url = f"{self.base_url}/agent/{agent_name}"
        payload = {"input": input_text}
        
        try:
            response = requests.post(
                url,
                headers={"Content-Type": "application/json"},
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                # Parse the streaming response
                lines = response.text.strip().split('\n')
                result = None
                
                for line in lines:
                    if line.startswith('data: '):
                        try:
                            data = json.loads(line[6:])
                            if data.get('phase') == 'done':
                                result = data
                                break
                        except json.JSONDecodeError:
                            continue
                
                return result if result else {"error": "No valid response received"}
            else:
                return {"error": f"HTTP {response.status_code}: {response.text}"}
                
        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}
    
    def parse_agent_response(self, response_data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse the agent response for display"""
        if 'error' in response_data:
            return {"status": "error", "message": response_data['error']}
        
        query_info = response_data.get('query', {})
        status = query_info.get('status', {})
        
        result = {
            "status": status.get('phase', 'unknown'),
            "token_usage": status.get('tokenUsage', {}),
            "responses": []
        }
        
        if 'responses' in status:
            for resp in status['responses']:
                content = resp.get('content', '')
                try:
                    # Try to parse as JSON
                    parsed_content = json.loads(content)
                    result["responses"].append(parsed_content)
                except json.JSONDecodeError:
                    # If not JSON, keep as string
                    result["responses"].append({"content": content})
        
        return result

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🤖 ARK Agentic Risk Analysis Platform</h1>
        <p>Kubernetes-native AI agents for quantitative financial risk assessment</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        base_url = st.text_input(
            "ARK Base URL",
            value=st.session_state.base_url,
            help="Base URL for your ARK deployment (e.g., https://your-ngrok-url or http://localhost:8080)"
        )
        st.session_state.base_url = base_url
        
        st.divider()
        
        st.header("🤖 Available Agents")
        agent_info = {
            "app-orchestrator-agent": "🎯 Main orchestrator for multi-agent workflows",
            "smart-risk-detector-agent": "🔍 Advanced risk analysis and detection",
            "google-finance-agent": "📈 Market trends and financial data",
            "economic-evaluator-agent": "💹 Economic indicators evaluation"
        }
        
        for agent, description in agent_info.items():
            st.markdown(f"**{agent}**")
            st.caption(description)
            st.divider()
    
    # Main content
    client = AgentClient(st.session_state.base_url)
    
    # Tabs for different functionalities
    tab1, tab2, tab3, tab4 = st.tabs(["🚀 Quick Demo", "🔧 Custom Query", "📊 Risk Dashboard", "📈 Query History"])
    
    with tab1:
        st.header("Quick Demo Scenarios")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="agent-card">
                <h3>🎯 App Orchestrator</h3>
                <p>Test the main orchestration agent with a comprehensive risk analysis request.</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Run Orchestrator Demo", key="orchestrator_demo"):
                with st.spinner("Running orchestrator demo..."):
                    result = client.query_agent(
                        "app-orchestrator-agent",
                        "Perform comprehensive risk analysis for Morocco market including economic indicators and trends"
                    )
                    
                    parsed_result = client.parse_agent_response(result)
                    
                    if parsed_result["status"] == "error":
                        st.error(f"Error: {parsed_result['message']}")
                    else:
                        st.success("✅ Orchestrator analysis complete!")
                        
                        # Display token usage
                        if parsed_result.get("token_usage"):
                            usage = parsed_result["token_usage"]
                            col_a, col_b, col_c = st.columns(3)
                            with col_a:
                                st.metric("Prompt Tokens", usage.get("promptTokens", 0))
                            with col_b:
                                st.metric("Completion Tokens", usage.get("completionTokens", 0))
                            with col_c:
                                st.metric("Total Tokens", usage.get("totalTokens", 0))
                        
                        # Display responses
                        for i, response in enumerate(parsed_result.get("responses", [])):
                            st.subheader(f"Response {i+1}")
                            if isinstance(response, dict):
                                st.json(response)
                            else:
                                st.write(response)
        
        with col2:
            st.markdown("""
            <div class="agent-card">
                <h3>📈 Market Trends Analysis</h3>
                <p>Get real-time market trends and financial insights for specific regions.</p>
            </div>
            """, unsafe_allow_html=True)
            
            region = st.selectbox("Select Region", ["Morocco", "USA", "Europe", "Global"], key="region_demo")
            
            if st.button("Analyze Market Trends", key="market_demo"):
                with st.spinner(f"Analyzing market trends for {region}..."):
                    result = client.query_agent(
                        "google-finance-agent",
                        f"what are the current market trends in {region}"
                    )
                    
                    parsed_result = client.parse_agent_response(result)
                    
                    if parsed_result["status"] == "error":
                        st.error(f"Error: {parsed_result['message']}")
                    else:
                        st.success(f"✅ Market analysis for {region} complete!")
                        
                        for response in parsed_result.get("responses", []):
                            if isinstance(response, dict):
                                # Display insights if available
                                if "insights" in response:
                                    st.subheader("Market Insights")
                                    for insight in response["insights"]:
                                        with st.expander(f"📊 {insight.get('url', 'Insight')}"):
                                            st.write(insight.get('summary', ''))
                                
                                if "reporting" in response:
                                    st.subheader("Market Report")
                                    st.write(response["reporting"])
                            else:
                                st.write(response)
    
    with tab2:
        st.header("Custom Agent Query")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            selected_agent = st.selectbox(
                "Select Agent",
                ["app-orchestrator-agent", "smart-risk-detector-agent", "google-finance-agent", "economic-evaluator-agent"],
                key="custom_agent"
            )
            
            # Predefined examples based on agent
            examples = {
                "app-orchestrator-agent": [
                    "Comprehensive risk analysis for tech portfolio",
                    "Evaluate market conditions for emerging markets"
                ],
                "smart-risk-detector-agent": [
                    "Analyze risks: inflation 3.2%, interest rate 4.5%, exchange rate 1.15",
                    "Risk assessment for portfolio with high volatility stocks"
                ],
                "google-finance-agent": [
                    "what are the trends in morocco",
                    "latest market performance for technology sector"
                ],
                "economic-evaluator-agent": [
                    "evaluate new values of inflation (0.5 update 10%), exchange rate (0.6 update 20%)",
                    "assess economic indicators for Q4 2024"
                ]
            }
            
            st.subheader("Example Queries")
            for example in examples.get(selected_agent, []):
                if st.button(f"📝 {example[:40]}...", key=f"example_{hash(example)}"):
                    st.session_state.custom_query = example
        
        with col2:
            custom_query = st.text_area(
                "Enter your query",
                height=150,
                value=st.session_state.get('custom_query', ''),
                placeholder=f"Enter your query for {selected_agent}..."
            )
            
            if st.button("🚀 Execute Query", type="primary"):
                if custom_query:
                    with st.spinner(f"Executing query on {selected_agent}..."):
                        start_time = time.time()
                        result = client.query_agent(selected_agent, custom_query)
                        execution_time = time.time() - start_time
                        
                        # Store in history
                        st.session_state.query_history.append({
                            "timestamp": datetime.now(),
                            "agent": selected_agent,
                            "query": custom_query,
                            "result": result,
                            "execution_time": execution_time
                        })
                        
                        parsed_result = client.parse_agent_response(result)
                        
                        if parsed_result["status"] == "error":
                            st.error(f"❌ Error: {parsed_result['message']}")
                        else:
                            st.success(f"✅ Query executed successfully in {execution_time:.2f}s")
                            
                            # Display metrics
                            if parsed_result.get("token_usage"):
                                usage = parsed_result["token_usage"]
                                col_a, col_b, col_c = st.columns(3)
                                with col_a:
                                    st.metric("Prompt Tokens", usage.get("promptTokens", 0))
                                with col_b:
                                    st.metric("Completion Tokens", usage.get("completionTokens", 0))
                                with col_c:
                                    st.metric("Total Tokens", usage.get("totalTokens", 0))
                            
                            # Display results
                            st.subheader("Results")
                            for response in parsed_result.get("responses", []):
                                if isinstance(response, dict):
                                    if response.get("content"):
                                        st.write(response["content"])
                                    else:
                                        st.json(response)
                                else:
                                    st.write(response)
                else:
                    st.warning("Please enter a query")
    
    with tab3:
        st.header("Risk Dashboard")
        
        # Sample risk analysis
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h3>Inflation Risk</h3>
                <h2 style="color: #fd7e14;">3.2%</h2>
                <p>Moderate</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card">
                <h3>Interest Rate</h3>
                <h2 style="color: #dc3545;">4.5%</h2>
                <p>High</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="metric-card">
                <h3>Exchange Rate</h3>
                <h2 style="color: #28a745;">1.15</h2>
                <p>Stable</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div class="metric-card">
                <h3>Overall Risk</h3>
                <h2 style="color: #fd7e14;">Medium</h2>
                <p>Monitor</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Risk visualization
        st.subheader("Risk Trends")
        
        # Sample data for visualization
        dates = pd.date_range(start='2024-01-01', end='2024-12-01', freq='M')[:10]
        risk_data = {
            'Date': dates,
            'Inflation_Risk': [2.1, 2.3, 2.8, 3.0, 3.2, 3.1, 2.9, 3.2, 3.4, 3.1, 2.8, 3.0][:10],
            'Interest_Rate_Risk': [4.0, 4.1, 4.3, 4.2, 4.5, 4.4, 4.6, 4.5, 4.3, 4.4, 4.2, 4.5][:10],
            'Exchange_Rate_Risk': [1.10, 1.12, 1.15, 1.14, 1.15, 1.16, 1.14, 1.15, 1.13, 1.15, 1.16, 1.14][:10]
        }
        
        df = pd.DataFrame(risk_data)
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Inflation Risk Trend', 'Interest Rate Risk', 'Exchange Rate Stability', 'Risk Correlation'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"type": "scatter"}]]
        )
        
        # Inflation trend
        fig.add_trace(
            go.Scatter(x=df['Date'], y=df['Inflation_Risk'], name='Inflation Risk', line=dict(color='#fd7e14')),
            row=1, col=1
        )
        
        # Interest rate trend
        fig.add_trace(
            go.Scatter(x=df['Date'], y=df['Interest_Rate_Risk'], name='Interest Rate Risk', line=dict(color='#dc3545')),
            row=1, col=2
        )
        
        # Exchange rate stability
        fig.add_trace(
            go.Scatter(x=df['Date'], y=df['Exchange_Rate_Risk'], name='Exchange Rate', line=dict(color='#28a745')),
            row=2, col=1
        )
        
        # Risk correlation scatter
        fig.add_trace(
            go.Scatter(x=df['Inflation_Risk'], y=df['Interest_Rate_Risk'], 
                      mode='markers', name='Risk Correlation',
                      marker=dict(color='#667eea', size=8)),
            row=2, col=2
        )
        
        fig.update_layout(height=600, showlegend=False, title_text="Risk Analysis Dashboard")
        st.plotly_chart(fig, use_container_width=True)
        
        # Real-time risk analysis
        st.subheader("Real-time Risk Analysis")
        
        if st.button("🔍 Run Smart Risk Analysis", key="risk_analysis"):
            with st.spinner("Running comprehensive risk analysis..."):
                result = client.query_agent(
                    "smart-risk-detector-agent",
                    "Analyze current market risks including inflation 3.2%, interest rate 4.5%, exchange rate 1.15 for Morocco market"
                )
                
                parsed_result = client.parse_agent_response(result)
                
                if parsed_result["status"] == "error":
                    st.error(f"Error: {parsed_result['message']}")
                else:
                    st.success("✅ Risk analysis complete!")
                    for response in parsed_result.get("responses", []):
                        if isinstance(response, dict):
                            st.json(response)
                        else:
                            st.write(response)
    
    with tab4:
        st.header("Query History")
        
        if st.session_state.query_history:
            # Summary metrics
            col1, col2, col3, col4 = st.columns(4)
            
            total_queries = len(st.session_state.query_history)
            avg_time = sum(q['execution_time'] for q in st.session_state.query_history) / total_queries
            successful_queries = sum(1 for q in st.session_state.query_history if 'error' not in q['result'])
            success_rate = (successful_queries / total_queries) * 100
            
            with col1:
                st.metric("Total Queries", total_queries)
            with col2:
                st.metric("Avg Response Time", f"{avg_time:.2f}s")
            with col3:
                st.metric("Success Rate", f"{success_rate:.1f}%")
            with col4:
                st.metric("Active Agents", len(set(q['agent'] for q in st.session_state.query_history)))
            
            # Query history table
            st.subheader("Recent Queries")
            
            for i, query in enumerate(reversed(st.session_state.query_history[-10:])):
                with st.expander(f"🔍 Query {total_queries - i}: {query['query'][:50]}... ({query['timestamp'].strftime('%H:%M:%S')})"):
                    col_a, col_b = st.columns([1, 3])
                    
                    with col_a:
                        st.write(f"**Agent:** {query['agent']}")
                        st.write(f"**Time:** {query['execution_time']:.2f}s")
                        st.write(f"**Status:** {'✅ Success' if 'error' not in query['result'] else '❌ Error'}")
                    
                    with col_b:
                        st.write("**Query:**")
                        st.code(query['query'])
                        
                        st.write("**Result:**")
                        parsed_result = client.parse_agent_response(query['result'])
                        if parsed_result["status"] == "error":
                            st.error(parsed_result['message'])
                        else:
                            for response in parsed_result.get("responses", []):
                                if isinstance(response, dict):
                                    st.json(response)
                                else:
                                    st.write(response)
            
            if st.button("🗑️ Clear History"):
                st.session_state.query_history = []
                st.rerun()
        else:
            st.info("No queries executed yet. Try running some queries in the other tabs!")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666;">
        <p>🤖 ARK Agentic Risk Analysis Platform | Built with Streamlit & ARK Framework</p>
        <p>For more information, visit the <a href="https://github.com/Hermann-web/McKinsey-AI-Hackathon-MWell-Asset-Management" target="_blank">GitHub Repository</a></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()