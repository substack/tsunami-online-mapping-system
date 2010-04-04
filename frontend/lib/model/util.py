from elixir import *
# all columns are not nullable, which should be the default
Column = (lambda *args, **kwargs :
    Field(*args, **(dict([('nullable',False)] + kwargs.items())))
)
