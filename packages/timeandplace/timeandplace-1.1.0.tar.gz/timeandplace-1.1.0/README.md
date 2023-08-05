# TimeAndPlace API & CLI Application 
[![](https://img.shields.io/pypi/v/timeandplace)](https://pypi.org/project/timeandplace/) ![](https://img.shields.io/pypi/l/timeandplace) ![](https://img.shields.io/pypi/implementation/timeandplace)

This repo contains both a Python3 API, and a command-line application for interacting with [@salamander2](https://github.com/salamander2)'s [TimeAndPlace](https://github.com/salamander2/TimeAndPlace) service over a network. The main reason behind this package is for use in another project I have planned for room occupancy tracking.

## What kind of data can be accessed?

Currently, this is mostly a Read-Only API. The following data can be accessed when logged in:
 - List of all student IDs
 - A particular student's info
 - Student location tracking **\***

**\*** This data can be written via the API

## CLI usage

The command-line app uses "action commands" in the format of:

```sh
timeandplace --username <username> --password <password> <action> [optional: --endpoint <url>]
```

A list of possible actions can be viewed by running:

```sh
timeandplace help
```

## API usage

All interaction is done via the `TimeAndPlace` object. It has the following methods:

```python
client = TimeAndPlace()
client.login(str, str)

# These require login to be called
client.getStudentInfo(int) -> StudentInfo
client.getAllStudents() -> List[int]
client.getAllCourses() -> List[CourseInfo]
client.signInStudentToTerminal(int, int)
client.signOutStudentFromTerminal(int, int)
```

I recommend taking a look at the [single source file](https://github.com/Ewpratten/timeandplace-api/blob/master/timeandplace/__init__.py) for more info on the API.