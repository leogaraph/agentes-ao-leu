"""Resumo de resultados.csv: modelo x categoria e top 3 por categoria."""
import csv, os
from collections import defaultdict
from statistics import median

p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resultados.csv")
with open(p, encoding="utf-8", newline="") as f:
    rows = [r for r in csv.DictReader(f) if r["categoria"] != "-"]
g = defaultdict(list)
for r in rows:
    g[(r["modelo"], r["categoria"])].append(r)


def stats(rs):
    return (sum(int(r["passou"]) for r in rs) / len(rs), median(float(r["segundos"]) for r in rs),
            median(int(r["tool_calls"]) for r in rs), sum(int(r["limite"]) for r in rs))


cats = sorted({c for _, c in g})


def geral(m):
    rs = [r for c in cats for r in g.get((m, c), [])]
    return -sum(int(r["passou"]) for r in rs) / max(1, len(rs)), m


modelos = sorted({m for m, _ in g}, key=geral)
print("modelo x categoria: acerto / tempo mediano / tool_calls mediano / limites")
print(f"{'modelo':42}" + "".join(f"{c:>24}" for c in cats))
for m in modelos:
    cel = []
    for c in cats:
        if (m, c) in g:
            a, t, tc, l = stats(g[(m, c)])
            cel.append(f"{a*100:.0f}%/{t:.0f}s/{tc:.0f}tc/{l}L")
        else:
            cel.append("-")
    print(f"{m:42}" + "".join(f"{x:>24}" for x in cel))
for c in cats:
    top = sorted(((stats(g[(m, c)]), m) for m in modelos if (m, c) in g), key=lambda x: (-x[0][0], x[0][1]))[:3]
    print(f"\nTop 3 {c}:")
    for i, ((a, t, tc, l), m) in enumerate(top, 1):
        print(f"  {i}. {m}  {a*100:.0f}%  {t:.0f}s")
