from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    PROJECT_NAME: str = "Financial CSI API"
    VERSION: str = "0.1.0"
    CORS_ORIGINS: list = ["*"]
    
    # Razorpay Settings
    RAZORPAY_ENABLED: bool = False
    RAZORPAY_MODE: str = "test"
    RAZORPAY_KEY_ID: str = ""
    RAZORPAY_KEY_SECRET: str = ""
    RAZORPAY_WEBHOOK_SECRET: str = ""

    DATABASE_URL: str = "sqlite:///./financial_csi.db"
    OPENAI_API_KEY: str = ""

    class Config:
        env_file = ".env"

    @property
    def PROJECT_ROOT(self) -> Path:
        return Path(__file__).resolve().parents[3]

    @property
    def DATA_DIR(self) -> Path:
        return self.PROJECT_ROOT / "data" / "generated"

    @property
    def DOCS_DIR(self) -> Path:
        return self.PROJECT_ROOT / "docs" / "generated"

settings = Settings()
