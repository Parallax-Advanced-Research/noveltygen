def gen(self):
    """
    3 – Actions: Non-goal-oriented movements of non-volitional objects are not considered actions.

    In order for a transformation sequence to exhibit action novelty, an action effect must be changed; changes to action
    preconditions are instead termed “rule” novelty.
    """
    transformations = ["add_effect", "remove_effect", "change_fluent_effect_value", "change_effect_probability"]
    return self.gen_r_transform(transformations=transformations)


def validate(self, rtransformation):
    return False