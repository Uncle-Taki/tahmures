# Chapter One rewrite — two visual production contexts

Prepared 2026-10-30. This handoff follows the owner's new Persian screenplay, not the older film's script. Complete polished Persian and English editions: `playscript/chapter-01-final-2026-10-30/`. Scope: local writing, analysis and preparation only.

- [Paper Puppet context](flow-paper-puppet/README.md)
- [Illustrated V2 context](flow-illustrated-v2/README.md)
- [Paper Puppet roadmap](flow-paper-puppet/ROADMAP.md) and [workflow](flow-paper-puppet/WORKFLOW.md)
- [Paper Puppet Character info](flow-paper-puppet/context/CHARACTER_INFO.md)
- [V2 Character info](flow-illustrated-v2/context/CHARACTER_INFO.md)
- [Cast and screenplay analysis](CAST_AND_SCRIPT_ANALYSIS.md)
- [Source/change ledger](SOURCE_AND_CHANGE_LOG.md)
- [Validation report](VALIDATION_REPORT.md)
- [Owner decisions](OWNER_DECISIONS.md)

Paper Puppet now has nine physical reference-image copies; Illustrated V2 has seven. Each branch has both final editorial scripts, eleven scene units, 44 action-led shot briefs, six Agent instruction files, three numbered UI guides and dialogue/asset/scene maps. Total: 88 branch-specific shot cards, with identical story and cue IDs. A shot brief may require further reviewed phase splitting; 44 does not claim a final clip count.

## Ten-step start

1. Read the final Persian screenplay.
2. Read the paired English screenplay or side-by-side HTML.
3. Review the substantive editorial changes and optional ending hook.
4. Choose ONE visual branch for a separate Flow project.
5. Read the branch Character info index and review supplied portraits/marked derivatives.
6. Paper Puppet: use the new Chapar/Arash references. V2: those two images remain missing. Prepare scene references for the pilot.
7. Review exact frames, props, poses and selected scene cast before any paid action.
8. Use branch guides to reconcile Agent rules and plan RW01-S11-SH01's held two-character pilot.
9. Record/review each language separately; measure timings and build a NEW edit.
10. Log settings, credit spend, actual takes, downloads and owner decisions locally.

The original writing/preparation run used no external generation. The later owner-authorized portrait/body correction task performed four built-in image_gen edits, recorded under flow-paper-puppet/portrait-body-candidate-01/. No Flow upload, voice/video generation, commit or push was performed. The original screenplay, selected artwork, canonical books, existing official Flow handoff and previous production sources are unchanged. Flow account registration/upload state was not inspected. Public documentation was checked; account controls/costs remain for the owner to verify.

## Rebuild and audit locally

From repository root:

```bash
rtk proxy /usr/bin/python3 editorial/media-handoff/chapter-01-rewrite-2026-10-30/scripts/build_packages.py
rtk proxy /usr/bin/python3 editorial/media-handoff/chapter-01-rewrite-2026-10-30/scripts/validate_packages.py
```

Uses existing system Pillow for copying metadata and local contact sheets, no new dependencies. Rebuild touches only this new package and the new editorial-final script outputs. `episode.json` is the input for any later editorial repair. Supporting review documents are maintained separately. FILE_INDEX.txt enumerates created outputs.

## Portrait / Create body inputs

- [Paper Puppet: nine pairs and four corrected body candidates](flow-paper-puppet/portrait-body-candidate-01/PAIR_INDEX.md).
- [Illustrated V2: seven pairs from unchanged body references](flow-illustrated-v2/portrait-body-candidate-01/PAIR_INDEX.md).
- [Paper Puppet gap-resolution record](flow-paper-puppet/portrait-body-candidate-01/DESIGN_GAP_RESOLUTION.md).

Use a portrait and body from the same revision. Each portrait is an exact crop of its matching full body. Corrected art and proposed scale are reviewable candidates, not silent replacements of selected source artwork.
