# Akvan Div — live Blender blockout

Final candidate: **akvan_div_base_v02.blend**. Open in Blender 5.3.0 and select scene Akvan_Inspection_v01 if needed. Original Scene is preserved. v01 and session_before_build_v01.blend are historical snapshots.

Review front_v01.png and three_quarter_v01.png. The reference is packed, locked and hidden in the clean viewport; unhide Akvan_ApprovedMaster to compare. Two named cameras provide front and three-quarter views. 03_Armature is reserved and empty.

Read connection-audit.md, build-validation-report.md, shot-contract-v01.md, and 09_CONTINUITY_AUDIT.md. Machine evidence is validation-v02.json and saved-file-audit-v02.log. New 3D work awaits human approval.

Recheck non-destructively from repository root:

```bash
/home/mehdi/.local/bin/blender-5.3 --background Characters/blender/akvan_div/akvan_div_base_v02.blend --python Characters/blender/akvan_div/inspect_saved.py
```

build_geometry.py regenerates reviewed six-object JSON execution payloads and geometry-source.json. It does not modify Blender until each code payload is reviewed and submitted through the local execution tool. Materials must already exist; saved project contains them. Payloads update meshes in place with bmesh.to_mesh and assign materials after slots exist. Never replay against unrelated scenes without a versioned snapshot. Studio and material settings are recorded in the saved editable project and report. Save new versions through the dedicated bridge route; do not overwrite these files.
