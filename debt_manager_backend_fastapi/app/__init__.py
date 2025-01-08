from flask_sqlalchemy import SQLAlchemy

from app.migrations.create_database import main

db = SQLAlchemy()

main()

