# %%
class VarGetter:
    def get_var(self, name):
        import __main__
        if hasattr(__main__, name):
            return getattr(__main__, name)
        else:
            return "no value"


# %%
if __name__ == "__main__":
    var_getter = VarGetter()

# %%
if __name__ == "__main__":
    print(var_getter.get_var("my_var"))

# %%
if __name__ == "__main__":
    my_var = 123
    print(var_getter.get_var("my_var"))

# %%
