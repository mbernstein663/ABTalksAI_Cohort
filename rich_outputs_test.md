# Testing RAG

Today we implemented fancy content generation features. After including streaming, our chatbot now renders tables that include policy/claim cards for structured outputs. It also cites chunks that it references by ID.
This is our test to make sure it works.

## Questions:

- Tell me information about the Gold PPO plan.
- What is the claim status for C1003?
- Can I use an out-of-network doctor?
- How do I appeal a denied claim?

### Question 1

The Gold PPO plan (Plan ID: P101) has a monthly premium of 500**, an **annual deductible of 2,000, and 10% copay coverage. It is a PPO plan with a Gold network tier, offering broader provider networks and higher coverage compared to lower-tier plans. For detailed cost specifics, consult your benefits guide or support.

**Card Render**

Plan Id

P101

Plan Name

Gold PPO

Monthly Premium

500

Annual Deductible

2000

Copay Pct

10

Coverage Type

PPO

Network Tier

Gold

### Question 2

The claim status for C1003 is Denied.

**Card Render**

Claim Id

C1003

Status

Denied

### Question 3

Yes, you can use an out-of-network doctor, but visiting an "in-network" provider typically results in lower out-of-pocket costs. To confirm if a specific doctor accepts your plan, check your health plan’s provider directory, contact your insurer, or ask the doctor’s office directly. For further assistance, contact your plan’s support team.

**Chunk Render**

Policy sources

medical_care_FAQ-chunk-2
medical_care_FAQ-chunk-3
medical_care_FAQ-chunk-4
medical_care_FAQ-chunk-5
medical_care_FAQ-chunk-1

### Question 4

To appeal a denied claim, contact the Marketplace Call Center at 1-800-318-2596 (TTY: 1-855-889-4325). A representative can guide you through the appeals process, including requesting a review by an independent third party. For specific claim details (e.g., claim ID C1003), ensure you have the denial notice and supporting documentation ready. If further assistance is needed, contact support.

**Chunk Render**

Policy sources

claims_process-chunk-9
medical_care_FAQ-chunk-5
claims_process-chunk-4
claims_process-chunk-7
benefits-chunk-13

## Observations

To be completely honest this worked way better than I thought it was going to and seems to be generating better responses when I switched `retrieve()` to the function from `tool_calling_chatbot.py`. This worked first try and is generating very strong results. Cool stuff!