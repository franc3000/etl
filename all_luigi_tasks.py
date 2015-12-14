#!/usr/bin/env python2.7

import luigi
from buyer_count import BuyerCount
from deed_append import DeedAppend


class AllLuigiTasks(luigi.WrapperTask):
    """Dummy task that triggers all dependency chains"""

    def requires(self):
        yield DeedAppend()
        yield BuyerCount()
