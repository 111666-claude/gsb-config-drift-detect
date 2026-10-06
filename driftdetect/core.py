"""多来源配置合并与漂移判定。"""


class Counter:
    """记录比对过程中扫过的配置行数。"""

    def __init__(self):
        self.scanned = 0


def detect(rows, sources, counter):
    """返回发生漂移的键到各来源取值的映射。"""
    first = sources[0]
    keys = []
    for r in rows:
        counter.scanned += 1
        if r["source"] == first and r["key"] not in keys:
            keys.append(r["key"])
    table = {}
    for key in keys:
        values = {}
        for src in sources:
            values[src] = ""
            for r in rows:
                counter.scanned += 1
                if r["source"] == src and r["key"] == key:
                    values[src] = r["value"]
        if len(set(values.values())) > 1:
            table[key] = values
    return table


def render(table, sources):
    """把漂移表渲染成文本。"""
    lines = []
    for key in table:
        lines.append(" ".join([key] + [table[key].get(src, "") for src in sources]))
    lines.append("drift=%d" % len(table))
    return "\n".join(lines)
