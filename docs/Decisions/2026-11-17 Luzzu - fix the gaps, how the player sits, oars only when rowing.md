---
type: decision
date: 2026-11-17
topic: Maltese Life
quote: "two issues popped up. 1: the luzzu model has gaps at the front and back on both sides a couple of pixels (or 1 pixel) big which allows you to see into the floor, two: the player model's feet when in the boat stick out of the front, see how we can change how the player sits. 3: the oars should be hidden when the boat isnt in motion"
---
# 2026-11-17 Luzzu: fix the gaps, how the player sits, oars only when rowing

> two issues popped up. 1: the luzzu model has gaps at the front and back on both sides a couple of pixels (or 1 pixel) big which allows you to see into the floor, two: the player model's feet when in the boat stick out of the front, see how we can change how the player sits. 3: the oars should be hidden when the boat isnt in motion

Found while playing the accepted luzzu in the owner's test instance:
1. **Gaps:** 1 to 2 px holes at both ends of the floor, on both sides, where you can see through the hull. Close them.
2. **Feet stick out of the front:** change how players sit in the luzzu so their legs stay inside the hull.
3. **Oars:** hidden while the boat is still; shown only while rowing.
