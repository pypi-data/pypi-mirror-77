# Unimatrix Crypto

A Python library that provides abstract around various primitives
for cryptographic operations.

Supported cryptographic implementations are:

- RSA PKCS1.5/SHA256


Supported key providers are:

- Local
- Google Cloud KMS


## Installation

```
pip install unimatrix.ext.crypto
```

## Usage

```
import os

from unimatrix.ext.crypto.lib.google import Signer


signer = Signer(resource_id="your/kms/key/resource/id")
some_data_to_sign = os.urandom(256)
sig = signer.sign(some_data_to_sign)

print(sig.verify(signer.public, some_data_to_sign))
```
