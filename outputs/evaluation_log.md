# Evaluation Log

## Checks run (see notebooks/SmartPickAI_PJ1.ipynb)
- All 5 persona weight sets add up to exactly 100% (asserted in the notebook).
- Budget / RAM / storage filters verified: every returned phone respects all three limits.
- Cleaning verified on all 413 rows: price ($ and commas removed), storage ('128', '256GB', '1TB' -> GB), 28 processor strings mapped to a score.
- Streamlit app smoke-tested for all 5 personas with no errors.
- Web frontend: top-5 names and scores for all 5 personas match recommendation.py exactly (tested in a simulated browser).
- Frontend bug caught during testing: weight names differed between Python (storage_gb, processor_score) and the page (storage, processor), which silently dropped two weights. Fixed by mapping names in build_frontend.py.

## One thing the AI got wrong, and how it was caught
While adapting the code to the real dataset, the AI "corrected" the keyword `heilo` to `helio`
(assuming a typo). Profiling the real data showed the dataset itself spells it "Heilo"
(e.g. `Heilo80P`), so the original keyword was right and the "fix" would have scored those phones as
unknown. Fix: match both spellings. Lesson: check assumptions against the actual data.

## Findings / limits
- 276 of 413 phones (67%) have processor "not mentioned", so they get a penalised score of 0.3.
- `Gen8`, `MediaTek` and `Snapdragon1P` are ambiguous names; they were scored 0.8, 0.5 and 0.5.
- Gamer and Business Professional return the same top 5 because their weights are similar
  (processor 35% vs 30%, RAM 30% vs 20%, battery 20% vs 30%). Widening the gap, e.g. giving Business
  more battery/price weight, would separate them.
