# MCP Integration

Today we integrated our MCP tools into our native LLM agentic setup by changing `multi_agent.py` to instruct the agents to the async tools that we developed in `langchain_agent.py` by connecting it to our MCP server directly.

## Error Stress Test

We changed the check_coverage function to yield an error which resulted in the following logs:

```{powershell}
INFO:     Started server process [22952]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
HISTORY TOKENS | session=1 | before=1248
SUMMARIZATION | triggered=False
HISTORY TOKENS | session=1 | before=1248
SUMMARIZATION | triggered=False
HISTORY TOKENS | session=1 | before=1248
SUMMARIZATION | triggered=False
STRUCTURE: both
Retrieval error (attempt 1/2): unhandled errors in a TaskGroup (1 sub-exception)
STRUCTURE: both
Retrieval error (attempt 2/2): unhandled errors in a TaskGroup (1 sub-exception)
ROUTE: coverage
POST /chat | status=200 | time=8476.88 ms
INFO:     127.0.0.1:64993 - "POST /chat HTTP/1.1" 200 OK
Local chatbot — type 'quit' to exit
The coverage details for maternity care on the Bronze HMO plan are not available in the provided context. For specific information, contact your insurance provider or member support directly.
```

This is good, it indicates that the fallback was handled and a response still yielded despite an internal tool failure :).

## Correct Outcome

HISTORY TOKENS | session=1 | before=1708
SUMMARIZATION | triggered=False
HISTORY TOKENS | session=1 | before=1708
SUMMARIZATION | triggered=False
HISTORY TOKENS | session=1 | before=1708
SUMMARIZATION | triggered=False
STRUCTURE: both
MCP TOOLS: ['check_coverage', 'get_claim_status']


> Entering new AgentExecutor chain...

Invoking: `get_claim_status` with `{'claim_id': 'C1003'}`


[{'type': 'text', 'text': '{\n  "claim_id": "C1003",\n  "status": "Denied"\n}', 'id': 'lc_7be5e2ed-a45f-4708-bebf-87ed8f4dc3ee'}]The claim status for **C1003** is **Denied**.

> Finished chain.
[(ToolAgentAction(tool='get_claim_status', tool_input={'claim_id': 'C1003'}, log="\nInvoking: `get_claim_status` with `{'claim_id': 'C1003'}`\n\n\n", message_log=[AIMessageChunk(content='', additional_kwargs={}, response_metadata={'model': 'qwen3:8b', 'created_at': '2026-08-11T02:26:08.0106718Z', 'done': True, 'done_reason': 'stop', 'total_duration': 5279171400, 'load_duration': 111316900, 'prompt_eval_count': 736, 'prompt_eval_duration': 410688000, 'eval_count': 189, 'eval_duration': 4721850000, 'logprobs': None, 'model_name': 'qwen3:8b', 'model_provider': 'ollama'}, id='lc_run--019feea4-2556-7651-9764-ae37e0c1efce', tool_calls=[{'name': 'get_claim_status', 'args': {'claim_id': 'C1003'}, 'id': '35cfd227-433b-4606-a458-449690cd972f', 'type': 'tool_call'}], invalid_tool_calls=[], usage_metadata={'input_tokens': 736, 'output_tokens': 189, 'total_tokens': 925}, tool_call_chunks=[{'name': 'get_claim_status', 'args': '{"claim_id": "C1003"}', 'id': '35cfd227-433b-4606-a458-449690cd972f', 'index': None, 'type': 'tool_call_chunk'}], chunk_position='last')], tool_call_id='35cfd227-433b-4606-a458-449690cd972f'), [{'type': 'text', 'text': '{\n  "claim_id": "C1003",\n  "status": "Denied"\n}', 'id': 'lc_7be5e2ed-a45f-4708-bebf-87ed8f4dc3ee'}])]
CHUNK IDS: ['claims_process-chunk-7', 'benefits-chunk-5', 'claims_process-chunk-8', 'claims_process-chunk-6', 'benefits-chunk-13']
ROUTE: claims
POST /chat | status=200 | time=16623.81 ms
INFO:     127.0.0.1:51402 - "POST /chat HTTP/1.1" 200 OK
Local chatbot — type 'quit' to exit
The claim status for **C1003** is **Denied**.