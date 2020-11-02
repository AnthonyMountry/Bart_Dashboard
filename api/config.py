import os
from os.path import join as path_join

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + path_join(os.getcwd(), 'db/dashboard.db')
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + path_join(os.getcwd(), 'db/_dashboard.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
