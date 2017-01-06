#!/bin/env python
'''
To be used with flowtable-env-setup.sh network.
Direct all traffic through the flowtable, and then the test portmirroring node.
'''
from __future__ import print_function

import os
import fnmatch

from vpp_papi import VPP


vpp_json_dir = '/usr/share/vpp/api/'

jsonfiles = []
for root, dirnames, filenames in os.walk(vpp_json_dir):
    for filename in fnmatch.filter(filenames, '*.api.json'):
        jsonfiles.append(os.path.join(vpp_json_dir, filename))

if not jsonfiles:
    print('Error: no json api files found')
    exit(-1)

vpp = VPP(jsonfiles)

if_1_name = 'tap-0'
if_2_name = 'tap-1'
if_3_name = 'tap-2'

r = vpp.connect('papi')
print(r)

if_1_sw_if_index = vpp.sw_interface_dump(name_filter_valid=1, name_filter=if_1_name)[0].sw_if_index
if_2_sw_if_index = vpp.sw_interface_dump(name_filter_valid=1, name_filter=if_2_name)[0].sw_if_index
if_3_sw_if_index = vpp.sw_interface_dump(name_filter_valid=1, name_filter=if_3_name)[0].sw_if_index

# add port-mirroring as available flowtable next node
r = vpp.add_node_next(node_name='flowtable-process', next_name='pm-hit')
print(r)
portmirroring_index = r.node_index

# configure portmirroring
r = vpp.pm_conf(dst_interface=if_3_sw_if_index, is_del=0)
print(r)

# hook on the first interface
# leave flows_max untouched
r = vpp.flowtable_conf(flows_max=0xffffffff,
                       sw_if_index=if_1_sw_if_index,
                       next_node_index=portmirroring_index,
                       enable_disable=0)
print(r)

# hook on the second interface
# leave flows_max untouched
r = vpp.flowtable_conf(flows_max=0xffffffff,
                       sw_if_index=if_2_sw_if_index,
                       next_node_index=portmirroring_index,
                       enable_disable=0)
print(r)

exit(vpp.disconnect())
