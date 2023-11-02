from cycling_data import CyclingData
from datetime import datetime
import csv
import locale
locale.setlocale(locale.LC_ALL, '')


class GarminImport(CyclingData):
    def __init__(self, db):
        super().__init__(db)

    def import_workouts(self, directory="workout_garmin"):
        with open(directory + "/" + "activities.csv") as f:
            reader = csv.DictReader(f)
            for data_row in reader:
                data = self.get_workout_data(data_row)
                if data != False:
                    self.store_db(data, 2)

    def get_workout_data(self, data_row):
        if data_row["Activiteittype"] != "Fietsen":
            return False

        total_time = self.get_seconds(data_row["Tijd"])
        distance = float(data_row["Afstand"])*1000
        date = datetime.strptime(data_row["Datum"], "%Y-%m-%d %H:%M:%S")
        highest_point = locale.atof(data_row["Maximum hoogte"])

        return {
            "total_time": total_time,
            "distance": distance,
            "max_speed": float(data_row["Max. snelheid"]),
            "avg_speed": float(data_row["Gemiddelde snelheid"]),
            "highest_point": highest_point,
            "elevation_gained": float(data_row["Totale stijging"]),
            "descend": float(data_row["Totale daling"]),
            "date": date.date()
        }

    def get_seconds(self, time):
        hour, minutes, seconds = map(int, time.split(":"))
        return hour*3600+minutes*60+seconds
