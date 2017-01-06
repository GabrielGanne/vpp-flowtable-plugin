VERSION = 1.0
RELEASE = 0
SOURCES_ARCHIVE_NAME = vpp-flowtable-plugin-$(VERSION)

sources-archive:
	echo $(SOURCES_ARCHIVE_NAME)
	git archive --format tar \
		--prefix $(SOURCES_ARCHIVE_NAME)/ \
		HEAD  | gzip -9 > $(SOURCES_ARCHIVE_NAME).tar.gz

flowtable-rpm: sources-archive
	- rpmbuild
	mv -v $(SOURCES_ARCHIVE_NAME).tar.gz $(shell rpmspec --eval='%{_sourcedir}')/
	rpmbuild -ba --clean \
		--define "_version $(VERSION)" \
		--define "_release $(RELEASE)" \
		flowtable-plugin/vpp-flowtable-plugin.spec

rpm: flowtable-rpm

.DEFAULT: rpm
