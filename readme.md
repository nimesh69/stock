cd backend/
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cd backend/
npm install

docker compose exec web python manage.py createsuperuser