import json
import logging
from typing import Union, Annotated
from fastapi import APIRouter, status
from fastapi import Form, Header
from starlette.responses import JSONResponse
from settings.config import Config
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()
Config = Config()
client = Config.get_mongo_client()

db = client["nutrition_ai"]
collection = db["nutrition_app_user"]


def save_recommendation_to_mongo(email: str, recommendation: str) -> None:
    try:
        collection_recommendation = db['nutrition_recommendation_data']
        if email in collection_recommendation.distinct("email_id"):
            collection_recommendation.update_one({"email_id": email}, {"$set": {"recommendation": recommendation}})
        collection_recommendation.insert_one({"email_id": email, "recommendation": recommendation})
        return None
    except Exception as e:
        logger.error(f"Error in writing recommendation data to mongo db: {str(e)}")
        return None


def save_chat_to_mongo(email: str, history: str) -> None:
    try:
        collection_chat = db['chat_data']
        if email in collection_chat.distinct("email_id"):
            collection_chat.update_one({"email_id": email}, {"$set": {"history": history}})
        collection_chat.insert_one({"email_id": email, "history": history})
        return None
    except Exception as e:
        logger.error(f"Error in writing chat data to mongo db: {str(e)}")
        return None


def save_meal_to_mongo(email: str, meal: dict) -> None:
    try:
        collection_meal = db['meal_data']
        if email in collection_meal.distinct("email_id"):
            collection_meal.update_one({"email_id": email}, {"$set": {"meal": meal}})
        collection_meal.insert_one({"email_id": email, "meal": meal})
        return None
    except Exception as e:
        logger.error(f"Error in writing meal data to mongo db: {str(e)}")
        return None


def load_meal_from_mongo(email: str) -> dict:
    try:
        collection_meal = db['meal_data']
        if email in collection_meal.distinct("email_id"):
            data = collection_meal.find_one({"email_id": email}, {"_id": 0})
            return data['meal']
        else:
            return {}
    except Exception as e:
        logger.error(f"Error in reading meal data from mongo db: {str(e)}")
        return {}


def save_grocery_list_to_mongo(email: str, grocery_list: dict) -> None:
    try:
        collection_grocery = db['grocery_data']
        if email in collection_grocery.distinct("email_id"):
            collection_grocery.update_one({"email_id": email}, {"$set": {"grocery_list": grocery_list}})
        collection_grocery.insert_one({"email_id": email, "grocery_list": grocery_list})
        return None
    except Exception as e:
        logger.error(f"Error in writing grocery list data to mongo db: {str(e)}")
        return None


def load_grocery_list_from_mongo(email: str) -> dict:
    try:
        collection_grocery = db['grocery_data']
        if email in collection_grocery.distinct("email_id"):
            data = collection_grocery.find_one({"email_id": email}, {"_id": 0})
            return data['grocery_list']
        else:
            return {}
    except Exception as e:
        logger.error(f"Error in reading grocery list data from mongo db: {str(e)}")
        return {}


def get_user_data_from_mongo(email: str) -> dict:
    try:
        if email in collection.distinct("email_id"):
            data = collection.find_one({"email_id": email}, {"_id": 0})
            return json.loads(data['data'])
        else:
            return {}
    except Exception as e:
        logger.error(f"Error in reading data from mongo db: {str(e)}")
        return {}


def verify_data(data: str) -> bool:
    """
    Verify presence of fields in data and its type
    Sample data
        {
      "name": "John Doe",
      "age": 25,
      "gender": "male", //male, female, other
      "height": 5.8, //in feet
      "weight": 150, //in lbs
      "activity_level": "moderate", //sedentary, light, moderate, active, very_active
      "exercise_hours": 3, //in hours
      "job_type": "student", //student, working
      "work_type": "office", //office, field, home, None
      "work_hours": 40,
      "cooking_hours": 5,
      "proficiency_in_cooking": "medium", //low, medium, high
      "goals": "healthy", //healthy, weight_loss, muscle_gain
      "dietary_restrictions": null, //None, vegetarian, vegan, gluten_free, dairy_free, nut_free
      "diet_type": "balanced", //balanced, keto, paleo, vegan, vegetarian
      "allergies": null, //None, peanuts, shellfish, soy, dairy, eggs, gluten
      "cuisine_preference": "indian", //american, italian, mexican, chinese, indian, thai, japanese
      "budget": 100, //0-100 dollars for weekly groceries
      "grocery_frequency": "weekly", //weekly, bi-weekly, monthly
      "calorie_goal": 2000
    }
    :param data:
    :return: bool
    """
    try:
        data = json.loads(data)
        if "name" in data and "age" in data and "gender" in data and "height" in data and "weight" in data and "activity_level" in data and "exercise_hours" in data and "job_type" in data and "work_type" in data and "work_hours" in data and "cooking_hours" in data and "proficiency_in_cooking" in data and "goals" in data and "dietary_restrictions" in data and "diet_type" in data and "allergies" in data and "cuisine_preference" in data and "budget" in data and "grocery_frequency" in data and "calorie_goal" in data:
            return True
        else:
            return False
    except Exception as e:
        logger.error(f"Error in verifying data: {str(e)}")
        return False


@router.post("/write_user_info_to_mongo", tags=["mongo_db"])
async def write_user_info_to_mongo(email_id: Annotated[Union[str, None], Header()],
                                   data: str = Form(...)) -> JSONResponse:
    """
       Writes data to mongo db
       data =
    Sample data in str
        {
      "name": "John Doe",
      "age": 25,
      "gender": "male", //male, female, other
      "height": 5.8, //in feet
      "weight": 150, //in lbs
      "activity_level": "moderate", //sedentary, light, moderate, active, very_active
      "exercise_hours": 3, //in hours
      "job_type": "student", //student, working
      "work_type": "office", //office, field, home, None
      "work_hours": 40,
      "cooking_hours": 5,
      "proficiency_in_cooking": "medium", //low, medium, high
      "goals": "healthy", //healthy, weight_loss, muscle_gain
      "dietary_restrictions": null, //None, vegetarian, vegan, gluten_free, dairy_free, nut_free
      "diet_type": "balanced", //balanced, keto, paleo, vegan, vegetarian
      "allergies": null, //None, peanuts, shellfish, soy, dairy, eggs, gluten
      "cuisine_preference": "indian", //american, italian, mexican, chinese, indian, thai, japanese
      "budget": 100, //0-100 dollars for weekly groceries
      "grocery_frequency": "weekly", //weekly, bi-weekly, monthly
      "calorie_goal": 2000
      }

       :param email_id:
       :param data:
       :return:
    """
    if verify_data(data):

        try:
            logger.info(f"Data received for writing to mongo db")
            if email_id in collection.distinct("email_id"):
                collection.update_one({"email_id": email_id}, {"$set": {"data": data}})
            else:
                collection.insert_one({"email_id": email_id, "data": data})
            return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Data written to mongo db"})
        except Exception as e:
            logger.error(f"Error in writing data to mongo db: {str(e)}")
            return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                content={"message": "Internal server error"})
    else:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"message": "Invalid data"})


@router.get("/read_user_info_from_mongo/{email}", tags=["mongo_db"])
async def read_user_info_from_mongo(email_id: str) -> JSONResponse:
    """
    Reads data from mongo db
    :param email_id:
    :return:
    """
    try:
        logger.info(f"Data received for reading from mongo db")
        if email_id in collection.distinct("email_id"):
            data = collection.find_one({"email_id": email_id}, {"_id": 0})
            return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Data fetched from mongo db",
                                                                         "data": data})
        else:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "No data found in mongo db"})
    except Exception as e:
        logger.error(f"Error in reading data from mongo db: {str(e)}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"message": "Internal server error"})


@router.get("/get_all_chats/{email_id}", tags=["mongo_db"])
async def get_all_chats(email_id: str) -> JSONResponse:
    """
    Reads data from mongo db
    :param email_id:
    :return:
    """
    try:
        logger.info(f"Data received for reading from mongo db")
        collection_chat = db['chat_data']
        if email_id in collection_chat.distinct("email_id"):
            data = collection_chat.find({"email_id": email_id}, {"_id": 0})
            return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Data fetched from mongo db",
                                                                         "data": data})
        else:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "No data found in mongo db"})
    except Exception as e:
        logger.error(f"Error in reading data from mongo db: {str(e)}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"message": "Internal server error"})


@router.delete("/delete_user_info_from_mongo/{email_id}", tags=["mongo_db"])
async def delete_user_info_from_mongo(email_id: str) -> JSONResponse:
    """
    Deletes data from mongo db
    :param email_id:
    :return:
    """
    try:
        logger.info(f"Data received for deleting from mongo db")
        if email_id in collection.distinct("email_id"):
            collection.delete_many({"email_id": email_id})
            return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Data deleted from mongo db"})
        else:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "No data found in mongo db"})
    except Exception as e:
        logger.error(f"Error in deleting data from mongo db: {str(e)}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"message": "Internal server error"})


@router.get("/get_old_recommendation/{email_id}", tags=["mongo_db"])
def get_old_recommendation_from_mongo(email_id: str) -> dict:
    try:
        collection_recommendation = db['nutrition_recommendation_data']
        if email_id in collection_recommendation.distinct("email_id"):
            data = collection_recommendation.find_one({"email_id": email_id}, {"_id": 0})
            return json.loads(data['recommendation'])
        else:
            return {}
    except Exception as e:
        logger.error(f"Error in reading recommendation data from mongo db: {str(e)}")
        return {}


