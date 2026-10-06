"""多来源配置合并与漂移判定。"""

_MISSING = object()


class Counter:
    """记录比对过程中扫过的配置行数。"""

    def __init__(self):
        self.scanned = 0


def detect(rows, sources, counter):
    """返回发生漂移的键到各来源取值的映射。"""
    # 单次线性扫描：scanned 与输入行数成正比，不随键数平方级放大。
    values = {}
    conflicts = set()
    for r in rows:
        counter.scanned += 1
        src = r["source"]
        if src not in sources:
            continue
        key = r["key"]
        value = r["value"].strip()
        cell = values.setdefault(key, {})
        if src in cell:
            # 来源内重复：同一来源同一键出现不同取值，按漂移处理。
            if cell[src] != value:
                conflicts.add(key)
        else:
            cell[src] = value

    table = {}
    for key in sorted(values):
        cell = values[key]
        states = [cell.get(src, _MISSING) for src in sources]
        drift = key in conflicts
        if not drift:
            # 缺失也算一种取值，且与空串不同；比较前已去掉两端空白。
            first = states[0]
            drift = any(state is not first and state != first for state in states[1:])
        if drift:
            table[key] = {src: state for src, state in zip(sources, states)}
    return table


def render(table, sources):
    """把漂移表渲染成文本。"""
    # 列按来源名排序，行按键排序，缺失的来源显示为 <missing>。
    cols = sorted(sources)
    keys = sorted(table)
    display = {}
    for key in keys:
        row = table[key]
        display[key] = [
            "<missing>" if row.get(src, _MISSING) is _MISSING else row[src]
            for src in cols
        ]

    widths = [len("key")] + [len(src) for src in cols]
    for key in keys:
        widths[0] = max(widths[0], len(key))
        for i, text in enumerate(display[key]):
            widths[i + 1] = max(widths[i + 1], len(text))

    def fmt(cells):
        return " | ".join(
            text.ljust(widths[i]) for i, text in enumerate(cells)
        ).rstrip()

    lines = []
    lines.append(fmt(["key"] + cols))
    lines.append("-+-".join("-" * w for w in widths))
    for key in keys:
        lines.append(fmt([key] + display[key]))
    lines.append("drift=%d" % len(table))
    return "\n".join(lines)
