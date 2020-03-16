from testcase_generator.generators.custom_generator import CustomGenerator


class CollectionGenerator(CustomGenerator):
    types = ()
    default_type = None

    def __init__(self, N, *args, **kwargs):
        self.type = kwargs.pop('type', self.default_type)
        self.generator_kwargs = kwargs.pop('generator_kwargs', {})
        super().__init__(N, *args, **kwargs)

    def _validate(self):
        super()._validate()
        if self.type not in self.types:
            raise ValueError('Unknown type {}. Choices: {}'.format(self.type, ', '.join(map(str, self.types))))

    def next(self):
        return getattr(self, self.type)(self.N, **self.generator_kwargs)
