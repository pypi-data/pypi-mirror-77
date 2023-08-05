# qdill

a VERY minimal python convenience library for dill

are you **tired** of writing `with open(...) as f` every time you try and use pickle/dill as you're hacking something together in python?

this is the library for you.

it defines some simple functions over dill so that you can just do

`var = qdill.load(filename)`  
OR  
`qdill.save(thing, filename)`

There's also a third `defaultLoad` function.  

It checks if the file exists, and if the file doesn't exist, it saves the default thing to the file AND returns the default thing.
i.e. `var = qdill.defaultLoad(default_thing, filename)`

you can read the code. it's all just ~25 lines in the `__init__.py`

**if you need more fine-grained control of dill...**  
_Don't use this 'library'_