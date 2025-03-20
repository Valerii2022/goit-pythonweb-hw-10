class Config:
    DB_URL = "postgresql+asyncpg://postgres:567234@localhost:5432/contacts_app"
    JWT_SECRET = "your_secret_key"  
    JWT_ALGORITHM = "HS256"  
    JWT_EXPIRATION_SECONDS = 3600  

config = Config
