---
name: mehdi-director
description: Orchestrate the Mehdi publishing workflow and choose the next appropriate capability.
---


Role:
Coordinate the full book-production lifecycle.

Workflow:
Context -> Research -> Knowledge -> Architecture -> Narrative -> Author -> Bilingual -> Review -> Media -> Publication

In the Tahmures repository, route story creation, tale rewriting, named
character or mythic-place changes, narrative localization, and character
continuity audits through `$mehdi-narrative` **and**
`$tahmures-narrative`. The first owns narrative craft; the second checks mythic
tier, cast, chronology, names, and existing continuity. An audit does not
authorize rewriting a frozen chapter.

When human notes exist for translated chapters, route the batch through
`$mehdi-human-review`: Context -> note reconciliation -> targeted bilingual,
narrative, or technical review as needed -> validation -> supervisory check ->
human signoff -> separate review-metadata reconciliation -> next batch. Do not
send it through full authoring or translation unless the note exposes a real
canonical-source synchronization defect.

After current human signoff across the book, route terminology consolidation,
process-metadata reconciliation, visual audit, whole-book bilingual review,
publication gates, publisher work, and final supervisory acceptance. Human
approval is revision-bound; machine checks and historical signoff cannot
substitute for it. Commit only with explicit authorization.

Rules:
- Do not become a source of truth.
- Read project context before making decisions.
- Use only necessary skills.
- Preserve human approval points.
