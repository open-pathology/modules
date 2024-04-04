IMAGE=helloworld

# this uses the host pip configuration when available for building the docker image
PIP_CONFIG=$(HOME)/.config/pip/pip.conf
PIP_SECRET=--secret id=pip,src=$(PIP_CONFIG)
PIP=$(if $(wildcard $(PIP_CONFIG)),$(PIP_SECRET))

IMAGE_MAIN=$(IMAGE)
image-main:
	@docker build $(PIP) --target main -t $(IMAGE_MAIN) .

IMAGE_TEST=$(IMAGE):test
image-test:
	@docker build $(PIP) --target test -t $(IMAGE_TEST) .

test: image-test
	@docker run -ti --rm -v $(WSI):/wsi:ro $(IMAGE_TEST) \
		pytest -s

lint: image-test
	@docker run -ti --rm $(IMAGE_TEST) \
		ruff check

# this runs the docker container to produce test results
UID=$(shell id -u)
WSI=$(PWD)/../data/wsi
gold: image-main
	@docker run -ti --rm -v $(WSI):/wsi:ro -v $(PWD):/out -w /out -u $(UID):$(UID) $(IMAGE_MAIN) \
		bash -c "cat tests/data/samples.jsonl | python3 /src/main.py"
