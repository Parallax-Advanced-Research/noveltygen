def gen(self):
    """
    5 – Interactions: Can be spatial, temporal, or other. Can include the SAIL-ON agent and other entities.

    A transformation sequence exhibits interaction novelty if a fluent is added to preconditions, effects,
    process conditions, or process changes, and that fluent is dynamic
    (present in one or more effects or process changes). The fluent must be relevant, and must involve 2 or more
    entities (i.e., Agent or Object subtypes).
    """
    transformations = ["add_precondition"]
    keep = set()
    precond = set()
    for op in self.domain.operators + self.domain.events:
        for eff in op.effects[0]:
            eff = eff[1]
            if hasattr(eff, "operator"):  # Expression
                keep.add(eff.left_child.name)
            else:  # Literal
                keep.add(eff.predicate.name)
    for pred in [x.name for x in self.domain.fluents if len(x.args) == 0 or x.name not in keep]:
        precond.add(pred)
    for pred in self.domain.predicates:
        precond.add(pred.name)
    return self.gen_r_transform(transformations=transformations, spec_avoid=list(precond))

def validate(self, rtransformation):
    return False


def eval_transformation(transform, args):
    print(transform, args)
    print(args)
    if (transform == 'add_precondition' or transform == 'add_effect') and args[1].class_name == 'fluents':
        for arg in args:
            print(arg)
        print("SUCCESS")
    else:
        print("FAIL")
    print("hafsf")
    return False