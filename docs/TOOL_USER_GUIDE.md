# Part II: Multi-Tool Agent User Guide

This guide provides an overview of all available tools in our realistic agent implementation, along with usage examples.

## Table of Contents

- [Overview](#overview)
- [Tools](#tools)
  - [1. Google Search](#1-google-search)
  - [2. Google Shopping](#2-google-shopping)
  - [3. Google Maps](#3-google-maps)
  - [4. Google Scholar](#4-google-scholar)
  - [5. Browse Website](#5-browse-website)
- [Agent Usage](#agent-usage)
- [Example Tasks](#example-tasks)

---

## Overview

Our agent supports **5 tools** powered by the Serper API and web scraping:

| Tool | Description | API Endpoint |
|------|-------------|--------------|
| Google Search | General web search | `google.serper.dev/search` |
| Google Shopping | Product search with prices | `google.serper.dev/shopping` |
| Google Maps | Place/location search | `google.serper.dev/places` |
| Google Scholar | Academic paper search | `google.serper.dev/scholar` |
| Browse Website | Web page content extraction | Direct HTTP request |

---

## Tools

### 1. Google Search

**Description**: Perform general web searches to find information, facts, news, or any web content.

**Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `query` | string or list | Yes | Search query (supports batch search with list) |
| `page` | int | No | Page number (default: 1) |
| `tbs` | string | No | Time filter: `anytime`, `past_hour`, `past_24h`, `past_week`, `past_month`, `past_year` |

**Example**:
```python
from src.tools import google_search

# Single search
result = google_search("What is machine learning?")

# Search with time filter
result = google_search("latest AI news", tbs="past_week")

# Batch search
result = google_search(["Python tutorial", "JavaScript tutorial"])
```

**Response Format**:
```json
{
  "organic": [
    {
      "title": "Machine Learning - Wikipedia",
      "link": "https://en.wikipedia.org/wiki/Machine_learning",
      "snippet": "Machine learning is a subset of artificial intelligence..."
    }
  ]
}
```

---

### 2. Google Shopping

**Description**: Search for products with prices, ratings, and availability information.

**Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `query` | string | Yes | Product search query |
| `num` | int | No | Number of results (default: 10) |
| `page` | int | No | Page number (default: 1) |

**Example**:
```python
from src.tools import google_shopping

# Search for products
result = google_shopping("iPhone 15 Pro", num=5)

# Get more results
result = google_shopping("wireless earbuds", num=10, page=2)
```

**Response Format**:
```json
{
  "shopping": [
    {
      "title": "Apple iPhone 15 Pro 128GB",
      "price": "HK$8,599.00",
      "source": "Apple Store",
      "rating": 4.8,
      "ratingCount": 1200,
      "link": "https://..."
    }
  ]
}
```

---

### 3. Google Maps

**Description**: Search for places, restaurants, attractions, or any location-based queries.

**Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `query` | string | Yes | Type of place to search |
| `location` | string | No | Location to search around |
| `num` | int | No | Number of results (default: 10) |

**Example**:
```python
from src.tools import google_maps_search

# Search for places
result = google_maps_search("coffee shops", location="Central, Hong Kong")

# Search for restaurants
result = google_maps_search("Italian restaurants", location="Tsim Sha Tsui", num=5)
```

**Response Format**:
```json
{
  "query": "coffee shops in Central, Hong Kong",
  "places": [
    {
      "title": "Chart Coffee (Central Market)",
      "rating": 4.7,
      "reviews": 466,
      "price_level": "$1–50",
      "category": "Coffee shop",
      "position": 1,
      "cid": "18204743282192435345",
      "google_maps_link": "https://www.google.com/maps?cid=18204743282192435345"
    }
  ],
  "total": 10
}
```

> **Note**: Serper Places API does not provide detailed address, coordinates, phone, or website information. Use the `google_maps_link` to view full details on Google Maps.

---

### 3.1 Place Recommendation (recommend_places)

**Description**: Get smart recommendations from place search results using a scoring algorithm.

**Algorithm**:
```
Score = Rating(40%) + Reviews(30%) + Position(30%)
```
- **Rating Score**: `(rating / 5.0) * 40`
- **Reviews Score**: `log-normalized(reviews) * 30`
- **Position Score**: `(1 / position) * 30`

**Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `places` | list | Yes | Place list from `google_maps_search` |
| `top_n` | int | No | Number of recommendations (default: 5) |
| `price_preference` | string | No | Filter: `any`, `budget`, `moderate`, `expensive` |

**Example**:
```python
from src.tools import google_maps_search, recommend_places

# Step 1: Search for places
result = google_maps_search("coffee shops", location="Central, Hong Kong")

# Step 2: Get recommendations
recommendations = recommend_places(result['places'], top_n=5)

# Step 3: Filter by budget
budget_recs = recommend_places(result['places'], top_n=3, price_preference="budget")
```

**Response Format**:
```json
{
  "recommendations": [
    {
      "title": "Chart Coffee (Central Market)",
      "rating": 4.7,
      "reviews": 466,
      "price_level": "$1–50",
      "recommendation_score": 93.93,
      "score_breakdown": {
        "rating_score": 37.6,
        "reviews_score": 26.33,
        "position_score": 30.0
      },
      "google_maps_link": "https://www.google.com/maps?cid=..."
    }
  ],
  "total_analyzed": 10,
  "price_filter": "any",
  "algorithm": "Weighted score: Rating(40%) + Reviews(30%) + Position(30%)"
}

---

### 4. Google Scholar

**Description**: Search for academic papers, research articles, and citations.

**Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `query` | string | Yes | Academic search query |
| `num` | int | No | Number of results (default: 10) |
| `year_low` | int | No | Filter papers from this year onwards |
| `year_high` | int | No | Filter papers up to this year |

**Example**:
```python
from src.tools import google_scholar

# Search for papers
result = google_scholar("transformer attention mechanism")

# Search with year filter
result = google_scholar("large language model", num=5, year_low=2023)

# Search within year range
result = google_scholar("BERT NLP", year_low=2018, year_high=2020)
```

**Response Format**:
```json
{
  "query": "transformer attention mechanism",
  "papers": [
    {
      "title": "Attention Is All You Need",
      "link": "https://arxiv.org/abs/1706.03762",
      "snippet": "The dominant sequence transduction models...",
      "publication_info": "A Vaswani, N Shazeer... - NeurIPS, 2017",
      "authors": ["A Vaswani", "N Shazeer", "N Parmar"],
      "year": 2017,
      "cited_by": 95000,
      "pdf_link": "https://arxiv.org/pdf/1706.03762.pdf"
    }
  ],
  "total": 10
}
```

---

### 5. Browse Website

**Description**: Extract and read the full text content from a webpage.

**Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `url` | string | Yes | URL of the website to browse |

**Example**:
```python
from src.tools import browse_website

# Read webpage content
content = browse_website("https://en.wikipedia.org/wiki/Artificial_intelligence")

# Read a news article
content = browse_website("https://www.bbc.com/news/technology-12345678")
```

**Response Format**:
```
Artificial intelligence (AI) is the capability of computational systems...
[Full text content of the webpage]
```

---

## Agent Usage

### Initialize the Agent

```python
from src.agent import SearchAgent

# Basic agent with Google Search only
agent = SearchAgent()

# Agent with all tools enabled
agent = SearchAgent(
    use_shopping=True,
    use_browsing=True,
    enable_maps=True,
    enable_scholar=True
)
```

### Agent Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `model` | str | `"deepseek-chat"` | LLM model to use |
| `temperature` | float | `0.0` | Model temperature |
| `max_steps` | int | `10` | Maximum reasoning steps |
| `use_tools` | bool | `True` | Enable tool usage |
| `use_shopping` | bool | `False` | Enable Google Shopping |
| `use_browsing` | bool | `False` | Enable website browsing |
| `enable_maps` | bool | `False` | Enable Google Maps |
| `enable_scholar` | bool | `False` | Enable Google Scholar |

### Solve a Question

```python
result = agent.solve("Find me the top 3 papers on LLM and recommend a textbook to buy")

print(result["final_answer"])      # The agent's answer
print(result["reasoning_steps"])   # Step-by-step reasoning
print(result["tool_calls"])        # List of tool calls made
```

---

## Example Tasks

### Task 1: Academic Research + Textbook Purchase

```python
agent = SearchAgent(
    use_shopping=True,
    use_browsing=True,
    enable_scholar=True
)

result = agent.solve("""
I want to research Large Language Models (LLM). Please:
1. Find recent papers on LLM (2023-2024)
2. Explain what LLM is
3. Recommend a deep learning textbook to buy
""")
```

### Task 2: Conference Preparation

```python
agent = SearchAgent(
    use_shopping=True,
    enable_maps=True,
    enable_scholar=True
)

result = agent.solve("""
I'm attending an AI conference in Hong Kong. Help me:
1. Find recent AI papers to discuss
2. Find hotels near Hong Kong Convention Centre
3. Find restaurants nearby
4. Recommend a laser pointer to buy for my presentation
""")
```

### Task 3: Thesis Topic Research

```python
agent = SearchAgent(
    use_shopping=True,
    use_browsing=True,
    enable_scholar=True
)

result = agent.solve("""
I'm choosing my thesis topic in computer vision. Please:
1. Find survey papers on object detection
2. Explain the current research trends
3. Find the original YOLO paper
4. Recommend edge computing hardware for experiments
""")
```

---

## Environment Setup

1. Set API keys in `.env` file:
```bash
Serper-API=your_serper_api_key
DeepSeek-API=your_deepseek_api_key
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the agent:
```bash
python -c "
from src.agent import SearchAgent
agent = SearchAgent(use_shopping=True, enable_scholar=True, enable_maps=True)
result = agent.solve('Your question here')
print(result['final_answer'])
"
```

---

## API Credits

Each tool call consumes Serper API credits:
- Google Search: 1 credit
- Google Shopping: 2 credits
- Google Maps: 1 credit
- Google Scholar: 1 credit

Monitor your usage at [serper.dev](https://serper.dev).

