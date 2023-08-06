from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from dapodik.base import DapodikObject


@dataclass(eq=False)
class SumberAir(DapodikObject):
    sumber_air_id: str
    nama: str
    sumber_air: str
    sumber_minum: str
    create_date: datetime
    last_update: datetime
    expired_date: Optional[datetime]
    last_sync: datetime
    _id: str = 'sumber_air_id'
