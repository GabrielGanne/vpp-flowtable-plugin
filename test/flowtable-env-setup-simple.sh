#!/bin/bash
#
# set up a network env with 2 namespaces:
#
# [ vpp1 ]------[vpp]------[ vpp2 ]
#
# vpp1: 192.168.0.1
# vpp2: 192.168.0.2

ip netns delete vpp1
ip netns delete vpp2
ip netns add vpp1
ip netns add vpp2

vppctl tap connect vpp1
vppctl tap connect vpp2
vppctl set interface state tap-0 up
vppctl set interface state tap-1 up
ip link set dev vpp1 netns vpp1
ip link set dev vpp2 netns vpp2
ip netns exec vpp1 ip link set vpp1 up
ip netns exec vpp2 ip link set vpp2 up

vppctl set interface l2 bridge tap-0 23
vppctl set interface l2 bridge tap-1 23

ip netns exec vpp1 ip addr add 192.168.0.1/24 dev vpp1
ip netns exec vpp2 ip addr add 192.168.0.2/24 dev vpp2

# smoke-test
ip netns exec vpp1 ping -c1 192.168.0.2
ip netns exec vpp2 ping -c1 192.168.0.1
