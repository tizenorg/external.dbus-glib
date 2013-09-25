Name:       dbus-glib
Summary:    GLib bindings for D-Bus
Version:    0.100
Release:    4
Group:      System/Libraries
License:    AFL/GPL
URL:        http://www.freedesktop.org/software/dbus/
Source0:    http://dbus.freedesktop.org/releases/dbus-glib/dbus-glib-%{version}.tar.gz
Source1001:	%{name}.manifest
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  libtool
BuildRequires:  expat-devel
BuildRequires:  gettext-tools
BuildRequires:  autoconf

%description
D-Bus add-on library to integrate the standard D-Bus library with
the GLib thread abstraction and main loop.

%package devel
Summary:    Libraries and headers for the D-Bus GLib bindings (Developement)
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
Headers and static libraries for the D-Bus GLib bindings (Developement)

%prep
%setup -q

%build
cp %{SOURCE1001} .
%configure --disable-static \
    --disable-tests \
    --enable-verbose-mode=yes \
    --disable-gtk-doc

make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install
rm -rf $RPM_BUILD_ROOT/usr/share/man
rm -rf $RPM_BUILD_ROOT/usr/share/gtk-doc

# don't care about bash completion in a consumer device
rm -rf $RPM_BUILD_ROOT/etc/bash_completion.d/dbus-bash-completion.sh
rm -rf $RPM_BUILD_ROOT/usr/libexec/dbus-bash-completion-helper

mkdir -p $RPM_BUILD_ROOT%{_datadir}/license
for keyword in LICENSE COPYING COPYRIGHT;
do
	for file in `find %{_builddir} -name $keyword`;
	do
		cat $file >> $RPM_BUILD_ROOT%{_datadir}/license/%{name};
		echo "";
	done;
done

# license
mkdir -p %{buildroot}/usr/share/license
cp COPYING %{buildroot}/usr/share/license/%{name}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%{_datadir}/license/%{name}
%{_libdir}/*glib*.so.*
/usr/share/license/%{name}

%files devel
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/dbus-glib-1.pc
%{_includedir}/dbus-1.0/dbus/*
%{_bindir}/dbus-binding-tool

