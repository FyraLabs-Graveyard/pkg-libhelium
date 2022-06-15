%define theme_version 1.2.4

Summary:        The Application Framework for tauOS apps
Name:           libhelium
Version:        1.0.0
Release:        6%{?dist}
License:        LGPLv2+
URL:            https://tauos.co
Source0:        https://github.com/tau-OS/libhelium/archive/refs/tags/%{version}.tar.gz
Source1:        https://github.com/tau-OS/tau-helium/archive/refs/tags/v%{theme_version}.tar.gz
# blueprint
Source2:        https://gitlab.gnome.org/jwestman/blueprint-compiler/-/archive/v0.2.0/blueprint-compiler-v0.2.0.tar.gz

BuildRequires:  sass
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  vala
BuildRequires:  valadoc
# Needed for wrap
BuildRequires:  git
BuildRequires:  pkgconfig(glib-2.0) >= 2.66.0
BuildRequires:  pkgconfig(gobject-introspection-1.0)
BuildRequires:  pkgconfig(gee-0.8)
BuildRequires:  pkgconfig(gtk4) >= 4.4

Requires: gtk4 >= 4.4
Requires: glib2 >= 2.66.0
Requires: libgee >= 0.20
Requires: tau-helium >= %{version}

%description
The Application Framework for tauOS apps

%package devel
Summary:        Development files for libhelium
Requires:       libhelium = %{version}-%{release}

%description devel
This package contains the libraries and header files that are needed
for writing applications with libhelium.

%package demo
Summary:        Demo app written with libhelium
Requires:       libhelium = %{version}-%{release}

%description demo
This package contains a demo app written with libhelium.

%package docs
Summary:        Documentation for libhelium
Requires:       libhelium = %{version}-%{release}

%description docs
This package contains the documentation for libhelium.

%prep
%autosetup

# extract the tarball
mkdir -p subprojects/tau-helium
tar -xvf %{SOURCE1} --strip-components=1 -C subprojects/tau-helium

mkdir -p subprojects/blueprint-compiler
tar -xvf %{SOURCE2} --strip-components=1 -C subprojects/blueprint-compiler

%build
%meson \
    -Ddemo=true \
    -Ddocumentation=true \
    --wrap-mode=default
%meson_build -j1

%install
# Install licenses
mkdir -p licenses
install -pm 0644 %SOURCE1 licenses/LICENSE
install -pm 0644 %SOURCE0 README.md
%meson_install

rm -rf %{buildroot}%{_bindir}/blueprint-compiler
rm -rf %{buildroot}%{_datadir}/themes/*

%files
%license licenses/LICENSE
%doc README.md
%{_libdir}/libhelium-1.0.so.1*
%{_libdir}/girepository-1.0

%files devel
%{_libdir}/libhelium-1.0.so*
%{_includedir}/*
%{_datadir}/gir-1.0/*
%{_libdir}/pkgconfig/*
%{_datadir}/vapi/*

%files demo
%{_bindir}/co.tauos.Helium1.Demo
%{_datadir}/applications/co.tauos.Helium1.Demo.desktop
%{_datadir}/icons/hicolor/*/apps/libhelium*.svg

%files docs
%{_docdir}/libhelium

%changelog
* Sat Jun 4 2022 Jamie Murphy <jamie@fyralabs.com> - 1.0-1
- Initial Release
