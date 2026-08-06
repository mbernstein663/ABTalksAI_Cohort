# Fine-Tuning Comparison

### Test 1

**Question**

What is the out-of-pocket maximum for Gold PPO?

**Held-out reference answer**

The available Gold PPO information does not include an out-of-pocket maximum. The out-of-pocket maximum is the most a member generally pays for covered services during a plan year, subject to the plan's rules and exclusions.

Check the plan's Summary of Benefits and Coverage or member portal for the official amount.

**Base model response**

The out-of-pocket maximum for Gold PPO (Premium Per Patient) is $10,500 per year.

**Fine-tuned model response**

The out-of-pocket maximum for Gold PPO (Premium Per Patient) is $10,500 per year.

*tone:* 4
*correctness:* 5
*disclaimer usage:* 1
*terminology clarity:* 2

---

### Test 2

**Question**

Do I need prior authorization for surgery?

**Held-out reference answer**

The available plan information does not include prior-authorization requirements for surgery. Check the plan's prior-authorization section or online authorization tool before scheduling the procedure. You can also call the member-services number on your insurance card.

An approved surgery claim in the sample records does not establish that every surgery is covered or that prior authorization is unnecessary.

**Base model response**

No, you do not typically need prior authorization for surgical procedures unless specifically required by your healthcare provider or under certain circumstances outlined in your insurance policy. Always check with your insurance company for details regarding any specific requirements.

**Fine-tuned model response**

No, you do not typically need prior authorization for surgical procedures unless specifically authorized by your healthcare provider.

*tone:*  2
*correctness:* 5
*disclaimer usage:* 1
*terminology clarity:* 3

---

### Test 3

**Question**

What is the status of claim C1005?

**Held-out reference answer**

Claim **C1005** is marked as **Pending**. This means the supplied record does not yet show a final approved or denied status. The available information does not provide an expected completion date.

**Base model response**

Claim C1005 has been denied by the insurer.

**Fine-tuned model response**

Claim C1005 has been denied by the insurer.

*tone:* 3
*correctness:* 5
*disclaimer usage:* 1
*terminology clarity:* 2

---

### Test 4

**Question**

What is the annual premium for Bronze HMO?

**Held-out reference answer**

The Bronze HMO annual premium is **$1,800**, calculated from its **$150 monthly premium multiplied by 12 months**. This is the cost of maintaining coverage and does not include deductibles or other out-of-pocket costs.

**Base model response**

The annual premium for Bronze HMO (Health Maintenance Organization) typically ranges from $100 to $250 per month. This price can vary depending on your location and other factors like your age, gender, and whether you have any pre-existing conditions. It's important to check with your specific HMO or health insurance provider for the most accurate and up-to-date information.

**Fine-tuned model response**

The annual premium for Bronze HMO (Health Maintenance Organization) varies by location and can range from $100 to $250 per month. You should contact your healthcare provider or the HMO's customer service department for the most accurate and up-to-date information.

*tone:* 3
*correctness:* 5
*disclaimer usage:* 3
*terminology clarity:* 3

---

### Test 5

**Question**

A surgery claim was approved under Silver HMO. Does that mean my surgery will also be covered?

**Held-out reference answer**

No. The approval of claim **C1004** does not establish coverage for another surgery. Coverage may depend on the procedure, member eligibility, provider network, authorization requirements, medical coding, and plan rules.

Use the insurer's online benefit or prior-authorization resources, or call the number on your insurance card, for a determination about your specific procedure.

**Base model response**

Yes, if your surgery was approved by Silver HMO, it typically means that your surgery will also be covered under their policy. However, specifics can vary depending on the terms of your individual Silver HMO contract. It's best to check with your healthcare provider or the specific Silver HMO office for the most accurate information regarding your particular situation.

**Fine-tuned model response**

Yes, if your surgery was approved by Silver HMO, it means your surgery will likely be covered under their policy. However, it's important to check with your specific HMO or plan to confirm coverage details.

*tone:* 3
*correctness:* 5
*disclaimer usage:* 5
*terminology clarity:* 2

---

## Conclusion

Overall, I think there is improvement over the base model for two reasons:

1. The fine-tuned model is more concrete about its answers. There is no "I think," but it will typically give a disclaimer to go back and check with your provider.
2. Its very short-winded in its reponses. It will not overexplain, and  might reduce headaches/frustration if it was implemented as an actual healthcare chatbot.

Overall, I don't think the work was worth it. I think it could be vastly improved with just some ordinary prompt engineering. I think fine-tuning should be saved for larger and more expansive RAG projects where we might have more supplemental training data.
