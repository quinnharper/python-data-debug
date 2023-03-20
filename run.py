from bokeh.layouts import column
from bokeh.models import ColumnDataSource, RangeTool
from bokeh.plotting import figure, show
from bokeh.palettes import Spectral4
import pandas

def run():

    # Mapping column names to the input data.
    #  * Column 1 - time
    #  * Column 2 - humidity
    #  * Column 3 - salinity
    #  * Column 4 - air_temperature
    #  * Column 5 - water_temperature
    #  * Column 6 - wind_speed

    COLUMN_NAMES = [
        "time",
        "humidity",
        "salinity",
        "air_temperature",
        "water_temperature",
        "wind_speed"
    ]

    # Load data into a pandas dataframe.
    data = pandas.read_csv("data.csv", dtype=float, header=None, names=COLUMN_NAMES, parse_dates=["time"], index_col="time")

    # Calculate averages by column, ignoring NaN values.
    means = data.mean(axis=0, skipna=True, numeric_only=True)

    # Calculate moving averages over days, quarters and years.
    daily_means = data.rolling(window="1d").mean()
    quarterly_means= data.rolling(window="91d").mean()
    yearly_means = data.rolling(window="365d").mean()

    # Plot the data
    plot_data(data)

    # Return the averages of each column
    return {
        'humidity': means[0],
        'salinity': means[1],
        'air_temperature': means[2],
        'water_temperature': means[3],
        'wind_speed': means[4]
    }

def append_non_nan(column, value):
    if value == value:
        column.append(value)

def plot_data(data):
    dates = data.index

    # Calculate moving averages over days, quarters and years.
    daily_means = data.rolling(window="1d").mean()
    quarterly_means= data.rolling(window="91d").mean()
    yearly_means = data.rolling(window="365d").mean()

    p = figure(height=300, width=800, tools="xpan", toolbar_location=None,
        x_axis_type="datetime", x_axis_location="above",
        background_fill_color="#efefef", x_range=(dates[0], dates[-1]), y_range=(-10,50))
    p.line("time", "air_temperature", source=data, color=Spectral4[0], legend_label="Air Temperature")
    p.line("time", "water_temperature", source=data, color=Spectral4[1], legend_label="Water Temperature")

    p.yaxis.axis_label = "Temperature"

    p.legend.location = "top_left"
    p.legend.click_policy="hide"

    select = figure(title="Drag the middle and edges of the selection box to change the range above",
        height=130, width=800, y_range=p.y_range,
        x_axis_type="datetime", y_axis_type=None,
        tools="", toolbar_location=None, background_fill_color="#efefef")

    range_tool = RangeTool(x_range=p.x_range, y_range=p.y_range)
    range_tool.overlay.fill_color = "navy"
    range_tool.overlay.fill_alpha = 0.2

    select.line("time", "air_temperature", source=data, color=Spectral4[0])
    select.line("time", "water_temperature", source=data, color=Spectral4[1])
    select.ygrid.grid_line_color = None
    select.add_tools(range_tool)

    show(column(p, select))

if __name__ == '__main__':
    import sys
    import time
    import math

    start = time.perf_counter()
    averages = run()
    end = time.perf_counter()

    CORRECT_HUMIDITY = 80.8129
    CORRECT_SALINITY = 36.1433
    CORRECT_AIR_TEMPERATURE = 19.7976
    CORRECT_WATER_TEMPERATURE = 34.1683
    CORRECT_WIND_SPEED = 5.6777

    ANSWERS = {
        'humidity': CORRECT_HUMIDITY,
        'salinity': CORRECT_SALINITY,
        'air_temperature': CORRECT_AIR_TEMPERATURE,
        'water_temperature':CORRECT_WATER_TEMPERATURE,
        'wind_speed': CORRECT_WIND_SPEED,
    }

    for column, value in ANSWERS.items():
        assert math.isclose(
            averages[column],
            value,
            rel_tol=1e-5,
        ), f"{column} should be {value}, instead {averages[column]}"

    print("Succesfully validated the data using {} in {} seconds".format(__file__, end - start))

    sys.exit(0)
