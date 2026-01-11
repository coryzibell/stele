# Stele Benchmark Suite

Test framework for measuring LLM token efficiency and accuracy when using stele vs JSON/Markdown formats.

## Directory Structure

```
bench/
├── datasets/          # Test datasets
│   ├── flat/         # Flat JSON records (10, 50, 100, 500 users)
│   ├── nested/       # Nested JSON (shallow, medium, deep)
│   └── markdown/     # Markdown documents (headers, tables, mixed)
├── prompts/          # Test questions with expected answers
│   ├── flat/         # Questions for flat datasets
│   ├── nested/       # Questions for nested datasets
│   └── markdown/     # Questions for markdown datasets
├── encoded/          # Stele-encoded versions (generated)
├── sessions/         # LLM test sessions (gitignored)
├── results/          # Test results and analysis
└── tools/            # Benchmark scripts
```

## Datasets

### Flat Datasets
Consistent user schema with varying sizes:
- `10.json` - 10 users with named identities
- `50.json` - 50 users with named identities
- `100.json` - 100 users with named identities
- `500.json` - 500 users with numbered identities

Schema: `id, name, email, role (admin/user/moderator), active (bool)`

### Nested Datasets
Organization structure with increasing depth:
- `shallow.json` - 2 levels (org -> departments)
- `medium.json` - 3 levels (org -> departments -> teams)
- `deep.json` - 4+ levels (org -> departments -> teams -> members -> skills)

### Markdown Datasets
Realistic documentation examples:
- `headers.md` - h1->h2->h3->h4 hierarchy with content
- `tables.md` - Multiple markdown tables (pricing, features, limits)
- `mixed.md` - Headers + tables + lists + code blocks (API guide)

## Prompts

Each dataset has corresponding prompt file with:
- Questions testing comprehension, counting, filtering, lookups
- Expected answers for accuracy measurement
- 10 questions per dataset

## Usage

1. **Encode datasets**: Convert JSON/Markdown to stele format
2. **Run tests**: Send both formats to LLM with prompts
3. **Measure**: Compare token usage and answer accuracy
4. **Analyze**: Generate report on efficiency gains

## Data Characteristics

- **Deterministic**: Seeded data for reproducibility
- **Realistic**: Credible schemas and content for research
- **Varied**: Tests flat, nested, and document structures
- **Comprehensive**: Edge cases and common patterns

## Phase Status

- [x] Phase 1: Dataset creation (COMPLETE)
- [ ] Phase 2: Encoding tools
- [ ] Phase 3: Test harness
- [ ] Phase 4: Analysis and reporting
