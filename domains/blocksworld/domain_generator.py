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
               RTransformation.REMOVE_ACTION]

num_domains_to_generate = 20
for rtr in rtr_choices:
    transform = blocks_world_ng.gen_r_transform(transformations=[rtr])
    r_transformation_used = transform[0]
    new_tsal_construct = transform[1]
    change_only = transform[2]
    #print("Generated domain #{}:".format(i))
    print("\tR-transformation used: {}".format(r_transformation_used))
    print("\tTSAL construct: {}...".format(str(new_tsal_construct).replace('\n',' ')[:50]))
    print("\tChanged: {}".format(change_only))
    print("Domain is : {}".format(blocks_world_ng.novelties['RTransformations'][-1][1]))
    print("-----------------------------------------------------")

