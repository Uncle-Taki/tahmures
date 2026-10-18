# Incorrect GLM candidate: three lossless transfer ZIPs

Extract incorrect-glm-candidate-part-01.zip, -part-02.zip and -part-03.zip
into the SAME empty directory. Each is an ordinary independent ZIP.
Part 01 contains the directly usable project files, Persian movie and the
first English-movie chunk. Parts 02 and 03 contain the remaining chunks.
The English AVI is split because it alone compresses to over 100 MB.
Chunks are binary fragments, not playable clips or source files for Gemini.

After extracting all three ZIPs, run from the extraction directory:

    python3 restore-incorrect-candidate.py

Requires Python 3.11+ standard library. The helper verifies chunks, reconstructs
the original English AVI without re-encoding and checks all 140 original files.
It refuses to overwrite a differing existing movie. Original chunks remain.
For code/art diagnosis the project in part 01 can be inspected without restoring
the English AVI. Preserving this rejected candidate does not approve its output.

All three ZIPs are below 100,000,000 bytes. Size alone does not make them Gemini
compatible: video inside ZIPs and file-count limits still apply. If unsupported,
attach extracted images/text/code in batches and videos separately.
