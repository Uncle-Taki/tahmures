---
name: mehdi-architecture
description: "Turn approved technical knowledge into clear system models, architecture explanations, diagrams, and explicit design trade-offs for a book or learning artifact."
---

# Mehdi architecture

Explain why before how. Build a model that helps the reader reason about a system, not merely memorize component names.

## Role

Bridge approved knowledge atoms and chapter blueprints into structured engineering explanations, mental models, component contracts, and explicit trade-offs.

In the Mehdi publishing lifecycle:
`Context → Research → Knowledge → Architecture → Narrative → Author → Bilingual → Review → Media → Publication`

Architecture establishes the technical boundaries, trust models, and failure semantics before narrative analogies or chapter prose are finalized.

## Inputs

Read the project context, intended audience, approved knowledge units (`$mehdi-knowledge`), relevant source code or authoritative documentation (`examples/python/` and `examples/go/`), and the chapter blueprint. Do not design from an isolated diagram or unverified terminology.

## Workflow

1. **System boundary & problem definition:** State the system boundary, purpose, actors, and the concrete problem the architecture solves.
2. **Components & responsibilities:** Identify components, responsibilities, explicit non-responsibilities, interfaces, state ownership, data flows, and external dependencies.
3. **Flow separation:** Separate control flow from data flow, and synchronous from asynchronous behavior.
4. **Invariants & trust boundaries:** Explain invariants, trust boundaries, consistency guarantees, failure modes, and recovery paths.
5. **Deterministic vs. prompt controls:** Distinguish what belongs in prompt instructions from what must be enforced in deterministic application code, data validation, access controls, or human governance.
6. **Trade-offs & alternatives:** Compare plausible alternatives and state why the selected design fits the stated constraints.
7. **Diagram selection & justification:** Choose a diagram only when it improves comprehension; use the simplest suitable form (context, component, sequence, state, deployment, or data-flow).
8. **Prose alignment:** Explain every diagram in prose and ensure labels, arrows, contracts, and boundaries agree strictly with the source code and text.

## Required component breakdown

For each major component or boundary, cover:
- **Responsibility and non-responsibility:** What the component owns and what surrounding systems or application code must enforce.
- **Contract:** Inputs, outputs, data formats, and error protocols.
- **State:** What state it owns, mutates, or depends on.
- **Failure modes:** How it fails, operational implications, and recovery/fallback mechanisms.
- **Adjacent relationships:** Trust, synchronization, and communication boundaries with neighbouring components.

## Tahmures repository rules

- **Deterministic enforcement:** Enforce identity, permissions, budgets, state transitions, rate limits, and irreversible actions in deterministic application code rather than prompt prose.
- **Implementation parity:** Architecture must reflect the canonical Python implementation (`examples/python/tahmures/`) and equivalent Go observable behavior (`examples/go/tahmures/`). Never invent phantom abstractions or expand teaching contracts beyond implemented code.
- **Chapter contract alignment:** Architectural outputs directly feed the mandatory chapter contract sections: `Mental Model`, `Core Concepts`, `Failure Analysis`, `Improved Design`, `Security Considerations`, `Operational Considerations`, `Trade-Offs`, and `When Prompting Is Not the Answer`.
- **Editable diagrams:** Keep diagram sources editable (e.g. Mermaid or Draw.io) and ensure terminology matches `book/fa/translation-glossary.md` and repository standards.

## Output

Provide:
1. A reader-oriented architecture narrative explaining why before how.
2. A component and boundary matrix detailing contracts and state ownership.
3. One or more justified, editable diagrams (context, sequence, component, or state).
4. Explicit design decisions, trade-offs, and failure mode analysis.
5. A concise ledger of assumptions requiring verification against source code.
