# WeatherData
This is a module that can be used for Python scripts and applications working with weather data in the IPM Decisions format

## How to install this package
To install the latest stable version, use this command

```python
pip install git+https://github.com/H2020-IPM-Decisions/WeatherData.git@main
```

To install a specific version, use this command, where the `v1.0.0` is one of the available tags

```bash
pip install git+https://github.com/H2020-IPM-Decisions/WeatherData.git@v1.0.0
```

## How to build a PyPi package
We used [these instructions](https://spike.sh/blog/how-to-create-a-pip-package-for-python/)

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
