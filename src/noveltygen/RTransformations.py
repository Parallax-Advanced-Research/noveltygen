import itertools
import random
import types
import copy
import os
import datetime
import difflib
import pprint
import sys
import typing
from typing import Union
from copy import deepcopy as dc
from tsal.translator.action import Action
from tsal.translator.event import Event
from tsal.translator.term import Term
from tsal.translator.predicate import Predicate
import string
from tsal.translator.derived_predicate import DerivedPredicate
from tsal.translator.expression import Expression
from tsal.translator.fluent import Fluent
from tsal.translator.literal import Literal

from queue import Queue
import time
import inspect

SAVEDIR = 'saved_novelty_examples'


# Process Flow:
# 1. Iterate over every possible transformation?
# 1.1 probability attached to transformation?
# 1.2 hierarchically organize the transformations, probability to step into each.
# 2. should be able to ask it to start anywhere in the hierarchy and only step downwards from there.
# 2.1 operates the same as main algorithm. Can denote multiple start points.
# 2.2 if start point is subset transform of another start point, ignore OR throw error. TODO: discuss

# dependency graph for removal.

class SubVar:
    class_name = 'ParentClass'


class SubVarE(SubVar):  # used for function typing to map variables that are subvars of earlier arguments
    class_name = 'effects0'


class SubVarFE(SubVar):  # used for function typing to map variables that are subvars of earlier arguments
    class_name = 'fluent_effects'
    bounds = []


class SubVarP(SubVar):  # used for function typing to map variables that are subvars of earlier arguments
    class_name = 'precond'


class ArgLength:
    class_name = 'ArgLength'
    max_args = 3
    min_args = 0


class ArgLengthP(ArgLength):
    class_name = "Predicates"
    types = ['predicates', 'fluents']
    max_args = 3
    min_args = 0


class ArgLengthDP(ArgLength):
    class_name = "DerivedPredicates"
    types = ['predicates', 'fluents']
    max_args = 4
    min_args = 2


class ArgLengthT(ArgLength):
    class_name = 'Terms'
    types = ['types']
    max_args = 3
    min_args = 0


class Bounds(ArgLength):  # TODO: match this to enumerating function
    min_args = 3
    max_args = 3
    class_name = 'Integers'


add_type_parent = True
max_parameter_num = 3
min_parameter_num = 1
max_preconditions = 4
min_preconditions = 1
fluent_max_args = 3
fluent_min_args = 0
max_effects = 4
min_effects = 1
max_predicates = 4
min_predicates = 1
max_pred_args = 4
min_pred_args = 1
match_types = True
dp_match_types = True
relevent_pre_eff = True
match_to_constants_first = True


# free or grounded(in parameters) variables, bool or prob.
# transform for add/remove parameters.
# knob for whether to add from action or not


# Transform Class. create transform objects? then parent child relation of objects?

class RTransformations:

    @staticmethod
    def get_random_value():
        return random.getrandbits(5)

    @staticmethod
    def gen_name(typ):
        letters = string.ascii_lowercase
        num_letters = round(random.uniform(4, 10))
        if typ:
            name = 'gen_' + typ + '_' + ''.join(random.choice(letters) for _ in range(num_letters))
        else:
            name = 'gen_' + ''.join(random.choice(letters) for _ in range(num_letters))
        return name

    def check(self, prob):
        if not prob:
            prob = self.t_prob
        if random.random() > prob:
            return True
        else:
            return False

    def add_type(self, name: str = None, parent: Term = None, avoid=[], spec_avoid=[]):
        # matches slides, addition of possibility to add type to document
        if not name:
            name = self.gen_name('type')
        while name in self.types:
            name = self.gen_name('type')
        if add_type_parent and not parent:
            self.add_type_parent(name, "object")
        if add_type_parent and parent:
            self.add_type_parent(name, parent)
        self.li_types.append(name)
        return ("add_type", self.types, name)

    def add_type_parent(self, type, parent):
        # matches slides and document
        if not type and not parent:
            type = random.choice([x for x in self.li_types if x])
        if not type:
            type = random.choice([x for x in self.li_types if
                                  x and (parent not in self.domain.types or x not in self.domain.types[parent])])
        if not parent:
            parent = random.choice(
                [x for x in self.li_types if x and (x not in self.domain.types or type not in self.domain.types[x])])
        if parent not in self.domain.types:
            self.domain.types[parent] = []
        self.domain.types[parent].append(type)
        self.types[type] = parent

    def remove_type_parent(self, type, parent):
        # matches slides and document. Assumes given arguments work/there is some super type in the domain
        if not type and not parent:
            type = random.choice(list({x for y in self.domain.types for x in self.domain.types[y]}))
        if not type:
            type = random.choice([x for x in self.domain.types[parent]])
        if not parent:
            parent = random.choice([x for x in self.domain.types if type in self.domain.types[x]])
        if parent not in self.domain.types:
            self.domain.types[parent] = []
        self.domain.types[parent].append(type)
        self.types[type] = parent

    def add_constant(self):
        pass

    def remove_constant(self):
        pass

    def add_fluent(self, name: str = None, args: ArgLengthT = [], bounds: Bounds = []):
        #  takes constructor args, instead of main fluent. Matches slides, not document
        if not name:
            name = self.gen_name('fluent')
        if not args:
            num_args = random.randrange(fluent_min_args, fluent_max_args + 1)
            args = []
            for i in range(num_args):
                typ = random.choice([x for x in self.li_types if x])
                term_name = '?' + self.gen_name('term')
                term = Term(name=term_name, type=typ)
                args.append(term)
        if not bounds:
            bounds = [0, 100, 2]
        fluent = Fluent(name, args, bounds)
        self.domain.fluents.append(fluent)

    def remove_fluent(self, fluent=None, avoid=[]):
        # matches slides, not in document
        if not fluent:
            fluent = random.choice(self.domain.fluents)
        self.domain.fluents = [x for x in self.domain.fluents if x != fluent]

    def add_action(self, preconditions: ArgLengthP = [], effects: ArgLengthP = [], max_pre=3, max_eff=3):
        new_action_name = self.gen_name('action')
        while new_action_name in [x.name for x in self.domain.operators]:
            new_action_name = self.gen_name('action')
        new_action = Action(name=new_action_name, params=[], precond=[], effects=[[]])
        self.new_dependencies(new_action)
        if preconditions:
            for precond in preconditions:
                self.add_precondition(new_action, precond)
        else:
            num_precond = random.randrange(min_preconditions, max_preconditions + 1)
            for i in range(num_precond):
                self.add_precondition(new_action)
        if effects:
            for effect in effects:
                self.add_effect(new_action, effect)
        else:
            num_effects = random.randrange(min_effects, max_effects + 1)
            for i in range(num_effects):
                self.add_effect(new_action)
        self.domain.operators.append(new_action)

    def add_event(self, event_name: str = None, avoid=[], spec_avoid=[]):
        """
        event_name: name of the event to add, a random one will be generated
        avoid: only for matching the same call style as other functions, not used here
        spec_avoid: only for matching the same call style as other functions, not used here
        """
        if not event_name:
            event_name = self.gen_name('event')
        while event_name in [x.name for x in self.domain.events]:
            event_name = self.gen_name('event')
        new_event = Event(name=event_name, params=[], precond=[], effects=[[]])
        self.domain.events.append(new_event)
        return "add_event", self.domain.events, new_event

    def add_event_full(self, preconditions: ArgLengthP = [], effects: ArgLengthP = [], max_pre=3, max_eff=3):
        """Adds a new event and does extra steps to populate it. This is a convenience because it is technically
        applying multiple RTransformations at the same time"""
        # TODO: Duration and distribution
        letters = string.ascii_lowercase
        num_letters = round(random.uniform(4, 10))
        new_event_name = 'gen_event_' + ''.join(random.choice(letters) for i in range(num_letters))
        while new_event_name in [x.name for x in self.domain.events]:
            new_event_name = 'gen_event_' + ''.join(random.choice(letters) for i in range(num_letters))
        new_event = Event(name=new_event_name, params=[], precond=[], effects=[[]])
        self.new_dependencies(new_event)
        if preconditions:
            for precond in preconditions:
                self.add_precondition(new_event, precond)
        else:
            num_precond = random.randrange(1, max_pre)
            for i in range(num_precond):
                self.add_precondition(new_event)
        if effects:
            for effect in effects:
                self.add_effect(new_event, effect)
        else:
            num_effects = random.randrange(1, max_eff)
            for i in range(num_effects):
                self.add_effect(new_event)
        self.domain.events.append(new_event)

    def remove_action(self, action: Action, prob=None, avoid=[]):
        if self.check(prob) or action not in self.domain.operators:
            return
        self.delete_dependencies(action)
        self.domain.operators.remove(action)

    def remove_event(self, event: Event=None, avoid=[], spec_avoid=[]):
        """
        event: event to remove, a random one will be chosen if none is provided
        avoid: events to avoid
        spec_avoid: only for matching the same call style as other functions, not used here
        TODO: To follow the single-step transformation paradigm, this should only remove an event if it has
        TODO: no preconditions or effects. This is not currently implemented.
        """

        if not self.domain.events:
            return "remove_event", None, None

        if not event:
            event = random.choice([x for x in self.domain.events if x not in avoid])

        if event not in self.domain.events:
            return "remove_event", None, None

        new_events = [e for e in self.domain.events if e != event]
        self.domain.events = new_events
        self.delete_dependencies(event)
        return "remove_event", self.domain.events, event

    def event_to_action(self, event: Event=None, avoid=[], spec_avoid=[]):

        if not self.domain.events:
            return "event_to_action", None, None

        if event is None:
            event = random.choice([x for x in self.domain.events if x not in avoid])

        if event not in self.domain.events:
            return "event_to_action", None, None

        # same_names = [x for x in self.domain.operators if x.name == event.name]
        new_action = Action(dc(event.name), dc(event.params), dc(event.precond), dc(event.effects), dc(event.duration))
        if event in self.domain.events:
            new_events = [e for e in self.domain.events if e != event]
            self.domain.events = new_events
            self.delete_dependencies(event)
        self.domain.operators.append(new_action)
        self.new_dependencies(new_action)

        return "event_to_action", event, new_action

    def action_to_event(self, action: Action=None, avoid=[], spec_avoid=[]):

        if not self.domain.operators:
            return "action_to_event", None, None

        if action is None:
            action = random.choice([x for x in self.domain.operators if x not in avoid])

        if action not in self.domain.operators:
            return "action_to_event", None, None

        new_event = Event(action.name, action.params, action.precond, action.effects, action.duration)
        self.domain.operators.remove(action)
        new_events = self.domain.events + [new_event]
        self.domain.events = new_events
        self.delete_dependencies(action)
        self.new_dependencies(new_event)

        return "action_to_event", action, new_event

    def get_relevent_terms(self, action_event):
        terms = []  # TODO: reference type to the type of fluents?
        q = Queue()
        for pred in action_event.precond:
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

    def help_add_precond_effect(self, action_event, predicate, positive, op, rc, choice, events=True, operators=True, avoid=[]):
        if not choice:
            return None, None, None

        if not action_event:
            choice_lst = []
            if events:
                choice_lst += self.domain.events
            if operators:
                choice_lst += self.domain.operators

            if not choice_lst:
                return None, None, None

            action_event = random.choice(choice_lst)
        terms = self.get_relevent_terms(action_event)

        typ = None
        tried = []
        tried_actions = []
        if predicate:
            typ = predicate.type
        if relevent_pre_eff and not predicate:
            if terms:
                found = False
                while not found:
                    found = True
                    left_over = [x for x in choice if x not in tried]
                    if not left_over:
                        tried_actions.append(action_event)
                        left_over_actions = [x for x in choice_lst if
                                             x not in tried_actions]
                        if not left_over_actions:  # TODO: raise error
                            return None, None, None
                        action_event = random.choice(left_over_actions)
                        tried = []
                        left_over = [x for x in choice if x not in tried]
                        terms = self.get_relevent_terms(action_event)
                    if not left_over:
                        return None, None, None
                    predicate = random.choice(left_over)
                    # target_predicate = 'space-color'
                    # predicate = random.choice([x for x in left_over if x.name == target_predicate])
                    tried.append(predicate)
                    if isinstance(predicate, Fluent):
                        typ = predicate.type
                        if not typ:
                            typ = 'int'
                    args = predicate.args
                    iter_args = dc(args)
                    if isinstance(predicate, Fluent):
                        iter_args.append(Term(name=Term(name='term'), type=predicate.type))
                    # random.shuffle(iter_args)
                    # if isinstance(new_effect, Literal):
                    #    if [x for x in action_event.precond + action_event.effects if
                    #        isinstance(x, Literal) and x.predicate == new_effect.predicate]:
                    #        new_effect = None
                    # if isinstance(new_effect, Expression):
                    #     if [x for x in action_event.precond + action_event.effects if
                    #         isinstance(x,
                    #                    Expression) and x.left_child == new_effect.left_child] or new_effect.operator == '!=':
                    #         new_effect = None
                    spec_args_lit_avoid = [x[2].predicate.args for x in avoid if
                                           x[1].name == action_event.name and isinstance(x[2], Literal) and x[
                                               2].predicate.name == predicate.name]
                    spec_args_exp_avoid = [x[2].left_child.args for x in avoid if
                                           x[1].name == action_event.name and isinstance(x[2], Expression) and x[
                                               2].left_child.name == predicate.name]
                    spec_args_avoid = spec_args_lit_avoid + spec_args_exp_avoid
                    effect_preds = [x[1] for x in action_event.effects[0] if isinstance(x[1], Literal)]
                    action_args_avoid = [x.predicate.args for x in action_event.precond + effect_preds if
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
        elif not predicate:
            predicate = random.choice([x for x in choice if x not in tried])
            tried.append(predicate)
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
                    elif typ == 'string':
                        rc = 'I dont know how to generate a relevent string as its domain dependeant atleats for monopoly'
                    else:
                        rc = "?" + self.gen_name(typ)
                if typ != 'int' and op not in non_numeric_ops:
                    op = random.choice(['=', '!='])
            new_predicate = Expression(operator=op, left_child=Predicate(name=predicate.name,
                                                                         args=[Term(name=x.name) for x in
                                                                               predicate.args]),
                                       right_child=rc)
        elif isinstance(predicate, Predicate):
            if not positive:
                positive = random.random() < .5
            new_predicate = Literal(Predicate(name=predicate.name, args=[Term(name=x.name) for x in predicate.args]),
                                    positive)
        return action_event, new_predicate, dc(action_event.params)

    def add_precondition(self, action_event: Union[Action, Event] = None, precond: Union[Predicate, Fluent] = None,
                         positive: bool = random.random() < .5,
                         op=random.choice(['>', '<', '<=', '>=', '=']),
                         rc=None, avoid=[], spec_avoid=[]):
        # TODO: add children types possibility in new precondition from predicate
        # TODO: link code between add effect and precondition, its so similar
        new_precond = None
        events = True
        operators = True
        if "events" in spec_avoid:
            events = False
        if "operators" in spec_avoid:
            operators = False
        tried = []

        while not new_precond:
            choicedp = [x for x in self.domain.predicates if
                        x.name not in [x.name for x in self.domain.derivedpredicates] + spec_avoid]
            choice = choicedp + [x for x in self.domain.fluents if x.name not in spec_avoid]
            #choicedp = [x for x in self.domain.predicates if x.name in [x.name for x in self.domain.derivedpredicates]]
            #choice = self.domain.predicates + self.domain.fluents

            if not choice:
                return None, None, None

            action_event, new_precond, new_params = self.help_add_precond_effect(action_event, precond, positive, op,
                                                                                 rc, choice, events, operators, avoid)
            if not action_event and not new_precond and not new_params:
                return None, None, None

            tried.append((action_event, new_precond))
            if isinstance(new_precond, Literal):
                if [x for x in action_event.precond + action_event.effects if
                    isinstance(x, Literal) and x.predicate == new_precond.predicate]:
                    new_precond = None
            elif isinstance(new_precond, Expression):
                if [x for x in action_event.precond + action_event.effects if
                    isinstance(x, Expression) and x == new_precond]:
                    new_precond = None

        action_event.precond += [new_precond]  # TODO: check if lit already in precond, make new one if so
        action_event.params = new_params
        self.new_depen(action_event, new_precond, 'precond')
        return "add_precondition", action_event, new_precond

    def add_effect(self, action_event: Union[Action, Event] = None, effect: Union[Predicate, Fluent] = None,
                   positive: bool = random.random() < .5,
                   op=random.choice(['+', '-', '*', '/']),
                   rc=None, avoid=[], spec_avoid=[]):
        # TODO: add children types possibility in new precondition from predicate
        new_effect = None
        events = True
        operators = True
        if "events" in spec_avoid:
            events = False
        if "operators" in spec_avoid:
            operators = False
        while not new_effect:
            choicedp = [x for x in self.domain.predicates if
                        x.name not in [x.name for x in self.domain.derivedpredicates]+spec_avoid]
            choice = choicedp + [x for x in self.domain.fluents if x.name not in spec_avoid]

            if not choice:
                return None, None, None

            action_event, new_effect, new_params = self.help_add_precond_effect(action_event, effect, positive, op, rc,
                                                                                choice, events, operators, avoid)

            if not action_event and not new_effect and not new_params:
                return None, None, None

            # if isinstance(new_effect, Literal):
            #    if [x for x in action_event.precond + action_event.effects if
            #        isinstance(x, Literal) and x.predicate == new_effect.predicate]:
            #        new_effect = None
            if isinstance(new_effect, Expression):
                if [x for x in action_event.precond + action_event.effects if
                    isinstance(x, Expression) and x.left_child == new_effect.left_child] or new_effect.operator == '!=':
                    new_effect = None
        if not action_event.effects:
            action_event.effects = [[]]
        action_event.effects[0] += [(random.random(), new_effect)]
        # TODO: check if lit already in effect, make new one if so  action_event.params = new_params
        action_event.params = new_params
        self.new_depen(action_event, new_effect, 'effect')
        return "add_effect", action_event, new_effect

    def change_effect_probability(self, action_event: Union[Action, Event]=None, effect: SubVarE=None,
                                  new_prob=random.random(), prob=None, avoid=[], spec_avoid=[]):
        if not action_event:
            action_event = random.choice(self.domain.operators+self.domain.events)
        effs = [x for x in action_event.effects[0] if isinstance(x[1], Expression)]
        while not effs:
            avoid.append(action_event)
            action_choices = [x for x in self.domain.operators + self.domain.events if x not in avoid]
            if not action_choices:
                return None, None, None
            action_event = random.choice([x for x in self.domain.operators + self.domain.events if x not in avoid])
            effs = [x for x in action_event.effects[0] if isinstance(x[1], Expression)]
        if not effect:
            effect = random.choice(effs)
        if self.check(prob):
            return
        remove = None
        if isinstance(effect, tuple):  # You can call this on the effect literal, or the tuple with prob
            effect = effect[1]
        new_effect = (new_prob, dc(effect))
        for eff in action_event.effects[0]:
            if eff[1] == effect:
                remove = eff
        action_event.effects[0].remove(remove)
        action_event.effects[0].append(new_effect)
        return "change_effect_probability", action_event, new_effect

    def change_fluent_effect_value(self, action_event: Union[Action, Event]=None, effect: SubVarFE=None,
                                   rc=None, avoid=[], spec_avoid=[]):
        if not action_event:
            action_event = random.choice(self.domain.operators + self.domain.events)
        effs = [x for x in action_event.effects[0] if isinstance(x[1], Expression)]
        while not effs:
            avoid.append(action_event)
            action_choices = [x for x in self.domain.operators + self.domain.events if x not in avoid]
            if not action_choices:
                return None, None, None
            action_event = random.choice(action_choices)
            effs = [x for x in action_event.effects[0] if isinstance(x[1], Expression)]
        if not effect:
            effect = random.choice(effs)
        if isinstance(effect, list):
            effect = effect[1]
        if isinstance(effect, tuple):
            effect = effect[1]
        if not rc:
            bounds = [x for x in self.domain.fluents if x.name == effect.left_child.name][0].bounds
            if bounds:
                rc = round(random.uniform(bounds[0], bounds[1]), bounds[2])
            else:
                rc = self.get_random_value()
        effect.right_child = rc
        return "change_fluent_effect_value", action_event, effect

    def change_event_frequency(self, event, freq, avoid=[]):
        pass

    def change_event_probability(self, event, prop, avoid=[]):
        pass

    def remove_effect(self, action_event: Union[Action, Event]=None, effect: SubVarE=None, prob=None, avoid=[], spec_avoid=[]):
        # TODO: update param list if possible
        if not action_event:
            action_event = random.choice(self.domain.operators+self.domain.events)
        if not effect:
            effect = random.choice(action_event.effects[0])
        if self.check(prob) or action_event not in self.domain.operators + self.domain.events:
            return
        effects = action_event.effects[0]
        if isinstance(effect, tuple):
            for eff in effects:
                if eff == effect:
                    effects.remove(eff)
                    break
        else:
            for eff in effects:
                if eff[1] == effect:
                    effects.remove(eff)
                    break
        action_event.effects = [effects]
        for dependency in self.dependencies['rlu'][action_event]:
            args = [action_event] + dependency[2:]
            if args[1] == 'effect' and args[2] == effect:
                self.dependencies[dependency[0]][dependency[1]].remove(args)
        return "remove_effect", action_event, effect

    def remove_precondition(self, action_event: Union[Action, Event]=None, precond: SubVarP=None, avoid=[], spec_avoid=[]):
        """
        action_event: Action or Event that has the precondition to be removed (if None, a random one is chosen)
        precond: precondition to be removed (if None, a random one is chosen)
        avoid: list of actions/events to avoid
        spec_avoid: list of specific preconditions to avoid # todo currently exists to keep API calls similar, but not used
        """

        # TODO: update param list if possible
        if action_event is None:
            action_event = random.choice([x for x in self.domain.operators+self.domain.events if x not in avoid])

        if action_event not in self.domain.operators + self.domain.events:
            # this should only happen an action_event is passed in and doesn't exist in the domain
            return

        preconds = action_event.precond

        if precond is None:
            precond = random.choice([x for x in action_event.precond if x not in spec_avoid])

        preconds.remove(precond)
        action_event.precond = preconds
        for dependency in self.dependencies['rlu'][action_event]:
            args = [action_event] + dependency[2:]
            if args[1] == 'precond' and args[2] == precond:
                self.dependencies[dependency[0]][dependency[1]].remove(args)

        return "remove_precondition", action_event, precond

    def remove_type(self, typ: Term):
        # TODO: typing on typ to match other functions, get possible args from domain
        # TODO: update to refelct remove pred
        # TODO: consider update where we link types to predicates, and remove predicates that involve type?
        remove = []
        dependencies = (self.dependencies['types'][typ])
        for action_event, p_e, depen_pred, term in dependencies:
            if p_e == 'precond':
                precond = action_event.precond
                if depen_pred in precond:  # Could have been previously deleted if multiple args of pred are of type typ
                    precond.remove(depen_pred)
                action_event.precond = precond
                for dependency in self.dependencies['rlu'][action_event]:
                    args = [action_event] + dependency[2:]
                    if args[1] == 'precond' and args[2] == depen_pred:
                        remove.append((dependency[0], dependency[1], args))
            elif p_e == 'effects':
                effects = action_event.effects[0]
                for eff in effects:
                    if eff[1] == depen_pred:
                        effects.remove(eff)
                        break
                action_event.effects = [effects]
                for dependency in self.dependencies['rlu'][action_event]:
                    args = [action_event] + dependency[2:]
                    if args[1] == 'effect' and args[2] == depen_pred:
                        remove.append((dependency[0], dependency[1], args))
            else:
                print("Something went wrong in Remove_Type")
        removed = []
        for dependency in remove:
            if dependency in removed:
                continue
            self.dependencies[dependency[0]][dependency[1]].remove(dependency[2])
            removed.append(dependency)
        new = [typ]
        remove = []
        while new:
            temp = dc(new)
            for t in temp:
                new.remove(t)
                remove.append(t)
                if t in self.domain.types:
                    new += self.domain.types[t]
                    if t in new:
                        new.remove(t)
        for t in remove:
            if t in self.domain.types:
                self.domain.types.pop(t)
            if t in self.li_types:
                self.li_types.remove(t)
            if t in self.types:
                self.types.pop(t)
        for t in self.domain.types:
            self.domain.types[t] = [x for x in self.domain.types[t] if x not in remove]

    # def change_type_parent(self, typ):
    #   pass  # TODO: This one feels excessively tricky

    def add_predicate(self, terms: ArgLengthT = []):
        letters = string.ascii_lowercase
        num_letters = round(random.uniform(4, 10))
        new_pred_name = self.gen_name('predicate')
        num_args = random.randrange(min_pred_args, max_pred_args + 1)
        args = []
        arg_names = []
        for i in range(num_args):
            typ = random.choice([x for x in self.li_types if x])
            name_length = random.randrange(2, 4)
            name = '?' + ''.join(random.sample(typ, name_length))
            while name in arg_names:
                name_length = random.randrange(2, 4)
                name = '?' + ''.join(random.sample(typ, name_length))
            arg_names.append(name)
            args.append(Term(name=Term(name=name), type=typ))
        new_pred = Predicate(name=new_pred_name, args=args)
        self.domain.predicates.append(new_pred)

    def remove_predicate(self, pred: Predicate):
        dependencies = dc(self.dependencies['predicates'][pred])
        for action_event, p_e, depen_pred in dependencies:
            if p_e == 'precond':
                self.remove_precondition(action_event, depen_pred)
            elif p_e == 'effects':
                self.remove_effect(action_event, depen_pred)
            else:
                print("Something went wrong in Remove_Predicate")

    def add_derived_predicate(self, predicates: ArgLengthDP = [], max_pred_range=3):
        pred_num = round(random.uniform(2, 2 + max_pred_range))
        pred_num = min(pred_num, len(self.domain.predicates))
        preds = random.sample(self.domain.predicates, pred_num)
        types = {}
        for pred in preds:
            pred_types = {}
            for arg in pred.args:
                if arg.type not in pred_types:
                    pred_types[arg.type] = 0
                pred_types[arg.type] += 1
            for p in pred_types:
                if p not in types:
                    types[p] = 0
                if pred_types[p] > types[p]:
                    types[p] = pred_types[p]
        predicates = dc(self.domain.predicates)
        random.shuffle(predicates)
        derived_pred = None
        for pred in predicates:
            pred_types = {}
            for arg in pred.args:
                if arg.type not in pred_types:
                    pred_types[arg.type] = 0
                pred_types[arg.type] += 1
            works = True
            for p in pred_types:
                if p not in types or pred_types[p] > types[p]:
                    works = False
                    break
            if works:
                derived_pred = pred
                break
        new_derived_predicate = DerivedPredicate(derived_pred.name, derived_pred.args, preds)
        self.domain.derivedpredicates.append(new_derived_predicate)

        # TODO: create new predicate for derived and arg list, match names of types
        pass

    def remove_derived_predicate(self, pred: DerivedPredicate):
        self.domain.derivedpredicates.remove(pred)

    def delete_dependencies(self, action_event):
        for dependency in self.dependencies['rlu'][action_event]:
            args = [action_event] + dependency[2:]
            self.dependencies[dependency[0]][dependency[1]].remove(args)
        self.dependencies['rlu'].pop(action_event)
        return

    def new_depen(self, action_event, literal, p_e):
        literals = []
        if isinstance(literal, Expression):
            literals += [(x, 'fluents', Fluent) for x in [literal.left_child, literal.right_child] if
                         isinstance(x, Fluent)]
        else:
            literals += [(literal.predicate, 'predicates', Predicate)]
        for predicate, key, obj in literals:
            new_args = []
            for term in predicate.args:
                typ = None
                for param in action_event.params:
                    if type(param.name) == Term and param.name == term:  # TODO:why is the name of a typed term a term

                        typ = param.type
                        break
                self.dependencies['types'][typ].append([action_event, p_e, literal, term])
                self.dependencies['rlu'][action_event].append(['types', typ, p_e, literal, term])
                new_args.append(Term(name=term, type=typ))
            temp_pred = obj(predicate.name, new_args)
            for pred in self.dependencies[key]:
                if not pred.name == temp_pred.name or not len(pred.args) == len(temp_pred.args):
                    continue
                eq = True
                for i in range(len(pred.args)):
                    typ = temp_pred.args[i].type
                    parent_found = False
                    if not typ == pred.args[i].type:
                        while typ in self.types and self.types[typ] != typ:
                            typ = self.types[typ]
                            if typ == pred.args[i].type:
                                parent_found = True
                                break
                        if not parent_found:
                            eq = False
                            continue
                if eq:
                    self.dependencies[key][pred].append([action_event, p_e, literal])
                    self.dependencies['rlu'][action_event].append([key, pred, p_e, literal])

    def new_dependencies(self, action_event):
        self.dependencies['rlu'][action_event] = []
        effects = [eff[1] for effect in action_event.effects for eff in effect]  # grab predicate from probability tuple
        # TODO: if double nested effects removed, update
        for literal in action_event.precond:
            self.new_depen(action_event, literal, 'precond')
        for literal in effects:
            self.new_depen(action_event, literal, 'effects')

    def update_params(self, action_event, init=False, test=False):
        new_params = []
        terms = []
        q = Queue()
        for predicate in action_event.precond + [x[1] for y in action_event.effects for x in y]:
            q.put((predicate, None))
        while not q.empty():
            predicate, typ = q.get()
            if isinstance(predicate, Expression):
                if predicate.value:
                    if isinstance(predicate.value, str) and predicate.value[0] == '?':
                        if not typ:
                            typ = 'int'
                        terms.append(Term(name=Term(name=predicate.value), type=typ))
                else:
                    l_predicate = predicate.left_child
                    l_typ = None
                    r_predicate = predicate.right_child
                    r_typ = None
                    if isinstance(l_predicate, Fluent):
                        l_real_predicate = [x for x in self.domain.fluents if x.name == predicate.left_child.name][0]
                        l_typ = l_real_predicate.type
                        l_predicate.type = l_typ
                    if isinstance(r_predicate, Fluent):
                        r_real_predicate = [x for x in self.domain.fluents if x.name == predicate.right_child.name][0]
                        r_typ = r_real_predicate.type
                        r_predicate.type = r_typ
                    q.put((predicate.right_child, l_typ))
                    q.put((predicate.left_child, r_typ))
            elif isinstance(predicate, Fluent):
                fluent = [x for x in self.domain.fluents if x.name == predicate.name][0]
                for i, arg in enumerate(fluent.args):
                    terms.append(Term(name=Term(name=predicate.args[i].name), type=arg.type))
            elif isinstance(predicate, Literal):
                real_predicate = [x for x in self.domain.predicates if x.name == predicate.predicate.name][0]
                for i, arg in enumerate(real_predicate.args):
                    terms.append(Term(name=Term(name=predicate.predicate.args[i].name), type=arg.type))
        for term in terms:
            found = False
            for param in new_params:
                if term.name.name == param.name.name:
                    if match_types or init:
                        found = True
                    # TODO: let be new, second, third, ect.. instance of type
                    # TODO: don't let any names match in params
                    break
            if not found:
                new_params += [term]  # was copy term
        # action_event.params = new_params  # TODO: If we want to keep empty params, update types in preconds?

    def find_dependencies(self):
        for pred in self.domain.predicates:
            self.dependencies['predicates'][pred] = []
        for fluent in self.domain.fluents:
            self.dependencies['fluents'][fluent] = []
            # initialize predicate dependency for each predicate to empty list
        for typ in self.domain.types:
            parent = None
            if isinstance(self.domain.types[typ], list):
                parent = typ
            if typ not in self.types:
                self.types[typ] = None
            for sub_typ in self.domain.types[typ]:
                self.types[sub_typ] = parent
        self.dependencies['types']['int'] = []
        for typ in self.types:
            self.dependencies['types'][typ] = []
        for action_event in self.domain.events + self.domain.operators:  # TODO: maybe processes?
            # self.update_params(action_event, init=True)
            self.new_dependencies(action_event)

    def __init__(self, domain, t_prob=1):
        self.types = {None: None}
        self.dependencies = {'predicates': {}, 'types': {}, 'fluents': {}, 'rlu': {}}  # rlu -> reverse look up
        # predicate -> (event/action, predicate), types -> (event/action, predicate, term), rlu -> (dictionary, args)
        """self.transformations = {'Transform': {'add_event': self.add_event,
                                              'events': {'remove_event': self.remove_event,
                                                         'event_to_action': self.event_to_action,
                                                         'add_effect': self.add_effect,
                                                         'effects': {'remove_effect': self.remove_effect},
                                                         'add_precondition': self.add_precondition,
                                                         'precond': {'remove_precondition': self.remove_precondition},
                                                         },
                                              'add_type': self.add_type,
                                              'li_types': {'remove_type': self.remove_type,
                                                           },
                                              'add_predicate': self.add_predicate,
                                              'predicates': {'remove_predicate': self.remove_predicate},
                                              'add_action': self.add_action,
                                              'operators': {'remove_action': self.remove_action,
                                                            'action_to_event': self.action_to_event,
                                                            'add_effect': self.add_effect,
                                                            'effects': {'remove_effect': self.remove_effect,
                                                                        'change_effect_probability': self.change_effect_probability,
                                                                        },
                                                            'add_precondition': self.add_precondition,
                                                            'precond': {'remove_precondition': self.remove_precondition}
                                                            }
                                              }
                                }"""

        self.domain = domain
        self.t_prob = t_prob
        self.find_dependencies()
        self.li_types = list(self.types.keys())
        self.arg_average = 2
        self.transforms = []
        self.args = []
        pass

    def transform(self, start='Transform', history=None, var=None, d=None, flag=False):
        if not history:
            history = []
        history = dc(history)
        if not var:
            var = self.domain
        if not d:
            d = self.transformations
        if isinstance(d, types.MethodType):
            if flag:
                d(*history)  # check flag, call function
        else:
            for key in d:
                temp_var = var
                if key == start:
                    flag = True
                if key in dir(var):
                    temp_var = getattr(temp_var, key)
                if isinstance(temp_var, list):
                    if isinstance(temp_var[0], list):
                        temp_var = temp_var[0]
                    # TODO: if double nested effects removed, update
                    for mem in temp_var:
                        self.transform(start=start, history=history + [mem], var=mem, d=d[key], flag=flag)
                    else:
                        self.transform(start=start, history=history, var=var, d=d[key], flag=flag)
                pass  # iterate deeper, check for start, set flag

    def get_num_transformations(self):
        total_transformations = {'total': 0}
        heads = ['add', 'rem', 'cha', 'eve', 'act']
        transformations = [x for x in dir(self) if x[:3] in heads]
        for transformation in transformations:
            r_transformation = getattr(self, transformation)
            r_transformation_name = str(r_transformation).split('.')[1].split(' ')[0]
            possible_args = []
            arg_types = typing.get_type_hints(r_transformation)
            for arg in arg_types:
                options = []
                p = None
                if hasattr(arg_types[arg], '__args__'):
                    arg_length = 0
                    for typ in arg_types[arg].__args__:
                        if not typ == type(None):
                            p = getattr(typ, 'class_name')
                            arg_length += len(getattr(self.domain, p))
                    options.append(arg_length)

                elif issubclass(arg_types[arg], SubVar):
                    for action_event in self.domain.operators + self.domain.events:
                        options.append(len(getattr(action_event, getattr(arg_types[arg], 'class_name'))))

                elif arg_types[arg] == bool:
                    options.append(len([True, False]))
                elif issubclass(arg_types[arg], ArgLength):
                    arg_length = 0
                    for i in range(arg_types[arg].min_args + 1, arg_types[arg].max_args + 1):
                        temp1 = []
                        if 'predicates' in arg_types[arg].types:
                            temp1 = [Literal(x, random.random() > .5) for x in self.domain.predicates]
                        temp2 = []
                        if 'fluents' in arg_types[arg].types:
                            temp2 = [Expression(operator=random.choice(['>', '<', '<=', '>=', '=']), left_child=x,
                                                right_child=round(random.uniform(x.bounds[0], x.bounds[1]),
                                                                  x.bounds[2])) for
                                     x in self.domain.fluents]
                        temp3 = []
                        if 'types' in arg_types[arg].types:
                            temp3 = [x for x in self.li_types]
                        arg_length += len([list(x) for x in itertools.combinations(temp1 + temp2 + temp3, i)])
                    options.append(arg_length)
                else:
                    p = getattr(arg_types[arg], 'class_name')
                    options.append(len(getattr(self.domain, p)))
                possible_args.append(options)
            transformation_total = 1
            prev = None
            for nums in possible_args:
                if len(nums) == 1:
                    transformation_total *= nums[0]
                    prev = nums[0]
                elif len(nums) == prev:
                    transformation_total /= prev
                    transformation_total = int(transformation_total)
                    additions = []
                    for num in nums:
                        additions.append(transformation_total * num)
                    transformation_total = sum(additions)
                else:
                    print("getNumTransformError")
            total_transformations[r_transformation_name] = transformation_total
        total_transformations['total'] = sum(total_transformations.values())
        return total_transformations

    def get_all_transformations(self):
        all_transformations = []
        heads = ['add', 'rem', 'cha', 'eve', 'act']
        transformations = [x for x in dir(self) if x[:3] in heads]
        for transformation in transformations:
            r_transformation = getattr(self, transformation)
            possible_args = []
            arg_types = typing.get_type_hints(r_transformation)
            for arg in arg_types:
                options = []
                p = None
                if hasattr(arg_types[arg], '__args__'):
                    for typ in arg_types[arg].__args__:
                        if typ != types.NoneType:
                            p = getattr(typ, 'class_name')
                            options += getattr(self.domain, p)

                elif issubclass(arg_types[arg], SubVar):
                    options.append(arg_types[arg])
                elif arg_types[arg] == bool:
                    options += [True, False]
                elif issubclass(arg_types[arg], ArgLength):
                    arg_length = 0
                    for i in range(arg_types[arg].min_args + 1, arg_types[arg].max_args + 1):
                        temp = [Literal(x, random.random() > .5) for x in self.domain.predicates]
                        temp2 = [Expression(operator=random.choice(['>', '<', '<=', '>=', '=']), left_child=x,
                                            right_child=round(random.uniform(x.bounds[0], x.bounds[1]), x.bounds[2]))
                                 for x
                                 in
                                 self.domain.fluents]
                        options += [list(x) for x in itertools.combinations(temp + temp2, i)]
                else:
                    p = getattr(arg_types[arg], 'class_name')
                    options += getattr(self.domain, p)
                possible_args.append(options)
            arg_choices = []
            iter_arg_choices = itertools.product(*possible_args)
            counter = 0
            for args in iter_arg_choices:
                counter += 1
                arg_choice = []
                prev = None
                for arg in args:
                    if isinstance(arg, type) and issubclass(arg, SubVar):
                        arg_choice.append(getattr(prev, arg.class_name))
                    else:
                        prev = arg
                        arg_choice.append(arg)
                arg_choices.append(arg_choice)
            for args in arg_choices:
                all_transformations.append((r_transformation, args))
        return all_transformations

    def get_all_transformation_kinds(self):
        heads = ['add', 'rem', 'cha', 'eve', 'act']
        transformations = [x for x in dir(self) if x[:3] in heads]
        return transformations

    def get_random_transformation(self):
        transformation = None
        args = None
        all_transformations = []
        heads = ['add', 'rem', 'cha', 'eve', 'act']
        transformations = [x for x in dir(self) if x[:3] in heads]
        transformation = random.choice(transformations)

        r_transformation = getattr(self, transformation)
        possible_args = []
        arg_types = typing.get_type_hints(r_transformation)
        for arg in arg_types:
            options = []
            p = None
            if hasattr(arg_types[arg], '__args__'):
                for typ in arg_types[arg].__args__:
                    if typ == str:
                        options.append(str)
                    elif typ != type(None):
                        p = getattr(typ, 'class_name')
                        options += getattr(self.domain, p)

            elif issubclass(arg_types[arg], SubVar):
                options.append(arg_types[arg])
            elif arg_types[arg] == bool:
                options += [True, False]
            elif issubclass(arg_types[arg], ArgLength):
                arg_length = 0
                for i in range(arg_types[arg].min_args + 1, arg_types[arg].max_args + 1):
                    temp = [Literal(x, random.random() > .5) for x in self.domain.predicates]
                    temp2 = [Expression(operator=random.choice(['>', '<', '<=', '>=', '=']), left_child=x,
                                        right_child=round(random.uniform(x.bounds[0], x.bounds[1]), x.bounds[2]))
                             for x
                             in
                             self.domain.fluents]
                    options += [list(x) for x in itertools.combinations(temp + temp2, i)]
            else:
                p = getattr(arg_types[arg], 'class_name')
                options += getattr(self.domain, p)
            possible_args.append(options)
        args = []
        for options in possible_args:
            arg = random.choice(options)
            if inspect.isclass(arg):
                if arg == str:
                    pass
                else:
                    n_arg = args[len(args) - 1]
                    for cn in arg.class_name.replace('0', ',0').split(','):
                        if cn.isdigit():
                            cn = int(cn)
                            n_arg = n_arg[cn]
                        else:
                            n_arg = getattr(n_arg, cn)
                    arg = random.choice(n_arg)
            args.append(arg)
        return transformation, args

    def tests(self, domain, save_tests=True):
        if save_tests:
            if not os.path.isdir(root + SAVEDIR):
                os.mkdir(SAVEDIR)
            if not os.path.isdir(root + SAVEDIR + '/' + domain.name):
                os.mkdir(SAVEDIR + '/' + domain.name)
            rt = RTransformations(dc(domain))
            typ = random.choice(rt.li_types)
            self.run_test(rt, save_tests, rt.remove_type, typ)

            rt = RTransformations(dc(domain))
            self.run_test(rt, save_tests, rt.add_type)

            # print("CHANGE TYPE PARENT NOT IMPLEMENTED")  # hard problem, need to discuss options

            rt = RTransformations(dc(domain))
            pred = random.choice(rt.domain.predicates)
            pred = rt.domain.predicates[0]
            self.run_test(rt, save_tests, rt.remove_predicate, pred)

            rt = RTransformations(dc(domain))
            self.run_test(rt, save_tests, rt.add_predicate)

            rt = RTransformations(dc(domain))
            # derivedpred = random.choice(rt.domain.derivedpredicates)
            # self.run_test(rt, save_tests, rt.remove_derived_predicate, derivedpred)

            rt = RTransformations(dc(domain))
            self.run_test(rt, save_tests, rt.add_derived_predicate)

            # print("REMOVE PROCESS NOT IMPLEMENTED")

            # print("ADD PROCESS NOT IMPLEMENTED")  # what is a process exactly

            rt = RTransformations(dc(domain))
            action = random.choice(rt.domain.operators)
            self.run_test(rt, save_tests, rt.remove_action, action)

            rt = RTransformations(dc(domain))
            action = random.choice(rt.domain.operators)
            self.run_test(rt, save_tests, rt.action_to_event, action)

            rt = RTransformations(dc(domain))
            # self.run_test(rt, save_tests, rt.add_action)

            rt = RTransformations(dc(domain))
            event = random.choice(rt.domain.events)
            self.run_test(rt, save_tests, rt.remove_event, event)

            rt = RTransformations(dc(domain))
            event = random.choice(rt.domain.events)
            self.run_test(rt, save_tests, rt.event_to_action, event)

            rt = RTransformations(dc(domain))
            # self.run_test(rt, save_tests, rt.add_event)

            rt = RTransformations(dc(domain))
            action_event = random.choice(rt.domain.operators + rt.domain.events)
            while not action_event.precond:
                action_event = random.choice(rt.domain.operators + rt.domain.events)
            precond = random.choice(action_event.precond)
            self.run_test(rt, save_tests, rt.remove_precondition, action_event, precond)

            rt = RTransformations(dc(domain))
            action_event = random.choice(rt.domain.operators + rt.domain.events)
            # target_action = 'pay'
            # action_event = random.choice([x for x in rt.domain.operators+rt.domain.events if x.name == target_action])
            self.run_test(rt, save_tests, rt.add_precondition, action_event)

            rt = RTransformations(dc(domain))
            action_event = random.choice(rt.domain.operators + rt.domain.events)
            while not (action_event.effects and action_event.effects[0]):
                action_event = random.choice(rt.domain.operators + rt.domain.events)
            effect = random.choice(action_event.effects[0])
            self.run_test(rt, save_tests, rt.remove_effect, action_event, effect)

            rt = RTransformations(dc(domain))
            action_event = random.choice(rt.domain.operators + rt.domain.events)
            while not (action_event.effects and action_event.effects[0]):
                action_event = random.choice(rt.domain.operators + rt.domain.events)
            effect = random.choice(action_event.effects[0])
            self.run_test(rt, save_tests, rt.change_effect_probability, action_event, effect)

            rt = RTransformations(dc(domain))
            action_event = random.choice(rt.domain.operators + rt.domain.events)
            self.run_test(rt, save_tests, rt.add_effect, action_event)

            # print("CHANGE FREQUENCY DISTRIBUTION EVENT NOT IMPLEMENTED")  # what

            rt = RTransformations(dc(domain))
            found = False
            while not found:
                action_event = random.choice(rt.domain.operators + rt.domain.events)
                if action_event.effects:
                    for x in action_event.effects[0]:
                        fluent_effects = action_event.fluent_effects
                        if fluent_effects:
                            found = True
                            break
            effect = random.choice(fluent_effects)
            self.run_test(rt, save_tests, rt.change_fluent_effect_value, action_event, effect)


def rtransform(domain, r_transformation=None, args=[], save_tests=True):
    # tests(domain)
    rt = RTransformations(dc(domain))
    if not r_transformation:
        (r_transformation, args) = rt.get_random_transformation()
        rt.transforms.append(r_transformation)
        rt.args.append(args)
    return rt
