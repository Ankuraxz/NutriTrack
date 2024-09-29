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


@router.get("/generate_recommendation/{email}", tags=["recommend"])
def recommendation_generator(email_id):
    """
    Generate recommendations based on user's preferences
    :param email_id:
    :return:
    """
    try:
        user_data = get_user_data_from_mongo(email_id)
        if user_data is None or user_data == {}:
            raise HTTPException(status_code=404, detail="User data not found in mongo db")
        template = """You are an AI powered Recommendation generator, you will be provided with a user profile  {user_data} 
        containing key information around weight, height, calorie count, body goals, diet goals etc. Generate Recommeneded activities, food, lifestyle changes, etc. based on the user's profile.
        Output these in plaintext short paragraph . Comment on Key exercises, Protien COntent per weight, Calorie Intake, lifestyle changes, must eat suplements and more.
        """

        prompt = PromptTemplate.from_template(template)
        chain = LLMChain(llm=chat_llm, prompt=prompt)
        response_raw = chain.run(user_data=user_data)
        response = json_cleaner(response_raw.strip())
        save_recommendation_to_mongo(email_id, response)
        return {"response": response}

    except Exception as e:
        logger.error(f"Error in recommendation generator: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error in recommendation generator: {str(e)}")
