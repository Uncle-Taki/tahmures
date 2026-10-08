---
name: mehdi-bilingual
description: Create and synchronize multilingual technical editions.
---


Rules:
- Preserve technical meaning.
- Follow glossary.
- Use natural target-language syntax, including modifier scope, condition,
  negation, and causal order; do not copy the source's sentence architecture.
- Preserve code, identifiers, URLs, and protected tokens.
- Classify Latin text before translating it: protect identifiers, fields,
  code, and citation titles; translate or explain ordinary reader-facing prose.
- Inspect rendered mixed-script order as well as source order. Use bidi
  controls only where justified and never inside executable or protected tokens.
- Respect human-approved wording and editorial preferences for the revision
  they cover, subject to canonical meaning and project rules.

Check semantic parity between languages.

When the input is human notes on an existing translation, use
`$mehdi-human-review` for note accounting and signoff. This skill supplies
bilingual quality checks, not the human-review lifecycle.
