import random
from link_utils_faster import AdequateQ, TuraevGenus, Mirror  
import spherogram
import time

def generate_random_link(min_crossings=20, max_crossings=40):
    while True:
        try:
            
            link = spherogram.random_link(
            crossings= random.randint(min_crossings, max_crossings),  
            num_components='any',
            consistent_twist_regions=True,
            simplify='basic'
        )
            return link
        except Exception:
            continue

def get_pd_code(link):
    return [list(crossing) for crossing in link.PD_code()]

def jones_span(link):
    jp = link.jones_polynomial()
    degrees = list(jp.dict().keys())
    return max(degrees) - min(degrees)

def count_crossings(pdcode):
    return len(pdcode)

def is_valid_candidate(link, pdcode):
    sp = jones_span(link)
    c = count_crossings(pdcode)
    return sp == 2 * c or sp == 2 * c - 2

def save_pd_code(pdcode, filename="interesting_links.txt"):
    with open(filename, "a") as f:
        f.write(str(pdcode) + "\n")

def process_links(num_trials=100):
    for _ in range(num_trials):
        link = generate_random_link()
        pdcode = get_pd_code(link)
        if not is_valid_candidate(link, pdcode):
            continue

        if AdequateQ(pdcode):
            continue

        tg = TuraevGenus(pdcode)
        sp = jones_span(link)
        c = count_crossings(pdcode)

        if sp == 2 * c - 2 * tg:
            save_pd_code(pdcode)
            print(f"Found interesting PD code (c={c}, g_T={tg}, span={sp})")

if __name__ == "__main__":
    start = time.time()
    process_links(num_trials=100)
    end = time.time()
    print(f"Finished in {end - start:.2f} seconds.")
