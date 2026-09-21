# Persian editorial warning triage — 2026-09-21

Baseline: 252 fa-editorial warnings (0 errors), all chapters 01-24.
Post-triage: 9 warnings, each dispositioned below. No heuristic warning
was dismissed without a recorded reason.

## Fixed in text (43 sites)

- 27 missing-ZWNJ morphology violations (settingهای, stageهایی, writeها,
  requirementهایی, ...): ordinary English terms with Persian suffixes
  lacking the glossary-mandated ZWNJ. Fixed by inserting U+200C in
  ch02, ch03, ch05, ch07, ch08, ch09, ch10, ch11, ch12, ch24.
- 16 word-order/ezafe repairs in machine-prechecked chapters
  (FA-002/FA-003 classes: head-first reordering, ezafe insertion,
  restored dropped qualifiers):
  - ch06 merchant وضعیت; ch08 unfamiliar/companion/nested;
    ch09 shared/confirmed/per-stage; ch17 نهایی state (5 sites);
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

These match the flag-only fragments FA-004..FA-012 recorded in
editorial/fa-review/chapters-01-09.md §3.7 ("review triggers only, no
blind string replacement; ambiguous fragments must be reported, not
guessed"). Human-approved corrections do not exist yet, so the text is
left untouched:

1. ch04 'validation قرارداد' (calibration corpus ch04, front-matter
   objective; needs terminology decision on validation)
2. ch07 'مجاز set' (FA-004 trigger)
3. ch07 'interpolation مرحله' (related FA class)
4. ch08 'اضافی ignored' (FA trigger)
5. ch08 'خام sample' (FA trigger)
6. ch08 'free نثر' (FA-007 trigger: از free نثر امن‌تر است)
7. ch08 'requirements پاسخ' (related FA class)
8. ch08 'flexible فیلد' (FA trigger)
9. ch09 'per وضعیت' (related FA class)

Decision rule applied: no calibration-corpus wording (ch01-09) and no
flag-only fragment was altered by the machine pass.
