from enum import Enum


class RTransformation(Enum):
    ACTION_TO_EVENT = 1
    ADD_ACTION = 2
    ADD_CONSTANT = 3
    ADD_DERIVED_PREDICATE = 4
    ADD_EFFECT = 5
    ADD_EVENT = 6
    ADD_FLUENT = 7
    ADD_PRECONDITION = 8
    ADD_PREDICATE = 9
    ADD_TYPE = 10
    ADD_TYPE_PARENT = 11
    CHANGE_EFFECT_PROBABILITY = 12
    CHANGE_EVENT_FREQUENCY = 13
    CHANGE_EVENT_PROBABILITY = 14
    CHANGE_FLUENT_EFFECT_VALUE = 15
    EVENT_TO_ACTION = 16
    REMOVE_ACTION = 17
    REMOVE_CONSTANT = 18
    REMOVE_DERIVED_PREDICATE = 19
    REMOVE_EFFECT = 20
    REMOVE_EVENT = 21
    REMOVE_FLUENT = 22
    REMOVE_PRECONDITION = 23
    REMOVE_PREDICATE = 24
    REMOVE_TYPE = 25
    REMOVE_TYPE_PARENT = 26