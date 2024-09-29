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
@router.get("/generate_meal/{email}", tags=["meal"])
def meal_generator(email_id):
    """
    Generate meals based on user's preferences
    :param email_id:
    :return:
    """
    try:
        user_data = get_user_data_from_mongo(email_id)
        if user_data is None or user_data == {}:
            raise HTTPException(status_code=404, detail="User data not found in mongo db")
        template = """You are an AI powered Meal generator, you will be provided with a user profile  {user_data} 
        containing information of "name", "age", "gender", //male, female, other "height", //in feet "weight", 
        //in lbs "activity_level", //sedentary, light, moderate, active, very_active "exercise_hours", //in hours 
        "job_type", //student, working "work_type", //office, field, home, None "work_hours", "cooking_hours", 
        //time dedicated to cooking "proficiency_in_cooking", //low, medium, high "goals", //healthy, weight_loss, 
        muscle_gain "dietary_restrictions": null, //None, vegetarian, vegan, gluten_free, dairy_free, 
        nut_free "diet_type", //balanced, keto, paleo, vegan, vegetarian "allergies", //None, peanuts, shellfish, 
        soy, dairy, eggs, gluten "cuisine_preference", //american, italian, mexican, chinese, indian, thai, 
        japanese "budget", //0-100 dollars for weekly groceries "grocery_frequency":, //weekly, bi-weekly, monthly and most importantly daily calorie intake goal

        TASK: You need to generate easy to cook at home meals for entire week, 3 meals per day as breakfast, lunch dinner based on user's preferences keeping in mind cooking hours & cooking proficiency and budget and dietary restrictions and allergy and nutritional goals and provide the information as json 
        Example Response: ['day1':['breakfast':"eggs 19 calorie", 'lunch':"chicken salad 24 calorie", 'dinner':"pasta 34 calorie"], 'day2':['breakfast':"oatmeal", 'lunch':"chicken sandwich", 'dinner':"rice"], 'day3':['breakfast':"pancakes", 'lunch':"chicken soup", 'dinner':"pasta"], 'day4':['breakfast':"eggs", 'lunch':"chicken salad", 'dinner':"pasta"], 'day5':['breakfast':"oatmeal", 'lunch':"chicken sandwich", 'dinner':"rice"], 'day6':['breakfast':"pancakes", 'lunch':"chicken soup", 'dinner':"pasta"], 'day7':['breakfast':"eggs", 'lunch':"chicken salad", 'dinner':"pasta"]]
        REMEMBER: day, breakfast, lunch, dinner are the keys and the values are the meals for the day along with their calorie count per serving
        RESPONSE CONSTRAINT: DO NOT OUTPUT EXTRA CHARACTERS, JUST OUTPUT RESPONSE TO THE CUSTOMER IN PROPER JSON.
        """

        prompt = PromptTemplate.from_template(template)
        chain = LLMChain(llm=chat_llm, prompt=prompt)
        response_raw = chain.run(user_data=user_data)
        response = json_cleaner(response_raw.strip())
        save_meal_to_mongo(email_id, response)
        return {"response": response}

    except Exception as e:
        logger.error(f"Error in meal generator: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error in meal generator: {str(e)}")




@router.get("/show_meal/{email}", tags=["meal"])
def show_meal(email_id):
    """
    Show meal from user's profile
    :param email_id:
    :return:
    """
    try:
        meal = load_meal_from_mongo(email_id)
        if meal is None:
            raise HTTPException(status_code=404, detail="Meal not found in user's profile")
        return meal

    except Exception as e:
        logger.error(f"Error in showing meal: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error in showing meal: {str(e)}")

