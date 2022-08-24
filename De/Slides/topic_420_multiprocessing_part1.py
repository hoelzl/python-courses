#!/usr/bin/env python
# coding: utf-8

# <img src="img/python-logo-notext.svg"
#      style="display:block;margin:auto;width:10%"/>
# <br>
# <div style="text-align:center; font-size:200%;"><b>Multiprocessing (Part 1)</b></div>
# <br/>
# <div style="text-align:center;">Dr. Matthias Hölzl</div>

# 
# # Multiprocessing
# 
# Beim Multiprocessing werden mehrere Python-Interpreter parallel ausgeführt, so dass
# mehrere Prozessor-Kerne genutzt werden können, da die verschiedenen Prozesse nicht
# durch ein GIL synchronisiert werden.
# 
# Allerdings wird die verwendung von gemeinsamen Daten zwischen den einzelnen Prozessen
# schwieriger (und potenziell ein Performance-Bottleneck).

# 
# Beim Multiprocessing gibt es einige Fallstricke; die [Programming
# Guidelines](https://docs.python.org/3/library/multiprocessing.html#programming-guidelines)
# in der Python Dokumentation sind hilfreich um sie zu vermeiden.

# In[ ]:


from os import getpid
from multiprocessing import Process


def print_message(task_id):
    print(f"Hello, from task {task_id}. PID is {getpid()}.", flush=True)


# In[ ]:


from threading import Thread


def run_threads():
    threads = [Thread(target=print_message, args=(i,)) for i in range(5)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()


# In[ ]:


if __name__ == "__main__":
    run_threads()


# In[ ]:


def run_processes():
    processes = [Process(target=print_message, args=(i,)) for i in range(5)]
    for process in processes:
        process.start()
    for process in processes:
        process.join()


# In[ ]:


if __name__ == "__main__":
    run_processes()


# In[ ]:




