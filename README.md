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
from noveltygen import NoveltyGenerator as NG
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

### Generate scenarios 

See domains/blocksworld/scenario_generator.py

## Future Tasks
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