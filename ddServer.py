# Start a TCP/IP Listener on the hard coded HOST and PORT
# Messages sent from a connected client must end with a '#' character
# The message format is shown in the usage text.

from datadog import initialize
from datadog import api
from datadog import statsd
import shlex
import sys
import SocketServer

options = {
    'api_key':'b6f16719fd3a231f6dd3375280234328',
    'app_key':'b541de66b524d9d96390e14cc734a8a508269093'
}

initialize(**options)

usage = """
Usage:
i key		[increment key]
d key 		[decrement key]
g key value  	[guage key value]
e title text tags
"""

def main(x):
	HOST, PORT =  "", 9999 # listen on any IP interface
	server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
	server.serve_forever()

class MyTCPHandler(SocketServer.BaseRequestHandler):
	"""
	The RequestHandler class for our server.

	It is instantiated once per connection to the server, and must
	override the handle() method to implement communication to the
	client.
	"""
	def handle(self):
		# self.request is the TCP socket connected to the client
		self.data = ""
		for  i in range (200):
			c= self.request.recv(1)
			#~ print c
			if c == '#':
				break
			self.data += c

		#~ print "{} send:".format(self.client_address[0]), self.data)
		if DataDogCmd(self.data.strip()):
			self.request.sendall("ok")
		else:
			self.request.sendall("fa")

def DataDogCmd(cmd):
	args = shlex.split(cmd)
	print args
	if len(args) < 2:
		print usage
		return False
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
		return False

	return True

if __name__ == '__main__':
    main(sys.argv[1:])
