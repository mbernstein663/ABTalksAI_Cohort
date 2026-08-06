# Streaming LLM Response

Today, day 18, we will be setting up streaming for LLM responses. This means that when we start chatting with our LLM app, instead of pasting all the response text at once- it will paste a character-by-character chunkwise stream of text like ChatGPT.

## Server Events

**SSE: Server Sent Events** and websockets are technologies that keep a persistent connection between a web browser and a server. SEEs are one-way data flows from server to client over HTTP. WebSockets provide two-way, full-duplex communication over a dedicated protocol.

## Timeout/Error Results

I temporarily set a 15 second wait time with a 10 second timeout and the system correctly responded with:

"The response timed out. Please try again."

The streamlit frontend uses a try and except format, so an error will come up if there is an issue on the backend- thus we will avoid testing for now.
