# Concepts to Review (running list — mistakes made + new things learned)

*(Not analysis findings — those live in `02_EDA_Notes.md`. This is a skills/revision log.)*

## Pandas — habits that bit me more than once

- **Reassignment.** `dropna()`, `unstack()`, `reset_index()`, `sort_values()` — none of these modify a dataframe in place. They return a *new* object. Either `df = df.method()` or pass `inplace=True`. This was my #1 recurring bug today — check for the `=` sign every single time before running a transforming cell.
- **Parentheses on method calls.** `df['col'].isnull` (no `()`) returns the method itself, not a result. Always `isnull()`.
- **Column names need quotes.** `df['MMSE']` not `df[MMSE]` — unquoted text is read as a variable name, not a string.
- **Grouping by multiple columns needs a list.** `df.groupby(['Subject ID', 'stage'])`, not two separate arguments.
- **`SettingWithCopyWarning`.** When filtering (`df[condition]`), pandas can't tell if the result is an independent copy or a view into the original. If you're going to modify the filtered result, make it explicit: `df[condition].copy()`.
- **`.rank()` ≠ `.sort_values()`.** Rank just labels each row 1st/2nd/3rd — it doesn't reorder anything. Sorting actually reorders rows.
- **`np.where(condition, value_if_true, value_if_false)`** — vectorized if/else applied across a whole column at once. Condition goes in slot 1 only; slots 2 and 3 are plain output values, not more conditions.

## Seaborn / plotting

- `regplot()` has no `hue` — it's axes-level, one line only. `lmplot()` is figure-level and supports `hue` (separate line + color per group).
- `sns.lineplot()` without `hue` or `units` defaults to averaging *everyone* into one summary line + confidence band. To draw raw individual lines (e.g. one per subject) without color-coding: `units='Subject ID', estimator=None`.
- Confidence interval band ≠ p-value / significance test. It's the range where the *true average line* likely sits — wider = less data in that region, not "less significant."
- `sns.distplot` is deprecated — use `histplot` or `displot`.
- Matplotlib not rendering inline: check `%matplotlib inline` was actually *run* (not just present), check the kernel matches the environment packages were installed in, try `plt.show()` explicitly, check `matplotlib.get_backend()`.

## Analytical reasoning — the recurring themes

- **Rows ≠ subjects.** `value_counts()` on a longitudinal dataset counts visit-rows, not people. A subject with more visits contributes more rows. Always check whether a stakeholder-facing number needs a subject-level count instead (`nunique()`).
- **Don't invent a clinical story a number doesn't support.** ("Maybe they passed away," "recently diagnosed," "lived longest with the disease.") If it's not something the data can actually show, say what the data *can* defensibly say instead.
- **Selection bias.** Dropping data because it "doesn't look dramatic enough" changes what population the analysis is really describing.
- **Pooled averages hide within-subject trends — and this pattern recurs in disguise.** Averaging a repeated-measures variable across many different people can mask real change happening *within* one person over time. Caught this twice today in two different forms: (1) the `Group` column applies to a subject's *entire* visit history, blending pre- and post-conversion MMSE together (Phase 1). (2) Raw *visit number* doesn't align to the same disease stage across different Converted subjects either — some convert by Visit 2, others not until Visit 4 — so grouping by visit number blends pre-/post-conversion subjects together all over again, even after already fixing issue (1). Lesson: fixing a pooling artifact on one axis (Group) doesn't mean another axis (visit number) isn't hiding the same problem. A paired/within-subject comparison anchored to each subject's *own* transition point (like the CDR ≥ 0.5 threshold) is more reliable than pooling by any axis that isn't synced per-subject.
- **Match comparison groups before trusting a visual difference.** Check both groups span a similar range (e.g. age) on the thing you're not testing, before attributing a gap to the thing you are testing.
- **Small-N noise ≠ real reversal.** A single uptick in a declining biological measure (like the nWBV "improvement") is much more likely measurement noise than a real biological change, especially with only 2-4 data points per subject.

## SQL / database design (new today)

- **Primary key** = uniquely identifies a row *within its own table*. **Foreign key** = a column that points to another table's primary key, linking the two tables together. (Mixed these up twice — a foreign key doesn't define a new column, it references one that already exists.)
- **Normalization rationale** = same "row vs. subject" idea as the pandas work, just in SQL form: split subject-level (constant) facts into one table, visit-level (changing) facts into another, so nothing gets redundantly repeated.
- **Reserved words** (like `GROUP`) need square brackets — `[Group]` — anywhere used as a column name in SQL Server.
- **No trailing comma** before the closing parenthesis in `CREATE TABLE`.
- **Column names must match exactly, underscores included**, between tables — `Subject_ID` (source table) and `subjectID` (my own table) are different identifiers to SQL Server even though they look similar.
- **`JOIN`** combines rows from two tables based on a matching column between them — needed whenever the columns you want are split across normalized tables (e.g. Group lives in Subjects, nWBV lives in Visits).
- **Public network access / firewall rules** sit *above* individual firewall IP rules on Azure SQL — if "Deny public network access" is Yes, no firewall rule matters until that's flipped.
