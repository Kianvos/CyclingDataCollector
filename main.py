import os
from dotenv import load_dotenv

from database import Database
from apple_import import AppleImport
from garmin_import import GarminImport


# todo env
def main():
    load_dotenv()

    db = Database(host=os.getenv("host"), user=os.getenv("db_user"),
                  password=os.getenv("db_password"), database=os.getenv("db_name"))
    db.connect()

    apple_import = AppleImport(db)
    apple_import.import_workouts()

    garmin_import = GarminImport(db)
    garmin_import.import_workouts()
    db.close()


if __name__ == "__main__":
    main()
