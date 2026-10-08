# Tahmures Media Production Roadmap (Chapters 01--04)

## Decision

Use a hybrid educational animation pipeline.

The project already has scripts, bilingual narration, scene blueprints,
character descriptions, technical diagrams, and subtitles. Production
should optimize for consistency and reuse, not maximum cinematic
generation.

## Recommended Architecture

### 1. Character and Environment Layer

-   Create reusable Tahmures character sheets.
-   Create Keeper and Div variants.
-   Create reusable locations.
-   Store references as the visual source of truth.

### 2. Educational Animation Layer

Use: - Manim - Motion Canvas - Remotion - Python video composition

For: - diagrams - technical explanations - bilingual captions - exact
text rendering

### 3. Cinematic Layer

Use AI video selectively: - entrances - atmosphere - emotional
transitions

Do not generate every scene with AI video.

## Production Tiers

### Tier 1: Pilot

Budget: \$0--10

Create Chapter 01 prototype: - generated images - deterministic
animation - free/local voice

Validate: - character consistency - narration quality - educational
clarity

### Tier 2: Chapters 01--04

Budget target: \$20--30

Use: - 80% deterministic illustration/animation - 20% cinematic AI shots

## Workflow

chapter markdown → media blueprint → scene specification → assets →
renderer → final video

## Responsibilities

GPT: - architecture - quality review - source protection

GLM: - bulk preparation - scene conversion - asset workflows -
validation

Codex: - renderer and automation code

## Execution Order

1.  Freeze media blueprints
2.  Build character bible
3.  Produce Chapter 01 pilot
4.  Review
5.  Create reusable templates
6.  Produce Chapters 02--04
7.  Scale to Chapters 05--24

## Production Philosophy

Target: "animated educational documentary"

not: "AI movie"

The project's value is consistency, teaching clarity, and
world-building.
