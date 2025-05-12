import random
import time
import spherogram
from link_utils_faster import AdequateQ, TuraevGenus, Mirror
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

def generate_random_pdcode(min_crossings=20, max_crossings=40):
    while True:
        try:
            link = spherogram.random_link(
                crossings= random.randint(min_crossings, max_crossings), 
                num_components='any',
                consistent_twist_regions=True,
                simplify='basic'
            )
            pdcode = [list(c) for c in link.PD_code()]
            jp = link.jones_polynomial()
            degrees = list(jp.dict().keys())
            span = max(degrees) - min(degrees)
            return pdcode, span
        except Exception:
            continue

def evaluate_pdcode(_):
    pdcode, span = generate_random_pdcode()
    c = len(pdcode)

    if not (span == 2 * c or span == 2 * c - 2):
        return None

    if AdequateQ(pdcode):
        return None

    tg = TuraevGenus(pdcode)
    if span == 2 * c - 2 * tg:
        return pdcode
    return None

def parallel_process_links(num_trials=100, workers=None, output_file="interesting_links.txt"):
    found = 0
    results = []

    with ProcessPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(evaluate_pdcode, _) for _ in range(num_trials)]
        for future in as_completed(futures):
            pdcode = future.result()
            if pdcode:
                results.append(pdcode)
                found += 1
                print(f"Found interesting PD code (c={len(pdcode)})")

    if results:
        with open(output_file, "a") as f:
            for pd in results:
                f.write(str(pd) + "\n")

    print(f"Total found: {found}")

if __name__ == "__main__":
    start = time.time()
    parallel_process_links(num_trials=1000, workers=None)  # use all cores
    end = time.time()
    print(f"Finished in {end - start:.2f} seconds.")
