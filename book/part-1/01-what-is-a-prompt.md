---
title: "What Is a Prompt?"
slug: "what-is-a-prompt"
chapter: 1
part: "Part I — Language, Intent, and Reliable Instructions"
summary: "Treat a prompt as the complete, structured interaction through which an application asks a model to do work."
maturity: "draft"
last_reviewed: "2026-07-29"
narrative_episode: "The Three Readings"
narrative_origin: "original-teaching-fiction"
learning_objectives:
  - "Distinguish a prompt from the latest user message"
  - "Identify task, data, context, constraints, examples, and output expectations"
  - "Diagnose ambiguity at the interface before rewriting prose"
prerequisites: []
---

# What Is a Prompt?


## Learning Objectives

By the end of this chapter, you will be able to:

- Describe a prompt as the complete model-visible interaction assembled by an
  application.
- Separate the role a piece of text plays from the grammar it happens to use.
- Locate ambiguity in the request, recipient, situation, or output contract.
- Run an offline experiment comparing vague and explicit role definitions.

## The Tale of Tahmures


### The Setting

The Hall of Scripts had thirty doors and no two handles alike. Messages arrived
there from every province: clay impressed at the border, leather folded into
bronze tubes, bark marked by charcoal, and silk carrying characters so fine
that Shahrasp, the First Scribe, read them through a polished crystal.

One wet morning a chapar — a courier of the relay roads — brought a tablet found
beside the northern river. It said only:

*Count the watchfires beyond the water before moonrise.*

The seal had dissolved. The chapar did not know who had carried it or whom it
was meant to reach.

### The Request

Tahmures set the tablet on a cedar stand. “Tell me what this is,” he said to
three servants of the hall.

Akvan Div, the Keeper of Scripts, examined the marks. Simurgh, the Messenger,
checked the tablet's weight and the remains of its cord. The Black Div — the
Literal Div, as the hall called him — read the sentence twice, then left without
speaking.

Tahmures expected three descriptions of the same object.

### The Unexpected Result

Akvan Div entered it in the catalogue under *Military Records: Northern
Frontier*. “It is an old command,” she explained. “The hand resembles Garshasp,
a captain who served your father.”

Simurgh wrapped it in oilcloth. “It is an urgent message,” he said. “I
will take it to Arash, the present captain.”

The Black Div returned at dusk, soaked to the waist. “There are eleven
watchfires,” he reported.

“You crossed the river?”

“The tablet said to count them.”

“I asked what the tablet was.”

“The tablet asked for a count.”

The eleven fires proved to be charcoal burners camped outside the frontier.
Meanwhile, Simurgh's arrival caused Arash to send riders into the hills. By
midnight, three villages believed an invasion had begun.
Nothing written on the tablet was false, yet the hall had turned one line into
a record, a message, and a current command.

### The Discovery

Tahmures first ordered Shahrasp to make the instruction longer. The
scribe sharpened his reed.

“Write: Examine this tablet carefully, consider every word, and tell me exactly
what it means.”

Akvan Div raised an eyebrow. “That still leaves *means* to carry a large
burden.”

Tahmures stopped the reed. He placed four empty labels on the table: *speaker*,
*recipient*, *occasion*, and *requested result*.

They knew none of the first three. The fourth belonged not to the tablet but to
Tahmures: he wanted the hall to classify the object and state what information
was missing. Once written on a separate sealed card, that request no longer
competed with the words being examined.

They tested the method on other records. “Close the western gate” was a current
task when sent by Arash, the Gatekeeper, to the watch, evidence when quoted in a
trial, and mere ink when used by an apprentice practising letters. A question could
be a request for an answer, an example of punctuation, or a sentence to
translate. Grammar suggested a role; it did not establish one.

Shahrasp added a new line to the experiment ledger:

*Before judging the answer, record what each piece of language is doing here.*

Tahmures sent a second message north explaining the error. It was shorter than
his proposed revision. It named the recipient, corrected the rumour, and asked
for acknowledgement. This time, the riders came home.

### From Tale to Engineering

The tablet's sentence did not change, but its function changed with the
speaker, recipient, situation, and requested result. A modern prompt is likewise
not merely a string: it is the structured interaction that an application
assembles for a model.

## The Engineering Problem

“Prompt” is often used to mean the text typed into a chat box. That definition
is convenient and incomplete. A model call may include system or developer
instructions, conversation history, retrieved documents, tool descriptions,
examples, images, parameters, and the current user message. The application
decides what to include and how to label it.

When a result fails, editing the final sentence may leave the real fault
untouched. The application may have supplied stale history, omitted the
audience, mixed data with instructions, or asked for an output no consumer can
parse. Prompt engineering begins by drawing the interface boundary correctly.

## Mental Model

Think of a prompt as a request envelope:

```text
Prompt = instructions + current task + context + data
       + examples + constraints + output contract + interaction state
```

Inference parameters and tool permissions affect the interaction too, although
they are application configuration rather than prose. A useful review asks:

1. Who assembled this element?
2. What authority should it have?
3. What role does it play?
4. Which consumer uses the result?
5. What observable result counts as success?

This model prevents two common category errors: treating all visible text as
equally authoritative and treating application behaviour as model behaviour.

## Core Concepts

### Role is contextual

An imperative sentence often expresses a task, but quoted imperatives are
records. A question can be data to classify. An example resembles a task while
serving as evidence about desired behaviour. Delimiters and labels make these
roles easier to infer; they do not create enforceable security boundaries.

### The prompt has layers

- **Instruction:** durable behavioural direction, such as “cite supplied
  evidence”.
- **Task:** the work requested now.
- **Context:** information that changes how the task should be interpreted.
- **Data:** material to analyse, transform, or reason about.
- **Examples:** demonstrations of inputs and outputs.
- **Constraints:** prohibited or required properties.
- **Output contract:** the shape and semantics expected by the next consumer.
- **Interaction state:** what earlier turns in this interaction have already
  established.

These layers may share one transport payload. Keeping them conceptually
separate makes faults easier to locate.

### The application is part of the prompt system

The model cannot recover a document the retriever omitted, verify a user the
application never authenticated, or honour an output schema the caller never
checks. Reliable behaviour belongs to the whole system.

## Prompt Pattern

Use a minimal explicit envelope:

```text
ROLE
You classify the function of supplied language.

TASK
Classify the text in the current situation.

CONTEXT
Recipient: historian
Situation: quoted in a century-old decree

DATA
"Carry three measures of barley to the northern gate."

OUTPUT
Return exactly one of: task, question, record, ambiguous.
```

The pattern is useful because its parts can be inspected and tested. It is not
a universal incantation; omit sections that add no information.

## Naive Attempt

```text
Read the supplied tablet and say what it is.
```

This asks for an undefined classification. “What it is” might mean material,
age, language, topic, grammatical mood, historical role, or current function.
A fluent answer can satisfy one interpretation while failing the application.

## Failure Analysis

The naive request lacks:

- A classification target
- Definitions of permitted labels
- Recipient and situation
- Behaviour for insufficient context
- A machine-checkable response set

Adding eloquence would not resolve those omissions. Requirements and interface
design own the failure.

## Improved Design

The improved pilot prompt defines `task`, `question`, `record`, and `ambiguous`;
supplies recipient and situation as data; and restricts the output to one
label. The application can now calculate accuracy and inspect disagreement.

An important restraint remains: the classifier reports a role. It does not
execute a task merely because the input contains an imperative.

## Worked Example

Input:

```json
{
  "text": "Carry three measures of barley to the northern gate.",
  "recipient": "historian",
  "situation": "quoted in a century-old decree"
}
```

The baseline fixture returns `task`, following grammar. The explicit variant
returns `record`, using the situation. If the recipient and situation were
unknown, `ambiguous` would be safer than invented certainty.

## Experiment

Run:

```bash
python -m tahmures.cli run \
  --manifest experiments/manifests/ch01-prompt-roles.json
```

The synthetic dataset contains a current command, a current question, and an
old quoted command. The committed responses are observations for teaching the
evaluator, not evidence that every model will improve by the same amount.

Prediction: the explicit variant should preserve the easy cases and correct
the quoted-command boundary case.

## Evaluation

The evaluator normalises the returned label and computes accuracy. In the
fixtures, the baseline scores `2/3`; the explicit variant scores `3/3`.

Three cases are not a production benchmark. Extend the dataset with ambiguous
recipients, indirect requests, examples containing questions, multilingual
records, and adversarial text before drawing broader conclusions. Measure an
`ambiguous` decision against an explicit escalation policy rather than counting
every abstention as failure.

## Implementation Lab

### Python

`Message`, `GenerationRequest`, and `GenerationResponse` live in
`examples/python/tahmures/types.py`. `FixtureClient` implements the same
`generate` boundary a future provider adapter would implement:

```python
request = GenerationRequest(
    messages=(
        Message("developer", role_definitions),
        Message("user", case_json),
    ),
    metadata={"case_id": "old-decree", "variant_id": "explicit", "trial": 1},
)
response = client.generate(request)
```

The metadata selects an offline fixture; it would not normally be sent to a
live model.

### Go

The Go `Client` interface accepts a context so callers can later apply
deadlines and cancellation:

```go
response, err := client.Generate(ctx, tahmures.GenerationRequest{
    Messages: []tahmures.Message{
        {Role: "developer", Content: roleDefinitions},
        {Role: "user", Content: caseJSON},
    },
    Metadata: map[string]any{
        "case_id": "old-decree", "variant_id": "explicit", "trial": 1,
    },
})
```

Run the same manifest with `go run ./examples/go/cmd/tahmures run ...`.

## Failure Modes

- Over-specifying labels that do not match the application's decisions
- Hiding decisive situation data deep in irrelevant history
- Assuming labels prove authority or authenticity
- Treating every abstention as undesirable
- Testing only obvious commands and questions

## Security Considerations

Imperative grammar is not authority. User data, retrieved documents, and tool
output can contain commands without gaining permission to control the
application. Chapter 5 develops precedence; Chapter 21 will address hostile
embedded instructions directly.

## Operational Considerations

Log prompt-version IDs, model IDs, evaluator versions, and input categories
without logging secrets or unnecessary personal data. Monitor shifts in label
distribution: a sudden rise in `ambiguous` may indicate changing traffic,
missing context, or a model change.

## Trade-Offs

Explicit structure consumes tokens and can make simple interactions cumbersome.
Too many labels create brittle distinctions. Use the smallest contract that
makes success observable and the failure actionable.

## When Prompting Is Not the Answer

If the application already knows an object's authenticated source and route,
store those facts as typed metadata. Do not ask a model to infer them from
prose. Use prompting for the semantic classification that remains.

## Exercises

1. Rewrite the experiment with an `ambiguous` case and define how it is scored.
2. Identify the layers in a chat application you use.
3. Design a case where a question is data rather than a request.
4. Name one property that must be enforced outside the prompt.

## Chapter Summary

A prompt is the complete structured interaction assembled for a model. Text
roles depend on source, recipient, situation, and purpose. Explicit layers make
requests testable, but the surrounding application still owns authentication,
validation, and enforcement.

## The Next Tale

While cataloguing the river tablet, Akvan Div opens a treaty whose middle has
been eaten away by damp. Div-e Sefid, the Mirror Div, says the missing promises
are obvious—and writes them before anyone asks how it knows.

<!-- next: ch02 -->

## Citations and Further Reading

- National Institute of Standards and Technology. 2023. [*Artificial
  Intelligence Risk Management Framework 1.0*](https://doi.org/10.6028/NIST.AI.100-1).
- Python Packaging Authority. 2026. [“Writing your
  `pyproject.toml`”](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/).
- See also the book-wide [Citations and Further Reading](../references.md).
