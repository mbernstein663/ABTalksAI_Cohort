# Query Test Results

How good is our RAG thus far in retrieving according to the question:

**"Is physical therapy covered under the Silver plan?"**

## Initial Results:

**Ultimatum**: The results are somewhat relevant, but the documents are also synthetic and there is only one chunk (structured) that actually mentions anything about the "silver plan" since I did not tailor the document creation for the plans specifically listed. But, I was disappointed to not see the Silver Plan chunk gathered as relevant.

We will try again with a different indexing (cosine similarity, HNSW), to see if it generates better results.

* ['--- Page 4 ---',

* 'Call the Marketplace Call Center at 1-800-318-2596 (TTY: 1-855-889-4325). A trained representative can help you find your insurerâ\x80\x99s number\nIs there an appeals process if I go to my regular doctor and find out later that my new plan doesnâ\x80\x99t cover them?\nYes. If your health insurance company doesnâ\x80\x99t pay for a visit to the doctor, you have the right to appeal the decision and have it reviewed by an independent third party.\nLearn about the appeals process\n.\nEmail this page\nEmail',

* 'Total sample cost $12,700 $5,600 $2,800\nPatient pays deductible $2,500 $1,900 $2,500\nPatient pays copays $250 $600 $75\nPatient pays coinsurance $1,900 $450 $45\nPatient pays $60 $20 $0\nlimits/exclusions\nTotal patient cost $4,710 $2,970 $2,620\nImportant: All content in this document is fictional. It is intended for software testing, document-processing demonstrations,\nand training exercises only.\nSynthetic training sample - not an actual health plan document Page 4',

* "Coverage Examples\nThese examples are not cost estimators. They show how the plan might cover sample medical situations. Actual costs depend on the services received,\nprovider charges, and plan rules.\nExample Peg Is Having a Baby Managing Type 2 Diabetes Mia's Simple Fracture\nSample care Prenatal visits, delivery, hospital Primary care visits, specialist visits, Emergency visit, x-ray, cast,\nstay, labs, anesthesia prescriptions, supplies follow-up visit\nTotal sample cost $12,700 $5,600 $2,800",

* 'Excluded Services and Other Covered Services\nServices Your Plan Generally Does NOT Cover Other Covered Services\nCosmetic surgery Acupuncture - 12 visits per year\nLong-term care Chiropractic care - 20 visits per year\nRoutine foot care Hearing aids - one device per ear every 36 months\nWeight-loss programs Infertility evaluation and limited treatment\nNon-emergency care outside the United States\nYour Rights to Continue Coverage']

## New Results:

New results were remarkably similar. It seems that the uncleaned nature of the chunks and irrelevancy of the generated documents are causing poor semantic association with the important parts of our query. Even though its explicitly mentioned, it seems to struggle with identifying the "silver plan" portion of the query because its embedding is probably making the retrieval become glued to the "benefits" cluster.

* [['--- Page 4 ---', 

* 'Call the Marketplace Call Center at 1-800-318-2596 (TTY: ...

*... [identical results] ...*

* ... months\nWeight-loss programs Infertility evaluation and limited treatment\nNon-emergency care outside the United States\nYour Rights to Continue Coverage']]

## Next Steps:

Regenerate the original documents, except this time ensure that they specifically mention the "silver plan" and are referencing the same ideas while the metadata remains identical between the documents.

## Regenerated:

[['Annual deductible $1,000 Exact value from plans.csv; no family or network split supplied.\nMember cost-share rate 30% Based on copay_pct; no service-specific schedule supplied.\nCoverage type HMO Exact categorical value from plans.csv.\nNetwork tier Bronze Exact categorical value from plans.csv.\nSynthetic claims linked to this plan\nClaim ID Member ID Procedure Claim amount Status Date filed\nC1005 M1003 X-ray $50 Pending 2023-04-10', 

'Call the Marketplace Call Center at 1-800-318-2596 (TTY: 1-855-889-4325). A trained representative can help you find your insurerâ\x80\x99s number\nIs there an appeals process if I go to my regular doctor and find out later that my new plan doesnâ\x80\x99t cover them?\nYes. If your health insurance company doesnâ\x80\x99t pay for a visit to the doctor, you have the right to appeal the decision and have it reviewed by an independent third party.\nLearn about the appeals process\n.\nEmail this page\nEmail', 

'- Prescription drug tiers, pharmacy rules, and formulary coverage\n- Claim allowed amount, paid amount, denial reason, and appeal outcome\nThis page intentionally avoids inventing benefits. It is a schema-aligned synthetic reference for\ndocument extraction and RAG testing.\nSynthetic training sample - not an actual health plan document Page 4', 

'C1005 M1003 X-ray $50 Pending 2023-04-10\nThese records show only the supplied procedure, amount, status, and filing date. No denial reason, allowed amount, payment amount, or\ndeductible accumulation is present in claims.csv.\nInformation not defined by the supplied schema\n- Out-of-pocket maximums and family accumulators\n- Service-specific copays, coinsurance, exclusions, and limits\n- Provider network rules, referral requirements, and prior authorization rules', 

'- Prescription drug tiers, pharmacy rules, and formulary coverage\n- Claim allowed amount, paid amount, denial reason, and appeal outcome\nThis page intentionally avoids inventing benefits. It is a schema-aligned synthetic reference for\ndocument extraction and RAG testing.\nSynthetic training sample - not an actual health plan document Page 3']]

## Results:

Again, we see a repeat of the same pitfall, although the gathered documents are not necessarily "irrelevant"- the embeddings are highly separated between groups, possibly because of characters, warnings, and junk content that gets pushed into the chunks- thus the RAG only pulls from the same document group. We may have to try again tomorrow and clean the chunks better.

# The Fix

**There was a major mistake in my code** that caused major separation between embeddings and ignoring text semantics. The embeddings were being generated from the chunk id's instead of the chunk content. The new `embeddings_2d.png` looks a lot more plausible now.

## New Results:

* [['Silver HMO (P102)\nLinked claims: 2. Status counts - Denied: 1, Approved: 1. Procedures - X-ray, Surgery.\nBronze HMO (P103)\nLinked claims: 1. Status counts - Pending: 1. Procedures - X-ray.\n8. Recommended production schema extensions\n9. Data dictionary\nplans.plan_id: Unique plan identifier and join key.\nplans.plan_name: Human-readable plan name.\nplans.monthly_premium: Monthly premium amount.\nplans.annual_deductible: Annual deductible amount.', 

* '- Do not infer coverage from procedure name or status alone.\n6. Supplied synthetic claim register\nThe plan cost-share percentage is shown only as reference data. The file does not provide enough information to calculate member responsibility, because deductible accumulation, allowed amount, service rules, and payment details are absent.\n7. Plan-specific claim observations\nGold PPO (P101)\nLinked claims: 2. Status counts - Pending: 1, Approved: 1. Procedures - X-ray, Surgery.\nSilver HMO (P102)', 

* 'Plan: Silver HMO. Premium: $300/month. Deductible: $1500. Coinsurance: 20%. Network: Silver.', 

* 'Summary of Benefits and Coverage: Synthetic\nPlan Comparison\nNorthstar Health Plan - dataset-aligned plan reference\nDOCUMENT_SET_ID: NORTHSTAR_SYNTHETIC_PLAN_LIBRARY\nSCHEMA_VERSION: 1.0\nSOURCE_FILES: plans.csv | claims.csv\nPLAN_IDS: P101 | P102 | P103\nPLAN_NAMES: Gold PPO | Silver HMO | Bronze HMO\nDATA_CLASSIFICATION: SYNTHETIC TRAINING ONLY\nIMPORTANT: Values below are reproduced from the supplied CSV files. The metal-tier labels are', 

* 'Bronze HMO $150 $1,000\n\nHMO / Bronze\n\nSelected plan schema linkage\nmember_id: M1001 plan_id: P101 plan_name: Gold PPO\nmonthly_premium: $500 | annual_deductible: $2,000 | copay_pct: 10 | network_tier: Gold\n\ncoverage_type: PPO\n\nSECTION 4 - DEPENDENT INFORMATION\n\nDependent name Relationship Date of birth\n\nStudent / disabled\n\nJordan Morgan Child 03/22/2017\n\nNo\n\nAvery Morgan Child 11/09/2020\n\nNo\n\nSECTION 5 - ACKNOWLEDGEMENTS\n\n[| | understand this is synthetic training data and not actual coverage.']]

Fixed! although the regenerated synthetic documents do not mention the surgery coverage explicitly, the gathered chunks are now relevant and cover silver plan schema specifically.
