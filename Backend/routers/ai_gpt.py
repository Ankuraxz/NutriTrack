import logging
import json
import os
import requests
from fastapi import APIRouter, Form, HTTPException, Header
from typing import Optional, Annotated, Union
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from routers.mongo_crud_data import *
from settings.config import Config
from settings.utils import json_cleaner

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()
Config = Config()
client = Config.get_mongo_client()
chat_llm = Config.get_openai_chat_connection()


@router.post("/chat", tags=["chat_ai"])
def chat(email_id: Annotated[Union[str, None], Header], message: str = Form(...), history: list = Form(...)):
    """
    Chat with AI about meals, nutrition and diet
    :param email_id:
    :param message:
    :param history:
    :return:
    """
    if history is None:
        history = []
    try:
        user_data = get_user_data_from_mongo(email_id)
        meal = load_meal_from_mongo(email_id)
        grocery_list = load_grocery_list_from_mongo(email_id)

        if "STOP" in message or "Stop" in message or "stop" in message:
            save_chat_to_mongo(email_id, json.dumps(history))
            return {"response": "STOPPING CHAT ", "history": history, "stop": True}

        template = """You are an AI powered Meal & Grocery Planner. Client will be talking to you about their queries 
        regarding meals, groceries, goals. Here is the history of chat {history}, now the customer is saying {message}. Please respond to the customer in a polite manner. In case there is no history of chat, 
        just respond to the customer's current message. You will be provided with a user profile  {user_data}
        containing information of user's preferences, goals, calorie intake goal , allergies etc.  Following is the meal {meal} and grocery list {grocery_list} for the user

        TASK: User can ask questions about the meal and grocery list  You need to answer queries related to nutritional information details, cooking time, ingredients, recipes, etc, in user preferred language
        ANSWER: You need to answer the queries based on the user's preferences, meal list and grocery list strictly and provide the information in a user friendly manner. 
        SUB_TASK: Address the user like a client needing help and provide the information in a user friendly manner.
        RESPONSE CONSTRAINT: DO NOT OUTPUT HISTORY OF CHAT, JUST OUTPUT RESPONSE TO THE CUSTOMER IN PLAIN TEXT
        """
        prompt = PromptTemplate.from_template(template)
        chain = LLMChain(llm=chat_llm, prompt=prompt)
        response_raw = chain.run( message=message, history= json.dumps(history), user_data=user_data, meal=meal, grocery_list=grocery_list)
        response = json_cleaner(response_raw.strip())

        history.append({"message": message, "response": response})
        save_chat_to_mongo(email_id, json.dumps(history))
        return {"response": response, "history": history, "stop": False}


    except Exception as e:
        logger.error(f"Error in chat: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error in chat: {str(e)}")
