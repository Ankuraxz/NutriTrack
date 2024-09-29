import logging
import os
import uuid
from fastapi import APIRouter, Form, HTTPException, Header, UploadFile, status
from fastapi.responses import JSONResponse
from typing import Optional, Annotated, Union
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, PublicAccess
from settings.config import Config
from settings.utils import get_username_from_email

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()
Config = Config()
vision_llm = Config.get_openai_vision_connection()

# Get the Azure Storage client from configuration
azure_storage_client = Config.get_azure_storage_client()

# Enable Python multipart form data
@router.post("/get_calorie_value", tags=["ai_image"])
async def get_calorie_value(email_id: Annotated[Union[str, None], Header()],
                            image_file: UploadFile = Form(...)):
    """
    Get calorie value of a food item from an image.

    :param email_id: The email of the user
    :param image_file: The uploaded image file
    :return: dict with the calorie value or an error message
    """
    try:
        username = get_username_from_email(email_id)
        logger.info(f"Processing image for user: {username}")
        print(image_file.content_type)

        # Validate image file type
        if image_file.content_type not in ["image/jpeg", "image/jpg", "image/png"]:
            return JSONResponse(content={"message": "Only .jpg/.jpeg/.png images are allowed"},
                                status_code=status.HTTP_400_BAD_REQUEST)

        # Generate a unique name for the image
        random_num = uuid.uuid4()
        image_name = f"image_{random_num}.jpg"
        image_path = f"/tmp/{image_name}"

        # Save the uploaded file locally
        with open(image_path, "wb") as f:
            f.write(await image_file.read())

        # Create or get the user's container
        container_name = username
        container_client = azure_storage_client.get_container_client(container_name)

        # Check if container exists, if not create it
        try:
            container_client.create_container(public_access=PublicAccess.Container)
            logger.info(f"Created container for user: {container_name}")
        except Exception as e:
            logger.info(f"Container for user {container_name} already exists or another issue occurred: {str(e)}")

        # Upload the file to Azure Blob Storage
        blob_client = azure_storage_client.get_blob_client(container=container_name, blob=image_name)
        with open(image_path, "rb") as data:
            blob_client.upload_blob(data)

        # Remove local file after uploading
        os.remove(image_path)

        # Construct the Azure Blob Storage URL for the uploaded image
        azure_blob_url = f"https://calorieinfo.blob.core.windows.net/{container_name}/{image_name}"
        logger.info(f"File uploaded to Azure Blob Storage: {azure_blob_url}")

        # Use OpenAI Vision model (or another API) to process the image and get calorie data
        response1 = vision_llm.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Guess the Calorie value of this food item from this image. Just give the number of calories, and no other chracter like around or about etc, "},
                        {"type": "image_url", "image_url": {"url": azure_blob_url}},
                    ],
                }
            ],
            max_tokens=300,
        )
        response2 = vision_llm.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text",
                         "text": "Guess the Food Item in this image. Just give the name of the dish "},
                        {"type": "image_url", "image_url": {"url": azure_blob_url}},
                    ],
                }
            ],
            max_tokens=300,
        )

        # Return the response with the calorie value
        return {"name": response2.choices[0].message.content, "calorie_value": response1.choices[0].message.content}

    except Exception as e:
        logger.error(f"Error processing image for calorie value: {str(e)}")
        return JSONResponse(content={"message": "An error occurred while processing the image."},
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
