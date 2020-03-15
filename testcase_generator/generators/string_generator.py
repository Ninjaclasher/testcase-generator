import string

from testcase_generator.generators.custom_generator import CustomGenerator


class StringGenerator(CustomGenerator):
    def __init__(self, N, *args, **kwargs):
        """
        N: a BoundedConstraint object or an integer for the string length
        kwargs:
            type: type of string to generate
                    standard: default string
                    palindrome: palindromic string
                    space_separated: space separated "words"
                    repeating: string consisting of a substring that is repeated more than 1 time
            charset: available characters to use, the default is all lowercase letters
        """
        self.type = kwargs.pop('type', 'standard')
        self.charset = kwargs.pop('charset', string.ascii_lowercase)
        super().__init__(N, *args, **kwargs)

    def _validate(self):
        if self.type not in ('standard', 'palindrome', 'space_separated', 'repeating'):
            raise ValueError('Unknown string type {}.'.format(self.type))

    def next(self):
        return ''.join(getattr(self, self.type)(self.N))

    @property
    def _char(self):
        return self.random.choice(self.charset)

    def standard(self, length):
        return [self._char for i in range(length)]

    def palindrome(self, length):
        chars = self.standard(length // 2)
        mid = [self._char] if length % 2 == 1 else []
        return chars + mid + chars[::-1]

    def space_separated(self, length):
        num_spaces = self.random.randint(0, (length - 1) // 2)
        chars = [[self._char] for i in range(num_spaces + 1)]
        remaining_length = length - num_spaces - (num_spaces + 1)
        for i in range(remaining_length):
            chars[self.random.randint(0, num_spaces)].append(self._char)
        return ' '.join(''.join(x) for x in chars)

    def repeating(self, length):
        if length == 1:
            return [self._char]
        factors = set()
        for i in range(1, int(length**0.5) + 1):
            if length % i == 0:
                factors.add(i)
                factors.add(length // i)
        factors.remove(length)
        repeated_length = self.random.choice(list(factors))
        return self.standard(repeated_length) * (length // repeated_length)
