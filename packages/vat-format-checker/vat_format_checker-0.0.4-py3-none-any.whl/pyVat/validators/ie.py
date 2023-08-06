# Copyright 2018 Agile Geeks

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software
# and associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute,
# sublicense, and/or sell copies of the Software, and to permit persons to whom the Software
# is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial
# portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT
# LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
# OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from __future__ import (
    unicode_literals,
    print_function,
    division
)
import re
from .generic import GenericValidator


class Validator(GenericValidator):
    """
    For rules see /docs/VIES-VAT Validation Routines-v15.0.doc
    """

    check_char_mapping = {
        0: 'W',
        1: 'A',
        2: 'B',
        3: 'C',
        4: 'D',
        5: 'E',
        6: 'F',
        7: 'G',
        8: 'H',
        9: 'I',
        10: 'J',
        11: 'K',
        12: 'L',
        13: 'M',
        14: 'N',
        15: 'O',
        16: 'P',
        17: 'Q',
        18: 'R',
        19: 'S',
        20: 'T',
        21: 'U',
        22: 'V'
    }

    def __init__(self):
        self.regexp = re.compile(r'^((\d{7}[a-z])|(\d[a-z\+\*]\d{5}[a-z]))$', re.IGNORECASE)

    def validate(self, vat_number):
        if super(Validator, self).validate(vat_number) is False:
            return False

        vat_number = str(vat_number)
        checksum = vat_number[7]

        #check for old style - second char sould be a letter
        try:
            int(vat_number[1])
        except:
            old_style = True
        else:
            old_style = False

        if old_style:
            n = '0' + vat_number[2:7] + vat_number[0]
            r = self.sum_weights(list(range(8,1,-1)), n) % 23
        else:
            r = r = self.sum_weights(list(range(8,1,-1)), vat_number) % 23

        return checksum == Validator.check_char_mapping[r]
