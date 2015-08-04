%define		plugin		discussion
%define		php_min_version 5.0.0
%include	/usr/lib/rpm/macros.php
Summary:	DokuWiki plugin: Add a comments section to Wiki pages
Name:		dokuwiki-plugin-%{plugin}
Version:	20150517
Release:	1
License:	GPL v2
Group:		Applications/WWW
Source0:	https://github.com/dokufreaks/plugin-%{plugin}/tarball/master/%{plugin}-%{version}.tar.gz
# Source0-md5:	3dcff9016981f572bc6a983641535a83
URL:		https://www.dokuwiki.org/plugin:discussion
BuildRequires:	rpm-php-pearprov >= 4.4.2-11
BuildRequires:	rpmbuild(macros) >= 1.520
Requires:	dokuwiki >= 20061106
Requires:	php(core) >= %{php_min_version}
Requires:	php(pcre)
Requires:	php(session)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		dokuconf	/etc/webapps/dokuwiki
%define		dokudir		/usr/share/dokuwiki
%define		plugindir	%{dokudir}/lib/plugins/%{plugin}
%define		find_lang 	%{_usrlibrpm}/dokuwiki-find-lang.sh %{buildroot}

# no pear deps
%define		_noautopear	pear

# exclude optional php dependencies
%define		_noautophp	php-someext

# put it together for rpmbuild
%define		_noautoreq	%{?_noautophp} %{?_noautopear}

%description
The Discussion Plugin adds a discussion section after your wiki page
for user comments. This is useful to separate page content and the
discussion thereof and also, if you don't want to give normal users
the right to edit the page but still want user contributed notes. A
second component of this plugin shows a list of all pages in a
namespace with a discussion section (called discussion threads)
ordered by most recent comments. This allows you to create a very
simple discussion forum in your wiki.

%prep
%setup -qc
mv *-%{plugin}-*/* .

version=$(awk '/^date/{print $2}' plugin.info.txt)
if [ "$(echo "$version" | tr -d -)" != %{version} ]; then
	: %%{version} mismatch
	exit 1
fi

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{plugindir}
cp -a . $RPM_BUILD_ROOT%{plugindir}
%{__rm} $RPM_BUILD_ROOT%{plugindir}/{COPYING,README}

%find_lang %{name}.lang

%clean
rm -rf $RPM_BUILD_ROOT

# use this post section if you package .css or .js files
%post
# force js/css cache refresh
if [ -f %{dokuconf}/local.php ]; then
	touch %{dokuconf}/local.php
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README
%dir %{plugindir}
%{plugindir}/*.css
%{plugindir}/*.js
%{plugindir}/*.php
%{plugindir}/*.txt
%{plugindir}/conf
%{plugindir}/images
%{plugindir}/syntax
