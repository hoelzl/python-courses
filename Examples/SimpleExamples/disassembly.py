# %%
from dis import dis
import operator

# %%
b = 4
a = b

# %%
a, b

# %%
dis("a = b")

# %%
a = 3
b = 4
a = a + b

# %%
a, b

# %%
dis("a = a + b")

# %%
a = 3
b = 4
a = a.__add__(b)

# %%
a, b

# %%
dis("a.__add__(b)")

# %%
a = 3
b = 4
a += b

# %%
a, b

# %%
dis("a += b")

# See Python/ceval.c (~line 2448) for the implementation of INPLACE_ADD.
# Calls PyNumber_InPlaceAdd() if the arguments are not unicode characters.
# See Objects/abstract.c for details, in particular binary_iop1()
# The in-place operations fall back to the non-in-place ones, therefore the
# bytecode has to emit a STORE_NAME instruction anyway.

# %%
a = 3
b = 4
# tmp = a.__iadd__(b)
tmp = operator.iadd(a, b)

# %%
a, b, tmp

# %%
dis("operator.iadd(a, b)")


# %%
a = (3,)
b = (4,)
tmp = operator.iadd(a, b)

# %%
a, b, tmp

# %%
a = [3]
b = [4]
tmp = operator.iadd(a, b)

# %%
a, b, tmp

# %%
dis("a[2]")

# %%
dis("a[2] = 5")

# %%
dis("a[2] += 5")

# %%
