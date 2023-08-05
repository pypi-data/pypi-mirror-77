from dataclasses import dataclass
from dapodik.base import BaseData


@dataclass
class UpdatePanelDashboard(BaseData):
    paneljumlahgtk: str
    paneljumlahguru: str
    paneljumlahtendik: str
    paneljumlahpns: str
    paneljumlahgty: str
    paneljumlahhonorer: str
    paneljumlahpd: str
    paneljumlahpdabk: str
    paneljumlahpdbantuanpd: str
    paneljumlahrombel: str
    paneljumlahrombelreguler: str
    paneljumlahrombeljauh: str
    paneljumlahrombelterbuka: str
    paneljumlahrk: str
    paneljumlahlab: str
    paneljumlahperpus: str
