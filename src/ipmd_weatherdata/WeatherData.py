#!/usr/bin/python3

#    Copyright (C) 2022  Tor-Einar Skog,  NIBIO
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

from datetime import datetime

# This is test documentation
class WeatherData:
    def __init__(self, *args, **kwargs):
        # Get the times
        self.timeStart = WeatherData.to_epoch_seconds(kwargs.get("timeStart", None))
        self.timeEnd = WeatherData.to_epoch_seconds(kwargs.get("timeEnd", None))
        self.interval = kwargs.get("interval", 3600)
        self.weatherParameters = kwargs.get("weatherParameters", None)
        self.locationWeatherData = []
        lwd_tmp = kwargs.get("locationWeatherData", [])
        if len(lwd_tmp) > 0:
            for lwd in lwd_tmp:
                self.locationWeatherData.append(LocationWeatherData(**lwd) if not isinstance(lwd, LocationWeatherData) else lwd)
         
    @classmethod
    def to_epoch_seconds(self,some_kind_of_date):
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
        
    def set_value(self, parameter, timestamp, value):
        col = self.weatherParameters.index(parameter)
        row = int((timestamp - self.timeStart) / 3600)
        self.locationWeatherData[0].data[row][col] = value

    def as_dict(self):
        retval = vars(self)
        retval["timeStart"] = None if self.timeStart is None else "%sZ" % datetime.utcfromtimestamp(self.timeStart).isoformat()
        retval["timeEnd"] = None if self.timeEnd is None else "%sZ" % datetime.utcfromtimestamp(self.timeEnd).isoformat()
        lwds_dict = []
        for lwd in self.locationWeatherData:
            lwds_dict.append(lwd.as_dict())
        retval["locationWeatherData"] = lwds_dict
        return retval

    # In which row can I get data for this point in time?
    def get_index_from_epoch_seconds(self, epoch_seconds):
        if epoch_seconds % 1 != 0:
            # Check that epoch_seconds is int
            raise ValueError("Timestamp %s is not an integer" % epoch_seconds)
        # Check that return value is an int
        index = (epoch_seconds - self.timeStart) / self.interval
        if index %1 != 0:
            raise ValueError("Timestamp %s is not divisible by %s" % (epoch_seconds,self.timeStart))
        return int(index)


class Parameter:
    #/** Method for how to create e.g. daily values from hourly values */
    AGGREGATION_TYPE_AVERAGE = "AVG";
    #    /** Method for how to create e.g. daily values from hourly values */
    AGGREGATION_TYPE_MINIMUM = "MIN";
    #    /** Method for how to create e.g. daily values from hourly values */
    AGGREGATION_TYPE_MAXIMUM = "MAX";
    #    /** Method for how to create e.g. daily values from hourly values */
    AGGREGATION_TYPE_SUM = "SUM";

class LocationWeatherData:
    def __init__(self, *args, **kwargs):
        self.altitude = kwargs.get("altitude", None)
        self.longitude = kwargs.get("longitude", None)
        self.latitude = kwargs.get("latitude", None)
        self.qc = kwargs.get("qc", None)
        self.data = kwargs.get("data",[])


    def as_dict(self):
        retval = vars(self)
        # Add location weather data
        return retval 


## UTIL methods
def filter_period(weather_data, time_start, time_end):
    # Get the start and end index
    #print(time_start)
    start_index = max(0,weather_data.get_index_from_epoch_seconds(WeatherData.to_epoch_seconds(time_start)))
    #print(start_index)
    end_index = min(weather_data.get_index_from_epoch_seconds(weather_data.timeEnd), weather_data.get_index_from_epoch_seconds(WeatherData.to_epoch_seconds(time_end)))
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