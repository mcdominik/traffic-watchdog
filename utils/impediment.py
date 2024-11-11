from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Impediment:
    title: str
    description: str
    pub_date: str
    url_with_details: Optional[str]
    lines: tuple[Optional[str]]
