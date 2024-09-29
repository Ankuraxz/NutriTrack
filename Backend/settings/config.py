import logging
import os
from langchain_openai import ChatOpenAI as OpenAI
import pymongo
import certifi
from openai import OpenAI as visionopenai
from azure.storage.blob import BlobServiceClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Config:
    _instance = None

    @staticmethod
    def get_instance():
        """Return the singleton instance of Config"""
        if Config._instance is None:
            Config._instance = Config()
        return Config._instance

    def __init__(self):
        if Config._instance is not None:
            raise Exception(
                "Config is a singleton class, use get_instance() to get the instance."
            )

        try:
            self.open_ai_key = os.environ["OPENAI_API_KEY"]
            self.mongo_uri = os.environ["MONGO_URI"]
            self.azure_storage_name = "calorieinfo"
            self.azure_storage_connection_string = os.environ["AZURE_STORAGE_CONN_STRING"]
            self.azure_storage_key = os.environ["AZURE_STORAGE_KEY"]

        except KeyError as e:
            logger.error(f"Missing environment variable: {e}")
            raise e

    def get_mongo_client(self):
        try:
            logger.info("Connecting to MongoDB")
            client = pymongo.MongoClient(os.environ['MONGO_URI'], ssl=True, tlsCAFile=certifi.where())
            client.admin.command('ping')
            logger.info(f"Connected to MongoDB")
            return client
        except Exception as e:
            logger.error(f"Error in connecting to MongoDB: {str(e)}")
            raise e

    def get_openai_chat_connection(self):
        try:
            logger.info("Connecting to GPT-4o's Latest Variant")
            chat_llm = OpenAI(max_tokens=4000, temperature=0.6, model='gpt-4o')
            if chat_llm is None:
                raise Exception("Error in connecting to GPT-4o's Latest Variant")
            else:
                logger.info("Connected to GPT-4o's Latest Variant")
            return chat_llm
        except Exception as e:
            logger.error(f"Error in connecting to GPT-3.5: {str(e)}")
            raise e

    def get_openai_vision_connection(self):
        try:
            logger.info("Connecting to OpenAI Vision")
            vision_client = visionopenai()
            if vision_client is None:
                raise Exception("Error in connecting to OpenAI Vision")
            else:
                logger.info("Connected to OpenAI Vision")
            return vision_client
        except Exception as e:
            logger.error(f"Error in connecting to OpenAI Vision: {str(e)}")
            raise e

    def get_azure_storage_client(self):
        try:
            logger.info("Connecting to Azure Storage")
            service = BlobServiceClient(account_url="https://calorieinfo.blob.core.windows.net",
                                        credential=self.azure_storage_key)
            if service:
                logger.info("Connected to Azure Storage")
                return service
            else:
                raise Exception("Error in connecting to Azure Storage")
        except Exception as e:
            logger.error(f"Error in connecting to Azure Storage: {str(e)}")
            raise e
