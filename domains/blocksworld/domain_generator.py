from noveltygen.novelty_generator import NoveltyGenerator as NG
from noveltygen.RTransformations import RTransformations

"""
Example showing how to generate blocksworld domains using RTransformations.

Run this from within 'domains/blocksworld'
"""

blocks_world_ng = NG("domain.tsal", "problem.tsal")
rtr = RTransformations(blocks_world_ng.domain)

print("All possible R Transformations:")
for t in rtr.get_all_transformation_kinds():
    print("\t{}".format(t))

rtr_choices = ['add_effect', 'add_precondition', 'remove_effect',]# 'remove_precondition']

num_domains_to_generate = 10
for i in range(num_domains_to_generate):
    transform = blocks_world_ng.gen_r_transform(transformations=rtr_choices)
    r_transformation_used = transform[0]
    new_tsal_construct = transform[1]
    change_only = transform[2]
    print("Generated domain #{}:".format(i))
    print("\tR-transformation used: {}".format(r_transformation_used))
    print("\tTSAL construct: {}...".format(str(new_tsal_construct).replace('\n',' ')[:50]))
    print("\tChanged: {}".format(change_only))
