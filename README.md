# ipmd_weatherdata
This is a module that can be used for Python scripts and applications working with weather data in the [IPM Decisions format](https://github.com/H2020-IPM-Decisions/WeatherService/blob/develop/docs/weather_service.md)

## How to install this package
To install the latest stable version, use this command

```python
pip install git+https://github.com/H2020-IPM-Decisions/WeatherData.git@main
```

To install a specific version, use this command, where the `v1.3.0` is one of the available tags

```bash
pip install git+https://github.com/H2020-IPM-Decisions/WeatherData.git@v1.3.0
```

To add this to requirements.txt, simply add this line:
```bash
git+https://github.com/H2020-IPM-Decisions/WeatherData.git@v1.3.0
```

## Usage
```python
from ipmd_weatherdata import WeatherData, weatherdata_utils

# Initialize the WeatherData object
wd_file = open("../data_files/2021_apelsvoll_redigert.json")
weather_data = WeatherData(**json.load(wd_file))
wd_file.close()

# Filter by period
time_start = "2021-01-01"
time_end = "2021-02-01"
weather_data = weatherdata_utils.filter_period(weather_data,time_start,time_end)

# Filter by parameters
parameters = [1002,2001]
weather_data = weatherdata_utils.filter_params(weather_data, parameters)

```

## How to create a PyPi package
We used [these instructions](https://spike.sh/blog/how-to-create-a-pip-package-for-python/)

Build command:
```bash
$ python3 -m build
```

In addition: How to tag a commit in a branch:
```bash 
$ git tag -a v1.0.0 -m "v1.0.0, first release to prod"
$ git push origin --tags
Enumerating objects: 1, done.
Counting objects: 100% (1/1), done.
Writing objects: 100% (1/1), 180 bytes | 180.00 KiB/s, done.
Total 1 (delta 0), reused 0 (delta 0), pack-reused 0
To github.com:H2020-IPM-Decisions/WeatherData.git
 * [new tag]         v1.0.0 -> v1.0.0
```
