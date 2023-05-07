def gen(self):
    """
    8 – Events:  A state change or series of state changes that are not the result of volitional
    action by an external agent or the point-of-view agent. Clarifications: Events include state
    changes with specific preconditions.

    An event novelty is a transformation sequence that affects T-SAL events that have both environmental and
    non-environmental triggers. At least one trigger of a modified event must be based on an environment function
    and at least one must be directly affected by an action. Event novelty sequences include those that modify the
    distribution of an environmental function that triggers such an event.
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