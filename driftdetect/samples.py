"""固定场景，用来复现题面里的锚点。"""

import json

from . import core


def _r(source, key, value):
    return {"source": source, "key": key, "value": value}


def run(name):
    if name == "onlyone":
        rows = [_r("dev", "a", "1"), _r("staging", "b", "2")]
        table = core.detect(rows, ["dev", "staging"], core.Counter())
        print(core.render(table, ["dev", "staging"]))
        return 0
    if name == "dup":
        rows = [_r("dev", "a", "1"), _r("dev", "a", "2"), _r("staging", "a", "2")]
        table = core.detect(rows, ["dev", "staging"], core.Counter())
        print(core.render(table, ["dev", "staging"]))
        return 0
    if name == "emptymissing":
        rows = [_r("dev", "a", "")]
        table = core.detect(rows, ["dev", "staging"], core.Counter())
        print(core.render(table, ["dev", "staging"]))
        return 0
    if name == "space":
        rows = [_r("dev", "a", "1"), _r("staging", "a", "1 ")]
        table = core.detect(rows, ["dev", "staging"], core.Counter())
        print(core.render(table, ["dev", "staging"]))
        return 0
    if name == "work":
        rows = []
        for i in range(2000):
            rows.append(_r("dev", "k%04d" % i, str(i)))
            rows.append(_r("staging", "k%04d" % i, str(i)))
        counter = core.Counter()
        core.detect(rows, ["dev", "staging"], counter)
        print(json.dumps({"keys": 2000, "scanned": counter.scanned}))
        return 0
    raise SystemExit("未知场景：" + name)
