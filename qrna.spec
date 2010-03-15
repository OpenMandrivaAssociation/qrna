%define name	qrna
%define version	2.0.3c
%define rel	5
%define release	%mkrel %{rel}

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	Prototype ncRNA genefinder
Group:		Sciences/Biology
License:	GPL
URL:		http://selab.janelia.org/software.html#qrna
Source:		ftp://selab.janelia.org/pub/software/%{name}-%{version}.tar.bz2
Patch:		fix_getline.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}

%description
QRNA uses comparative genome sequence analysis to detect 
conserved RNA secondary structures, including both ncRNA genes 
and cis-regulatory RNA structures.

%prep
%setup -q
%patch
chmod 644  Licenses/*

%build
# squid library
(cd squid && %make CFLAGS="$RPM_OPT_FLAGS")
(cd squid02 && %make CFLAGS="$RPM_OPT_FLAGS")

# qrna
(cd src && %make CFLAGS="$RPM_OPT_FLAGS")

%install
rm -rf %{buildroot}

# executables
install -d -m 755 %{buildroot}%{_bindir}
install -m 755 src/{main,cfgbuild,eqrna,eqrna_sample,shuffle,rnamat_main} %{buildroot}%{_bindir}
install -m 755 scripts/* %{buildroot}%{_bindir}

# data
install -d -m 755 %{buildroot}%{_datadir}/%{name}
install -m 644 lib/* %{buildroot}/%{_datadir}/%{name}

# configuration
install -d -m 755 %{buildroot}%{_sysconfdir}/profile.d
echo "export QRNADB=%{_datadir}/%{name}" > %{buildroot}%{_sysconfdir}/profile.d/%{name}.sh
echo "setenv QRNADB %{_datadir}/%{name}" > %{buildroot}%{_sysconfdir}/profile.d/%{name}.csh

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc 00README INSTALL Licenses/* documentation/userguide.pdf
%{_bindir}/*
%{_datadir}/%{name}
%config(noreplace) %{_sysconfdir}/profile.d/*


