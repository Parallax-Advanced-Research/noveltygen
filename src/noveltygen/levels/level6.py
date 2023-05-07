def gen(self):
    """
    6 – Environment: A change in an element of an open-world space that may impact the entire task space and is independent of a specific entity.

     An environment novelty is a transformation sequence in which environmental functions, processes, or events are modified.
     Environmental functions are those functions outside of agent control, meaning they are not affected by functions.
     Environmental processes and events are those that are conditioned on or triggered by only environmental
    functions and position-valued functions.
    """
    transformations = ["add_precondition", "add_effect"]
    return self.gen_r_transform(transformations=transformations, spec_avoid=["operators"])

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