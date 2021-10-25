read -p "Enter revision's name: " name

alembic revision --autogenerate -m "$name"
