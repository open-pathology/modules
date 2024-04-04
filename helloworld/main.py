import json
import sys
from argparse import ArgumentParser
from pathlib import Path

import numpy
from PIL import Image
from skimage.filters import threshold_otsu
from tifffile import TiffFile


def make_mask(wsi, output, threshold):
    """Generate mask bitmap and associated report using tiles compressed size."""

    # create mask
    with TiffFile(wsi) as tif:
        page = tif.pages[0]

        # figure out how tiles are organized
        h, w, _ = page.shape
        tx, ty = page.tilewidth, page.tilelength
        dx = (w + tx - 1) // tx
        dy = (h + ty - 1) // ty

        # use compressed size as pixels
        tiles = numpy.reshape(page.databytecounts, (dy, dx))

        # assume only tiles above the threshold are foreground
        mask = tiles >= threshold_otsu(tiles)
        png = f"{wsi.stem}.png"
        Image.fromarray(mask).save(Path(output, png))

    # create analysis response
    sz = dx * dy
    nz = int(mask.sum())
    fg = nz / sz
    ok = fg >= threshold
    return {
        "$mask": png,
        "coverage": {
            "size": sz,
            "mask": nz,
            "area": fg,
            "%": f"{fg*100:.2f}",
            "present": ok,
        },
    }


def main(lines, threshold):
    """Produce quick and dirty foreground mask for each requests."""

    for line in lines:
        request = json.loads(line)
        try:
            results = make_mask(
                Path(request["inputs"]["wsi"]),
                Path(request["outputs"]),
                threshold,
            )
            print(json.dumps({"id": request["id"], "results": results}))
        except Exception as err:
            print(json.dumps({"id": request["id"], "error": repr(err)}))


if __name__ == "__main__":
    p = ArgumentParser()
    p.add_argument("--threshold", type=float, default=0.01)
    args = p.parse_args()
    main(sys.stdin, **vars(args))
