# %% [markdown] lang="de" tags=["subslide"]
#
# ## Truthiness
#
# Die `if`-Anweisung kann als Argument beliebige Python-Werte bekommen,
# nicht nur Boolesche Werte.
#
#  Folgende Werte gelten als *nicht wahr*
#
#  - `None` und `False`
#  - `0` und `0.0` (und Null-Werte von anderen Zahlentypen)
#  - Leere Strings, Sequences und Collections: ``
#
#  Alle anderen Werte gelten als wahr.

# %% [markdown] lang="en" tags=["subslide"]
#
# ## Truthiness
#
# The `if` statement can take any Python value as an argument,
# not just Boolean values.
#
#  The following values are considered *not true*
#
#  - `None` and `False`
#  - `0` and `0.0` (and null values of other number types)
#  - Empty strings, sequences and collections: ``
#
#  All other values are considered true.


# %% tags=["subslide", "keep"]
def check(value):
    if value:
        print(f"{value} is truthy.")
    else:
        print(f"{value} is falsy.")


# %%
check(True)

# %%
check(False)

# %% tags=["subslide"]
check(None)

# %%
check(0)

# %%
check(1)

# %% tags=["subslide"]
check("")

# %%
check("123")

# %%
check([])

# %%
check([1, 2, 3])
