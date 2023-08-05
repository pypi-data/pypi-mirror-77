# YTKD

### ytkd-api is sponsored by:	
<a href="https://www.developingnow.com/"><img src="https://github.com/alinisarhaider/ytkd_api/blob/master/developingco_logo.png?raw=true"/></a>

## Description
A YouTube key word detection API that takes in video URL and key words and outputs each key word along with its time of occurrence in the video.

## Installation

Download using pip via pypi.

```bash
$ pip install ytkd-api
```

## Getting started

Import YTKD:

```python
>>> from ytkd-api import YTKD
```
Assign data.
```python
>>> url = 'https://www.youtube.com/watch?v=vW9edcLqND0'
>>> keywords = 'and, to'
```

Create an object of YTKD.
```python
>>> ytkd = YTKD(url=url, keywords=keywords)
```
Get the expected processing time.
```python
>>> ytkd.get_expected_time() # returns the expected time in minutes e.g. 5
```
Get the results for the given keywords.
```python
>>> ytkd.get_results() # returns the results in form of a dictionary of type {str: list}
```