A small chatbot that replies in Azerbaijani using LangChain’s tool-calling agent with OpenAI gpt-4o-mini.
It provides two tools: calculator (safe math-only eval) and forecaster (short weather from wttr.in).
The agent selects tools based on the system prompt and returns concise, human-readable answers.
Tool activity is logged via a custom BaseCallbackHandler to tool_usage.log (event,tool name, input, output, timestamps).