from typing import Annotated
from fastmcp import FastMCP

mcp = FastMCP("Demo 🚀")


@mcp.tool
def add(
    a: Annotated[int, "First number to add"], b: Annotated[int, "Second number to add"]
) -> int:
    """Add two integers and return the sum"""
    return a + b


@mcp.tool
def multiply(
    a: Annotated[float, "First number to multiply"],
    b: Annotated[float, "Second number to multiply"],
) -> float:
    """Multiply two numbers and return the product"""
    return a * b


@mcp.tool
def word_count(text: Annotated[str, "Text to analyze for word count"]) -> dict:
    """Count words, characters, and unique words in the given text"""
    words = text.split()
    return {
        "word_count": len(words),
        "char_count": len(text),
        "unique_words": len(set(word.lower() for word in words)),
    }

# --------------------
# CONCRETE IMPLEMENTATION
# --------------------

import statistics
from urllib.parse import urlparse

from pydantic import HttpUrl

from abc import ABC, abstractmethod
from typing import List, Optional

from pydantic import BaseModel, HttpUrl

# --------------------
# SCHEMAS
# --------------------

class NewsInput(BaseModel):
    sources: List[HttpUrl]


class NewsOutput(BaseModel):
    summaries: List[str]
    inflation_pct: Optional[float] = None
    exchange_rate_pct: Optional[float] = None
    interest_rate_pct: Optional[float] = None


class MetricsUpdateInput(BaseModel):
    inflation_pct: float
    exchange_rate_pct: float
    interest_rate_pct: float
    yesterday_inflation: float
    yesterday_exchange_rate: float
    yesterday_interest_rate: float


class MetricsUpdateOutput(BaseModel):
    inflation: float
    exchange_rate: float
    interest_rate: float


class RiskOpportunityInput(BaseModel):
    summaries: List[str]
    metrics: MetricsUpdateOutput
    firm: str


class RiskOpportunityOutput(BaseModel):
    risks: List[str]
    opportunities: List[str]


class RecommendationInput(BaseModel):
    risks: List[str]
    opportunities: List[str]


class RecommendationOutput(BaseModel):
    synthesis: str
    recommendations: List[str]


# --------------------
# ABSTRACT CLASS
# --------------------


class NewsAgent(ABC):
    @abstractmethod
    def analyze_news(self) -> NewsOutput:
        """Take news sources, return summaries + predicted metric evolutions."""
        pass

    @abstractmethod
    def compute_metric_updates(self, data: MetricsUpdateInput) -> MetricsUpdateOutput:
        """Take metric % evolutions + yesterday's values, return updated metrics."""
        pass

    @abstractmethod
    def detect_risks_opportunities(
        self, data: RiskOpportunityInput
    ) -> RiskOpportunityOutput:
        """Take summaries + new metrics + firm, return identified risks & opportunities."""
        pass

    @abstractmethod
    def generate_recommendations(
        self, data: RecommendationInput
    ) -> RecommendationOutput:
        """Take risks & opportunities, return synthesis and recommendations."""
        pass


class FinancialNewsAgent(NewsAgent):
    """
    A concrete implementation of NewsAgent for financial news analysis.
    This implementation simulates real-world financial news processing.
    """

    def __init__(self):
        # Economic indicators keywords for analysis
        self.inflation_keywords = [
            "inflation",
            "cpi",
            "consumer price",
            "price rise",
            "monetary policy",
        ]
        self.exchange_keywords = [
            "exchange rate",
            "currency",
            "forex",
            "dollar",
            "euro",
            "yen",
        ]
        self.interest_keywords = [
            "interest rate",
            "federal reserve",
            "central bank",
            "fed",
            "monetary",
        ]

    def analyze_news(self) -> NewsOutput:
        """
        Simulates analyzing news sources and extracting economic indicators.
        In a real implementation, this would fetch and parse actual news content.
        """
        sources = [
            "https://www.google.com/finance/",
            "https://bloomberg.com/article",
            "https://fed.gov/announcement",
        ]
        urls = [HttpUrl(url) for url in sources]
        data = NewsInput(sources=urls)
        summaries = []
        inflation_signals = []
        exchange_signals = []
        interest_signals = []

        for source_url in data.sources:
            # Simulate news content analysis based on URL domain
            domain = urlparse(str(source_url)).netloc.lower()

            if "bloomberg" in domain or "reuters" in domain:
                summary = f"Financial markets report from {domain}: Mixed economic signals with focus on monetary policy"
                inflation_signals.append(0.2)  # Slight inflationary pressure
                exchange_signals.append(-0.1)  # Minor currency weakening
                interest_signals.append(0.15)  # Potential rate increase

            elif "fed" in domain or "centralbank" in domain:
                summary = f"Central bank communication from {domain}: Policy stance remains data-dependent"
                inflation_signals.append(0.1)
                exchange_signals.append(0.05)
                interest_signals.append(0.25)  # Higher probability of rate action

            elif "wsj" in domain or "ft.com" in domain:
                summary = f"Market analysis from {domain}: Corporate earnings and economic indicators show resilience"
                inflation_signals.append(0.05)
                exchange_signals.append(0.1)
                interest_signals.append(0.0)

            else:
                summary = f"Economic news from {domain}: General market developments and policy discussions"
                inflation_signals.append(0.0)
                exchange_signals.append(0.0)
                interest_signals.append(0.05)

            summaries.append(summary)

        # Aggregate signals into predictions
        inflation_pct = (
            statistics.mean(inflation_signals) if inflation_signals else None
        )
        exchange_rate_pct = (
            statistics.mean(exchange_signals) if exchange_signals else None
        )
        interest_rate_pct = (
            statistics.mean(interest_signals) if interest_signals else None
        )

        return NewsOutput(
            summaries=summaries,
            inflation_pct=inflation_pct,
            exchange_rate_pct=exchange_rate_pct,
            interest_rate_pct=interest_rate_pct,
        )

    def compute_metric_updates(self, data: MetricsUpdateInput) -> MetricsUpdateOutput:
        """
        Computes updated metrics based on percentage changes and previous values.
        """
        # Apply percentage changes to yesterday's values
        new_inflation = data.yesterday_inflation * (1 + data.inflation_pct / 100)
        new_exchange_rate = data.yesterday_exchange_rate * (
            1 + data.exchange_rate_pct / 100
        )
        new_interest_rate = data.yesterday_interest_rate * (
            1 + data.interest_rate_pct / 100
        )

        # Apply bounds to keep values realistic
        new_inflation = max(0, min(new_inflation, 20))  # Cap inflation at 20%
        new_exchange_rate = max(0.1, new_exchange_rate)  # Minimum exchange rate
        new_interest_rate = max(
            0, min(new_interest_rate, 15)
        )  # Cap interest rate at 15%

        return MetricsUpdateOutput(
            inflation=round(new_inflation, 2),
            exchange_rate=round(new_exchange_rate, 4),
            interest_rate=round(new_interest_rate, 2),
        )

    def detect_risks_opportunities(
        self, data: RiskOpportunityInput
    ) -> RiskOpportunityOutput:
        """
        Identifies risks and opportunities based on news summaries and economic metrics.
        """
        risks = []
        opportunities = []

        # Analyze inflation risks/opportunities
        if data.metrics.inflation > 4.0:
            risks.append(
                f"High inflation ({data.metrics.inflation}%) may erode {data.firm}'s profit margins"
            )
            opportunities.append(
                f"Pricing power opportunities for {data.firm} in inflationary environment"
            )
        elif data.metrics.inflation < 1.0:
            risks.append(
                f"Deflationary pressure ({data.metrics.inflation}%) may signal economic weakness"
            )

        # Analyze interest rate impacts
        if data.metrics.interest_rate > 6.0:
            risks.append(
                f"High interest rates ({data.metrics.interest_rate}%) increase {data.firm}'s borrowing costs"
            )
            opportunities.append(f"Higher yields on {data.firm}'s cash investments")
        elif data.metrics.interest_rate < 2.0:
            opportunities.append(
                f"Low borrowing costs ({data.metrics.interest_rate}%) enable expansion financing for {data.firm}"
            )

        # Analyze exchange rate impacts (assuming USD base)
        if data.metrics.exchange_rate > 1.2:  # Assuming EUR/USD or similar
            risks.append(
                f"Strong currency may hurt {data.firm}'s export competitiveness"
            )
            opportunities.append(
                f"Favorable conditions for {data.firm}'s international acquisitions"
            )
        elif data.metrics.exchange_rate < 0.9:
            opportunities.append(f"Weak currency boosts {data.firm}'s export revenues")
            risks.append(
                f"Higher import costs for {data.firm}'s international operations"
            )

        # Analyze news sentiment
        negative_keywords = [
            "uncertainty",
            "volatility",
            "decline",
            "crisis",
            "recession",
        ]
        positive_keywords = ["growth", "expansion", "bullish", "optimistic", "recovery"]

        for summary in data.summaries:
            summary_lower = summary.lower()

            if any(keyword in summary_lower for keyword in negative_keywords):
                risks.append(
                    f"Market uncertainty may impact {data.firm}'s business confidence"
                )

            if any(keyword in summary_lower for keyword in positive_keywords):
                opportunities.append(
                    f"Positive market sentiment creates growth opportunities for {data.firm}"
                )

        return RiskOpportunityOutput(risks=risks, opportunities=opportunities)

    def generate_recommendations(
        self, data: RecommendationInput
    ) -> RecommendationOutput:
        """
        Generates strategic recommendations based on identified risks and opportunities.
        """
        total_items = len(data.risks) + len(data.opportunities)
        risk_ratio = len(data.risks) / total_items if total_items > 0 else 0

        # Generate synthesis
        if risk_ratio > 0.6:
            synthesis = (
                "Current market conditions present significant challenges with elevated risks across "
                "multiple dimensions. A defensive strategy focusing on risk mitigation and capital "
                "preservation is recommended."
            )
        elif risk_ratio < 0.3:
            synthesis = (
                "Market environment is favorable with abundant opportunities outweighing risks. "
                "An aggressive growth strategy leveraging current conditions is advisable."
            )
        else:
            synthesis = (
                "Balanced risk-opportunity landscape requires a measured approach combining "
                "selective risk mitigation with strategic opportunity capture."
            )

        # Generate specific recommendations
        recommendations = []

        # Risk-based recommendations
        if any("inflation" in risk.lower() for risk in data.risks):
            recommendations.append(
                "Implement dynamic pricing strategies to maintain margins amid inflationary pressures"
            )
            recommendations.append(
                "Consider inflation-hedged investments and contracts"
            )

        if any("interest rate" in risk.lower() for risk in data.risks):
            recommendations.append(
                "Prioritize debt refinancing before rates increase further"
            )
            recommendations.append(
                "Accelerate capital-intensive projects while financing costs remain manageable"
            )

        if any(
            "currency" in risk.lower() or "exchange" in risk.lower()
            for risk in data.risks
        ):
            recommendations.append(
                "Implement currency hedging strategies for international operations"
            )
            recommendations.append(
                "Diversify revenue streams across multiple currencies"
            )

        # Opportunity-based recommendations
        if any(
            "growth" in opp.lower() or "expansion" in opp.lower()
            for opp in data.opportunities
        ):
            recommendations.append(
                "Accelerate market expansion plans to capitalize on favorable conditions"
            )
            recommendations.append(
                "Increase marketing and sales investments to capture market share"
            )

        if any(
            "acquisition" in opp.lower() or "investment" in opp.lower()
            for opp in data.opportunities
        ):
            recommendations.append(
                "Evaluate strategic acquisition opportunities while valuations are attractive"
            )
            recommendations.append(
                "Strengthen balance sheet to take advantage of investment opportunities"
            )

        # Default recommendations if lists are empty
        if not recommendations:
            recommendations = [
                "Monitor economic indicators closely for emerging trends",
                "Maintain operational flexibility to adapt to changing conditions",
                "Strengthen stakeholder communication regarding market outlook",
            ]

        return RecommendationOutput(
            synthesis=synthesis, recommendations=recommendations
        )


our_agent = FinancialNewsAgent()
@mcp.tool
def analyzenews():
    """
    Simulates analyzing news sources and extracting economic indicators.
    In a real implementation, this would fetch and parse actual news content.
    """
    return our_agent.analyze_news()


if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000, path="/")
