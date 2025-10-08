from config import API_KEY
import math
import requests
import json
import time
from pathlib import Path
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.tools import tool
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.callbacks import BaseCallbackHandler


@tool
def calculator(expr:str)->str:
    """Tool that calculates mathematical expressions"""
    allowed_functs={k:v for k, v in math.__dict__.items() if not k.startswith("__") }

    try:

        result= eval(expr, {"__builtins__":{}}, allowed_functs)
        return result

    except Exception as e:
        return f"Hesablama xətası: {e}"



    
@tool
def forecaster(city:str)-> str:
    """Tool that returns weather forecast of given city"""
    try:
        url=f"https://wttr.in/{city}?format=3"
        response=requests.get(url)
        return response.text
    
    except Exception as e:
        return f"Hava proqnozu tapılmadı {e}"
    
llm=ChatOpenAI(api_key=API_KEY, model="gpt-4o-mini", temperature=0.1)

prompt=ChatPromptTemplate.from_messages([
    ("system","You are chatbot in Azerbaijani."
    "If question request mathematical calculation, then use 'calculator'-tool. "
    "If question ask about weather forecast, then use 'forecaster'-tool."
    "Digər hallarda öz biliyinə əsasən cavab ver." ),
    ("human","{input}"),
    ("placeholder","{agent_scratchpad}")
])

class ToolLogger(BaseCallbackHandler):
    def __init__(self, filename: str = "tool_usage.log"):
        base_dir = Path(__file__).resolve().parent   
        self.path = str(base_dir / filename)

    def _w(self, obj):
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(obj, ensure_ascii=False) + "\n")

    def on_tool_start(self, serialized, input_str, **kwargs):
        self._w({"event":"tool_start","tool":serialized.get("name"),
                 "input":input_str,"t":time.strftime("%F %T")})

    def on_tool_end(self, output, **kwargs):
        self._w({"event":"tool_end","output":str(output)[:300],
                 "t":time.strftime("%F %T")})

tools=[calculator, forecaster]
loggers=[ToolLogger()]
agent=create_tool_calling_agent(llm,tools,prompt)
agent_exe=AgentExecutor(agent=agent, tools=tools,verbose=False, callbacks=loggers)


if __name__=="__main__":
    print("Zəhmət olmasa, sualınızı qeyd edin(çıxış üçün q düyməsini klikləyin)")
    while True:
        ask=input("Sualınız: ").strip()
        if ask.lower()=="q":
            print("Görüşənədək!!")
            break
        answer=agent_exe.invoke({"input":ask},config={"callbacks":loggers})
        print("Bot Cavab: ",answer["output"])


