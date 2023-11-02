
# CycleDataLink - Fietsgegevens importeren naar database

CycleDataLink is een handige app waarmee je moeiteloos fietsgegevens van verschillende bronnen kunt importeren en opslaan in een centrale database. Deze app ondersteunt Apple Health Workouts (gpx) en Garmin Workouts.

## Gebruik

1. Kopieer het `.env.example`-bestand naar `.env` en vul de vereiste gegevens in.

2. Zorg ervoor dat je Garmin-gegevensbestand de naam 'activities.csv' heeft en zich bevindt in de map 'workout_garmin'.

3. Plaats Apple Health gpx-bestanden in de map 'workouts_apple'.

4. Voer het volgende commando uit in de terminal om de app te starten: `python3 main.py`

**Opmerking**: 
- CycleDataLink ondersteunt momenteel alleen Garmin CSV-bestanden in het Nederlands.
- Houd er rekening mee dat bij het importeren van Apple Health workouts, een kans bestaat dat andere type workouts worden ingeladen en dat het dus niet 100% zeker is dat je alleen je fietsritten krijgt.
- In de gpx files staat de afstand niet. Deze wordt berekent door een gpx library, deze wijkt wat af van de door apple aangegeven kilometers. Ongeveer 1% afwijking.
