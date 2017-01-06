%define _name   vpp-flowtable-plugin
%define _plugin flowtable-plugin

Name: %{_name}
Summary: Vector Packet Processing
License: Apache
Version: %{_version}
Release: %{_release}
Requires: vpp vpp-dev
Source0: %{_name}-%{version}.tar.gz

%description
This package provides an flowtable plugin for vpp

%package devel
Summary: VPP header files, static libraries
Group: Development/Libraries
Requires: vpp-flowtable-plugin = %{_version}-%{_release}, vpp-dev

%description devel
This package contains the headers for C bindings for the vpp-flowtable-plugin

%define debug_package %{nil}

%prep
%setup -q
pushd %{_plugin}
autoreconf -i
popd

%build
pushd %{_plugin}
%configure
make
popd

%install
#
# vpp-flowtable-plugin
#
mkdir -p -m755 %{buildroot}%{_libdir}/vpp_plugins
install -m 644 %{_plugin}/.libs/flowtable_plugin.so %{buildroot}%{_libdir}/vpp_plugins/flowtable_plugin.so

mkdir -p -m755 %{buildroot}/usr/share/vpp/api/
install -p -m 644 %{_plugin}/flowtable/flowtable.api.json %{buildroot}/usr/share/vpp/api/flowtable.api.json

#
# vpp-flowtable-plugin-devel
#
mkdir -p -m755 %{buildroot}%{_includedir}/flowtable/
install -m 644 %{_plugin}/flowtable/flowdata.h %{buildroot}%{_includedir}/flowtable/flowdata.h
install -m 644 %{_plugin}/flowtable/flowtable.h %{buildroot}%{_includedir}/flowtable/flowtable.h
install -m 644 %{_plugin}/flowtable/flowtable.api.h %{buildroot}%{_includedir}/flowtable/flowtable.api.h


%files
%defattr(-,bin,bin)
%{_libdir}/vpp_plugins/flowtable_plugin.so
/usr/share/vpp/api/flowtable.api.json

%files devel
%defattr(-,bin,bin)
%{_includedir}/flowtable/*
