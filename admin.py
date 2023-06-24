"""
This module provides utility functions and a model for managing admin users.

The module includes functions for hashing and verifying passwords using bcrypt,
as well as a model class representing an admin user.
"""

import bcrypt

from flask_login import UserMixin

from models import db


class Admin(db.Model, UserMixin):
    """
    Model representing an admin user.

    Attributes:
        id (db.Column): The primary key of the admin user.
        username (db.Column): The username of the admin user.
        password (db.Column): The hashed password of the admin user.

    Methods:
        set_password: Set the password for the admin user by hashing it.
        check_password: Check if a provided password matches the hashed password of the admin user.
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def set_password(self, password):
        """
        Set the password for the admin user by hashing it.

        Args:
            password (str): The plain-text password to be hashed.
        """

        self.password = hash_password(password)

    def check_password(self, password):
        """
        Check if a provided password matches the hashed password of the admin user.

        Args:
            password (str): The plain-text password to be checked.

        Returns:
            bool: True if the provided password matches the hashed password, False otherwise.
        """

        return verify_password(password, self.password)


def hash_password(password):
    """
    Hash a password using bcrypt.

    Args:
        password (str): The plain-text password to be hashed.

    Returns:
        str: The hashed password.
    """

    salt = bcrypt.gensalt()

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    return hashed_password.decode('utf-8')


def verify_password(password, hashed_password):
    """
    Verify if a provided password matches a hashed password using bcrypt.

    Args:
        password (str): The plain-text password to be checked.
        hashed_password (str): The hashed password to be compared against.

    Returns:
        bool: True if the provided password matches the hashed password, False otherwise.
    """

    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
