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
from .weatherdata_utils import *

class WeatherData:
    """Represents weather data in the IPM Decisions format"""
    def __init__(self, *args, **kwargs):
        # Get the times
        self.timeStart = to_epoch_seconds(kwargs.get("timeStart", None))
        self.timeEnd = to_epoch_seconds(kwargs.get("timeEnd", None))
        self.interval = kwargs.get("interval", 3600)
        self.weatherParameters = kwargs.get("weatherParameters", None)
        self.locationWeatherData = []
        lwd_tmp = kwargs.get("locationWeatherData", [])
        if len(lwd_tmp) > 0:
            for lwd in lwd_tmp:
                self.locationWeatherData.append(LocationWeatherData(**lwd) if not isinstance(lwd, LocationWeatherData) else lwd)
             
    def set_value(self, parameter:int, timestamp:int, value:float):
        """Assigns a value to a given parameter at the specified timestamp"""
        col = self.weatherParameters.index(parameter)
        row = int((timestamp - self.timeStart) / self.interval)
        self.locationWeatherData[0].data[row][col] = value

    def as_dict(self):
        """Get a dictionary representation of the object. Great for e.g. Flask apps"""
        retval = vars(self)
        retval["timeStart"] = None if self.timeStart is None else "%sZ" % datetime.utcfromtimestamp(self.timeStart).isoformat()
        retval["timeEnd"] = None if self.timeEnd is None else "%sZ" % datetime.utcfromtimestamp(self.timeEnd).isoformat()
        lwds_dict = []
        for lwd in self.locationWeatherData:
            lwds_dict.append(lwd.as_dict())
        retval["locationWeatherData"] = lwds_dict
        return retval

    def get_index_from_epoch_seconds(self, epoch_seconds:int):
        """In which row can I get data for this point in time?"""
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
