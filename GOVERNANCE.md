# Governance Checklist

## What do we need to look out for?

**Internal Database Schema:** 

- member_id

**External Schema:**

- Member names
- Member location/address
- Other PII such as credit cards, SSNs, insurance, etc

*Make sure to include warning not to expose sensitive information through chat system*

## Bias Risks

- The chatbot might speak differently to someone on a lower plan tier (economic)
- The bot might speak to the user differently knowing that they are a certain experience level (age bias)
- The user might ask to avoid guardrials and answer questions that require immediate action (urgency/prompt bias) 

## Accountability

Ultimately, who is **responsible for reviewing chat outputs?**

Whoever or whatever team is shipping the bot is/are ultimately responsible. Not every team or initiative will have a governance specialist available to track all guardrails or ensure perfect compliance. This means it is **you** that is responsible if someone on your team does not handle it or is specifically assigned.
