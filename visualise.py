import os
from dotenv import load_dotenv
import pandas
import matplotlib.pyplot as pyplot
from database import Database


def main():
    load_dotenv()

    db = Database(host=os.getenv("host"), user=os.getenv("db_user"),
                  password=os.getenv("db_password"), database=os.getenv("db_name"))

    db.connect()

    day_distance_chart(db)
    month_distance_chart(db)
    calender_day_distance_chart(db)
    pyplot.show()

    db.close()


def day_distance_chart(db):
    table = "workout"
    fields = ["sum(distance)/1000 as distance", "day_week.day as day"]
    joins = [
        {
            "type": "left join",
            "join_table": "day_week",
            "join_table_field": "id",
            "table": table,
            "field": "day_id"
        }
    ]
    order_by = "day_week.id"
    group_by = order_by
    data = db.select(table, fields, joins=joins,
                     order_by=order_by, group_by=group_by)

    bar_data = ["day", "distance"]
    title = "Totaal gereden afstand per dag van de week"
    xlabel = "Dag van de week"
    ylabel = "Totaal gereden afstand (in kilometers)"
    plot_bar_chart(data, bar_data, title, xlabel,
                   ylabel, ytick=250, ytext=True)


def month_distance_chart(db):
    table = "workout"
    fields = ["monthname(date) as month", "sum(distance)/1000 as distance"]
    order_by = "month(date)"
    group_by = ["month", order_by]
    data = db.select(table, fields, order_by=order_by, group_by=group_by)

    bar_data = ["month", "distance"]
    title = "Totaal gereden afstand per maand (alle jaren)"
    xlabel = "Maand"
    ylabel = "Totaal gereden afstand (in kilometers)"
    plot_bar_chart(data, bar_data, title, xlabel,
                   ylabel, ytick=250, ytext=True)


def calender_day_distance_chart(db):
    table = "workout"
    fields = ["DAY(date) as day", "sum(distance)/1000 as distance"]
    order_by = "day"
    group_by = order_by
    data = db.select(table, fields, order_by=order_by, group_by=group_by)

    bar_data = ["day", "distance"]
    title = "Totaal gereden afstand per kalenderdag (alle jaren)"
    xlabel = "Dag"
    ylabel = "Totaal gereden afstand (in kilometers)"
    plot_bar_chart(data, bar_data, title, xlabel,
                   ylabel, type="line", ytick=50)


def plot_bar_chart(data, bar_data, title="", xlabel="", ylabel="", type="bar", ytick=None, ytext=None):
    df = pandas.DataFrame(data)
    x, y = df[bar_data[0]], df[bar_data[1]]
    pyplot.figure(figsize=(12, 8))
    if type == "bar":
        pyplot.bar(x, y)

    elif type == "line":
        create_line_chart(x, y)

    if ytick:
        pyplot.yticks(range(0, int(max(y))+100, ytick))

    if ytext:
        add_text_labels(y)

    pyplot.title(title)
    pyplot.xlabel(xlabel)
    pyplot.ylabel(ylabel)
    pyplot.xticks(x)


def create_line_chart(x, y):
    pyplot.yticks(range(0, int(max(y))+100, 50))
    pyplot.ylim(0, max(y) + 100)
    pyplot.plot(x, y, ** {'marker': 'o'})


def add_text_labels(y):
    above_text = int(max(y)/50)
    for i, v in enumerate(y):
        v = round(v, 2)
        pyplot.text(i-0.4, v+above_text, str(v))


if __name__ == "__main__":
    main()
