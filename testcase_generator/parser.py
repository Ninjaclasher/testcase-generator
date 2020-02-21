import yaml

from .models import Batch, BoundedConstraint, Case


class ConstraintParser:
    def __init__(self, data):
        self.batches = []
        self.data = yaml.safe_load(data)

    def parse_case(self, constraints, batch_constraints={}):
        constraints_dict = {}
        for var, constraint in batch_constraints.items():
            constraints_dict[var] = constraint.copy()

        for var, constraint in constraints.items():
            if var not in constraints_dict.keys():
                constraints_dict[var] = Case().get(var).copy()

            if not isinstance(constraints_dict[var], BoundedConstraint):
                raise ValueError('The parser does not support modifiying constraint {} as '
                                 'it is not a BoundedConstraint'.format(var))

            _min, _max = constraints_dict[var].args

            constraint = str(constraint).split('~')
            if len(constraint) == 1:
                constraint = constraint[0]
                if constraint == 'MAX':
                    _min = _max
                elif constraint == 'MIN':
                    _max = _min
                else:
                    new_value = eval(constraint)
                    if not (_min <= new_value <= _max):
                        raise ValueError('{} for constraint {} is not in the '
                                         'global or batch constraints'.format(new_value, var))
                    _min = new_value
                    _max = new_value
            elif len(constraint) == 2:
                lower, upper = constraint
                if lower.strip():
                    lower = eval(lower.strip())
                    if lower < _min:
                        raise ValueError('{} for constraint {} is not in the '
                                         'global or batch constraints'.format(lower, var))
                    _min = lower
                if upper.strip():
                    upper = eval(upper.strip())
                    if upper > _max:
                        raise ValueError('{} for constraint {} is not in the '
                                         'global or batch constraints'.format(upper, var))
                    _max = upper
                if _max < _min:
                    raise ValueError('Lowerbound is larger than upperbound for constraint {}'.format(var))
            else:
                raise ValueError('Too many arguments')

            constraints_dict[var].set_args(_min, _max)

        return constraints_dict

    def parse(self):
        for batch in self.data:
            batch_constraints = self.parse_case(batch.get('constraints', {}))
            cases = []
            for case in batch['cases']:
                constraints = self.parse_case(case.get('constraints', {}), batch_constraints)
                for i in range(case.get('repeat', 1)):
                    cases.append(Case(constraints))

            self.batches.append(
                Batch(
                    num=batch['batch'],
                    cases=cases,
                    start=batch.get('start', 0),
                )
            )
