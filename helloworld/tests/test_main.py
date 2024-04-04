import json
from pathlib import Path

from main import main


def test_mask(tmp_path, capsys):
    tests = ["CMU-1.svs", "CMU-2.svs", "CMU-3.svs"]

    # create a batch of requests
    lines = []
    for i, name in enumerate(tests):
        out = Path(tmp_path, str(i))
        out.mkdir()
        req = dict(id=str(i), inputs={"wsi": f"/wsi/{name}"}, outputs=str(out))
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
    data = Path(__file__).parent / "data"
    for i, line in enumerate(results):
        rep = json.loads(line)
        res = rep["results"]
        ref = Path(data, tests[i]).with_suffix(".json")
        png = Path(data, tests[i]).with_suffix(".png")
        out = Path(tmp_path, str(i))
        assert rep["id"] == str(i)
        assert rep["results"] == json.loads(ref.read_text())
        assert png.read_bytes() == Path(out, res["$mask"]).read_bytes()
