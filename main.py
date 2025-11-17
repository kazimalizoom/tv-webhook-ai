from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, Dict
from openai import OpenAI
import os

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class TvPayload(BaseModel):
    symbol: str
    timeframe: Optional[str] = None
    price: Optional[float] = None
    extra: Optional[Dict] = None


@app.post("/tv-webhook")
async def tv_webhook(payload: TvPayload):

    prompt = f"""
    أنت محلل فني محترف.

    البيانات:
    - الرمز: {payload.symbol}
    - الفريم: {payload.timeframe}
    - السعر: {payload.price}
    - إضافات: {payload.extra}

    المطلوب:
    - الاتجاه الحالي
    - هل يوجد دخول BUY/SELL؟
    - SL
    - TP1
    - السبب الفني

    أعد الإجابة بصيغة JSON فقط.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    answer = response.choices[0].message.content

    return {
        "ai_response": answer,
        "raw_payload": payload
    }
