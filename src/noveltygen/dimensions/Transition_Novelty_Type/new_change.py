def gen(self):
    transformations = ["add_effect"]
    return self.gen_r_transform(transformations=transformations)


def validate(self):
    for transform, args in list(zip(self.rt.transforms, self.rt.args)):
        retval = eval_transformation(self, transform, args)
        if retval:
            return True
    return False


def eval_transformation(self, transform, args):
    if transform == 'add_effect':
        return True
    return False
