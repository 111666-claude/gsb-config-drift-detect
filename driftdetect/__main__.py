"""命令行入口。"""

import argparse
import csv

from . import core, samples


def _read_csv(path):
    rows = []
    with open(path, "r", encoding="utf-8", newline="") as fh:
        for item in csv.DictReader(fh):
            rows.append({"source": item["source"], "key": item["key"], "value": item["value"]})
    return rows


def main(argv=None):
    ap = argparse.ArgumentParser(prog="driftdetect")
    sub = ap.add_subparsers(dest="cmd")

    p_rep = sub.add_parser("report")
    p_rep.add_argument("--csv", required=True)
    p_rep.add_argument("--source", action="append", required=True)

    p_demo = sub.add_parser("demo")
    p_demo.add_argument("--name", required=True)

    args = ap.parse_args(argv)

    if args.cmd == "report":
        rows = _read_csv(args.csv)
        table = core.detect(rows, args.source, core.Counter())
        print(core.render(table, args.source))
        return 0
    if args.cmd == "demo":
        return samples.run(args.name)

    ap.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
