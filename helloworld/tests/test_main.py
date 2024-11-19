import json
from pathlib import Path

from main import main


def test_mask(tmp_path, capsys):
    tests = ["CMU-1.svs", "CMU-2.svs", "CMU-3.svs", "missing"]

    # create a batch of requests
    lines = []
    for test in tests:
        out = Path(tmp_path, test)
        out.mkdir()
        req = dict(id=test, inputs={"wsi": f"/wsi/{test}"}, outputs=str(out))
        lines.append(json.dumps(req))

    # execute
    main(lines, threshold=0.01)

    # capture the output
    out, err = capsys.readouterr()
    assert len(out) != 0
    assert len(err) == 0
    results = out.splitlines()
    assert len(results) == len(tests)

    # validate results
    for test, result in zip(tests, results):
        data = Path(__file__).parent / "data" / test
        rep = json.loads(result)
        res = rep["results"]
        ref = Path(data, "output.json")
        png = Path(data, "mask.png")
        out = Path(tmp_path, test)
        assert rep["id"] == test
        assert rep["results"] == json.loads(ref.read_text())
        # if there was an error, there will be no output mask (for the time being)
        if "error" not in rep["results"]:
            assert png.read_bytes() == Path(out, res["$mask"]).read_bytes()
