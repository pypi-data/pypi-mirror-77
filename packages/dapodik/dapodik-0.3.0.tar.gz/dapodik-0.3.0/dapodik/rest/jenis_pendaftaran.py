from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from dapodik.base import DapodikObject
from dapodik.utils.decorator import set_meta


@set_meta('jenis_pendaftaran_id')
@dataclass(eq=False)
class JenisPendaftaran(DapodikObject):
    jenis_pendaftaran_id: str
    nama: str
    daftar_sekolah: str
    daftar_rombel: str
    create_date: datetime
    last_update: datetime
    expired_date: Optional[datetime]
    last_sync: datetime
