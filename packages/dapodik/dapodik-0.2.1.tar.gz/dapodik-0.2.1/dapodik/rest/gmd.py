from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from dapodik.base import DapodikObject


@dataclass(eq=False)
class Gmd(DapodikObject):
    id_gmd: str
    nm_gmd: str
    create_date: datetime
    last_update: datetime
    expired_date: Optional[datetime]
    last_sync: datetime
    _id: str = 'id_gmd'
