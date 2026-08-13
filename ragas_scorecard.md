# RAGAS Scorecard

## Average Scores

| Metric | Score |
|---|---:|
| Faithfulness | 0.563 |
| Answer Relevancy | 0.622 |
| Context Precision | 0.409 |
| Context Recall | 0.537 |

## Per-Question Scores

| Question | Faithfulness | Answer Relevancy | Context Precision | Context Recall |
|---|---:|---:|---:|---:|
| What is the annual deductible for plan P101? | 0.000 | 1.000 | 0.000 | 0.000 |
| What is the annual deductible for plan P102? | 0.000 | 1.000 | 0.000 | 0.000 |
| Which has the lower annual deductible, P101 or P102? | 0.000 | 0.928 | 0.000 | 0.000 |
| What is the annual deductible for plan P103? | 0.500 | 0.000 | 0.000 | 0.000 |
| Are X-rays excluded under plan P102? | 0.714 | 1.000 | 1.000 | 1.000 |
| Is surgery specifically covered or excluded under plan P101? | 0.750 | 0.000 | 0.646 | 1.000 |
| What services are explicitly excluded under plan P101? | 0.000 | 0.000 | 0.000 | 0.000 |
| Does the denied X-ray claim C1003 prove that X-rays are excluded under P102? | 0.667 | 0.000 | 0.917 | 0.667 |
| What is the status of claim C1004? | 1.000 | 1.000 | 1.000 | 1.000 |
| What is the status of claim C1003? | 1.000 | 1.000 | 1.000 | 1.000 |
| What is the status of claim C1001? | 1.000 | 1.000 | 1.000 | 1.000 |
| What is the status of claim C1002? | 1.000 | 1.000 | 1.000 | 1.000 |
| How do the monthly premiums of P101 and P102 compare? | 1.000 | 0.780 | 0.000 | 1.000 |
| How do the annual deductibles of P101 and P102 compare? | 0.333 | 0.916 | 0.000 | 1.000 |
| How do the member cost-share rates of P101 and P102 compare? | 0.500 | 0.000 | 0.000 | 0.000 |
| How do the coverage type and network tier of P101 and P102 compare? | 1.000 | 0.567 | 0.806 | 1.000 |
| Which plan has the lowest monthly premium among P101, P102, and P103? | 0.000 | 1.000 | 0.000 | 0.000 |
| Which plan has the lowest annual deductible among P101, P102, and P103? | 0.667 | 0.000 | 0.000 | 0.000 |

## Conclusion

**Hypothesis**: Ultimately, it seems like our context precision is the weakest suit in our RAG application scores. This indicates that the retrieved chunks have weak relevancy to the questions. This is most likely because the synthetic documents I created did not align perfectly with the types of questions that a user might ask and all potentially important insurance information. 

**What to do**: The smart thing to do here is to run an A/B test where I implement stronger synthetic documents and possibly try adjusting chunking parameters like size and overlap. Overall, not a bad result.
