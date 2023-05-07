(define (domain :monopoly)
  (:requirements :typing :numerics :equality)
  (:types token space spacetype title stage player status color offer - int)
  (:constants
  
    PROPERTY - spacetype
    RAILROAD - spacetype
    UTILITY CHANCE CHEST GO JUST_VISITING FREE_PARKING JAIL GO_TO_JAIL TAX - spacetype

    PRE_ROLL - stage ROLL - stage MOVE - stage POST_ROLL - stage 
    VISIT - stage AUCTION - stage TURN_END - stage

    NOTITLE - title

    NOPLAYER - player

    LOST FREE JAILED - status

    NOCOLOR - color
  )
  (:predicates 
       (space-mortgaged ?s - space)
       (extra-turn)
       (just-bought-house ?s - space)
       (just-sold-house ?s - space)
       (just-obtained ?s - space)
       
       (need-maintenance ?house-cost - int ?hotel-cost - int)
       (need-share-wealth ?amount - int)
       (need-collection ?amount - int)
       (need-move ?sp - space)
       
       (nearest-of-type ?p - player ?stype - spacetype ?sp - space)
       (next-of-type-after ?stype - spacetype ?num - int ?sp - space)
       (next-of-type-after-a ?stype - spacetype ?num - int ?sp - space)
       (next-of-type-after-b ?stype - spacetype ?num - int ?sp - space)
       
       (auction-passed ?p - player)
       
       (offer-processing ?o - offer)
       (offer-made ?o - offer)
       (offer-cancelled ?o - offer)
       (offer-still-works ?o - offer)
       (included-properties-still-owned ?o - offer)
       (requested-properties-still-owned ?o - offer)
       (offer-requests-property ?o - offer ?p - space)
       (offer-includes-property ?o - offer ?p - space)
       
       
       (player-space ?p - player ?s - space)
       (same-space-type ?s1 - space ?s2 - space)
       (same-space-num ?s1 - space ?s2 - space)
       (lower-space-num ?s1 - space ?s2 - space)
       (higher-space-num ?s1 - space ?s2 - space)
       (same-owner ?s1 - space ?s2 - space)
       (same-houses ?s1 - space ?s2 - space)
       (more-houses ?s1 - space ?s2 - space)
       (fewer-houses ?s1 - space ?s2 - space)
       (same-hotels ?s1 - space ?s2 - space)
       (same-color ?s1 - space ?s2 - space)
       (lower-rent ?s1 - space ?s2 - space)
       (higher-rent ?s1 - space ?s2 - space)
  )
 
  (:functions 
      (self) - player
      (current-player) - player
      (current-performer) - player
      (turn-stage) - stage
  
      (position-space ?i - int) - space
      (max-position) - int

      (space-type ?s - space) - spacetype
      (space-num ?s - space) - int
      (space-owned ?s - space) - player
      (space-houses ?s - space) - int
      (space-hotels ?s - space) - int
      (space-title ?s - space) - title
      (space-color ?s - space) - color
      (space-rent ?s - space) - int
      
      (player-cash ?p - player) - int
      (player-position ?p - player) - int
      (player-next ?p - player) - player
      (player-status ?p - player) - status
      (player-get-out-of-jail-frees ?p - player) - int
      (player-turns-in-jail ?p - player) - int
      (player-railroads-owned ?p - player) - int
      (player-utilities-owned ?p - player) - int
      
      (title-cost ?t - title) - int
      (title-rent-unimproved ?t - title) - int
      (title-rent-houses ?t - title ?houses - int) - int
      (title-mortgage-value ?t - title) - int
      (title-house-cost ?t - title) - int
      (title-name ?t - title) - string
      
      (monopoly-owned ?c - color) - player
      (monopoly-min-houses ?c - color) - int
      (monopoly-max-houses ?c - color) - int

      (utilities-owned-multiplier ?count - int) - int
      (utility-multiplier) - int
      (railroad-rent ?count - int) - int
      
      (current-offer) - offer
      (offer-requests-cash ?o - offer) - int
      (offer-includes-cash ?o - offer) - int
      (offer-partner ?o - offer) - player
      (offer-offerer ?o - offer) - player

      (die1-value) - int
      (die2-value) - int
      
      (just-visiting-position) - int
      (doubles-rolled-in-row) - int
      
      (available-houses) - int
      (available-hotels) - int
      
      (chance-card) - int
      (chest-card) - int
      
      (auction-last-bid) - int
      (auction-last-bidder) - player
      (auction-current-bidder) - player
  )
  
  ;; PRE_ROLL stage (see also PRE_ROLL/POST_ROLL)
  
  (:action pay_jail_fine
   :parameters ()
      :precondition 
        (and 
            (eq (current-player) ?p)
            (eq (turn-stage) PRE_ROLL)
            (eq (player-status ?p) JAILED)
            (> (player-cash ?p) 50)
        )
   :effect 
        (and 
            (decrease (player-cash ?p) 50)
            (set (player-status ?p) GETTING_OUT)
        )
  )

  (:action use_get_out_of_jail_card
   :parameters ()
      :precondition 
        (and 
            (eq (turn-stage) PRE_ROLL)
            (eq (current-player) ?p)
            (eq (player-status ?p) JAILED)
            (> (player-get-out-of-jail-frees ?p) 0)
        )
   :effect (and (decrease (player-get-out-of-jail-frees ?p) 1)
                (set (player-status ?p) GETTING_OUT))
  )  
  ;; ROLL stage

  (:action roll_die
      :parameters ()
   :precondition (and (eq (current-player) ?p)
                   (eq (turn-stage) PRE_ROLL)
              )
   :effect (and (set (turn-stage) ROLL))
  )

  (:event die-roll
   :parameters ()
   :precondition (eq (turn-stage) ROLL)
   :effect (and ;(randomize (die1-value) (:uniform 1 6))
                ;(randomize (die2-value) (:uniform 1 6))
                (set (die1-value) 3)
                (set (die2-value) 3)
                (set (turn-stage) MOVE))
  )
  
  
  ;; MOVE stage
  
  (:event move
   :parameters ()
   :precondition (and (eq (turn-stage) MOVE) (eq (current-player) ?p)
                   (eq (die1-value) ?die1)
                   (eq (die2-value) ?die2)
                   (eq (max-position) ?max)
                   (eq (player-status ?p) FREE))
   :effect (and (set (player-position ?p) (mod (+ ?die1 (+ ?die2 (player-position ?p))) ?max))
                (set (turn-stage) VISIT))
  )
  
  (:event collect-salary
   :parameters ()
   :precondition 
        (and 
            (eq (turn-stage) MOVE) 
            (eq (current-player) ?p)
            (eq (die1-value) ?die1)
            (eq (die2-value) ?die2)
            (eq (max-position) ?max)
            (eq (player-status ?p) FREE)
            (>= (+ ?die1 (+ ?die2 (player-position ?p))) ?max)
        )
   :effect 
        (and 
            (increase (player-cash ?p) 200)
            (set (turn-stage) VISIT)
        )
  )

  (:event doubles-in-jail
   :parameters ()
   :precondition (and (eq (current-player) ?p)
                   (eq (turn-stage) MOVE)
                   (eq (die1-value) ?d)
                   (eq (die2-value) ?d)
                   (eq (player-status ?p) JAILED))
   :effect (and (set (player-status ?p) GETTING_OUT))
  )
  
  (:event doubles-into-jail
   :parameters ()
   :precondition (and (eq (current-player) ?p)
                   (eq (turn-stage) MOVE)
                   (eq (die1-value) ?d)
                   (eq (die2-value) ?d)
                   (eq (doubles-rolled-in-row) 2)
                   (not (extra-turn))
                   (eq (player-status ?p) FREE))
   :effect (and (set (player-status ?p) CAUGHT)
                (set (doubles-rolled-in-row) 0))
  )
 
  (:event doubles-extra-turn
   :parameters ()
   :precondition (and
                   (eq (turn-stage) MOVE)
                   (eq (die1-value) ?d)
                   (eq (die2-value) ?d)
                   (< (doubles-rolled-in-row) 2)
                   (not (extra-turn)))
   :effect (and (extra-turn)
                (increase (doubles-rolled-in-row) 1))
  )

  ;; VISIT stage - unowned property
  
  (:action purchase
   :parameters (?space - space)
      :precondition 
        (and 
            (eq (turn-stage) VISIT)
            (eq (current-player) ?p)
            (eq (player-position ?p) ?pos) 
            (eq (position-space ?pos) ?space)
            (eq (space-title ?space) ?title)
            (neq (space-title ?space) NOTITLE)
            (eq (space-owned ?space) NOPLAYER)
            (< (title-cost ?title) (player-cash ?p))
            (eq (title-rent-unimproved ?title) ?new-rent)
            (eq (title-cost ?title) ?cost)
        )
   :effect 
        (and 
            (decrease (player-cash ?p) ?cost)
            (set (space-owned ?space) ?p)
            (just-obtained ?space)
            (set (space-rent ?space) ?new-rent)
            (set (turn-stage) POST_ROLL)
        )
  )
  
  (:event monopolizes
   :parameters ()
   :precondition 
        (and 
            (just-obtained ?space)
            (neq (space-color ?space) NOCOLOR)

            (eq (space-color ?space) ?color)
            (eq (space-owned ?space) ?p)
            (eq (space-num ?space) ?n1)

            (eq (space-color ?sp2) ?color)
            (eq (space-owned ?sp2) ?p)
            (neq (space-num ?sp2) ?n1)
            (eq (space-num ?sp2) ?n2)

            (eq (space-color ?sp3) ?color)
            (eq (space-owned ?sp3) ?p)
            (neq (space-num ?sp3) ?n1)
            (neq (space-num ?sp3) ?n2)

            (eq (space-title ?space) ?t1)
            (eq (space-title ?sp2) ?t2)
            (eq (space-title ?sp3) ?t3)

        )
   :effect 
        (and 
            (set (monopoly-owned ?color) ?p)
            (set (space-rent ?space) (* 2 (title-rent-unimproved ?t1)))
            (set (space-rent ?sp2) (* 2 (title-rent-unimproved ?t2)))
            (set (space-rent ?sp3) (* 2 (title-rent-unimproved ?t3)))
        )
  )
   

  (:event update-railroad-rent
   :parameters (?rr - space)
   :precondition 
        (and 
            (just-obtained ?space)
            (eq (space-type ?space) RAILROAD)
            (eq (space-owned ?space) ?owner)
            (eq (player-railroads-owned ?owner) ?roads)
            ;(assign ?new-roads (+ 1 ?roads))
            (eq (railroad-rent ?new-roads) ?rent)

            (eq (space-owned ?rr) ?owner)
            (eq (space-type ?rr) RAILROAD)
        )
   :effect 
        (and 
            (set (space-rent ?rr) ?rent)
            (set (player-railroads-owned ?owner) ?new-roads)
        )
  )

  (:event update-utilities-owned
   :parameters ()
   :precondition 
        (and 
            (just-obtained ?space)
            (eq (space-type ?space) UTILITY)
            (eq (space-owned ?space) ?owner)
        )
   :effect (and (increase (player-utilities-owned ?owner) 1))
  )
  
  (:event update-utility-multiplier-2
   :parameters ()
   :precondition 
        (and 
            (eq (player-utilities-owned ?any-owner) 2)
            ;(eq (utilities-owned-multiplier 2) ?mult)
            (neq (utility-multiplier) ?mult)
        )
   :effect (and (set (utility-multiplier) ?mult))
  )
  
  (:event update-utility-multiplier-1
   :parameters ()
   :precondition 
        (and 
            (eq (player-utilities-owned ?any-owner) 1)
            ;(eq (utilities-owned-multiplier 1) ?mult)
            (neq (utility-multiplier) ?mult)
        )
   :effect (and (set (utility-multiplier) ?mult))
  )
  
  
  (:event rent-set
   :parameters ()
   :precondition (just-obtained ?space)
   :effect (and (not (just-obtained ?space)))
  )
  

  (:action start-auction
   :parameters ()
      :precondition 
        (and 
            (eq (current-player) ?p)
            (eq (turn-stage) VISIT)
            (eq (player-position ?p) ?pos) 
            (eq (position-space ?pos) ?space)
            (neq (space-title ?space) NOTITLE)
            (eq (space-owned ?space) NOPLAYER)
        )
   :effect (and (set (turn-stage) AUCTION)
                (set (auction-current-bidder) ?p)
                (set (auction-last-bidder) NOPLAYER)
                (set (auction-last-bid) 0)
           )
  )
  
   
  
  ;; VISIT stage - owned property

  (:event pay
   :parameters ()
   :precondition (and (eq (current-player) ?p)
                   (eq (turn-stage) VISIT)
                   (eq (player-position ?p) ?pos) 
                   (eq (position-space ?pos) ?space)
                   (eq (space-owned ?space) ?owner)
                   (eq (space-rent ?space) ?cost)
                   (> (space-rent ?space) 0)
              )
   :effect 
        (and 
            (decrease (player-cash ?p) ?cost)
            (increase (player-cash ?owner) ?cost)
            (set (turn-stage) POST_ROLL)
        )
  )
  
  (:event pay-utility
   :parameters ()
   :precondition (and (eq (current-player) ?p)
                   (eq (turn-stage) VISIT)
                   (eq (player-position ?p) ?pos) 
                   (eq (position-space ?pos) ?space)
                   (eq (space-type ?space) UTILITY)
                   (neq (space-owned ?space) NOPLAYER)
                   (eq (space-owned ?space) ?owner)
                   (eq (utility-multiplier) ?mult)
              )
   :effect 
        (and 
            (decrease (player-cash ?p) (* ?mult (+ (die1-value) (die2-value))))
            (increase (player-cash ?owner) (* ?mult (+ (die1-value) (die2-value))))
            (set (turn-stage) POST_ROLL)
        )
  )

  (:event stay-free
   :parameters ()
   :precondition (and (eq (current-player) ?p)
                   (eq (turn-stage) VISIT)
                   (eq (player-position ?p) ?pos) 
                   (eq (position-space ?pos) ?space)
                   (space-mortgaged ?space)
              )
   :effect 
        (and 
            (set (turn-stage) POST_ROLL)
        )
  )

  (:event fail-to-pay
   :parameters ()
   :precondition (and (eq (current-player) ?p)
                   (eq (turn-stage) VISIT)
                   (eq (player-position ?p) ?pos) 
                   (eq (position-space ?pos) ?space)
                   (neq (space-title ?space) NOTITLE)
                   (neq (space-owned ?space) NOPLAYER)
                   (eq (space-owned ?space) ?owner)
                   (eq (space-rent ?space) ?cost)
                   (< (player-cash ?p) ?cost)
                   (eq (player-cash ?p) ?cash)
              )
   :effect 
        (and 
            (set (player-cash ?p) 0)
            (increase (player-cash ?owner) ?cash)
            (set (player-status ?p) LOST)
            (set (turn-stage) TURN_END)
        )
  )
  
  ;; VISIT stage - chance
  (:event visit-chance
   :parameters ()
   :precondition 
        (and 
            (eq (current-player) ?p)
            (eq (turn-stage) VISIT)
            (eq (player-position ?p) ?pos) 
            (eq (position-space ?pos) ?space)
            (eq (space-type ?space) CHANCE)
            ;(assign ?chance-card (:uniform 1 17))
        )
   :effect 
        (and 
            (set (chance-card) ?chance-card)
            (set (turn-stage) POST_ROLL)
        )
  )
  
  (:event chance-finished
   :parameters ()
   :precondition 
        (and 
            (neq (chance-card) -1)
        )
   :effect 
        (and 
            (set (chance-card) -1)
        )
  )

  (:event chance-go-to-jail
   :parameters ()
   :precondition 
        (and 
            (eq (chance-card) 1)
            (eq (current-player) ?p)
        )
   :effect 
        (and 
            (set (player-status ?p) CAUGHT)
        )
  )

  (:event chance-get-out-of-jail-free
   :parameters ()
   :precondition 
        (and 
            (eq (chance-card) 2)
            (eq (current-player) ?p)
        )
   :effect 
        (and 
            (increase (player-get-out-of-jail-frees ?p) 1)
        )
  )


  (:event chance-go-to-illinois-avenue
   :parameters ()
   :precondition 
        (and 
            (eq (chance-card) 3)
            (eq (title-name ?t) Illinois_Avenue)
            (eq (space-title ?sp) ?t)
        )
   :effect 
        (and 
            (need-move ?sp)
        )
  )


  (:event chance-go-to-st-charles
   :parameters ()
   :precondition 
        (and 
            (eq (chance-card) 4)
            (eq (title-name ?t) St_Charles_Place)
            (eq (space-title ?sp) ?t)
        )
   :effect 
        (and 
            (need-move ?sp)
        )
  )

  (:event chance-go-to-nearest-utility-pay-10-mult
   :parameters ()
   :precondition 
        (and 
            (eq (chance-card) 5)
            (eq (current-player) ?p)
            (nearest-of-type ?p UTILITY ?sp)
        )
   :effect 
        (and 
            (need-move ?sp)
            (set (utility-multiplier) 10)
            (set (turn-stage) VISIT)
        )
  )
  
  (:event chance-go-to-nearest-railroad-pay-double
   :parameters ()
   :precondition 
        (and 
            ;(or (eq (chance-card) 6) (eq (chance-card) 7))
            (eq (current-player) ?p)
            (nearest-of-type ?p RAILROAD ?sp)
            (eq (space-rent ?sp) ?rent)
            (eq (space-owned ?sp) ?owner)
        )
   :effect 
        (and 
            (decrease (player-cash ?p) ?rent)
            (increase (player-cash ?owner) ?rent)
            (need-move ?sp)
            (set (turn-stage) VISIT)
        )
  )
  
  ;(;:event chance-general-repairs
  ; :parameters ()
  ; :precondition
  ;      (and
  ;          (eq (chance-card) 8)
  ;      )
  ; :effect
  ;      (and
  ;          (need-maintenance 25 100)
  ;      )
  ;)

  (:event chance-back-3-spaces
   :parameters ()
   :precondition 
        (and 
            (eq (chance-card) 9)
            (eq (current-player) ?p)
        )
   :effect 
        (and 
            (decrease (player-position ?p) 3)
            (set (turn-stage) VISIT)
        )
  )

  (:event chance-go-to-reading-railroad
   :parameters ()
   :precondition 
        (and 
            (eq (chance-card) 10)
            (eq (title-name ?t) Reading_Railroad)
            (eq (space-title ?sp) ?t)
        )
   :effect 
        (and 
            (need-move ?sp)
        )
  )

  (:event chance-go-to-boardwalk
   :parameters ()
   :precondition 
        (and 
            (eq (chance-card) 11)
            (eq (title-name ?t) Boardwalk)
            (eq (space-title ?sp) ?t)
        )
   :effect 
        (and 
            (need-move ?sp)
        )
  )

  (:event chance-pay-poor-tax
   :parameters ()
   :precondition 
        (and 
            (eq (chance-card) 12)
            (eq (current-player) ?p)
        )
   :effect 
        (and 
            (decrease (player-cash ?p) 15)
        )
  )

  (:event chance-building-loan-matures
   :parameters ()
   :precondition 
        (and 
            (eq (chance-card) 13)
            (eq (current-player) ?p)
        )
   :effect 
        (and 
            (increase (player-cash ?p) 150)
        )
  )

  (:event chance-win-crossword-competition
   :parameters ()
   :precondition 
        (and 
            (eq (chance-card) 14)
            (eq (current-player) ?p)
        )
   :effect 
        (and 
            (increase (player-cash ?p) 100)
        )
  )

  (:event chance-bank-dividend
   :parameters ()
   :precondition 
        (and 
            (eq (chance-card) 15)
            (eq (current-player) ?p)
        )
   :effect 
        (and 
            (increase (player-cash ?p) 50)
        )
  )
  
  ;(;:event chance-elected-board-chairman
  ; :parameters ()
  ; :precondition
  ;      (and
  ;          (eq (chance-card) 16)
  ;      )
  ; :effect
  ;      (and
  ;          (need-share-wealth 50)
  ;      )
  ;)

  (:event chance-advance-to-go
   :parameters ()
   :precondition 
        (and 
            (eq (chance-card) 17)
            (eq (space-num ?sp) 0)
        )
   :effect 
        (and 
            (need-move ?sp)
        )
  )

  (:event maintain-property-without-hotel
   :parameters (?sp - space)
   :precondition 
        (and 
            (need-maintenance ?house-cost ?hotel-cost)
            (eq (space-owned ?sp) ?p)
            (eq (current-player) ?p)
            (eq (space-houses ?sp) ?n)
            (< (space-houses ?sp) 5)
        )
   :effect 
        (and 
            (decrease (player-cash ?p) (* ?n ?house-cost))
            (not (need-maintenance ?house-cost ?hotel-cost))
        )
  )

  (:event maintain-property-with-hotel
   :parameters (?sp - space)
   :precondition 
        (and 
            (need-maintenance ?house-cost ?hotel-cost)
            (eq (space-owned ?sp) ?p)
            (eq (current-player) ?p)
            (eq (space-houses ?sp) 5)
        )
   :effect 
        (and 
            (decrease (player-cash ?p) ?hotel-cost)
            (not (need-maintenance ?house-cost ?hotel-cost))
        )
  )

  (:event bribe-for-election
   :parameters (?o - player)
   :precondition 
        (and 
            (need-share-wealth ?amount)
            (eq (current-player) ?p)
            (eq (player-cash ?o) ?any)
            (neq (current-player) ?o)
            (neq (player-status ?o) lost)
        )
   :effect 
        (and 
            (decrease (player-cash ?p) ?amount)
            (increase (player-cash ?o) ?amount)
            (not (need-share-wealth ?amount))
        )
  )

  (:event do-free-trip-move
   :parameters ()
   :precondition 
        (and 
            (eq (current-player) ?p)
            (need-move ?sp)
            (eq (space-num ?sp) ?pos)
        )
   :effect 
        (and 
            (set (player-position ?p) ?pos)
            (not (need-move ?sp))
        )
  )

  (:event do-free-trip-salary
   :parameters ()
   :precondition 
        (and 
            (eq (current-player) ?p)
            (need-move ?sp)
            (eq (player-position ?p) ?pos)
            (< (space-num ?sp) ?pos)
        )
   :effect 
        (and 
            (increase (player-cash ?p) 200)
        )
  )

  ;; VISIT stage - community chest
  (:event visit-community-chest
   :parameters ()
   :precondition 
        (and 
            (eq (current-player) ?p)
            (eq (turn-stage) VISIT)
            (eq (player-position ?p) ?pos) 
            (eq (position-space ?pos) ?space)
            (eq (space-type ?space) CHEST)
            ;(assign ?chest-card (:uniform 1 17))
        )
   :effect 
        (and 
            (set (chest-card) ?chest-card)
            (set (turn-stage) POST_ROLL)
        )
  )
  
  ;(;:event chest-finished
   ;:parameters ()
   ;:precondition
   ;     (and
   ;         (neq (chest-card) -1)
   ;     )
   ;:effect
   ;     (and
   ;         (set (chest-card) -1)
   ;     )
  ;)

  (:event chest-go-to-jail
   :parameters ()
   :precondition 
        (and 
            (eq (chest-card) 1)
            (eq (current-player) ?p)
        )
   :effect 
        (and 
            (set (player-status ?p) CAUGHT)
        )
  )

  (:event chest-get-out-of-jail-free
   :parameters ()
   :precondition 
        (and 
            (eq (chest-card) 2)
            (eq (current-player) ?p)
        )
   :effect 
        (and 
            (increase (player-get-out-of-jail-frees ?p) 1)
        )
  )

  (:event chest-sale-of-stock
   :parameters ()
   :precondition 
        (and 
            (eq (chest-card) 3)
            (eq (current-player) ?p)
        )
   :effect 
        (and 
            (increase (player-cash ?p) 45)
        )
  )

  (:event chest-bank-error
   :parameters ()
   :precondition 
        (and 
            (eq (chest-card) 4)
            (eq (current-player) ?p)
        )
   :effect 
        (and 
            (increase (player-cash ?p) 200)
        )
  )

  (:event chest-doctor-fee
   :parameters ()
   :precondition 
        (and 
            (eq (chest-card) 5)
            (eq (current-player) ?p)
        )
   :effect 
        (and 
            (decrease (player-cash ?p) 50)
        )
  )

  (:event chest-holiday-fund-matures
   :parameters ()
   :precondition 
        (and 
            (eq (chest-card) 6)
            (eq (current-player) ?p)
        )
   :effect 
        (and 
            (increase (player-cash ?p) 100)
        )
  )

  (:event chest-income-tax-refund
   :parameters ()
   :precondition 
        (and 
            (eq (chest-card) 7)
            (eq (current-player) ?p)
        )
   :effect 
        (and 
            (increase (player-cash ?p) 20)
        )
  )

  (:event chest-life-insurance-matures
   :parameters ()
   :precondition 
        (and 
            (eq (chest-card) 8)
            (eq (current-player) ?p)
        )
   :effect 
        (and 
            (increase (player-cash ?p) 100)
        )
  )

  (:event chest-hospital-fee
   :parameters ()
   :precondition 
        (and 
            (eq (chest-card) 9)
            (eq (current-player) ?p)
        )
   :effect 
        (and 
            (decrease (player-cash ?p) 100)
        )
  )

  (:event chest-school-fee
   :parameters ()
   :precondition 
        (and 
            (eq (chest-card) 10)
            (eq (current-player) ?p)
        )
   :effect 
        (and 
            (decrease (player-cash ?p) 150)
        )
  )

  (:event chest-consultancy-fee
   :parameters ()
   :precondition 
        (and 
            (eq (chest-card) 11)
            (eq (current-player) ?p)
        )
   :effect 
        (and 
            (increase (player-cash ?p) 25)
        )
  )

  (:event chest-beauty-contest
   :parameters ()
   :precondition 
        (and 
            (eq (chest-card) 12)
            (eq (current-player) ?p)
        )
   :effect 
        (and 
            (increase (player-cash ?p) 10)
        )
  )

  (:event chest-inherit-money
   :parameters ()
   :precondition 
        (and 
            (eq (chest-card) 13)
            (eq (current-player) ?p)
        )
   :effect 
        (and 
            (increase (player-cash ?p) 100)
        )
  )

  ;(;:event chest-opera-night
  ; :parameters ()
  ; :precondition
  ;      (and
  ;          (eq (chest-card) 13)
  ;      )
  ; :effect
  ;      (and
  ;          (need-collection 50)
  ;      )
  ;)

  (:event chest-advance-to-go
   :parameters ()
   :precondition 
        (and 
            (eq (chest-card) 14)
            (eq (space-num ?sp) 0)
        )
   :effect 
        (and 
            (need-move ?sp)
        )
  )

  ;(;:event chest-street-repairs
  ; :parameters ()
  ; :precondition
  ;      (and
  ;          (eq (chest-card) 15)
  ;      )
  ; :effect
  ;      (and
  ;          (need-maintenance 40 115)
  ;      )
  ;)

  ;(;:event chest-birthday
  ; :parameters ()
  ; :precondition
  ;      (and
  ;          (eq (chest-card) 16)
  ;      )
  ; :effect
  ;      (and
  ;          (need-collection 10)
  ;      )
  ;)

  (:event collect-money
   :parameters (?o - player)
   :precondition 
        (and 
            (need-collection ?amount)
            (eq (current-player) ?p)
            (eq (player-cash ?o) ?any)
            (neq (current-player) ?o)
            (neq (player-status ?o) lost)
        )
   :effect 
        (and 
            (decrease (player-cash ?o) ?amount)
            (increase (player-cash ?p) ?amount)
            (not (need-collection ?amount))
        )
  )
  
  
  ;; VISIT stage - go to jail

  (:event visit-go-to-jail
   :parameters ()
   :precondition 
        (and 
            (eq (current-player) ?p)
            (eq (turn-stage) VISIT)
            (eq (player-position ?p) ?pos) 
            (eq (position-space ?pos) ?space)
            (eq (space-type ?space) GO_TO_JAIL)
        )
   :effect 
        (and 
            (set (player-status ?p) CAUGHT)
            (set (turn-stage) POST_ROLL)
        )
  )


  ;; VISIT stage - everything else

  (:event visit-boring
   :parameters ()
   :precondition 
        (and 
            (eq (turn-stage) VISIT)
            (eq (current-player) ?p)
            (eq (player-position ?p) ?pos) 
            (eq (position-space ?pos) ?space)
            ;(or (eq (space-type ?space) GO)
            ;    (eq (space-type ?space) FREE_PARKING)
            ;    (eq (space-type ?space) JUST_VISITING)
            ;)
        )
   :effect 
        (and 
            (set (turn-stage) POST_ROLL)
        )
  )

  ;; AUCTION stage
  
  (:action bid-in-auction
   :parameters (?amount - int)
      :precondition 
        (and 
            (eq (turn-stage) AUCTION)
            (eq (auction-current-bidder) ?p)
            (> (player-cash ?p) ?amount)
            (< (auction-last-bid) ?amount)
        )
   :effect (and (set (auction-last-bid) ?amount)
                (set (auction-last-bidder) ?p))
  )
  
  (:action pass-bid
   :parameters ()
      :precondition 
        (and 
            (eq (turn-stage) AUCTION)
            (eq (auction-current-bidder) ?p)
            (neq (auction-last-bidder) ?p)
            (eq (player-next ?p) ?next-p)
        )
   :effect 
        (and 
            (auction-passed ?p) 
            (set (auction-current-bidder) ?next-p)
            (set (current-performer) ?next-p)
        )
  )
  
  (:event goto-next-bidder
   :parameters ()
   :precondition 
        (and 
            (eq (turn-stage) AUCTION)
            (eq (auction-current-bidder) ?p)
            (auction-passed ?p)
            (eq (player-status ?p) LOST)
            (eq (player-next ?p) ?next-p)
        )
   :effect 
        (and 
            (set (auction-current-bidder) ?next-p)
            (set (current-performer) ?next-p)
        )
  )
   
  (:event end-auction-win
   :parameters ()
   :precondition 
        (and 
            (eq (turn-stage) AUCTION)
            (eq (auction-current-bidder) ?p)
            (eq (auction-last-bidder) ?p)
            (not (auction-passed ?p))
            (> (auction-last-bid) 0)
            (eq (auction-last-bid) ?amount)
            (eq (current-player) ?cur-p)
            (player-space ?cur-p ?space)
            (eq (space-title ?space) ?title)
            (eq (title-rent-unimproved ?title) ?new-rent)
            (eq (current-player) ?next)
        )
   :effect 
        (and 
            (decrease (player-cash ?p) ?amount)
            (set (space-owned ?space) ?p)
            (just-obtained ?space)
            (set (space-rent ?space) ?new-rent)
            (set (turn-stage) POST_ROLL)
            (set (current-performer) ?next)
        )
  )
  
  (:event end-auction-no-bid
   :parameters ()
   :precondition 
        (and 
            (eq (turn-stage) AUCTION)
            (eq (current-player) ?p)
            (eq (auction-current-bidder) ?p)
            (eq (auction-last-bidder) NOPLAYER)
            (auction-passed ?p)
        )
   :effect 
        (and 
            (set (current-performer) ?p)
            (set (turn-stage) POST_ROLL)
        )
  )
  
  (:event reset-bid-pass-bid
   :parameters (?p - player)
   :precondition 
        (and 
            (eq (turn-stage) POST_ROLL)
            (auction-passed ?p)
        )
   :effect 
        (and 
            (not (auction-passed ?p))
        )
  )

  ;; PRE_ROLL/POST_ROLL stage

  (:action mortgage_property
   :parameters (?sp - space)
      :precondition 
        (and
           ;(or (eq (turn-stage) PRE_ROLL) (eq (turn-stage) POST_ROLL))
           (eq (space-owned ?sp) ?p)
           (not (space-mortgaged ?sp))
           (eq (space-title ?sp) ?title)
           (eq (space-color ?sp) ?color)
           (eq (title-mortgage-value ?title) ?cash)
           (eq (monopoly-max-houses ?color) 0)
        )
   :effect 
        (and 
            (space-mortgaged ?sp)
            (set (space-rent ?sp) 0)
            (increase (player-cash ?p) ?cash)
        )
  )

  (:action free_mortgage
   :parameters (?sp - space)
      :precondition 
        (and
           ;(or (eq (turn-stage) PRE_ROLL) (eq (turn-stage) POST_ROLL))
           (space-mortgaged ?sp)
           (eq (space-owned ?sp) ?p)
           (eq (space-title ?sp) ?title)
           (eq (title-mortgage-value ?title) ?cash)
           (>= (player-cash ?p) (* 1.1 ?cash))
        )
   :effect 
        (and 
            (decrease (player-cash ?p) (* 1.1 ?cash))
            (not (space-mortgaged ?sp))
            (just-obtained ?sp)
        )
  )

  (:action buy_house
   :parameters (?sp - space)
      :precondition 
        (and
            ;(or (eq (turn-stage) PRE_ROLL) (eq (turn-stage) POST_ROLL))
            (eq (space-color ?sp) ?color)
            (eq (monopoly-owned ?color) ?p)
            (eq (monopoly-min-houses ?color) ?min)
            (> (available-houses) 0)
            (eq (space-houses ?sp) ?min)
            (eq (space-title ?sp) ?t)
            (eq (title-house-cost ?t) ?cost)
            (>= (player-cash ?p) ?cost)
        )
   :effect 
        (and 
            (decrease (player-cash ?p) ?cost)
            (set (space-houses ?sp) (+ ?min 1))
            (decrease (available-houses) 1)
            (just-bought-house ?sp)
        )
  )
  
  (:action buy_hotel
   :parameters (?sp - space)
      :precondition 
        (and
            ;(or (eq (turn-stage) PRE_ROLL) (eq (turn-stage) POST_ROLL))
            (eq (space-color ?sp) ?color)
            (eq (monopoly-owned ?color) ?p)
            (>= (monopoly-min-houses ?color) 4)
            (> (available-hotels) 1)
            (eq (space-houses ?sp) 4)
            (eq (space-title ?sp) ?t)
            (eq (title-house-cost ?t) ?cost)
            (>= (player-cash ?p) ?cost)
        )
   :effect 
        (and 
            (decrease (player-cash ?p) ?cost)
            (set (space-houses ?sp) 5)
            (increase (available-houses) 4)
            (just-bought-house ?sp)
        )
  )
  
  (:event buy-done
   :parameters ()
   :precondition (and (just-bought-house ?sp))
   :effect (and (not (just-bought-house ?sp)))
  )

  (:event update-max-houses-buy
   :parameters ()
   :precondition 
        (and 
            (just-bought-house ?sp1)
            (neq (space-color ?sp1) NOCOLOR)
            (eq (monopoly-max-houses ?color) ?max)
            (> (space-houses ?sp1) ?max)
            (eq (space-houses ?sp1) ?new-max)
        )
   :effect 
        (and (set (monopoly-max-houses ?color) ?new-max))
  )


  (:event update-min-houses
   :parameters ()
   :precondition 
        (and 
            (just-bought-house ?sp1)
            (neq (space-color ?sp1) NOCOLOR)
            (eq (space-houses ?sp1) ?max)

            (eq (space-color ?sp1) ?color)
            (eq (space-num ?sp1) ?n1)

            (eq (space-color ?sp2) ?color)
            (eq (space-houses ?sp2) ?max)
            (neq (space-num ?sp2) ?n1)
            (eq (space-num ?sp2) ?n2)

            (eq (space-color ?sp3) ?color)
            (eq (space-houses ?sp3) ?max)
            (neq (space-num ?sp3) ?n1)
            (neq (space-num ?sp3) ?n2)
        )
   :effect (and (set (monopoly-min-houses ?color) ?max))
  )

  (:action sell_house
   :parameters (?sp - space)
      :precondition 
        (and
            ;(or (eq (turn-stage) PRE_ROLL) (eq (turn-stage) POST_ROLL))
            (eq (space-owned ?sp) ?p)
            (> (space-houses ?sp) 0)
            (eq (space-color ?sp) ?color)
            (eq (monopoly-max-houses ?color) ?max)
            (eq (space-houses ?sp) ?max)
            (eq (space-title ?sp) ?t)
            (eq (title-house-cost ?t) ?cost)
        )
   :effect 
        (and 
            (increase (player-cash ?p) (/ ?cost 2))
            (set (space-houses ?sp) (- ?max 1))
            (increase (available-houses) 1)
            (just-sold-house ?sp)
        )
  )

  (:action sell_hotel
   :parameters (?sp - space)
      :precondition 
        (and 
            ;(or (eq (turn-stage) PRE_ROLL) (eq (turn-stage) POST_ROLL))
            (eq (space-owned ?sp) ?p)
            (eq (space-houses ?sp) 5)
            (eq (space-title ?sp) ?t)
            (eq (title-house-cost ?t) ?cost)
            (>= (available-houses) 4)
        )
   :effect (and (increase (player-cash ?p) (/ ?cost 2))
                (set (space-houses ?sp) 4)
                (decrease (available-houses) 4)
           )
  )
  
  (:event update-non-monopoly-rent
   :parameters (?sp - space)
   :precondition 
        (and 
            (just-obtained ?sp)
            (eq (space-owned ?sp) ?p)
            (eq (space-color ?sp) ?color)
            (neq (monopoly-owned ?color) ?p)
            (eq (space-title ?sp) ?t)
            (eq (space-type ?sp) PROPERTY)
            (eq (title-rent-unimproved ?t) ?new-rent)
        )
   :effect 
        (and 
            (set (space-rent ?sp) ?new-rent)
        )
  )

  (:event update-monopoly-rent-no-house
   :parameters (?sp - space)
   :precondition 
        (and 
            ;(or (just-obtained ?sp) (just-sold-house ?sp))
            (eq (space-color ?sp) ?color)
            (neq (monopoly-owned ?color) NOPLAYER)
            (eq (space-title ?sp) ?t)
            (eq (title-rent-unimproved ?t) ?new-rent)
            (eq (space-houses ?sp) 0)
        )
   :effect 
        (and 
            (set (space-rent ?sp) (* 2 ?new-rent))
        )
  )

  (:event update-monopoly-rent-with-house
   :parameters (?sp - space)
   :precondition 
        (and 
            ;(or (just-bought-house ?sp) (just-sold-house ?sp))
            (eq (space-color ?sp) ?color)
            (neq (monopoly-owned ?color) NOPLAYER)
            (eq (space-title ?sp) ?t)
            (eq (space-houses ?sp) ?houses)
            (> (space-houses ?sp) 0)
            (eq (title-rent-houses ?t ?houses) ?new-rent)
        )
   :effect 
        (and 
            (set (space-rent ?sp) ?new-rent)
        )
  )

  (:action sell_all_color_houses
   :parameters (?color - color)
      :precondition 
        (and 
            ;(or (eq (turn-stage) PRE_ROLL) (eq (turn-stage) POST_ROLL))
            (eq (monopoly-owned ?color) ?p)

            (eq (space-color ?sp1) ?color)
            (eq (space-num ?sp1) ?n1)

            (eq (space-color ?sp2) ?color)
            (neq (space-num ?sp2) ?n1)
            (eq (space-num ?sp2) ?n2)

            (eq (space-color ?sp3) ?color)
            (neq (space-num ?sp3) ?n1)
            (neq (space-num ?sp3) ?n2)

            (eq (space-title ?sp1) ?t)
            (eq (space-houses ?sp1) ?count1)
            (eq (space-houses ?sp2) ?count2)
            (eq (space-houses ?sp3) ?count3)
            (eq (title-house-cost ?t) ?cost)
        )
   :effect 
        (and 
            (increase (player-cash ?p) (/ (* ?cost (+ ?count1 (+ ?count2 ?count3))) 2))
            (set (space-houses ?sp1) 0)
            (set (space-houses ?sp2) 0)
            (set (space-houses ?sp3) 0)
            (increase (available-houses) (+ ?count1 (+ ?count2 ?count3)))
            (just-sold-house ?sp1)
            (just-sold-house ?sp2)
            (just-sold-house ?sp3)
        )
  )

  (:event sold-done
   :parameters ()
   :precondition (and (just-sold-house ?sp))
   :effect (and (not (just-sold-house ?sp)))
  )

  (:event update-min-houses-sell
   :parameters ()
   :precondition (and (just-sold-house ?sp1)
                      (neq (space-color ?sp1) NOCOLOR)
                      (eq (monopoly-min-houses ?color) ?min)
                      (< (space-houses ?sp1) ?min)
                      (eq (space-houses ?sp1) ?new-min)
                 )
   :effect (and (set (monopoly-min-houses ?color) ?new-min)
           )
  )

  (:event update-max-houses-sell
   :parameters ()
   :precondition (and (just-sold-house ?sp1)
                      (neq (space-color ?sp1) NOCOLOR)
                      (eq (space-houses ?sp1) ?min)

                      (eq (space-color ?sp1) ?color)
                      (eq (space-num ?sp1) ?n1)

                      (eq (space-color ?sp2) ?color)
                      (eq (space-houses ?sp2) ?min)
                      (neq (space-num ?sp2) ?n1)
                      (eq (space-num ?sp2) ?n2)
                      
                      (eq (space-color ?sp3) ?color)
                      (eq (space-houses ?sp3) ?min)
                      (neq (space-num ?sp3) ?n1)
                      (neq (space-num ?sp3) ?n2)
                 )
   :effect (and (set (monopoly-max-houses ?color) ?min)
           )
  )


  (:action start_offer
   :parameters (?to_player - player)
      :precondition (eq (current-offer) ?offer)
   :effect 
        (and 
            (increase (current-offer) 1)
            (set (offer-offerer ?offer) ?p)
            (set (offer-partner ?offer) ?to_player)
        )
  )

  (:action add_property_include
   :parameters (?space - space)
      :precondition 
        (and 
            (eq (current-offer) ?offer)
            (eq (offer-offerer ?offer) ?p)
            (eq (space-owned ?space) ?p)
            (not (space-mortgaged ?space))
            (eq (space-color ?space) ?color)
            (eq (monopoly-max-houses ?color) 0)
            (not (offer-includes-property ?offer ?space))
        )
   :effect (and (offer-includes-property ?offer ?space))
  )


  (:action add_cash_include
   :parameters (?cash - int)
      :precondition 
        (and 
            (eq (current-offer) ?offer)
            (eq (offer-offerer ?offer) ?p)
            (eq (offer-includes-cash ?offer) 0)
            (eq (offer-requests-cash ?offer) 0)
        )
   :effect (and (set (offer-includes-cash ?offer) ?cash))
  )

  (:action add_property_request
   :parameters (?space - Space)
      :precondition 
        (and 
            (eq (current-offer) ?offer)
            (eq (offer-offerer ?offer) ?p)
            (eq (space-owned ?space) ?partner)
            (eq (offer-partner ?offer) ?partner)
            (not (offer-requests-property ?offer ?space))
        )
   :effect (and (offer-requests-property ?offer ?space))
  )

  (:action add_cash_request
   :parameters (?cash - int)
      :precondition 
        (and 
            (eq (current-offer) ?offer)
            (eq (offer-offerer ?offer) ?p)
            (eq (offer-requests-cash ?offer) 0)
            (eq (offer-includes-cash ?offer) 0)
        )
   :effect (and (set (offer-requests-cash ?offer) ?cash))
  )

  (:action make_trade_offer
   :parameters ()
      :precondition 
        (and 
            (eq (current-offer) ?offer)
            (eq (offer-offerer ?offer) ?p)
            (not (offer-made ?offer))
            (not (offer-cancelled ?offer))
        )
   :effect (and (offer-made ?offer))
  )

  (:action accept_trade_offer
   :parameters (?offer - offer)
      :precondition 
        (and 
            (eq (offer-partner ?offer) ?p)
            (not (offer-cancelled ?offer))
            (offer-still-works ?offer)
        )
   :effect (and (offer-processing ?offer))
  )

  (:event transfer_included_cash
   :parameters (?offer - offer)
   :precondition 
        (and 
            (offer-processing ?offer)
            (eq (offer-includes-cash ?offer) ?cash)
            (eq (offer-offerer ?offer) ?p1)
            (eq (offer-partner ?offer) ?p2)
        )
   :effect 
        (and 
            (decrease (player-cash ?p1) ?cash)
            (increase (player-cash ?p2) ?cash)
        )
  )

  (:event transfer_requested_cash
   :parameters (?offer - offer)
   :precondition 
        (and 
            (offer-processing ?offer)
            (eq (offer-requests-cash ?offer) ?cash)
            (eq (offer-offerer ?offer) ?p1)
            (eq (offer-partner ?offer) ?p2)
        )
   :effect 
        (and 
            (decrease (player-cash ?p2) ?cash)
            (increase (player-cash ?p1) ?cash)
        )
  )

  (:event transfer_included_property
   :parameters (?offer - offer)
   :precondition 
        (and 
            (offer-processing ?offer)
            (offer-includes-property ?offer ?space)
            (eq (offer-partner ?offer) ?p2)
        )
   :effect 
        (and 
            (set (space-owned ?space) ?p2)
        )
  )

  (:event transfer_requested_property
   :parameters (?offer - offer)
   :precondition 
        (and 
            (offer-processing ?offer)
            (offer-requests-property ?offer ?space)
            (eq (offer-offerer ?offer) ?p1)
        )
   :effect 
        (and 
            (set (space-owned ?space) ?p1)
        )
  )

  (:event offer_finishes
   :parameters (?offer - offer)
   :precondition 
        (and 
            (offer-processing ?offer)
        )
   :effect 
        (and 
            (not (offer-processing ?offer))
            (offer-cancelled ?offer)
        )
  )
  
  ;; TURN_END stage
  (:action concluded_actions
   :parameters ()
      :precondition 
        (and 
            (eq (current-player) ?p)
            (eq (turn-stage) POST_ROLL)
        )
   :effect 
        (and (set (turn-stage) TURN_END))
  )
  
  (:event offer-expires
   :parameters (?offer - offer)
   :precondition
        (and
            (offer-made ?offer)
            (not (offer-cancelled ?offer))
        )
   :effect
        (and 
            (offer-cancelled ?offer)
        )
   )
  
  (:event progress-turn
   :parameters ()
   :precondition 
        (and 
            (eq (turn-stage) TURN_END)
            (eq (current-player) ?p)
            (eq (player-next ?p) ?next)
            (not (extra-turn))
        )   
   :effect 
        (and 
            (set (turn-stage) PRE_ROLL)
            (set (current-player) ?next)
            (set (current-performer) ?next)
            (set (doubles-rolled-in-row) 0)
        )
   )
  
  (:event start-extra-turn
   :parameters ()
   :precondition 
        (and 
            (eq (turn-stage) TURN_END)
            (extra-turn)
        )
   :effect (and (set (turn-stage) PRE_ROLL)
                (not (extra-turn))
           )
   )

  ;; General skip eliminated player events
  (:event move-on
   :parameters ()
   :precondition 
        (and 
            (eq (current-player) ?p)
            (eq (player-status ?p) LOST)
            (eq (player-next ?p) ?next)
        )
   :effect 
        (and 
            (set (turn-stage) PRE_ROLL)
            (set (current-player) ?next)
            (set (current-performer) ?next)
        )
  )
  
  ;; General Jail events
  
  (:event enters-jail
   :parameters ()
   :precondition 
        (and (eq (player-status ?p) CAUGHT))
   :effect 
        (and 
            (set (player-status ?p) JAILED)
            (set (player-position ?p) -1)
            (set (player-turns-in-jail ?p) 0)
            (set (turn-stage) TURN_END)
        )
  )

  (:event leave-jail
   :parameters ()
   :precondition 
        (and 
            (eq (current-player) ?p)
            (eq (player-status ?p) GETTING_OUT)
            (eq (just-visiting-position) ?new-spot)
        )
   :effect 
        (and 
            (set (player-status ?p) FREE)
            (set (player-position ?p) ?new-spot)
        )
  )
  
  
  ;; GNOME action, use uncertain


  (:action skip_turn
   :parameters ()
      :precondition 
        (and  
            (eq (current-player) ?p) 
            (eq (player-status ?p) jailed) 
            (< (player-turns-in-jail ?p) 3) 
            (eq (player-next ?p) ?next)
        )
   :effect 
        (and 
            (increase (player-turns-in-jail ?p) 1) 
            (set (turn-stage) TURN_END) 
            (set (current-player) ?next)
            (set (current-performer) ?next)
        )
  )
)


