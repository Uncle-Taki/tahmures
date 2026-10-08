# Semantic character and location migration

An audit proposes changes; it does not apply them. The frozen English source,
accepted narrative register, chapter hooks, technical contracts, and current
human-review work remain protected until a scoped owner-approved revision.

For each current character or location record: name, chapters, narrative
function, relationship to Tahmures, mythic tier, technical causal role,
English/Persian naming, continuity dependencies, and risk. Then ask:

1. What exact action does this actor perform in the tale's failure and remedy?
2. Is an existing canonical or project-fiction character naturally suited to
   that action? Does replacement alter their identity or chronology?
3. Is a stable unnamed court/craft role clearer and less costly than a name?
4. Does a rename change the engineering metaphor, agency, chapter hook, or
   already human-reviewed Persian wording?

Allowed proposed actions: `KEEP`, `RENAME`, `REPLACE_WITH_TAHMURES`,
`REPLACE_WITH_SHAHRASP`, `REPLACE_WITH_HUSHANG`, `REPLACE_WITH_JAMSHID`,
`REPLACE_WITH_DIV_ROLE`, `REPLACE_WITH_UNNAMED_COURT_ROLE`,
`LOCALIZE_PLACE`, and `DEFER`. Prefer `KEEP` where a role already teaches
correctly. Do not replace the First Scribe with Shahrasp merely to increase
mythic names, or a permission owner with a div merely for drama.

Before any implementation, make a per-scene source/target function map,
obtain the needed narrative/chronology approval, edit canonical English in a
small batch, preserve the technical bridge, update `book/narrative-continuity.md`
in the same batch, verify the diff, then synchronize Persian against stable
English and route affected human-review evidence. No name swap is complete
until the causal lesson and both editions still agree.
