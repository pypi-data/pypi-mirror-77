from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from dapodik.base import BaseData


@dataclass
class FasilitasLayanan(BaseData):
    fasilitas_layanan_id: str
    nama: str
    create_date: datetime
    last_update: datetime
    expired_date: Optional[datetime]
    last_sync: datetime
