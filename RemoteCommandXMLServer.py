from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import sys
import RemoteCommandInclude
import subprocess
import argparse


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


def main():
    # Create server
    with SimpleXMLRPCServer((args.server_ip, args.port),
                            requestHandler=RequestHandler) as server:

        server.register_function(run_command,
                                 'run_command')

        sys.stdout.write("Starting to serve forever...\n\n")
        # Run the server's main loop
        server.serve_forever()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--server_ip', help="IP to use for the server.", default='localhost')
    parser.add_argument('-p', '--port', help="Port to bind to.", default=RemoteCommandInclude.REMOTECOMMANDPORT)
    args = parser.parse_args()
