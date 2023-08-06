from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from dapodik.base import DapodikObject


@dataclass(eq=False)
class TingkatPendidikan(DapodikObject):
    tingkat_pendidikan_id: str
    kode: str
    nama: str
    jenjang_pendidikan_id: str
    create_date: datetime
    last_update: datetime
    expired_date: Optional[datetime]
    last_sync: datetime
    _id: str = 'tingkat_pendidikan_id'
