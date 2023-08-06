from dataclasses import dataclass
from datetime import datetime
from dapodik.base import DapodikObject
from typing import Optional


@dataclass(eq=False)
class SumberListrik(DapodikObject):
    sumber_listrik_id: str
    nama: str
    create_date: datetime
    last_update: datetime
    expired_date: Optional[datetime]
    last_sync: datetime
    _id: str = 'sumber_listrik_id'
