# Stakeholder Insight Summary 

Audience: memory clinic operations / care team lead (not a technical audience — business language only, matches the style of the Retail Sales project's executive summary).

## Finding 1 — A normal exam doesn't always mean a normal memory score
We compared each patient's clinical exam rating with their memory test score across every visit (SQL), then separately charted brain-scan volume against age by group in Power BI. About 1 in 8 patients with a normal clinical exam still scored lower than expected on the memory test and this shows up at almost the same rate in patients who stay healthy as in patients who later develop dementia. So a low score alone doesn't predict decline. But the brain scans add a piece the memory test misses: volume loss can already be underway while the memory test still looks normal, since the scan picks up physical change earlier than the test picks up symptoms.

## Finding 2 — The memory test stops being useful once someone's already diagnosed
We compared memory test scores across clinical severity levels (Python boxplot). Once a patient has a dementia diagnosis, the memory test can't really tell mild cases apart from moderate ones — the two groups score almost the same on average, with a lot of overlap.

## Finding 3 — Brain volume loss is universal after diagnosis, but the pace is very different person to person
We compared each patient's brain scan from before and after their diagnosis changed, first in Python and then confirmed with a per-patient chart in Power BI. Every single patient who developed dementia during the study showed real volume loss — so the decline itself is something a clinic can count on seeing. But how fast it happened varied a lot: the fastest-declining patient lost volume roughly seven times quicker than the slowest.

What could you do with these findings
---
- flag patients with this normal-exam-but-lower-score combination for a shorter check-in window (say, 6 months instead of a year) rather than waiting for the next scheduled visit to catch a decline the exam alone wouldn't yet show.
- for patients already diagnosed, track how they're doing using the doctor's own clinical rating or a brain scan where available, rather than relying on memory test score changes — past a certain point, the test just isn't sensitive enough to catch further decline.
- move away from putting every patient on the same fixed check-in schedule. Use each patient's own pace of decline to set how often they're seen — more frequent visits for fast decliners, longer gaps for slow ones — which uses clinic time more efficiently without missing the patients who need closer attention.
## Draft one-paragraph summary (for README / portfolio site)

*(Draft below — review once the three findings above are confirmed/edited, then finalize.)*

This project analyzed longitudinal MRI and cognitive assessment data from 150 patients across up to 5 clinic visits to identify how dementia progression shows up in the data available to a memory clinic, and where the standard monitoring protocol could be improved. Three findings stood out: cognitive test scores can look deceptively normal even as structural brain decline is already underway, making a combined CDR-normal/low-MMSE result a useful early flag; the cognitive test loses its ability to distinguish mild from moderate dementia once a diagnosis is made, so progression tracking should shift to other markers at that point; and while brain-volume decline was universal among patients who converted to dementia, the rate varied nearly sevenfold between individuals, arguing for individualized rather than fixed-interval monitoring. Together these findings support a shift from a uniform, calendar-based follow-up schedule to a risk-adjusted one driven by each patient's own trajectory.
