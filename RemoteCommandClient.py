import xmlrpc.client
import RemoteCommandInclude


class RemoteCommands:
    def __init__(self, remote_ip='localhost', remote_port=RemoteCommandInclude.REMOTECOMMANDPORT):
        self.s = xmlrpc.client.ServerProxy('http://{}:{}'.format(remote_ip,
                                                                 remote_port))
