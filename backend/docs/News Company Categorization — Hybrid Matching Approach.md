# News Company Categorization — Hybrid Matching Approach

## Overview

The news categorization system uses a **hybrid approach** to determine which companies an article is related to.

Instead of relying only on embedding similarity, the system combines:

1. **Company symbol matching**
2. **Company name matching**
3. **Company alias matching**
4. **Headline matching**
5. **Body matching**
6. **Semantic embedding similarity**

The main goal is to prevent false positives caused by embeddings.

---

# Why Embedding-Only Matching Is Not Enough

The initial implementation used cosine similarity:

```text
Article embedding
        ↓
Compare with every company embedding
        ↓
similarity >= 0.70
        ↓
Create ArticleCategory
```

This caused incorrect matches.

### Example

Article:

```text
Sanima Capital Limited (SANCAP) and Nepal Stock Exchange
signed an agreement for listing Sanima Equity Fund-2 (SAEF2).
```

Company:

```text
SGHL
Sanigad Hydro Limited
```

The article is **not about SGHL**.

However, the embedding similarity was:

```text
SGHL similarity = 0.49
```

This happens because both the article and company are related to general concepts such as:

- Nepal
- financial markets
- companies
- listing
- NEPSE
- securities
- investment

The embedding model recognizes semantic similarity but does not understand that:

```text
Sanima Capital
```

and:

```text
Sanigad Hydro
```

are different companies.

Therefore:

> **Embedding similarity should be treated as supporting evidence, not as the only company-identification mechanism.**

---

# Hybrid Matching Architecture

The new system works like this:

```text
                    Crawled Article
                          │
                          ▼
                ┌───────────────────┐
                │ Build Article Text│
                └─────────┬─────────┘
                          │
                          ▼
                Generate Article Vector
                          │
                          ▼
             ┌─────────────────────────┐
             │ Compare Against Company │
             │       Embeddings        │
             └────────────┬────────────┘
                          │
             ┌────────────┴────────────┐
             │                         │
             ▼                         ▼
       Exact Matching           Embedding Matching
             │                         │
       ┌─────┼─────┐                   │
       │     │     │                   │
       ▼     ▼     ▼                   ▼
    Symbol Name Alias             Cosine Similarity
       │     │     │                   │
       └─────┴─────┘                   │
             │                         │
             └──────────┬──────────────┘
                        ▼
                  Final Decision
                        │
                        ▼
                ArticleCategory
```

---

# Company Information

Each company should contain:

```python
{
    "symbol": "SGHL",
    "name": "Sanigad Hydro Limited",
    "sector": "Hydropower",
    "aliases": [
        "SGHL",
        "Sanigad Hydro",
        "Sanigad Hydropower",
        "Sanigad Hydro Limited",
    ],
    "description": (
        "Hydropower company in Nepal involved in "
        "hydroelectricity generation."
    ),
}
```

The company information is used for both:

- exact text matching
- embedding generation

---

# 1. Symbol Matching

The stock symbol is the strongest exact signal.

Examples:

```text
NABIL
NLIC
SHIVM
ICFC
SGHL
```

If:

```text
SGHL
```

appears in the article, there is strong evidence that the article is related to Sanigad Hydro.

### Symbol in headline

Higher confidence:

```text
SGHL announces new hydropower project
```

### Symbol in body

Still useful:

```text
The company, SGHL, announced...
```

---

# 2. Company Name Matching

The complete company name is also checked.

Example:

```text
Sanigad Hydro Limited
```

If it appears in the headline or body, the article can be associated with SGHL.

---

# 3. Alias Matching

Companies can have multiple names.

Example:

```text
SGHL
Sanigad Hydro
Sanigad Hydropower
Sanigad Hydro Limited
```

All of these should identify the same company.

This is especially important because news sources may use:

```text
Sanigad Hydro
```

instead of:

```text
Sanigad Hydro Limited
```

---

# 4. Headline Matching

A company mentioned in the headline is a strong signal.

For example:

```text
Nabil Bank reports strong quarterly earnings
```

The headline contains:

```text
Nabil Bank
```

Therefore the article is very likely related to Nabil Bank.

Headline matches receive a higher bonus than body matches.

Recommended weights:

| Match | Bonus |
|---|---:|
| Symbol in headline | +0.30 |
| Company name in headline | +0.30 |
| Alias in headline | +0.25 |
| Symbol in body | +0.20 |
| Company name in body | +0.20 |
| Alias in body | +0.15 |

These values can be adjusted after testing real articles.

---

# 5. Body Matching

The article body is also checked.

For example:

```text
The company announced that NABIL will...
```

Even if NABIL is not in the headline, the body provides explicit evidence.

Body matches receive a smaller bonus than headline matches because an article may mention a company without actually being primarily about it.

---

# 6. Embedding Similarity

The system still uses:

```text
sentence-transformers/all-MiniLM-L6-v2
```

Both company and article text are converted into vectors.

Example:

```text
Article
   ↓
384-dimensional vector

Company
   ↓
384-dimensional vector
```

Cosine similarity is then calculated:

```text
similarity = cosine(article_vector, company_vector)
```

However:

> Cosine similarity is not a probability.

A similarity of:

```text
0.49
```

does **not** mean:

```text
49% chance that the article is about the company.
```

It only means the two texts are semantically similar according to the embedding model.

---

# Why Embedding Similarity Is Secondary

Consider this article:

```text
Sanima Capital Limited (SANCAP)
and Nepal Stock Exchange signed an agreement
for listing Sanima Equity Fund-2 (SAEF2).
```

Compare against:

```text
SGHL
Sanigad Hydro Limited
Hydropower company in Nepal.
```

The embedding might return:

```text
0.49
```

But there is:

```text
Symbol match:  NO
Name match:    NO
Alias match:   NO
```

Therefore:

```text
SGHL → reject
```

Even though the embedding similarity is 0.49.

This prevents generic financial-market language from creating incorrect company categories.

---

# Embedding Contribution

The raw embedding score should not be added directly to the final score.

For example:

```text
0.49 embedding
```

should not automatically contribute:

```text
+0.49
```

because this gives embeddings too much influence.

Instead, the embedding score is converted into a smaller supporting score.

Recommended mapping:

| Raw Similarity | Embedding Contribution |
|---:|---:|
| < 0.50 | 0.00 |
| 0.50–0.59 | 0.05 |
| 0.60–0.69 | 0.10 |
| 0.70–0.79 | 0.20 |
| 0.80–0.89 | 0.30 |
| >= 0.90 | 0.40 |

This makes embedding similarity a supporting signal.

---

# Final Score

The final score is:

```text
final_score =
    exact_match_bonus
    +
    embedding_contribution
```

Example:

```text
Headline symbol match = +0.30
Embedding similarity  = 0.72
Embedding contribution = +0.20

Final score = 0.50
```

The exact values can be tuned later using real articles.

---

# Important Acceptance Rule

The most important rule is:

```text
                Company mentioned?
                       │
              ┌────────┴────────┐
              │                 │
             YES                NO
              │                 │
              ▼                 ▼
        Accept as exact      Check embedding
          entity match             │
                                   ▼
                          similarity >= 0.80?
                              │          │
                             YES         NO
                              │          │
                              ▼          ▼
                           Accept      Reject
```

Therefore:

### Exact company match

If a company symbol/name/alias appears:

```text
Accept
```

### No exact match

Only accept an embedding-only match when similarity is sufficiently high:

```text
embedding >= 0.80
```

This protects the system against false positives.

---

# Example 1 — Correct Match

Article:

```text
Nabil Bank Limited reports strong quarterly profit.
```

Company:

```text
NABIL
Nabil Bank Limited
```

Results:

```text
Symbol headline:  YES
Name headline:    YES
Embedding:        0.72
```

Result:

```text
ArticleCategory
company = NABIL
method = hybrid_headline
```

---

# Example 2 — Body Match

Article:

```text
The banking sector showed strong growth.

Nabil Bank Limited reported an increase in
quarterly earnings.
```

Results:

```text
Headline match: NO
Body match:     YES
Embedding:      0.68
```

Result:

```text
ArticleCategory
company = NABIL
method = hybrid_body
```

---

# Example 3 — False Embedding Match

Article:

```text
Sanima Capital Limited (SANCAP) signed an
agreement with NEPSE for listing SAEF2.
```

Company:

```text
SGHL
Sanigad Hydro Limited
```

Results:

```text
Headline match: NO
Body match:     NO
Embedding:      0.49
```

Because:

```text
0.49 < 0.80
```

the result is rejected.

```text
No ArticleCategory created.
```

This is the desired behavior.

---

# Example 4 — Strong Embedding-Only Match

Suppose an article does not explicitly mention the company name but its content is highly related:

```text
Hydropower producer announces increased
electricity generation and improved revenue...
```

And:

```text
Exact match:    NO
Embedding:      0.86
```

Since:

```text
0.86 >= 0.80
```

the system can create:

```text
ArticleCategory
method = embedding
```

This allows the system to find relevant articles even when the company name is not explicitly present.

---

# Word Boundary Matching

Exact matching should not simply use:

```python
if term in text:
```

because this can produce accidental matches.

Instead, use regular expressions:

```python
import re


def contains_term(self, text, term):
    if not term:
        return False

    pattern = rf"\b{re.escape(term.strip().lower())}\b"

    return bool(
        re.search(
            pattern,
            text,
            re.IGNORECASE,
        )
    )
```

This makes matching safer.

For example:

```text
SGHL
```

matches:

```text
SGHL announced...
```

but does not accidentally match an unrelated substring.

---

# Avoid Double Counting

Suppose the headline is:

```text
Nabil Bank Limited (NABIL) announces new results
```

The same company appears as:

```text
Nabil Bank Limited
Nabil
NABIL
```

Do not add:

```text
+0.30 symbol
+0.30 name
+0.25 alias
```

for a total of:

```text
+0.85
```

Instead, treat the headline as one strong entity match.

For example:

```text
Headline entity match = +0.30
```

This prevents the score from being artificially inflated.

---

# ArticleCategory Method

The `method` field should indicate how the company was identified.

Recommended values:

```text
exact_headline
exact_body
hybrid_headline
hybrid_body
embedding
```

Examples:

| Article | Company | Method |
|---|---|---|
| Nabil Bank announces profit | NABIL | hybrid_headline |
| Article mentions Nabil in body | NABIL | hybrid_body |
| Highly similar article without name | NABIL | embedding |

This makes debugging much easier.

---

# Recommended Database Information

An `ArticleCategory` record should ideally contain:

```text
article_id
company_id
confidence
method
```

If possible, also store:

```text
embedding_similarity
```

This is useful because:

```text
confidence
```

and:

```text
embedding_similarity
```

are different concepts.

For example:

```text
company: NABIL
confidence: 0.72
embedding_similarity: 0.49
method: hybrid_headline
```

This tells you that the article was accepted primarily because the company was explicitly identified, not because the embedding was highly similar.

---

# Recommended Thresholds

Initial values:

```text
Final threshold:
0.60

Embedding-only threshold:
0.80
```

However, these are starting points.

They should be adjusted after testing real articles.

Do not assume:

```text
0.70 = correct
```

or:

```text
0.49 = incorrect
```

Cosine similarity is model/data dependent.

The important distinction is:

```text
Explicit entity match
        >
Semantic similarity
```

for company identification.

---

# Complete Processing Flow

The final processing pipeline is:

```text
1. Crawl article
       │
       ▼
2. Save RawArticle
       │
       ▼
3. Build article text
       │
       ▼
4. Generate ArticleEmbedding
       │
       ▼
5. For every company:
       │
       ├── Check symbol
       ├── Check company name
       ├── Check aliases
       ├── Check headline
       ├── Check body
       └── Calculate embedding similarity
       │
       ▼
6. Calculate final score
       │
       ▼
7. Apply acceptance rules
       │
       ├── Exact match → accept
       │
       └── No exact match
              │
              └── embedding >= 0.80 → accept
       │
       ▼
8. Create ArticleCategory
       │
       ▼
9. Store confidence + method
```

---

# Why This Approach Is Better

The original system was:

```text
Article
   ↓
Embedding
   ↓
Similarity
   ↓
Category
```

The problem was:

```text
Semantic similarity ≠ company identity
```

The new system is:

```text
Article
   │
   ├── Explicit company identity
   │       ├── symbol
   │       ├── name
   │       └── alias
   │
   └── Semantic similarity
           └── embedding
```

This is better suited to financial news because many unrelated companies share generic terminology:

```text
NEPSE
shares
listing
trading
investment
bank
capital
fund
earnings
revenue
```

Embeddings can therefore produce false positives.

Explicit company matching provides the strong identity signal, while embeddings provide a fallback for articles where the company is described indirectly.

---

# Summary

The categorization system should follow these priorities:

```text
1. Symbol/name/alias in headline
        ↓
2. Symbol/name/alias in body
        ↓
3. High embedding similarity
        ↓
4. Reject weak embedding-only matches
```

The key rule is:

> **Do not allow a moderate embedding similarity such as 0.49 to identify a company by itself.**

For the SGHL example:

```text
SGHL embedding = 0.49
No SGHL symbol/name/alias found
        ↓
REJECT
```

For an article explicitly mentioning NABIL:

```text
NABIL found in headline
+
embedding similarity
        ↓
ACCEPT
```

This gives the system a much stronger foundation for accurate company-level news categorization.