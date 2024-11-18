# XDG_DATA_HOME
# https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html
DATA_ROOT=$(or $(XDG_DATA_HOME),$(HOME)/.local/share)
WSI_ROOT=$(DATA_ROOT)/testdata/wsi

WSI_LIST=CMU-1.svs CMU-2.svs CMU-3.svs

download: $(foreach file,$(WSI_LIST),$(WSI_ROOT)/$(file))

URL=https://openslide.cs.cmu.edu/download/openslide-testdata/Aperio
$(WSI_ROOT)/%:
	@mkdir -p $(@D)
	curl $(URL)/$* -o $@
