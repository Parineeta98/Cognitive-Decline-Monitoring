# OASIS-2 Dementia Progression Project — Overview

**Roadmap slot:** Week 6 (Jul 13–19), Data Analyst 3-Month Roadmap
**Domain:** Healthcare / Neuroscience
**Dataset:** [OASIS-2 Longitudinal Scan Data](https://www.kaggle.com/datasets/nadiatriki/oasis-2-longitudinal-scan-data) (Kaggle: nadiatriki/oasis-2-longitudinal-scan-data)

---

## Why this project

- Diversifies the portfolio — the other two projects (Farmer's Market, Kaggle Retail) are both retail/sales flavored. This is healthcare/neuroscience.
- Directly reinforces the neuroscience → analytics career narrative (needed for Week 9 interview prep: 90-second story).
- Tabular, MRI-*derived* features — no raw imaging/signal-processing pipeline needed, so it fits a one-week build.
- Deliberately framed as a **BI/stakeholder analytics** project, not an ML prediction project — most public use of this dataset goes the ML/classification route. Reframing it as an operations/monitoring question for a memory clinic is the differentiator.

## Dataset at a glance

- 150 subjects, aged 60–96, each scanned on 2+ visits ≥1 year apart
- 373 total imaging sessions/visits
- 72 subjects nondemented throughout; 64 demented at first visit and remained so (51 with mild-to-moderate Alzheimer's); remainder converted from nondemented to demented during the study

## Business question

> Which demographic and MRI-derived brain measures track with dementia progression across visits, and what should a memory clinic's monitoring/intervention protocol look like as a result?

## Deliverables (revised Jul 9 — full pipeline milestone project, not just Python + Power BI)

- [ ] Python analysis (pandas, seaborn) — cleaning, EDA, trends, group comparisons
- [ ] Load cleaned data into Azure SQL DB + analytical SQL queries
- [ ] Power BI dashboard connected via SQL (DirectQuery/Import), DAX-driven measures
- [ ] Stakeholder insight summary: 3 findings + 3 actions
- [ ] Push to GitHub with README (matches existing project pattern)
- [ ] Add to portfolio site alongside the other two projects

See `04_Project_Plan.md` for the phase-by-phase schedule.

## Status log

- **Jul 9:** Domain + dataset chosen (revised same night from a generic healthcare dataset to this one, at her request, to use her own background). Vault created.
- **Jul 9 (later):** Scope revised to a full Python + SQL + DAX + Power BI pipeline project at her request — reuses the existing Azure SQL DB from the AZ-900 sprint and finally exercises the un-assessed PL-300 skill "SQL in Power BI." Phase plan added (`04_Project_Plan.md`), tasks created.
