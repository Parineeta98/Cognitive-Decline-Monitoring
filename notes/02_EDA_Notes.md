# EDA Notes (fill in as you go)

## Step 1 — Load & shape

- `df.shape` → 373, 15
- `df.info()` → 373 entries, 15 columns, 3 dtypes: float, int and object
- `df.isnull().sum()` → null values in SES- 19, MMSE - 2
- SES: excluded from analysis entirely — out of scope for this business question, not a data-quality call. Left untouched in the dataframe.
- MMSE: dropped the 2 rows with missing MMSE (`df.dropna(subset=['MMSE'])`), not the subjects they belong to. Both nulls traced to one subject (OAS2_0181), visits 2 and 3 — visit 1 had a valid MMSE (26) and was kept. Rule applied: scope exclusion to what the row is missing, not to the whole subject, unless a specific analysis (e.g. a per-subject trend) requires complete visit history.
## Step 2 — Group distribution

- `df['Group'].value_counts()` →
- Split of Demented / Nondemented / Converted →
Group 
Nondemented 190 
Demented 146 
Converted 37
`df['Group'].value_counts()` → Nondemented 190, Demented 144, Converted 37 rows — but these are visit-rows, not subjects. Project overview lists actual subject counts as 72 / 64 / 14. A subject with more visits contributes more rows, so row counts overstate group size by ~2–2.6x. Use subject-level counts (`nunique('Subject ID')` per group) for any stakeholder-facing percentage.
## Step 3 — Candidate columns for the business question

Shortlist (5–8 columns most relevant to "what tracks with dementia progression"):

age, mmse, cdr, nWBV, eTIV, asf(could be redundant for analysis), visit, mr delay

## Step 4 — Early observations

*(free-form notes as patterns show up — this becomes raw material for the findings doc)*

- - Grouped means (`Age`, `MMSE`, `nWBV`) by Group: Nondemented has the highest MMSE (~29.2) and nWBV (~0.74); Demented the lowest (~24.5 / ~0.72); Converted sits between but notably close to Nondemented on MMSE (~28.7).
- Converted's MMSE proximity to Nondemented is likely a pooling artifact: the Group label applies to a subject's _entire_ visit history, so Converted rows blend each subject's pre-conversion (still-healthy) scores with their post-conversion (declined) scores. The pooled average masks the within-subject decline — this is why per-subject progression lines (Phase 2) matter more than the group average for this cohort.
- Converted subjects have the oldest mean age (~79.8) — consistent with less time-to-decline for a subject to convert within the study window

**nWBV vs Age by Group (lmplot, hue=Group)**

- All three groups decline with age — expected, normal aging affects everyone.
- Nondemented sits clearly above Demented at the same age — a real, age-independent gap (confirmed fair since Demented/Nondemented have near-identical age IQRs: 71-81 vs 71-82).
- Converted's age distribution skews older (IQR 74-86) — caveat when comparing Converted to the other two groups.
- Converted's nWBV line sits closer to Demented, despite Converted's _MMSE_ average (Phase 1) sitting closer to Nondemented — nWBV and MMSE tell different stories for this group. Likely explanation: structural decline (nWBV) may be gradual and present at every visit, while MMSE stays near-normal longer and drops closer to formal diagnosis. Candidate finding.
- Converted's confidence band widens past ~age 85 — sparse data there, read with caution.

**Per-subject progression lines (Converted, x=MR Delay)**

- General decline across all 14 subjects, but rates vary widely.
- One subject (~0103) showed a mid-study uptick — measurement noise, not real biological improvement; don't over-read single wiggles in small-N longitudinal data.
- Two subjects had notably longer study observation windows (>2500 days) — a fact about follow-up length, not disease duration or survival.

**Early vs. later split (CDR = 0 → "early", CDR ≥ 0.5 → "later")**

- CDR (not nWBV) is the right marker for pre-/post-conversion, since nWBV itself has noise. Likely how the `Group` column was originally derived.
- Pooled histogram of nWBV by early/later was messy/overlapping — pooling across 14 different people mixes in between-person baseline variation.
- Fixed with a paired, per-subject comparison (each subject's own early avg vs. their own later avg): all 14/14 subjects declined — strong, clean finding.
- Decline magnitude varies widely: 0.006 (smallest, OAS2_0118) to 0.044 (largest, OAS2_0133).
- Business angle: a memory clinic can't assume one uniform decline timeline — monitoring frequency may need to be individualized rather than fixed.

**Charts kept:** sorted bar chart of per-subject decline; per-subject line chart.

**MMSE vs CDR (boxplot, x=CDR, y=MMSE)**

- Median MMSE declines as CDR increases (as expected), but CDR 1 and CDR 2 have nearly identical medians (~21) and heavily overlapping ranges — MMSE loses its ability to distinguish mild from moderate dementia once CDR reaches 1+. Business implication: MMSE alone isn't reliable for tracking severity once someone's already diagnosed; other measures (CDR's own criteria, or structural markers like nWBV) matter more at that stage.
- CDR = 0 has a handful of outlier patients scoring notably below their peers (MMSE 25-27 vs. the typical 29-30) — cases where the two assessments disagree. Candidate "watch list" criterion for early follow-up, not necessarily a diagnosis flag on its own.
- Mechanism: CDR only has 4 discrete levels vs. MMSE's 31-point scale — coarse binning naturally pools a wide range of true severity into each CDR bucket, which is why the boxes are so wide and overlapping.

**MMSE by Visit and Group (SQL: JOIN visits + subject_table, GROUP BY visit, subj_group)**

- Visit 1 counts match known subject totals exactly (14 Converted / 64 Demented / 72 Nondemented) — confirms the JOIN and the loaded data are correct.
- Sample size collapses fast as visit number increases: Demented goes 64 → 61 → 15 → 3 → 1 by Visit 5. Visit 4-5 numbers for every group are too thin to trust (as low as n=1 — see the Demented Visit 5 "average" of MMSE 4, which is really just one person's raw score, not an average).
- Within the reliable range (Visits 1-3): Nondemented stays flat (~29, n=72/70/34); Demented shows real decline (25.3 → 24.25 → 24.4, still backed by a decent sample).
- Converted looks flat (~28-30) across all 5 visits instead of declining like Demented. Reason: raw visit number doesn't align to the same disease stage across different Converted subjects — some cross CDR ≥ 0.5 by Visit 2, others not until Visit 4 — so each visit-number bucket blends pre- and post-conversion subjects together. This is the *same pooling artifact* as the Group-column issue from Phase 1, just recurring through a different column. **The CDR-based early/later split is the reliable way to see Converted's real decline; raw visit number is not a valid time axis for this group** (consistent with `01_Dataset_Schema.md`'s original note to use MR Delay, not visit number, as the actual time axis).
- General rule to carry forward: always pair an average with its underlying row count before trusting it, especially at higher visit numbers where the cohort thins out non-randomly.

**Watch-list flag rate by group (SQL: JOIN + WHERE cdr=0 and mmse<28 + GROUP BY subj_group)**

- 11 distinct subjects total flagged (CDR = 0 but MMSE < 28, i.e. the two assessments disagree): 9 Nondemented, 2 Converted. Zero Demented, which makes sense — Demented subjects are CDR ≥ 0.5 from their first visit, so they can't appear in a CDR = 0 filter.
- Raw counts are misleading given very different group sizes (72 Nondemented vs. 14 Converted total). Rate *within* each group: 9/72 = 12.5% Nondemented, 2/14 = 14.29% Converted — comparable rates, not a dramatic difference.
- Caveat: built on small counts (2 and 9 people) — read this as "the pattern shows up at a similar rate in both groups," not a strong predictive signal on its own.
- Business relevance: supports the "watch list" candidate action from the MMSE/CDR boxplot finding. Low MMSE despite a normal CDR isn't unique to people who stay healthy — it shows up about as often among people who go on to convert, which is a reasonable justification for flagging these 11 patients for closer follow-up regardless of their current diagnosis label.

**Demented per-subject nWBV decline, first vs. last visit (SQL: subquery + self-join)**

- Built a self-join comparing each Demented subject's first-visit nWBV to their last-visit nWBV: a subquery finds each subject's MIN/MAX visit number, then `visits` is joined back to itself twice (aliased `v1`/`v2`) to pull the actual nWBV at each of those specific visits.
- Majority of Demented subjects show a clear, real decline — same conclusion as Converted, reinforcing nWBV as a reliable progression marker across both groups.
- Less unanimous than Converted's clean 14/14, though, and now with a clear reason why: Converted's comparison was anchored to each subject's own CDR-based transition point (a real disease milestone — CDR crossing 0 → 0.5). This Demented comparison just uses "whichever visit happened to be first vs. last," with no equivalent anchor, so more of the signal sits close to the measurement-noise floor at the edges.
- OAS2_0181 (the subject with only 1 visit remaining after the Day 1 MMSE-cleaning decision) shows first visit = last visit = same row — excluded from the tally, no real before/after to compare. Good reminder that a data-cleaning decision from early in the project can resurface in unexpected places later.
- ~7 subjects showed very small magnitude changes (0.001-0.008, one even a tiny increase) — likely within nWBV's normal scan-to-scan measurement noise rather than confidently "no decline." Framed as ambiguous at this resolution, not as a contradicting finding.

**ASF vs. eTIV redundancy check (SQL: SELECT eTIV, ASF ORDER BY eTIV)**

- Resolves the open question flagged in `01_Dataset_Schema.md` on day one ("check if ASF is redundant for analysis").
- Near-perfectly monotonic inverse relationship, no scatter: as eTIV decreases, ASF increases consistently across every row. Matches the expected mechanism (ASF scales a raw scan to a reference head size, so a bigger head needs a smaller scaling factor).
- Conclusion: ASF and eTIV are effectively redundant. Dropping ASF from the analysis shortlist and dashboard — keeping eTIV only, since it's also the more directly interpretable of the two (an actual volume vs. an abstract scaling factor).