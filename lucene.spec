# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define section         free
%define nversion        2.3
%define gcj_support     0

Summary:	High-performance, full-featured text search engine
Name:		lucene
Version:	2.4.0
Release:	1
License:	Apache License
Url:		http://lucene.apache.org/
Group:		Development/Java
Source0:	http://www.apache.org/dist/lucene/java/%{name}-%{version}-src.tar.gz
Source1:	lucene-1.9-OSGi-MANIFEST.MF
Source2:	lucene-1.9-analysis-OSGi-MANIFEST.MF
Patch4:		lucene-2.3.0-db-javadoc.patch
BuildRequires:	ant
BuildRequires:	ant-nodeps
BuildRequires:	javacc
BuildRequires:	java-javadoc
BuildRequires:	java-rpmbuild
BuildRequires:	junit
BuildRequires:	jtidy
BuildRequires:	jakarta-commons-digester
BuildRequires:	jline
BuildRequires:	regexp
BuildRequires:	zip
Provides:	lucene-core = %{version}-%{release}
# previously used by eclipse but no longer needed
Obsoletes:	lucene-devel < %{version}
%if !%{gcj_support}
BuildRequires:	java-devel
BuildArch:	noarch
%else
BuildRequires:	java-gcj-compat-devel
%endif

%description
Jakarta Lucene is a high-performance, full-featured text search engine
written entirely in Java. It is a technology suitable for nearly any
application that requires full-text search, especially cross-platform.

%package javadoc
Summary:	Javadoc for Lucene
Group:		Development/Java

%description javadoc
Javadoc for Lucene.

%package demo
Summary:	Lucene demonstrations and samples
Group:		Development/Java
Requires:	%{name} = %{version}-%{release}

%description demo
%{summary}.

%package contrib
Summary:	Lucene contributed extensions
Group:		Development/Java
Requires:	%{name} = %{version}-%{release}

%description contrib
%{summary}.

#%package contrib-db
#Summary:	Lucene contributed bdb extensions
#Group:		Internet/WWW/Indexing/Search
#Requires:	%{name} = %{version}-%{release}
#Requires:	berkeleydb
#Requires:	berkeleydb-native >= 0:4.3.29

#%description contrib-db
#%{summary}.

%prep
%setup -q
%remove_java_binaries

%patch4 -p0 -b .db-javadoc

%build
mkdir -p docs
mkdir -p lib
export OPT_JAR_LIST="ant/ant-junit junit"
export CLASSPATH=$(build-classpath jline jtidy regexp commons-digester)
#pushd contrib/db/bdb/lib
#ln -sf $(build-classpath berkeleydb-native) .
#popd
#pushd contrib/db/bdb-je/lib
#ln -sf $(build-classpath berkeleydb) .
#popd
rm -r contrib/db

#FIXME:	Tests freeze randomly. Turning on debug messages shows warnings like:

# [junit] GC Warning:	Repeated allocation of very large block (appr. size 512000):
# [junit] 	May lead to memory leak and poor performance.

# See:	http://koji.fedoraproject.org/koji/getfile?taskID=169839&name=build.log
# for an example

%ant -Dbuild.sysclasspath=first \
  -Djavacc.home=%{_bindir}/javacc \
  -Djavacc.jar=%{_javadir}/javacc.jar \
  -Djavacc.jar.dir=%{_javadir} \
  -Djavadoc.link=%{_javadocdir}/java \
  -Dversion=%{version} \
  package
#  package test generate-test-reports

mkdir META-INF
cp %{SOURCE1} META-INF/MANIFEST.MF
zip -u build/lucene-core-%{version}.jar META-INF/MANIFEST.MF
cp %{SOURCE2} META-INF/MANIFEST.MF
zip -u build/contrib/analyzers/lucene-analyzers-%{version}.jar META-INF/MANIFEST.MF

%install
install -d -m 0755 %{buildroot}%{_javadir}
install -m 0644 build/%{name}-core-%{version}.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
install -m 0644 build/%{name}-demos-%{version}.jar %{buildroot}%{_javadir}/%{name}-demos-%{version}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{version}.jar; do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

# contrib jars
install -d -m 0755 %{buildroot}%{_javadir}/%{name}-contrib
for c in analyzers ant highlighter lucli memory misc queries similarity snowball spellchecker surround swing wordnet xml-query-parser; do
    install -m 0644 build/contrib/$c/%{name}-${c}-%{version}.jar \
		%{buildroot}%{_javadir}/%{name}-contrib
done
(cd %{buildroot}%{_javadir}/%{name}-contrib && for jar in *-%{version}.jar; do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

# bdb contrib jars
#install -d -m 0755 %{buildroot}%{_javadir}/%{name}-contrib-db
#install -m 0644 build/contrib/db/bdb/%{name}-bdb-%{version}.jar \
#		%{buildroot}%{_javadir}/%{name}-contrib-db
#install -m 0644 build/contrib/db/bdb-je/%{name}-bdb-je-%{version}.jar \
#		%{buildroot}%{_javadir}/%{name}-contrib-db
#(cd %{buildroot}%{_javadir}/%{name}-contrib-db && for jar in *-%{version}.jar; do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

# javadoc
install -d -m 0755 %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -pr build/docs/api/* \
  %{buildroot}%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}

# webapp
install -d -m 0755 %{buildroot}%{_datadir}/%{name}-%{version}
install -m 0644 build/%{name}web.war \
  %{buildroot}%{_datadir}/%{name}-%{version}

%gcj_compile

%if %{gcj_support}
%post
%update_gcjdb

%postun
%clean_gcjdb
%endif

%files
%doc CHANGES.txt LICENSE.txt README.txt
%{_javadir}/%{name}-%{version}.jar
%{_javadir}/%{name}.jar
%{_datadir}/%{name}-%{version}
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%{_libdir}/gcj/%{name}/%{name}-%{version}.jar.*
%endif

%files javadoc
%{_javadocdir}/%{name}-%{version}
%ghost %{_javadocdir}/%{name}

%files contrib
%{_javadir}/%{name}-contrib
%if %{gcj_support}
%{_libdir}/gcj/%{name}/lucene-analyzers-%{version}.jar.*
%{_libdir}/gcj/%{name}/lucene-ant-%{version}.jar.*
%{_libdir}/gcj/%{name}/lucene-highlighter-%{version}.jar.*
%{_libdir}/gcj/%{name}/lucene-lucli-%{version}.jar.*
%{_libdir}/gcj/%{name}/lucene-memory-%{version}.jar.*
%{_libdir}/gcj/%{name}/lucene-misc-%{version}.jar.*
%{_libdir}/gcj/%{name}/lucene-queries-%{version}.jar.*
%{_libdir}/gcj/%{name}/lucene-snowball-%{version}.jar.*
%{_libdir}/gcj/%{name}/lucene-spellchecker-%{version}.jar.*
%{_libdir}/gcj/%{name}/lucene-surround-%{version}.jar.*
%{_libdir}/gcj/%{name}/lucene-swing-%{version}.jar.*
%{_libdir}/gcj/%{name}/lucene-wordnet-%{version}.jar.*
%{_libdir}/gcj/%{name}/lucene-xml-query-parser-%{version}.jar.*
%endif

#%files contrib-db
#%{_javadir}/%{name}-contrib-db
#%if %{with_gcj}
#%{_libdir}/gcj/%{name}/lucene-bdb-%{version}.jar.*
#%{_libdir}/gcj/%{name}/lucene-bdb-je-%{version}.jar.*
#%endif

%files demo
%{_javadir}/%{name}-demos-%{version}.jar
%{_javadir}/%{name}-demos.jar
%if %{gcj_support}
%{_libdir}/gcj/%{name}/%{name}-demos-%{version}.jar.*
%endif

