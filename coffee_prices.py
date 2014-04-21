# -*- coding: utf-8 -*-
# coffee_prices.py
# Copyright (C) 2014 Kali Kaneko
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
Scraper for getting coffee prices in different international markets.
"""
from collections import namedtuple
from functools import partial

from lxml import html
import requests

TARGET = "http://www.infoaserca.gob.mx/fisicos/cfe_pci.asp"
COUNTRY = u"México"


PriceData = namedtuple('PriceData', ["product_type", "place", "last_price",
                                     "prev_price", "current_day", "prev_day"])

# The page has a single table, that on 2014-04-20 has the
# following structure:
# Product type | Place | Last price | Net change | Previous prize | current day
# | prev day
# We will skip delta column (1-index 4) because it's in a span and we can
# just substract it.

readcol = lambda tree, index: tree.xpath(
    '//table/tr[*]/td[%s]/text()' % index)


def parsetable():
    """
    Parse coffee prices table.

    :return: a generator, that yields a tuple of row values
    :rtype: generator of PriceData
    """
    page = requests.get(TARGET)
    tree = html.fromstring(page.text)
    rc = partial(readcol, tree)

    for row in zip(rc(1), rc(2), rc(3), rc(5), rc(6), rc(7)):
        yield PriceData(*row)

if __name__ == "__main__":
    print
    print "COFFE DAILY PRICES (MXN)"
    fmt = "%12s"
    for row in parsetable():
        if COUNTRY in row.product_type:
            print
            print "---------------------------------"
            print row.product_type, "(%s)" % row.place
            print
            print '\t'.join((fmt % row.current_day, fmt % row.prev_day))
            print '\t'.join((fmt % row.last_price, fmt % row.prev_price))
