def gen(self):
    transformations = ["change_fluent_effect_value"]
    t = self.gen_r_transform(transformations=transformations)
    while t[2].operator not in ["+", "-", "*", "/"]:
        t = self.gen_r_transform(transformations=transformations)
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
    if transform == "change_fluent_effect_value":
        return True
    return False