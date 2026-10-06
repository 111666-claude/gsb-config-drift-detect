"""多来源配置合并与漂移判定。"""


_MISSING = object()


class Counter:
    """记录比对过程中扫过的配置行数。"""

    def __init__(self):
        self.scanned = 0


def detect(rows, sources, counter):
    """返回发生漂移的键到各来源取值的映射。"""
    values = {}
    repeated = set()
    for r in rows:
        counter.scanned += 1
        per_source = values.setdefault(r["key"], {})
        value = r["value"].strip()
        if r["source"] in per_source and per_source[r["source"]] != value:
            repeated.add(r["key"])
        per_source[r["source"]] = value
    table = {}
    for key, per_source in values.items():
        seen = {per_source.get(src, _MISSING) for src in sources}
        if len(seen) > 1 or key in repeated:
            table[key] = per_source
    return table


def render(table, sources):
    """把漂移表渲染成文本。"""
    sources = sorted(sources)
    header = ["key"] + list(sources)
    body = []
    for key in sorted(table):
        per_source = table[key]
        body.append([key] + [per_source.get(src, "<missing>") for src in sources])
    widths = [len(cell) for cell in header]
    for line in body:
        for i, cell in enumerate(line):
            widths[i] = max(widths[i], len(cell))

    def fmt(cells):
        return " | ".join(cell.ljust(widths[i]) for i, cell in enumerate(cells))

    lines = [fmt(header), " | ".join("-" * w for w in widths)]
    lines.extend(fmt(line) for line in body)
    lines.append("drift=%d" % len(table))
    return "\n".join(lines)
