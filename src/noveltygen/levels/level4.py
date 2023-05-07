import random
import time

def gen(self):
    """
    4 – Relations: Can be spatial, temporal, or other. Can include the SAIL-ON agent and other entities.

    A transformation sequence exhibits relation novelty if a static fluent
    (one not present in any effects or process changes) is created or added to conditions or preconditions.
    The fluent must be relevant, and must involve 2 or more entities (i.e., Agent or Object subtypes).
    """
    transformations = ["add_precondition"]
    precond = set()
    for op in self.domain.operators + self.domain.events:
        for eff in op.effects[0]:
            eff = eff[1]
            if hasattr(eff, "operator"):  # Expression
                precond.add(eff.left_child.name)
            else:  # Literal
                precond.add(eff.predicate.name)
    for pred in [x.name for x in self.domain.fluents if len(x.args) == 0]:
        precond.add(pred)
    for pred in [x.name for x in self.domain.predicates if len(x.args) < 2]:
        precond.add(pred)
    return self.gen_r_transform(transformations=transformations, spec_avoid=list(precond))


def validate(self):
    print('h')
    for transform, args in list(zip(self.rt.transforms, self.rt.args)):
        b = eval_transformation(self, transform, args)
        print('b', b)
        if b:
            print('a')
            return True
    return False


def eval_transformation(self, transform, args):
    if transform == 'add_precondition' and args[1].class_name == 'fluents':
        fluent = args[1]
        if len(fluent.args) == 0:
            return False
        found = False
        for action_event in self.domain.operators+self.domain.events:
            for effect in action_event.effects[0]:
                effect = effect[1]
                if not hasattr(effect, "left_child"):
                    continue
                effect = effect.left_child
                if effect.name == fluent.name:
                    found = True
                    break
            if found:
                break
        if not found:
            print("SUCCESS")
            print(transform, args)
            time.sleep(3)
            return True
        else:
            print("FAIL")
            return False
    elif transform == 'add_fluent':
        print("SUCCESS, but not as much?")
        return False #TODO: make true, for now not interested
    else:
        print("FAIL")
        return False
