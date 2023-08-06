from dataclasses import dataclass
from datetime import datetime
from dapodik.base import DapodikObject
from typing import Optional
from dapodik.utils.decorator import set_meta


@set_meta('sumber_listrik_id')
@dataclass(eq=False)
class SumberListrik(DapodikObject):
    sumber_listrik_id: str
    nama: str
    create_date: datetime
    last_update: datetime
    expired_date: Optional[datetime]
    last_sync: datetime
