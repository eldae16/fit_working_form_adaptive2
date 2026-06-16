#!/usr/bin/env python
import os
import sys

try:
    import pysqlite3
    sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
except ImportError:
    pass

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fit_service.settings')

from django.core.management import execute_from_command_line

execute_from_command_line(sys.argv)