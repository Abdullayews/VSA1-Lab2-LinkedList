import csv
import os
import platform
import statistics
import sys
import time

from playlist import Playlist
from undo_stack import UndoStack
from print_queue import PrintQueue

SIZES = [100, 1000, 10000]
REPEATS = 5
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "test_results")


def timed(fn):
    t = time.perf_counter()
    fn()
    return (time.perf_counter() - t) * 1000.0  # ms


def median_ms(fn_setup, fn_run):
    vals = []
    for _ in range(REPEATS):
        ctx = fn_setup()
        vals.append(timed(lambda: fn_run(ctx)))
    return statistics.median(vals)


def build_playlist(n):
    pl = Playlist()
    for i in range(n):
        pl.addSong(i, f"Song{i}", "Artist", "3:30")
    return pl


def bench_playlist():
    rows = []
    for n in SIZES:
        # Insert: N emeliyyatin umumi vaxti
        ins = median_ms(Playlist, lambda pl: [pl.addSong(i, f"Song{i}", "A", "3:30") for i in range(n)])
        # Search: en pis hal (sonuncu element), 1 emeliyyat ucun orta vaxt
        pl = build_playlist(n)
        reps = 50
        srch = timed(lambda: [pl.searchSong(n - 1) for _ in range(reps)]) / reps
        # Delete: en pis hal (sonuncu element), sonra yeniden elave olunur (olcuye daxil deyil)
        dels = []
        for _ in range(reps):
            dels.append(timed(lambda: pl.deleteSong(n - 1)))
            pl.addSong(n - 1, "x", "A", "3:30")
        rows.append([n, round(ins, 4), round(srch, 6), round(statistics.median(dels), 6)])
    return rows


def bench_stack():
    rows = []
    for n in SIZES:
        push = median_ms(UndoStack, lambda s: [s.pushAction(i, "act") for i in range(n)])

        def setup():
            s = UndoStack()
            for i in range(n):
                s.pushAction(i, "act")
            return s

        pop = median_ms(setup, lambda s: [s.undoAction() for _ in range(n)])
        rows.append([n, round(push, 4), round(pop, 4)])
    return rows


def bench_queue():
    rows = []
    for n in SIZES:
        enq = median_ms(PrintQueue, lambda q: [q.enqueue(i, "S", 1) for i in range(n)])

        def setup():
            q = PrintQueue()
            for i in range(n):
                q.enqueue(i, "S", 1)
            return q

        deq = median_ms(setup, lambda q: [q.dequeue() for _ in range(n)])
        pk = median_ms(setup, lambda q: [q.peek() for _ in range(n)])
        rows.append([n, round(enq, 4), round(deq, 4), round(pk, 4)])
    return rows


def save(name, header, rows):
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, name), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
    print("\n" + name)
    print(" | ".join(header))
    for r in rows:
        print(" | ".join(str(x) for x in r))


def plot(name, title, xlabel, ylabel, header, rows):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib tapilmadi: pip install matplotlib")
        return
    plt.figure()
    xs = [r[0] for r in rows]
    for i in range(1, len(header)):
        plt.plot(xs, [r[i] for r in rows], marker="o", label=header[i])
    plt.xscale("log")
    plt.yscale("log")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True, which="both", alpha=0.3)
    plt.legend()
    plt.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close()


def main():
    print("Sistem melumatlari (avtomatik):")
    print("OS:", platform.platform())
    print("CPU:", platform.processor() or platform.machine())
    print("Python:", sys.version.split()[0], platform.python_implementation())
    print("CPU cores:", os.cpu_count())
    print("RAM, GPU, Computer Model, Storage, Power Mode: manual doldurun")

    h1 = ["Element sayi", "Insert (ms)", "Search (ms)", "Delete (ms)"]
    r1 = bench_playlist()
    save("task1_playlist.csv", h1, r1)
    plot("task1_graph.png", "Playlist (Linked List)", "Element sayi", "Icra muddeti (ms)", h1, r1)

    h2 = ["Emeliyyat sayi", "Push (ms)", "Pop (ms)"]
    r2 = bench_stack()
    save("task2_stack.csv", h2, r2)
    plot("task2_graph.png", "Undo History (Stack)", "Emeliyyat sayi", "Icra muddeti (ms)", h2, r2)

    h3 = ["Element sayi", "Enqueue (ms)", "Dequeue (ms)", "Peek (ms)"]
    r3 = bench_queue()
    save("task3_queue.csv", h3, r3)
    plot("task3_graph.png", "Print Queue (Queue)", "Element sayi", "Icra muddeti (ms)", h3, r3)


if __name__ == "__main__":
    main()
