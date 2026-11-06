"""Refresh tokens live in Windows Credential Manager, never application JSON."""
import ctypes
import hashlib
import sys
from ctypes import wintypes


class Credential(ctypes.Structure):
    _fields_ = [('Flags', wintypes.DWORD), ('Type', wintypes.DWORD), ('TargetName', wintypes.LPWSTR),
                ('Comment', wintypes.LPWSTR), ('LastWritten', wintypes.FILETIME),
                ('CredentialBlobSize', wintypes.DWORD), ('CredentialBlob', ctypes.POINTER(ctypes.c_ubyte)),
                ('Persist', wintypes.DWORD), ('AttributeCount', wintypes.DWORD),
                ('Attributes', ctypes.c_void_p), ('TargetAlias', wintypes.LPWSTR), ('UserName', wintypes.LPWSTR)]


class SecureStorage:
    @staticmethod
    def _api():
        if sys.platform != 'win32':
            raise OSError('Lưu phiên an toàn hiện chỉ hỗ trợ Windows.')
        api = ctypes.WinDLL('Advapi32.dll', use_last_error=True)
        api.CredWriteW.argtypes = [ctypes.POINTER(Credential), wintypes.DWORD]
        api.CredReadW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD, ctypes.POINTER(ctypes.POINTER(Credential))]
        api.CredDeleteW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD]
        api.CredFree.argtypes = [ctypes.c_void_p]
        return api

    @staticmethod
    def target(project):
        return 'AbyssalSkillsD/refresh/' + hashlib.sha256(project.encode()).hexdigest()[:24]

    @classmethod
    def write(cls, project, token):
        blob = token.encode('utf-8')
        buffer = (ctypes.c_ubyte * len(blob)).from_buffer_copy(blob)
        credential = Credential(Type=1, TargetName=cls.target(project), CredentialBlobSize=len(blob),
                                CredentialBlob=buffer, Persist=2, UserName='AbyssalSkillsD')
        if not cls._api().CredWriteW(ctypes.byref(credential), 0):
            raise ctypes.WinError(ctypes.get_last_error())

    @classmethod
    def read(cls, project):
        pointer = ctypes.POINTER(Credential)()
        api = cls._api()
        if not api.CredReadW(cls.target(project), 1, 0, ctypes.byref(pointer)):
            if ctypes.get_last_error() == 1168:
                return None
            raise ctypes.WinError(ctypes.get_last_error())
        try:
            return ctypes.string_at(pointer.contents.CredentialBlob, pointer.contents.CredentialBlobSize).decode('utf-8')
        finally:
            api.CredFree(pointer)

    @classmethod
    def delete(cls, project):
        api = cls._api()
        if not api.CredDeleteW(cls.target(project), 1, 0) and ctypes.get_last_error() != 1168:
            raise ctypes.WinError(ctypes.get_last_error())
