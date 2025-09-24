# Natomas Unified School District
## After School Extended Learning Core Program Providers — Cycle B (2026–27 & 2027–28)
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
- [x] Cover Page  
- [x] Proposal Checklist  
- [x] References  
- [x] Budget Sheet  
- [x] Proposal Narrative  
- [x] Application Questionnaire  
- [x] Assurances  
- [x] Non-Collusion Affidavit  
- [x] Non-Disclosure Agreement  
- [x] Workers’ Comp Certification  
- [x] Fingerprinting Certification

---

## Appendix C: References
| Organization | Contact | Phone | Email | Dates | Description |
|--------------|---------|-------|-------|-------|-------------|
{% for r in references -%}
| {{ r.organization or "TBD" }} | {{ r.contact_name or "TBD" }} | {{ r.phone or "TBD" }} | {{ r.email or "TBD" }} | {{ r.dates_of_service or "TBD" }} | {{ r.description or "TBD" }} |
{% endfor %}

---

## Appendix D: Budget Description Sheet

**Program Model:** After School Extended Learning Core Program (ELO-P)
**Target Audience:** {{ program_details.target_audience or "TK–6 students" }}
**Program Duration:** {{ program_details.program_duration or "All school days when school is in session" }}
**Daily Schedule:** {{ program_details.daily_hours or "Minimum 3 hours/day after school dismissal until ~6:00 PM" }}
**Staffing Ratios:** TK/K {{ staffing_ratios.tk_k_ratio or "1:10" }} (max {{ staffing_ratios.tk_k_max_per_site or 40 }} per site), Grades 1–6 {{ staffing_ratios.grades_1_6_ratio or "1:20" }}

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
| **Total Program Cost** | {{ (budget.categories.staffing + budget.categories.instructional_materials + budget.categories.supplies + budget.categories.supervision + budget.categories.professional_development + budget.categories.transportation + budget.categories.admin_overhead + budget.categories.subcontracted_services) | default("TBD") }} |

---

## Narrative
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

### Evaluation & Outcomes
{{ narrative.evaluation_outcomes or "TBD" }}

### Sustainability & Innovation
{{ narrative.sustainability_innovation or "TBD" }}

---

## Application Questionnaire
{% for key, answer in application_questions.items() %}
- {{ key }}: {{ answer or "TBD" }}
{% endfor %}

---

## Appendix E: Assurances
Initials: {{ legal.assurances_initials or "____" }}

---

## Appendix F: Non-Collusion Affidavit
[District affidavit language here]

---

## Appendix G: Non-Disclosure Agreement
Disclosee: {{ legal.nda_disclosee_name or "TBD" }}
[District NDA terms here]

---

## Appendix H: Workers’ Compensation Certification
Company: {{ legal.workers_comp_company_name or "TBD" }}  
Representative: {{ legal.workers_comp_rep_name or "TBD" }}

---

## Fingerprinting / Background Certification
[District form to be inserted]

