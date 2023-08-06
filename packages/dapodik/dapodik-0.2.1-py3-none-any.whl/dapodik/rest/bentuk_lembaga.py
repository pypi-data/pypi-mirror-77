from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from dapodik.base import DapodikObject


@dataclass(eq=False)
class BentukLembaga(DapodikObject):
    bentuk_lembaga_id: str
    nama: str
    create_date: datetime
    last_update: datetime
    expired_date: Optional[datetime]
    last_sync: datetime
    _id: str = 'bentuk_lembaga_id'
