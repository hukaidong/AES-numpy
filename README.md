# AES-numpy

An AES (Advanced Encryption Standard) implementation based on numpy.

## Usage

Command line demostration:

```shell
>>> python example.py
Data you want to encrypt:
aabbccddeeffgghhiijjkkllmmnnooppqqrrssttuuvvwwxxyyzz
b"aabbccddeeffgghhiijjkkllmmnnooppqqrrssttuuvvwwxxyyzz"
```

As library:

```python
from aes import aes_encrypt, aes_decrypt

# Key MUST be a 16 bytes string.

encrypted = aes_encrypt("DATA", "KEY")
data = aes_decrypt("ENCRYPTED", "KEY")
```
