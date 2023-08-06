# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytest_assert_utils', 'pytest_assert_utils.util', 'tests']

package_data = \
{'': ['*']}

modules = \
['pytest', 'LICENSE', 'CHANGELOG', 'README']
entry_points = \
{'pytest11': ['assert_utils = pytest_assert_utils']}

setup_kwargs = {
    'name': 'pytest-assert-utils',
    'version': '0.2.1',
    'description': 'Useful assertion utilities for use with pytest',
    'long_description': "# pytest-assert-utils\n\nHandy assertion utilities for use with pytest\n\n\n# Installation\n\n```bash\npip install pytest-assert-utils\n```\n\n\n# Usage\n\n## assert_dict_is_subset\n```python\ndef assert_dict_is_subset(subset, superset, recursive=True)\n```\n\nAssert `subset` is a non-strict subset of `superset`\n\nIf this assertion fails, a pretty diff will be printed by pytest.\n\n```python\n>>> from pytest_assert_utils import assert_dict_is_subset\n\n>>> expected = {'a': 12}\n>>> actual = {'b': 20, 'a': 12}\n>>> assert_dict_is_subset(expected, actual)\n\n>>> expected = {'a': 12}\n>>> actual = {'b': 50000}\n>>> assert_dict_is_subset(expected, actual)\nTraceback (most recent call last):\n ...\nAssertionError\n```\n\n## assert_model_attrs\n```python\ndef assert_model_attrs(instance, _d=UNSET, **attrs)\n```\n\nAssert a model instance has the specified attr values\n\nMay be passed a dict of attrs, or kwargs as attrs\n\n```python\n>>> from pytest_assert_utils import assert_model_attrs\n\n>>> from collections import namedtuple\n>>> Model = namedtuple('Model', 'id,key,other_key,parent', defaults=(None,)*4)\n\n>>> assert_model_attrs(Model(), {})\n\n>>> assert_model_attrs(Model(key='value'), {'key': 'value'})\n>>> assert_model_attrs(Model(key='value'), key='value')\n>>> assert_model_attrs(Model(key='value'), key='not the value')\nTraceback (most recent call last):\n ...\nAssertionError\n\n>>> assert_model_attrs(Model(key='value', other_key='other_value'), key='value')\n```\n\n## Any\nMeta-value which compares True to any object (of the specified type(s))\n\n```python\n>>> from pytest_assert_utils import util\n\n>>> util.Any() == 'stuff'\nTrue\n>>> util.Any() == 1\nTrue\n>>> util.Any() == None\nTrue\n>>> util.Any() == object()\nTrue\n\n>>> util.Any(int) == 1\nTrue\n>>> util.Any(int) == '1'\nFalse\n```\n\n## Optional\nMeta-value which compares True to None or the optionally specified value\n\n```python\n>>> from pytest_assert_utils import util\n\n>>> util.Optional() == None\nTrue\n>>> util.Optional() is None  # this will not work!\nFalse\n>>> util.Optional(24) == 24\nTrue\n>>> util.Optional(24) == None\nTrue\n\n>>> util.Optional(Any(int)) == 1\nTrue\n>>> util.Optional(Any(int)) == None\nTrue\n>>> util.Optional(Any(int)) == '1'\nFalse\n```\n\n## Collection\nSpecial class enabling equality comparisons to check items in any collection (list, set, tuple, etc)\n\n```python\n>>> from pytest_assert_utils import util\n\n>>> util.Collection.containing(1) == [1, 2, 3]\nTrue\n>>> util.Collection.containing(1) == {1, 2, 3}\nTrue\n>>> util.Collection.containing(1) == (1, 2, 3)\nTrue\n\n>>> util.Collection.containing(1) == [4, 5, 6]\nFalse\n>>> util.Collection.containing(1) == {4, 5, 6}\nFalse\n>>> util.Collection.containing(1) == (4, 5, 6)\nFalse\n```\n\n## List\nSpecial class enabling equality comparisons to check items in a list\n\n```python\n>>> from pytest_assert_utils import util\n\n>>> util.List.containing(1) == [1, 2, 3]\nTrue\n>>> util.List.containing(1) == [4, 5, 6]\nFalse\n\n>>> util.List.not_containing(1) == [1, 2, 3]\nFalse\n>>> util.List.not_containing(1) == [4, 5, 6]\nTrue\n\n>>> util.List.empty() == [1, 2, 3]\nFalse\n>>> util.List.empty() == []\nTrue\n\n>>> util.List.not_empty() == [1, 2, 3]\nTrue\n>>> util.List.not_empty() == []\nFalse\n```\n\n## Set\nSpecial class enabling equality comparisons to check items in a set\n\n```python\n>>> from pytest_assert_utils import util\n\n>>> util.Set.containing(1) == {1, 2, 3}\nTrue\n>>> util.Set.containing(1) == {4, 5, 6}\nFalse\n\n>>> util.Set.not_containing(1) == {1, 2, 3}\nFalse\n>>> util.Set.not_containing(1) == {4, 5, 6}\nTrue\n\n>>> util.Set.empty() == {1, 2, 3}\nFalse\n>>> util.Set.empty() == set()\nTrue\n\n>>> util.Set.not_empty() == {1, 2, 3}\nTrue\n>>> util.Set.not_empty() == set()\nFalse\n```\n\n## Dict\nSpecial class enabling equality comparisons to check items in a dict\n\n```python\n>>> from pytest_assert_utils import util\n\n>>> util.Dict.containing('a') == {'a': 1, 'b': 2}\nTrue\n>>> util.Dict.containing(a=1) == {'a': 1, 'b': 2}\nTrue\n>>> util.Dict.containing({'a': 1}) == {'a': 1, 'b': 2}\nTrue\n>>> util.Dict.containing('a') == {'b': 2}\nFalse\n>>> util.Dict.containing(a=1) == {'b': 2}\nFalse\n>>> util.Dict.containing({'a': 1}) == {'b': 2}\nFalse\n\n>>> util.Dict.not_containing('a') == {'a': 1, 'b': 2}\nFalse\n>>> util.Dict.not_containing(a=1) == {'a': 1, 'b': 2}\nFalse\n>>> util.Dict.not_containing({'a': 1}) == {'a': 1, 'b': 2}\nFalse\n>>> util.Dict.not_containing('a') == {'b': 2}\nTrue\n>>> util.Dict.not_containing(a=1) == {'b': 2}\nTrue\n>>> util.Dict.not_containing({'a': 1}) == {'b': 2}\nTrue\n\n>>> util.Dict.empty() == {'a': 1, 'b': 2, 'c': 3}\nFalse\n>>> util.Dict.empty() == {}\nTrue\n\n>>> util.Dict.not_empty() == {'a': 1, 'b': 2, 'c': 3}\nTrue\n>>> util.Dict.not_empty() == {}\nFalse\n```\n\n## Str\nSpecial class enabling equality comparisons to check items in a string\n\n```python\n>>> from pytest_assert_utils import util\n\n>>> util.Str.containing('app') == 'apple'\nTrue\n>>> util.Str.containing('app') == 'happy'\nTrue\n>>> util.Str.containing('app') == 'banana'\nFalse\n\n>>> util.Str.not_containing('app') == 'apple'\nFalse\n>>> util.Str.not_containing('app') == 'happy'\nFalse\n>>> util.Str.not_containing('app') == 'banana'\nTrue\n\n>>> util.Str.empty() == 'hamster'\nFalse\n>>> util.Str.empty() == ''\nTrue\n\n>>> util.Str.not_empty() == 'hamster'\nTrue\n>>> util.Str.not_empty() == ''\nFalse\n```\n",
    'author': 'Zach "theY4Kman" Kanzler',
    'author_email': 'they4kman@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/theY4Kman/pytest-assert-utils',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
