# This is the datadog exaample python with a main added so you can manually send stuff to datadog
from datadog import initialize
import sys

# These are specific to the user account on datadog
options = {
    'api_key':'b6f16719fd3a231f6dd3375280234328',
    'app_key':'b541de66b524d9d96390e14cc734a8a508269093'
}

initialize(**options)

# Use Datadog REST API client
from datadog import api

#~ title = "Something big happened!"
#~ text = 'And let me tell you all about it here!'
#~ tags = ['version:1', 'application:web']

#~ api.Event.create(title=title, text=text, tags=tags)


# Use Statsd, a Python client for DogStatsd
from datadog import statsd

#~ statsd.increment('MyAppCount')
#~ statsd.gauge('LifeEtc', 42)

# Or ThreadStats, an alternative tool to collect and flush metrics, using Datadog REST API
#~ from datadog import ThreadStats
#~ stats = ThreadStats()
#~ stats.start()
#~ stats.increment('home.page.hits')

usage = """
Usage:
i key		[increment key]
d key 		[decrement key]
g key value  	[guage key value]
e title text tags
"""

def main(args):

	if len(args) < 2:
		print usage
	elif args[0] == 'i':
		statsd.increment(args[1])
	elif args[0] == 'd':
		statsd.decrement(args[1])
	elif args[0] == 'g':
		statsd.gauge(args[1], float(args[2]))
	elif args[0] == 'e':
		api.Event.create(title=args[1], text=args[2], tags=args[3])
	else:
		print usage


if __name__ == '__main__':
	main(sys.argv[1:])

