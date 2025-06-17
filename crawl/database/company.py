from database.entity import Entity
from utils.tools import builder

@builder
class Company(Entity):
    id: str
    name: str
    stage: str
    scale: str
    welfare: str
    table_name: str = "company"
    key_name: str = "id"
    
    def __post_init__(self):
        self.name = self.name.strip()
        self.stage = self.stage.strip()
        self.scale = self.scale.strip()
        