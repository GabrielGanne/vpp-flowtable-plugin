# A flowtable plugin

Provide a stateful node with flow-level API, available for consecutive nodes or external applications.

## Objective

Provides a flowtable node to do flow classification, and associate a flow
context that can be enriched as needed by another node or an external
application.

The objective is to be adaptable so as to be used for any
stateful use such as load-balancing, firewall ...

Compared to the classifier, it stores a flow context, which changes the following:
* a flow context (which can be updated with external information)
* it can offload
* flows have a lifetime

## Sources
* vppsb : within flowtable directory
* github : https://github.com/GabrielGanne/vpp-flowtable

## Build
``` bash
cd <plugin-dir>

autoreconf -i -f
mkdir build && pushd build
../configure --prefix=/usr
make
sudo make install
popd
```

To build using vpp source tree instead of an installed one :
``` bash
export VPP_ROOT=~/vpp/build-root/install-vpp-native
...
../configure --prefix=$VPP_ROOT/vpp
# then build && install
```

## CLI
* configuration
```
 flowtable [max-flows <n>] [intf <name>] [next-node <name>] [disable]
```

The traffic from the given *intf* is redirected to the flowtable using vnet_hw_interface_rx_redirect_to_node()

## API
I used ~0 (or 0xff for u8) to leave configuration parameter unchanged.

* flowtable configuration
```
 flowtable_conf(flows_max, sw_if_index, next_node_index, enable_disable)
```
* send additional informations to the flowtable
```
 flowtable_update(is_ip4, ip_src, ip_dst, port_src, port_dst # used to compute flow key
                  lifetime, offloaded, infos) # additional flow informations
```

## Test

In itself, the flowtable only provides a context and an API.

I added a simple port-mirroring node to test with an external application receiving the mirrored traffic and updating the flowtable using the binary API.

### simple conf

2 scripts for quick flowtable test :

* ~/test/flowtable-env-setup.sh
    creates 2 connected namespaces vpp1 & vpp2
* ~/test/flowtable-api-conf.py
    redirect all traffic through the flowtable


### Perfs
Tested with handoff node, with two working nodes.

#### Platform
* Platform: Intel(R) Xeon(R) CPU E5-2697 v2 @ 2.70GHz, 30720 KB Cache

#### pktgen
* pktgen: gen 8k flows of 128 Bytes packets at ~7Gbps 2 interfaces
* modify flowtable to expire flows after each packet (flow ttl = 0)

show run max gives: avg Clocks = 211.0

About half of it to process the packet, and the other half to lookup the flow contexts.

#### Breaking Point
pktgen cannot create many flows, so I tested with BP to test the number of flow context creation per second
* Total BW: 12Gbps
* Max flows 2.4 M # Breaking Point flows (2.4M) != vpp flows (4M)
* avg pps : 750~800 k
* avg flow creation rate : 18k/s
* Max flow creation rate : 50k/s
* ~4.5% recycled flows

The flow count difference between Breaking Point and vpp flowtable's is caused by the timer management.

### portmirroring node
The node is only used as a sample to test the flowtable and has no value in itself.

## Current status

* Default behavior is to connect transparently to given interface.
* Can reroute packets to given node
* Can receive additional information
* Can offload sessions
* Only support IP packets
* if the maximum number of flows is reached, the flowtable will recycle a flow by expiring a flow which was about to expire (typically the first flow found in the timer-wheel's next-slot)

## Planned
* split flowtable into two ip4/ip6 nodes

## Main contributors

* Gabriel Ganne - gabriel.ganne@qosmos.com
* Christophe Fontaine - christophe.fontaine@qosmos.com (2016-07 ietf's hackathon : https://github.com/christophefontaine/flowtable-plugin)

