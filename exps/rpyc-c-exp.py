import rpyc

conn = rpyc.connect("localhost", 18861)
result = conn.root.exposed_add(10, 20)
print("Result:", result)
conn.close()