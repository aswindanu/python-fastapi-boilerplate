# migrate
alembic revision --autogenerate -m "First migration"
alembic upgrade head
# seeding
python database/seed.py
# start
uvicorn main:app --host 0.0.0.0 --reload