# Persian editorial warning triage — 2026-09-21

Baseline: 252 fa-editorial warnings (0 errors), all chapters 01-24.
Post-triage: 9 warnings, each dispositioned below. No heuristic warning
was dismissed without a recorded reason.

## Fixed in text (43 sites)

- 27 missing-ZWNJ morphology violations (settingهای, stageهایی, writeها,
  requirementهایی, ...): ordinary English terms with Persian suffixes
  lacking the glossary-mandated ZWNJ. Fixed by inserting U+200C in
  ch02, ch03, ch05, ch07, ch08, ch09, ch10, ch11, ch12, ch24.
- 16 word-order/ezafe repairs across the human-reviewed calibration corpus
  (ch06, ch08, ch09) and machine-prechecked chapters (ch10, ch15, ch17,
  ch20, ch21). These were targeted integrity repairs, not a retranslation
  (head-first reordering, ezafe insertion, and restored dropped qualifiers):
  - ch06 merchant وضعیت; ch08 unfamiliar/companion/nested;
    ch09 shared/idempotency-key/confirmed; ch17 نهایی state (5 sites);
    ch20 regression مجموعه/آزمون (2); ch21 اصلی key;
    ch10 diversityِ پاسخ‌ها; ch15 recallِ رکورد فعال.
  English technical meaning verified against the canonical source
  before each fix; protected tokens untouched.

## Validator tuning (false-positive classes removed)

- morphology heuristic now flags only missing-ZWNJ suffixes;
  glossary-sanctioned Latin\u200csuffix forms are not flagged (~179 sites)
- markdown headings stripped from prose: "Python\n\n\nقرارداد"-style
  heading-boundary artifacts eliminated (~17 sites)
- Persian suffixed nouns like نوع‌دار/پاسخ‌پذیر/پاسخ‌گو after a Latin
  head no longer flagged (correct head+adjective order, ~8 sites)
- retained-term objective/summary phrases with correct Persian
  structure confirmed as legitimate (~4 sites)

## Remaining 9 warnings — pending human terminology decisions

These warnings require the contextual review rule recorded in
editorial/fa-review/chapters-01-09.md §3.7 ("review triggers only, no blind
string replacement; ambiguous fragments must be reported, not guessed").
They are not a one-to-one match to FA-004..FA-012: `flexible فیلد` matches
FA-005 and `free نثر` matches FA-008; `اضافی ignored` and `خام sample` are
related to the FA-009 and FA-010 classes, respectively. FA-004, FA-006, and
FA-007 do not occur in the current warning output. Human-approved corrections
did not exist at the time of triage, so the text was left untouched:

1. ch04 'validation قرارداد' (calibration corpus ch04, front-matter
   objective; needs terminology decision on validation)
2. ch07 'مجاز set' (contextual terminology review)
3. ch07 'interpolation مرحله' (related FA class)
4. ch08 'اضافی ignored' (related to FA-009)
5. ch08 'خام sample' (related to FA-010)
6. ch08 'free نثر' (FA-008: از free نثر امن‌تر است)
7. ch08 'requirements پاسخ' (related FA class)
8. ch08 'flexible فیلد' (FA-005)
9. ch09 'per وضعیت' (related FA class)

Decision rule applied: no calibration-corpus wording (ch01-09) and no
flag-only fragment was altered by the machine pass.

## D16 spot-check and disposition correction — 2026-09-27

- `editorial/review-status.yml` confirms that ch06, ch08, and ch09 are
  `human_reviewed`; ch17 is `machine_prechecked`. The repaired-site summary
  above now records those states accurately.
- The ch06 repair at fa:160 was checked against en:160: the four merchant-only
  examples imply that merchant status may be predictive. The current Persian
  preserves that relation without changing protected technical tokens.
- The ch08 repairs were checked against the canonical source: consequential
  unfamiliar status (en:397 / fa:327), companion status field (en:402 /
  fa:331), and nested records (en:463 / fa:365). The Persian now uses a
  head-first phrase with the appropriate ezafe where needed.
- The ch09 repairs were checked against shared type (en:148 / fa:143) and
  confirmed status (en:239 / fa:219). The source-aligned idempotency-key
  wording in the same Persian sentence was also confirmed.
- The five ch17 `state نهایی` repairs were checked as head-first Persian
  constructions for the source's terminal-state concepts. Their protected
  English technical terms remain unchanged.
