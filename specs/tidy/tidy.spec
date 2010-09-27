# $Id$
# Authority: dag

%define snap 20091203

Summary: Utility to clean up and pretty print HTML/XHTML/XML
Name: tidy
Version: 0.99.0
Release: 1.%{snap}%{?dist}
License: W3C
Group: Applications/Text
URL: http://tidy.sourceforge.net/

Source0: tidy-%{snap}cvs.tar.gz
Source10: tidy-cvs_checkout.sh
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: doxygen
BuildRequires: libtool
BuildRequires: libxslt
Requires: libtidy = %{version}-%{release}

%description
When editing HTML it's easy to make mistakes. Wouldn't it be nice if
there was a simple way to fix these mistakes automatically and tidy up
sloppy editing into nicely layed out markup? Well now there is! Dave
Raggett's HTML TIDY is a free utility for doing just that. It also
works great on the atrociously hard to read markup generated by
specialized HTML editors and conversion tools, and can help you
identify where you need to pay further attention on making your pages
more accessible to people with disabilities.

%package -n libtidy
Summary: Shared libraries for %{name}
Group: System Environment/Libraries

%description -n libtidy
When editing HTML it's easy to make mistakes. Wouldn't it be nice if
there was a simple way to fix these mistakes automatically and tidy up
sloppy editing into nicely layed out markup? Well now there is! Dave
Raggett's HTML TIDY is a free utility for doing just that. It also
works great on the atrociously hard to read markup generated by
specialized HTML editors and conversion tools, and can help you
identify where you need to pay further attention on making your pages
more accessible to people with disabilities.

%package -n libtidy-devel
Summary: Header files, libraries and development documentation for libtidy.
Group: Development/Libraries
Provides: tidy-devel = %{version}-%{release}
Requires: libtidy = %{version}-%{release}

%description -n libtidy-devel
This package contains the header files, static libraries and development
documentation for libtidy. If you like to develop programs using libtidy,
you will need to install libtidy-devel.

%prep
%setup -n %{name}
sh build/gnuauto/setup.sh

%build
%configure \
    --disable-static \
    --disable-dependency-tracking
%{__make} %{?_smp_mflags}

### api docs
doxygen htmldoc/doxygen.cfg

### make doc steps gleaned from build/gmake/Makefile
pushd htmldoc
../console/tidy -xml-config >tidy-config.xml
../console/tidy -xml-help   >tidy-help.xml
xsltproc -o tidy.1 tidy1.xsl tidy-help.xml
xsltproc -o quickref.html quickref-html.xsl tidy-config.xml
popd

%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR="%{buildroot}"

%{__install} -Dp -m0644 htmldoc/tidy.1 %{buildroot}%{_mandir}/man1/tidy.1

%clean
%{__rm} -rf %{buildroot}

%post -n libtidy -p /sbin/ldconfig
%postun -n libtidy -p /sbin/ldconfig

%files
%defattr(-, root, root, 0755)
%doc htmldoc/*.html htmldoc/*.css htmldoc/*.gif
%doc %{_mandir}/man1/tidy.1*
%{_bindir}/tab2space
%{_bindir}/tidy

%files -n libtidy
%defattr(-, root, root, 0755)
%{_libdir}/libtidy-0.99.so.0*

%files -n libtidy-devel
%defattr(-, root, root, 0755)
%doc htmldoc/api/*
%{_includedir}/*.h
%{_libdir}/libtidy.so
%exclude %{_libdir}/libtidy.la

%changelog
* Thu Sep 23 2010 Dag Wieers <dag@wieers.com> - 0.99.0-1
- Initial package. (based on fedora)