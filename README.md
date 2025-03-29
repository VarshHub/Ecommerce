This Flask app is an e-commerce platform where users can view products, add them to the cart, and place orders. The admin panel allows managing products and orders.

Tech Stack

Backend: Flask (Python)
Database: MySQL / SQLite (specify which one)
Frontend: HTML, CSS, JavaScript
Other Tools: Bootstrap, Jinja2


How to Run the Project

git clone https://github.com/VarshHub/Ecommerce.git

cd Ecommerce

python -m venv venv
source venv/bin/activate  # For Linux/Mac
venv\Scripts\activate     # For Windows

pip install -r requirements.txt

FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your_secret_key
DATABASE_URL=mysql://username:password@localhost/db_name  # Modify for your DB

flask run

Project Structure
/your-flask-app
 ├── /static                 # Static files (CSS, JS, images)
 ├── /templates              # HTML templates
 ├── app.py                  # Main Flask application file
 ├── .env                    # Environment variables
 ├── README.md               # Project instructions
 ├── .gitignore              # Files to ignore




