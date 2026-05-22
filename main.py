from src.db import create_database
from src.config import config

def main():
    params = config()
    create_database("Course_project_3", params)

if __name__ == "__main__":
    main()