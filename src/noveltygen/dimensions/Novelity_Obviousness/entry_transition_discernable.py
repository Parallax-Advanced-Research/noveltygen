def gen(self):
    transformations = ["remove_effect", "add_effect"] #add effect
    return self.gen_r_transform(transformations=transformations)


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