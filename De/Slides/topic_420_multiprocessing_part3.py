#!/usr/bin/env python
# coding: utf-8

# <img src="img/python-logo-notext.svg"
#      style="display:block;margin:auto;width:10%"/>
# <br>
# <div style="text-align:center; font-size:200%;"><b>Multiprocessing (Part 3)</b></div>
# <br/>
# <div style="text-align:center;">Dr. Matthias Hölzl</div>

# In[ ]:


def perform_computation(x):
    return 2 * x ** 2 + 1


# In[ ]:


if __name__ == "__main__":
    print("List comprehension:")
    print([perform_computation(x) for x in [1, 2, 3]])


# In[ ]:


if __name__ == "__main__":
    print("Map")
    print(list(map(perform_computation, [1, 2, 3])))


# In[ ]:


from multiprocessing import Pool


# In[ ]:


if __name__ == "__main__":
    print("Map with process pool")
    with Pool(processes=4) as p:
        print(p.map(perform_computation, [1, 2, 3]))

