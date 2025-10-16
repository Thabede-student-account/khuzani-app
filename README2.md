1. Create virtualenv and install:
python -m venv venv
source venv/bin/activate (Windows: venv\Scripts\activate)
pip install -r requirements.txt


2. Create .env with:
SECRET_KEY=your-secret
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your@email.com
MAIL_PASSWORD=yourpassword
MAIL_DEFAULT_SENDER=your@email.com
BOOKING_EMAIL=khuzani.booking@email.com


3. Initialize DB (Flask-Migrate):
export FLASK_APP=app.py
flask db init
flask db migrate -m "init"
flask db upgrade


4. Create initial admin (temporary route):
Run the app and visit /admin/setup to create admin (username=admin, password=changeme). Remove or protect this route in production.


5. Run:
python app.py
