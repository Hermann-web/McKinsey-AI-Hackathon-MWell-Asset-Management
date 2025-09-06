#!/usr/bin/env node

/**
 * JavaScript MCP Server for NewsAgent functionality
 * Requires: @modelcontextprotocol/sdk
 */

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

// --------------------
// SCHEMAS (using plain objects since we don't have Pydantic)
// --------------------

class NewsInput {
  constructor(sources) {
    this.sources = sources; // Array of URLs
  }
}

class NewsOutput {
  constructor(summaries, inflation_pct = null, exchange_rate_pct = null, interest_rate_pct = null) {
    this.summaries = summaries;
    this.inflation_pct = inflation_pct;
    this.exchange_rate_pct = exchange_rate_pct;
    this.interest_rate_pct = interest_rate_pct;
  }
}

class MetricsUpdateInput {
  constructor(inflation_pct, exchange_rate_pct, interest_rate_pct, yesterday_inflation, yesterday_exchange_rate, yesterday_interest_rate) {
    this.inflation_pct = inflation_pct;
    this.exchange_rate_pct = exchange_rate_pct;
    this.interest_rate_pct = interest_rate_pct;
    this.yesterday_inflation = yesterday_inflation;
    this.yesterday_exchange_rate = yesterday_exchange_rate;
    this.yesterday_interest_rate = yesterday_interest_rate;
  }
}

class MetricsUpdateOutput {
  constructor(inflation, exchange_rate, interest_rate) {
    this.inflation = inflation;
    this.exchange_rate = exchange_rate;
    this.interest_rate = interest_rate;
  }
}

class RiskOpportunityInput {
  constructor(summaries, metrics, firm) {
    this.summaries = summaries;
    this.metrics = metrics;
    this.firm = firm;
  }
}

class RiskOpportunityOutput {
  constructor(risks, opportunities) {
    this.risks = risks;
    this.opportunities = opportunities;
  }
}

class RecommendationInput {
  constructor(risks, opportunities) {
    this.risks = risks;
    this.opportunities = opportunities;
  }
}

class RecommendationOutput {
  constructor(synthesis, recommendations) {
    this.synthesis = synthesis;
    this.recommendations = recommendations;
  }
}

// --------------------
// FINANCIAL NEWS AGENT IMPLEMENTATION
// --------------------

class FinancialNewsAgent {
  constructor() {
    // Economic indicators keywords for analysis
    this.inflation_keywords = ["inflation", "cpi", "consumer price", "price rise", "monetary policy"];
    this.exchange_keywords = ["exchange rate", "currency", "forex", "dollar", "euro", "yen"];
    this.interest_keywords = ["interest rate", "federal reserve", "central bank", "fed", "monetary"];
  }

  analyzeNews(sources) {
    const summaries = [];
    const inflation_signals = [];
    const exchange_signals = [];
    const interest_signals = [];

    for (const source_url of sources) {
      // Simulate news content analysis based on URL domain
      const url = new URL(source_url);
      const domain = url.hostname.toLowerCase();

      let summary, inflationSignal, exchangeSignal, interestSignal;

      if (domain.includes("bloomberg") || domain.includes("reuters")) {
        summary = `Financial markets report from ${domain}: Mixed economic signals with focus on monetary policy`;
        inflationSignal = 0.2;  // Slight inflationary pressure
        exchangeSignal = -0.1;  // Minor currency weakening
        interestSignal = 0.15;  // Potential rate increase
      } else if (domain.includes("fed") || domain.includes("centralbank")) {
        summary = `Central bank communication from ${domain}: Policy stance remains data-dependent`;
        inflationSignal = 0.1;
        exchangeSignal = 0.05;
        interestSignal = 0.25;  // Higher probability of rate action
      } else if (domain.includes("wsj") || domain.includes("ft.com")) {
        summary = `Market analysis from ${domain}: Corporate earnings and economic indicators show resilience`;
        inflationSignal = 0.05;
        exchangeSignal = 0.1;
        interestSignal = 0.0;
      } else {
        summary = `Economic news from ${domain}: General market developments and policy discussions`;
        inflationSignal = 0.0;
        exchangeSignal = 0.0;
        interestSignal = 0.05;
      }

      summaries.push(summary);
      inflation_signals.push(inflationSignal);
      exchange_signals.push(exchangeSignal);
      interest_signals.push(interestSignal);
    }

    // Calculate mean of signals
    const mean = (arr) => arr.length > 0 ? arr.reduce((a, b) => a + b, 0) / arr.length : null;

    const inflation_pct = mean(inflation_signals);
    const exchange_rate_pct = mean(exchange_signals);
    const interest_rate_pct = mean(interest_signals);

    return new NewsOutput(summaries, inflation_pct, exchange_rate_pct, interest_rate_pct);
  }

  computeMetricUpdates(data) {
    // Apply percentage changes to yesterday's values
    let new_inflation = data.yesterday_inflation * (1 + data.inflation_pct / 100);
    let new_exchange_rate = data.yesterday_exchange_rate * (1 + data.exchange_rate_pct / 100);
    let new_interest_rate = data.yesterday_interest_rate * (1 + data.interest_rate_pct / 100);

    // Apply bounds to keep values realistic
    new_inflation = Math.max(0, Math.min(new_inflation, 20));  // Cap inflation at 20%
    new_exchange_rate = Math.max(0.1, new_exchange_rate);  // Minimum exchange rate
    new_interest_rate = Math.max(0, Math.min(new_interest_rate, 15));  // Cap interest rate at 15%

    return new MetricsUpdateOutput(
      Math.round(new_inflation * 100) / 100,
      Math.round(new_exchange_rate * 10000) / 10000,
      Math.round(new_interest_rate * 100) / 100
    );
  }

  detectRisksOpportunities(data) {
    const risks = [];
    const opportunities = [];

    // Analyze inflation risks/opportunities
    if (data.metrics.inflation > 4.0) {
      risks.push(`High inflation (${data.metrics.inflation}%) may erode ${data.firm}'s profit margins`);
      opportunities.push(`Pricing power opportunities for ${data.firm} in inflationary environment`);
    } else if (data.metrics.inflation < 1.0) {
      risks.push(`Deflationary pressure (${data.metrics.inflation}%) may signal economic weakness`);
    }

    // Analyze interest rate impacts
    if (data.metrics.interest_rate > 6.0) {
      risks.push(`High interest rates (${data.metrics.interest_rate}%) increase ${data.firm}'s borrowing costs`);
      opportunities.push(`Higher yields on ${data.firm}'s cash investments`);
    } else if (data.metrics.interest_rate < 2.0) {
      opportunities.push(`Low borrowing costs (${data.metrics.interest_rate}%) enable expansion financing for ${data.firm}`);
    }

    // Analyze exchange rate impacts (assuming USD base)
    if (data.metrics.exchange_rate > 1.2) {  // Assuming EUR/USD or similar
      risks.push(`Strong currency may hurt ${data.firm}'s export competitiveness`);
      opportunities.push(`Favorable conditions for ${data.firm}'s international acquisitions`);
    } else if (data.metrics.exchange_rate < 0.9) {
      opportunities.push(`Weak currency boosts ${data.firm}'s export revenues`);
      risks.push(`Higher import costs for ${data.firm}'s international operations`);
    }

    // Analyze news sentiment
    const negative_keywords = ["uncertainty", "volatility", "decline", "crisis", "recession"];
    const positive_keywords = ["growth", "expansion", "bullish", "optimistic", "recovery"];

    for (const summary of data.summaries) {
      const summary_lower = summary.toLowerCase();

      if (negative_keywords.some(keyword => summary_lower.includes(keyword))) {
        risks.push(`Market uncertainty may impact ${data.firm}'s business confidence`);
      }

      if (positive_keywords.some(keyword => summary_lower.includes(keyword))) {
        opportunities.push(`Positive market sentiment creates growth opportunities for ${data.firm}`);
      }
    }

    return new RiskOpportunityOutput(risks, opportunities);
  }

  generateRecommendations(data) {
    const total_items = data.risks.length + data.opportunities.length;
    const risk_ratio = total_items > 0 ? data.risks.length / total_items : 0;

    // Generate synthesis
    let synthesis;
    if (risk_ratio > 0.6) {
      synthesis = "Current market conditions present significant challenges with elevated risks across " +
        "multiple dimensions. A defensive strategy focusing on risk mitigation and capital " +
        "preservation is recommended.";
    } else if (risk_ratio < 0.3) {
      synthesis = "Market environment is favorable with abundant opportunities outweighing risks. " +
        "An aggressive growth strategy leveraging current conditions is advisable.";
    } else {
      synthesis = "Balanced risk-opportunity landscape requires a measured approach combining " +
        "selective risk mitigation with strategic opportunity capture.";
    }

    // Generate specific recommendations
    const recommendations = [];

    // Risk-based recommendations
    if (data.risks.some(risk => risk.toLowerCase().includes("inflation"))) {
      recommendations.push("Implement dynamic pricing strategies to maintain margins amid inflationary pressures");
      recommendations.push("Consider inflation-hedged investments and contracts");
    }

    if (data.risks.some(risk => risk.toLowerCase().includes("interest rate"))) {
      recommendations.push("Prioritize debt refinancing before rates increase further");
      recommendations.push("Accelerate capital-intensive projects while financing costs remain manageable");
    }

    if (data.risks.some(risk => risk.toLowerCase().includes("currency") || risk.toLowerCase().includes("exchange"))) {
      recommendations.push("Implement currency hedging strategies for international operations");
      recommendations.push("Diversify revenue streams across multiple currencies");
    }

    // Opportunity-based recommendations
    if (data.opportunities.some(opp => opp.toLowerCase().includes("growth") || opp.toLowerCase().includes("expansion"))) {
      recommendations.push("Accelerate market expansion plans to capitalize on favorable conditions");
      recommendations.push("Increase marketing and sales investments to capture market share");
    }

    if (data.opportunities.some(opp => opp.toLowerCase().includes("acquisition") || opp.toLowerCase().includes("investment"))) {
      recommendations.push("Evaluate strategic acquisition opportunities while valuations are attractive");
      recommendations.push("Strengthen balance sheet to take advantage of investment opportunities");
    }

    // Default recommendations if lists are empty
    if (recommendations.length === 0) {
      recommendations.push("Monitor economic indicators closely for emerging trends");
      recommendations.push("Maintain operational flexibility to adapt to changing conditions");
      recommendations.push("Strengthen stakeholder communication regarding market outlook");
    }

    return new RecommendationOutput(synthesis, recommendations);
  }
}

// --------------------
// MCP SERVER SETUP
// --------------------

class NewsAgentServer {
  constructor() {
    this.server = new Server(
      {
        name: "news-agent-server",
        version: "0.1.0",
      },
      {
        capabilities: {
          tools: {},
        },
      }
    );

    this.newsAgent = new FinancialNewsAgent();
    this.setupHandlers();
  }

  setupHandlers() {
    this.server.setRequestHandler(ListToolsRequestSchema, async () => {
      return {
        tools: [
          {
            name: "analyze_news",
            description: "Analyze news from given sources and predict metric evolutions",
            inputSchema: {
              type: "object",
              properties: {
                sources: {
                  type: "array",
                  items: { type: "string" },
                  description: "List of news source URLs"
                }
              },
              required: ["sources"]
            }
          },
          {
            name: "compute_metric_updates", 
            description: "Compute updated metrics based on percentage changes and yesterday's values",
            inputSchema: {
              type: "object",
              properties: {
                inflation_pct: { type: "number", description: "Inflation percentage change" },
                exchange_rate_pct: { type: "number", description: "Exchange rate percentage change" },
                interest_rate_pct: { type: "number", description: "Interest rate percentage change" },
                yesterday_inflation: { type: "number", description: "Yesterday's inflation value" },
                yesterday_exchange_rate: { type: "number", description: "Yesterday's exchange rate value" },
                yesterday_interest_rate: { type: "number", description: "Yesterday's interest rate value" }
              },
              required: ["inflation_pct", "exchange_rate_pct", "interest_rate_pct", "yesterday_inflation", "yesterday_exchange_rate", "yesterday_interest_rate"]
            }
          },
          {
            name: "detect_risks_opportunities",
            description: "Detect risks and opportunities based on summaries and metrics for a specific firm",
            inputSchema: {
              type: "object",
              properties: {
                summaries: {
                  type: "array",
                  items: { type: "string" },
                  description: "List of news summaries"
                },
                inflation: { type: "number", description: "Current inflation value" },
                exchange_rate: { type: "number", description: "Current exchange rate value" },
                interest_rate: { type: "number", description: "Current interest rate value" },
                firm: { type: "string", description: "Name of the firm to analyze" }
              },
              required: ["summaries", "inflation", "exchange_rate", "interest_rate", "firm"]
            }
          },
          {
            name: "generate_recommendations",
            description: "Generate synthesis and recommendations based on identified risks and opportunities",
            inputSchema: {
              type: "object",
              properties: {
                risks: {
                  type: "array",
                  items: { type: "string" },
                  description: "List of identified risks"
                },
                opportunities: {
                  type: "array",
                  items: { type: "string" },
                  description: "List of identified opportunities"
                }
              },
              required: ["risks", "opportunities"]
            }
          }
        ]
      };
    });

    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      try {
        switch (request.params.name) {
          case "analyze_news": {
            const { sources } = request.params.arguments;
            const result = this.newsAgent.analyzeNews(sources);
            return {
              content: [{ type: "text", text: JSON.stringify(result, null, 2) }]
            };
          }

          case "compute_metric_updates": {
            const {
              inflation_pct,
              exchange_rate_pct,
              interest_rate_pct,
              yesterday_inflation,
              yesterday_exchange_rate,
              yesterday_interest_rate
            } = request.params.arguments;
            
            const input = new MetricsUpdateInput(
              inflation_pct,
              exchange_rate_pct,
              interest_rate_pct,
              yesterday_inflation,
              yesterday_exchange_rate,
              yesterday_interest_rate
            );
            
            const result = this.newsAgent.computeMetricUpdates(input);
            return {
              content: [{ type: "text", text: JSON.stringify(result, null, 2) }]
            };
          }

          case "detect_risks_opportunities": {
            const { summaries, inflation, exchange_rate, interest_rate, firm } = request.params.arguments;
            
            const metrics = new MetricsUpdateOutput(inflation, exchange_rate, interest_rate);
            const input = new RiskOpportunityInput(summaries, metrics, firm);
            
            const result = this.newsAgent.detectRisksOpportunities(input);
            return {
              content: [{ type: "text", text: JSON.stringify(result, null, 2) }]
            };
          }

          case "generate_recommendations": {
            const { risks, opportunities } = request.params.arguments;
            
            const input = new RecommendationInput(risks, opportunities);
            const result = this.newsAgent.generateRecommendations(input);
            return {
              content: [{ type: "text", text: JSON.stringify(result, null, 2) }]
            };
          }

          default:
            throw new Error(`Unknown tool: ${request.params.name}`);
        }
      } catch (error) {
        return {
          content: [{ type: "text", text: JSON.stringify({ error: error.message }, null, 2) }]
        };
      }
    });
  }

  async run() {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error("News Agent MCP server running on stdio");
  }
}

// --------------------
// SERVER MAIN
// --------------------

const server = new NewsAgentServer();
server.run().catch(console.error);