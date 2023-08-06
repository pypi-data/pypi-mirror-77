# crudlib
*One API, More Database.*

[![Build Status](https://github.com/zxyle/crudlib/workflows/Python%20package/badge.svg)](https://github.com/zxyle/crudlib/actions?query=workflow%3A%22Python+package%22)
[![pypi version](https://img.shields.io/pypi/v/crudlib.svg)](https://pypi.org/project/crudlib/)
[![GitHub license](https://img.shields.io/github/license/zxyle/crudlib.svg)](https://github.com/zxyle/crudlib/blob/master/LICENSE)
[![Documentation Status](https://readthedocs.org/projects/crudlib/badge/?version=latest)](https://crudlib.readthedocs.io/en/latest/?badge=latest)

Implement a set of interfaces to operate databases such as MySQL and MariaDB.
His goal is not to build a powerful ORM framework like SQLAlchemy,
just to satisfy the most basic CRUD operations.

## Quick Start
```python
from crudlib import MySQL

my = MySQL()
my.insert_one(tb="developers", doc={"name": "Zheng"})

rows = my.query(tb="developers", condition={"age": ">=18"})

# Use SQL directly
my.execute("SELECT User FROM mysql.user;")
```

## Installation
```bash
pip install crudlib
```

## Features
* MySQL
* MariaDB

## License
This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for more details.

## Sponsors
* [JetBrains](https://www.jetbrains.com/) - Offer free Open Source license.
