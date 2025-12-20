---
layout: stele
title: Home
---

<div class="doc-header">
  <div class="classification">TRANSMISSION ACTIVE</div>
  <h1>stele</h1>
  <p class="subtitle">structured data format optimized for LLM consumption</p>
</div>

## The Problem

Every API call has a cost. Every token in that call adds to it.

**JSON burns tokens on ceremony:**

```json
{"users":[{"id":1,"name":"alice","role":"admin"},{"id":2,"name":"bob","role":"user"}]}
```

Quotes. Braces. Colons. Repeated keys. Every row repeats the same field names.

## The Solution

**stele encodes once, streams values:**

<div class="readout">
  <span class="readout-label">STELE OUTPUT</span>
@users|id^i|name^s|role^s
*1|alice|admin
*2|bob|user
</div>

Schema declared once. Data rows are pure values. **30-50% fewer tokens.**

---

## Design Philosophy

stele is built on one principle: **minimize tokens while maximizing model comprehension.**

| Goal | How |
|------|-----|
| Token efficiency | Eliminate JSON's syntactic overhead |
| Model parseability | Structure that LLMs extract accurately without examples |
| Schema compression | Declare field names once, reference by position |

Human readability is a secondary benefit, useful for debugging. But make no mistake: stele exists because every token costs money, and JSON burns tokens on ceremony.

---

## Quick Comparison

| Format | Haiku Accuracy | Tokens (50 records) |
|--------|----------------|---------------------|
| JSON | baseline | 6,757 |
| TOON | 59.8% | 8,744 (+29%) |
| stele | **100%** | **5,918 (-12%)** |

stele parses at parity with JSON while being smaller. Smaller models handle it cold.

---

<div style="text-align: center; margin: 3rem 0;">

## Read the Full Specification

<a href="{{ '/spec' | relative_url }}" style="display: inline-block; font-family: 'Cinzel', serif; font-size: 1.25rem; letter-spacing: 0.15em; padding: 1rem 2rem; border: 2px solid #4ECDC4; color: #4ECDC4; text-decoration: none; transition: all 0.3s ease;">
&#x1339D; ENTER THE TABLETS &#x1339E;
</a>

</div>

---

## Implementation

The reference implementation is [**base-d**](https://github.com/coryzibell/base-d), a Rust CLI and library.

```bash
# JSON to stele
echo '{"users":[{"id":1,"name":"alice"}]}' | base-d stele

# stele to JSON
echo '@users|id^i|name^s*1|alice' | base-d stele -d
```

---

## Related Formats

| Format | Model Reads Structure | Compression | Use Case |
|--------|----------------------|-------------|----------|
| **stele** | Yes | 30-50% | Working data |
| **carrier98** | No | 90-97% | Shuttle data |

They are siblings. Same family, different jobs.
