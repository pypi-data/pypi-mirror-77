from dataclasses import dataclass
from datetime import datetime


@dataclass
class Content:
    vaknl_acco_id: int
    giataid: int
    goalid: int
    source: str  # provider of the data
    timestamp: str  # timestamp updated

    def __post_init__(self):
        if isinstance(self.vaknl_acco_id, str):
            self.goalid = int(self.vaknl_acco_id)
        if isinstance(self.giataid, str):
            self.giataid = int(self.giataid)
        if isinstance(self.goalid, str):
            self.goalid = int(self.goalid)
        if not self.timestamp:
            self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
