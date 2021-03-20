#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from django.db import connection


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'resauto.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

def setup_database():
    cursor = connection.cursor()
    #create table queries
    orders_query = """CREATE TABLE IF NOT EXISTS orders(
                        order_id INT(),
                        order
                    )"""

    #execute all crete queries
    cursor.execute(orders_query)


if __name__ == '__main__':
    setup_database()
    main()
