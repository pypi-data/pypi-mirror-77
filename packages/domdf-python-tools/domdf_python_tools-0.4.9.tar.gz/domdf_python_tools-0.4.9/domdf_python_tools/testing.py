#!/usr/bin/env python
#
#  testing.py
"""
Handy functions for testing code.

Requires `pytest <https://docs.pytest.org/en/stable/>`_ to be installed.
"""
#
#  Copyright © 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#

# stdlib
import itertools
import random
from functools import lru_cache
from typing import List, Sequence

# 3rd party
import pytest
from _pytest.mark import MarkDecorator

# this package
from domdf_python_tools.utils import Len


def testing_boolean_values(
		extra_truthy: Sequence = (),
		extra_falsy: Sequence = (),
		) -> MarkDecorator:
	"""
	Returns a `pytest.mark.parametrize <https://docs.pytest.org/en/stable/parametrize.html>`_
	decorator that provides a list of strings, integers and booleans, and the boolean representations of them.

	The parametrized arguments are ``boolean_string`` for the input value,
	and ``expected_boolean`` for the expected output.

	:param extra_truthy: Additional values that should be considered :py:obj:`True`.
	:param extra_falsy: Additional values that should be considered :py:obj:`False`.
	"""

	truthy = [
			True,
			"True",
			"true",
			"tRUe",
			'y',
			'Y',
			"YES",
			"yes",
			"Yes",
			"yEs",
			"ON",
			"on",
			'1',
			1,
			*extra_truthy,
			]

	falsy = [
			False,
			"False",
			"false",
			"falSE",
			'n',
			'N',
			"NO",
			"no",
			"nO",
			"OFF",
			"off",
			"oFF",
			'0',
			0,
			*extra_falsy,
			]

	boolean_strings = [
			*itertools.zip_longest(truthy, [], fillvalue=True),
			*itertools.zip_longest(falsy, [], fillvalue=False),
			]

	return pytest.mark.parametrize("boolean_string, expected_boolean", boolean_strings)


whitespace = " \t\n\r"


@lru_cache(1)
def whitespace_perms_list() -> List[str]:
	chain = itertools.chain.from_iterable(itertools.permutations(whitespace, n) for n in Len(whitespace))
	return list("".join(x) for x in chain)


def whitespace_perms(ratio: float = 0.5) -> MarkDecorator:
	r"""
	Returns a `pytest.mark.parametrize <https://docs.pytest.org/en/stable/parametrize.html>`_
	decorator that provides permutations of whitespace (strictly only ``␣\n\t\r``).
	Not all permutations are returned, as there are a lot of them;
	instead a random selection of the permutations is returned.
	By default ½ of the permutations are returned, but this can be configured using the ``ratio`` argument.

	The single parametrized argument is ``char``.

	:param ratio: The ratio of the number of permutations to select to the total number of permutations.
	"""

	perms = whitespace_perms_list()
	return pytest.mark.parametrize("char", random.sample(perms, int(len(perms) * ratio)))


def count(stop: int, start: int = 0, step: int = 1) -> MarkDecorator:
	"""
	Returns a `pytest.mark.parametrize <https://docs.pytest.org/en/stable/parametrize.html>`_
	decorator that provides a list of numbers between ``start`` and ``stop`` with an interval of ``step``.

	The single parametrized argument is ``count``.

	:param stop: The stop value passed to :class:`range`.
	:param start: The start value passed to :class:`range`.
	:param step: The step passed to :class:`range`.
	"""

	return pytest.mark.parametrize("count", range(start, stop, step))
