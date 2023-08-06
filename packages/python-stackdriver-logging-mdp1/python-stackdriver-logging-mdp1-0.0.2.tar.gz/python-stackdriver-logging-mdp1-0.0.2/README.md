
# Logging library for Python using Stackdriver

## Reference for good logging
[here](https://fangpenlin.com/posts/2012/08/26/good-logging-practice-in-python/)
Check out 'Write logging records everywhere with a proper level' section 


## To use logging:
1. Copy logging.yaml and stackdriver.py into the project you want to use
2. In order to import the logger, 'from stackdriver import stackdriver_logger' 
3. In order to initialize the logger, 'mdp_logger = stackdriver_logger()'
4. In order to use the logger, 'mdp_logger.info('shows up on stackdriver and console')'

## Logging Levels in current configuration (set in logging.yaml)
 - debug: lowest level and logs of these kinds don't show up as of current configuration
 - info: info logs will show up on stdout and in stackdriver
 - warning: warn logs will show up on stdout and in stackdriver
 - error: error logs will show up on stdout and in stackdrtiver
 - critical: critical logs will show up on stdout and in stackdriver

## Change log level that shows up in Stackdriver
In logging.yaml, under handlers:stackdriver, change the level field to the lowest level you want to see in stackdriver.
Anything that level and higher will now show up.

## Change log level that shows up on console
In logging.yaml, under handlers:console, change the level field to the lowest level you want to see show up in console.
Anything that level and higher will now show up.