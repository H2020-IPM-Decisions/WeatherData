## UTIL methods
from datetime import datetime
def to_epoch_seconds(some_kind_of_date):
    """Attempts to convert a date string into Epoch seconds"""
    # Epochs and None are returned as is
    # We only try to convert strings
    try:
        # if the date is an invalid string, the ValueError is propagated
        return datetime.fromisoformat(some_kind_of_date.replace("Z","+00:00")).timestamp()
    except (TypeError, AttributeError):
        if some_kind_of_date is None or isinstance(some_kind_of_date, int):
            return some_kind_of_date
        else:
            raise TypeError("Date (timeStart or timeEnd) is neither None, int or String. Please check your input!")

def filter_period(weather_data, time_start, time_end):
    # Get the start and end index
    #print(time_start)
    start_index = max(0,weather_data.get_index_from_epoch_seconds(to_epoch_seconds(time_start)))
    #print(start_index)
    end_index = min(weather_data.get_index_from_epoch_seconds(weather_data.timeEnd), weather_data.get_index_from_epoch_seconds(to_epoch_seconds(time_end)))
    for lwd in weather_data.locationWeatherData:
        lwd.data = lwd.data[start_index:end_index]
    # Adjust timeStart and timeEnd
    weather_data.timeStart = weather_data.timeStart + (start_index * weather_data.interval)
    weather_data.timeEnd = weather_data.timeStart + (end_index * weather_data.interval)
    return weather_data

def filter_params(weather_data, params):
    #print(params)
    include_columns_indexes = []
    for param in params:
        try:
            include_columns_indexes.append(weather_data.weatherParameters.index(param))
        except ValueError:
            pass
    for lwd in weather_data.locationWeatherData:
        # Transpose the matrix
        # Referring to this: https://stackoverflow.com/questions/8421337/rotating-a-two-dimensional-array-in-python
        data_transposed = list(zip(*lwd.data, strict=True))
        #print(data_transposed)
        filtered_data_transposed = []
        for include_column_index in include_columns_indexes:
            filtered_data_transposed.append(data_transposed[include_column_index])
        lwd.data = list(zip(*filtered_data_transposed))
        lwd.length = len(lwd.data)
    # Adjust parameters index
    weather_data.weatherParameters = [weather_data.weatherParameters[include_column_index] for include_column_index in include_columns_indexes ]
    return weather_data