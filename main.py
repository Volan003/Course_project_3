from src.api import load_data_from_json
from src.config import config
from src.utils import create_database, save_data_to_database


def main():
    params = config()
    database_name = "course_project_3"

    create_database(database_name, params)

    database_name_params = params.copy()
    database_name_params['database_name'] = database_name

    data = load_data_from_json("data/data.json")
    save_data_to_database(data, database_name, params)


if __name__ == "__main__":
    main()
