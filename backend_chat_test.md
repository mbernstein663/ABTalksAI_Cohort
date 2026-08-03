# Original API Setup

We have our working uvicorn server set up with successful "health," "chat," and "history" operations (GET, POST, GET, respectively.). Here are the results logs, everything seems to check out okay and be working well:

## Chat Test

**Successful Responses**:

Q: "What is the monthly premium for Gold PPO?"
A: The monthly premium for Gold PPO is $500.

Q: "What is the claim status for C1003, and how do I appeal if it was denied??"
A: The claim status for C1003 is **Denied**. If you need to appeal, contact your insurance providerâs support team for specific steps, as the appeal process details are not included in the provided context.

Q: "Is maternity care covered on the Bronze HMO plan?"
A: The context does not specify whether maternity care is covered under the Bronze HMO plan. For detailed coverage information, please contact support.

```{Powershell}
PS C:\Users\micro> $body = @{
>>     session_id = 1
>>     member_id  = 101
>>     message    = "What is the monthly premium for Gold PPO?"
>> } | ConvertTo-Json
PS C:\Users\micro> Invoke-RestMethod `
>>     -Uri "http://127.0.0.1:8000/chat" `
>>     -Method Post `
>>     -ContentType "application/json" `
>>     -Body $body


session_id : 1
member_id  : 101
answer     : The monthly premium for Gold PPO is $500.
structure  : structured
history    : {@{role=user; message=What is the monthly premium for Gold PPO?}, @{role=assistant; message=The monthly premium for Gold PPO is $500.}}



PS C:\Users\micro> # if curling gives 422:
PS C:\Users\micro>
PS C:\Users\micro> $body = @{
>>     session_id = 1
>>     member_id  = 101
>>     message    = "What is the claim status for C1003, and how do I appeal if it was denied??"
>> } | ConvertTo-Json
PS C:\Users\micro>
PS C:\Users\micro> Invoke-RestMethod `
>>     -Uri "http://127.0.0.1:8000/chat" `
>>     -Method Post `
>>     -ContentType "application/json" `
>>     -Body $body


session_id : 1
member_id  : 101
answer     : The claim status for C1003 is **Denied**. If you need to appeal, contact your insurance providerâs support team for specific steps, as the appeal process details are not included in the
             provided context.
structure  : both
history    : {@{role=user; message=What is the monthly premium for Gold PPO?}, @{role=assistant; message=The monthly premium for Gold PPO is $500.}, @{role=user; message=What is the claim status for C1003,
             and how do I appeal if it was denied??}, @{role=assistant; message=The claim status for C1003 is **Denied**. If you need to appeal, contact your insurance providerâs support team for specific
             steps, as the appeal process details are not included in the provided context.}}



PS C:\Users\micro> # if curling gives 422:
PS C:\Users\micro>
PS C:\Users\micro> $body = @{
>>     session_id = 1
>>     member_id  = 101
>>     message    = "Is maternity care covered on the Bronze HMO plan?"
>> } | ConvertTo-Json
PS C:\Users\micro>
PS C:\Users\micro> Invoke-RestMethod `
>>     -Uri "http://127.0.0.1:8000/chat" `
>>     -Method Post `
>>     -ContentType "application/json" `
>>     -Body $body


session_id : 1
member_id  : 101
answer     : The context does not specify whether maternity care is covered under the Bronze HMO plan. For detailed coverage information, please contact support.
structure  : unstructured
history    : {@{role=user; message=What is the monthly premium for Gold PPO?}, @{role=assistant; message=The monthly premium for Gold PPO is $500.}, @{role=user; message=What is the claim status for C1003,
             and how do I appeal if it was denied??}, @{role=assistant; message=The claim status for C1003 is **Denied**. If you need to appeal, contact your insurance providerâs support team for specific
             steps, as the appeal process details are not included in the provided context.}...}

```

## History test

```{Powershell}
PS C:\Users\micro> Invoke-RestMethod `
>>     -Uri "http://127.0.0.1:8000/history/1" `
>>     -Method Get |
>>     ConvertTo-Json -Depth 10
{
    "session_id":  1,
    "member_id":  101,
    "history":  [
                    {
                        "role":  "user",
                        "message":  "What is the monthly premium for Gold PPO?"
                    },
                    {
                        "role":  "assistant",
                        "message":  "The monthly premium for Gold PPO is $500."
                    },
                    {
                        "role":  "user",
                        "message":  "What is the claim status for C1003, and how do I appeal if it was denied??"
                    },
                    {
                        "role":  "assistant",
                        "message":  "The claim status for C1003 is **Denied**. If you need to appeal, contact your insurance providerâs support team for specific steps, as the appeal process details are not included in the provided context."
                    },
                    {
                        "role":  "user",
                        "message":  "Is maternity care covered on the Bronze HMO plan?"
                    },
                    {
                        "role":  "assistant",
                        "message":  "The context does not specify whether maternity care is covered under the Bronze HMO plan. For detailed coverage information, please contact support."
                    }
                ]
}

```
