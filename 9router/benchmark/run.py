"""Benchmark de modelos 9router via opencode. Stdlib only.
Uso: python run.py [--modelos a,b] [--categorias x,y] [--repeticoes N] [--retomar]"""
import argparse, csv, glob, json, os, re, shutil, subprocess, sys, time
from datetime import datetime

AQUI = os.path.dirname(os.path.abspath(__file__))
CSV = os.path.join(AQUI, "resultados.csv")
CAMPOS = "modelo,categoria,tarefa,passou,segundos,tool_calls,limite,erro,timestamp".split(",")
TIMEOUT = 240
OPENCODE = shutil.which("opencode.cmd") or shutil.which("opencode") or "opencode"


def san(s):
    return re.sub(r"[^A-Za-z0-9._-]+", "_", s)


def carregar_tarefas(cats):
    out = []
    for p in sorted(glob.glob(os.path.join(AQUI, "tarefas", "*", "*.json"))):
        cat = os.path.basename(os.path.dirname(p))
        if cats and cat not in cats:
            continue
        with open(p, encoding="utf-8") as f:
            out.append((cat, os.path.splitext(os.path.basename(p))[0], json.load(f)))
    return out


def rodar_opencode(modelo, prompt, wd):
    """Retorna (texto, tool_calls, erro, limite, segundos)."""
    t0 = time.time()
    # prompt via stdin: evita problemas de aspas/newline no cmd.exe
    p = subprocess.Popen([OPENCODE, "run", "-m", "9router/" + modelo, "--format", "json"], cwd=wd,
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         encoding="utf-8", errors="replace")
    estourou = False
    try:
        out, err = p.communicate(prompt, timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        estourou = True
        subprocess.run(["taskkill", "/T", "/F", "/PID", str(p.pid)], capture_output=True)  # mata a arvore
        out, err = p.communicate()
    seg = time.time() - t0
    texto, tools, erro = [], 0, ""
    for ln in (out or "").splitlines():
        try:
            ev = json.loads(ln)
        except ValueError:
            continue
        t = str(ev.get("type", ""))
        if t == "text":
            texto.append((ev.get("part") or {}).get("text", ""))
        elif t == "error":
            e = ev.get("error", ev)
            erro = e if isinstance(e, str) else json.dumps(e, ensure_ascii=False)
            d = e.get("data") if isinstance(e, dict) else None
            if isinstance(d, dict) and d.get("message"):
                erro = f"{e.get('name', '')}: {d['message']}"
        elif "tool" in t:
            tools += 1
    if estourou:
        erro = erro or "timeout"
    elif not erro and p.returncode and not texto:
        erro = f"exit {p.returncode}: {(err or '').strip()[-200:]}"
    low = erro.lower()
    limite = int("usage limit" in low or "429" in low or "rate limit" in low or "rate-limit" in low)
    return "".join(texto).strip(), tools, erro.replace("\n", " ")[:300], limite, seg


def checar(check, texto, wd, originais):
    # corpus: texto final + arquivos novos/modificados (os de entrada nao contam)
    corpus = texto
    for nome in os.listdir(wd):
        fp = os.path.join(wd, nome)
        if os.path.isfile(fp) and not nome.startswith("_teste"):
            with open(fp, encoding="utf-8", errors="replace") as f:
                conteudo = f.read()
            if originais.get(nome) != conteudo:
                corpus += "\n" + conteudo
    for c in (check if isinstance(check, list) else [check]):
        t = c["tipo"]
        if t == "regex_all":
            ok = all(re.search(x, corpus) for x in c["padroes"])
        elif t == "regex_none":
            ok = not any(re.search(x, corpus) for x in c["padroes"])
        elif t == "json_keys":
            try:
                d = json.loads(texto)
            except ValueError:
                return False
            ok = isinstance(d, dict) and all(k in d for k in c.get("chaves", [])) and \
                all(d.get(k) == v for k, v in c.get("valores", {}).items())
        elif t == "python_assert":
            with open(os.path.join(wd, "_teste.py"), "w", encoding="utf-8") as f:
                f.write(c["teste"])
            try:
                ok = subprocess.run([sys.executable, "_teste.py"], cwd=wd, capture_output=True, timeout=30).returncode == 0
            except subprocess.TimeoutExpired:
                ok = False
        else:
            raise ValueError("check desconhecido: " + t)
        if not ok:
            return False
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--modelos")
    ap.add_argument("--categorias")
    ap.add_argument("--repeticoes", type=int, default=1)
    ap.add_argument("--retomar", action="store_true")
    a = ap.parse_args()
    if a.modelos:
        modelos = [m.strip() for m in a.modelos.split(",") if m.strip()]
    else:
        with open(os.path.join(AQUI, "modelos.txt"), encoding="utf-8") as f:
            modelos = [l.strip() for l in f if l.strip() and not l.startswith("#")]
    cats = [c.strip() for c in a.categorias.split(",")] if a.categorias else None
    tarefas = carregar_tarefas(cats)

    feitos = set()
    if a.retomar and os.path.exists(CSV):
        with open(CSV, encoding="utf-8", newline="") as f:
            for r in csv.DictReader(f):
                if r["passou"] == "1" or (r["erro"] and r["limite"] != "1"):
                    feitos.add((r["modelo"], r["categoria"], r["tarefa"]))

    novo = not os.path.exists(CSV)
    with open(CSV, "a", encoding="utf-8", newline="") as fcsv:
        w = csv.writer(fcsv)
        if novo:
            w.writerow(CAMPOS)
            fcsv.flush()
        for m in modelos:
            seguidos = 0
            pular = False
            for cat, nome, t in tarefas:
                if pular:
                    break
                if (m, cat, nome) in feitos:
                    continue
                for _ in range(a.repeticoes):
                    wd = os.path.join(AQUI, "work", san(m), f"{cat}_{nome}")
                    shutil.rmtree(wd, ignore_errors=True)
                    os.makedirs(wd)
                    arqs = t.get("arquivos", {})
                    for fn, cont in arqs.items():
                        with open(os.path.join(wd, fn), "w", encoding="utf-8", newline="") as f:
                            f.write(cont)
                    texto, tools, erro, limite, seg = rodar_opencode(m, t["prompt"], wd)
                    passou = 0 if erro and not texto and not tools else int(checar(t["check"], texto, wd, arqs))
                    w.writerow([m, cat, nome, passou, round(seg, 1), tools, limite, erro,
                                datetime.now().isoformat(timespec="seconds")])
                    fcsv.flush()
                    print(f"{m} {cat}/{nome}: {'OK' if passou else 'FALHOU'} {seg:.0f}s tools={tools}"
                          + (f" erro={erro[:80]}" if erro else ""), flush=True)
                    seguidos = seguidos + 1 if limite else 0
                    if seguidos >= 2:
                        print(f"{m}: limite 2x seguidas, pulando o resto", flush=True)
                        w.writerow([m, "-", "-", 0, 0, 0, 1, "pulado: limite 2x seguidas",
                                    datetime.now().isoformat(timespec="seconds")])
                        fcsv.flush()
                        pular = True
                        break


if __name__ == "__main__":
    main()
