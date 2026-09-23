import os
import json

from dotenv import load_dotenv
from openai import OpenAI

from app.ai.tool_registry import get_tool


load_dotenv()


NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")

if not NVIDIA_API_KEY:
    raise ValueError(
        "NVIDIA_API_KEY .env dosyasinda bulunamadi."
    )


client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",  # Ollama gercek bir key kontrol etmiyor, herhangi bir string olur
    timeout=60.0,
    max_retries=0
)


MODEL = "qwen2.5:3b-instruct-q4_K_M"


# ============================================================
# TOOL EXECUTION
# ============================================================

def execute_tool(tool_name, arguments):

    tool = get_tool(tool_name)

    if tool is None:
        raise ValueError(
            f"Tool bulunamadi: {tool_name}"
        )

    return tool(**arguments)


# ============================================================
# CHAT
# ============================================================

def chat(message):

    tools = [

        {
            "type": "function",
            "function": {
                "name": "financial_summary",
                "description": (
                    "Toplam gelir, toplam gider ve net sonucu getirir."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "additionalProperties": False
                }
            }
        },

        {
            "type": "function",
            "function": {
                "name": "invoice_count",
                "description": (
                    "Toplam fatura sayisini getirir."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "additionalProperties": False
                }
            }
        },

        {
            "type": "function",
            "function": {
                "name": "top_expense_categories",
                "description": (
                    "En yuksek gider kategorilerini getirir."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "limit": {
                            "type": "integer",
                            "description": "Kategori sayisi. 1-10."
                        }
                    },
                    "required": ["limit"],
                    "additionalProperties": False
                }
            }
        },

        {
            "type": "function",
            "function": {
                "name": "recent_transactions",
                "description": (
                    "Son finansal islemleri getirir."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "limit": {
                            "type": "integer",
                            "description": "Islem sayisi. 1-20."
                        }
                    },
                    "required": ["limit"],
                    "additionalProperties": False
                }
            }
        },

        {
            "type": "function",
            "function": {
                "name": "all_transactions",
                "description": (
                    "Tum finansal islemleri getirir."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "additionalProperties": False
                }
            }
        },

        {
            "type": "function",
            "function": {
                "name": "expense_category_percentage",
                "description": (
                    "Belirli bir gider kategorisinin "
                    "toplam giderler icindeki yuzdesini hesaplar."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "category_name": {
                            "type": "string",
                            "description": (
                                "Gider kategorisinin adi."
                            )
                        }
                    },
                    "required": ["category_name"],
                    "additionalProperties": False
                }
            }
        },

        {
            "type": "function",
            "function": {
                "name": "monthly_summary",
                "description": (
                    "Belirtilen ay icin toplam gelir, "
                    "gider ve net sonucu getirir."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "year": {
                            "type": "integer"
                        },
                        "month": {
                            "type": "integer"
                        }
                    },
                    "required": ["year", "month"],
                    "additionalProperties": False
                }
            }
        },

        {
            "type": "function",
            "function": {
                "name": "expense_by_category",
                "description": (
                    "Tum giderleri kategori bazinda "
                    "toplayarak getirir."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "additionalProperties": False
                }
            }
        },

        {
            "type": "function",
            "function": {
                "name": "income_by_category",
                "description": (
                    "Tum gelirleri kategori bazinda "
                    "toplayarak getirir."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "additionalProperties": False
                }
            }
        },

        {
            "type": "function",
            "function": {
                "name": "expense_growth",
                "description": (
                    "Belirtilen ayin giderini "
                    "bir onceki ayla karsilastirir."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "year": {
                            "type": "integer"
                        },
                        "month": {
                            "type": "integer"
                        }
                    },
                    "required": ["year", "month"],
                    "additionalProperties": False
                }
            }
        },

        {
            "type": "function",
            "function": {
                "name": "profit_margin",
                "description": (
                    "Toplam gelir ve net sonuc kullanilarak "
                    "kar marjini hesaplar."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "additionalProperties": False
                }
            }
        },

        {
            "type": "function",
            "function": {
                "name": "income_expense_ratio",
                "description": (
                    "Toplam gelirin toplam gidere oranini hesaplar."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "additionalProperties": False
                }
            }
        }
    ]


    # ========================================================
    # SYSTEM MESSAGE
    # ========================================================

    messages = [
        {
            "role": "system",
            "content": (
                "Sen Karnex AI finansal asistanisin. "

                "Finansal sorulari cevaplarken "
                "veritabani araclarini kullan. "

                "Veritabani verilerini kullan ve veri uydurma. "

                "Kullanici belirli bir gider kategorisinin "
                "toplam gider icindeki yuzdesini sorarsa "
                "expense_category_percentage kullan. "

                "Kullanici kategori bazli gider dagilimi "
                "sorarsa expense_by_category kullan. "

                "Kullanici kategori bazli gelir dagilimi "
                "sorarsa income_by_category kullan. "

                "Kullanici aylik finansal ozet sorarsa "
                "monthly_summary kullan. "

                "Kullanici giderlerin aylik degisimini "
                "sorarsa expense_growth kullan. "

                "Kullanici kar marjini sorarsa "
                "profit_margin kullan. "

                "Kullanici gelir/gider oranini sorarsa "
                "income_expense_ratio kullan. "

                "Gereksiz tool cagrisi yapma. "
                "Ayni tool'u ayni parametrelerle tekrar cagirma. "
                "Ancak farkli parametrelerle (farkli ay, farkli "
                "kategori vb.) birden fazla tool cagrisi gerekiyorsa "
                "bunu yap. "

                "Tool sonucundaki veriler disinda "
                "finansal rakam uydurma. "

                "Sonucu Turkce, acik ve kisa ver."
            )
        },
        {
            "role": "user",
            "content": message
        }
    ]


    # ========================================================
    # FIRST LLM CALL
    # ========================================================


    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=tools,
        tool_choice="auto",
        temperature=0.2,
        max_tokens=300,
        extra_body={
            "chat_template_kwargs": {
                "enable_thinking": False
            }
        }
    )


    assistant_message = response.choices[0].message


    # ========================================================
    # NO TOOL
    # ========================================================

    if not assistant_message.tool_calls:

        if assistant_message.content:
            return assistant_message.content

        return "Model herhangi bir cevap uretemedi."


    # ========================================================
    # TOOL CALLS
    # ========================================================

    messages.append(assistant_message)

    executed_tools = set()

    for tool_call in assistant_message.tool_calls:

        tool_name = tool_call.function.name
        raw_arguments = tool_call.function.arguments or "{}"

        dedup_key = (tool_name, raw_arguments)

        if dedup_key in executed_tools:
            continue

        executed_tools.add(dedup_key)


        try:
            arguments = json.loads(raw_arguments)

        except json.JSONDecodeError:

            arguments = {}


        # ====================================================
        # LIMIT CONTROLS
        # ====================================================

        if tool_name == "top_expense_categories":

            try:
                limit = int(
                    arguments.get("limit", 5)
                )

            except (TypeError, ValueError):

                limit = 5

            arguments["limit"] = max(
                1,
                min(limit, 10)
            )


        elif tool_name == "recent_transactions":

            try:
                limit = int(
                    arguments.get("limit", 5)
                )

            except (TypeError, ValueError):

                limit = 5

            arguments["limit"] = max(
                1,
                min(limit, 20)
            )


        # ====================================================
        # EXECUTE TOOL
        # ====================================================

        try:
            tool_result = execute_tool(
                tool_name,
                arguments
            )

        except Exception as exc:
            tool_result = {
                "error": str(exc)
            }

        # ====================================================
        # TOOL RESULT
        # ====================================================

        messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(
                    tool_result,
                    ensure_ascii=False,
                    default=str
                )
            }
        )


    # ========================================================
    # FINAL LLM CALL
    # ========================================================

    final_response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.2,
        max_tokens=700,
        extra_body={
            "chat_template_kwargs": {
                "enable_thinking": False
            }
        }
    )


    final_content = final_response.choices[0].message.content


    if not final_content:

        return (
            "Veriler alindi ancak anlamli "
            "bir cevap olusturulamadi."
        )


    return final_content