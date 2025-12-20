---
layout: stele
title: stele
---

<div class="doc-header">
  <div class="classification">MODEL-READABLE</div>
  <h1>stele</h1>
  <p class="subtitle">structured data format optimized for LLM consumption</p>
  <div class="doc-meta">
    <div class="meta-field">
      <span class="meta-label">Document</span>
      <span class="meta-value">STELE-SPEC-001</span>
    </div>
    <div class="meta-field">
      <span class="meta-label">Revision</span>
      <span class="meta-value">1.8</span>
    </div>
    <div class="meta-field">
      <span class="meta-label">Status</span>
      <span class="meta-value"><span class="stamp stamp-go">APPROVED</span></span>
    </div>
  </div>
</div>

## Abstract

**stele** is a structured data format optimized for LLM consumption. The goal is simple: **fewer tokens, less money.**

JSON wastes tokens on syntax—quotes, braces, colons, repeated keys. stele eliminates this overhead while keeping data parseable by models. Where carrier98 is opaque (maximum density, the model shuttles without parsing), stele is transparent—the model reads and reasons over the structure directly.

Human readability is a secondary benefit, useful for debugging and inspection. But make no mistake: stele exists because every token costs money, and JSON burns tokens on ceremony.

<div class="readout">
  <span class="readout-label">EXAMPLE OUTPUT</span>
@ᚠ=video,ᚡ=id,ᚢ=title,ᚣ=tags
 ᚠ჻ᚡˢ┃ᚠ჻ᚢˢ┃ᚣˢ⟦⟧▓◉dQw4w9WgXcQ┃Never▓Gonna▓Give▓You▓Up┃music◈80s
</div>
<details>
<summary>Expanded (human-readable field names)</summary>

```
@┃video჻idˢ┃video჻titleˢ┃tagsˢ⟦⟧▓◉dQw4w9WgXcQ┃Never▓Gonna▓Give▓You▓Up┃music◈80s
```
</details>

---

## Design Philosophy

Every API call has a cost. Every token in that call adds to it. stele is designed around one principle: **minimize tokens while maximizing model comprehension.**

**Primary goals:**
- **Token efficiency** — Eliminate JSON's syntactic overhead
- **Model parseability** — Structure that LLMs extract accurately without examples
- **Schema compression** — Declare field names once, reference by position

**Secondary benefits:**
- Human-scannable for debugging
- Grep-friendly for quick inspection
- No escaping needed—quotes, braces, newlines are just content

> The format is optimized for the machine that costs money to run. Human readability comes along for the ride.

---

## Delimiter Specification

| Symbol | Unicode | Name | Purpose |
|--------|---------|------|---------|
| `@` | U+0040 | At sign | Schema line start |
| `◉` | U+25C9 | Fisheye | Row start marker |
| `┃` | U+2503 | Heavy vertical | Field separator |
| `჻` | U+10FB | Georgian comma | Nested path separator |
| `◈` | U+25C8 | Diamond in diamond | Primitive array element separator |
| `∅` | U+2205 | Empty set | Null value |
| `▓` | U+2593 | Dark shade | Minified space |
| `⟦` `⟧` | U+27E6 U+27E7 | Mathematical brackets | Array type markers |
| `,` `=` | U+002C U+003D | Comma, equals | Metadata key-value pairs |

**Type markers** (superscript, single character):

| Symbol | Unicode | Type |
|--------|---------|------|
| `ˢ` | U+02E2 | string |
| `ⁱ` | U+2071 | integer |
| `ᶠ` | U+1DA0 | float |
| `ᵇ` | U+1D47 | boolean |

Type markers replace the verbose `:str`, `:int`, `:float`, `:bool` annotations. Example: `nameˢ` instead of `name:str`.

These characters were chosen for:
- **Rarity**: Almost never appear in real data
- **Visibility**: Distinct at a glance
- **Single-token**: Most tokenizers encode each as one unit

> **Note on the field separator:** The heavy vertical `┃` (U+2503) is *not* the standard pipe `|` (U+007C). Compare them side by side: `┃` vs `|`. The heavy vertical is thicker and extends the full line height. This distinction matters—the standard pipe appears frequently in code and shell commands, while the heavy vertical is rare enough to serve as an unambiguous delimiter.

---

## Array Flattening

stele handles nested structures and arrays by flattening them into indexed paths using the Georgian comma `჻` as the path separator.

### Primitive Arrays (Inline)

Arrays of primitives (strings, numbers, booleans) use the diamond separator `◈` for compact inline representation:

<div class="readout">
  <span class="readout-label">PRIMITIVE ARRAY</span>
@ᚠ=tags
ᚠˢ⟦⟧
◉music◈80s◈classic
</div>
<details>
<summary>Expanded</summary>

```
@┃tagsˢ⟦⟧
◉music◈80s◈classic
```
</details>

**Equivalent JSON:**
```json
{
  "tags": ["music", "80s", "classic"]
}
```

The `tagsˢ⟦⟧` schema declares an array of strings. Values are joined with `◈`. This is more compact than indexed paths for primitive arrays.

### Arrays of Objects (Indexed Paths)

Arrays containing objects use indexed paths with the Georgian comma `჻`:

<div class="readout">
  <span class="readout-label">ARRAY OF OBJECTS</span>
@ᚠ=video,ᚡ=id,ᚢ=title,ᚣ=tags,ᚤ=comments,ᚥ=author,ᚦ=text
ᚠ჻ᚡˢ┃ᚠ჻ᚢˢ┃ᚣˢ⟦⟧┃ᚤ჻0჻ᚥˢ┃ᚤ჻0჻ᚦˢ┃ᚤ⟦⟧
◉dQw4w9WgXcQ┃Never▓Gonna▓Give▓You▓Up┃music◈80s┃alice┃Great!┃∅
</div>
<details>
<summary>Expanded</summary>

```
@┃video჻idˢ┃video჻titleˢ┃tagsˢ⟦⟧┃comments჻0჻authorˢ┃comments჻0჻textˢ┃comments⟦⟧
◉dQw4w9WgXcQ┃Never▓Gonna▓Give▓You▓Up┃music◈80s┃alice┃Great!┃∅
```
</details>

**Equivalent JSON:**
```json
{
  "video": {
    "id": "dQw4w9WgXcQ",
    "title": "Never Gonna Give You Up"
  },
  "tags": ["music", "80s"],
  "comments": [
    {
      "author": "alice",
      "text": "Great!"
    }
  ]
}
```

### Nested Arrays

Arrays within arrays work naturally:

<div class="readout">
  <span class="readout-label">NESTED ARRAYS</span>
@ᚠ=comments,ᚡ=replies,ᚢ=author
ᚠ჻0჻ᚡ჻0჻ᚢˢ┃ᚠ჻0჻ᚡ჻1჻ᚢˢ┃ᚠ჻1჻ᚡ჻0჻ᚢˢ┃ᚠ⟦⟧┃ᚠ჻0჻ᚡ⟦⟧┃ᚠ჻1჻ᚡ⟦⟧▓◉alice┃bob┃carol┃∅┃∅┃∅
</div>
<details>
<summary>Expanded</summary>

```
@┃comments჻0჻replies჻0჻authorˢ┃comments჻0჻replies჻1჻authorˢ┃comments჻1჻replies჻0჻authorˢ┃comments⟦⟧┃comments჻0჻replies⟦⟧┃comments჻1჻replies⟦⟧▓◉alice┃bob┃carol┃∅┃∅┃∅
```
</details>

**Path syntax:**
- `comments჻0` — First comment
- `comments჻0჻replies჻0` — First reply to first comment
- `comments჻0჻replies჻1` — Second reply to first comment

**Array markers:**
- `comments⟦⟧` — Top-level array marker
- `comments჻0჻replies⟦⟧` — Nested array marker

All array markers have `∅` values and exist solely for decoder metadata.

### Complex Nesting: Where stele Shines

Real-world API responses often have deeply nested structures—arrays of objects containing arrays of objects. This is where many formats fail. stele handles it naturally.

**Example: YouTube-style API response**

```json
{
  "video": {
    "id": "dQw4w9WgXcQ",
    "title": "Never Gonna Give You Up",
    "views": 1500000000
  },
  "comments": [
    {
      "author": "alice",
      "text": "Classic!",
      "replies": [
        {"author": "bob", "text": "Agreed!"},
        {"author": "carol", "text": "Never gets old"}
      ]
    },
    {
      "author": "dave",
      "text": "Still watching in 2024",
      "replies": ⟦⟧
    }
  ]
}
```

**stele output:**

<div class="readout">
  <span class="readout-label">DEEPLY NESTED STRUCTURE</span>
@ᚠ=video,ᚡ=id,ᚢ=title,ᚣ=views,ᚤ=comments,ᚥ=author,ᚦ=text,ᚧ=replies
ᚠ჻ᚡˢ┃ᚠ჻ᚢˢ┃ᚠ჻ᚣⁱ┃ᚤ჻0჻ᚥˢ┃ᚤ჻0჻ᚦˢ┃ᚤ჻0჻ᚧ჻0჻ᚥˢ┃ᚤ჻0჻ᚧ჻0჻ᚦˢ┃ᚤ჻0჻ᚧ჻1჻ᚥˢ┃ᚤ჻0჻ᚧ჻1჻ᚦˢ┃ᚤ჻1჻ᚥˢ┃ᚤ჻1჻ᚦˢ┃ᚤ⟦⟧┃ᚤ჻0჻ᚧ⟦⟧┃ᚤ჻1჻ᚧ⟦⟧▓◉dQw4w9WgXcQ┃Never▓Gonna▓Give▓You▓Up┃1500000000┃alice┃Classic!┃bob┃Agreed!┃carol┃Never▓gets▓old┃dave┃Still▓watching▓in▓2024┃∅┃∅┃∅
</div>
<details>
<summary>Expanded</summary>

```
@┃video჻idˢ┃video჻titleˢ┃video჻viewsⁱ┃comments჻0჻authorˢ┃comments჻0჻textˢ┃comments჻0჻replies჻0჻authorˢ┃comments჻0჻replies჻0჻textˢ┃comments჻0჻replies჻1჻authorˢ┃comments჻0჻replies჻1჻textˢ┃comments჻1჻authorˢ┃comments჻1჻textˢ┃comments⟦⟧┃comments჻0჻replies⟦⟧┃comments჻1჻replies⟦⟧▓◉dQw4w9WgXcQ┃Never▓Gonna▓Give▓You▓Up┃1500000000┃alice┃Classic!┃bob┃Agreed!┃carol┃Never▓gets▓old┃dave┃Still▓watching▓in▓2024┃∅┃∅┃∅
```
</details>

**Key observations:**
- `comments჻0჻replies჻1჻author` — Four levels deep, completely unambiguous
- `comments჻1჻replies⟦⟧` — Empty array preserved via marker
- Every path is explicit—no counting indentation or tracking state
- **Round-trips perfectly**—decode produces identical JSON

**Cold parse test:** We gave this to Haiku with zero format explanation and asked: *"Who replied to the first comment?"* Answer: *"bob and carol"*. Correct.

This is the complexity level where whitespace-based formats break down. Stele handles it because structure is encoded in the path, not inferred from layout.

### Try It Yourself: Model Cold Parse Test

Copy this stele data and paste it to any LLM with the questions below. No format explanation needed.

<div class="readout">
  <span class="readout-label">COPY THIS</span>
@┃org჻foundedⁱ┃org჻nameˢ┃teams჻0჻leadˢ┃teams჻0჻members჻0჻nameˢ┃teams჻0჻members჻0჻skillsˢ⟦⟧┃teams჻0჻members჻1჻nameˢ┃teams჻0჻members჻1჻skillsˢ⟦⟧┃teams჻0჻nameˢ┃teams჻1჻leadˢ┃teams჻1჻members჻0჻nameˢ┃teams჻1჻members჻0჻skillsˢ⟦⟧┃teams჻1჻nameˢ┃teams⟦⟧┃teams჻0჻members⟦⟧┃teams჻1჻members⟦⟧
◉2019┃Acme▓Corp┃alice┃bob┃rust◈python┃carol┃go┃Engineering┃dave┃eve┃figma◈css◈animation┃Design┃∅┃∅┃∅

Questions:
1. What skills does bob have?
2. Who leads the Design team?
3. How many members are on the Engineering team?
4. What is eve's third skill?
</div>

**Expected answers:**
1. rust, python
2. dave
3. 2 (bob and carol)
4. animation

If your model answers correctly with zero prompting about the format, stele works for your use case.

### Try It Yourself: Tokenized Version

Same test, but with field names tokenized to runic characters and superscript type markers. The token map is in the first line. Can your model still parse it cold?

<div class="readout">
  <span class="readout-label">COPY THIS (TOKENIZED)</span>
@ᚠ=org,ᚡ=founded,ᚢ=name,ᚣ=teams,ᚤ=lead,ᚥ=members,ᚦ=skills
ᚠ჻ᚡⁱ┃ᚠ჻ᚢˢ┃ᚣ჻0჻ᚤˢ┃ᚣ჻0჻ᚥ჻0჻ᚢˢ┃ᚣ჻0჻ᚥ჻0჻ᚦˢ⟦⟧┃ᚣ჻0჻ᚥ჻1჻ᚢˢ┃ᚣ჻0჻ᚥ჻1჻ᚦˢ⟦⟧┃ᚣ჻0჻ᚢˢ┃ᚣ჻1჻ᚤˢ┃ᚣ჻1჻ᚥ჻0჻ᚢˢ┃ᚣ჻1჻ᚥ჻0჻ᚦˢ⟦⟧┃ᚣ჻1჻ᚢˢ┃ᚣ⟦⟧┃ᚣ჻0჻ᚥ⟦⟧┃ᚣ჻1჻ᚥ⟦⟧
◉2019┃Acme▓Corp┃alice┃bob┃rust◈python┃carol┃go┃Engineering┃dave┃eve┃figma◈css◈animation┃Design┃∅┃∅┃∅

Questions:
1. What skills does bob have?
2. Who leads the Design team?
3. How many members are on the Engineering team?
4. What is eve's third skill?
</div>

**Expected answers:** Same as above. If your model handles both versions identically, tokenization is safe for your use case.

Here's the equivalent JSON for comparison—same data, same structure:

```json
{"org":{"founded":2019,"name":"Acme Corp"},"teams":[{"lead":"alice","members":[{"name":"bob","skills":["rust","python"]},{"name":"carol","skills":["go"]}],"name":"Engineering"},{"lead":"dave","members":[{"name":"eve","skills":["figma","css","animation"]}],"name":"Design"}]}
```

> **Note on size:** For single complex records, stele's schema overhead can exceed JSON. The savings come with multiple rows of similar structure—see [Context Efficiency](#context-efficiency) for benchmarks showing 30-50% reduction on typical datasets.

### Large Dataset Test: Service Logs

This example demonstrates stele with 16 rows of nested log data. The schema is declared once; data rows are pure values.

<div class="readout">
  <span class="readout-label">COPY THIS (16 ROWS)</span>
@logs┃levelˢ┃messageˢ┃service჻instanceˢ┃service჻nameˢ┃timestampⁱ
◉info┃Request▓received┃us-east-1a┃api┃1701590400
◉debug┃Parsing▓payload┃us-east-1a┃api┃1701590401
◉info┃Auth▓validated┃us-east-1a┃api┃1701590402
◉warn┃Slow▓query▓detected┃us-east-1b┃db┃1701590403
◉info┃Response▓sent┃us-east-1a┃api┃1701590404
◉error┃Connection▓timeout┃us-east-1b┃db┃1701590405
◉info┃Cache▓hit┃us-east-1c┃cache┃1701590406
◉debug┃Middleware▓executed┃us-east-1a┃api┃1701590407
◉info┃Request▓completed┃us-east-1a┃api┃1701590408
◉warn┃Cache▓miss┃us-east-1c┃cache┃1701590409
◉info┃Query▓executed┃us-east-1b┃db┃1701590410
◉debug┃Response▓formatted┃us-east-1a┃api┃1701590411
◉info┃Metrics▓recorded┃us-east-1a┃api┃1701590412
◉error┃Redis▓disconnect┃us-east-1c┃cache┃1701590413
◉info┃Reconnected┃us-east-1b┃db┃1701590414
◉info┃Health▓check▓OK┃us-east-1a┃api┃1701590415

Questions:
1. How many error-level logs are there?
2. Which service had the "Slow query detected" warning?
3. What instance is the cache service running on?
4. What was the last message from the db service?
</div>

**Expected answers:**
1. 2 (Connection timeout, Redis disconnect)
2. db
3. us-east-1c
4. Reconnected

**Size comparison:**
- JSON: 2,138 bytes
- stele: 1,054 bytes (51% reduction)

With 16 rows sharing the same schema, stele cuts size in half. The schema overhead is amortized across all rows.

### Why This Hybrid Approach?

stele uses two strategies for arrays:

| Array Type | Strategy | Example |
|------------|----------|---------|
| Primitives | Inline with `◈` | `tagsˢ⟦⟧` → `music◈80s◈classic` |
| Objects | Indexed paths | `comments჻0჻authorˢ` → indexed fields |

**Benefits:**
- Primitive arrays are compact—no schema bloat for simple lists
- Object arrays have explicit structure—no ambiguity about nesting levels
- Paths are self-documenting (`comments჻0჻replies჻1` reads naturally)
- Array boundaries are clear from path prefixes or `⟦⟧` markers
- Single token for each separator (Georgian comma `჻` and diamond `◈` are rare in content)

> **Note:** The Georgian comma `჻` (U+10FB) was chosen for its visibility and rarity. It's distinct at a glance and almost never appears in real data.

---

## Field Name Tokenization

For maximum compression, stele can tokenize field names using single Unicode characters from ancient scripts. This reduces schema overhead while remaining regex-safe—no ASCII, no digits, no modern text patterns.

### Token Alphabet

Tokens are assigned from these Unicode ranges in order:

| Priority | Script | Range | Count | Plane |
|----------|--------|-------|-------|-------|
| 1 | Runic | U+16A0 – U+16F8 | 89 | BMP |
| 2 | Egyptian Hieroglyphs | U+13000 – U+1342F | 1072 | SMP |
| 3 | Cuneiform | U+12000 – U+123FF | 1024 | SMP |

**Why this order:**
- **Runic first**: Basic Multilingual Plane (BMP) means 2-byte UTF-8, better compatibility across systems
- **Hieroglyphs/Cuneiform overflow**: Supplementary Multilingual Plane (SMP) requires 4-byte UTF-8, used only for schemas with 90+ fields

89 runic characters cover the vast majority of real-world schemas.

### Token Map Syntax

The schema line includes a token map in the metadata section:

```
@ᚠ=video,ᚡ=id,ᚢ=title,ᚣ=comments,ᚤ=author,ᚥ=text,ᚦ=replies
ᚠ჻ᚡˢ┃ᚠ჻ᚢˢ┃ᚣ჻0჻ᚤˢ┃ᚣ჻0჻ᚥˢ┃ᚣ჻0჻ᚦ჻0჻ᚤˢ┃...
```

**Format:** `@` followed by comma-separated `token=fieldname` pairs, then the schema fields with superscript type markers.

### Example: Tokenized vs Untokenized

**Untokenized (readable):**
```
@┃video჻idˢ┃video჻titleˢ┃comments჻0჻authorˢ┃comments჻0჻textˢ
◉dQw4w9WgXcQ┃Never▓Gonna▓Give▓You▓Up┃alice┃Classic!
```

**Tokenized (compact):**
```
@ᚠ=video,ᚡ=id,ᚢ=title,ᚣ=comments,ᚤ=author,ᚥ=text
ᚠ჻ᚡˢ┃ᚠ჻ᚢˢ┃ᚣ჻0჻ᚤˢ┃ᚣ჻0჻ᚥˢ
◉dQw4w9WgXcQ┃Never▓Gonna▓Give▓You▓Up┃alice┃Classic!
```

Data rows are unchanged—only schema field names are tokenized.

### Why Ancient Scripts?

| Requirement | Solution |
|-------------|----------|
| No ASCII collision | Ancient scripts contain no Latin, digits, or punctuation |
| No regex match | `\w`, `[a-zA-Z0-9]`, `\d` won't match runic/hieroglyphs |
| No delimiter collision | Scripts don't include `┃`, `჻`, `◈`, `⟦⟧`, etc. |
| Model parseability | Tested: Haiku parses tokenized schemas cold with 100% accuracy |
| Visual distinction | Immediately obvious these are tokens, not data |

### Tokenization Rules

1. **Collect unique field names** from flattened schema paths
2. **Assign tokens** starting at ᚠ (U+16A0), incrementing through runic
3. **Overflow to hieroglyphs** at 𓀀 (U+13000) if runic exhausted
4. **Overflow to cuneiform** at 𒀀 (U+12000) if hieroglyphs exhausted
5. **Exclude from tokenization:**
   - Array indices (remain as digits: `჻0჻`, `჻1჻`)
   - Type annotations (`:str`, `:int`, etc.)
   - Array markers (`⟦⟧`)

### Constraints

**DO NOT use as tokens:**
- ASCII characters (0x00–0x7F)
- Digits in any script
- stele delimiters (`◉`, `┃`, `჻`, `◈`, `∅`, `▓`, `⟦`, `⟧`)
- Common Unicode punctuation

**Numeric tokens break parsing.** Array indices use digits (`჻0჻`, `჻1჻`), so numeric tokens like `1=field` create ambiguity in paths like `1჻0჻2`—is `1` a token or index? Ancient scripts avoid this entirely.

### CLI Flags

```bash
# Full compression (default) - field + value tokenization
base-d stele encode input.json
base-d stele encode --level full input.json

# Light compression - field tokenization only
base-d stele encode --level light input.json

# No compression - human-readable
base-d stele encode --level none input.json

# Multiline output (any level)
base-d stele encode --multiline input.json
```

---

## Value Dictionary (v1.8)

Field name tokenization compresses the schema header. But what about repeated **values**? Log levels (`info`, `error`), status codes (`active`, `pending`), enum-like fields—these repeat across rows but aren't compressed.

Value dictionaries extend tokenization to data values using a separate Unicode block: **Egyptian Hieroglyphs**.

### Dual Dictionary Design

| Dictionary | Script | Range | Purpose |
|------------|--------|-------|---------|
| Field names | Runic | U+16A0–U+16F8 | Schema paths |
| Values | Hieroglyphs | U+13000–U+1342F | Repeated data values |

The visual distinction is immediate—runic tokens appear in schema position, hieroglyphs appear in value position. No ambiguity.

### Syntax

Two `@` lines before the schema:

```
@ᚠ=level,ᚡ=message,ᚢ=service჻instance,ᚣ=service჻name,ᚤ=timestamp
@𓀀=info,𓀁=debug,𓀂=error,𓀃=warn,𓀄=api,𓀅=db,𓀆=cache,𓀇=us-east-1a
@logs┃ᚠˢ┃ᚡˢ┃ᚢˢ┃ᚣˢ┃ᚤⁱ
◉𓀀┃Request▓received┃𓀇┃𓀄┃1701590400
◉𓀂┃Connection▓timeout┃𓀈┃𓀅┃1701590405
```

- **Line 1**: Field name dictionary (runic)
- **Line 2**: Value dictionary (hieroglyphs)
- **Line 3**: Schema with tokenized field names
- **Line 4+**: Data rows with tokenized values

### Detection

Parsers distinguish dictionaries by the first character after `@`:

```rust
fn is_field_token(c: char) -> bool { ('\u{16A0}'..='\u{16F8}').contains(&c) }
fn is_value_token(c: char) -> bool { ('\u{13000}'..='\u{1342F}').contains(&c) }
```

- `@ᚠ=...` → Field dictionary (runic first char)
- `@𓀀=...` → Value dictionary (hieroglyph first char)
- `@logs┃...` → Schema line (ASCII first char)

### Encoding Rules

1. **Scan all values** across all rows
2. **Count frequency** of each unique value
3. **Tokenize values** appearing 2+ times (configurable threshold)
4. **Assign hieroglyphs** starting at 𓀀 (U+13000)
5. **Emit value dictionary** after field dictionary, before schema

**Exclude from value tokenization:**
- Numeric values (timestamps, IDs, counts)
- Unique strings (messages, names)
- Values appearing only once

### Example: Service Logs

16 log entries with repeated levels, services, and instances:

<div class="readout">
  <span class="readout-label">WITH VALUE DICTIONARY</span>
@ᚠ=level,ᚡ=message,ᚢ=service჻instance,ᚣ=service჻name,ᚤ=timestamp
@𓀀=info,𓀁=debug,𓀂=error,𓀃=warn,𓀄=api,𓀅=db,𓀆=cache,𓀇=us-east-1a,𓀈=us-east-1b,𓀉=us-east-1c
@logs┃ᚠˢ┃ᚡˢ┃ᚢˢ┃ᚣˢ┃ᚤⁱ
◉𓀀┃Request▓received┃𓀇┃𓀄┃1701590400
◉𓀁┃Parsing▓payload┃𓀇┃𓀄┃1701590401
◉𓀀┃Auth▓validated┃𓀇┃𓀄┃1701590402
◉𓀃┃Slow▓query▓detected┃𓀈┃𓀅┃1701590403
◉𓀀┃Response▓sent┃𓀇┃𓀄┃1701590404
◉𓀂┃Connection▓timeout┃𓀈┃𓀅┃1701590405
◉𓀀┃Cache▓hit┃𓀉┃𓀆┃1701590406
◉𓀁┃Middleware▓executed┃𓀇┃𓀄┃1701590407
◉𓀀┃Request▓completed┃𓀇┃𓀄┃1701590408
◉𓀃┃Cache▓miss┃𓀉┃𓀆┃1701590409
◉𓀀┃Query▓executed┃𓀈┃𓀅┃1701590410
◉𓀁┃Response▓formatted┃𓀇┃┃𓀄1701590411
◉𓀀┃Metrics▓recorded┃𓀇┃𓀄┃1701590412
◉𓀂┃Redis▓disconnect┃𓀉┃𓀆┃1701590413
◉𓀀┃Reconnected┃𓀈┃𓀅┃1701590414
◉𓀀┃Health▓check▓OK┃𓀇┃𓀄┃1701590415

Questions:
1. How many error-level logs are there?
2. Which service had the "Slow query detected" warning?
3. What instance is the cache service running on?
4. What was the last message from the db service?
</div>

**Expected answers:**
1. 2 (Connection timeout, Redis disconnect)
2. db
3. us-east-1c
4. Reconnected

**Cold parse test:** Haiku answered all 4 correctly with zero format explanation. It recognized both dictionaries, decoded the hieroglyph tokens, and traversed the data accurately.

### Size Impact

For datasets with repeated categorical values:

| Scenario | Without Value Dict | With Value Dict | Savings |
|----------|-------------------|-----------------|---------|
| 16 logs, 4 levels, 3 services | 1,054 bytes | ~850 bytes | ~20% |
| 100 logs, same categories | ~6,500 bytes | ~4,800 bytes | ~26% |
| 1000 logs, enum-heavy | ~65,000 bytes | ~42,000 bytes | ~35% |

The more rows and the more repetition, the greater the savings.

### CLI Usage

See [CLI Flags](#cli-flags) above. Full compression (`--level full`) is the default.

---

## Model Accuracy: stele vs TOON

We benchmarked stele against [TOON](https://github.com/toon-format/toon)'s published results using the same GitHub repositories dataset (top repositories by stars).

### Haiku Retrieval Accuracy

TOON's benchmark showed Haiku struggling with their whitespace-based format:

| Format | TOON Benchmark | stele Benchmark |
|--------|----------------|-----------------|
| Accuracy | 59.8% (125/209) | **100%** (10/10 complex queries) |
| Format explanation | Required | None (cold parse) |

We tested stele with 10 complex retrieval questions including aggregations, sorting, filtering, ratio calculations, and counting—all answered correctly by Haiku with zero format explanation.

### Why the Difference?

**TOON** uses whitespace indentation for structure. Smaller models struggle to:
- Track indentation depth accurately
- Distinguish significant whitespace from formatting
- Parse collapsed/minified content (impossible with TOON)

**stele** uses explicit Unicode delimiters (`◉`, `┃`, `▓`, `჻`). Models can:
- Count visible characters reliably
- Parse structure without inferring from spacing
- Handle minified single-string format identically to expanded
- Follow explicit path-based nesting (`comments჻0჻replies჻1`)

### Token Efficiency Comparison

Using TOON's GitHub repos benchmark data (50 records):

| Format | Tokens | vs JSON |
|--------|--------|---------|
| JSON | 6,757 | baseline |
| TOON | ~8,744 | +29% worse |
| stele | 5,918 | **-12.4% better** |

On flat tabular data, stele outperforms both JSON and TOON. TOON's strength is mixed nested structures—but stele handles those too with path flattening.

### The Full Picture

| Capability | stele | TOON |
|------------|-------|------|
| Flat tabular | -12% tokens | +6% overhead |
| Nested structures | ✓ (path flattening) | ✓ (indentation) |
| Deep nesting (5+ levels) | ✓ stable | degrades |
| Minifiable | ✓ single string | ✗ whitespace required |
| Haiku accuracy | 100% cold | 59.8% |
| Human readability | good | better |

stele fills an unclaimed niche: **nested + minifiable + token-efficient + small-model-friendly**.

### stele vs JSON Parsing Parity

We tested whether stele degrades model comprehension compared to raw JSON. Using 10 users with nested objects (address, company, geo coordinates) plus metadata:

| Format | Size | Parsing Errors | Reasoning Errors |
|--------|------|----------------|------------------|
| JSON | 4,170 bytes | 0 | 2 |
| stele | 3,117 bytes | 0 | 2 |

Both formats produced identical parsing results. The reasoning errors (finding minimum values, pattern matching) occurred on *both* formats with different wrong answers—indicating model reasoning limits, not format comprehension issues.

**Conclusion:** stele parses at parity with JSON while being 25% smaller.

[Try it yourself →](benchmarks/)

---

## Format Structure

### Schema Declaration

```
@{root_key}┃{field}:{type}┃{field}:{type}...
```

The schema line begins with `@`, optionally followed by a root key (the JSON wrapper object name), then field definitions separated by `┃`.

**Supported types:**
- `int` — Integer values
- `float` — Floating point values
- `str` — String values
- `bool` — Boolean values (`true`/`false`)
- `{type}⟦⟧` — Array of type (e.g., `str⟦⟧`, `int⟦⟧`)

### Data Rows

```
◉{value}┃{value}┃{value}...
```

Each row begins with `◉`, followed by values in schema order, separated by `┃`.

### Header Metadata

When JSON has scalar fields alongside an array, stele extracts them as header metadata:

```
@{root_key}[{key}={value},{key}={value}]┃{field}{type}...
```

<div class="readout">
  <span class="readout-label">API RESPONSE WITH METADATA</span>
@ᚠ=students,ᚡ=id,ᚢ=name,ᚣ=grade
ᚠ[class=Year▓1,school_name=Springfield▓High]┃ᚡˢ┃ᚢˢ┃ᚣⁱ▓◉A1┃alice┃95▓◉B2┃bob┃87▓◉C3┃carol┃92
</div>
<details>
<summary>Expanded</summary>

```
@students[class=Year▓1,school_name=Springfield▓High]┃idˢ┃nameˢ┃gradeⁱ▓◉A1┃alice┃95▓◉B2┃bob┃87▓◉C3┃carol┃92
```
</details>

**Equivalent JSON:**
```json
{
  "school_name": "Springfield High",
  "class": "Year 1",
  "students": [
    {"id": "A1", "name": "alice", "grade": 95},
    {"id": "B2", "name": "bob", "grade": 87},
    {"id": "C3", "name": "carol", "grade": 92}
  ]
}
```

**Rules:**
- Metadata keys are bare (no spaces)
- Metadata values use `▓` for spaces
- Keys sorted alphabetically for deterministic output
- Only extracted when JSON has scalar fields + exactly one array of objects

This pattern is common in API responses (`{count, next, results: [...]}`) where pagination or context metadata wraps the main data.

---

## Examples

### Simple Record Set

<div class="readout">
  <span class="readout-label">STELE FORMAT</span>
@ᚠ=crew,ᚡ=id,ᚢ=name,ᚣ=role
ᚠ┃ᚡⁱ┃ᚢˢ┃ᚣˢ▓◉1┃Glenn┃Pilot▓◉2┃Carpenter┃Pilot▓◉3┃Johnson┃Computer
</div>
<details>
<summary>Expanded</summary>

```
@crew┃idⁱ┃nameˢ┃roleˢ▓◉1┃Glenn┃Pilot▓◉2┃Carpenter┃Pilot▓◉3┃Johnson┃Computer
```
</details>

**Equivalent JSON:**
```json
{"crew":[
  {"id":1,"name":"Glenn","role":"Pilot"},
  {"id":2,"name":"Carpenter","role":"Pilot"},
  {"id":3,"name":"Johnson","role":"Computer"}
]}
```

### With Arrays

<div class="readout">
  <span class="readout-label">STELE FORMAT</span>
@ᚠ=missions,ᚡ=name,ᚢ=crew
ᚠ჻ᚡˢ┃ᚠ჻ᚢˢ⟦⟧┃ᚠ⟦⟧▓◉Mercury-Atlas▓6┃Glenn┃∅▓◉Apollo▓11┃Armstrong◈Aldrin◈Collins┃∅
</div>
<details>
<summary>Expanded</summary>

```
@┃missions჻nameˢ┃missions჻crewˢ⟦⟧┃missions⟦⟧▓◉Mercury-Atlas▓6┃Glenn┃∅▓◉Apollo▓11┃Armstrong◈Aldrin◈Collins┃∅
```
</details>

### With Nulls

<div class="readout">
  <span class="readout-label">STELE FORMAT</span>
@ᚠ=telemetry,ᚡ=timestamp,ᚢ=altitude,ᚣ=notes
ᚠ┃ᚡⁱ┃ᚢᶠ┃ᚣˢ▓◉1621234567┃408.5┃∅▓◉1621234568┃∅┃Signal▓lost▓◉1621234569┃412.1┃Reacquired
</div>
<details>
<summary>Expanded</summary>

```
@telemetry┃timestampⁱ┃altitudeᶠ┃notesˢ▓◉1621234567┃408.5┃∅▓◉1621234568┃∅┃Signal▓lost▓◉1621234569┃412.1┃Reacquired
```
</details>

### Embedded Content

stele handles embedded JSON, code, or any content without escaping:

<div class="readout">
  <span class="readout-label">STELE FORMAT</span>
@ᚠ=logs,ᚡ=level,ᚢ=message
ᚠ┃ᚡˢ┃ᚢˢ▓◉error┃Failed▓to▓parse▓{"key":▓"value"}▓◉info┃User▓said▓"hello,▓world"▓◉debug┃Multiline▓content▓works
</div>
<details>
<summary>Expanded</summary>

```
@logs┃levelˢ┃messageˢ▓◉error┃Failed▓to▓parse▓{"key":▓"value"}▓◉info┃User▓said▓"hello,▓world"▓◉debug┃Multiline▓content▓works
```
</details>

The heavy pipe `┃` delimiter is rare enough that typical content passes through unchanged.

---

## Context Efficiency

| Content Type | JSON | stele | Reduction |
|--------------|------|-------|-----------|
| 10 simple records | 450 bytes | 280 bytes | 38% |
| 100 records | 4,200 bytes | 2,100 bytes | 50% |
| Nested with arrays | 890 bytes | 520 bytes | 42% |
| **SWAPI people (5 records, nested)** | **1,117 bytes** | **725 bytes** | **35%** |

### Real-World Benchmark: Star Wars API

Tested against actual SWAPI data with nested arrays (films, vehicles, starships per character):

<div class="readout">
  <span class="readout-label">SWAPI IN STELE</span>
@ᚠ=people,ᚡ=name,ᚢ=height,ᚣ=films,ᚤ=vehicles
ᚠ჻0჻ᚡˢ┃ᚠ჻0჻ᚢˢ┃ᚠ჻0჻ᚣˢ⟦⟧┃ᚠ჻0჻ᚤˢ⟦⟧┃ᚠ჻1჻ᚡˢ┃ᚠ჻1჻ᚣˢ⟦⟧┃ᚠ⟦⟧▓◉Luke▓Skywalker┃172┃film/1◈film/2┃vehicle/14┃C-3PO┃film/1┃∅
</div>
<details>
<summary>Expanded</summary>

```
@┃people჻0჻nameˢ┃people჻0჻heightˢ┃people჻0჻filmsˢ⟦⟧┃people჻0჻vehiclesˢ⟦⟧┃people჻1჻nameˢ┃people჻1჻filmsˢ⟦⟧┃people⟦⟧▓◉Luke▓Skywalker┃172┃film/1◈film/2┃vehicle/14┃C-3PO┃film/1┃∅
```
</details>

Note the `▓` (U+2593) replacing spaces in names—this prevents whitespace mangling in terminals and parsers while remaining visually distinct. Models read it as a space naturally.

**Result:** 35% reduction, parsed correctly by Haiku with zero format explanation. Path-based nesting makes relationships explicit.

stele achieves 30-50% context reduction over JSON for typical structured data. For maximum compression, use carrier98.

---

## Escape Hatch

When data contains stele delimiters (rare), wrap the field in carrier98 encoding:

```
◉normal value┃𓍹carrier98_encoded_value𓍺┃another value
```

The hieroglyph delimiters `𓍹...𓍺` signal encoded content. Decode the carrier98 payload to recover the original value.

---

## Relationship to carrier98

| Property | stele | carrier98 |
|----------|-------|-----------|
| Model reads structure | Yes | No |
| Human reads structure | Yes | No |
| Context reduction | 30-50% | 90-97% |
| Use case | Working data | Shuttle data |
| Parsing required | Minimal | Full decode |

**Use stele when:** The model needs to understand and transform the data.

**Use carrier98 when:** The model passes data through unchanged—maximum density, minimum tokens.

They are siblings. Same family, different jobs.

---

## Implementation

### CLI

```bash
# JSON → stele
echo '{"users":[{"id":1,"name":"alice"}]}' | base-d stele

# JSON → stele (minified single line)
echo '{"users":[{"id":1,"name":"alice"}]}' | base-d stele -m

# stele → JSON (works with both formats)
echo '@users┃idⁱ┃nameˢ▓◉1┃alice' | base-d stele -d

# Pretty-print JSON output
base-d stele -d -p < data.stele
```

### Library

```rust
use base_d::{encode_stele, encode_stele_minified, decode_stele};

let json = r#"{"users":[{"id":1,"name":"alice"}]}"#;
let stele = encode_stele(json)?;           // multi-line
let minified = encode_stele_minified(json)?; // single line
let restored = decode_stele(&stele, false)?;
```

---

## Reference

**Specification version:** 1.0

**Implementation:** [base-d](https://github.com/coryzibell/base-d) (Rust)

**Related:** [carrier98](/) — opaque wire format for maximum density
