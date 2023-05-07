def gen(self):
    """
    7 – Goals:  The purpose of a behavior by an agent in the environment.

    Goal novelties are those that include a T-Transformation changing how the performance function of a
    scenario generator is calculated.
    """

    return self.tt.change_goal()

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