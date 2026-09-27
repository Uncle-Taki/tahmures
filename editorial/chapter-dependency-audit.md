# Chapter Dependency Audit — D14

## Decision rule

An edge is **REQUIRED** only when the dependent chapter directly relies on the
parent chapter's mental model to achieve its learning objectives. A relationship
that supplies useful background or appears in the historical reading sequence is
**SUPPORTING**, and is not encoded in prerequisite metadata. The review inspected
each English chapter's learning objectives, engineering problem, core concepts,
and chapter summary.

## Verified charter edges

The following declared charter edges are **REQUIRED**:

- C01→C02, C01→C03, C03→C04, C04→C05, C04→C07, and C04→C08.
- C03→C09, C08→C09, C03→C10, C06→C10, and C10→C11.
- C04→C12, C12→C13, C13→C14, C05→C15, and C12→C15.
- C05→C16, C08→C16, C15→C16, C09→C17, C16→C17, C08→C18,
  C12→C18, and C17→C18.
- C03→C19, C08→C19, C10→C19, C06→C20, and C19→C20.
- C05→C21, C13→C21, C14→C21, C16→C21, C16→C22, and C21→C22.
- C19→C23, C20→C23, C22→C23, C17→C24, C18→C24, C19→C24,
  C20→C24, C21→C24, C22→C24, and C23→C24.

## Excluded charter edges

| Edge | Classification | Evidence |
| --- | --- | --- |
| C02→C04 | SUPPORTING | Owner decision: uncertainty helps framing but the chapter's reliable-prompt structure depends on C01 and C03. |
| C04→C06 | SUPPORTING | Prompt anatomy is useful background; representative examples and boundary cases depend directly on requirements. |
| C09→C10 | SUPPORTING | Workflows may supply applications, but variance/selection control relies directly on requirements and examples. |

No declared edge was classified **INVALID**.

## Missing required edges

| Edge | Evidence |
| --- | --- |
| C01→C04 | Owner decision and Chapter 4's use of the complete model-visible prompt before it decomposes that prompt into reliable fields. |
| C03→C06 | Chapter 6 selects representative and boundary examples against stated rules and acceptance criteria. |

The final canonical graph is `editorial/chapter-dependencies.yml`; it contains
only the REQUIRED edges listed above.
