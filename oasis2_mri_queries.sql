-- spliting data as information that changes for subjects in every visit and that stays stable over the course of the study
-- subjects_table holds data that will stay stable
create table subject_table
(subjectID nvarchar(50) primary key,
subj_group nvarchar(50),
m_f nvarchar(50),
hand nvarchar(50),
educ tinyint,
ses float
)

--visits table holds data that changes with every visit from the subject
create table visits
(subjectID nvarchar(50),
age tinyint,
mmse float,
cdr float,
nwbv float,
asf float,
mriID nvarchar(50) primary key,
etiv smallint,
mr_delay smallint,
visit tinyint,
foreign key (subjectID) references subject_table(subjectID)
)

-- inserting into subject_table as Staging_OASIS has 371 visit-rows without it the same subject's info 
-- would try to insert multiple times and violate the primary key. So we use distinct to collapse it into 150 unique subjects

insert into subject_table (subjectID, subj_group, m_f, hand, educ, ses)
select distinct Subject_ID, [group], M_F, Hand, EDUC, SES from Staging_OASIS

insert into visits (subjectID, age, mmse, cdr, nwbv, asf, mriID, etiv, mr_delay, visit)
select Subject_ID, Age, MMSE, CDR, nWBV, ASF, MRI_ID, eTIV, MR_Delay, Visit from Staging_OASIS

-- Average nWBV per subject group
select avg(visits.nwbv),
subject_table.subj_group
from visits
join subject_table  on visits.subjectID = subject_table.subjectID
group by subject_table.subj_group 

-- Average MMSE per group, visit and respective count
select avg(mmse),
visits.visit
from visits
group by visits.visit

select avg(visits.mmse),
subject_table.subj_group,
visits.visit,
count(*)
from visits
join subject_table  on visits.subjectID = subject_table.subjectID
group by subject_table.subj_group, visits.visit 

-- Watch-list count of subjects where the two assessments disagree (CDR=0 but MMSE>28)
select count (distinct visits.subjectID),
subject_table.subj_group
from visits 
join subject_table on visits.subjectID = subject_table.subjectID
where mmse < 28 and cdr = 0
group by subject_table.subj_group

-- Comparing nWBV of demented subjects on their first and last visit
select demented_visit_range.subjectID, demented_visit_range.first_visit, v1.nwbv, demented_visit_range.last_visit, v2.nwbv
from (
select visits.subjectID, min(visit) as first_visit, max(visit) as last_visit
from visits
join subject_table  on visits.subjectID = subject_table.subjectID
where subj_group = 'Demented'  
group by visits.subjectID
) as demented_visit_range 

join visits as v1 on demented_visit_range.subjectID = 
v1.subjectID and demented_visit_range.first_visit = v1.visit
join visits as v2 on demented_visit_range.subjectID = 
v2.subjectID and demented_visit_range.last_visit = v2.visit 

-- ASF vs eTIV 
select etiv, asf
from visits
order by etiv desc
