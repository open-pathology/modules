download: data/wsi

URL=https://openslide.cs.cmu.edu/download/openslide-testdata/Aperio
data/wsi:
	mkdir -p $@
	@cd $@; $(foreach file,CMU-1.svs CMU-2.svs CMU-3.svs,curl -O $(URL)/$(file);)
