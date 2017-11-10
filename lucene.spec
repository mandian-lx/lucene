%{?_javapackages_macros:%_javapackages_macros}
%bcond_with     jp_minimal

Summary:        High-performance, full-featured text search engine
Name:           lucene
Version:        6.1.0
Release:        6.1
Epoch:          0
Group:          Development/Java
License:        ASL 2.0
URL:            http://lucene.apache.org/
# solr source contains both lucene and dev-tools
Source0:        http://www.apache.org/dist/lucene/solr/%{version}/solr-%{version}-src.tgz

Patch0:         0001-Disable-ivy-settings.patch
Patch1:         0002-Dependency-generation.patch
# CVE-2017-12629 - https://bugzilla.redhat.com/show_bug.cgi?id=1501529
# Backport of lucene part of https://github.com/apache/lucene-solr/commit/926cc4d65b6d2cc40ff07f76d50ddeda947e3cc4
Patch2:         0001-SOLR-11477-Disallow-resolving-of-external-entities-i.patch

BuildRequires:  ant
BuildRequires:  ivy-local
BuildRequires:  maven-local

BuildRequires:  mvn(org.apache:apache:pom:)
BuildRequires:  mvn(jakarta-regexp:jakarta-regexp)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
%if %{without jp_minimal}
BuildRequires:  mvn(com.carrotsearch.randomizedtesting:randomizedtesting-runner)
BuildRequires:  mvn(com.ibm.icu:icu4j)
BuildRequires:  mvn(commons-codec:commons-codec)
BuildRequires:  mvn(commons-logging:commons-logging)
BuildRequires:  mvn(com.spatial4j:spatial4j)
BuildRequires:  mvn(javax.servlet:javax.servlet-api)
BuildRequires:  mvn(javax.servlet:servlet-api)
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(net.sourceforge.nekohtml:nekohtml)
BuildRequires:  mvn(org.antlr:antlr4-runtime)
BuildRequires:  mvn(org.apache.commons:commons-compress)
BuildRequires:  mvn(org.apache.httpcomponents:httpclient)
BuildRequires:  mvn(org.apache.httpcomponents:httpcore)
BuildRequires:  mvn(org.apache.uima:Tagger)
BuildRequires:  mvn(org.apache.uima:uimaj-core)
BuildRequires:  mvn(org.apache.uima:WhitespaceTokenizer)
BuildRequires:  mvn(org.carrot2:morfologik-fsa)
BuildRequires:  mvn(org.carrot2:morfologik-polish)
BuildRequires:  mvn(org.carrot2:morfologik-stemming)
BuildRequires:  mvn(org.eclipse.jetty:jetty-continuation)
BuildRequires:  mvn(org.eclipse.jetty:jetty-http)
BuildRequires:  mvn(org.eclipse.jetty:jetty-io)
BuildRequires:  mvn(org.eclipse.jetty:jetty-server)
BuildRequires:  mvn(org.eclipse.jetty:jetty-servlet)
BuildRequires:  mvn(org.eclipse.jetty:jetty-util)
BuildRequires:  mvn(org.ow2.asm:asm)
BuildRequires:  mvn(org.ow2.asm:asm-commons)
BuildRequires:  mvn(xerces:xercesImpl)
%endif
BuildRequires:  mvn(org.apache.lucene:lucene-solr-grandparent:pom:)

Provides:       %{name}-core = %{epoch}:%{version}-%{release}

BuildArch:      noarch

%description
Apache Lucene is a high-performance, full-featured text search
engine library written entirely in Java. It is a technology suitable
for nearly any application that requires full-text search, especially
cross-platform.

%package analysis
Summary:      Lucene Common Analyzers

%description analysis
Lucene Common Analyzers.

%package queries
Summary:      Lucene Queries Module

%description queries
Lucene Queries Module.

%package queryparser
Summary:      Lucene QueryParsers Module

%description queryparser
Lucene QueryParsers Module.

%package analyzers-smartcn
Summary:      Smart Chinese Analyzer

%description analyzers-smartcn
Lucene Smart Chinese Analyzer.

%package sandbox
Summary:      Lucene Sandbox Module

%description sandbox
Lucene Sandbox Module.

%if %{without jp_minimal}
%package parent
Summary:      Parent POM for Lucene

%description parent
Parent POM for Lucene.

%package solr-grandparent
Summary:      Lucene Solr grandparent POM

%description solr-grandparent
Lucene Solr grandparent POM.

%package backward-codecs
Summary:      Lucene Backward Codecs Module

%description backward-codecs
Codecs for older versions of Lucene.

%package benchmark
Summary:      Lucene Benchmarking Module

%description benchmark
Lucene Benchmarking Module.

%package replicator
Summary:      Lucene Replicator Module

%description replicator
Lucene Replicator Module.

%package grouping
Summary:      Lucene Grouping Module

%description grouping
Lucene Grouping Module.

%package highlighter
Summary:      Lucene Highlighter Module

%description highlighter
Lucene Highlighter Module.

%package misc
Summary:      Miscellaneous Lucene extensions

%description misc
Miscellaneous Lucene extensions.

%package test-framework
Summary:      Apache Lucene Java Test Framework

%description test-framework
Apache Lucene Java Test Framework.

%package memory
Summary:      Lucene Memory Module

%description memory
High-performance single-document index to compare against Query.

%package expressions
Summary:      Lucene Expressions Module

%description expressions
Dynamically computed values to sort/facet/search on based on a pluggable
grammar.

%package demo
Summary:      Lucene Demo Module

%description demo
Demo for Apache Lucene Java.

%package classification
Summary:      Lucene Classification Module

%description classification
Lucene Classification Module.

%package join
Summary:      Lucene Join Module

%description join
Lucene Join Module.

%package suggest
Summary:      Lucene Suggest Module

%description suggest
Lucene Suggest Module.

%package facet
Summary:      Lucene Facets Module

%description facet
Package for Faceted Indexing and Search.

%package spatial
Summary:      Geospatial indexing APIs for Apache Lucene

%description spatial
Geospatial indexing APIs for Apache Lucene.

%package spatial-extras
Summary:      Spatial Strategies for Apache Lucene

%description spatial-extras
Spatial Strategies for Apache Lucene.

%package spatial3d
Summary:      Lucene Spatial 3D

%description spatial3d
Spatial shapes implemented using 3D planar geometry

%package codecs
Summary:      Codecs and postings formats for Apache Lucene

%description codecs
Codecs and postings formats for Apache Lucene.

%package analyzers-phonetic
Summary:      Lucene Phonetic Filters

%description analyzers-phonetic
Provides phonetic encoding via Commons Codec.

%package analyzers-icu
Summary:      Lucene ICU Analysis Components

%description analyzers-icu
Provides integration with ICU (International Components for Unicode) for
stronger Unicode and internationalization support.

%package analyzers-morfologik
Summary:      Lucene Morfologik Polish Lemmatizer

%description analyzers-morfologik
A dictionary-driven lemmatizer for Polish (includes morphosyntactic
annotations).

%package analyzers-uima
Summary:      Lucene UIMA Analysis Components

%description analyzers-uima
Lucene Integration with UIMA for extracting metadata from arbitrary (text)
fields and enrich document with features extracted from UIMA types (language,
sentences, concepts, named entities, etc.).

%package analyzers-kuromoji
Summary:      Lucene Kuromoji Japanese Morphological Analyzer

%description analyzers-kuromoji
Lucene Kuromoji Japanese Morphological Analyzer.

%package analyzers-stempel
Summary:      Lucene Stempel Analyzer

%description analyzers-stempel
Lucene Stempel Analyzer.

%endif # without jp_minimal

%package javadoc
Summary:        Javadoc for Lucene

%description javadoc
%{summary}.

%prep
%setup -q -n solr-%{version}

%patch0 -p1
%patch1 -p1
%patch2 -p1

rm -rf solr

find -name "*.jar" -delete

mv lucene/*.txt .

sed -i -e "s|/Export-Package>|/Export-Package><_nouses>true</_nouses>|g" dev-tools/maven/pom.xml.template

# make the target public
sed -i 's/-filter-pom-templates/filter-pom-templates/' lucene/common-build.xml
# avoid descent to other modules to avoid unnecessary compilation of modules we
# will recompile with maven anyway
%pom_xpath_remove 'target[@name="compile-tools"]/modules-crawl' lucene/build.xml

# suggest provides spellchecker
%mvn_alias :%{name}-suggest :%{name}-spellchecker

# compatibility with existing packages
%mvn_alias :%{name}-analyzers-common :%{name}-analyzers

%mvn_package ":%{name}-analysis-modules-aggregator" %{name}-analysis
%mvn_package ":%{name}-analyzers-common" %{name}-analysis
%mvn_package ":{*}-aggregator" @1

%build
pushd %{name}
find -maxdepth 2 -type d -exec mkdir -p '{}/lib' \;
# generate dependencies
ant -f common-build.xml filter-pom-templates -Divy.mode=local -Dversion=%{version}

# fix source dir + move to expected place
for pom in `find build/poms/%{name} -name pom.xml`; do
    sed 's/\${module-path}/${basedir}/g' "$pom" > "${pom##build/poms/%{name}/}"
done
%pom_disable_module src/test core
%pom_disable_module src/test codecs

# unresolvable test dep
%pom_remove_dep org.locationtech.spatial4j:spatial4j::test spatial-extras

# fix dep on spatial4j
%pom_change_dep org.locationtech.spatial4j:spatial4j com.spatial4j:spatial4j spatial-extras
%pom_change_dep org.locationtech.spatial4j:spatial4j com.spatial4j:spatial4j benchmark
find benchmark spatial-extras -name *.java -exec sed -i \
  -e 's/org\.locationtech\.spatial4j/com.spatial4j.core/' {} \;

# test deps
%pom_add_dep org.antlr:antlr-runtime::test demo

popd

mv lucene/build/poms/pom.xml .

# deal with split packages in core/misc modules by adding additional metadata and
# require-bundling the core bundle from misc
%pom_xpath_set "pom:Export-Package" "*;version=\"%{version}\""
%pom_add_plugin org.apache.felix:maven-bundle-plugin lucene/misc \
"<configuration><instructions>
<Require-Bundle>org.apache.lucene.core;bundle-version=\"%{version}\"</Require-Bundle>
<Export-Package>
 org.apache.lucene.document;version=\"%{version}\";misc=split;mandatory:=misc,
 org.apache.lucene.index;version=\"%{version}\";misc=split;mandatory:=misc,
 org.apache.lucene.search;version=\"%{version}\";misc=split;mandatory:=misc,
 org.apache.lucene.store;version=\"%{version}\";misc=split;mandatory:=misc,
 org.apache.lucene.util.fst;version=\"%{version}\";misc=split;mandatory:=misc,
 *;version=\"%{version}\"</Export-Package>
</instructions></configuration>"

%pom_disable_module solr
%pom_remove_plugin -r :gmaven-plugin
%pom_remove_plugin -r :maven-enforcer-plugin
%pom_remove_plugin -r :forbiddenapis
%pom_remove_plugin -r :buildnumber-maven-plugin

%if %{with jp_minimal}
pushd lucene
%pom_disable_module backward-codecs
%pom_disable_module codecs
%pom_disable_module test-framework
%pom_disable_module benchmark
%pom_disable_module classification
%pom_disable_module demo
%pom_disable_module expressions
%pom_disable_module facet
%pom_disable_module grouping
%pom_disable_module highlighter
%pom_disable_module join
%pom_disable_module memory
%pom_disable_module misc
%pom_disable_module replicator
%pom_disable_module spatial
%pom_disable_module spatial-extras
%pom_disable_module spatial3d
%pom_disable_module suggest

%pom_disable_module icu analysis
%pom_disable_module kuromoji analysis
%pom_disable_module morfologik analysis
%pom_disable_module phonetic analysis
%pom_disable_module stempel analysis
%pom_disable_module uima analysis

popd

%mvn_package :lucene-parent __noinstall
%mvn_package :lucene-solr-grandparent __noinstall
%endif


# For some reason TestHtmlParser.testTurkish fails when building inside SCLs
%mvn_build -s -f

%install
%mvn_install

# Use the same directory of the main package for subpackage licence and docs
%global _docdir_fmt %{name}

%files -f .mfiles-%{name}-core
%doc CHANGES.txt README.txt MIGRATE.txt
%doc LICENSE.txt NOTICE.txt

%files analysis -f .mfiles-%{name}-analysis
%files queries -f .mfiles-%{name}-queries
%files queryparser -f .mfiles-%{name}-queryparser
%files analyzers-smartcn -f .mfiles-%{name}-analyzers-smartcn
%files sandbox -f .mfiles-%{name}-sandbox
%if %{without jp_minimal}
%files parent -f .mfiles-%{name}-parent
%files solr-grandparent -f .mfiles-%{name}-solr-grandparent
%files benchmark -f .mfiles-%{name}-benchmark
%files backward-codecs -f .mfiles-%{name}-backward-codecs
%files replicator -f .mfiles-%{name}-replicator
%files grouping -f .mfiles-%{name}-grouping
%files highlighter -f .mfiles-%{name}-highlighter
%files misc -f .mfiles-%{name}-misc
%files test-framework -f .mfiles-%{name}-test-framework
%files memory -f .mfiles-%{name}-memory
%files expressions -f .mfiles-%{name}-expressions
%files demo -f .mfiles-%{name}-demo
%files classification -f .mfiles-%{name}-classification
%files join -f .mfiles-%{name}-join
%files suggest -f .mfiles-%{name}-suggest
%files facet -f .mfiles-%{name}-facet
%files spatial -f .mfiles-%{name}-spatial
%files spatial-extras -f .mfiles-%{name}-spatial-extras
%files spatial3d -f .mfiles-%{name}-spatial3d
%files codecs -f .mfiles-%{name}-codecs
%files analyzers-phonetic -f .mfiles-%{name}-analyzers-phonetic
%files analyzers-icu -f .mfiles-%{name}-analyzers-icu
%files analyzers-morfologik -f .mfiles-%{name}-analyzers-morfologik
%files analyzers-uima -f .mfiles-%{name}-analyzers-uima
%files analyzers-kuromoji -f .mfiles-%{name}-analyzers-kuromoji
%files analyzers-stempel -f .mfiles-%{name}-analyzers-stempel
%endif

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt NOTICE.txt

%changelog
* Mon Oct 16 2017 Michael Simacek <msimacek@redhat.com> - 0:6.1.0-6
- Backport fix for CVE-2017-12629

* Thu Sep 21 2017 Mat Booth <mat.booth@redhat.com> - 0:6.1.0-5
- Rebuild to regenerate OSGi metadata due to objectweb-asm update

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0:6.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Apr 04 2017 Mat Booth <mat.booth@redhat.com> - 0:6.1.0-3
- Add better OSGi metadata for dealing with core/misc split packages
- Drop F24-specific hack

* Tue Mar 21 2017 Michael Simacek <msimacek@redhat.com> - 0:6.1.0-2
- Update jp_minimal conditional

* Mon Mar 20 2017 Mat Booth <mat.booth@redhat.com> - 0:6.1.0-1
- Update to lucene 6
- Add "spatial-extras" subpackage, this decouples dependencies on spatial4j.

* Thu Mar 16 2017 Michael Simacek <msimacek@redhat.com> - 0:5.5.0-7
- Add jp_minimal conditional

* Mon Feb 06 2017 Michael Simacek <msimacek@redhat.com> - 0:5.5.0-6
- Remove buildnumber-plugin

* Mon Aug 22 2016 Roman Vais <rvais@redhat.com> - 0:5.5.0-5
- Removed test dependency macros for lucene demo that caused conflict (duplicity)

* Wed Jul 13 2016 Roland Grunberg <rgrunber@redhat.com> - 0:5.5.0-4
- analyzers-common should have versioned requires on package from core.

* Fri Jul 08 2016 Mat Booth <mat.booth@redhat.com> - 0:5.5.0-3
- Misc module should require core module, the split package
  causes problems for OSGi consumers

* Mon Apr 18 2016 Mat Booth <mat.booth@redhat.com> - 0:5.5.0-2
- Add missing BR on ant, fixes FTBFS

* Wed Feb 24 2016 Michael Simacek <msimacek@redhat.com> - 0:5.5.0-1
- Update to upstream version 5.5.0

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0:5.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 25 2016 Alexander Kurtakov <akurtako@redhat.com> 0:5.4.1-2
- Organize Sources numbering.
- Drop old jpackage header - package has nothing in common anymore.
- Drop 3+ years old provides/obsoletes.
- Move old changelog to separate file to ease working with the spec file.

* Mon Jan 25 2016 Alexander Kurtakov <akurtako@redhat.com> 0:5.4.1-1
- Update to upstream 5.4.1 release.

* Thu Jan 21 2016 Alexander Kurtakov <akurtako@redhat.com> 0:5.4.0-1
- Update to upstream 5.4.0 release.

* Tue Oct 6 2015 Alexander Kurtakov <akurtako@redhat.com> 0:5.3.1-1
- Update to upstream 5.3.1 release.

* Thu Aug 27 2015 Alexander Kurtakov <akurtako@redhat.com> 0:5.3.0-1
- Update to upstream 5.3.0 release.

* Wed Aug 26 2015 Mat Booth <mat.booth@redhat.com> - 0:5.2.1-4
- Remove forbidden SCL macros

* Wed Jun 24 2015 Alexander Kurtakov <akurtako@redhat.com> 0:5.2.1-3
- Disable generation of uses clauses in OSGi manifests.

* Wed Jun 24 2015 Alexander Kurtakov <akurtako@redhat.com> 0:5.2.1-2
- Drop old workarounds.

* Tue Jun 23 2015 Alexander Kurtakov <akurtako@redhat.com> 0:5.2.1-1
- Update to upstream 5.2.1.

