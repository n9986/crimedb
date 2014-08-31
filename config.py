import os

ROOT_DIR = os.getcwd()

STORAGE = {
    'engine': 'csv',
    'db_path': os.path.join(ROOT_DIR, 'fixtures/sample_data.csv'),
}

# STORAGE = {
#     'engine': 'sqlite',
#     'db_path': os.path.join(ROOT_DIR, 'fixtures/sample_data.db')
# }

