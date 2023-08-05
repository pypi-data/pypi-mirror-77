# agrox
a web enum python module

### Install
* pip install AGROX

### fuzzing Example 
```python
from argox.argo import Argo

argo = Argo("https://github.com/PUFF")
data = argo.fuzzer()
print(data)

```

### Dns Enum Example 
```python
from argox.argo import Argo

argo = Argo("https://github.com")
print(argo.DnsEnum())
```

### portscan Example 
```python
from argox.argo import Argo

def scan(host):
    argo = Argo("https://github.com")
    return argo.scanport(host,debug=False)

host = input("Enter host ip")
print(scan(host))

```
