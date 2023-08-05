# yyutils: provide some python tools which often used
<br>
All tools are be provided as decorators.

## Installation

Not provide using `pip` install yet.

## Usage

### Counter

A decorator to count the number of times the function is called.

```
from yyutils import Counter

@Counter
def foo(*args,**kwargs):
    pass
```

### Timer

A decorator to calculate function execution time.

```
from yyutils import Timer

@Timer
def foo(*args,**kwargs):
    pass
```

### Retry_timer

A decorator to help if function execution fail, how many times will retry and what is the retry interval.

```
from yyutils import Retry_timer

@Retry_timer()
def foo(*arg,**kwargs):
    pass
```

with parameters:
```
@Retry_timer(interval=1, retry_times=10)
def foo(*arg,**kwargs):
    pass
```

### Schedule

A decorator to schedule the function execution time.

```
from yyutils import Schedule

@Schedule()
def foo(*arg,**kwargs):
    pass
```

with parameters:
```
@Schedule(interval=10)
def foo(*arg,**kwargs):
    pass
```

### Error_Log

A decorator for logging Exception but not stop the program.

```
from yyutils import Error_Log

@Error_Log
def foo(*args,**kwargs):
    pass
```

### TypePrints

A decorator for print func.__doc__ like type prints.

```
from yyutils import TypePrints

@TypePrints
def foo(*args,**kwargs):
    pass
```
