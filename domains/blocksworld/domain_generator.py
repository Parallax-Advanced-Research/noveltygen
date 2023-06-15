from noveltygen.novelty_generator import NoveltyGenerator as NG
from noveltygen.RTransformations import RTransformations
from noveltygen.RTransformation import RTransformation
from noveltygen.levels.novelty_level import NoveltyLevel

"""
Example showing how to generate blocksworld domains using RTransformations.

Run this from within 'domains/blocksworld'
"""


blocks_world_ng = NG("domain.tsal", "problem.tsal")

print("Original domain:")
print(blocks_world_ng.domain)
print("-----------------------------------------------------")

# for level_i in NoveltyLevel.__members__.values():
#     transform = blocks_world_ng.gen_by_level[level_i]()
#     r_transformation_used = transform[0]
#     new_tsal_construct = transform[1]
#     change_only = transform[2]
#     print("Generated domain #{}:".format(level_i))
#     print("\tR-transformation used: {}".format(r_transformation_used))
#     print("\tTSAL construct: {}...".format(str(new_tsal_construct).replace('\n', ' ')[:50]))
#     print("\tChanged: {}".format(change_only))
#     print("Domain is : {}".format(blocks_world_ng.domain))
#     print("-----------------------------------------------------")

#rtr = RTransformations(blocks_world_ng.domain)

# print("All possible R Transformations:")
# for t in rtr.get_all_transformation_kinds():
#     print("\t{}".format(t))

rtr_choices = [RTransformation.ADD_EFFECT,
               RTransformation.ADD_PRECONDITION,
               RTransformation.REMOVE_EFFECT,
               RTransformation.REMOVE_PRECONDITION,
               RTransformation.ACTION_TO_EVENT,
               RTransformation.EVENT_TO_ACTION,
               RTransformation.ADD_EVENT,
               RTransformation.REMOVE_EVENT,
               RTransformation.ADD_ACTION,
               RTransformation.REMOVE_ACTION,
               RTransformation.ADD_PREDICATE,
               RTransformation.REMOVE_PREDICATE,
               RTransformation.ADD_FLUENT,
               RTransformation.REMOVE_FLUENT,
               # TODO: add these
               #RTransformation.ADD_CONSTANT,
               #RTransformation.REMOVE_CONSTANT,
               #RTransformation.ADD_DERIVED_PREDICATE,
               #RTransformation.REMOVE_DERIVED_PREDICATE,
               RTransformation.ADD_TYPE,
               RTransformation.REMOVE_TYPE,
                RTransformation.ADD_TYPE_PARENT,
                RTransformation.REMOVE_TYPE_PARENT,
                RTransformation.CHANGE_EFFECT_PROBABILITY,
                RTransformation.CHANGE_EVENT_FREQUENCY,
                RTransformation.CHANGE_EVENT_PROBABILITY,
                RTransformation.CHANGE_FLUENT_EFFECT_VALUE
               ]

num_domains_to_generate = 20
for rtr in rtr_choices:
    transform = blocks_world_ng.gen_r_transform(transformations=[rtr])
    r_transformation_used = transform[0]
    new_tsal_construct = transform[1]
    change_only = transform[2]
    if r_transformation_used is None and new_tsal_construct is None and change_only is None:
        print("No valid transformation found for {}".format(rtr))
        print("-----------------------------------------------------")
        continue
    print("\tR-transformation used: {}".format(r_transformation_used))
    print("\tTSAL construct: {}...".format(str(new_tsal_construct).replace('\n',' ')[:50]))
    print("\tChanged: {}".format(change_only))
    print("Domain is : {}".format(blocks_world_ng.novelties['RTransformations'][-1][1]))
    print("-----------------------------------------------------")

