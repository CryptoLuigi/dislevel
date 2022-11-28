from dataclasses import dataclass

__version__ = "3.0.1"


@dataclass
class VersionInfo:
    major: int
    minor: int
    micro: int
    releaselevel: str
    serial: int


version_info = VersionInfo(3, 0, 1, "latest", 0)
