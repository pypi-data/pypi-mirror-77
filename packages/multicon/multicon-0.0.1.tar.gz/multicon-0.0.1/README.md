# multicon
A tiny module for joining multiple configs into one.

## Usage
```python
import multicon

c1 = {
	'a': 123,
	'b': 256,
	'c': [1, 2, 3],
	'd': {
		'da': 1,
		'db': 2,
		'dc': 3,
		'dd': {
			'dda': 997
		}
	}
}

c2 = {
	'b': 112,
	'e': 9427
}

c = Config(c1, c2)
print(dict(c))
```

```python
import multicon

c1 = {
	'a': 123,
	'b': 256,
	'c': [1, 2, 3],
	'd': {
		'da': 1,
		'db': 2,
		'dc': 3,
		'dd': {
			'dda': 997
		}
	}
}

c2 = {
	'b': 112,
	'e': 9427
}

c3 = {
	'd': {
		'db': 18,
		'dd': [1, 2, 3, 4, 5, 6, 7],
	}
}

multiconfig = multicon.MultiConfig([c1, c2, c3], {})
try:
	print(multiconfig['a'])
	print(multiconfig['b'])
	print(multiconfig['c'])
	print(multiconfig['d'])
	print(multiconfig['dd'])
except multicon.ConfigKeyNotExistError:
	print('Key not exist')

```
