from testcase_generator.generators.custom_generator import CustomGenerator
from testcase_generator.models import ChoiceConstraint


class CollectionGenerator(CustomGenerator):
    types = ()
    default_type = None
    default_value_generator = None

    def __init__(self, N, *args, **kwargs):
        self.type = kwargs.pop('type', self.default_type)
        self.V = kwargs.pop('V', self.default_value_generator)
        super().__init__(N, *args, **kwargs)

    def _validate(self):
        super()._validate()
        if self.type not in self.types:
            raise ValueError('Unknown type {}. Choices: {}'.format(self.type, ', '.join(map(str, self.types))))
        if not isinstance(self.V, ChoiceConstraint):
            raise ValueError('V must be a ChoiceConstraint, not {}'.format(type(self.V).__name__))

    def next(self):
        return getattr(self, self.type)(self.N, **self.kwargs)
