Name:		cdi-api
Version:	2.0.SP1
Release:	1
Summary:	Contexts and Dependency Injection 2.0 API
Group:		Development/Java
License:	Apache-2.0
URL:		https://github.com/cdi-spec/cdi
Source0:	https://github.com/cdi-spec/cdi/archive/refs/tags/%{version}.tar.gz

BuildArch:	noarch
BuildRequires:	python
BuildRequires:	maven
BuildRequires:	java-current-devel
BuildRequires:	javax.inject
BuildRequires:	jakarta-el
BuildRequires:	jboss-interceptors-1.2-api
# The interceptors POM parents jboss-parent, and that RPM does not
# require the parent, so Maven cannot read the POM without it.
BuildRequires:	mvn(org.jboss:jboss-parent:pom::)
BuildSystem:	maven

%description
CDI 2.0 API (javax.enterprise). This is the last release whose packages
are javax.enterprise, which JTA 1.2 @TransactionScoped imports.

%prep
%setup -q -n cdi-%{version}
cp -p LICENSE.txt README.md api/
# The spec module is the document. Publish the API jar only.
# weld-parent 61 replaces 36 and runs a license bundle we do not ship.
# Coordinates and dependency versions are already on this POM.
python - <<'PY'
import re
import shutil
from pathlib import Path
root = Path(".").resolve()
mod = root / "api"
stage = root.parent / "cdi-api-module"
if stage.exists():
	shutil.rmtree(stage)
shutil.copytree(mod, stage)
for child in list(root.iterdir()):
	if child.is_dir():
		shutil.rmtree(child)
	else:
		child.unlink()
for child in list(stage.iterdir()):
	shutil.move(str(child), root / child.name)
shutil.rmtree(stage)
pom = Path("pom.xml")
text = pom.read_text()
text = re.sub(r"\s*<parent>.*?</parent>", "", text, count=1, flags=re.S)
text = re.sub(
	r"\s*<plugin>\s*<groupId>org\.apache\.felix</groupId>\s*<artifactId>maven-bundle-plugin</artifactId>.*?</plugin>",
	"",
	text,
	count=1,
	flags=re.S,
)
text = re.sub(
	r"\s*<archive>\s*<manifestFile>.*?</manifestFile>\s*</archive>",
	"",
	text,
	count=1,
	flags=re.S,
)
pom.write_text(text)
PY

%files -f .mfiles
%doc LICENSE.txt README.md
