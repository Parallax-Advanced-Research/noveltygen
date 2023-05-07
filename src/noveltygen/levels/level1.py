def gen(self):
    """
    1 – Objects: Objects may experience state changes as a result of actions by the i) SAIL-ON agent, ii) an external
     agent, or iii) an event.

    To introduce object novelty, a transformation sequence must at least either add a new type that inherits from Object
    or add a new fluent that relates an object type to something else. To ensure relevance, that new type or fluent
    must affect the preconditions or effects of some action, or the conditions or changes of some process.
    """
    transformations = ["add_type"]
    return self.gen_r_transform(transformations=transformations)



def validate(self, rtransformation):
    return False
