import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    MUSE_WONDER_KEY: str = os.getenv("MUSE_WONDER_API_KEY", "")
    SAM_API_KEY: str = os.getenv("MUSE_IMAGE_SAM_API_KEY", "")
    BASETEN_KEY: str = os.getenv("BASETEN_API_KEY", "")

settings = Settings()
