# OASIS-2 — Dataset Schema Notes

Fill in / correct these once the CSV is actually loaded — this is a starting reference from the dataset documentation.

| Column     | Meaning                             | Notes                                                                                       |
| ---------- | ----------------------------------- | ------------------------------------------------------------------------------------------- |
| Subject ID | Unique subject identifier           | Repeats across visits (longitudinal)                                                        |
| MRI ID     | Unique scan/session identifier      | One per visit                                                                               |
| Group      | Demented / Nondemented / Converted  | "Converted" = became demented during the study — key group for progression analysis         |
| Visit      | Visit number for that subject       | 1, 2, 3...                                                                                  |
| MR Delay   | Days since first visit              | Use this for the actual time axis, not just visit number                                    |
| M/F        | Sex                                 |                                                                                             |
| Hand       | Handedness                          | Likely low-variance, may not be useful                                                      |
| Age        | Age at visit                        |                                                                                             |
| EDUC       | Years of education                  |                                                                                             |
| SES        | Socioeconomic status                | Categorical scale, check direction (low = high status or vice versa — verify, don't assume) |
| MMSE       | Mini-Mental State Exam score        | Cognitive test, 0–30, lower = more impairment                                               |
| CDR        | Clinical Dementia Rating            | 0 = none, 0.5 = very mild, 1 = mild, 2 = moderate                                           |
| eTIV       | Estimated total intracranial volume | Roughly stable per subject — used to normalize brain volume for head size                   |
| nWBV       | Normalized whole-brain volume       | Key variable — shrinks with age/dementia                                                    |
| ASF        | Atlas scaling factor                | Used to compute eTIV from scan; check if it's redundant for analysis                        |

## Known data quirks to check for during EDA

- [ ] Missing values in SES and/or MMSE (common in this dataset — some subjects have gaps)
- [ ] Whether "Converted" subjects have enough visits before conversion to show a trend (vs. converting on visit 2 of 2)
- [ ] Whether nWBV needs to be examined per-subject (line per subject) rather than pooled, since baseline brain size varies naturally by person
