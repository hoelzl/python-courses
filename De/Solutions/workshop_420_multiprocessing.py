#!/usr/bin/env python
# coding: utf-8

# 
# # Monte-Carlo Methoden
# 
# Monte-Carlo Methoden sind statistische Berechnungen, die wiederholte Berechnungen mit
# Zufallszahlen verwenden, um numerische Ergebnisse zu erhalten. In dieser Aufgabe
# wollen wir die Zahl $\pi$ mit Monte-Carlo Methoden berechnen. Der Grundgedanke ist
# folgender:
# 
# - $\pi$ entspricht dem Flächeninhalt eines Kreises mit Radius 1.
# - Wir erzeugen zwei Zufallszahlen $x$ und $y$, die jeweils zwischen 0 und 1 liegen.
# - Wir berechnen $x^2 + y^2$ und testen, ob der Wert $\leq 1$ ist. In diesem Fall
#   liegt der Punkt $(x, y)$ im Kreis mit Radius 1 um den Ursprung andererseits nicht.
# - Wir führen diese Berechnung sehr oft durch, und zählen, welcher Prozentsatz der
#   Punkte im Kreis liegt.
# - Da alle Punkte im ersten Quadranten liegen, erhalten wir eine Approximation von
#   $\pi$ indem wir das Ergebnis mit 4 multiplizieren.
# 

# 
# Die folgende Funktion erzeugt einen Punkt $(x, y)$ wie beschrieben:

# In[2]:


from random import random


def get_random_point():
    return random(), random()


# In[3]:


get_random_point()


# 
# Implementieren Sie eine Funktion `is_in_circle(x, y)`, die überprüft, ob ein
# derartiger Punkt innerhalb des Kreises mit Radius 1 liegt.

# In[5]:


def is_in_circle(x, y) -> bool:
    return x ** 2 + y ** 2 <= 1


# In[7]:


is_in_circle(0.9, 0.9)


# In[8]:


is_in_circle(0.25, 0.3)


# 
# Implementieren Sie eine Funktion `is_random_point_in_circle()`, die überprüft, ob ein
# zufällig gewählter Punkt innerhalb des Kreises mit Radius 1 liegt.

# In[10]:


def is_random_point_in_circle() -> bool:
    return is_in_circle(*get_random_point())


# In[33]:


is_random_point_in_circle()


# 
# Wie können Sie die oben beschriebene Methode anzuwenden um $\pi$ zu berechnen?
# Implementieren Sie eine sequentielle Version unter Zuhilfenahme von
# `is_random_point_in_circle()` und mindestens eine parallele Version. Testen Sie die
# Performance verschiedener Vorgehensweisen.

# In[34]:


def compute_pi_sequentially(num_iterations):
    result = []
    for _ in range(num_iterations):
        result.append(is_random_point_in_circle())
    return 4 * sum(result) / len(result)


# In[37]:


NUM_ITERATIONS = 10_000_000


# In[38]:


# if __name__ == "__main__":
#     print("Sequential value:")
#     print(compute_pi_sequentially(NUM_ITERATIONS))


# In[39]:


from timeit import timeit

# if __name__ == "__main__":
#     print("Sequential:")
#     print(timeit(lambda: compute_pi_sequentially(NUM_ITERATIONS), number=5))


# In[ ]:


from multiprocessing import Pool


def bad_parallel_version(num_iterations):
    points = (get_random_point() for _ in range(num_iterations))
    with Pool(processes=16) as pool:
        result = list(pool.starmap(is_in_circle, points, chunksize=1000))
    return 4 * sum(result) / len(result)


# In[ ]:


if __name__ == "__main__":
    print("Bad parallel value:")
    print(bad_parallel_version(NUM_ITERATIONS))


# In[ ]:


if __name__ == "__main__":
    print("Bad parallel:")
    print(timeit(lambda: bad_parallel_version(NUM_ITERATIONS), number=5))


# In[ ]:


def better_parallel_version(num_iterations):
    num_processes = 16
    iterations_per_process = [num_iterations // num_processes] * num_processes
    with Pool(processes=num_processes) as pool:
        result = list(pool.imap(compute_pi_sequentially, iterations_per_process))
    return sum(result) / len(result)


# In[ ]:


if __name__ == "__main__":
    print("Better parallel value:")
    print(better_parallel_version(NUM_ITERATIONS))


# In[ ]:


if __name__ == "__main__":
    print("Better parallel:")
    print(timeit(lambda: better_parallel_version(NUM_ITERATIONS), number=5))

