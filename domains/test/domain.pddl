(define (domain data-network)
(:requirements :adl :typing :negative-preconditions :equality :action-costs)
(:types
    agent
)
(:predicates
    (is-blue ?ag - agent)
    (holds-flag ?ag - agent)
    (all-blue-dead)
)
(:fluents
    (test ?ag - agent) - agent
    (self) - agent
)
(:action take_flag
    :parameters (?ag - agent)
    :precondition
    (and
        (is_blue ?ag)
    )
    :effect
    (and
        (holds_flag ?ag)
    )
)

)