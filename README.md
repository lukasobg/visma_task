# Visma task

Run the file with one of
```
python main.py
python main.py --verbose
```

## Task Description


The task is to design two classes, one responsible for identifying
URI requests, and a client class that uses the first class.

URI requests are strings consisting of three parts: the scheme, the path, and the parameters.

An example and general format shown below.

visma-identity://login?source=severa
scheme://path?param1=value1&param2=value2&...

The above string must be parsed such that the scheme, path and parameters are extracted (splits by '://', '?', '&' and '=').

These attributes must then be validated. In other words
- the scheme must be 'visma-sign'
- the path must be one of 'login', 'confirm', 'sign' (=identification)
- the parameter values must be of certain types, e.g.
  - source: string
  - paymentnumber: integer

The RequestIdentifier class receives a URI-string as input, parses and validates it and stores the path and parameteres of the URI request. 

The path and parameters can be accessed/returned with getter functions.

The Client class initializes a RequestIdentifier instance, feeds it a URI-request,
'runs' the identifier, and finally stores the identified instance.

## Challenges and further improvements

The most challenging part for me was not knowing the context and making some guesses to what each class should do. I did not implement error handling, for example what
happens if an empty string is given as a URI request or the source parameter is missing from the parameter dictionary.
The concept of a client class was not that familiar for me but I think I got the idea.

Edge cases and error handling should be implemented. Similarly, the validation is implemented with True/False logic instead of potentially raising an error for invalid requests. Many of the prints here are as a demonstration of this code but they should probably be removed in production.

I used a little over 3 hours for the task.