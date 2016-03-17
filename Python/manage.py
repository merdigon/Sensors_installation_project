#!/usr/bin/env python
import os
import sys

PROJECT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "AlarmSystem")
sys.path.append(PROJECT)
sys.path.append(os.path.join(PROJECT, "lib"))

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AlarmSystem.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
