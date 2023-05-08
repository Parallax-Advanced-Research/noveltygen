import copy
from copy import deepcopy as dc
import random
from tsal.translator.expression import Expression
from tsal.translator.fluent import Fluent
from tsal.translator.literal import Literal
from tsal.translator.term import Term
from tsal.translator.predicate import Predicate
from queue import Queue
from tsal.translator.problem import Problem
from src.noveltygen.RTransformations import RTransformations

match_to_constants_first = True


class Generator:
    def __init__(self):
        pass

    def draw(self, scenario=None):
        pass


class ObjectGenerator(Generator):

    def __init__(self, num, typ, name):
        super().__init__()
        self.name = name
        self.num = num
        self.typ = typ

    def draw(self, scenario=None):
        ret_val = []
        for i in range(self.num):
            ret_val.append(Term.constant(self.name + str(i), self.typ))
        print(ret_val)
        return ret_val


class ValueGenerator(Generator):
    gen = None

    def __init__(self, gen=lambda: 0):
        if not type(gen) == type(lambda: 0):
            raise TypeError  # argument needs to be of function type.
        self.gen = gen
        pass

    def draw(self, scenario=None):
        return self.gen()


class RelationGenerator(Generator):
    pred = None
    args = []
    vg = ValueGenerator()

    def __init__(self, pred=None, args=[], vg=ValueGenerator()):
        self.pred = pred
        self.args = args
        self.vg = vg
        pass

    def draw(self, objects=None):
        print("Calling draw on RelationGenerator for pred {}".format(self.pred))
        print("self.args={}".format(self.args))
        ret_val = []
        for arg_set in self.args:
            print("arg_set={}".format(arg_set))
            #if self.vg:
            print("p = type(self.pred={})(self.pred.name={}, arg_set={})".format(type(self.pred), self.pred.name, arg_set))
            # if type(self.pred) == Fluent:
            #     p = Fluent(self.pred.name, args=arg_set), self.vg.draw())
            p = type(self.pred)(self.pred.name, arg_set)#, self.vg.draw())
            print("p={}".format(p))
            ret_val.append(p)
        return ret_val


class Performance():
    perf_func = None

    def __init__(self, performance_func):
        perf_func = performance_func


class ScenarioGenerator(Generator):
    class TTransformation:
        def __init__(self, sg):
            self.sg = sg
            pass

        def add_object_gen(self,
                           og):  # There should only be one object generator per object type, with the newest taking precedence.
            self.sg.object_generators[og.typ] = og
            pass

        def add_relation_gen(self, rg):
            self.sg.relation_generators.append(rg)
            pass

        def add_value_gen(self, vg):
            self.sg.value_generators.append(vg)
            pass

        def add_performance_metric(self, m):
            self.sg.performance = m
            pass

        def add_default_value(self, d):
            # d=(fluent_name, default_value) where d[0] = fluent_name and d[1] = default_value. There will only be 1 default value for any fluent name, with the newest taking precedence.
            self.sg.defaults[d[0]] = d[1]
            pass

    def __init__(self, domain=None, defaults=None, value_generators=None, object_generators=None, relation_generators=None,
                 performance=None, create_from_scratch=False, goal=[]):
        """
        If the domain is given, build a scenario generator from the domain. Otherwise, build a scenario generator
        from the other given parameters.
        """
        super().__init__()
        self.defaults = {}

        if create_from_scratch:
            print("Domain is {} NO SG GIVEN, MAKING SG FROM DOMAIN".format(domain))  # TODO: PRINT TO LOG FILE
            self.domain = domain
            self.build_fluents()
            self.build_defaults()
            self.build_object_generators()
            self.build_value_generators()
            self.build_relation_generators()
            self.tt = ScenarioGenerator.TTransformation(self)
        else:
            self.defaults = defaults
            self.value_generators = value_generators
            self.object_generators = object_generators
            self.relation_generators = relation_generators
            self.performance = performance
            self.goal = goal
            self.tt = ScenarioGenerator.TTransformation(self)


    def draw(self, scenario=None):
        objects = []
        for og in self.object_generators:
            # objects += self.object_generators[og].draw()
            new_objs = og.draw()
            print("Adding objects to draw: {}".format(new_objs))
            objects += new_objs
        inits = []
        for rg in self.relation_generators:
            new_rels = rg.draw(objects)
            print("Adding relations to draw: {}".format(new_rels))
            inits += new_rels

        #inits += list(self.defaults)
        print("inits={}".format(inits))
        scenario = Problem(objects=objects, init=inits, goal=self.goal)
        # TODO - the following code chunk seems leftover and needs to be moved somewhere else,
        # TODO - like in a change_goal() function
        # s = [x for x in inits if isinstance(x, Predicate) and x.args[0].name == 'self'][0]
        # s = Expression(operator=s.name, left_child=s.args[0], right_child=s.args[1])
        # goals = {"self": [s], "others": {}}
        # for a in [a for a in objects if a.type == scenario.self.type and a != scenario.self]:
        #     tmp = copy.deepcopy(s)
        #     tmp.right_child = a
        #     goals["others"][a.value] = [tmp]
        # scenario.goal = goals
        # tt = TTransformations(problem=scenario, domain=self.domain)
        # for agent in tt.problem.goal['others']:
        #     tt.change_goal(agent=agent)
        print(scenario)

    def build_object_generators(self, num=5):
        # print("CREATING OBJECT GENERATORS FROM TYPES, " + str(num) + " OF EACH") TODO:PRINT TO LOG FILE

        ret_val = []
        for typ in self.domain.litypes:
            ret_val.append(ObjectGenerator(name="gen_" + typ, num=num, typ=typ))
        self.object_generators = ret_val

    def build_value_generators(self):
        self.value_generators = []

    def build_relation_generators(self):  # implement
        ret_val = []
        for pred in [pred for pred in self.domain.predicates if len(pred.args) > 1]:
            pass
        for pred in self.fluents:
            args = []
            for arg in pred.args:
                args.append(None)
            print("self.defaults[{}] = {}".format(pred.name, self.defaults[pred.name]))
            ret_val.append(RelationGenerator(pred=pred, args=args, vg=self.defaults[pred.name]))
        self.relation_generators = ret_val

    def build_fluents(self):
        self.fluents = self.domain.fluents

    def build_defaults(self):
        for fluent in self.fluents:
            self.defaults[fluent.name] = None
            if fluent.type == 'int':
                # self.defaults[fluent.name] = 0
                self.defaults[fluent.name] = ValueGenerator(gen=lambda: 0)
                pass
            elif fluent.type == 'string':
                self.defaults[fluent.name] = ValueGenerator(gen=lambda: "nil")
            elif fluent.type in list(self.domain.constants.keys()):
                self.defaults[fluent.name] = ValueGenerator(
                    gen=lambda: random.choice(self.domain.constants[fluent.type]))
            else:
                self.defaults[fluent.name] = None

    def build_defaults2(self, objects):
        print(objects)
        defaults = []
        for f in self.domain.fluents:
            args_lst = []
            for arg in f.args:
                new_arg_lst = []
                for obj in [obj for obj in objects if obj.type == arg.type]:
                    if args_lst:
                        for arg_lst in args_lst:
                            new_arg_lst.append(arg_lst + [obj])
                    else:
                        new_arg_lst.append([obj])
                args_lst = new_arg_lst
            if args_lst:
                for arg_lst in args_lst:
                    if f.type != "int" and f.type != "string":  # TODO: HANDLE ELSE
                        print([obj for obj in objects if obj.type == f.type])
                        defaults.append(Predicate('=', [Fluent(f.name, arg_lst, typ=f.type),
                                                        random.choice([obj for obj in objects if obj.type == f.type])]))
                    elif f.type == "int":
                        pass
                    elif f.type == "string":
                        pass
            else:
                if f.type != "int" and f.type != "string":  # TODO: HANDLE ELSE
                    print([obj for obj in objects if obj.type == f.type])
                    defaults.append(Predicate('=', [Fluent(f.name, typ=f.type),
                                                    random.choice([obj for obj in objects if obj.type == f.type])]))
                elif f.type == "int":
                    pass
                elif f.type == "string":
                    pass
        return defaults


class TTransformations:
    def __init__(self, problem, domain, rt=None):
        self.problem = problem
        self.domain = domain
        if not rt:
            rt = RTransformations(domain=domain)
        self.rt = rt
        self.types = self.rt.types

    def change_init(self, new_inits=[]):
        new_scenario = dc(self.problem)
        for i in new_inits:
            if i.positive:
                if i.predicate not in new_scenario.init:
                    new_scenario.init.append(i.predicate)
            else:
                if i.predicate in new_scenario.init:
                    new_scenario.init.remove(i.predicate)
        uniq_str = ""
        for init in new_inits:
            uniq_str += "-" + str(hash(init))
        new_scenario.name = new_scenario.name + uniq_str
        return new_scenario

    def get_relevent_terms(self, goal):
        terms = []  # TODO: reference type to the type of fluents?
        q = Queue()
        for pred in goal:
            q.put((pred, None))
        while not q.empty():
            pred, typ = q.get()
            if isinstance(pred, Expression):
                if pred.value:
                    if isinstance(pred.value, str) and pred.value[0] == '?':
                        if not typ:
                            typ = 'int'
                        t = Term(name=Term(name=pred.value), type=typ)
                        t_in_terms = [x for x in terms if x == t]
                        if not t_in_terms:
                            terms.append(t)
                else:
                    l_predicate = pred.left_child
                    l_typ = None
                    r_predicate = pred.right_child
                    r_typ = None
                    if isinstance(l_predicate, Fluent):
                        l_real_predicate = [x for x in self.domain.fluents if x.name == pred.left_child.name][0]
                        l_typ = l_real_predicate.type
                    if isinstance(r_predicate, Fluent):
                        r_real_predicate = [x for x in self.domain.fluents if x.name == pred.right_child.name][0]
                        r_typ = r_real_predicate.type
                    q.put((pred.right_child, l_typ))
                    q.put((pred.left_child, r_typ))
            elif isinstance(pred, Fluent):
                fluent = [x for x in self.domain.fluents if x.name == pred.name][0]
                for i, arg in enumerate(fluent.args):
                    t = Term(name=Term(name=pred.args[i].name), type=arg.type)
                    t_in_terms = [x for x in terms if x == t]
                    if not t_in_terms:
                        terms.append(t)
            elif isinstance(pred, Literal):
                real_predicate = [x for x in self.domain.predicates if x.name == pred.predicate.name][0]
                for i, arg in enumerate(real_predicate.args):
                    t = Term(name=Term(name=pred.predicate.args[i].name), type=arg.type)
                    t_in_terms = [x for x in terms if x == t]
                    if not t_in_terms:
                        terms.append(t)
        random.shuffle(terms)
        return terms

    def help_add_precond_effect(self, goal, predicate, positive, op, rc, choice, avoid=[]):
        terms = self.get_relevent_terms(goal)
        typ = None
        tried = []
        tried_actions = []
        if predicate:
            typ = predicate.type
        while not predicate:
            if terms:
                found = False
                while not found:
                    found = True
                    left_over = [x for x in choice if x not in tried]
                    if not left_over:
                        tried_actions.append(goal)
                        left_over_actions = [x for x in self.domain.operators + self.domain.events if
                                             x not in tried_actions]
                        if not left_over_actions:  # TODO: raise error
                            return None, None, None
                        goal = random.choice(left_over_actions)
                        tried = []
                        left_over = [x for x in choice if x not in tried]
                        terms = self.get_relevent_terms(goal)
                    predicate = random.choice(left_over)
                    # target_predicate = 'space-color'
                    # predicate = random.choice([x for x in left_over if x.name == target_predicate])
                    tried.append(predicate)
                    if isinstance(predicate, Fluent):
                        typ = predicate.type
                        if not typ:
                            typ = 'int'
                    if isinstance(predicate, Fluent) and not typ:
                        print("here")
                    args = predicate.args
                    iter_args = dc(args)
                    if isinstance(predicate, Fluent):
                        iter_args.append(Term(name=Term(name='term'), type=predicate.type))
                    spec_args_lit_avoid = [x[2].predicate.args for x in avoid if
                                           x[1].name == goal.name and isinstance(x[2], Literal) and x[
                                               2].predicate.name == predicate.name]
                    spec_args_exp_avoid = [x[2].left_child.args for x in avoid if
                                           x[1].name == goal.name and isinstance(x[2], Expression) and x[
                                               2].left_child.name == predicate.name]
                    spec_args_avoid = spec_args_lit_avoid + spec_args_exp_avoid
                    # effect_preds = [x[1] for x in goal.effects[0] if isinstance(x[1], Literal)]
                    action_args_avoid = [x.predicate.args for x in goal if
                                         isinstance(x, Literal) and
                                         x.predicate.name == predicate.name]  # TODO line 385 here
                    using_lst = Queue()
                    using_lst_finalized = []
                    using_lst.put([])
                    if not iter_args and args:
                        found = False
                    while not using_lst.empty():
                        using = using_lst.get()
                        if len(using) == len(iter_args):
                            using_lst_finalized.append(using)
                            continue
                        arg = iter_args[len(using)]
                        arg_found = False
                        constants_and_terms = [x for x in terms]
                        if arg.type in self.domain.constants:
                            constants_and_terms += self.domain.constants[arg.type]
                        if arg.type in self.problem.objects:
                            constants_and_terms += [Term(name=Term(name=x), type=arg.type) for x in
                                                    self.problem.objects[arg.type]]
                        random.shuffle(constants_and_terms)

                        for term in constants_and_terms:
                            if arg.type == term.type or (
                                    term in self.types and arg.type in self.types[term]) or (
                                    arg in self.types and term.type in self.types[arg]):
                                if term.name:
                                    term = Term(name=term.name.name)
                                else:
                                    term = Term(name=term.value)
                                if term in using:
                                    continue
                                using_lst.put(using + [term])
                    if not using_lst_finalized:
                        found = False  # NOT FOUND
                        continue
                    use_lst_after_avoid = [x for x in using_lst_finalized if
                                           x not in spec_args_avoid + action_args_avoid]
                    if not use_lst_after_avoid:
                        found = False  # NOT FOUND
                        continue
                    use_choice = random.choice(use_lst_after_avoid)
                    if len(predicate.args) != len(use_choice):
                        use_choice = use_choice[:-1]
                    if isinstance(predicate, Predicate):
                        predicate = Predicate(name=predicate.name,
                                              args=use_choice)
                    elif isinstance(predicate, Fluent):
                        predicate = Fluent(name=predicate.name, args=use_choice,
                                           bounds=predicate.bounds)
            else:
                predicate = random.choice([x for x in choice if x not in tried])
                if isinstance(predicate, Fluent):
                    typ = predicate.type
                    if not type:
                        typ = 'int'
                tried.append(predicate)
        # elif not predicate:
        #    predicate = random.choice([x for x in choice if x not in tried])
        #    tried.append(predicate)
        new_predicate = None
        non_numeric_ops = ['=', '!=']
        if isinstance(predicate, Fluent):
            if not rc:
                args = [Term(name=x.name.name) for x in terms if x.type == typ]
                if typ in self.domain.constants:
                    args.extend([Term(value=x.value) for x in self.domain.constants[typ]])
                if args:
                    rc = random.choice(args)
                    rc = dc(rc)
                else:
                    if match_to_constants_first and typ in self.domain.constants:
                        rc = random.choice(self.domain.constants[typ])
                    elif typ == 'int':
                        rc = round(random.uniform(predicate.bounds[0], predicate.bounds[1]), predicate.bounds[2])
                    else:
                        rc = "?" + self.rt.gen_name(typ)
                if typ != 'int' and op not in non_numeric_ops:
                    op = random.choice(['=', '!='])
            # temp = predicate.args
            # if temp and len([x.type for x in temp if x.type]):
            #    print("here")

            new_predicate = Expression(operator=op, left_child=Predicate(name=predicate.name,
                                                                         args=[Term(name=x.name) for x in
                                                                               predicate.args]),
                                       right_child=rc)
        elif isinstance(predicate, Predicate):
            if not positive:
                positive = random.random() < .5
            new_predicate = Literal(Predicate(name=predicate.name, args=[Term(name=x.name) for x in predicate.args]),
                                    positive)
        return goal, new_predicate

    def add_goal(self, goal=None, goal_choice=None,
                 positive: bool = random.random() < .5,
                 op=random.choice(['>', '<', '<=', '>=', '=']),
                 rc=None, avoid=[]):
        # TODO: add children types possibility in new precondition from predicate
        # TODO: link code between add effect and precondition, its so similar
        new_goal = None
        tried = []
        while not new_goal:
            # choicedp = [x for x in self.domain.predicates if x.name in [x.name for x in self.domain.derivedpredicates]]
            choice = self.domain.predicates + self.domain.fluents
            goal, new_goal = self.help_add_precond_effect(goal, goal_choice, positive, op,
                                                          rc, choice, avoid)
            tried.append((goal, new_goal))
            if isinstance(new_goal, Literal):
                if [x for x in goal if
                    isinstance(x, Literal) and x.predicate == new_goal.predicate]:
                    new_goal = None
            elif isinstance(new_goal, Expression):
                if [x for x in goal if
                    isinstance(x, Expression) and x == new_goal]:
                    new_goal = None

        goal += [new_goal]  # TODO: check if lit already in precond, make new one if so
        return goal, new_goal

    def change_goal(self, agent=None, len_min=3, len_max=5):
        if len(self.problem.goal['others']) == 0:
            return None, None, None

        if not agent:
            agent = random.choice(list(self.problem.goal['others'].keys()))

        self.problem.goal['others'][agent] = [[x for x in self.problem.goal['others'][agent] if isinstance(x,
                                                                                                           Expression) and x.left_child.name == "self" and x.right_child.value == agent][
                                                  0]]
        for i in range(random.randrange(len_min, len_max)):
            goal, new_goal = self.add_goal(goal=self.problem.goal['others'][agent])
        return "change_goal", agent, self.problem.goal['others'][agent]
