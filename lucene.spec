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

Summary:        High-performance, full-featured text search engine
Name:           lucene
Version:        2.9.4
Release:        6
Epoch:          0
License:        ASL 2.0
URL:            http://lucene.apache.org/
Group:          Development/Java
Source0:        http://archive.apache.org/dist/lucene/java/%{name}-%{version}-src.tar.gz
Source1:        lucene-%{version}-core-OSGi-MANIFEST.MF
Source2:        lucene-%{version}-analysis-OSGi-MANIFEST.MF
Patch1:         0001-Remove-bdb-packageset.patch
Patch2:         0002-Fix-version-string.patch
Patch3:         0003-Remove-classpath.patch
BuildRequires:  jpackage-utils >= 0:1.6
BuildRequires:  ant >= 0:1.6
BuildRequires:  ant-junit >= 0:1.6
BuildRequires:  junit
BuildRequires:  javacc
BuildRequires:  java-javadoc
BuildRequires:  jline
BuildRequires:  jtidy
BuildRequires:  regexp
BuildRequires:  apache-commons-digester
BuildRequires:  unzip
BuildRequires:  zip
BuildRequires:  java-devel >= 0:1.6.0
BuildRequires:  apache-commons-compress
BuildRequires:  icu4j
# for tests
BuildRequires:  subversion

Provides:       lucene-core = %{version}-%{release}
# previously used by eclipse but no longer needed
Obsoletes:      lucene-devel < %{version}
BuildArch:      noarch

Requires:       jpackage-utils

%description
Apache Lucene is a high-performance, full-featured text search
engine library written entirely in Java. It is a technology suitable
for nearly any application that requires full-text search, especially
cross-platform.

%package javadoc
Summary:        Javadoc for Lucene
Group:          Development/Java
Requires:       jpackage-utils

%description javadoc
%{summary}.

%package demo
Summary:        Lucene demonstration library
Group:          Development/Java
Requires:       %{name} = %{version}-%{release}

%description demo
%{summary}.

%package contrib
Summary:        Lucene contributed extensions
Group:          Development/Java
Requires:       %{name} = %{version}-%{release}

%description contrib
%{summary}.

%prep
%setup -q -n %{name}-%{version}
# remove all binary libs
find . -name "*.jar" -exec rm -f {} \;

%patch1 -p1 -b .db-javadoc
%patch2 -p1 -b .fixmanifests
%patch3 -p1 -b .removeclasspath

iconv --from=ISO-8859-1 --to=UTF-8 CHANGES.txt > CHANGES.txt.new

# prepare pom files (replace @version@ with real version)
find contrib -iname '*.pom.xml.template' -exec \
             sed -i "s:@version@:%{version}:g" \{\} \;

%build
mkdir -p docs
mkdir -p lib
export OPT_JAR_LIST="ant/ant-junit junit"
export CLASSPATH=$(build-classpath jline jtidy regexp commons-digester apache-commons-compress icu4j)
rm -r contrib/db

ant -Dbuild.sysclasspath=first \
  -Djavacc.home=%{_bindir}/javacc \
  -Djavacc.jar=%{_javadir}/javacc.jar \
  -Djavacc.jar.dir=%{_javadir} \
  -Djavadoc.link=%{_javadocdir}/java \
  -Dversion=%{version} \
  package 
        
# add missing OSGi metadata to manifests
mkdir META-INF
unzip -o build/lucene-core-%{version}.jar META-INF/MANIFEST.MF
cat %{SOURCE1} >> META-INF/MANIFEST.MF
sed -i '/^\r$/d' META-INF/MANIFEST.MF
zip -u build/lucene-core-%{version}.jar META-INF/MANIFEST.MF
unzip -o build/contrib/analyzers/common/lucene-analyzers-%{version}.jar META-INF/MANIFEST.MF
cat %{SOURCE2} >> META-INF/MANIFEST.MF
sed -i '/^\r$/d' META-INF/MANIFEST.MF
zip -u build/contrib/analyzers/common/lucene-analyzers-%{version}.jar META-INF/MANIFEST.MF
cp contrib/analyzers/common/pom.xml.template contrib/analyzers/
cp build/contrib/analyzers/common/lucene-analyzers-%{version}.jar build/contrib/analyzers/

%install

# jars
install -d -m 0755 $RPM_BUILD_ROOT%{_javadir}
install -d -m 0755 $RPM_BUILD_ROOT%{_mavenpomdir}
install -m 0644 build/%{name}-core-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar
ln -sf %{name}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-core.jar
install -m 0644 build/%{name}-demos-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-demos.jar

# contrib jars
install -d -m 0755 $RPM_BUILD_ROOT%{_javadir}/%{name}-contrib
for c in analyzers ant benchmark collation fast-vector-highlighter highlighter \
         instantiated lucli memory misc queries queryparser regex remote \
         snowball spatial spellchecker surround swing wikipedia wordnet \
         xml-query-parser; do
    install -m 0644 build/contrib/$c/%{name}-${c}-%{version}.jar \
        $RPM_BUILD_ROOT%{_javadir}/%{name}-contrib/%{name}-${c}.jar

    install -m 0644 contrib/$c/pom.xml.template \
               $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP.lucene-contrib-lucene-$c.pom
    %add_to_maven_depmap org.apache.lucene lucene-$c %{version} JPP/lucene-contrib lucene-$c
done

# main poms
for pom in contrib core demos parent; do
    install -m 0644 lucene-$pom-pom.xml.template \
           $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP-lucene-$pom.pom
    %add_to_maven_depmap org.apache.lucene lucene-$pom %{version} JPP lucene-$pom
done

# javadoc
install -d -m 0755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -pr build/docs/api/* \
  $RPM_BUILD_ROOT%{_javadocdir}/%{name}

# webapp
install -d -m 0755 $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}
install -m 0644 build/%{name}web.war \
  $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}

%pre javadoc
# workaround for rpm bug, can be removed in F-17
[ $1 -gt 1 ] && [ -L %{_javadocdir}/%{name} ] && \
rm -rf $(readlink -f %{_javadocdir}/%{name}) %{_javadocdir}/%{name} || :

%post
%update_maven_depmap

%postun
%update_maven_depmap


%files
%doc CHANGES.txt LICENSE.txt README.txt NOTICE.txt
%{_mavenpomdir}/JPP*pom
%{_mavendepmapfragdir}/%{name}
%{_javadir}/%{name}.jar
%{_javadir}/%{name}-core.jar
%{_datadir}/%{name}-%{version}

%files javadoc
%doc LICENSE.txt
%{_javadocdir}/%{name}

%files contrib
%{_javadir}/%{name}-contrib
%doc contrib/CHANGES.txt

%files demo
%{_javadir}/%{name}-demos.jar

