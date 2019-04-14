import yaml

from .models import Case, Batch


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

            constraint = str(constraint).split('~')
            if len(constraint) == 1:
                constraint = constraint[0]
                if constraint == 'MAX':
                    constraints_dict[var].MIN = constraints_dict[var].MAX
                elif constraint == 'MIN':
                    constraints_dict[var].MAX = constraints_dict[var].MIN
                else:
                    new_value = eval(constraint)
                    if not (constraints_dict[var].MIN <= new_value <= constraints_dict[var].MAX):
                        raise ValueError('{} for constraint {} is not in the '
                                         'global or batch constraints'.format(new_value, var))
                    constraints_dict[var].MIN = new_value
                    constraints_dict[var].MAX = new_value
            elif len(constraint) == 2:
                lower, upper = constraint
                if lower.strip():
                    constraints_dict[var].MIN = max(constraints_dict[var].MIN, eval(lower))
                if upper.strip():
                    constraints_dict[var].MAX = min(constraints_dict[var].MAX, eval(upper))
                if constraints_dict[var].MIN > constraints_dict[var].MAX:
                    raise ValueError('Lowerbound is larger than upperbound for constraint {}'.format(var))
            else:
                raise ValueError

        return constraints_dict

    def parse(self):
        for batch in self.data:
            batch_constraints = self.parse_case(batch.get('constraints', {}))

            self.batches.append(
                Batch(
                    num=batch['batch'],
                    cases=[Case(self.parse_case(case, batch_constraints)) for case in batch['cases']],
                )
            )
