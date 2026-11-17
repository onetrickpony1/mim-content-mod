---
type: "topic"
---
# Keeping the vault up to date

After every change (a design, an owner decision, code):

1. **The note's fields** (`status`, `tier`): change them in the one note the change is about. Don't copy facts into a second note; link to it.
2. **An owner decision** gets a note in `Decisions/` with the owner's exact words (template [[Templates/Decision|Decision]]). Decision notes are never edited: a new one replaces an old one and links back.
3. **Where a new note goes:** the folder of its subject. A note that belongs to two subjects goes where it mostly belongs and is linked from the other subject page.
4. **Lists before notes:** an item lives as a line in its list until it is agreed for building. Then it gets its own note ([[Templates/Item|Item]]) and the list line links to it.
5. **When something is built:** set the item's `status` to `built` and fill in its `id` (the mod's item or entity id).
6. **Food art accepted by the owner:** add it to [[Food in the mod]], move its row from **Not yet** to **In the mod** in [[Food progress]], and re-run `art/tools/doc_pictures.py` for its picture.
7. **[[STATUS]]** is updated whenever what's in progress or waiting changes.
8. **Git:** commit the docs with the change they describe, one subject per commit, staging files by name.

**Status values:** `idea` → `open` (being designed or waiting on the owner) → `planned` (agreed) → `built` → `dropped`.
