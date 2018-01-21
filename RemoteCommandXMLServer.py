from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import sys
import RemoteCommandInclude
import subprocess


# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


def run_command(command, *args):
    command_to_run = [command]
    command_args = list(args)
    sys.__stderr__.write('args: {}\n\n'.format(args))
    if args and type(args) == str:
        sys.__stderr__.write('Type is string.\n')
        command_args = list(args)
    sys.__stderr__.write('args: {}\n'.format(command_args))
    command_to_run.extend(command_args)
    p = subprocess.Popen(command_to_run, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, errors = p.communicate(timeout=60)
    if output:
        return str(output, 'utf-8')
    else:
        return 'Error: {}'.format(errors)

# Create server
with SimpleXMLRPCServer(("localhost", RemoteCommandInclude.REMOTECOMMANDPORT),
                        requestHandler=RequestHandler) as server:
    server.register_introspection_functions()

    # Register pow() function; this will use the value of
    # pow.__name__ as the name, which is just 'pow'.
    server.register_function(pow)

    # Register a function under a different name
    def adder_function(x, y):
        return x + y
    server.register_function(adder_function, 'add')

    # Register an instance; all the methods of the instance are
    # published as XML-RPC methods (in this case, just 'mul').
    class MyFuncs:
        def mul(self, x, y):
            return x * y

    server.register_instance(MyFuncs())

    server.register_function(run_command,
                             'run_command')

    sys.stdout.write("Starting to serve forever...\n\n")
    # Run the server's main loop
    server.serve_forever()
