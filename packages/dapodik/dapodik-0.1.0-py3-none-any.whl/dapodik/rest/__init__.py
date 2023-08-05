from dapodik.base import BaseDapodik, Rest
from .agama import Agama
from .akreditasi import Akreditasi
from .akses_internet import AksesInternet
from .alat_transportasi import AlatTransportasi
from .bank import Bank
from .bentuk_lembaga import BentukLembaga
from .child_delete import ChildDelete
from .fasilitas_layanan import FasilitasLayanan
from .gmd import Gmd
from .jadwal_paud import JadwalPaud
from .jenis_gugus import JenisGugus
from .jenis_hapus_buku import JenisHapusBuku
from .jenis_keluar import JenisKeluar
from .jenis_lk import JenisLk
from .jenis_pendaftaran import JenisPendaftaran
from .jenis_prasarana import JenisPrasarana
from .jenis_sarana import JenisSarana
from .jenis_tinggal import JenisTinggal
from .kategori_tk import KategoriTk
from .kebutuhan_khusus import KebutuhanKhusus
from .klasifikasi_lembaga import KlasifikasiLembaga
from .lembaga_pengangkat import LembagaPengangkat
from .mst_wilayah import MstWilayah
from .pangkat_golongan import PangkatGolongan
from .pekerjaan import Pekerjaan
from .pengguna import Pengguna
from .penghasilan import Penghasilan
from .role_pengguna import RolePengguna
from .status_keaktifan_pegawai import StatusKeaktifanPegawai
from .status_kepegawaian import StatusKepegawaian
from .status_kepemilikan_sarpras import StatusKepemilikanSarpras
from .sumber_air import SumberAir
from .sumber_dana_sekolah import SumberDanaSekolah
from .sumber_gaji import SumberGaji
from .sumber_listrik import SumberListrik
from .sync_log import SyncLog
from .tingkat_pendidikan import TingkatPendidikan
from .waktu_penyelenggaraan import WaktuPenyelenggaraan


class BaseRest(BaseDapodik):
    _Agama: Rest = None
    _Akreditasi: Rest = None
    _AksesInternet: Rest = None
    _AlatTransportasi: Rest = None
    _Bank: Rest = None
    _BentukLembaga: Rest = None
    _ChildDelete: Rest = None
    _FasilitasLayanan: Rest = None
    _Gmd: Rest = None
    _JadwalPaud: Rest = None
    _JenisGugus: Rest = None
    _JenisHapusBuku: Rest = None
    _JenisKeluar: Rest = None
    _JenisLk: Rest = None
    _JenisPendaftaran: Rest = None
    _JenisPrasarana: Rest = None
    _JenisSarana: Rest = None
    _JenisTinggal: Rest = None
    _KategoriTk: Rest = None
    _KebutuhanKhusus: Rest = None
    _KlasifikasiLembaga: Rest = None
    _LembagaPengangkat: Rest = None
    _MstWilayah: Rest = None
    _PangkatGolongan: Rest = None
    _Pekerjaan: Rest = None
    _Pengguna: Rest = None
    _Penghasilan: Rest = None
    _RolePengguna: Rest = None
    _StatusKeaktifanPegawai: Rest = None
    _StatusKepegawaian: Rest = None
    _StatusKepemilikanSarpras: Rest = None
    _SumberAir: Rest = None
    _SumberDanaSekolah: Rest = None
    _SumberGaji: Rest = None
    _SumberListrik: Rest = None
    _SyncLog: Rest = None
    _TingkatPendidikan: Rest = None
    _WaktuPenyelenggaraan: Rest = None

    @property
    def Agama(self) -> Rest:
        if self._Agama:
            return self._Agama
        self._Agama = Rest(
            self, Agama, 'rest/Agama'
        )
        return self._Agama

    @property
    def Akreditasi(self) -> Rest:
        if self._Akreditasi:
            return self._Akreditasi
        self._Akreditasi = Rest(
            self, Akreditasi, 'rest/Akreditasi'
        )
        return self._Akreditasi

    @property
    def AksesInternet(self) -> Rest:
        if self._AksesInternet:
            return self._AksesInternet
        self._AksesInternet = Rest(
            self, AksesInternet, 'rest/AksesInternet'
        )
        return self._AksesInternet

    @property
    def AlatTransportasi(self) -> Rest:
        if self._AlatTransportasi:
            return self._AlatTransportasi
        self._AlatTransportasi = Rest(
            self, AlatTransportasi, 'rest/AlatTransportasi'
        )
        return self._AlatTransportasi

    @property
    def Bank(self) -> Rest:
        if self._Bank:
            return self._Bank
        self._Bank = Rest(
            self, Bank, 'rest/Bank'
        )
        return self._Bank

    @property
    def BentukLembaga(self) -> Rest:
        if self._BentukLembaga:
            return self._BentukLembaga
        self._BentukLembaga = Rest(
            self, BentukLembaga, 'rest/BentukLembaga'
        )
        return self._BentukLembaga

    @property
    def ChildDelete(self) -> Rest:
        if self._ChildDelete:
            return self._ChildDelete
        self._ChildDelete = Rest(
            self, ChildDelete, 'rest/ChildDelete'
        )
        return self._ChildDelete

    @property
    def FasilitasLayanan(self) -> Rest:
        if self._FasilitasLayanan:
            return self._FasilitasLayanan
        self._FasilitasLayanan = Rest(
            self, FasilitasLayanan, 'rest/FasilitasLayanan'
        )
        return self._FasilitasLayanan

    @property
    def Gmd(self) -> Rest:
        if self._Gmd:
            return self._Gmd
        self._Gmd = Rest(
            self, Gmd, 'rest/Gmd'
        )
        return self._Gmd

    @property
    def JadwalPaud(self) -> Rest:
        if self._JadwalPaud:
            return self._JadwalPaud
        self._JadwalPaud = Rest(
            self, JadwalPaud, 'rest/JadwalPaud'
        )
        return self._JadwalPaud

    @property
    def JenisGugus(self) -> Rest:
        if self._JenisGugus:
            return self._JenisGugus
        self._JenisGugus = Rest(
            self, JenisGugus, 'rest/JenisGugus'
        )
        return self._JenisGugus

    @property
    def JenisHapusBuku(self) -> Rest:
        if self._JenisHapusBuku:
            return self._JenisHapusBuku
        self._JenisHapusBuku = Rest(
            self, JenisHapusBuku, 'rest/JenisHapusBuku'
        )
        return self._JenisHapusBuku

    @property
    def JenisKeluar(self) -> Rest:
        if self._JenisKeluar:
            return self._JenisKeluar
        self._JenisKeluar = Rest(
            self, JenisKeluar, 'rest/JenisKeluar'
        )
        return self._JenisKeluar

    @property
    def JenisLk(self) -> Rest:
        if self._JenisLk:
            return self._JenisLk
        self._JenisLk = Rest(
            self, JenisLk, 'rest/JenisLk'
        )
        return self._JenisLk

    @property
    def JenisPendaftaran(self) -> Rest:
        if self._JenisPendaftaran:
            return self._JenisPendaftaran
        self._JenisPendaftaran = Rest(
            self, JenisPendaftaran, 'rest/JenisPendaftaran'
        )
        return self._JenisPendaftaran

    @property
    def JenisPrasarana(self) -> Rest:
        if self._JenisPrasarana:
            return self._JenisPrasarana
        self._JenisPrasarana = Rest(
            self, JenisPrasarana, 'rest/JenisPrasarana'
        )
        return self._JenisPrasarana

    @property
    def JenisSarana(self) -> Rest:
        if self._JenisSarana:
            return self._JenisSarana
        self._JenisSarana = Rest(
            self, JenisSarana, 'rest/JenisSarana'
        )
        return self._JenisSarana

    @property
    def JenisTinggal(self) -> Rest:
        if self._JenisTinggal:
            return self._JenisTinggal
        self._JenisTinggal = Rest(
            self, JenisTinggal, 'rest/JenisTinggal'
        )
        return self._JenisTinggal

    @property
    def KategoriTk(self) -> Rest:
        if self._KategoriTk:
            return self._KategoriTk
        self._KategoriTk = Rest(
            self, KategoriTk, 'rest/KategoriTk'
        )
        return self._KategoriTk

    @property
    def KebutuhanKhusus(self) -> Rest:
        if self._KebutuhanKhusus:
            return self._KebutuhanKhusus
        self._KebutuhanKhusus = Rest(
            self, KebutuhanKhusus, 'rest/KebutuhanKhusus'
        )
        return self._KebutuhanKhusus

    @property
    def KlasifikasiLembaga(self) -> Rest:
        if self._KlasifikasiLembaga:
            return self._KlasifikasiLembaga
        self._KlasifikasiLembaga = Rest(
            self, KlasifikasiLembaga, 'rest/KlasifikasiLembaga'
        )
        return self._KlasifikasiLembaga

    @property
    def LembagaPengangkat(self) -> Rest:
        if self._LembagaPengangkat:
            return self._LembagaPengangkat
        self._LembagaPengangkat = Rest(
            self, LembagaPengangkat, 'rest/LembagaPengangkat'
        )
        return self._LembagaPengangkat

    @property
    def MstWilayah(self) -> Rest:
        if self._MstWilayah:
            return self._MstWilayah
        self._MstWilayah = Rest(
            self, MstWilayah, 'rest/MstWilayah'
        )
        return self._MstWilayah

    @property
    def PangkatGolongan(self) -> Rest:
        if self._PangkatGolongan:
            return self._PangkatGolongan
        self._PangkatGolongan = Rest(
            self, PangkatGolongan, 'rest/PangkatGolongan'
        )
        return self._PangkatGolongan

    @property
    def Pekerjaan(self) -> Rest:
        if self._Pekerjaan:
            return self._Pekerjaan
        self._Pekerjaan = Rest(
            self, Pekerjaan, 'rest/Pekerjaan'
        )
        return self._Pekerjaan

    @property
    def Pengguna(self) -> Rest:
        if self._Pengguna:
            return self._Pengguna
        self._Pengguna = Rest(
            self, Pengguna, 'rest/Pengguna'
        )
        return self._Pengguna

    @property
    def Penghasilan(self) -> Rest:
        if self._Penghasilan:
            return self._Penghasilan
        self._Penghasilan = Rest(
            self, Penghasilan, 'rest/Penghasilan'
        )
        return self._Penghasilan

    @property
    def RolePengguna(self) -> Rest:
        if self._RolePengguna:
            return self._RolePengguna
        self._RolePengguna = Rest(
            self, RolePengguna, 'rest/RolePengguna'
        )
        return self._RolePengguna

    @property
    def StatusKeaktifanPegawai(self) -> Rest:
        if self._StatusKeaktifanPegawai:
            return self._StatusKeaktifanPegawai
        self._StatusKeaktifanPegawai = Rest(
            self, StatusKeaktifanPegawai, 'rest/StatusKeaktifanPegawai'
        )
        return self._StatusKeaktifanPegawai

    @property
    def StatusKepegawaian(self) -> Rest:
        if self._StatusKepegawaian:
            return self._StatusKepegawaian
        self._StatusKepegawaian = Rest(
            self, StatusKepegawaian, 'rest/StatusKepegawaian'
        )
        return self._StatusKepegawaian

    @property
    def StatusKepemilikanSarpras(self) -> Rest:
        if self._StatusKepemilikanSarpras:
            return self._StatusKepemilikanSarpras
        self._StatusKepemilikanSarpras = Rest(
            self, StatusKepemilikanSarpras, 'rest/StatusKepemilikanSarpras'
        )
        return self._StatusKepemilikanSarpras

    @property
    def SumberAir(self) -> Rest:
        if self._SumberAir:
            return self._SumberAir
        self._SumberAir = Rest(
            self, SumberAir, 'rest/SumberAir'
        )
        return self._SumberAir

    @property
    def SumberDanaSekolah(self) -> Rest:
        if self._SumberDanaSekolah:
            return self._SumberDanaSekolah
        self._SumberDanaSekolah = Rest(
            self, SumberDanaSekolah, 'rest/SumberDanaSekolah'
        )
        return self._SumberDanaSekolah

    @property
    def SumberGaji(self) -> Rest:
        if self._SumberGaji:
            return self._SumberGaji
        self._SumberGaji = Rest(
            self, SumberGaji, 'rest/SumberGaji'
        )
        return self._SumberGaji

    @property
    def SumberListrik(self) -> Rest:
        if self._SumberListrik:
            return self._SumberListrik
        self._SumberListrik = Rest(
            self, SumberListrik, 'rest/SumberListrik'
        )
        return self._SumberListrik

    @property
    def SyncLog(self) -> Rest:
        if self._SyncLog:
            return self._SyncLog
        self._SyncLog = Rest(
            self, SyncLog, 'rest/SyncLog'
        )
        return self._SyncLog

    @property
    def TingkatPendidikan(self) -> Rest:
        if self._TingkatPendidikan:
            return self._TingkatPendidikan
        self._TingkatPendidikan = Rest(
            self, TingkatPendidikan, 'rest/TingkatPendidikan'
        )
        return self._TingkatPendidikan

    @property
    def WaktuPenyelenggaraan(self) -> Rest:
        if self._WaktuPenyelenggaraan:
            return self._WaktuPenyelenggaraan
        self._WaktuPenyelenggaraan = Rest(
            self, WaktuPenyelenggaraan, 'rest/WaktuPenyelenggaraan'
        )
        return self._WaktuPenyelenggaraan
