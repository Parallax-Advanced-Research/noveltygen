# Novelty Generator

Novelty Generation using the Tsal Language. Allows the user to generate novel domain and problem
files given a base domain and problem. 

***

## About

This is the implementation of the novelty generator from the following publications. Please cite the most recent publication if you use this code in your work:
* Molineaux, Dannenhauer, and Kildebeck (2023) - "A Framework for Characterizing Novel Environment Transformations in General Environments" *Under Review*
* Dannenhauer, D., Reifsnyder, N., Regester, AJ., Molineaux, M. "Transforming Environments to Evaluate Agent Adaptation." Advances in Cognitive Systems (ACS). George Mason University, Arlington, VA. 2022.

Related work:

* Molineaux, M., Dannenhauer, D. "An Environment Transformation-based Framework for Comparison of Open-World Learning Agents." Designing Artificial Intelligence for Open Worlds. AAAI Spring Symposium Series 2022. Stanford University, CA. 2022. 

## Installation
This package depends on our submodule [tsal-interpreter](put-link-here.com). After cloning the novelty generator into your project, make sure to initialize the interepreter. This can be
done as follows:
```commandline
# get the repo and and submodules
git clone ...
cd novelty-generator
git submodule update --init --remote

# set up a virtualenv and install packages
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# add the novelty generator to your python path
pip install .
```

If you plan to modify the novelty generator code, install via:

```commandline
pip install -e .
```

## Usage

These examples can be found in examples/example.py. These examples build on each other.

### Creating a novelty generator
```python
from novelty_generator import NoveltyGenerator as NG
ng = NG(domain_file='domains/blocksworld/domain.tsal', problem_file='domains/blocksworld/problem.tsal')
```

### Generating a novelty at a novelty level

Novelty levels refer to a categorization of different kinds of novelty from Kildebeck et al. 2022 - "2022 Novelty Hierarchy." *Unpublished manuscript.*

```python
transform = NG.Novelty_Levels.LEVEL1.value.gen(ng)
```

Transform objects represent the novel change that has occurred, and consists of a 3-tuple: (Transformation_name, transformed_object, transformation)

```python 
print("\t{}", transform)
```

For example, a Level 3 transform in the blocksworld domain looks like:

```python
transform = NG.Novelty_Levels.LEVEL3.value.gen(ng)
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

### Generate a novelty at each novelty level
```python
for level in NG.Novelty_Levels:  
    transform = level.value.gen(ng)
```

## Future Tasks
- Refactor the code so there's a top level src directory with all code under that. Move the current exmaples/ directory to a src/generation_methods directory; it's not really containing current examples, but instead different ways of constraining novelty generation.
- Add documentation for the Scenario Generator
- Add example of a T-Transformation
- Add search capability to generate T-transformations
- Add a TSAL Simulator so that we can test agents directly on novelty, similar to the pddl-gym library


## Support
Please submit an issue for any bugs or feature requests. Please contact Dustin (@dtdannen | dustin.dannenhauer@parallaxresearch.org) or Noah (@noahreifsnyder | noah.reifsnyder@parallaxresearch.org) with questions.

## Acknowledgements
This material is based upon work supported by the Defense Advanced Research Projects Agency (DARPA) under Contract No. HR001121C0236. Any opinions, findings, and conclusions or recommendations expressed in this material are those of the author(s) and do not necessarily reflect the views of the Defense Advanced Research Projects Agency (DARPA).


## License
MIT - please see the included license.