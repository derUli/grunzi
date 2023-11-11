@echo off
pybabel extract . -o data\locale\base.pot
pybabel update -i data\locale\base.pot -d data\locale
pybabel compile -d data\locale --use-fuzzy