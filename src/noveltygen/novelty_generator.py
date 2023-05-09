import copy
import difflib
import os
from noveltygen import dimensions
import random
import datetime
from enum import Enum
import tsal
import tsal.interpreter
import tsal.translator.pddlToTsal

from noveltygen.RTransformations import RTransformations
from noveltygen.TTransformations import TTransformations
from noveltygen.TTransformations import ScenarioGenerator

from noveltygen.levels.novelty_level import NoveltyLevel
from noveltygen.levels import level1
from noveltygen.levels import level2
from noveltygen.levels import level3
from noveltygen.levels import level4
from noveltygen.levels import level5
from noveltygen.levels import level6
from noveltygen.levels import level7
from noveltygen.levels import level8


root = os.path.dirname(os.path.realpath(__file__))
root_ = root + "/"
sbcl = None
comb = None
remove_command = None
cp_dir = None

SAVEDIR = 'saved_novelty_examples'

novel_directory = "/novel"
um_domain_file = novel_directory + "/um_domain.pddl"
novel_domain_file = novel_directory + "/novel_domain.pddl"
novel_problem_file = novel_directory + "/novel_problem.pddl"


class NoveltyGenerator:
    novelty_range = (0, 0)
    generators = {}
    validators = {}
    novel_domain = False
    novel_problem = False
    novelty_dimension_funcs = {}
    dims = {}
    levels = {}

    def __init__(self, domain_file=None, problem_file=None):
        self.domain_file = domain_file
        self.problem_file = problem_file
        self.novelties = {"RTransformations": [], "TTransformations": []}
        if domain_file and not problem_file:
            self.domain = tsal.interpreter.Interpreter(domain_file=domain_file).domain
            self.problem = None
        elif domain_file and problem_file:
            interpreter = tsal.interpreter.Interpreter(domain_file=domain_file, problem_file=problem_file)
            self.domain = interpreter.domain
            self.problem = interpreter.problem
        self.rt = RTransformations(copy.deepcopy(self.domain))
        self.tt = TTransformations(self.problem, self.domain)
        self.sg = ScenarioGenerator(domain=self.domain)
        self.d_metrics = {}  # novelty -> agent -> problem -> score
        self.um_v_metrics = {}  # problem -> score ONLY FOR UM AGENT
        self.m_v_metrics = {}  # novelty -> problem -> score ONLY FOR M AGENT
        self.is_relevant = {}
        self.gen_by_level = {}
        self.load_novelty_levels2()

    def generate(self, level=0):
        assert_str = "Support novelty levels " + str(self.novelty_range[0]) + " through " + str(self.novelty_range[1])
        assert self.novelty_range[0] <= level <= self.novelty_range[1], assert_str
        self.generators[level](self)
        #getattr(self, "generate" + str(novelty_level.py))()
        #self.validate4()

    def validate(self, level):
        assert_str = "Support novelty levels " + str(self.novelty_range[0]) + " through " + str(self.novelty_range[1])
        assert self.novelty_range[0] <= level <= self.novelty_range[1], assert_str
        ret_val = getattr(self, "validate" + str(level))()
        print(ret_val)
        return ret_val

    def gen_r_transform(self, transformations=[], spec_avoid=[] ,actions=True, events=True):
        self.rt = RTransformations(copy.deepcopy(self.domain))
        while transformations:
            rt_i = random.choice(transformations)
            func = rt_i
            if isinstance(rt_i, Enum):
                func = str(rt_i.name).lower()
            #func = str(rt_i.name).lower()
            #transformations.remove(func)

            t = getattr(self.rt, func)(avoid=[x[0] for x in self.novelties['RTransformations'] if x[0][0] == func], spec_avoid=spec_avoid)
            if t[1] is not None:
                self.novel_domain = True
                self.novelties['RTransformations'].append((t, self.rt.domain))
                return t
            else:
                continue

        return None, None, None

    def select_novelties(self, num):
        self.novelties['RTransformations'] = random.sample(self.novelties['RTransformations'], min(len(self.novelties['RTransformations']), num))

    def save_novelties(self):
        for novelty in self.novelties['RTransformations']:
            func_name = novelty[0][0]
            func_dir = SAVEDIR + '/' + self.domain.name + '/' + func_name
            if not os.path.isdir(root_ + func_dir):
                os.makedirs(root_ + func_dir)
            pre_novelty = repr(self.domain)
            curr_time = datetime.datetime.now().strftime("%d-%m-%Y~%H_%M_%S,%f")
            test_filename = root_ + func_dir + '/' + func_name + '_' + curr_time
            desc = ','.join([repr(x) for x in novelty[0][1:]])
            post_novelty = repr(novelty[1])
            diff = ''.join(list(
                difflib.Differ().compare(pre_novelty.splitlines(keepends=True),
                                         post_novelty.splitlines(keepends=True))))
            output = '\n'.join([desc, 'DOMAIN CHANGE:', diff])
            with open(test_filename, 'w+') as f:
                f.write(output)

    def novelty_relevance(self, novelty):
        self.is_relevant[novelty] = False
        for key in self.d_metrics[novelty]['m']:
            m_metric = self.d_metrics[novelty]['m'][key]
            if key in self.d_metrics[novelty]['um']:
                um_metric = self.d_metrics[novelty]['um'][key]
            else:
                um_metric = self.um_v_metrics[key]
            if not m_metric or not um_metric:
                continue
            diff = m_metric - um_metric
            if diff != 0:
                self.is_relevant[novelty] = True

    def load_novelty_dimensions(self, dir_str='dimensions'):
        novelty_dimension_types = os.listdir(dir_str)
        for typ in novelty_dimension_types:
            path = "dimensions/" + typ
            if not os.path.isdir(path) or typ[0] == '_':
                continue
            novelty_dimension_files = os.listdir(path)
            for fi in novelty_dimension_files:
                if fi[0] == '_':
                    continue
                fi = fi[:-3]
                self.dims[fi.upper()] = getattr(getattr(dimensions, typ), fi)
        Novelty_Dimensions = Enum("Novelty_Dimensions", self.dims)

    def load_novelty_levels(self, dir_str='levels'):
        for level in os.listdir(dir_str):
            if level[0] == '_':
                continue
            level = level[:-3]
            self.levels[level.upper()] = getattr(self.levels, level)
        Novelty_Levels = Enum("Novelty_Levels", self.levels)

    def load_novelty_levels2(self):
        self.gen_by_level[NoveltyLevel.LEVEL1] = lambda: level1.gen(self)
        self.gen_by_level[NoveltyLevel.LEVEL2] = lambda: level2.gen(self)
        self.gen_by_level[NoveltyLevel.LEVEL3] = lambda: level3.gen(self)
        self.gen_by_level[NoveltyLevel.LEVEL4] = lambda: level4.gen(self)
        self.gen_by_level[NoveltyLevel.LEVEL5] = lambda: level5.gen(self)
        self.gen_by_level[NoveltyLevel.LEVEL6] = lambda: level6.gen(self)
        self.gen_by_level[NoveltyLevel.LEVEL7] = lambda: level7.gen(self)
        self.gen_by_level[NoveltyLevel.LEVEL8] = lambda: level8.gen(self)

    def novelty_controllability(self, potential_solutions):
        return False




