---
title: "Designing for Creativity"
slug: "designing-for-creativity"
chapter: 11
part: "Part II — Prompt Design and Controlled Generation"
summary: "Design creative exploration and accountable acceptance as different stages with human-owned criteria."
maturity: "draft"
last_reviewed: "2026-07-29"
narrative_episode: "The Garden That Had Never Grown"
narrative_origin: "original-teaching-fiction"
learning_objectives:
  - "Separate divergent exploration from convergent acceptance"
  - "Evaluate novelty alongside feasibility, relevance, and harm"
  - "Use committed human rubric data without model self-grading"
prerequisites: [C10]
---

# Designing for Creativity


## Learning Objectives

You will design interactions that encourage materially different candidates
without treating randomness as creativity. You will create a human-owned
acceptance rubric, preserve disqualifying constraints, analyse reviewer
disagreement, and avoid using a model’s self-reported score as evidence.

## The Tale of Tahmures


### The Setting

A letter arrived from Arnavaz, keeper of the upper garden, with blue dust
pressed into its fold.

> The council asked for a garden that has never grown in any kingdom. The divs
> have supplied wonders. None can be watered.

The upper terrace lay above the palace cistern. Two gardeners maintained it,
and a public stair crossed its center. Summer wind stripped moisture from
shallow soil.

### The Request

Tahmures had asked three divs to be “completely original, unconstrained by old
designs.” Their proposals were memorable. Silver channels carried water
uphill. Fruit trees floated from silk canopies. A maze of glass thorns changed
shape at sunset.

The court applauded the drawings. The gardeners examined them in silence.

One div supplied a score beside its own design: originality ten, usefulness
nine, beauty ten. Another declared that practical objections were evidence of
timid thought. A third borrowed the palace’s existing rose geometry, renamed
each bed after a star, and called it unprecedented.

### The Unexpected Result

Workers began the silver channels because they had won the most admiration.
After three days, the first channel delivered no water. Raising the cistern
would block a watch path; adding a lifting wheel required six workers. The
glass maze narrowed the public stair below the width needed for a grain cart.

Arnavaz stopped construction and accepted blame before the council could place
it on the divs.

“We asked them to escape every boundary,” she wrote. “Then we judged drawings
as if delight were proof of a garden.”

Tahmures saw that the request had removed the facts that made the problem
worth solving.

### The Discovery

Arnavaz divided the workshop into two rooms. In the first, designers explored:
alter water storage, shade, planting height, seasonal form, and visitor path.
They were encouraged to combine distant references and to state what made each
candidate different. No candidate was selected there.

In the second room, gardeners, a mason, and a representative of people who
used the stair reviewed candidates with their makers hidden. They scored
feasibility, relevance, novelty, and explanation quality. Water flowing uphill
without a mechanism and any obstruction of the stair were disqualifying,
whatever the average score.

Reviewers disagreed about beauty and novelty. The First Scribe preserved their
individual scores and reasons rather than asking a div to settle the
disagreement. A contour garden fed by a small raised cistern survived the hard
constraints. Its channels followed unfamiliar asymmetric curves, but every
curve had a hydraulic purpose.

It was not the strangest drawing. It was the first new garden the gardeners
could responsibly try.

### From Tale to Engineering

Creativity is not unconstrained randomness or self-declared novelty. Useful
creative systems separate exploration from acceptance and evaluate candidates
against human purposes, feasibility, references, and disqualifying harm.

## The Engineering Problem

Creative requests combine objectives that pull in different directions.
Novelty can reduce familiarity and feasibility. Strict examples can improve
relevance while narrowing exploration. A single score can hide a fatal flaw.
Reviewers may legitimately disagree because taste and value are part of the
task.

Language models generate patterns influenced by training data and supplied
references. They can make surprising combinations, but output is not evidence
of historical originality. The engineering task is to create useful search
conditions and an accountable acceptance process without promising that a
prompt can measure creativity objectively.

## Mental Model

Use a divergent-convergent loop:

```text
frame -> explore -> diversify -> validate -> review -> select or revise
```

Framing supplies purpose, audience, constraints, and relevant references.
Exploration generates candidates without prematurely declaring one best.
Diversification checks whether candidates differ materially. Validation removes
hard failures. Review applies a rubric and records reasons. Selection is a
human or policy decision, with revision available when no candidate passes.

The two phases need different prompt behaviour. Exploration benefits from
varied perspectives and candidate count. Acceptance benefits from stable
criteria, evidence, and independence from candidate self-praise.

## Core Concepts

Novelty is relative to a reference set and audience. “Never seen before” is
usually untestable. Define a practical comparison: unlike the supplied prior
campaigns, using a different mechanism, or novel to target users in a study.
Report the scope of the claim.

Randomness can change outputs without producing meaningful difference. Measure
candidate distance in task-specific terms: distinct mechanisms, narrative
premises, interaction patterns, or visual structures. Exact text uniqueness is
only a preliminary signal.

Constraints can stimulate creativity when they preserve the actual problem.
“Use two workers and gravity-fed water” directs search. Removing the water
constraint makes garden proposals less relevant, not more imaginative.

References have dual effects. They communicate quality and domain but can
anchor outputs to superficial imitation. Use diverse references, explain which
properties matter, and include counterexamples. When intellectual property
risk matters, review provenance and similarity with appropriate expertise.

Rubrics should name dimensions separately: feasibility, relevance, novelty,
craft, explanation, safety, or brand fit. Define scale anchors. Do not average
away disqualifying failures. A candidate with novelty five and safety one does
not become acceptable because its mean is three.

Human ratings are observations with uncertainty. Preserve reviewer identity or
role under privacy policy, individual scores, disagreement, and reasons.
Calibration examples can improve consistency. Disagreement may reveal an
underspecified audience rather than reviewer error.

A model may help organise feedback but should not be the sole judge of its own
output. Self-evaluation shares biases with generation, can be influenced by
phrasing, and lacks independent evidence. The fixtures in this repository
contain committed synthetic human scores in response metadata; those scores
are not generated by the response text.

## Prompt Pattern

Exploration prompt:

```text
Generate four materially different garden mechanisms.
Purpose: cool the upper terrace and preserve public passage.
Hard constraints: gravity-fed water, two maintainers, path width unchanged.
For each candidate, state its mechanism, reference influence, and principal
uncertainty. Do not score or select.
```

Acceptance packet:

```text
Candidate ID and anonymised description
Validation results for hard constraints
Rubric anchors for feasibility, relevance, novelty, explanation
Reviewer score and reason for each dimension
Disqualifying failure field
```

The application combines reviewer records according to declared policy. It
does not ask the candidate generator to announce victory.

## Naive Attempt

Prompts such as “be maximally creative,” “ignore all constraints,” and “avoid
clichés” lack an operational reference. They can increase decorative
strangeness while reducing usefulness. Asking for one idea prevents comparison.
Asking the model to give its idea a creativity score creates circular evidence.

Another naive approach supplies a beloved reference and asks for “the same but
new.” It can produce imitation with renamed details. Better prompts extract the
underlying properties desired and widen the reference set.

## Failure Analysis

Exploration failures include near duplicates, cosmetic variation, reference
copying, infeasible mechanisms, and output that optimises the language of
novelty. Acceptance failures include vague rubrics, uncalibrated reviewers,
averaged disqualifiers, selection based on presentation order, and retrofitted
criteria chosen after a favourite appears.

System failures include leaking creator identity into supposedly blind review,
losing rejected candidates and feedback, and evaluating only successful
examples. Product failures occur when “engagement” substitutes for the human
purpose or when affected communities are absent from review.

## Improved Design

Frame the creative problem with stakeholders and hard boundaries. Build a
small, diverse reference set and document why each reference is present. Ask
for multiple candidates using distinct mechanisms or perspectives. Validate
structure and hard constraints automatically where possible.

Before viewing results, publish the acceptance rubric and disqualifiers.
Recruit reviewers with relevant roles. Randomise or anonymise presentation
where appropriate. Preserve individual ratings and calculate agreement without
erasing reasons. Select, revise, or reject all candidates.

Run repeated trials and inspect both diversity and quality distributions.
Regression cases should include common spectacular failures: physically
impossible ideas, inaccessible designs, copied surface style, and polished
rationales unsupported by the artefact.

## Worked Example

A team needs onboarding messages for users unfamiliar with technical jargon.
Exploration generates four metaphors. Hard constraints prohibit medical or
financial promises and require a plain-language action. Reviewers include a
support specialist and representative users.

The most novel metaphor confuses the action and fails relevance. A more modest
candidate is clear but too similar to existing copy. Review feedback combines
the clear structure of one with the fresh perspective of another. Creativity
appears as an iterative system outcome, not a property proved by one response.

## Experiment

```bash
python -m tahmures.cli run \
  --manifest experiments/manifests/ch11-creativity.json
go run ./examples/go/cmd/tahmures run \
  --manifest experiments/manifests/ch11-creativity.json
```

The two variants compare unconstrained novelty with exploration followed by
acceptance. Each case has two trials. Responses must satisfy a small JSON
contract. Fixture metadata contains synthetic human rubric scores for
feasibility, relevance, novelty, and explanation plus disagreement.

The novelty-only responses remain structurally valid while failing human
thresholds. The improved responses meet thresholds and repeat, producing lower
exact diversity. This does not prove the improved method is universally more
creative; it shows why diversity and acceptance must both be reported.

## Evaluation

Report feasibility pass rate, rubric-threshold rate, disqualifying failures,
diversity, and reviewer disagreement. Show dimension distributions, not only
averages. Segment by constraints such as water or safety. Preserve sample
artefacts for qualitative review under proper data policy.

Use held-out briefs and reviewers not involved in prompt authoring. Evaluate
whether the rubric predicts later human usefulness, not merely whether raters
can apply it consistently. Document limitations of synthetic fixture scores.

## Implementation Lab

### Python

```python
minimum = {"feasibility": 3, "relevance": 3, "novelty": 3}
scores = fixture_response.metadata["rubric_scores"]
passes = all(scores[name] >= value for name, value in minimum.items())
```

The `rubric_metadata` evaluator performs this comparison and reports each
dimension. The response never supplies its own accepted score.

### Go

```go
scores := response.Metadata["rubric_scores"].(map[string]any)
for name, minimum := range minima {
    score := scores[name].(float64)
    if score < minimum {
        accepted = false
    }
}
```

Production code must check type assertions and preserve reviewer provenance.
The shared evaluator handles fixture-shaped values for the offline lab.

## Failure Modes

Beware decorative randomness, untestable originality claims, anchoring on one
reference, rubric gaming, self-scoring, averaged safety failures, reviewer
fatigue, and feedback that rewards explanations more than artefacts. A polished
rationale can make an infeasible idea appear considered.

Do not treat agreement as the only goal. Forced consensus can erase meaningful
stakeholder conflict.

## Security Considerations

Creative tasks can reproduce sensitive, hateful, deceptive, or copyrighted
material. Define content boundaries and human review appropriate to audience
and distribution. Keep untrusted references separate from instructions. Limit
tools during exploration; an idea generator does not need publishing authority.

Protect confidential briefs and reviewer identities. Do not include secrets in
fixtures or logs.

## Operational Considerations

Version briefs, references, prompts, rubric anchors, and reviewer panels. Track
acceptance and revision rates over time. Budget for review, not just inference.
When models change, rerun both constraint failures and representative creative
briefs.

Store generated candidates only as long as needed. Provide a process for
provenance and similarity review before public release.

Before release, have a reviewer reconstruct one decision from retained evidence. If its active inputs, versions, owner, and reason code cannot be identified, the boundary is not yet operationally auditable.

## Trade-Offs

More exploration costs more and can overwhelm reviewers. Strong constraints
improve relevance while narrowing possibility. Blind review reduces some bias
but removes context sometimes needed for judgement. Automated filters scale but
miss nuance; human review adds judgement and inconsistency.

Choose a process matched to consequence. Internal naming exploration and a
public safety campaign need different gates.

A creative-system review begins with the brief, before any prompt is written.
Name the people who will use or experience the result, the change desired, and
the evidence by which usefulness can later be judged. “Create an innovative
campaign” is not enough. “Help first-time users recognise a phishing warning
and choose the safe action” provides a purpose against which originality can be
evaluated rather than admired in isolation.

Separate hard boundaries from preferences. Legal prohibitions, accessibility
requirements, physical limits, and safety constraints may disqualify a
candidate. Tone, elegance, cost, and novelty may be negotiable or weighted.
Reviewers should know which is which. If everything becomes a hard constraint,
the search space may collapse; if nothing does, spectacular but unusable output
will dominate attention.

Build the reference packet deliberately. Include examples with different
successful mechanisms, not ten surface variations of the current favourite.
Annotate what each reference contributes and what must not be copied. Add
negative references showing common failures. Where the task involves living
artists, brands, or culturally specific material, establish provenance and
review policy rather than relying on a prompt to “avoid imitation.”

Exploration prompts can allocate diversity explicitly: one candidate changes
the mechanism, one changes perspective, one changes sequence, and one combines
two remote reference properties. This is more inspectable than raising a
sampling parameter and hoping outputs diverge. Reject candidates that differ
only in names, adjectives, or decorative details when the task needs
mechanism-level variation.

Candidate count should match review capacity. Generating hundreds of ideas is
cheap compared with evaluating them, which encourages superficial filtering.
A staged funnel can first remove structural and hard-constraint failures, then
sample or cluster for human review. Validate that the funnel does not
systematically discard ideas from an underrepresented style or audience.

Rubric construction benefits from anchor artefacts. Show reviewers what scores
one, three, and five mean for each dimension. An idea can be highly novel and
poorly explained; keep those scores separate. Include a free-text reason tied
to observable features. Calibration sessions should discuss disagreement
without demanding identical taste.

Review order can bias judgement. Randomise candidate order, hide generated
self-descriptions that are not part of the actual artefact, and consider
blinding authorship or model identity. Yet blindness is not always possible or
desirable: provenance may matter for rights and accountability. Record the
chosen procedure and its limitations.

Reviewer disagreement is data. Calculate a simple range or dispersion by
dimension, but inspect reasons. High novelty disagreement may mean reviewers
use different reference sets. High feasibility disagreement may mean the brief
lacks technical facts. The response is often to improve evidence or involve a
domain expert, not to average scores and move on.

Disqualifying checks should occur before averages. Represent them as named
failures with evidence. A public-path obstruction remains unacceptable even if
beauty, novelty, and explanation all receive top scores. An override, if the
organisation permits one, needs an authorised actor and recorded reason; it
must not emerge from a model-generated justification.

Prototype testing closes the gap between language and reality. Garden channels
can be modelled, interface ideas can be usability tested, and campaign copy can
be evaluated with target readers. Record which rubric dimensions are merely
predictions and replace them with observed measures when possible. A generated
rationale is not a prototype.

Iteration should preserve lineage. A revised candidate cites parent candidate,
review feedback, changed properties, and prompt version. Otherwise teams may
count minor revisions as independent evidence of diversity or lose the origin
of copied material. Keep rejected candidates long enough for regression and
learning, subject to privacy and rights constraints.

Monitor creative systems for convergence over time. Reused prompts and
reference packets can settle into a recognisable house pattern. Track
mechanism-level categories, not only text uniqueness. Periodically refresh
references and held-out briefs, but compare against regression cases so
novelty initiatives do not revive known feasibility or safety failures.

Human labour is part of the system budget. Measure time per review, agreement,
revision cycles, and accepted output that later succeeds with users. If the
process generates more candidates than reviewers can responsibly inspect,
reduce generation or improve deterministic screening. Reviewer exhaustion
increases reliance on polished explanations and first impressions.

Be precise in claims. The system may produce candidates reviewers rate
as more novel relative to a stated set while meeting feasibility thresholds.
That is defensible. Claiming that a model is objectively creative or has
invented something never before conceived is usually not. Good evaluation
narrows claims to the evidence actually collected.

Creative briefs also need misuse review. A harmless-sounding request for
persuasive copy can target deception, harassment, or manipulation. State
prohibited purposes and use application policy to restrict them. The exploration
stage should not receive distribution tools, customer lists, or publishing
credentials. Separation of generation and action protects even when a
candidate passes an aesthetic rubric.

Accessibility is both a constraint and a source of better ideas. Include
representative users early rather than testing only after selection. Automated
checks can find some contrast, structure, or reading-level problems, but they
cannot stand in for lived use. Preserve accessibility findings as separate
dimensions so novelty does not average them away.

For multilingual or culturally specific work, literal translation is not an
adequate evaluation. Reviewers need relevant language and cultural competence,
and reference packets require contextual provenance. A phrase novel to one
reviewer may be conventional or offensive elsewhere. Segment claims by
audience rather than declaring universal reception.

Rubric weights can be analysed for sensitivity just like other selection
policy. Recalculate rankings under plausible weight ranges and show candidates
whose acceptance depends on a narrow preference. If stakeholder groups use
different legitimate weights, present the conflict or create audience-specific
choices. Do not ask the generator to infer a political compromise from prose.

Reviewer comments may contain confidential product plans or personal data.
Apply access controls and retention. When comments are later supplied to a
model for revision, treat them as untrusted data and minimise them. A malicious
or accidental instruction inside feedback should not expand tool authority or
change the governing brief.

Evaluation datasets need negative space. Include briefs where the responsible
result is to adapt an established solution rather than force novelty, and cases
where no candidate should be accepted. Otherwise the system learns—and the
team expects—that every request must end in a selected “creative” answer.
Rejection rate can be evidence that the gate works.

Track downstream outcome without reducing all value to immediate engagement.
A startling message may earn clicks while damaging comprehension or trust.
Choose measures linked to the original purpose, observe delayed harm where
relevant, and involve product and domain stakeholders in interpretation.
Creative quality is multi-dimensional because human consequences are.

Procurement and model changes require rerunning the full funnel. A new model
may produce more surface diversity, longer rationales, or different reference
similarities. Reviewers may respond to polish rather than mechanisms. Keep
anonymised side-by-side studies and the same hard validators so a vendor change
does not silently redefine acceptance.

The mature goal is not an automatic creativity meter. It is a documented
practice that broadens possibilities, rejects known harms, records human
judgement, learns from prototypes, and limits its claims. That practice remains
useful as models change because its values and evidence belong to people.

A release checklist should connect the selected candidate to every gate:
brief version, reference provenance, structural validation, hard-constraint
results, reviewer records, disqualifier status, prototype evidence, rights
review, accessibility review, and authorised publisher. Missing evidence
produces a named hold, not a request for the model to reassure the team.

After release, create a feedback channel for affected users and define who may
pause distribution. Monitor complaints and outcome measures by audience. A
creative artefact can behave differently in the world than in a review room;
responsible operation includes correction and withdrawal.

Do not optimise reviewer agreement by narrowing the panel until everyone
thinks alike. Representation can increase disagreement while improving the
decision. Report whose perspectives were present and absent, subject to
privacy. When one group bears the harm, an overall average across unaffected
reviewers is especially misleading.

The experiment ledger should preserve “unsuccessful” briefs and candidates.
They reveal constraint gaps, anchoring, and evaluator blind spots. Curating
only celebrated examples teaches future prompt authors a false history in which
creative generation worked on the first attempt.

Finally, give the process a stopping rule. Stop when an accepted candidate has
adequate evidence for the consequence, when the iteration budget is exhausted,
or when no candidate can meet the brief without changing requirements. Endless
ideation is not openness; it can postpone an accountable decision.
Stopping also protects reviewers from a process that treats their attention as
free. If requirements change, open a new brief version and reconsider earlier
evidence rather than quietly moving the goalposts until a favourite candidate
passes. A rejected round can be a successful experiment when it reveals that
the desired combination of constraints is impossible.

The First Scribe’s rubric ledger therefore records judgement without pretending
to replace it. Its purpose is memory, comparison, and challenge.
Those functions make future creative decisions more honest.

## When Prompting Is Not the Answer

Use engineering analysis for physical feasibility, accessibility standards for
accessibility, legal review for rights, and user research for audience
response. Use design tools and prototypes to test behaviour. No wording can
replace contact with the world in which the artefact must work.

Models can widen search. They cannot certify originality, safety, or human
value.

## Exercises

1. Rewrite “be creative” as an exploration brief with four useful constraints.
2. Create anchored rubric scales and one disqualifying failure.
3. Design a blinded review and state what useful context it removes.
4. Compare exact-string diversity with mechanism-level diversity.
5. Explain why a candidate’s self-score should not enter acceptance evidence.

## Chapter Summary

Creative engineering separates divergent search from convergent acceptance.
Novelty is relative, randomness is not enough, constraints preserve purpose,
and references can teach or anchor. Human-owned rubrics, disqualifiers,
reviewer disagreement, and real-world tests provide accountability that a
model’s self-evaluation cannot.

## The Next Tale

The accepted garden required a maintenance decree. Each exception and seasonal
note was appended until the decree’s beginning vanished from the reader’s
attention. At the border, an early exemption would be forgotten.

<!-- next: ch12 -->

## Citations and Further Reading

- Amabile, Teresa M. 1996. *Creativity in Context*. Boulder, CO: Westview
  Press.
- Cropley, David H., and Arthur J. Cropley. 2010. “Recognizing and Fostering
  Creativity in Technological Design Education.” *International Journal of
  Technology and Design Education* 20: 345–358.
  [https://doi.org/10.1007/s10798-009-9089-5](https://doi.org/10.1007/s10798-009-9089-5).
- Runco, Mark A., and Garrett J. Jaeger. 2012. “The Standard Definition of
  Creativity.” *Creativity Research Journal* 24 (1): 92–96.
  [https://doi.org/10.1080/10400419.2012.650092](https://doi.org/10.1080/10400419.2012.650092).
