import openai
import json
from src.settings import openai_api_key

client = openai.OpenAI(api_key=openai_api_key)

def process_and_send_translation(query_dict):
    prompt = f"""
Translate EVERY item's "message" to English, regardless of the source language.
Keep "role" unchanged and preserve order and length.
Return ONLY the translated JSON array, no extra text.
Conversation: {json.dumps(query_dict, ensure_ascii=False)}
"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0
    )
 
    translated_json_str = response.choices[0].message.content.strip()
    translated_list = json.loads(translated_json_str) 
   
    return json.dumps(translated_list, ensure_ascii=False, indent=4)




def process_and_mark_answers(query_dict):
    prompt = f"""
    You are a strict evaluator.
    
    For EACH criteria in the provided evaluation data:
    - Assign a mark OUT OF 5.
    - Use only the 'result' and 'rationale' values for marking.
    - Respond ONLY with a JSON array in this format:
    
    [
        {{
            "criteria_id": "...",
            "mark": X
        }},
        ...
    ]
    
    Evaluation Data: {json.dumps(query_dict, ensure_ascii=False)}
    """
   
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0
    )
   
    marks_json_str = response.choices[0].message.content.strip()
    marks_list = json.loads(marks_json_str)
   
    return json.dumps(marks_list, ensure_ascii=False, indent=4)


