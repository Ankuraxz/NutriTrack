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
from settings.utils import json_cleaner, clean_grocery_list

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()
Config = Config()
client = Config.get_mongo_client()
chat_llm = Config.get_openai_chat_connection()

@router.get("/generate_grocery_list/{email}", tags=["grocery"])
def generate_grocery_list(email_id: str):
    """
    Generate grocery list based on user's preferences
    :param email_id:
    :return:
    """
    try:
        user_data = get_user_data_from_mongo(email_id)
        if user_data is None or user_data == {}:
            raise HTTPException(status_code=404, detail="User data not found in mongo db")
        budget = user_data['budget']
        grocery_frequency = user_data['grocery_frequency']
        dietary_restrictions = user_data['dietary_restrictions']
        allergies = user_data['allergies']
        diet_type = user_data['diet_type']

        meal = load_meal_from_mongo(email_id)
        if meal is None or meal == {}:
            raise HTTPException(status_code=404, detail="Meal not found in user's profile")

        template = """
        You are an AI powered Grocery list generator, you will be provided with a user's meal list {meal} and user information including budget {budget}, dietary restrictions {dietary_restrictions}, allergies {allergies}, diet type {diet_type}.
        TASK: You need to generate grocery list for 1 grocery frequency {grocery_frequency} along with amount needed for the user based on their meal list and user information and provide the information as comma seperated string
        Example Response: "eggs 1 tray, bread 2 pack, milk 3 litre, chicken 1kg, rice 1kg, pasta, fruits, vegetables, cheese, butter, oil, sugar, salt, spices, herbs, nuts, seeds, flour, grains, legumes, beverages 2 pack, snacks 1 pack, condiments 3 pack, sauces 1 bottle, canned goods 1 can, frozen foods, dairy 1 litre, bakery, deli, meat 1 kg, seafood 1 kg"
        RESPONSE CONSTRAINT: DO NOT OUTPUT EXTRA CHARACTERS, JUST OUTPUT RESPONSE TO THE CUSTOMER IN PROPER STRING WITH QUANTITY. """

        prompt = PromptTemplate.from_template(template)
        chain = LLMChain(llm=chat_llm, prompt=prompt)
        response_raw = chain.run(meal=meal, budget=budget, dietary_restrictions=dietary_restrictions, allergies=allergies,
                                    diet_type=diet_type, grocery_frequency=grocery_frequency)
        response = json_cleaner(response_raw.strip())
        grocery = {"grocery_list": response}
        save_grocery_list_to_mongo(email_id, grocery)
        return {"response": response}

    except Exception as e:
        logger.error(f"Error in grocery list generator: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error in grocery list generator: {str(e)}")



@router.get("/show_grocery_list/{email}", tags=["grocery"])
def show_grocery_list(email_id):
    """
    Show grocery list from user's profile
    :param email_id:
    :return:
    """
    try:
        grocery_list = load_grocery_list_from_mongo(email_id)
        if grocery_list is None:
            raise HTTPException(status_code=404, detail="Grocery list not found in user's profile")
        return clean_grocery_list(grocery_list)

    except Exception as e:
        logger.error(f"Error in showing grocery list: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error in showing grocery list: {str(e)}")

