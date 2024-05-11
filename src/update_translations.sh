pybabel extract . -o data/locales/base.pot
pybabel update -i data/locales/base.pot -d data/locales
pybabel compile -d data/locales --use-fuzzy