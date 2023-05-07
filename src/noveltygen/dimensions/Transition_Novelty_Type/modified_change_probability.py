def gen(self):
    transformations = ["change_effect_probability"]
    return self.gen_r_transform(transformations=transformations)
    pass


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
    if transform == "change_effect_probability":
        return True
    return False