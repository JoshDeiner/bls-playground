from pydantic import BaseModel
from typing import Dict, Optional

class Calculation(BaseModel):
    pct_changes: Optional[Dict[str, str]]
    net_changes: Optional[Dict[str, str]]

    class Config:
        orm_mode = True
