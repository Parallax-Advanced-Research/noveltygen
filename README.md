# Novelty Generator

Novelty Generation using the Tsal Language. Allows the user to generate novel domain and problem
files given a base domain and problem. 

***

## About

This is the implementation of the novelty generator from the following publications. Please cite the most recent publication if you use this code in your work:
* Dannenhauer, D., Reifsnyder, N., Regester, AJ., Molineaux, M. "Transforming Environments to Evaluate Agent Adaptation." Advances in Cognitive Systems (ACS). George Mason University, Arlington, VA. 2022.

Related work:

* Molineaux, M., Dannenhauer, D. "An Environment Transformation-based Framework for Comparison of Open-World Learning Agents." Designing Artificial Intelligence for Open Worlds. AAAI Spring Symposium Series 2022. Stanford University, CA. 2022. 

## Installation
This package depends on [tsal](https://github.com/Parallax-Advanced-Research/tsal) library for reading, modifying, and saving tsal files. Eventually we will have these on pypi, until then please clone that project first, before following the steps below.
```commandline
# get the tsal repo, we'll come back to this soon
git clone https://github.com/Parallax-Advanced-Research/tsal.git

# clone this repo
git clone https://github.com/Parallax-Advanced-Research/noveltygen.git

# create a virtualenv
cd noveltygen
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# and now make sure to install tsal
cd ../tsal/
pip install .  # use the -e flag if you end up modifying tsal code
```

If you plan to modify the novelty generator code, install via:

```commandline
pip install -e .
```

## Usage

These examples can be found in examples/example.py. These examples build on each other.

### Creating a novelty generator
```python
from noveltygen.novelty_generator import NoveltyGenerator as NG
ng = NG(domain_file='domains/blocksworld/domain.tsal', problem_file='domains/blocksworld/problem.tsal')
```

### Generating a novelty at any novelty level

Novelty levels refer to a categorization of different kinds of novelty from Kildebeck et al. 2022 - "2022 Novelty Hierarchy." *Unpublished manuscript.*

```python
from noveltygen.levels.novelty_level import NoveltyLevel
transform = ng.gen_by_level[NoveltyLevel.LEVEL1]()
```

Transform objects represent the novel change that has occurred, and consists of a 3-tuple: (Transformation_name, transformed_object, transformation)

```python 
print("\t{}", transform)
```

For example, a Level 3 transform in the blocksworld domain looks like:

```python
transform = ng.gen_by_level[NoveltyLevel.LEVEL3]()
print("\t{}", transform)
```
and the transform output:
```
('remove_effect',    # transformation name
 (:action unstack    # the modified TSAL construct, which here is an action
	:parameters (?x ?y)
	:precondition (and  (on ?x ?y) (clear ?x) (handempty))
	:effect (and (not (handempty)) (not (clear ?x)) (clear ?y) (holding ?x))
	), 
  (1.0, (not (on ?x ?y))), # the content of the transformation - this is what was removed
)
```

### Generate novelties based on a specific set of RTransformations

```python
from noveltygen.RTransformation import RTransformation

# choose your RTransformations 
rtransforms = [RTransformation.ADD_EFFECT,
               RTransformation.ADD_PRECONDITION,
               RTransformation.REMOVE_EFFECT]

# get a new environment only considering those RTransformations
transform = ng.gen_r_transform(transformations=rtransforms)
```


### Generate scenarios 

See domains/blocksworld/scenario_generator.py for a complete example

Create some object generators

```python
# define the object generators
block_objects_gen = ObjectGenerator(3, "block", "b")
player_objects_gen = ObjectGenerator(1, "player", "p")
```

Create a relation generator for `ontable` predicate:

```python
# get the blocks objects you want for the relation generation arguments
single_object_args = [[b] for b in block_objects_gen.draw()]

# set up relation generator for ontable
ontable_pred = [pred for pred in blocks_world_ng.domain.predicates if pred.name == "ontable"][0]
ontable_relation_gen = RelationGenerator(ontable_pred, single_object_args)
```

and make another one to say all blocks are `clear`:

```python
# set up relation generator for clear
clear_pred = [pred for pred in blocks_world_ng.domain.predicates if pred.name == "clear"][0]
clear_relation_gen = RelationGenerator(clear_pred, single_object_args)
```

Scenarios must have at least one player object, and `self` must be set in the initial facts:

```python
# set up relation generator for (= (self) p1)
self_fluent = [fluent for fluent in blocks_world_ng.domain.fluents if fluent.name == "self"][0]
equal_pred = Predicate("=")
# since only one player can be self, choose the first one (only matters when there's multiple players)
first_player = player_objects_gen.draw()[0]
player_relation_gen = RelationGenerator(equal_pred, [[self_fluent, first_player]])
```

Sometimes you have relations with no arguments:

```python
# set up relation generator for (handempty)
handempty_pred = [pred for pred in blocks_world_ng.domain.predicates if pred.name == "handempty"][0]

# NOTE: to specify no args as a possible arg_set, use an empty list [], hence the nested empty list [[]], which means
# there is one arg_set here and it's an empty arg_set. This is not the same as saying there are no arg_sets.
handempty_relation_gen = RelationGenerator(handempty_pred, [[]], "self")
```

Make a goal

```python
# generate a goal
self_expression = Expression(operator="=", 
                             left_child=Fluent(name="self"), 
                             right_child=Expression(value=first_player))
on_pred = [pred for pred in blocks_world_ng.domain.predicates if pred.name == "on"][0]

double_object_args = [[b1, b2] for b1 in block_objects_gen.draw() for b2 in block_objects_gen.draw() if b1 != b2]

on_relation = RelationGenerator(on_pred, double_object_args).draw()[0]
goal = [[self_expression, on_relation]]
```

Finally, put it all together into a scenario generator and call `draw()` to generate scenarios:

```python
bsg = ScenarioGenerator(object_generators=[block_objects_gen, player_objects_gen], 
                        relation_generators=[ontable_relation_gen, clear_relation_gen, player_relation_gen, handempty_relation_gen], 
                        domain=blocks_world_ng.domain, 
                        goal=goal)

problem_instance = bsg.draw()
```

## Future Tasks
- Add example of a T-Transformation
- Add search capability to generate T-transformations
- Add a TSAL Simulator so that we can test agents directly on novelty, similar to the pddl-gym library


## Support
Please submit an issue for any bugs or feature requests. Please contact Dustin (@dtdannen | dustin.dannenhauer@parallaxresearch.org) or Noah (@noahreifsnyder | noah.reifsnyder@parallaxresearch.org) with questions.

## Acknowledgements
This material is based upon work supported by the Defense Advanced Research Projects Agency (DARPA) under Contract No. HR001121C0236. Any opinions, findings, and conclusions or recommendations expressed in this material are those of the author(s) and do not necessarily reflect the views of the Defense Advanced Research Projects Agency (DARPA).


## License
MIT - please see the included license.