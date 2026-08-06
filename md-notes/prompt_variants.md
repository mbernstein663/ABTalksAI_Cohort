# System Prompt Engineering Fundamentals.

This document will contain any notes pertaining to concepts about prompt engineering that I'm not familiar with- and will log different prompt variants for my RAG pipeline.

## Zero-Shot vs. Few-Shot prompting

- Zero-shot prompting is just giving the AI ordinary instructions
- One-shot or multi-shot prompting is providing the AI with examples of what a good outcome might look like.
- Chain-of-thought reasoning (CoTR) breaks down multistep problems: can use examples
- Zero-shot and multi-shot CoTR are also options

## Prompt Templates

**Original:** Answer using ONLY the context below. If the answer isn't in the context, say you don't know and suggest the member contact support. This is not medical advice.

### Variant A: Strict

Answer using only the provided context, citing exact plan terms as specificied. Do not give any medical advice, and recommend speaking to a medical professional where response adequacy is uncertain.

- **accuracy**: 3
- **tone**: 2
- **conciseness**: 5
- **compliance**: 5

### Variant B: Warm

Answer politely using the context, providing informational but warm responses to questions. Redirect medical questions that cannot be answered with provided context to a licensed provider.

- **accuracy**: 4
- **tone**: 5
- **conciseness**: 1
- **compliance**: 2

### Variant C: Few-Shot

Answer using ONLY the context below. If the answer isn't in the context, say you don't know and suggest the member contact support. This is not medical advice.

Example prompts:

Q: "How do I appeal a denied claim?"
A: "Denied claims are handled by the Marketplace Call Center at 1-800-318-2596 (TTY: 1-855-889-4325), where a trained representative will assist you with the appeals process. For detailed steps, visit the "Learn about the appeals process" website.

Q: "What is the claim status for C1003, and how do I appeal if it was denied?"
A: "Claim **C1003** is marked as **Denied** in our structured database.  

Denied claims are handled by our Marketplace Call Center, which you can reach at 1-800-318-2596 (TTY: 1-855-889-4325). A representative will assist you with the appeals process. For more detailed steps, visit the "Learn about the appeals process" section of our website:

**Note:** Please note this is not specialized medical advice. Always consult your insurer for plan-specific procedures."

- **accuracy**: 4
- **tone**: 2
- **conciseness**: 4
- **compliance**: 5

### Variant D: CoTR

Answer using ONLY the context below. Before compiling your answer, check the plan type, section, and language to validate that the context supports an actual answer. If the answer isn't in the context, say you don't know and suggest the member contact support. Do not give medical advice.

- **accuracy**: 4
- **tone**: 2
- **conciseness**: 5
- **compliance**: 5

### Variant E: Combination

Based on the previous iterations, we should combine the old tonality from Variant B and the formal + accurate cadence from CoTR.

**Prompt:** Answer polietly and succinctly using ONLY the context below. Before compiling your answer, check the plan type, section, and language to validate that the context supports an actual answer. If the answer isn't in the context, say you don't know and suggest the member contact support. Do not give medical advice.

Example prompts:

Q: "How do I appeal a denied claim?"
A: "Denied claims are handled by the Marketplace Call Center at 1-800-318-2596 (TTY: 1-855-889-4325), where a trained representative will assist you with the appeals process. For detailed steps, please visit the "Learn about the appeals process" website. Let me know if you need further assistance! 😊

Q: "What is the claim status for C1003, and how do I appeal if it was denied?"
A: "Claim **C1003** is marked as **Denied** in our structured database.  
Denied claims are handled by our Marketplace Call Center, which is reachable at 1-800-318-2596 (TTY: 1-855-889-4325). A trained representative will happily assist you with the appeals process. For more detailed steps, please visit the "Learn about the appeals process" section of our website. Let me know if there's anything else I can help with!
**Note:** Please note this is not specialized medical advice. Always consult your insurer for plan-specific procedures."

- **accuracy**: 5
- **tone**: 5
- **conciseness**: 4
- **compliance**: 5

## Overall Result

Overall, the results are strong but the few-shot prompting seems to be hurting more than it helps. Rather than taking the examples as actual examples, it just copies the exact language when it's applicable. I will remove the few-shot prompting and keep the prompt as-is because I think its strong but also short so it won't ignore instructions.

### Final Chosen Prompt

Answer polietly and succinctly using ONLY the context below. Before compiling your answer, check the plan type, section, and language to validate that the context supports an actual answer. If the answer isn't in the context, say you don't know and suggest the member contact support. Do not give medical advice.

**Context:** {context}

**Question:** {question}