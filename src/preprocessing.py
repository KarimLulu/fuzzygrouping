import string
from collections import Mapping

class Cleaner(object):

    def __init__(self, intab="", outtab="", table=None,
                 lowercase=False, strip_chars=string.whitespace):
        self.intab = intab
        self.outtab = outtab
        self.lowercase = lowercase
        self.strip_chars = strip_chars
        self.table = table

    @property
    def translate(self):
        return any([self.intab, self.outtab, self.table])

    @property
    def table(self):
        return self._table

    @table.setter
    def table(self, value):
        if len(self.intab) != len(self.outtab):
            raise ValueError("Intab and outtab should be of equal length, got {0} and {1} instead".format(len(self.intab), len(self.outtab)))
        else:
            self._table = str.maketrans(self.intab, self.outtab)
        if value == 'punctuation':
            self._table.update(str.maketrans(string.punctuation, ' '*len(string.punctuation)))
        elif isinstance(value, Mapping):
            self._table.update(value)

    def make_text(self, text):
        if not isinstance(text, (str, bytes)):
            text = str(text)
        return text

    def __call__(self, text):
        text = self.make_text(text)
        if self.lowercase:
            text = text.lower()
        if self.translate:
            text = text.translate(self.table)
        if self.strip_chars:
            text = text.strip(self.strip_chars)
        return text

if __name__=='__main__':
    text = "\t\r\n Hello World! #;.., \r\n "
    cleaner = Cleaner(table='punctuation', intab='l', outtab='q', lowercase=True)
    assert cleaner(text)=='heqqo worqd'
