import random, time
from concurrent.futures import ProcessPoolExecutor, as_completed
import spherogram

PAIR_A = ((0, 1), (2, 3))
PAIR_B = ((0, 3), (1, 2))

def state_graph_info(pd_code, pairs):
    max_lbl = max(max(x) for x in pd_code)
    parent  = list(range(max_lbl + 1))
    rank    = [0]*(max_lbl + 1)
    comps   = len(parent)

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    def union(x, y):
        nonlocal comps
        rx, ry = find(x), find(y)
        if rx != ry:
            if rank[rx] < rank[ry]:
                parent[rx] = ry
            elif rank[rx] > rank[ry]:
                parent[ry] = rx
            else:
                parent[ry] = rx
                rank[rx] += 1
            comps -= 1

    i1,j1 = pairs[0]
    i2,j2 = pairs[1]
    for a,b,c,d in pd_code:
        union([a,b,c,d][i1], [a,b,c,d][j1])
        union([a,b,c,d][i2], [a,b,c,d][j2])

    has_loop = any(find(cross[i1]) == find(cross[j2]) for cross in pd_code)
    return comps, has_loop

def evaluate_pdcode():
    random.seed()
    try:
        link = spherogram.random_link(
            crossings=random.randint(20,40),
            num_components='any',
            consistent_twist_regions=True,
            simplify='basic'
        )
        pd  = [list(c) for c in link.PD_code()]
        c   = len(pd)

        # --- cheap tests first -----------------------------------------
        compA, loopA = state_graph_info(pd, PAIR_A)
        compB, loopB = state_graph_info(pd, PAIR_B)

        if not (loopA or loopB):                # adequate => reject
            return None

        gT = (c + 2 - compA - compB)//2
        if gT < 2:                              # want genus ≥2
            return None
        # ----------------------------------------------------------------

        # Jones polynomial check
        jp    = link.jones_polynomial()
        degs  = jp.dict().keys()
        span  = max(degs) - min(degs)

        if span in {2*c, 2*c-2}:                # easy alternating cases
            return None

        if span + 2*gT == 2*c:                  # final equality
            return pd
        return None
    except Exception:
        return None

def parallel_process_links(n_trials=10_000, workers=None,
                           outfile='interesting_links.txt'):
    found, results = 0, []
    with ProcessPoolExecutor(max_workers=workers) as pool:
        futs = [pool.submit(evaluate_pdcode) for _ in range(n_trials)]
        for fut in as_completed(futs):
            pd = fut.result()
            if pd:
                found += 1
                results.append(pd)
                print(f'✔ found (c={len(pd)})')

    if results:
        with open(outfile,'a') as f:
            for pd in results:
                f.write(str(pd)+'\n')
    print(f'Total qualifying diagrams: {found}')

if __name__ == '__main__':
    t0 = time.time()
    parallel_process_links(n_trials=10000, workers=None)
    print(f'Finished in {time.time()-t0:.2f} s')
