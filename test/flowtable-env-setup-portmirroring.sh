#!/bin/bash
#
# set up a network env with 3 namespaces:
#
# [ vpp1 ]------[vpp]------[ vpp2 ]
#                 |
#              [ vpp3 ]
#
# vpp1: 192.168.0.1
# vpp2: 192.168.0.2
# vpp3: 192.168.1.1

for i in `seq 1 3`
do
    ip netns delete vpp$i
    ip netns add vpp$i
    vppctl tap connect vpp$i
    vppctl set interface state tap-$(($i - 1)) up
    ip link set dev vpp$i netns vpp$i
    ip netns exec vpp$i ip link set vpp$i up
done

vppctl set interface l2 bridge tap-0 23
vppctl set interface l2 bridge tap-1 23

ip netns exec vpp1 ip addr add 192.168.0.1/24 dev vpp1
ip netns exec vpp2 ip addr add 192.168.0.2/24 dev vpp2

vppctl set int l3 tap-2
vppctl set int ip addr tap-2 192.168.1.1/24

# test
ip netns exec vpp1 ping -c1 192.168.0.2
ip netns exec vpp2 ping -c1 192.168.0.1
