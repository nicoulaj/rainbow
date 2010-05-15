# ──────────────────────────────────────────────────────────────────────────────────────────────────
# Licensing
#   This program is free software: you can redistribute it and/or modify it under the terms of the
#   GNU General Public License as published by the Free Software Foundation, either version 3
#   of the License, or (at your option) any later version.
#   This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
#   even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#   You should have received a copy of the GNU General Public License along with this program.
#   If not, see <http://www.gnu.org/licenses/>.
#
# Usage
#   Run 'make' to build the Debian package.
#
# Prerequisites
#   The following packages must be installed:
#     * debhelper
#     * devscripts
#     * make
# ──────────────────────────────────────────────────────────────────────────────────────────────────

SHELL=/bin/bash
SOURCE_DIR=src
OUTPUT_DIR=.
DISTRIB=`lsb_release -sc`
VERSION=`cat ${SOURCE_DIR}/VERSION`

prepare_changelog =                                                               \
  sed -e "s/DISTRIB/$(1)/g"                                                       \
      -e "s/PACKAGE_VERSION/$(2)-1~$(1)1/g"                                       \
      ${SOURCE_DIR}/debian/changelog.template > ${SOURCE_DIR}/debian/changelog

all: deb

deb:
	@echo "Building Debian package (distrib: ${DISTRIB}, version: ${VERSION})"
	@$(call prepare_changelog,${DISTRIB},${VERSION})
	@(cd ${SOURCE_DIR} && debuild -b -i -I -us -uc)

signed-deb:
	@echo "Building signed Debian package (distrib: ${DISTRIB}, version: ${VERSION})"
	@$(call prepare_changelog,${DISTRIB},${VERSION})
	@(cd ${SOURCE_DIR} && debuild -b -i -I)

src-pkg:
	@echo "Building source package (distrib: ${DISTRIB}, version: ${VERSION})"
	@$(call prepare_changelog,${DISTRIB},${VERSION})
	@(cd ${SOURCE_DIR} && debuild -S -i -I -us -uc)

signed-src-pkg:
	@echo "Building signed source package (distrib: ${DISTRIB}, version: ${VERSION})"
	@$(call prepare_changelog,${DISTRIB},${VERSION})
	@(cd ${SOURCE_DIR} && debuild -S -i -I)

release-for-distrib: clean signed-deb signed-src-pkg
	@echo "Uploading source package to Launchpad (distrib: ${DISTRIB}, version: ${VERSION})"
	@dput ppa:julien-nicoulaud/colorex colorex_*_source.changes

release:
	@$(MAKE) release-for-distrib DISTRIB=jaunty
	@$(MAKE) release-for-distrib DISTRIB=karmic
	@$(MAKE) release-for-distrib DISTRIB=lucid
	@$(MAKE) release-for-distrib DISTRIB=maverick

clean:
	@echo "Cleaning output files"
	@rm -vf ${OUTPUT_DIR}/*.{dsc,deb,tar.gz,changes,build,dsc,upload}
	@rm -rvf ${SOURCE_DIR}/debian/colorex.debhelper.log \
	         ${SOURCE_DIR}/debian/colorex.substvars \
	         ${SOURCE_DIR}/debian/colorex \
	         ${SOURCE_DIR}/debian/changelog \
	         ${SOURCE_DIR}/debian/files
