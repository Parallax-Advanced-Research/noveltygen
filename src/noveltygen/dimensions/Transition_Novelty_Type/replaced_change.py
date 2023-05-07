def gen(self):
    transformations = ["change_fluent_effect_value"]
    return self.gen_r_transform(transformations=transformations)


def validate(self):
    for transform, args in list(zip(self.rt.transforms, self.rt.args)):
        b = eval_transformation(self, transform, args)
        if b:
            return True
    return False


def eval_transformation(self, transform, args):
    if transform == "change_fluent_effect_value":
        return True
    return False