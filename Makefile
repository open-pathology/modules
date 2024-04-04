# XDG_DATA_HOME
# https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html
DATA=$(if $(XDG_DATA_HOME),$(XDG_DATA_HOME)/testdata/wsi,$(HOME)/.local/share/testdata/wsi)

download: $(DATA)

URL=https://openslide.cs.cmu.edu/download/openslide-testdata/Aperio
$(DATA):
	mkdir -p $@
	@cd $@; $(foreach file,CMU-1.svs CMU-2.svs CMU-3.svs,curl -O $(URL)/$(file);)
