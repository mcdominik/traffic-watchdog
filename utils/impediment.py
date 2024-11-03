from dataclasses import dataclass
from typing import Optional

from utils.vehicle import Vehicle


@dataclass(frozen=True)
class Impediment:
    title: str
    description: str
    pub_date: str
    url_with_details: Optional[str]
    vehicle: Optional[Vehicle]
    line: Optional[str]
