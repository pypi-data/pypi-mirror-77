from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from dapodik.base import DapodikObject
from dapodik.utils.decorator import set_meta


@set_meta('sumber_dana_sekolah_id')
@dataclass(eq=False)
class SumberDanaSekolah(DapodikObject):
    sumber_dana_sekolah_id: str
    nama: str
    create_date: datetime
    last_update: datetime
    expired_date: Optional[datetime]
    last_sync: datetime
