# %% [markdown]
#
# # Example for "scientific mode"


# %% [markdown]
# ## A plot
# 
# Let's plot something.

# %%
import numpy as np
import matplotlib.pyplot as plt

# %%
page_load_time = np.random.normal(3.0, 1.0, 100)
purchase_amount = np.random.normal(50.0, 1.5, 100) - page_load_time

# %%
plt.figure(figsize=(12, 8))
plt.scatter(page_load_time, purchase_amount)
plt.show()

# %% [markdown]
# ## Another plot
# 
# And a nice function.

# %%
x = np.linspace(-4.0, 5.0, 200)
y = x ** 3 -  x ** 2 - 8 * x + 20
plt.plot(x, y)
plt.show()

# %%
