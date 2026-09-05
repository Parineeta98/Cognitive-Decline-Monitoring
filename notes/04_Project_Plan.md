# Project Plan — Phase Schedule

Mapped to actual free windows (Mon–Wed 9–11:30pm, Thu–Fri flexible, Sat–Sun after 3pm).

- [x] **Phase 1 (Fri Jul 10):** Data foundations — load CSV in pandas, `df.shape` / `.info()` / `.isnull().sum()`, handle missing SES/MMSE (documented decision, not blind dropna), descriptive stats per Group. ✅ Confirmed Jul 13 (done late, in Monday's window — see penalty log)
- [x] **Phase 2 (Sat–Sun Jul 11–12, after 3pm):** Seaborn EDA — nWBV vs Age by Group ✅, per-subject progression lines for Converted ✅ (both raw + paired early/later comparison — stronger than the original ask). MMSE vs CDR — **still missing**. 3 candidate findings — 2 solid ones surfaced (MMSE/nWBV divergence in Converted; 14/14 paired decline), need a 3rd + explicit shortlist before this phase closes.
- [x] **Phase 3 (same weekend):** Load cleaned data into the existing Azure SQL DB (`sb-sql-2026.database.windows.net` / `free-sql-db-5841888`), same pattern as the Farmer's Market ingest. Write analytical SQL queries (avg nWBV by group, MMSE trend by visit, etc.) — real reps toward the 25-problem SQL target, and sets up the Power BI connection.
- [x] **Phase 4 (Mon–Wed Jul 13–15, 9–11:30pm):** Power BI dashboard connected via SQL (DirectQuery or Import — not a flat CSV import). DAX measures for KPI cards (avg nWBV/MMSE by group, % converted), trend line over visits/age, demographics page, filters on Group/Age/SES. Also finally exercises the un-assessed PL-300 skill "SQL in Power BI."
- [ ] **Phase 5 (Thu–Fri Jul 16–17):** Write the 3 findings + 3 actions stakeholder summary (`03_Findings_and_Actions.md`) in business language. Publish the dashboard to Power BI Service. Push notebook + dashboard to GitHub with a README.
- [ ] **Phase 6 (Sat–Sun Jul 18–19):** Add the project to both portfolio sites (corporate + academic). Close out the still-open LinkedIn headline task from Week 5.

## Why the pipeline changed (Jul 9)

Original scope was Python (pandas/seaborn) + Power BI only. Revised same day to a full Python → SQL → DAX → Power BI milestone project, reusing the Azure SQL DB set up during the AZ-900 catch-up sprint instead of leaving it idle. This also closes a gap in the PL-300 assessment table: "SQL in Power BI (DirectQuery, Import)" has been marked as a completed skill for weeks but never actually assessed or exercised in a real project.
