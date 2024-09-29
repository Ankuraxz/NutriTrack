import logging
from typing import Union, Annotated
from fastapi import APIRouter, status, HTTPException
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
collection = db["calorie_data"]


@router.post("/write_calorie_to_mongo", tags=["calorie"])
async def write_calorie_to_mongo(email_id: Annotated[Union[str, None], Header()],
                                 calorie: int = Form(...), food_item: str = Form(...)) -> JSONResponse:
    """
    Writes data to mongo db
    :param email_id:
    :param calorie:
    :param food_item:
    :return:
    """
    try:
        logger.info(f"Data received for writing to mongo db")
        today_date = datetime.now().date()
        collection.insert_one(
            {"email_id": email_id, "calorie": calorie, "food_item": food_item, "date": str(today_date)})
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Data written to mongo db"})
    except Exception as e:
        logger.error(f"Error in writing data to mongo db: {str(e)}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"message": "Internal server error"})


@router.get("/get_total_calorie_by_date/{email_id}/{date}", tags=["calorie"])
async def get_total_calorie_by_date(email_id: str, date: str) -> JSONResponse:
    """
    Reads calorie data from MongoDB for a specific user (email_id) and date.
    :param email_id: The email ID of the user.
    :param date: The date for which to retrieve the calorie data (YYYY-MM-DD).
    :return: Total calorie count for the given date.
    """
    try:
        # The date is already expected to be in the "YYYY-MM-DD" string format
        logger.info(f"Data received for reading from mongo db for email_id: {email_id} and date: {date}")

        # Check if the email_id exists in the database
        if email_id in collection.distinct("email_id"):
            # Query to filter records by email_id and the exact date (which is stored as a string)
            calorie_data = collection.find({"email_id": email_id, "date": date})

            # Calculate the total calorie intake for the specified date
            total_calories = sum([entry.get('calorie', 0) for entry in calorie_data])

            # Return the total calorie count in the response
            return JSONResponse(status_code=200, content={"email_id": email_id, "date": date,
                                                          "total_calories": total_calories})
        else:
            # Handle case where email_id is not found
            return JSONResponse(status_code=404, content={"message": "Email ID not found in database"})
    except Exception as e:
        logger.error(f"Error while fetching calorie data: {e}")
        return JSONResponse(status_code=500, content={"message": "An error occurred while fetching calorie data"})


@router.get("/get_individual_calorie_by_date/{email_id}/{date}", tags=["calorie"])
async def get_individual_calorie_by_date(email_id: str, date: str) -> JSONResponse:
    """
    Reads calorie data from MongoDB for a specific user (email_id) and date.
    :param email_id: The email ID of the user.
    :param date: The date for which to retrieve the calorie data (YYYY-MM-DD).
    :return: Individual calorie count for the given date.
    """
    try:
        logger.info(f"Fetching calorie data for email_id: {email_id} and date: {date}")

        if email_id not in collection.distinct("email_id"):
            raise HTTPException(status_code=404, detail="Email ID not found in the database")

        # Query to filter records by email_id and the exact date
        calorie_data = collection.find(
            {"email_id": email_id, "date": date},
            {"_id": 0}
        )
        if calorie_data:
            # Return the individual calorie data for the specified date
            return JSONResponse(status_code=200, content={"email_id": email_id, "date": date, "calorie_data": list(calorie_data)})
        else:
            raise HTTPException(status_code=404, detail="No calorie data found for the specified date")
    except HTTPException as http_err:
        logger.warning(f"HTTP error occurred: {http_err.detail}")
        raise http_err

    except Exception as e:
        logger.error(f"Error while fetching calorie data: {e}")
        return JSONResponse(status_code=500, content={"message": "An internal server error occurred"})


@router.get("/get_weekly_calorie/{email_id}", tags=["calorie"])
async def get_weekly_calorie(email_id: str) -> JSONResponse:
    """
    Gets the day-by-day total calorie consumption for the last 7 days for the specified user.
    :param email_id: The email ID of the user.
    :return: Day-by-day total calorie consumption in the last 7 days.
    """
    try:
        logger.info(f"Fetching daily calorie data for the last 7 days for {email_id}")

        # Calculate today and 7 days ago as strings in the format "YYYY-MM-DD"
        today = datetime.now().date()
        week_ago = today - timedelta(days=7)

        today_str = str(today)
        week_ago_str = str(week_ago)

        # Aggregate day-by-day calorie data for the last 7 days
        daily_calorie_cursor = collection.aggregate([
            {
                # Match records within the last 7 days by comparing string dates
                "$match": {
                    "email_id": email_id,
                    "date": {"$gte": week_ago_str, "$lte": today_str}
                }
            },
            {
                # Group by date string and sum calories
                "$group": {
                    "_id": "$date",
                    "total_calories": {"$sum": "$calorie"}
                }
            },
            {
                # Sort the results by date in descending order
                "$sort": {"_id": -1}
            }
        ])

        # Convert the cursor to a list of daily calorie data
        daily_calorie_data = []
        for day_data in daily_calorie_cursor:
            daily_calorie_data.append({
                "date": day_data["_id"],
                "total_calories": day_data["total_calories"]
            })

        return JSONResponse(status_code=status.HTTP_200_OK, content={"daily_calorie_data": daily_calorie_data})

    except Exception as e:
        logger.error(f"Error in fetching daily calorie data from MongoDB: {str(e)}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"message": "Internal server error"})
