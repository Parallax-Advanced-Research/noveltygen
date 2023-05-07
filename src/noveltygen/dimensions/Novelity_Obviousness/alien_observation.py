def gen(self):
    transformations = ["add_fluent", "add_predicate"] #new fluent instead
    effects = set()
    for op in self.domain.operators+self.domain.events:
        for eff in op.effects[0]:
            eff = eff[1]
            if hasattr(eff, "operator"):  # Expression
                effects.add(eff.left_child.name)
            else:  # Literal
                effects.add(eff.predicate.name)
    t = self.gen_r_transform(transformations=transformations, spec_avoid=list(effects))
    return t


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
    print("WE CANT DETERMINE THIS")
    return False