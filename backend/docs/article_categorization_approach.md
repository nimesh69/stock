# Article-to-Company Categorization: Multiplicative Scoring Approach

## Overview

This document explains the scoring system used to automatically categorize news articles by company. The system combines **semantic embedding similarity** with **exact text matching** to determine whether an article is about a specific company.

---

## The Problem with Additive Scoring

The original approach used additive scoring:

```
final_score = exact_match_bonus + embedding_contribution
```

Where:
- `exact_match_bonus` = 0.15–0.30 (depending on match location)
- `embedding_contribution` = 0.0–0.40 (heavily compressed)

### Why it failed

| Scenario | Exact Bonus | Max Embedding | Final Score | Passes 0.60? |
|----------|-------------|---------------|-------------|--------------|
| No exact match | 0 | 0.40 | **0.40** | ❌ Never |
| Alias in body | 0.15 | 0.40 | **0.55** | ❌ Never |
| Symbol/Name in body | 0.20 | 0.40 | **0.60** | ⚠️ Barely |
| Alias in headline | 0.25 | 0.40 | **0.65** | ✓ |
| Symbol/Name in headline | 0.30 | 0.40 | **0.70** | ✓ |

**Key insight:** Without an exact text match, it was mathematically impossible to reach the 0.60 threshold. Yet 97% of article-company pairs had no exact match — the articles were *about* companies without literally naming them.

---

## The Multiplicative Solution

The new approach uses multiplicative scoring:

```
final_score = embedding_similarity × confidence_boost
```

Where:
- `embedding_similarity` = raw cosine similarity (0.0–1.0)
- `confidence_boost` = 1.0–1.20 (based on exact match location)

### Why it works better

| Scenario | Embedding | Boost | Final Score | Passes 0.55? |
|----------|-----------|-------|-------------|--------------|
| No exact match, strong semantic match | 0.70 | 1.00 | **0.70** | ✓ Yes |
| Body mention + strong semantic match | 0.65 | 1.05 | **0.68** | ✓ Yes |
| Headline mention + strong semantic match | 0.60 | 1.15 | **0.69** | ✓ Yes |
| Weak semantic match, no mention | 0.30 | 1.00 | **0.30** | ❌ No (correct) |
| Weak semantic match, body mention | 0.35 | 1.05 | **0.37** | ❌ No (correct) |

**Embedding is the primary signal.** Exact match boosts confidence but isn't required.

---

## Scoring Rules

### 1. Embedding Floor (Hard Gate)

Articles with embedding similarity below the floor are rejected immediately — no need to check exact matches.

```python
if embedding_score < embedding_floor:  # default: 0.35
    reject
```

This prevents completely unrelated articles from being evaluated.

### 2. Confidence Boosts

| Match Type | Boost | Method Code | Description |
|------------|-------|-------------|-------------|
| Symbol in headline | 1.20 | `hl_sym` | Ticker symbol appears in headline |
| Name in headline | 1.15 | `hl_name` | Full company name in headline |
| Alias in headline | 1.10 | `hl_alias` | Known alias in headline |
| Symbol/Name in body | 1.05 | `body` | Ticker or name in article body |
| Alias in body | 1.02 | `body_alias` | Known alias in body |
| No exact match | 1.00 | `embed` | Pure semantic match |

### 3. Weak Embedding Penalty

For body matches with weak embeddings (< 0.45), apply a 20% penalty:

```python
if embedding_score < 0.45 and method.startswith("body"):
    final_score = final_score × 0.8
```

This prevents false positives like "Apple pie recipe" matching Apple Inc.

### 4. Threshold Gate

Final score must exceed the threshold (default: 0.55) to create a category.

```python
if final_score < threshold:
    reject
```

---

## Example Walkthroughs

### Example 1: Semantic match, no exact mention

**Article:** *"The Cupertino tech giant unveiled new AI features for its flagship phone..."*

**Company:** Apple Inc. (AAPL)

| Step | Value |
|------|-------|
| Embedding similarity | 0.82 (article is clearly about Apple) |
| Exact match? | No "Apple", "AAPL", or alias found |
| Boost | 1.00 |
| Final score | 0.82 × 1.00 = **0.82** |
| Passes 0.55? | ✓ Yes |
| Method | `embed` |

**Result:** Categorized as Apple article despite no literal mention.

---

### Example 2: Headline mention + strong semantic match

**Article:** *"Apple Inc. reports record Q3 earnings amid AI push"*

**Company:** Apple Inc. (AAPL)

| Step | Value |
|------|-------|
| Embedding similarity | 0.78 |
| Exact match? | "Apple Inc." in headline |
| Boost | 1.15 (name in headline) |
| Final score | 0.78 × 1.15 = **0.90** (capped at 1.0) |
| Passes 0.55? | ✓ Yes |
| Method | `hl_name` |

**Result:** High-confidence categorization.

---

### Example 3: False positive prevention

**Article:** *"I ate an apple pie for breakfast at the new cafe"*

**Company:** Apple Inc. (AAPL)

| Step | Value |
|------|-------|
| Embedding similarity | 0.25 (article is about food, not tech) |
| Exact match? | "apple" in body |
| Floor check | 0.25 < 0.35 → **rejected immediately** |
| Final score | N/A |

**Result:** Correctly rejected. The embedding floor catches semantic mismatches before exact match logic can create a false positive.

---

### Example 4: Edge case — weak body mention

**Article:** *"Several tech companies, including Apple, were mentioned in the report"*

**Company:** Apple Inc. (AAPL)

| Step | Value |
|------|-------|
| Embedding similarity | 0.40 (weak — article is about tech broadly) |
| Exact match? | "Apple" in body |
| Boost | 1.05 (body match) |
| Weak penalty | 0.40 × 1.05 = 0.42; 0.42 × 0.8 = **0.34** |
| Passes 0.55? | ❌ No |

**Result:** Correctly rejected. The article mentions Apple but isn't *about* Apple.

---

## Architecture

```
┌─────────────────┐
│  RawArticle     │
│  (headline,     │
│   body)         │
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│  SentenceTransformer    │
│  (all-MiniLM-L6-v2)     │
│  → article_vector       │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐     ┌─────────────────────┐
│  For each company:      │◄────│  CompanyEmbedding   │
│                         │     │  (pre-computed)     │
│  1. Cosine similarity   │     └─────────────────────┘
│  2. Exact match check   │
│  3. Apply boost         │
│  4. Floor + threshold   │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│  ArticleCategory        │
│  (article, company,     │
│   confidence, method)   │
└─────────────────────────┘
```

---

## Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--threshold` | 0.55 | Minimum final score to create a category |
| `--embedding-floor` | 0.35 | Minimum raw embedding to evaluate at all |
| `--debug` | false | Print per-article scoring details |
| `--debug-company` | null | Filter debug to specific company |
| `--sample` | 0 | Process only N articles (for testing) |

### Tuning guidelines

| Goal | Action |
|------|--------|
| Too many false positives | Raise `--threshold` or `--embedding-floor` |
| Too few categories | Lower `--threshold` or `--embedding-floor` |
| Noisy embedding-only matches | Raise `--embedding-floor` |
| Missing relevant articles | Lower `--threshold` |

---

## Method Codes

Stored in the database `method` field (max 20 chars):

| Code | Full Name | Meaning |
|------|-----------|---------|
| `hl_sym` | Headline Symbol | Ticker in headline |
| `hl_name` | Headline Name | Company name in headline |
| `hl_alias` | Headline Alias | Alias in headline |
| `body` | Body Match | Symbol or name in body |
| `body_alias` | Body Alias | Alias in body |
| `embed` | Embedding Only | Pure semantic match |

---

## Key Design Decisions

1. **Embedding as primary signal** — Most articles about companies don't literally name them. Semantic similarity captures "aboutness" better than keyword matching.

2. **Exact match as confidence booster** — When a company is explicitly named, we trust the embedding more. The boost is multiplicative, not additive, so it scales with embedding strength.

3. **Embedding floor as noise gate** — Completely unrelated articles are filtered before exact match logic can create false positives.

4. **Weak body penalty** — Body mentions with weak embeddings are penalized because body text is noisier than headlines.

5. **Capped at 1.0** — Final scores are capped to maintain a 0–1 probability-like scale.
