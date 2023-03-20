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
    data = pandas.read_csv("data.csv", usecols=[1,2,3,4,5], dtype=float, header=None, names=COLUMN_NAMES)

    # Calculate averages by column, ignoring NaN values.
    means = data.mean(axis=0, skipna=True, numeric_only=True)

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
