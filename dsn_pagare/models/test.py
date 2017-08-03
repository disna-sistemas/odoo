#!/usr/bin/env python
# -*- coding: utf-8 -*-

import openerp
#from openerp import models, fields, api
import number_to_letter

class TestToWord(unittest.TestCase):

    _inherit = "payment.order"

    def test_total(self):
        print self.total

TestToWord

#    def test_to_word(self):
#        print number_to_letter.to_word(1420.36, 'EUR')