import os
import gpxpy.gpx
import gpxpy

from cycling_data import CyclingData


class AppleImport(CyclingData):

    def import_workouts(self, directory="workouts_apple"):
        for file in os.listdir(directory):
            if file.endswith(".gpx"):
                gpx_file = open(directory + "/" + file)
                data = self.get_workout_data(gpx_file)
                if data != False:
                    self.store_db(data, 1)

    def get_workout_data(self, gpx_file):
        gpx = gpxpy.parse(gpx_file)

        highest_point = -999
        elevation_gained = 0
        total_descend = 0
        date = None
        last_elevation = None

        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    if last_elevation is not None:
                        date = point.time
                        elevation_change = point.elevation - last_elevation
                        if elevation_change < 0:
                            total_descend += abs(elevation_change)
                        else:
                            elevation_gained += elevation_change
                    last_elevation = point.elevation
                    if (point.elevation > highest_point):
                        highest_point = point.elevation

        moving_data = gpx.get_moving_data(raw=False)
        total_time = moving_data.moving_time
        distance = moving_data.moving_distance + moving_data.stopped_distance
        max_speed = moving_data.max_speed*3.6
        try:
            avg_speed = distance/total_time*3.6
        except:
            return False
        # Exclude most walk and running workouts
        if max_speed < 16 and avg_speed < 12:
            return False

        return {
            "total_time": total_time,
            "distance": distance,
            "max_speed": max_speed,
            "avg_speed": avg_speed,
            "highest_point": highest_point,
            "elevation_gained": elevation_gained,
            "descend": total_descend,
            "date": date.date()
        }
