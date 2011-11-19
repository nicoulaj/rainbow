SHELL=/bin/bash
PKG_NAME=rainbow
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

deb: prepare-changelog
	@(cd ${SOURCE_DIR} && debuild -b -i -I -us -uc)

signed-deb: prepare-changelog
	@(cd ${SOURCE_DIR} && debuild -b -i -I)

src-pkg: prepare-changelog
	@(cd ${SOURCE_DIR} && debuild -S -i -I -us -uc)

signed-src-pkg: prepare-changelog
	@(cd ${SOURCE_DIR} && debuild -S -i -I)

release-for-distrib: clean signed-deb signed-src-pkg
	@dput ppa:rainbow/ppa ${PKG_NAME}_*_source.changes

release:
	@$(MAKE) release-for-distrib DISTRIB=lucid
	@$(MAKE) release-for-distrib DISTRIB=maverick
	@$(MAKE) release-for-distrib DISTRIB=natty
	@$(MAKE) release-for-distrib DISTRIB=oneiric

clean:
	@rm -vf ${OUTPUT_DIR}/*.{dsc,deb,tar.gz,changes,build,dsc,upload}
	@rm -rvf ${SOURCE_DIR}/debian/*debhelper* \
	         ${SOURCE_DIR}/debian/*substvars* \
	         ${SOURCE_DIR}/debian/${PKG_NAME} \
	         ${SOURCE_DIR}/debian/changelog \
	         ${SOURCE_DIR}/debian/files \
	         ${SOURCE_DIR}/rainbowc \
	         ${DOC_DIR}
