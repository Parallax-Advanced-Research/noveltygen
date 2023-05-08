from noveltygen.novelty_generator import NoveltyGenerator as NG
from noveltygen.TTransformations import ScenarioGenerator
from noveltygen.TTransformations import ObjectGenerator
from noveltygen.TTransformations import RelationGenerator
from tsal.translator.predicate import Predicate
from tsal.translator.expression import Expression
from tsal.translator.fluent import Fluent

blocks_world_ng = NG("domain.tsal", "problem.tsal")
print("-----------------------------------------------------")
# define the object generators
block_objects_gen = ObjectGenerator(3, "block", "b")
player_objects_gen = ObjectGenerator(1, "player", "p")

# get the blocks objects
single_object_args = [[b] for b in block_objects_gen.draw()]

# set up relation generator for ontable
ontable_pred = [pred for pred in blocks_world_ng.domain.predicates if pred.name == "ontable"][0]
ontable_relation_gen = RelationGenerator(ontable_pred, single_object_args)

# set up relation generator for clear
clear_pred = [pred for pred in blocks_world_ng.domain.predicates if pred.name == "clear"][0]
clear_relation_gen = RelationGenerator(clear_pred, single_object_args)

# set up relation generator for (= (self) p1)
self_fluent = [fluent for fluent in blocks_world_ng.domain.fluents if fluent.name == "self"][0]
equal_pred = Predicate("=")
# since only one player can be self, choose the first one (only matters when there's multiple players)
first_player = player_objects_gen.draw()[0]
player_relation_gen = RelationGenerator(equal_pred, [[self_fluent, first_player]])

# set up relation generator for (handempty)
handempty_pred = [pred for pred in blocks_world_ng.domain.predicates if pred.name == "handempty"][0]

# NOTE: to specify no args as a possible arg_set, use an empty list [], hence the nested empty list [[]], which means
# there is one arg_set here and it's an empty arg_set. This is not the same as saying there are no arg_sets.
handempty_relation_gen = RelationGenerator(handempty_pred, [[]], "self")

# generate a goal
# TODO - make goal a proper object in tsal
self_expression = Expression(operator="=", left_child=Fluent(name="self"), right_child=Expression(value=first_player))
on_pred = [pred for pred in blocks_world_ng.domain.predicates if pred.name == "on"][0]

double_object_args = [[b1, b2] for b1 in block_objects_gen.draw() for b2 in block_objects_gen.draw() if b1 != b2]

on_relation = RelationGenerator(on_pred, double_object_args).draw()[0]
goal = [[self_expression, on_relation]]

bsg = ScenarioGenerator(object_generators=[block_objects_gen, player_objects_gen], relation_generators=[ontable_relation_gen, clear_relation_gen, player_relation_gen, handempty_relation_gen], domain=blocks_world_ng.domain, goal=goal)

print(bsg.draw())
