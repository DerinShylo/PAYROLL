import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'your-secret-key'

    # --- MYSQL DIRECT CONNECTION ---
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:admin123@localhost/payroll'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
