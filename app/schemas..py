from pydantic import BaseModel
from typing import Optional

class UploadResponse(BaseModel):
    id: int
    file_name: str
    file_path: str

class ReceiptOut(BaseModel):
    id: int
    purchased_at: str
    merchant_name: str
    total_amount: float
    file_path: str

    class Config:
        orm_mode = True
