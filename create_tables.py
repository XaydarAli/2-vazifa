from database import ENGINE, Base
from models import User

Base.metadata.create_all(ENGINE)