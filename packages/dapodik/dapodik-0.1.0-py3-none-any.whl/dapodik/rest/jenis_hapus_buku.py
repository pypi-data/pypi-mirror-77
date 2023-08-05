from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from dapodik.base import BaseData


@dataclass
class JenisHapusBuku(BaseData):
    id_hapus_buku: str
    ket_hapus_buku: str
    u_prasarana: str
    u_sarana: str
    create_date: datetime
    last_update: datetime
    expired_date: Optional[datetime]
    last_sync: datetime
