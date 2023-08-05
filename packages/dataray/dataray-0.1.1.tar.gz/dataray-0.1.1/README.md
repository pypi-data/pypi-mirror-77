# DataRay

DataRay is a class of decorators helping detect the metadata of the data.

The motivation of this package is to help understand how your api request data looks like. Normally we can directly
check how the api request looks like via some UI platform such as postman etc. With this package, user may directly
get the data structure and some basic metadata of the requested data

## Features
* Json Structure
* Further feature coming soon


## Detect the Json Structure

```python
# here is your customer request function. Now it is supposed to return list or dict you are interested in looking into
from dataray import dataray

@ dataray.ray
def request_func(*args, **kwargs):
    ...
```
Then every time calling `request_func`, the json structure will be printed out.