from abc import ABC, abstractmethod


class CyclingData(ABC):
    def __init__(self, db):
        self.db = db

    @abstractmethod
    def import_workouts(self, directory):
        pass

    @abstractmethod
    def get_workout_data(self):
        pass

    def store_db(self, data, source, user_id=1):
        date = data['date']
        day_id = self.__get_day_id(date)
        columns = ("user_id", "highest_point", "total_time", "max_speed",
                   "avg_speed", "distance", "date", "elevation_gained", "descend", "day_id", "source_id")
        self.db.insert_data("workout", columns, (user_id, data["highest_point"], data["total_time"], data["max_speed"], data["avg_speed"],
                                                 data["distance"], date, data["elevation_gained"], data["descend"], day_id, source))

    # Get the id of the day, for example the id for Monday is 1
    def __get_day_id(self, date):
        return date.weekday() + 1
