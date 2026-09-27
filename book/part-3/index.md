---
title: "Part III — Context, Memory, Tools, and Agents"
summary: "Place model interaction inside governed systems for knowledge, state, capability, autonomy, and transfer."
---

# Part III — Context, Memory, Tools, and Agents

Part III moves from bounded interactions to controlled application systems.
Tahmures learns that useful language must travel through explicit boundaries:
context construction, evidence retrieval, memory policy, tool authorisation,
agent control, and typed hand-offs.

The learning arc is:

1. [Context Engineering](13-context-engineering.md) constructs a sufficient,
   scoped, and traceable working set.
2. [Retrieval-Augmented Generation](14-retrieval-augmented-generation.md)
   separates retrieval quality, evidence validity, and answer quality.
3. [Memory and State](15-memory-and-state.md) governs writing, recall,
   correction, expiry, and deletion.
4. [Tools and Permissions](16-tools-and-permissions.md) gives generated
   proposals only the capability an application explicitly authorises.
5. [Agents and Termination](17-agents-and-termination.md) bounds iterative work
   with current goals, budgets, cancellation, and terminal states.
6. [Hand-offs and Multi-step Systems](18-hand-offs-and-multi-step-systems.md)
   preserves constraints, authority, provenance, and uncertainty across
   component boundaries.

All six experiments run offline against synthetic datasets and recorded
fixtures. Python is the canonical teaching implementation; Go preserves the
same observable contracts and report metrics.
