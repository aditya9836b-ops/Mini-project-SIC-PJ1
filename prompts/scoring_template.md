# Scoring Template

1. Filter by max budget, minimum RAM and minimum storage.
2. Min-Max scale every feature in the persona's weight table to 0-1.
3. Invert price (1 - scaled price) so cheaper phones score higher.
4. final_score = sum(weight x scaled_feature) x 100.
5. Rank descending and return the top 5.

## Processor score tiers (heuristic)
| Score | Tier | Matches |
|---|---|---|
| 1.0 | Flagship | Snapdragon 888, 8 Gen 2, 8+ Gen 1, Dimensity 9000 |
| 0.8 | Upper mid-range | Snapdragon 750G, Dimensity 1080, "Gen8" (ambiguous) |
| 0.6 | Mid-range | Snapdragon 720G/695, Dimensity 700/720, Helio ("Heilo" in data) |
| 0.5 | Unrecognised model | "MediaTek", "Snapdragon1P" |
| 0.4 | Entry level | Snapdragon 410/425/439/450, Helio P35 |
| 0.3 | Missing | "not mentioned" (penalised so missing data cannot win) |
