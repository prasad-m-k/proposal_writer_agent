# Natomas Unified School District
## Request for Qualifications (RFQ) – Cycle B: Enrichment Program Provider
**Proposal Submission Deadline:** September 26, 2025, at 4:00 PM (Pacific)  
**Submission Method:** Electronically through Secure Bids

---

## Appendix A: Cover Page

**Company Name:** {{ submission.company_name or "TBD" }}  
**Authorized Representative Name:** {{ submission.rep_name or "TBD" }}  
**Title:** {{ submission.title or "TBD" }}  
**Email:** {{ submission.email or "TBD" }}  
**Phone:** {{ submission.phone or "TBD" }}  
**Address:** {{ submission.address or "TBD" }}

**Authorized Signature:** {{ submission.signature_name or "TBD" }}  
**Date:** {{ submission.signature_date or "TBD" }}

---

## Appendix B: Proposal Checklist

- [x] Signed Cover Page (Appendix A)  
- [x] Proposal Checklist (Appendix B)  
- [x] References (Appendix C)  
- [x] Budget Description (Attachment)  
- [x] Proposal Narrative (Attachment)  
  - Organizational Overview  
  - Program Design  
  - High Quality Programming Elements  
  - Staffing / Training  
  - Evaluation & Outcomes  
  - Sustainability & Innovation  
- [x] Application Questions (Attachment)  
- [x] Non-Collusion Affidavit (Appendix D)  
- [x] Non-Disclosure Agreement (Appendix E)  
- [x] Workers’ Compensation Certification (Appendix F)

---

## Appendix C: References

| Organization | Contact Name | Phone | Email | Dates of Service | Program/Service Description |
|--------------|--------------|-------|-------|------------------|-----------------------------|
{% for r in references %}
| {{ r.organization or "TBD" }} | {{ r.contact_name or "TBD" }} | {{ r.phone or "TBD" }} | {{ r.email or "TBD" }} | {{ r.dates_of_service or "TBD" }} | {{ r.description or "TBD" }} |
{% endfor %}

---

## Attachment: Budget Description Sheet

**Budget Assumptions:** Minimum {{ budget.min_students_per_site }} students per site, per day. Max ${{ budget.per_student_per_day_usd }} per student/day.

| Category                | Cost ($) |
|------------------------|---------:|
| Staffing                 | {{ budget.categories.staffing }} |
| Instructional Materials  | {{ budget.categories.instructional_materials }} |
| Program Supplies         | {{ budget.categories.program_supplies }} |
| Supervision              | {{ budget.categories.supervision }} |
| Professional Development | {{ budget.categories.professional_development }} |
| Transportation           | {{ budget.categories.transportation }} |
| Administrative Costs     | {{ budget.categories.admin_costs }} |
| **Total (per site/day)** | {{ (budget.categories.staffing
                               + budget.categories.instructional_materials
                               + budget.categories.program_supplies
                               + budget.categories.supervision
                               + budget.categories.professional_development
                               + budget.categories.transportation
                               + budget.categories.admin_costs) | default(0) }} |

---

## Attachment: Proposal Narrative

### Organizational Overview
{{ narrative.org_overview or "TBD" }}

### Program Design
{{ narrative.program_design or "TBD" }}

### High-Quality Programming Elements
{{ narrative.hq_elements or "TBD" }}

### Staffing and Training
{{ narrative.staffing_training or "TBD" }}

### Evaluation and Outcomes
{{ narrative.evaluation_outcomes or "TBD" }}

### Sustainability and Innovation
{{ narrative.sustainability_innovation or "TBD" }}

---

## Attachment: Application Questions

1. Current enrichment provider information (schools, services provided).  
{{ application_questions.q1_current_provider or "TBD" }}

2. Prior experience with NUSD LEAP Academy.  
{{ application_questions.q2_prior_nusd_provider or "TBD" }}

3. Other school districts currently served.  
{{ application_questions.q3_other_districts or "TBD" }}

4. Any terminated contracts or pending investigations?  
{{ application_questions.q4_terminated_or_investigations or "TBD" }}

5. Capacity: number of sites and rationale.  
{{ application_questions.q5_capacity_sites_and_rationale or "TBD" }}

6. Capacity: ability to serve during summer/intersessions.  
{{ application_questions.q6_capacity_summer_intersession or "TBD" }}

7. Litigation status with any school district.  
{{ application_questions.q7_litigation_status or "TBD" }}

8. Community engagement experience (Natomas or similar).  
{{ application_questions.q8_natomas_community_experience or "TBD" }}

9. Experience working with school communities.  
{{ application_questions.q9_school_partnership_experience or "TBD" }}

10. Safe and supportive environment – how ensured.  
{{ application_questions.q10_safe_supportive_environment or "TBD" }}

11. Active and engaged learning – literacy, math, integration.  
{{ application_questions.q11_active_engaged_learning or "TBD" }}

12. Skill-building opportunities.  
{{ application_questions.q12_skill_building or "TBD" }}

13. Youth voice and leadership.  
{{ application_questions.q13_youth_voice_leadership or "TBD" }}

14. Diversity, access, and equity (including students with disabilities).  
{{ application_questions.q14_diversity_access_equity_disabilities or "TBD" }}

15. Quality staff – qualifications and support.  
{{ application_questions.q15_quality_staff or "TBD" }}

16. Clear vision, mission, purpose aligned with NUSD’s Theory of Action.  
{{ application_questions.q16_vision_mission_alignment_to_theory_of_action or "TBD" }}

17. Collaborative partnerships.  
{{ application_questions.q17_collaborative_partnerships or "TBD" }}

18. Program management plan.  
{{ application_questions.q18_program_management_plan or "TBD" }}

19. Staff supervision, support, professional development, and handling absences/issues.  
{{ application_questions.q19_staff_supervision_pd_absences_concerns or "TBD" }}

---

## Appendix D: Non-Collusion Affidavit

I, _________________________________________, _______________________________  
(Name)                                   (Title)

Of ______________________________________________________ hereby certify:  
(Company Name)

That all statements of fact in this proposal are true, and that such proposal is genuine and not collusive or a sham;  
That such proposal was not made in the interest of, or on behalf of, any undisclosed person, partnership, company, association, organization, or corporation;  
That said applicant has not, directly or indirectly, by agreement, communication, or conference with anyone, attempted to induce action prejudicial to the interest of the Natomas Unified School District, or of any other applicant or anyone else interested in the proposed contract;  
That prior to the public opening and reading of proposals, said applicant did not, directly or indirectly, induce or solicit, or collude, conspire, connive, or agree with anyone else that said applicant or anyone else would submit a false or sham proposal, or that anyone should refrain from applying or withdraw his proposal;  
That said applicant has not, in any manner, directly or indirectly, sought by agreement, communication, or conference with anyone to raise or fix the proposal price of said applicant or of anyone else.

Furthermore, the above-named certifies:  
That no current Board member or employee of the Natomas Unified School District, and no one who has been a Board member or who has been employed by the Natomas Unified School District within the past two years has participated in the application, selling, or promoting this contract;  
That no such current or former Board member or employee has an ownership interest in this contract, nor shall any such current or former Board member or employee derive compensation, directly or indirectly, from this contract;  
That said applicant does not know of any facts which constitute a violation of Conflict of Interest laws.

Government Code of the State of California, Section 87100 et seq. states in part: No public official at any level of state or local government shall make, participate in making, or in any way attempt to use his official position to influence a governmental decision in which he knows, or has reason to know, he has a financial interest. The applicant understands that any violation of this Statement of Compliance shall make any agreement or contract voidable by the District.

**Signature:** ____________________________   **Date:** _____________

---

## Appendix E: Non-Disclosure Agreement

This Agreement (“Agreement”) is made between the Natomas Unified School District (“District”) and {{ legal.nda_disclosee_name or "____________________________" }} (“Disclosee”), and entered into concurrently with the Independent Contractor Agreement.

### 1. Confidential Information
“Confidential Information” means nonpublic information that the District designates as confidential or which, under the circumstances of disclosure, ought to be treated as confidential. Confidential Information includes, without limitation, information relating to students (including FERPA-protected records), personnel, operations, finances, contact lists, and proprietary data. Confidential Information does not include information that becomes public without breach, or that is lawfully obtained from another source without restriction.

### 2. Obligations of Disclosee
Disclosee shall: (a) keep strictly confidential all Confidential Information; (b) use such information solely for the purpose of performing services for the District; (c) disclose such information only to personnel and subcontractors with a need to know who are bound by written obligations no less stringent than this Agreement; and (d) comply with all applicable laws and District policies, including FERPA and California Education Code §49073.1.

### 3. Security; Return/Destruction
Disclosee shall implement reasonable and appropriate safeguards to protect Confidential Information. Upon District request, Disclosee shall promptly return or destroy all Confidential Information and certify such destruction in writing. Disclosee shall also assist the District in notifications and remedial actions in the event of any unauthorized disclosure.

### 4. Remedies
Disclosee acknowledges that a breach of this Agreement may cause irreparable harm to the District. The District shall be entitled to seek injunctive relief, in addition to any other remedies available at law or equity.

### 5. Governing Law; Venue
This Agreement shall be governed by the laws of the State of California. Venue shall lie exclusively in the state and federal courts sitting in Sacramento County, California.

### 6. Miscellaneous
This Agreement constitutes the entire agreement regarding Confidential Information, may be modified only in writing signed by both parties, and shall bind and inure to the benefit of the parties and their successors and permitted assigns. If any provision is held invalid, the remainder shall remain in force. All obligations survive termination of the parties’ relationship.

**Authorized Signature (Disclosee):** ____________________________   **Date:** _____________

---

## Appendix F: Workers’ Compensation Certification

Labor Code Section 3700 in relevant part provides:

Every employer except the State shall secure the payment of compensation in one or more of the following ways:
- By being insured against liability to pay compensation by one or more insurers duly authorized to write compensation insurance in this State.
- By securing from the Director of Industrial Relations a certificate of consent to self-insure, which may be given upon furnishing satisfactory proof to the Director of Industrial Relations of ability to self-insure and to pay any compensation that may become due to its employees.

I am aware of the provisions of Section 3700 of the Labor Code which require every employer to be insured against liability for workers’ compensation or to undertake self-insurance in accordance with the provisions of that code, and I will comply with such provisions before commencing the performance of the Services of this Agreement.

**Company Name:** {{ legal.workers_comp_company_name or "TBD" }}  
**Authorized Representative Name:** {{ legal.workers_comp_rep_name or "TBD" }}

**Authorized Signature:** ______________________________    **Date:** __________________


