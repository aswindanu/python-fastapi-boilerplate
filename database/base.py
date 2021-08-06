from database.setup import Base

# NOTE: Every additional model
# inside dir models/* should be imported here
# for Alembic migration
from models.user import User
from models.item import Item
