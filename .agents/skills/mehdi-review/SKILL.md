---
name: mehdi-review
description: Perform technical, editorial, and consistency review.
---


Review:
- technical correctness
- evidence quality
- terminology
- narrative consistency
- implementation alignment
- reader understanding

Report blocking issues separately.

Name the gate being reviewed. Keep these outcomes distinct:

- **Machine semantic acceptance:** the target reflects the current canonical
  source; this is not human approval.
- **Human-review repair acceptance:** all human notes are accounted for and
  machine repairs are ready for human signoff; this is not that signoff.
- **Final human signoff:** an authorized human approves the specified current
  content revision, with recorded evidence. A machine cannot grant this gate.
- **Publication acceptance:** separate whole-book, artifact, and release gates
  pass; translation parity or human signoff alone does not grant it.

For human-note repair audits, use `$mehdi-human-review` for the ledger and
approval boundary. Report exact remaining blockers and human preferences.
