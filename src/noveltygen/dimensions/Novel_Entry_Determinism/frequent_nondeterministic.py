def gen(self):
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
    if transform == "remove_effect":
        return True
    return False