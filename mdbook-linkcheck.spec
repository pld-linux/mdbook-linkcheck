Summary:	Utility to create modern online books from Markdown files
Summary(pl.UTF-8):	Narzędzie do tworzenia nowoczesnych książek online z plików Markdown
Name:		mdbook-linkcheck
Version:	0.7.7
Release:	1
License:	MPL v2.0
Group:		Applications/Text
#Source0Download: https://github.com/Michael-F-Bryan/mdbook-linkcheck/releases
Source0:	https://github.com/Michael-F-Bryan/mdbook-linkcheck/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	caeaad5d2675cdd76114f5074689f554
# cd mdbook-linkcheck-%{version}
# cargo vendor
# cd ..
# tar cJf mdbook-linkcheck-vendor-%{version}.tar.xz mdbook-linkcheck-%{version}/{vendor,Cargo.lock}
Source1:	%{name}-vendor-%{version}.tar.xz
# Source1-md5:	b932d6b28dc2fb0e5938393c4ccebca0
URL:		https://github.com/Michael-F-Bryan/mdbook-linkcheck
BuildRequires:	cargo
BuildRequires:	openssl-devel >= 1.1.1
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 2.004
BuildRequires:	rust
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	mdbook >= 0.4.0
Requires:	mdbook < 0.5
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
mdBook is a utility to create modern online books from Markdown files.

%description -l pl.UTF-8
mdBook to narzędzie do tworzenia nowoczesnych książek online z plików
Markdown.

%prep
%setup -q -b1

# use our offline registry
export CARGO_HOME="$(pwd)/.cargo"

mkdir -p "$CARGO_HOME"
cat >.cargo/config <<EOF
[source.crates-io]
registry = 'https://github.com/rust-lang/crates.io-index'
replace-with = 'vendored-sources'

[source.vendored-sources]
directory = '$PWD/vendor'
EOF

%build
export CARGO_HOME="$(pwd)/.cargo"
export OPENSSL_NO_VENDOR=1

%cargo_build --frozen

%install
rm -rf $RPM_BUILD_ROOT

export CARGO_HOME="$(pwd)/.cargo"
export OPENSSL_NO_VENDOR=1

%cargo_install \
	--path . \
	--root $RPM_BUILD_ROOT%{_prefix}

%{__rm} $RPM_BUILD_ROOT%{_prefix}/.crates.toml
%{__rm} $RPM_BUILD_ROOT%{_prefix}/.crates2.json

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE README.md
%attr(755,root,root) %{_bindir}/mdbook-linkcheck
