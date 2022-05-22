# %%
import sys
import gc

# %%
sys.getsizeof("")

# %%
sys.getsizeof("a")

# %%
sys.getsizeof("ab")

# %%
sys.getsizeof("abc")

# %%
sys.getsizeof("äöü")

# %%
sys.getsizeof([])

# %%
sys.getsizeof([""])

# %%
sys.getsizeof(["a"])

# %%
sys.getsizeof(["ab"])

# %%
sys.getsizeof(["a", "b"])

# %%
sys.getsizeof(["a", "b", "c"])

# %%
sys.getsizeof(["a", "b", "c", "d", "e"])

# %%
sys.getsizeof(["a" * 100, "b" * 100, "c" * 100, "d" * 100, "e" * 100])

# %%
def compute_total_size(obj, output=True):
    def pr(*args, **kwargs):
        if output:
            print(*args, **kwargs)

    seen_ids = set()
    computed_size = 0
    worklist = [obj]
    while worklist:
        pr(f"Worklist: {repr(worklist)[:72]}")
        current = worklist.pop()
        if id(current) in seen_ids:
            continue
        seen_ids.add(id(current))
        current_size = sys.getsizeof(current)
        computed_size += current_size
        pr(f"  Current item:        {repr(current)[:59]}")
        pr(f"  Current item size:   {current_size}")
        pr(f"  Computed total size: {computed_size}")
        worklist.extend(gc.get_referents(current))
    return computed_size


# %%
compute_total_size("", output=True)

# %%
compute_total_size("a")

# %%
compute_total_size("ab")

# %%
compute_total_size("abc")

# %%
compute_total_size("äöü")

# %%
compute_total_size([])

# %%
compute_total_size([""])

# %%
compute_total_size(["a"])

# %%
compute_total_size(["ab"])

# %%
compute_total_size(["a", "b"])

# %%
compute_total_size(["a", "b", "c"])

# %%
compute_total_size(["a", "b", "c", "d", "e"])

# %%
compute_total_size(["a" * 20, "b" * 20, "c" * 20, "d" * 20, "e" * 20])

# %%
my_list = [1, 2, 3, 4]
your_list = [1, my_list, my_list, 2, 3, 4, 5]
compute_total_size(your_list)

# %%
compute_total_size([1, [1, 2, 3, 4], [1, 2, 3, 4], 2, 3, 4, 5])

# %%
print(compute_total_size(my_list, False) - 4 * compute_total_size(1, False))
print(compute_total_size(your_list, output=False))
print(compute_total_size([1, [1, 2, 3, 4], [1, 2, 3, 4], 2, 3, 4, 5], output=False))

# %%
