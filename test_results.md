## What's my copay percentage?

**Structure:** structured

**Result:**

Structured database result:
(10,)

---

Structured database result:
(20,)

---

Structured database result:
(30,)

**Score:** good

---

## What is the annual deductible for Silver HMO?

**Structure:** structured

**Result:**

Structured database result:
(1500,)

**Score:** good

---

## What is the monthly premium for Gold PPO?

**Structure:** structured

**Result:**

Structured database result:
(500,)

**Score:** good

---

## What is the claim status for C1003?

**Structure:** structured

**Result:**

Structured database result:
('Denied',)

**Score:** good

---

## What is the claim amount for C1002?

**Structure:** structured

**Result:**

Structured database result:
(1200,)

**Score:** good

---

## Is maternity care covered on the Bronze HMO plan?

**Structure:** unstructured

**Result:**

Retrieved document:
Plan: Bronze HMO. Premium: $150/month. Deductible: $1000. Coinsurance: 30%. Network: Bronze.

---

Retrieved document:
Bronze HMO $150 $1,000

HMO / Bronze

Selected plan schema linkage
member_id: M1001 plan_id: P101 plan_name: Gold PPO
monthly_premium: $500 | annual_deductible: $2,000 | copay_pct: 10 | network_tier: Gold

coverage_type: PPO

SECTION 4 - DEPENDENT INFORMATION

Dependent name Relationship Date of birth

Student / disabled

Jordan Morgan Child 03/22/2017

No

Avery Morgan Child 11/09/2020

No

SECTION 5 - ACKNOWLEDGEMENTS

[| | understand this is synthetic training data and not actual coverage.

---

Retrieved document:
Plan: Silver HMO. Premium: $300/month. Deductible: $1500. Coinsurance: 20%. Network: Silver.

---

Retrieved document:
Silver HMO (P102)
Linked claims: 2. Status counts - Denied: 1, Approved: 1. Procedures - X-ray, Surgery.
Bronze HMO (P103)
Linked claims: 1. Status counts - Pending: 1. Procedures - X-ray.
8. Recommended production schema extensions
9. Data dictionary
plans.plan_id: Unique plan identifier and join key.
plans.plan_name: Human-readable plan name.
plans.monthly_premium: Monthly premium amount.
plans.annual_deductible: Annual deductible amount.

---

Retrieved document:
- Do not infer coverage from procedure name or status alone.
6. Supplied synthetic claim register
The plan cost-share percentage is shown only as reference data. The file does not provide enough information to calculate member responsibility, because deductible accumulation, allowed amount, service rules, and payment details are absent.
7. Plan-specific claim observations
Gold PPO (P101)
Linked claims: 2. Status counts - Pending: 1, Approved: 1. Procedures - X-ray, Surgery.
Silver HMO (P102)

**Score:** partial

---

## Do I need prior authorization for surgery?

**Structure:** unstructured

**Result:**

Retrieved document:
C1002 M1001 Surgery $1,200 Approved 2023-03-15
These records show only the supplied procedure, amount, status, and filing date. No denial reason, allowed amount, payment amount, or
deductible accumulation is present in claims.csv.
Information not defined by the supplied schema
- Out-of-pocket maximums and family accumulators
- Service-specific copays, coinsurance, exclusions, and limits
- Provider network rules, referral requirements, and prior authorization rules

---

Retrieved document:
C1004 M1002 Surgery $900 Approved 2023-03-20
These records show only the supplied procedure, amount, status, and filing date. No denial reason, allowed amount, payment amount, or
deductible accumulation is present in claims.csv.
Information not defined by the supplied schema
- Out-of-pocket maximums and family accumulators
- Service-specific copays, coinsurance, exclusions, and limits
- Provider network rules, referral requirements, and prior authorization rules

---

Retrieved document:
More info
Getting regular medical care
Most health plans give you the best deal on services when you see a doctor who has a contract with your health plan. While you may be able to see doctors who donât contract with your plan, visiting an âin-networkâ provider usually means youâll have lower out-of-pocket costs.
Finding a doctor in your plan

---

Retrieved document:
Call the Marketplace Call Center at 1-800-318-2596 (TTY: 1-855-889-4325). A trained representative can help you find your insurerâs number
Is there an appeals process if I go to my regular doctor and find out later that my new plan doesnât cover them?
Yes. If your health insurance company doesnât pay for a visit to the doctor, you have the right to appeal the decision and have it reviewed by an independent third party.
Learn about the appeals process
.
Email this page
Email

---

Retrieved document:
Finding a doctor in your plan
To find out if your doctors and other health care providers are covered by your new Marketplace plan, or to find a covered provider if you donât have one yet:
Visit your health planâs website and check their provider directory, which is a list of the doctors, hospitals, and other health care providers that your plan contracts with to provide care.

**Score:** good

---

## Can I use an out-of-network doctor?

**Structure:** unstructured

**Result:**

Retrieved document:
More info
Getting regular medical care
Most health plans give you the best deal on services when you see a doctor who has a contract with your health plan. While you may be able to see doctors who donât contract with your plan, visiting an âin-networkâ provider usually means youâll have lower out-of-pocket costs.
Finding a doctor in your plan

---

Retrieved document:
Finding a doctor in your plan
To find out if your doctors and other health care providers are covered by your new Marketplace plan, or to find a covered provider if you donât have one yet:
Visit your health planâs website and check their provider directory, which is a list of the doctors, hospitals, and other health care providers that your plan contracts with to provide care.

---

Retrieved document:
See your health planâs provider directory. You can get this by contacting your plan, visiting the planâs website, or using a link that youâll find on the plan description in your Marketplace account.
Call your insurer to ask about specific providers. This number is on your insurance card and the insurerâs website.
Call your doctorâs office. They can tell you if they accept your health plan.

---

Retrieved document:
Call the Marketplace Call Center at 1-800-318-2596 (TTY: 1-855-889-4325). A trained representative can help you find your insurerâs number
Is there an appeals process if I go to my regular doctor and find out later that my new plan doesnât cover them?
Yes. If your health insurance company doesnât pay for a visit to the doctor, you have the right to appeal the decision and have it reviewed by an independent third party.
Learn about the appeals process
.
Email this page
Email

---

Retrieved document:
Using your health insurance coverage
Email this page
Email
Print this page
Print
More info
Improving your health
Getting prescription medications
Getting regular medical care
Getting emergency care
Finding resources on staying healthy
Appealing an insurance company decision
More info
Getting regular medical care

**Score:** good

---

## How do I appeal a denied claim?

**Structure:** unstructured

**Result:**

Retrieved document:
claims.status: Approved, Denied, or Pending.
claims.date_filed: Date the claim was filed.

---

Retrieved document:
Call the Marketplace Call Center at 1-800-318-2596 (TTY: 1-855-889-4325). A trained representative can help you find your insurerâs number
Is there an appeals process if I go to my regular doctor and find out later that my new plan doesnât cover them?
Yes. If your health insurance company doesnât pay for a visit to the doctor, you have the right to appeal the decision and have it reviewed by an independent third party.
Learn about the appeals process
.
Email this page
Email

---

Retrieved document:
5. Review duplicate risk: Check whether the same member, procedure, amount, and filing date already exist under another claim_id.
6. Apply configured rules: Use only implemented benefit, authorization, network, and pricing rules. These rules are not supplied by the current CSV schema and must not be invented.
7. Assign outcome: Use Approved, Denied, or Pending as represented in the supplied data. Store a reason field in a production schema even though claims.csv does not contain one.

---

Retrieved document:
Silver HMO (P102)
Linked claims: 2. Status counts - Denied: 1, Approved: 1. Procedures - X-ray, Surgery.
Bronze HMO (P103)
Linked claims: 1. Status counts - Pending: 1. Procedures - X-ray.
8. Recommended production schema extensions
9. Data dictionary
plans.plan_id: Unique plan identifier and join key.
plans.plan_name: Human-readable plan name.
plans.monthly_premium: Monthly premium amount.
plans.annual_deductible: Annual deductible amount.

---

Retrieved document:
Annual deductible $1,500 Exact value from plans.csv; no family or network split supplied.
Member cost-share rate 20% Based on copay_pct; no service-specific schedule supplied.
Coverage type HMO Exact categorical value from plans.csv.
Network tier Silver Exact categorical value from plans.csv.
Synthetic claims linked to this plan
Claim ID Member ID Procedure Claim amount Status Date filed
C1003 M1002 X-ray $150 Denied 2023-04-05
C1004 M1002 Surgery $900 Approved 2023-03-20

**Score:** good

---

## What is the claim status for C1003, and how do I appeal if it was denied?

**Structure:** both

**Result:**

Structured database result:
('Denied',)

---

Retrieved document:
C1005 M1003 X-ray $50 Pending 2023-04-10
These records show only the supplied procedure, amount, status, and filing date. No denial reason, allowed amount, payment amount, or
deductible accumulation is present in claims.csv.
Information not defined by the supplied schema
- Out-of-pocket maximums and family accumulators
- Service-specific copays, coinsurance, exclusions, and limits
- Provider network rules, referral requirements, and prior authorization rules

---

Retrieved document:
C1002 M1001 Surgery $1,200 Approved 2023-03-15
These records show only the supplied procedure, amount, status, and filing date. No denial reason, allowed amount, payment amount, or
deductible accumulation is present in claims.csv.
Information not defined by the supplied schema
- Out-of-pocket maximums and family accumulators
- Service-specific copays, coinsurance, exclusions, and limits
- Provider network rules, referral requirements, and prior authorization rules

---

Retrieved document:
C1004 M1002 Surgery $900 Approved 2023-03-20
These records show only the supplied procedure, amount, status, and filing date. No denial reason, allowed amount, payment amount, or
deductible accumulation is present in claims.csv.
Information not defined by the supplied schema
- Out-of-pocket maximums and family accumulators
- Service-specific copays, coinsurance, exclusions, and limits
- Provider network rules, referral requirements, and prior authorization rules

---

Retrieved document:
claims.status: Approved, Denied, or Pending.
claims.date_filed: Date the claim was filed.

---

Retrieved document:
Silver HMO (P102)
Linked claims: 2. Status counts - Denied: 1, Approved: 1. Procedures - X-ray, Surgery.
Bronze HMO (P103)
Linked claims: 1. Status counts - Pending: 1. Procedures - X-ray.
8. Recommended production schema extensions
9. Data dictionary
plans.plan_id: Unique plan identifier and join key.
plans.plan_name: Human-readable plan name.
plans.monthly_premium: Monthly premium amount.
plans.annual_deductible: Annual deductible amount.

**Score:** good

---

# Overall Result

Much stronger than expected. 90% of results were good, only one was partial because it pulled a "Silver HMO" chunk for a "Bronze HMO" plan question. Overall the results are surprisingly good and relevant to the questions. Happy with the results!
