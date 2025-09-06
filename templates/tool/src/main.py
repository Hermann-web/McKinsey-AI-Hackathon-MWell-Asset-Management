from typing import Annotated, List, Optional, Dict, Any
from fastmcp import FastMCP
# import statistics
# from urllib.parse import urlparse

mcp = FastMCP("Demo 🚀")

# --------------------
# BASIC TOOLS
# --------------------

@mcp.tool
def add(
    a: Annotated[int, "First number to add"], 
    b: Annotated[int, "Second number to add"]
) -> int:
    """Add two integers and return the sum"""
    return a + b


@mcp.tool
def multiply(
    a: Annotated[float, "First number to multiply"],
    b: Annotated[float, "Second number to multiply"],
) -> float:
    """Multiply two numbers and return the product"""
    return a * b * 2


# @mcp.tool
# def word_count(text: Annotated[str, "Text to analyze for word count"]) -> Dict[str, int]:
#     """Count words, characters, and unique words in the given text"""
#     words = text.split()
#     return {
#         "word_count": len(words),
#         "char_count": len(text),
#         "unique_words": len(set(word.lower() for word in words)),
#     }


# # --------------------
# # FINANCIAL NEWS LOGIC
# # --------------------

# @mcp.tool
# def analyze_news() -> Dict[str, Any]:
#     """Simulates analyzing news sources and extracting economic indicators."""
#     sources: List[str] = [
#         "https://www.google.com/finance/",
#         "https://bloomberg.com/article",
#         "https://fed.gov/announcement",
#     ]

#     summaries: List[str] = []
#     inflation_signals: List[float] = []
#     exchange_signals: List[float] = []
#     interest_signals: List[float] = []

#     for source_url in sources:
#         domain = urlparse(source_url).netloc.lower()

#         if "bloomberg" in domain or "reuters" in domain:
#             summary = f"Financial markets report from {domain}: Mixed economic signals with focus on monetary policy"
#             inflation_signals.append(0.2)
#             exchange_signals.append(-0.1)
#             interest_signals.append(0.15)

#         elif "fed" in domain or "centralbank" in domain:
#             summary = f"Central bank communication from {domain}: Policy stance remains data-dependent"
#             inflation_signals.append(0.1)
#             exchange_signals.append(0.05)
#             interest_signals.append(0.25)

#         elif "wsj" in domain or "ft.com" in domain:
#             summary = f"Market analysis from {domain}: Corporate earnings and economic indicators show resilience"
#             inflation_signals.append(0.05)
#             exchange_signals.append(0.1)
#             interest_signals.append(0.0)

#         else:
#             summary = f"Economic news from {domain}: General market developments and policy discussions"
#             inflation_signals.append(0.0)
#             exchange_signals.append(0.0)
#             interest_signals.append(0.05)

#         summaries.append(summary)

#     return {
#         "summaries": summaries,
#         "inflation_pct": statistics.mean(inflation_signals) if inflation_signals else None,
#         "exchange_rate_pct": statistics.mean(exchange_signals) if exchange_signals else None,
#         "interest_rate_pct": statistics.mean(interest_signals) if interest_signals else None,
#     }

# @mcp.tool
# def compute_metric_updates(
#     inflation_pct: Annotated[float, "Inflation percentage change"],
#     exchange_rate_pct: Annotated[float, "Exchange rate percentage change"],
#     interest_rate_pct: Annotated[float, "Interest rate percentage change"],
#     yesterday_inflation: Annotated[float, "Yesterday's inflation value"],
#     yesterday_exchange_rate: Annotated[float, "Yesterday's exchange rate value"],
#     yesterday_interest_rate: Annotated[float, "Yesterday's interest rate value"],
# ) -> Dict[str, float]:
#     """Computes updated metrics based on percentage changes and previous values."""
#     new_inflation = yesterday_inflation * (1 + inflation_pct / 100)
#     new_exchange_rate = yesterday_exchange_rate * (1 + exchange_rate_pct / 100)
#     new_interest_rate = yesterday_interest_rate * (1 + interest_rate_pct / 100)

#     new_inflation = max(0, min(new_inflation, 20))
#     new_exchange_rate = max(0.1, new_exchange_rate)
#     new_interest_rate = max(0, min(new_interest_rate, 15))

#     return {
#         "inflation": round(new_inflation, 2),
#         "exchange_rate": round(new_exchange_rate, 4),
#         "interest_rate": round(new_interest_rate, 2),
#     }

# @mcp.tool
# def detect_risks_opportunities(
#     summaries: Annotated[List[str], "News summaries"],
#     metrics: Annotated[Dict[str, float], "Economic metrics"],
#     firm: Annotated[str, "Firm name"],
# ) -> Dict[str, List[str]]:
#     """Identifies risks and opportunities from summaries + metrics."""
#     risks: List[str] = []
#     opportunities: List[str] = []

#     inflation = metrics["inflation"]
#     interest_rate = metrics["interest_rate"]
#     exchange_rate = metrics["exchange_rate"]

#     if inflation > 4.0:
#         risks.append(f"High inflation ({inflation}%) may erode {firm}'s profit margins")
#         opportunities.append(f"Pricing power opportunities for {firm}")
#     elif inflation < 1.0:
#         risks.append(f"Deflationary pressure ({inflation}%) may signal economic weakness")

#     if interest_rate > 6.0:
#         risks.append(f"High interest rates ({interest_rate}%) increase {firm}'s borrowing costs")
#         opportunities.append(f"Higher yields on {firm}'s cash investments")
#     elif interest_rate < 2.0:
#         opportunities.append(f"Low borrowing costs ({interest_rate}%) enable expansion financing for {firm}")

#     if exchange_rate > 1.2:
#         risks.append(f"Strong currency may hurt {firm}'s export competitiveness")
#         opportunities.append(f"Favorable conditions for international acquisitions")
#     elif exchange_rate < 0.9:
#         opportunities.append(f"Weak currency boosts {firm}'s export revenues")
#         risks.append(f"Higher import costs for {firm}'s operations")

#     return {"risks": risks, "opportunities": opportunities}

# @mcp.tool
# def generate_recommendations(
#     risks: Annotated[List[str], "Identified risks"],
#     opportunities: Annotated[List[str], "Identified opportunities"],
# ) -> Dict[str, Any]:
#     """Generates strategic recommendations from risks & opportunities."""
#     total_items = len(risks) + len(opportunities)
#     risk_ratio = len(risks) / total_items if total_items > 0 else 0

#     if risk_ratio > 0.6:
#         synthesis = "Significant risks detected. Defensive strategy recommended."
#     elif risk_ratio < 0.3:
#         synthesis = "Opportunities outweigh risks. Aggressive growth strategy recommended."
#     else:
#         synthesis = "Balanced outlook. Adopt a mixed strategy."

#     recommendations: List[str] = []
#     if not recommendations:
#         recommendations = [
#             "Monitor economic indicators closely",
#             "Maintain operational flexibility",
#             "Strengthen stakeholder communication",
#         ]

#     return {"synthesis": synthesis, "recommendations": recommendations}


if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000, path="/")
