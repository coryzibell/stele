---
layout: default
title: Research
nav_order: 3
---

# Token Efficiency Research

This document outlines methodology for measuring stele's token efficiency compared to other formats.

## Goal

Prove that stele reduces API token consumption while maintaining model comprehension accuracy.

## Hypothesis

Stele ASCII achieves equivalent or better parsing accuracy with 30-50% fewer input tokens compared to JSON and markdown.

## Reference Implementation

All encoding tests use [base-d](https://github.com/coryzibell/base-d), the Rust reference implementation.

```bash
# JSON to stele ASCII
echo '{"users":[{"id":1,"name":"alice"}]}' | base-d stele -m ascii

# Markdown to stele ASCII
cat data.md | base-d stele -m ascii --markdown
```

## Formats Under Test

| Format | Description | Expected Tokens |
|--------|-------------|-----------------|
| JSON | Standard interchange format | Baseline |
| Markdown | Tables and documents | ~Similar to JSON |
| Stele ASCII | Schema-once, values-stream | 30-50% fewer |
| Stele Light | Unicode runic field tokens | Variable (unicode overhead) |

**Note:** ASCII mode is preferred for token efficiency because Unicode characters often tokenize to multiple tokens in BPE tokenizers.

## Token Measurement Methodology

### Source: Claude Code Session Logs

Claude Code stores detailed token usage in JSONL session files:

```
~/.claude/projects/{project}/{session-id}.jsonl
```

Each message includes usage data:

```json
{
  "message": {
    "usage": {
      "input_tokens": 1234,
      "cache_creation_input_tokens": 567,
      "cache_read_input_tokens": 8901,
      "output_tokens": 234
    }
  }
}
```

### Metrics to Extract

- `input_tokens` - Raw input token count (primary metric)
- `output_tokens` - Response length
- `cache_read_input_tokens` - Indicates repeated content

### Experiment Design

1. **Create test datasets** at varying sizes (10, 50, 100, 500 records)
2. **Encode each dataset** in JSON, Markdown table, and Stele ASCII
3. **Send identical prompts** to Claude API (e.g., "Extract field X from record Y")
4. **Log token counts** from session JSONL files
5. **Measure accuracy** - Did the model correctly parse and extract?
6. **Test across models** - Haiku, Sonnet, Opus

### Control Variables

- Same underlying data
- Same extraction prompts
- Same model version
- Fresh session (no cache effects for primary measurement)

## Preliminary Results

### Byte Compression (Proxy for Token Reduction)

| Source Format | Stele ASCII | Reduction |
|---------------|-------------|-----------|
| JSON (1409 bytes) | 589 bytes | **58%** |
| Markdown table (431 bytes) | 335 bytes | **22%** |

### Parse Accuracy

Tested with Claude (cold, no examples provided):

| Format | Haiku | Sonnet | Opus |
|--------|-------|--------|------|
| JSON | baseline | baseline | baseline |
| Stele ASCII | 100% | TBD | TBD |

*Haiku 100% accuracy from stele spec testing.*

## Next Steps

- [ ] Build automated test harness
- [ ] Generate standardized test datasets
- [ ] Run controlled experiments across model sizes
- [ ] Extract and analyze token counts from session logs
- [ ] Document findings for publication

## Publication Notes

Target: Joint paper on structured data formats optimized for LLM token efficiency.

**Authors:**
- kautau (coryzibell) - Format design, implementation
- Q (q@luola.observer) - Experiment design, analysis, validation

---

*Last updated: January 2026*
