from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI


class LinuxRouter( Node ):
    "A Node with IP forwarding enabled."

    def config( self, **params ):
        super( LinuxRouter, self).config( **params )
        # Enable forwarding on the router
        self.cmd( 'sysctl net.ipv4.ip_forward=1' )
        self.cmd( 'sysctl -w net.mptcp.mptcp_enabled=0' )
        self.cmd( 'sysctl -w net.mptcp.mptcp_path_manager=fullmesh' )

    def terminate( self ):
        self.cmd( 'sysctl net.ipv4.ip_forward=0' )
        super( LinuxRouter, self ).terminate()

class NetworkTopo( Topo ):

    def build( self, **_opts ):

        defaultIP = '10.0.0.1/24'  # IP address for r0
        r0 = self.addNode( 'r0', cls=LinuxRouter, ip='10.0.0.1/24' )
        r1 = self.addNode( 'r1', cls=LinuxRouter, ip='10.0.1.1/24' )
        h1 = self.addNode( 'h1', cls=LinuxRouter, ip='10.0.0.100/24' )
        h2 = self.addNode( 'h2', cls=LinuxRouter, ip='10.0.2.100/24' )
        s1, s2, s3, s4 = [ self.addSwitch( s ) for s in ('s1', 's2', 's3', 's4') ]

        self.addLink( s1, h1, intfName2='h1-eth0',
                      params2={ 'ip' :  '10.0.0.100/24'} ) 
        self.addLink( s1, r0, intfName2='r0-eth0',
                      params2={ 'ip' : '10.0.0.1/24' } )
        self.addLink( s2, r0, intfName2='r0-eth1',
                      params2={ 'ip' : '10.0.2.1/24' } )
        self.addLink( s2, h2, intfName2='h2-eth0',
                      params2={ 'ip' : '10.0.2.100/24' } )

        self.addLink( s3, h1, intfName2='h1-eth1',
                      params2={ 'ip' :  '10.0.1.100/24'} )
        self.addLink( s3, r1, intfName2='r1-eth0',
                      params2={ 'ip' : '10.0.1.1/24' } )
        self.addLink( s4, r1, intfName2='r1-eth1',
                      params2={ 'ip' : '10.0.3.1/24' } )
        self.addLink( s4, h2, intfName2='h2-eth1',
                      params2={ 'ip' : '10.0.3.100/24' } )



def run():
    "Test linux router"
    topo = NetworkTopo()
    net = Mininet( topo=topo )  # controller is used by s1-s3
    net.start()
    info( '*** Routing Table on Router:\n' )
    info( net[ 'r0' ].cmd( 'route' ))

    net['h2'].cmd('ip route add 10.0.0.100 via 10.0.2.1 dev h2-eth0')
    net['h2'].cmd('ip route add 10.0.1.100 via 10.0.3.1 dev h2-eth1')
    net['h1'].cmd('ip route add 10.0.2.100 via 10.0.0.1 dev h1-eth0')
    net['h1'].cmd('ip route add 10.0.3.100 via 10.0.1.1 dev h1-eth1')

    net['h1'].cmd('tc qdisc add dev h1-eth0 root tbf rate 50mbit burst 1mbit latency 1ms')
    net['h1'].cmd('tc qdisc add dev h1-eth1 root tbf rate 50mbit burst 1mbit latency 1ms')
    net['h2'].cmd('tc qdisc add dev h2-eth0 root tbf rate 50Mbit burst 1mbit latency 1ms')
    net['h2'].cmd('tc qdisc add dev h2-eth1 root tbf rate 50mbit burst 1mbit latency 1ms')
    net['r0'].cmd('tc qdisc add dev r0-eth0 root tbf rate 50mbit burst 1mbit latency 1ms')
    net['r0'].cmd('tc qdisc add dev r0-eth1 root tbf rate 50mbit burst 1mbit latency 1ms')
    net['r1'].cmd('tc qdisc add dev r1-eth0 root tbf rate 50mbit burst 1mbit latency 1ms')
    net['r1'].cmd('tc qdisc add dev r1-eth1 root tbf rate 50mbit burst 1mbit latency 1ms')

    CLI( net )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    run()              
