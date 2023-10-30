from pydantic import BaseModel

class StoneActivationRequest(BaseModel):
    stone_id: str
    user_id: int
    power_duration: int
