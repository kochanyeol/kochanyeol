from pydantic import BaseModel, Field
from datetime import datetime
from fastapi import FastAPI
import uuid

app = FastAPI()

class User(BaseModel):
    user_id: str  = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    role: str = "user"
    created_at: str = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

@app.post("/users")
def create_user(user: User):
    return user