---
type: "topic"
---
# Art pipeline

How the mod's art is made and checked (since the art pilot, 2026-11-17). The details are in `art/README.md` and `art/STYLE.md` in the repo.

1. **Reference photos** of the real thing (Wikimedia Commons, licences recorded).
2. **Scripts make the art**: textures from shape, light, palette and noise rules; models from box geometry. Nothing is painted by hand, so everything can be re-made.
3. **Measured against vanilla**: colours, contrast, outline and light direction are kept inside vanilla's own numbers.
4. **Seen in the game**: `tools/run-art.sh` builds the mod and takes screenshots on an invisible desktop (never on the owner's screens), beside vanilla blocks and items.
5. **Judged by an independent reviewer** (a sub-agent), never by whoever made it (owner, 2026-11-17). Fixes follow the review, then it is reviewed again.
