# A/B Test Results

**Variant A:** k=3 retrieved chunks  
**Variant B:** k=5 retrieved chunks  
**Sample size:** 15 questions

## Question 1

**Question:** How does prior authorization work?

**Classification:** unstructured

| k=3 | k=5 |
|---|---|
| The context does not provide details on how prior authorization works, as it explicitly states that authorization rules are not included in the supplied schema. For specific plan rules, contact support.<br><br>**Tokens:** 35<br>**Score:** 1 <br><br>**Chunks:** enrollment-chunk-4, claims_process-chunk-9, benefits-chunk-5, claims_process-chunk-4, benefits-chunk-9 | The context does not provide details on how prior authorization works. For specific plan rules or authorization processes, contact support.<br><br>**Tokens:** 23<br>**Score:** 1 <br><br>**Chunks:** enrollment-chunk-4, claims_process-chunk-9, benefits-chunk-5, claims_process-chunk-4, benefits-chunk-9 |

## Question 2

**Question:** When is prior authorization required?

**Classification:** unstructured

| k=3 | k=5 |
|---|---|
| The context provided does not specify when prior authorization is required. For detailed guidance, please contact support.<br><br>**Tokens:** 20<br>**Score:** 1 <br><br>**Chunks:** enrollment-chunk-4, claims_process-chunk-4, claims_process-chunk-9, claims_process-chunk-3, claims_process-chunk-5 | The context provided does not specify when prior authorization is required. For detailed guidance, contact support.<br><br>**Tokens:** 19<br>**Score:** 1<br><br>**Chunks:** enrollment-chunk-4, claims_process-chunk-4, claims_process-chunk-9, claims_process-chunk-3, claims_process-chunk-5 |

## Question 3

**Question:** How do I appeal a denied claim?

**Classification:** both

| k=3 | k=5 |
|---|---|
| To appeal a denied claim, contact the Marketplace Call Center at 1-800-318-2596 (TTY: 1-855-889-4325). A representative can guide you through the process, which includes having your claim reviewed by an independent third party. For specific steps, refer to the "Learn about the appeals process" link provided in the context.<br><br>**Tokens:** 75<br>**Score:** 1 <br><br>**Chunks:** claims_process-chunk-9, medical_care_FAQ-chunk-5, claims_process-chunk-4, claims_process-chunk-7, benefits-chunk-13 | To appeal a denied claim, contact the Marketplace Call Center at 1-800-318-2596 (TTY: 1-855-889-4325) for assistance. A representative can guide you through the appeals process and help locate your insurer’s contact information. If further support is needed, contact customer support. Do not provide medical advice.<br><br>**Tokens:** 71<br>**Score:** 1 <br><br>**Chunks:** claims_process-chunk-9, medical_care_FAQ-chunk-5, claims_process-chunk-4, claims_process-chunk-7, benefits-chunk-13 |

## Question 4

**Question:** What steps are involved in an appeal after a denial?

**Classification:** unstructured

| k=3 | k=5 |
|---|---|
| The context does not provide detailed steps for appealing a denial. For specific guidance, contact the Marketplace Call Center at 1-800-318-2596 or your insurer’s support team. Do not seek medical advice.<br><br>**Tokens:** 44<br>**Score:** 0 <br><br>**Chunks:** claims_process-chunk-9, medical_care_FAQ-chunk-5, claims_process-chunk-4, claims_process-chunk-3, claims_process-chunk-7 | The context mentions the right to appeal a denied claim through an independent third party but does not specify detailed steps for the appeal process. For guidance, contact the Marketplace Call Center at 1-800-318-2596. Do not contact support for medical advice.<br><br>**Tokens:** 53<br>**Score:** 1<br><br>**Chunks:** claims_process-chunk-9, medical_care_FAQ-chunk-5, claims_process-chunk-4, claims_process-chunk-3, claims_process-chunk-7 |

## Question 5

**Question:** How does in-network coverage differ from out-of-network coverage?

**Classification:** unstructured

| k=3 | k=5 |
|---|---|
| The context explains that in-network providers (contracted with your health plan) typically result in lower out-of-pocket costs compared to out-of-network providers, which may not have contracts with your plan and could lead to higher expenses. Specific cost details (e.g., deductibles, coinsurance) vary by plan tier. For precise differences, consult your plan’s documentation or contact support.<br><br>**Tokens:** 76<br>**Score:** 1 <br><br>**Chunks:** medical_care_FAQ-chunk-2, benefits-chunk-2, enrollment-chunk-3, plan-1, benefits-chunk-5 | In-network coverage refers to services provided by doctors or providers contracted with your health plan, typically resulting in lower out-of-pocket costs like deductibles, copays, or coinsurance. Out-of-network coverage involves providers not contracted with your plan, often leading to higher costs, as the plan may not cover all expenses or may require higher payments. Always check your plan’s network details for specific terms.<br><br>**Tokens:** 79<br>**Score:** 1<br><br>**Chunks:** medical_care_FAQ-chunk-2, benefits-chunk-2, enrollment-chunk-3, plan-1, benefits-chunk-5 |

## Question 6

**Question:** What happens if I receive care from an out-of-network provider?

**Classification:** unstructured

| k=3 | k=5 |
|---|---|
| If you receive care from an out-of-network provider, your health plan may not cover the full cost, and you could face higher out-of-pocket expenses, such as copayments, deductibles, or coinsurance. Always check your plan’s provider directory or contact your insurer for specific details. For further assistance, contact your health plan’s support.<br><br>**Tokens:** 70<br>**Score:** 1 <br><br>**Chunks:** medical_care_FAQ-chunk-2, medical_care_FAQ-chunk-3, medical_care_FAQ-chunk-4, medical_care_FAQ-chunk-1, plan-2 | The context does not specify the exact consequences of receiving care from an out-of-network provider. For detailed information, please contact your health plan's support.<br><br>**Tokens:** 30<br>**Score:** 0 <br><br>**Chunks:** medical_care_FAQ-chunk-2, medical_care_FAQ-chunk-3, medical_care_FAQ-chunk-4, medical_care_FAQ-chunk-1, plan-2 |

## Question 7

**Question:** What kinds of services can be excluded from coverage?

**Classification:** unstructured

| k=3 | k=5 |
|---|---|
| The context provided does not specify services that can be excluded from coverage. For detailed information, please contact your health plan's support team.<br><br>**Tokens:** 27<br>**Score:** 1<br><br>**Chunks:** medical_care_FAQ-chunk-2, medical_care_FAQ-chunk-3, benefits-chunk-5, medical_care_FAQ-chunk-1, plan-2 | The context does not specify particular services that are excluded from coverage. For detailed information about excluded services, please contact your health plan's support team.<br><br>**Tokens:** 29<br>**Score:** 1 <br><br>**Chunks:** medical_care_FAQ-chunk-2, medical_care_FAQ-chunk-3, benefits-chunk-5, medical_care_FAQ-chunk-1, plan-2 |

## Question 8

**Question:** How can I tell whether a service is eligible for coverage?

**Classification:** unstructured

| k=3 | k=5 |
|---|---|
| The context does not provide specific guidance on determining service eligibility. To check coverage for a service, contact your health plan’s customer support or review your plan’s benefits guide. If you need further assistance, reach out to your insurer directly.<br><br>**Tokens:** 47<br>**Score:** 1<br><br>**Chunks:** medical_care_FAQ-chunk-3, medical_care_FAQ-chunk-4, benefits-chunk-5, medical_care_FAQ-chunk-2, medical_care_FAQ-chunk-5 | The context does not provide specific guidance on determining service eligibility for coverage. To check if a service is covered, contact your insurer directly using the number on your insurance card or visit their website. If you need further assistance, contact the Marketplace Call Center at 1-800-318-2596.<br><br>**Tokens:** 60<br>**Score:** 1<br><br>**Chunks:** medical_care_FAQ-chunk-3, medical_care_FAQ-chunk-4, benefits-chunk-5, medical_care_FAQ-chunk-2, medical_care_FAQ-chunk-5 |

## Question 9

**Question:** What information do I need to submit an appeal for a claim?

**Classification:** both

| k=3 | k=5 |
|---|---|
| The context does not specify the exact information required to submit an appeal for a claim. For assistance, contact the Marketplace Call Center at 1-800-318-2596 (TTY: 1-855-889-4325) or your insurer’s appeals process.<br><br>**Tokens:** 55<br>**Score:** 1 <br><br>**Chunks:** claims_process-chunk-9, claims_process-chunk-4, claims_process-chunk-3, medical_care_FAQ-chunk-5, claims_process-chunk-7 | The context does not specify the exact information required to submit an appeal. For details, contact your insurer or the Marketplace Call Center at 1-800-318-2596.<br><br>**Tokens:** 36<br>**Score:** 1 <br><br>**Chunks:** claims_process-chunk-9, claims_process-chunk-4, claims_process-chunk-3, medical_care_FAQ-chunk-5, claims_process-chunk-7 |

## Question 10

**Question:** How are denied claims handled during the appeal process?

**Classification:** both

| k=3 | k=5 |
|---|---|
| If a claim is denied, you have the right to appeal the decision. The appeal will be reviewed by an independent third party to determine if the denial was justified. For specific guidance or to initiate the process, contact the Marketplace Call Center at 1-800-318-2596. If you need further assistance, reach out to your insurer’s support team. <br><br>*Note: This response is based on the provided context. For personalized help, contact support.*<br><br>**Tokens:** 93<br>**Score:** 1 <br><br>**Chunks:** claims_process-chunk-9, medical_care_FAQ-chunk-5, claims_process-chunk-4, claims_process-chunk-7, claims_process-chunk-1 | If a claim is denied, you have the right to appeal the decision. The appeal will be reviewed by an independent third party. For assistance with the appeals process, contact the Marketplace Call Center at 1-800-318-2596.<br><br>**Tokens:** 49<br>**Score:** 1<br><br>**Chunks:** claims_process-chunk-9, medical_care_FAQ-chunk-5, claims_process-chunk-4, claims_process-chunk-7, claims_process-chunk-1 |

## Question 11

**Question:** Does coverage require prior authorization for some services?

**Classification:** unstructured

| k=3 | k=5 |
|---|---|
| The provided context does not specify whether prior authorization is required for services. For detailed information, contact your health plan's support or review your plan's documentation.<br><br>**Tokens:** 31<br>**Score:** 1<br><br>**Chunks:** medical_care_FAQ-chunk-2, medical_care_FAQ-chunk-3, medical_care_FAQ-chunk-5, medical_care_FAQ-chunk-4, benefits-chunk-5 | The context provided does not specify whether prior authorization is required for services. For detailed information, please contact your health plan's support team.<br><br>**Tokens:** 27<br>**Score:** 1<br><br>**Chunks:** medical_care_FAQ-chunk-2, medical_care_FAQ-chunk-3, medical_care_FAQ-chunk-5, medical_care_FAQ-chunk-4, benefits-chunk-5 |

## Question 12

**Question:** How should I verify whether a provider is in-network?

**Classification:** unstructured

| k=3 | k=5 |
|---|---|
| To verify if a provider is in-network:  <br>1. Check your health plan’s provider directory on their website or via the Marketplace account.  <br>2. Contact your insurer using the number on your insurance card or their website.  <br>3. Call the provider’s office directly to confirm they accept your plan.  <br><br>For specific details, refer to your plan’s documentation or contact support if needed.<br><br>**Tokens:** 78<br>**Score:** 1<br><br>**Chunks:** medical_care_FAQ-chunk-2, medical_care_FAQ-chunk-3, medical_care_FAQ-chunk-4, claims_process-chunk-3, benefits-chunk-5 | To verify if a provider is in-network:  <br>1. Check your health plan’s provider directory on their website.  <br>2. Contact your insurer using the number on your insurance card.  <br>3. Call the provider’s office to confirm they accept your plan.  <br><br>In-network providers typically offer lower out-of-pocket costs. If unsure, contact your plan’s customer service for confirmation.<br><br>**Tokens:** 76<br>**Score:** 1<br><br>**Chunks:** medical_care_FAQ-chunk-2, medical_care_FAQ-chunk-3, medical_care_FAQ-chunk-4, claims_process-chunk-3, benefits-chunk-5 |

## Question 13

**Question:** What should I do if a service is not covered?

**Classification:** unstructured

| k=3 | k=5 |
|---|---|
| If a service is not covered by your plan, you can appeal the decision through an independent third-party review. Contact your insurer’s customer service using the number on your insurance card or the Marketplace Call Center at 1-800-318-2596 for assistance. Do not seek medical advice; consult your healthcare provider for guidance.<br><br>**Tokens:** 66<br>**Score:** 1<br><br>**Chunks:** medical_care_FAQ-chunk-5, medical_care_FAQ-chunk-3, medical_care_FAQ-chunk-2, medical_care_FAQ-chunk-1, medical_care_FAQ-chunk-4 | If a service is not covered by your plan, you can appeal the decision through an independent third-party review. Contact your insurer directly using the number on your insurance card or the Marketplace Call Center (1-800-318-2596) for guidance. Review your plan’s provider directory to confirm if the service provider is in-network, as out-of-network services may not be covered. For detailed steps, visit your plan’s website or contact support.<br><br>**Tokens:** 90<br>**Score:** 1<br><br>**Chunks:** medical_care_FAQ-chunk-5, medical_care_FAQ-chunk-3, medical_care_FAQ-chunk-2, medical_care_FAQ-chunk-1, medical_care_FAQ-chunk-4 |

## Question 14

**Question:** Can an out-of-network service still be eligible for coverage?

**Classification:** unstructured

| k=3 | k=5 |
|---|---|
| The context does not specify whether out-of-network services are eligible for coverage. It emphasizes that in-network providers typically offer lower costs and outlines an appeals process for denied claims. For precise details about your plan, contact your insurer or the Marketplace Call Center at 1-800-318-2596.<br><br>**Tokens:** 60<br>**Score:** 0<br><br>**Chunks:** medical_care_FAQ-chunk-2, plan-2, plan-1, medical_care_FAQ-chunk-3, medical_care_FAQ-chunk-5 | If you receive care from an out-of-network provider, coverage may still be possible, but it typically depends on your plan's specific terms. Out-of-network services often involve higher out-of-pocket costs, and coverage may be limited or require prior authorization. For detailed information about your plan's coverage, contact your insurer directly or visit their provider directory. If you're unsure, reach out to the Marketplace Call Center at 1-800-318-2596.<br><br>**Tokens:** 92<br>**Score:** 1<br><br>**Chunks:** medical_care_FAQ-chunk-2, plan-2, plan-1, medical_care_FAQ-chunk-3, medical_care_FAQ-chunk-5 |

## Question 15

**Question:** What details should I review before appealing a denied claim?

**Classification:** both

| k=3 | k=5 |
|---|---|
| The context does not specify details to review before appealing a denied claim. For assistance, contact the Marketplace Call Center at 1-800-318-2596.<br><br>**Tokens:** 33<br>**Score:** 0<br><br>**Chunks:** claims_process-chunk-9, claims_process-chunk-4, claims_process-chunk-3, medical_care_FAQ-chunk-5, claims_process-chunk-7 | Before appealing a denied claim, review the following details from the context:  <br>1. **Claim status** (denied, approved, pending) and **filing date**.  <br>2. **Duplicate risk**: Ensure no identical claim (same member, procedure, amount, date) exists under another claim_id.  <br>3. **Plan linkage**: Verify the claim is linked to a valid plan_id in plans.csv, including plan_name, annual_deductible, copay_pct, coverage_type, and network_tier.  <br>4. **Schema validity**: Confirm required fields (e.g., unique claim_id, correct date format, numeric amount) are present.  <br>5. **Rules compliance**: Ensure the denial aligns with implemented benefit, network, or pricing rules.  <br><br>If the context does not explicitly address these points, contact support for further guidance.<br><br>**Tokens:** 172<br>**Score:** 1<br><br>**Chunks:** claims_process-chunk-9, claims_process-chunk-4, claims_process-chunk-3, medical_care_FAQ-chunk-5, claims_process-chunk-7 |

# Results

| Variant | Total Score |  Accuracy | Total Answer Tokens |
| ------- | ----------: | --------: | ------------------: |
| **k=3** |   **12/15** | **80.0%** |             **810** |
| **k=5** |   **14/15** | **93.3%** |             **906** |

Overall k=5 achieved 11% higher token usage but 13.3% accuracy improvement over k=3. Overall, more chunks seems to yield better results. We will stick with k=5. Kartheek gave me the idea to use chunks lol