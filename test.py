import dpath

myobject = {"key1": "value1", "key2": {"dict2": "hello", "wor/ld": {"dfg": 12}}}

print(
    [
        x[0].split(";")[-1]
        for x in dpath.search(myobject, "**", yielded=True, separator=";")
    ]
)
