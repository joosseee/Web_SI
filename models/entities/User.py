from werkzeug.security import check_password_hash,generate_password_hash
from flask_login import UserMixin
import sqlite3
import hashlib
import pandas as pd

class User(UserMixin):
    def __init__(self,username="",tel_number="",password="",province="",permission="",emails_total="", emails_phising="",emails_clicked="") -> None:
        self.username = username
        self.tel_number = tel_number
        self.password = password
        self.province = province
        self.permission = permission
        self.email_total = emails_total
        self.emails_phising = emails_phising
        self.emails_clicked = emails_clicked

    @classmethod
    def check_password(self,hashed_password,password):
        return hashlib.md5(password.encode()).hexdigest() == hashed_password
    
    def get_id(self):
        return self.username
