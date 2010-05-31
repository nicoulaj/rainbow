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
PKG_NAME=colorex
DISTRIB=`lsb_release -sc`
VERSION=`cat ${SOURCE_DIR}/VERSION`
SOURCE_DIR=src
OUTPUT_DIR=.
DOC_DIR=doc


all: deb

prepare-changelog:
	@sed -e "s/DISTRIB/${DISTRIB}/g" \
	     -e "s/PACKAGE_VERSION/${VERSION}-1~${DISTRIB}1/g" \
	     ${SOURCE_DIR}/debian/changelog.template > ${SOURCE_DIR}/debian/changelog

doc: clean
	@echo "Generating documentation with Epydoc."
	@epydoc --config epydoc.cfg

deb: prepare-changelog
	@echo "Building Debian package (distrib: ${DISTRIB}, version: ${VERSION})"
	@(cd ${SOURCE_DIR} && debuild -b -i -I -us -uc)

signed-deb: prepare-changelog
	@echo "Building signed Debian package (distrib: ${DISTRIB}, version: ${VERSION})"
	@(cd ${SOURCE_DIR} && debuild -b -i -I)

src-pkg: prepare-changelog
	@echo "Building source package (distrib: ${DISTRIB}, version: ${VERSION})"
	@(cd ${SOURCE_DIR} && debuild -S -i -I -us -uc)

signed-src-pkg: prepare-changelog
	@echo "Building signed source package (distrib: ${DISTRIB}, version: ${VERSION})"
	@(cd ${SOURCE_DIR} && debuild -S -i -I)

release-for-distrib: clean signed-deb signed-src-pkg
	@echo "Uploading source package to Launchpad (distrib: ${DISTRIB}, version: ${VERSION})"
	@dput ppa:julien-nicoulaud/colorex ${PKG_NAME}_*_source.changes

release:
	@$(MAKE) release-for-distrib DISTRIB=jaunty
	@$(MAKE) release-for-distrib DISTRIB=karmic
	@$(MAKE) release-for-distrib DISTRIB=lucid
	@$(MAKE) release-for-distrib DISTRIB=maverick

clean:
	@echo "Cleaning output files"
	@rm -vf ${OUTPUT_DIR}/*.{dsc,deb,tar.gz,changes,build,dsc,upload}
	@rm -rvf ${SOURCE_DIR}/debian/*debhelper* \
	         ${SOURCE_DIR}/debian/*substvars* \
	         ${SOURCE_DIR}/debian/${PKG_NAME} \
	         ${SOURCE_DIR}/debian/changelog \
	         ${SOURCE_DIR}/debian/files \
	         ${DOC_DIR}
