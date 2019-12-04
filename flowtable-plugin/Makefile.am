# Copyright (c) 2017 Cisco and/or its affiliates.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

AUTOMAKE_OPTIONS = foreign subdir-objects
AM_CFLAGS = -Wall -Wextra -I@TOOLKIT_INCLUDE@

flowtable_plugin_la_CFLAGS = -DDEBUG -g

CFLAGS += -DDEBUG -g

# if VPP_ROOT is set, use it to compile
# eg. VPP_ROOT=~/vpp/build-root/install-vpp-native
if VPP_ROOT
CFLAGS += -I$(VPP_ROOT)/vpp/include
LDFLAGS += -L$(VPP_ROOT)/vpp/lib64

VPPAPIGEN = $(VPP_ROOT)/vpp/bin/vppapigen
else
VPPAPIGEN = vppapigen
endif

lib_LTLIBRARIES = flowtable_plugin.la
flowtable_plugin_la_SOURCES = \
    flowtable/api.c \
    flowtable/flowtable.c \
    flowtable/flowtable_node.c \
    flowtable/nodes_registration.c

nobase_include_HEADERS = \
	flowtable/flowtable.h \
	flowtable/flowdata.h \
	flowtable/flowtable.api.h

flowtable_plugin_la_LDFLAGS = -module

SUFFIXES = .api.h .api .api.json

%.api.h: %.api
	mkdir -p `dirname $@` ;                          \
	vppapigen --input $^ --output $@ --outputdir=flowtable

%.api.json: %.api
	@echo "  JSON APIGEN  " $@ ;                     \
	mkdir -p `dirname $@` ;                          \
	vppapigen --input $^ JSON --output $@ --outputdir=flowtable

apidir = $(prefix)/api/plugins
apiincludedir = ${includedir}/vpp_plugins
api_DATA = \
	$(patsubst %.api,%.api.json,$(API_FILES))

BUILT_SOURCES = \
	$(patsubst %.api,%.api.h,$(API_FILES))

install-data-hook:
	mkdir $(libdir)/vpp_plugins || true
	cp $(libdir)/flowtable_plugin.so.*.*.* $(libdir)/vpp_plugins/flowtable_plugin.so
	rm -f $(libdir)/flowtable_plugin.*

CLEANFILES = $(BUILT_SOURCES)
