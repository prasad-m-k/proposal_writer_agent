# Natomas Unified School District
## Summer School Extended Learning Core Program Providers — Cycle B (2026 & 2027)
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
- [x] References (Appendix C, ≥3 from last 5 years)
- [x] Budget Sheet (Appendix D + attachment)
- [x] Proposal Narrative (Attachment)
  - Need for Program
  - Program Design
  - High-Quality Programming Elements
  - Organizational Focus
  - Professional Development
  - Success & Sustainability
  - Innovation
- [x] Application Questions (Attachment, 20 total)
- [x] Assurances to Meet Requirements (Appendix E)
- [x] Non-Collusion Affidavit (Appendix F)
- [x] Non-Disclosure Agreement (Appendix G)
- [x] Workers' Compensation Certification (Appendix H)

---

## Appendix C: References

| Organization | Contact Name | Phone | Email | Dates of Service | Program/Service Description |
|--------------|--------------|-------|-------|------------------|----------------------------|
{% for r in references %}
| {{ r.organization or "TBD" }} | {{ r.contact_name or "TBD" }} | {{ r.phone or "TBD" }} | {{ r.email or "TBD" }} | {{ r.dates_of_service or "TBD" }} | {{ r.description or "TBD" }} |
{% endfor %}

---

## Appendix D: Budget Description Sheet

**Program Model:** Summer School Extended Learning Core Program
**Budget Option:** {{ budget.option or "TBD" }}
**Baseline Capacity:** {{ budget.students_per_site or 200 }} students per site per day
**Maximum Cost per Student:** ${{ budget.cap_per_student or "TBD" }}/student
**TK/K Maximum per Site:** {{ budget.tk_k_max or 40 }} students

| Category | Cost ($) |
|----------|----------|
| Staffing | {{ budget.categories.staffing or "TBD" }} |
| Instructional Materials | {{ budget.categories.instructional_materials or "TBD" }} |
| Supplies | {{ budget.categories.supplies or "TBD" }} |
| Supervision | {{ budget.categories.supervision or "TBD" }} |
| Professional Development | {{ budget.categories.professional_development or "TBD" }} |
| Transportation | {{ budget.categories.transportation or "TBD" }} |
| Administrative/Overhead | {{ budget.categories.admin_overhead or "TBD" }} |
| Subcontracted Services | {{ budget.categories.subcontracted_services or "TBD" }} |
| **Total (per site/day)** | {{ (budget.categories.staffing + budget.categories.instructional_materials + budget.categories.supplies + budget.categories.supervision + budget.categories.professional_development + budget.categories.transportation + budget.categories.admin_overhead + budget.categories.subcontracted_services) | default("TBD") }} |

{% if budget.option == "Option 2" %}
### Intervention Services Plan
{{ budget.intervention_plan or "TBD" }}
{% endif %}

---

## Attachment: Proposal Narrative

### Need for Program
{{ narrative.need_for_program or "TBD" }}

### Program Design
{{ narrative.program_design or "TBD" }}

### High-Quality Programming Elements
{{ narrative.hq_elements or "TBD" }}

### Organizational Focus
{{ narrative.org_focus or "TBD" }}

### Professional Development
{{ narrative.professional_development or "TBD" }}

### Success & Sustainability
{{ narrative.success_sustainability or "TBD" }}

### Innovation
{{ narrative.innovation or "TBD" }}

---

## Attachment: Application Questions

1. **Current summer program provider information (schools, services provided).**
{{ application_questions.q1_current_provider or "TBD" }}

2. **Prior experience with NUSD or similar summer programs.**
{{ application_questions.q2_prior_experience or "TBD" }}

3. **Other school districts currently served.**
{{ application_questions.q3_other_districts or "TBD" }}

4. **Any terminated contracts or pending investigations?**
{{ application_questions.q4_terminated_contracts or "TBD" }}

5. **Capacity: number of sites and rationale.**
{{ application_questions.q5_capacity_sites or "TBD" }}

6. **Capacity: maximum students per site.**
{{ application_questions.q6_capacity_students or "TBD" }}

7. **Litigation status with any school district.**
{{ application_questions.q7_litigation_status or "TBD" }}

8. **Community engagement experience (Natomas or similar).**
{{ application_questions.q8_community_engagement or "TBD" }}

9. **Experience working with school communities.**
{{ application_questions.q9_school_partnerships or "TBD" }}

10. **Safe and supportive environment – how ensured.**
{{ application_questions.q10_safe_environment or "TBD" }}

11. **Active and engaged learning – academic support approach.**
{{ application_questions.q11_active_learning or "TBD" }}

12. **Skill-building opportunities and enrichment activities.**
{{ application_questions.q12_skill_building or "TBD" }}

13. **Youth voice and leadership development.**
{{ application_questions.q13_youth_voice or "TBD" }}

14. **Diversity, equity, access, and inclusion (including students with disabilities).**
{{ application_questions.q14_equity_access or "TBD" }}

15. **Quality staff – qualifications and support.**
{{ application_questions.q15_quality_staff or "TBD" }}

16. **Clear vision, mission, purpose aligned with NUSD's goals.**
{{ application_questions.q16_vision_alignment or "TBD" }}

17. **Collaborative partnerships and community engagement.**
{{ application_questions.q17_collaborations or "TBD" }}

18. **Continuous Quality Improvement (CQI) plan.**
{{ application_questions.q18_cqi_plan or "TBD" }}

19. **Program management and oversight plan.**
{{ application_questions.q19_program_management or "TBD" }}

20. **Staff supervision, professional development, and handling absences/concerns.**
{{ application_questions.q20_staffing_absences_pd or "TBD" }}

---

## Appendix E: Assurances to Meet Requirements

I, {{ submission.rep_name or "___________________" }}, {{ submission.title or "___________________" }} of {{ submission.company_name or "___________________" }}, hereby provide assurance that our organization will meet all requirements outlined in this RFP, including but not limited to:

- Full-day, 9-hour summer school programs for TK–6 students over ≥30 non-school days
- Academic support, enrichment, youth development, SEL, and family engagement components
- Required staffing ratios: TK/K 1:10 (max 40 per site), Grades 1–6 1:20
- On-site coordinator at each site
- All staff DOJ/TB cleared and culturally responsive
- Safety procedures, attendance tracking, and progress reporting
- Compliance with all district policies and procedures

**Initial Here:** {{ legal.assurances_initials or "____" }}

---

## Appendix F: Non-Collusion Affidavit

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

**Signature:** ____________________________   **Date:** _____________

---

## Appendix G: Non-Disclosure Agreement

This Agreement ("Agreement") is made between the Natomas Unified School District ("District") and {{ legal.nda_disclosee_name or "____________________________" }} ("Disclosee"), and entered into concurrently with the Independent Contractor Agreement.

### 1. Confidential Information
"Confidential Information" means nonpublic information that the District designates as confidential or which, under the circumstances of disclosure, ought to be treated as confidential. Confidential Information includes, without limitation, information relating to students (including FERPA-protected records), personnel, operations, finances, contact lists, and proprietary data. Confidential Information does not include information that becomes public without breach, or that is lawfully obtained from another source without restriction.

### 2. Obligations of Disclosee
Disclosee shall: (a) keep strictly confidential all Confidential Information; (b) use such information solely for the purpose of performing services for the District; (c) disclose such information only to personnel and subcontractors with a need to know who are bound by written obligations no less stringent than this Agreement; and (d) comply with all applicable laws and District policies, including FERPA and California Education Code §49073.1.

### 3. Security; Return/Destruction
Disclosee shall implement reasonable and appropriate safeguards to protect Confidential Information. Upon District request, Disclosee shall promptly return or destroy all Confidential Information and certify such destruction in writing. Disclosee shall also assist the District in notifications and remedial actions in the event of any unauthorized disclosure.

### 4. Remedies
Disclosee acknowledges that a breach of this Agreement may cause irreparable harm to the District. The District shall be entitled to seek injunctive relief, in addition to any other remedies available at law or equity.

### 5. Governing Law; Venue
This Agreement shall be governed by the laws of the State of California. Venue shall lie exclusively in the state and federal courts sitting in Sacramento County, California.

### 6. Miscellaneous
This Agreement constitutes the entire agreement regarding Confidential Information, may be modified only in writing signed by both parties, and shall bind and inure to the benefit of the parties and their successors and permitted assigns. If any provision is held invalid, the remainder shall remain in force. All obligations survive termination of the parties' relationship.

**Authorized Signature (Disclosee):** ____________________________   **Date:** _____________

---

## Appendix H: Workers' Compensation Certification

Labor Code Section 3700 in relevant part provides:

Every employer except the State shall secure the payment of compensation in one or more of the following ways:
- By being insured against liability to pay compensation by one or more insurers duly authorized to write compensation insurance in this State.
- By securing from the Director of Industrial Relations a certificate of consent to self-insure, which may be given upon furnishing satisfactory proof to the Director of Industrial Relations of ability to self-insure and to pay any compensation that may become due to its employees.

I am aware of the provisions of Section 3700 of the Labor Code which require every employer to be insured against liability for workers' compensation or to undertake self-insurance in accordance with the provisions of that code, and I will comply with such provisions before commencing the performance of the Services of this Agreement.

**Company Name:** {{ legal.workers_comp_company or "TBD" }}
**Authorized Representative Name:** {{ legal.workers_comp_rep or "TBD" }}

**Authorized Signature:** ______________________________    **Date:** __________________

---

## Program Schedule & Timeline

**Key Dates:**
- **RFP Published:** {{ schedule.publish or "August 25, 2025" }}
- **Questions Due:** {{ schedule.questions_due or "September 12, 2025 (4:00 PM PT)" }}
- **Q&A Posted:** {{ schedule.qa_posted or "September 19, 2025 (4:00 PM PT)" }}
- **Proposal Due:** {{ schedule.proposal_due or "September 26, 2025 (4:00 PM PT)" }}
- **Review Period:** {{ schedule.review or "September 29 – October 17, 2025" }}
- **Selection Week:** {{ schedule.selection or "Week of October 20, 2025" }}
- **Board Approval 1:** {{ schedule.board_approval_1 or "November 19, 2025" }}
- **Board Approval 2:** {{ schedule.board_approval_2 or "January 14, 2026" }}

**Program Delivery:** Summer 2026 & 2027
**Program Duration:** ≥30 non-school days per summer
**Daily Schedule:** 9 hours/day
**Target Audience:** TK–6 students