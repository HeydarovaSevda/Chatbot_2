## DESIGN  
### Purpose & Scope  
A small Azerbaijani chatbot that can:  
Calculate math expressions (calculator)  
Fetch weather summaries (forecaster)  
Uses LangChain tool-calling agent with OpenAI gpt-4o-mini.  


### Architecture  
LLM: ChatOpenAI(model="gpt-4o-mini", temperature=0.1)  
Agent: create_tool_calling_agent(llm, tools, prompt)  
Executor: AgentExecutor(agent, tools, callbacks=...)  
Tools: Python @tool functions  
Logging: ToolLogger(BaseCallbackHandler) → tool_usage.log  


### Tool Interface & I/O  
@tool  
def calculator(expr: str) -> str:  
    """Calculates a math expression."""  
    ...  

@tool  
def forecaster(city: str) -> str:  
    """Returns short weather for a city (wttr.in ?format=3)."""  
    ...  

**Inputs:** single named arg (expr or city), plain text  
**Outputs:** short string suitable for direct display  


### Tool-Call Decision Logic  
The LLM decides via function-calling guided by the system prompt:  
LLM decides via function-calling using system rules:  
Math/calculation questions → calculator  
Weather questions → forecaster  
Other queries → direct LLM reply (no tool)  


### Safety & Validation  
**calculator**
Evaluates with no builtins: eval(expr, {"__builtins__": {}}, allowed_functs)  
allowed_functs is a whitelist from math  
Errors are caught and returned as user-safe messages  

**forecaster**  
city input; HTTP call wrapped in try/except
Network issues return a concise message: Hava proqnozu tapılmadı...  
Uses wttr.in short-text endpoint: https://wttr.in/{city}?format=3  
No secrets or internal details in outputs/logs  


### Logging & Observability  
ToolLogger(BaseCallbackHandler) records:   
tool_start: event, tool name, input, timestamp   
tool_end: event, output (truncated), timestamp  
Destination: tool_usage.log (same directory as the script)  


### Error Handling  
All tool calls are wrapped in try/except. On error, the chatbot returns a clear, non-technical message (e.g., “Hesablama xətası…”, “Hava proqnozu tapılmadı…”) and continues running.