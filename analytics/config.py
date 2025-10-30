import logging
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Set up environment variables for database credentials
db_username = os.getenv("DB_USERNAME", "myuser")  # Default to 'myuser' if not set
db_password = os.getenv("DB_PASSWORD", "vincentf12")  # Default to 'vincentf12' if not set
db_host = os.getenv("DB_HOST", "127.0.0.1")
db_port = os.getenv("DB_PORT", "5433")  # Use 5433 as the port
db_name = os.getenv("DB_NAME", "mydatabase")

app = Flask(__name__)

# Set the SQLAlchemy URI using environment variables
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Set logging level
app.logger.setLevel(logging.DEBUG)