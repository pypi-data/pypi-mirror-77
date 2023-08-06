# PyTCID

> :info: Unofficial Python API for verifying Turkish Identity Cards.

> :warning: This is **not** an official API.

This is an API Wrapper around the NVI ID Verification web services, one can use this package to
verify a Government Issued Citizenship Card.

Install it by:

```shell script
pip install pytcid
```

```python
import tcid
tcid.verify_national_id(12345678900, 'Name', 'Document No', 1900, birth_day=0, birth_month=0, surname='Surname')
```

Some national ID cards do not cary the optional keyword arguments, therefore, if the ID card you are
verifying does not carry information about the birth date, birth month or the surname, you may omit
these details. If the card **does** cary this information, you must provide it for successful verification.

