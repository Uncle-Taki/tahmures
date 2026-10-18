# GLM Revision 1 — SESSION STATE (COMPLETE)

Task: CHARACTER_LAYOUT01_MOUTHLESS_REPAIR, bounded revision 1 (v3 → v4).
Mode: IMPLEMENT_AND_VERIFY. Status: **ALL LOCAL STAGES COMPLETE.**
Final GLM report: `Characters/tahmures/workflow/layout01-mouthless-repair/
reports/glm/implementation-02.md`. Completion token was emitted there.
This file is a resume point, NOT a report; no Codex/Claude/human acceptance
is claimed.

## Completed stages (all verified)

- Stage 10 sprites: build_10_sprites.py (3 runs; final run clean). All 14
  sprites + masks + provenance + region npy. M=2616 P=3217 (asserted
  v3-identical), U=1820; ink_head=1394, ink_beard=345, patch_ink=336,
  neck_clean=277 (gold 265 + trim 12; 234 in eroded domain), opening=59 at
  the y240 lip parting line, bbox [531,239,554,242); moustache solve:
  kept=1436, dropped=2, solved=353, fallback=29, guarded=0.
- Stage 20 previews: A/B/C saved; coverage 0/0 each; A diff 2371 (0
  escaping), B 283 (0 escaping; all intended neck repair), C 342 (0
  escaping); B/C differ at exactly the 59 opening px; R1-01 warm crescent 0.
- Stage 30 stress: 18/18 samples pass (coverage 0/0, confined, receiver
  dark, vacated strips byte-exact for all 4 moustache offsets over both
  states, (0,0) byte-identical to previews).
- Stage 40 plates: 27 plates in previews/plates/ incl. R1_01..R1_04
  before/after evidence plates.
- Stage 50 manifest: layout01-v4, schema 3.0.0, repair_regions + honest
  known_limitations; pivots match v2 eye/brow values.
- Candidate report: implementation-report.md at candidate root.
- Stage 60 validation: checker 185/185 pass via
  `rtk proxy /usr/bin/python3` (literal `rtk proxy python3` fails: book
  .venv has no PIL — recorded honestly); fixed point verified; final index
  rebuilt AFTER stage 70 so it covers code/_verify_report.json.
- Stage 70 independent checks: ALL PASS (recomposition byte-equality,
  independent float composite max diff 1, mask==alpha, provenance partition
  + source claims, eye/brow pivots == v2, coverage 0/0, outer boundary
  alpha never raised, no banned duplicates, stress present/pass, v3 tree
  unchanged vs its own index, vacated-strip identity, R1 recounts).
  Results: code/_verify_report.json.

## R1 before/after (consistent classifiers, see _verify_report.json)

- R1-01 warm crescent in [530,230,542,237): v3 6 (Codex 8 with their
  classifier) → v4 0; over clone zone 0.
- R1-02 head_base dark in [486,209,597,238): v3 1234 dark/1234 exact
  (Codex 1233) → v4 87 (86 diffusion fills at the moustache/beard boundary
  y229-237, colors ~(46,34,29); 1 kept master stray (556,209)). Beard dark
  stays 818/809-810 exact — clone/natural beard are legitimately dark
  (revision brief: exact-dark matches are not a defect); functional proof
  is the vacated-strip byte-identity.
- R1-03 opening: 59 px at [531,239,554,242), B/C differ only there.
- R1-04 garment (r>=120 & r-b>=90 & b<=70 & y>=300, visible):
  head_base v3 265 → v4 0; hair_back v3 6 → v4 0. (The earlier "419"
  estimate used a wider classifier; 265 is the reproducible count.)

## Repo gates

- git diff --check: clean (only pre-existing untracked Characters/ + li*3).
- make check PYTHON=.venv/bin/python: PASS (see final report).

## Pitfalls that remain true for any future correction round

- Never pass zero-masked seed arrays to diffuse(); region must include
  invisible buffers, boundary must be real art.
- Garment vs neck-skin classifier MUST keep b<=70 (skin reaches r-b=147
  with b>=73).
- Census masks must intersect layer alpha (stale full-canvas RGB).
- v2 moustache alpha is binary 253/254; soft edges live in RGB blends.
- files-sha256.json must be rebuilt after ANY file under the candidate
  root changes (including reports); rerun build_60 last.
- Never edit the supervisor checker; record both command variants.
