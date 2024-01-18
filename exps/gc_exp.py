import gc

def hello_references():
    print("function called")
    
rs = gc.get_referrers(hello_references)

del hello_references

gc.collect()

for i in rs:
    print(i)