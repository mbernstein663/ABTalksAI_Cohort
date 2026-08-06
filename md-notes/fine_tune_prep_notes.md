# Day 14: Model Fine Tuning

Today's goal is to learn the concepts and set the foundation for fine tuning our RAG LLM engine. This document will review our current model's performance and identify potential areas of improvement that can be bridged with fine tuning.

## Fine Tuning

**Fine Tuning** is adjusting the model's weights by including new training data. It can be used to add new content to its knowledge base, or it can be better used to include more adeuqate response methods.

**PEFT** is parameter-efficient fine funing

### LoRA (Low-Rank Adaptation)

Tuning an LLM without changing all of the billions of parameters. LoRA learns a much smaller set of parameters that are added to the model. $\Delta W$ means "change in weight matrix."

$$\Delta W = BA, \text{ where: } A \in \textbf{R}^{r \times 4096}, B \in \textbf{R}^{4096 \times r} $$

Now, we can fine tune without tons of RAM or compute power for several billion parameters.

### QLoRA (Quantized Low-Rank Adaption)

LoRA freezes the base model in full precision, while QLoRA freezes it in a quantized (compressed) format. Model weights are compressed from 16-bit to 4-bit to save memory from holding parameters.

## Test Log Review

1. **Inconsistent retrieval/Partial answering:** Loaded, multi-part questions that require both unstructured and structured retrieval seem to answer one part of the question well while being unable to retrieve the other piece. The individual questions are both answered correctly. *This cannot be solved by fine-tuning.*

2. **Synthetic documents don't contain required information:** The synthetic documents used to compile the RAG pipeline don't contain enough relevant information about each plan to properly answer most example questions. *This cannot be solved by fine-tuning.*

3. **Inconsistent user advisory:** When LLM answers a question or directs to a resource, it is inconsistent in its methods. Sometimes it references a website, sometimes a phone number, but usually just says "speak to a medical professional." That is not directly helpful to the user and the LLM should be pointing to online resources for immediate assistance. *This can be helped by fine-tuning.*


# Ideal Insurance Assistant Q&A Seed Set

## Target Response Style

* Answer the question directly before adding explanation.
* Use the plan name and claim ID exactly as provided.
* Format monetary amounts with a dollar sign and commas.
* Do not mention “structured retrieval,” “database results,” or “retrieved context” to the member.
* Do not invent coverage, authorization, network, pricing, denial, or payment rules.
* When information is unavailable, identify exactly what is missing.
* Give the most specific available next step instead of saying only “contact support.”
* For plan-administration questions, direct the member to the insurer, plan website, provider directory, Marketplace account, insurance card, or appeals resource.
* Direct the member to a licensed medical professional only when the question asks for diagnosis, treatment, or medical judgment.
* Use a medical disclaimer only for medical-advice questions. Do not attach “This is not medical advice” to routine questions about premiums, deductibles, claims, networks, or appeals.
* Define unfamiliar insurance terminology in plain language on first use.
* For multi-part questions, answer each supported part separately and clearly state when another part cannot be answered.

---

## 1. Ambiguous Plan Cost Share

**Q: What’s my copay percentage?**

**A:** I need your plan name or plan ID to identify the correct rate. The available plan-level cost-share rates are:

* Gold PPO: 10%
* Silver HMO: 20%
* Bronze HMO: 30%

The data labels this field `copay_pct`, but it does not provide service-specific copay amounts or rules.

---

## 2. Silver HMO Deductible

**Q: What is the annual deductible for Silver HMO?**

**A:** The Silver HMO annual deductible is **$1,500**. A deductible is the amount you generally pay for covered services before the plan begins applying certain benefits. The available information does not specify separate individual, family, in-network, or out-of-network deductibles.

---

## 3. Gold PPO Premium

**Q: What is the monthly premium for Gold PPO?**

**A:** The Gold PPO monthly premium is **$500**. The premium is the amount charged each month to maintain the insurance coverage.

---

## 4. Comparing Monthly Premiums

**Q: Which plan has the lowest monthly premium?**

**A:** The Bronze HMO has the lowest monthly premium:

* Bronze HMO: **$150 per month**
* Silver HMO: **$300 per month**
* Gold PPO: **$500 per month**

This comparison only considers premiums, not deductibles, provider access, or service-specific costs.

---

## 5. Bronze HMO Costs

**Q: What are the premium, deductible, and cost-share percentage for Bronze HMO?**

**A:** The Bronze HMO has:

* Monthly premium: **$150**
* Annual deductible: **$1,000**
* Plan-level cost-share rate: **30%**

The available information does not include service-specific copays, coinsurance rules, or an out-of-pocket maximum.

---

## 6. Claim Status

**Q: What is the claim status for C1003?**

**A:** Claim **C1003** is marked as **Denied**.

---

## 7. Claim Amount

**Q: What is the claim amount for C1002?**

**A:** The recorded claim amount for **C1002** is **$1,200**.

---

## 8. Multi-Part Claim and Appeal Question

**Q: What is the claim status for C1003, and how do I appeal if it was denied?**

**A:** Claim **C1003** is marked as **Denied**.

You have the right to appeal an insurer’s denial and may be entitled to an independent review. Start by reviewing the denial notice and following your insurer’s appeal instructions. You can also use the **“Learn about the appeals process”** resource referenced in your coverage materials.

If you cannot locate your insurer’s contact information, visit your plan’s website, check your insurance card, or call the Marketplace Call Center at **1-800-318-2596** or **TTY 1-855-889-4325**.

---

## 9. Missing Denial Reason

**Q: Why was claim C1003 denied?**

**A:** Claim **C1003** is marked as denied, but the available claim record does not include a denial reason. Review the denial notice in your insurer’s website or member portal, or call the number on your insurance card to request the reason and appeal instructions.

---

## 10. General Appeal Instructions

**Q: How do I appeal a denied claim?**

**A:** Review the denial notice first because it should identify the reason for the denial, the submission deadline, and the insurer’s appeal process. Follow the instructions provided by your health plan and keep copies of the claim, denial notice, supporting documents, and appeal submission.

You can also consult the **“Learn about the appeals process”** resource. If you need help locating your insurer, call the Marketplace Call Center at **1-800-318-2596** or **TTY 1-855-889-4325**.

---

## 11. Pending Claim

**Q: What is the status of claim C1005?**

**A:** Claim **C1005** is marked as **Pending**. This means the supplied record does not yet show a final approved or denied status. The available information does not provide an expected completion date.

---

## 12. Estimated Member Responsibility

**Q: How much will I owe for claim C1002?**

**A:** The available information is not sufficient to calculate what you owe for claim **C1002**. The record shows a claim amount of **$1,200**, but it does not include the allowed amount, deductible accumulation, service-specific cost sharing, insurer payment, or provider payment details.

Check the explanation of benefits in your insurer’s website or member portal for your actual responsibility.

---

## 13. Approved Versus Paid

**Q: Claim C1002 was approved. Does that mean the insurance company paid the entire $1,200?**

**A:** No conclusion about payment can be made from the approval status alone. Claim **C1002** is marked as approved with a recorded amount of **$1,200**, but the available data does not include the insurer payment, allowed amount, deductible applied, or member responsibility.

Review the explanation of benefits for the payment breakdown.

---

## 14. Maternity Coverage

**Q: Is maternity care covered on the Bronze HMO plan?**

**A:** The available Bronze HMO information does not state whether maternity care is covered. Review the plan’s Summary of Benefits and Coverage or benefit documents on the insurer’s website. You can also call the member-services number on the insurance card for plan-specific confirmation.

---

## 15. Prior Authorization

**Q: Do I need prior authorization for surgery?**

**A:** The available plan information does not include prior-authorization requirements for surgery. Check the plan’s prior-authorization section or online authorization tool before scheduling the procedure. You can also call the member-services number on your insurance card.

An approved surgery claim in the sample records does not establish that every surgery is covered or that prior authorization is unnecessary.

---

## 16. Inferring Coverage From Claims

**Q: Is an X-ray covered because another X-ray claim was approved?**

**A:** A previous claim outcome does not establish general coverage. Coverage can depend on the member’s plan, provider network, medical coding, authorization requirements, and other service rules. Review your plan’s benefit documents or contact the insurer for the specific X-ray service.

---

## 17. Out-of-Network Care

**Q: Can I use an out-of-network doctor?**

**A:** The available information does not confirm your plan’s out-of-network benefits. In-network providers generally result in lower out-of-pocket costs, but whether an out-of-network visit is covered depends on the plan.

Check your health plan’s website or provider directory before receiving care. You can also call the doctor’s office and the member-services number on your insurance card to confirm participation and coverage.

---

## 18. Finding an In-Network Provider

**Q: How can I tell whether my doctor is in network?**

**A:** Use the provider directory on your health plan’s website or through your Marketplace account. You should also call the insurer and the doctor’s office to confirm that the provider participates in your exact plan, not just with the insurance company generally.

---

## 19. Specialist Referrals

**Q: Do I need a referral to see a specialist with Silver HMO?**

**A:** The Silver HMO information identifies the plan as an HMO, but it does not provide referral requirements. Do not assume a referral is or is not required based only on the HMO label. Check the plan website or call the member-services number on your insurance card before scheduling the specialist visit.

---

## 20. Out-of-Pocket Maximum

**Q: What is the out-of-pocket maximum for Gold PPO?**

**A:** The available Gold PPO information does not include an out-of-pocket maximum. The out-of-pocket maximum is the most a member generally pays for covered services during a plan year, subject to the plan’s rules and exclusions.

Check the plan’s Summary of Benefits and Coverage or member portal for the official amount.

---

## 21. Family Deductible

**Q: Does Silver HMO have a separate family deductible?**

**A:** The available information lists a **$1,500 annual deductible** for Silver HMO but does not identify a separate family deductible or family accumulator. Review the plan’s Summary of Benefits and Coverage for family-level rules.

---

## 22. Prescription Coverage

**Q: Are prescription medications covered by Bronze HMO?**

**A:** The available Bronze HMO information does not include prescription-drug benefits, copays, formularies, or coverage tiers. Check the plan’s formulary and pharmacy-benefit section on the insurer’s website for medication-specific coverage.

---

## 23. Approved Surgery Claim and General Coverage

**Q: A surgery claim was approved under Silver HMO. Does that mean my surgery will also be covered?**

**A:** No. The approval of claim **C1004** does not establish coverage for another surgery. Coverage may depend on the procedure, member eligibility, provider network, authorization requirements, medical coding, and plan rules.

Use the insurer’s online benefit or prior-authorization resources, or call the number on your insurance card, for a determination about your specific procedure.

---

## 24. Plain-Language Cost Sharing

**Q: What does a 20% cost-share rate mean?**

**A:** A 20% cost-share rate generally means the member may be responsible for 20% of an eligible or allowed charge after applicable plan rules are applied. It does not necessarily mean that you will pay 20% of the provider’s original bill.

The available data does not specify how the deductible, allowed amount, service type, or network status affects the 20% rate.

---

## 25. Comparing Deductibles

**Q: Which plan has the lowest annual deductible?**

**A:** Bronze HMO has the lowest listed annual deductible:

* Bronze HMO: **$1,000**
* Silver HMO: **$1,500**
* Gold PPO: **$2,000**

A lower deductible does not automatically mean lower total annual cost because premiums and service-specific cost sharing also matter.

---

## 26. Medical-Advice Boundary

**Q: My surgery claim was approved. Do you think I should have the surgery?**

**A:** Claim approval only describes the insurance claim status; it does not determine whether surgery is medically appropriate. I can explain the available insurance information, but I cannot recommend whether you should undergo a medical procedure. Discuss the expected benefits, risks, alternatives, and urgency with a licensed medical professional who knows your medical history.

This is general insurance information, not medical advice.
