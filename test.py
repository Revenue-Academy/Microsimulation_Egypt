import json 

with open('tax_incentives_benchmark.json') as f:
    vars = json.load(f)
#record_vars_sorted = dict(sorted(record_vars.items()))
vars_list = []
for k, s in vars.items():
    print(s)
    for x, y in s.items():
        print(x)
