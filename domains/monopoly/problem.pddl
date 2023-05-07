

(define (problem monopoly-1) (:domain :monopoly)
    (:objects
        corner-go - space
        prop-1-1 - space
        chest-1 - space
        prop-1-2 - space
        income-tax - space
        railroad-1 - space
        prop-2-1 - space
        chance-1 - space
        prop-2-2 - space
        prop-2-3 - space
        corner-visiting - space
        prop-3-1 - space
        utility-1 - space
        prop-3-2 - space
        prop-3-3 - space
        railroad-2 - space
        prop-4-1 - space
        chest-2 - space
        prop-4-2 - space
        prop-4-3 - space
        corner-free - space
        prop-5-1 - space
        chance-2 - space
        prop-5-2 - space
        prop-5-3 - space
        railroad-3 - space
        prop-6-1 - space
        prop-6-2 - space
        utility-2 - space
        prop-6-3 - space
        corner-goto-jail - space
        prop-7-1 - space
        prop-7-2 - space
        chest-3 - space
        prop-7-3 - space
        railroad-4 - space
        chance-3 - space
        prop-8-1 - space
        luxury-tax - space
        prop-8-2 - space


        title-1-1
        title-1-2
        title-2-1
        title-2-2
        title-2-3
        title-3-1
        title-3-2
        title-3-3
        title-4-1
        title-4-2
        title-4-3
        title-5-1
        title-5-2
        title-5-3
        title-6-1
        title-6-2
        title-6-3
        title-7-1
        title-7-2
        title-7-3
        title-8-1
        title-8-2 - title
        
        title-u1 title-u2 title-r1 title-r2 title-r3 title-r4 - title


        brown light_blue purple orange red yellow green dark_blue - color

        p1 p2 p3 p4 - player
    )
    (:init
        (= (space-num corner-go)  0)
        (= (space-num prop-1-1)	1)
        (= (space-num chest-1)	2)
        (= (space-num prop-1-2)	3)
        (= (space-num income-tax)	4)
        (= (space-num railroad-1)	5)
        (= (space-num prop-2-1)	6)
        (= (space-num chance-1)	7)
        (= (space-num prop-2-2)	8)
        (= (space-num prop-2-3)	9)
        (= (space-num corner-visiting)	10)
        (= (space-num prop-3-1)	11)
        (= (space-num utility-1)	12)
        (= (space-num prop-3-2)	13)
        (= (space-num prop-3-3)	14)
        (= (space-num railroad-2)	15)
        (= (space-num prop-4-1)	16)
        (= (space-num chest-2)	17)
        (= (space-num prop-4-2)	18)
        (= (space-num prop-4-3)	19)
        (= (space-num corner-free)	20)
        (= (space-num prop-5-1)	21)
        (= (space-num chance-2)	22)
        (= (space-num prop-5-2)	23)
        (= (space-num prop-5-3)	24)
        (= (space-num railroad-3)	25)
        (= (space-num prop-6-1)	26)
        (= (space-num prop-6-2)	27)
        (= (space-num utility-2)	28)
        (= (space-num prop-6-3)	29)
        (= (space-num corner-goto-jail)	30)
        (= (space-num prop-7-1)	31)
        (= (space-num prop-7-2)	32)
        (= (space-num chest-3)	33)
        (= (space-num prop-7-3)	34)
        (= (space-num railroad-4)	35)
        (= (space-num chance-3)	36)
        (= (space-num prop-8-1)	37)
        (= (space-num luxury-tax)	38)
        (= (space-num prop-8-2)	39)
        
        (= (position-space 0) corner-go)
        (= (position-space 1) prop-1-1)
        (= (position-space 2) chest-1)
        (= (position-space 3) prop-1-2)
        (= (position-space 4) income-tax)
        (= (position-space 5) railroad-1)
        (= (position-space 6) prop-2-1)
        (= (position-space 7) chance-1)
        (= (position-space 8) prop-2-2)
        (= (position-space 9) prop-2-3)
        (= (position-space 10) corner-visiting)
        (= (position-space 11) prop-3-1)
        (= (position-space 12) utility-1)
        (= (position-space 13) prop-3-2)
        (= (position-space 14) prop-3-3)
        (= (position-space 15) railroad-2)
        (= (position-space 16) prop-4-1)
        (= (position-space 17) chest-2)
        (= (position-space 18) prop-4-2)
        (= (position-space 19) prop-4-3)
        (= (position-space 20) corner-free)
        (= (position-space 21) prop-5-1)
        (= (position-space 22) chance-2)
        (= (position-space 23) prop-5-2)
        (= (position-space 24) prop-5-3)
        (= (position-space 25) railroad-3)
        (= (position-space 26) prop-6-1)
        (= (position-space 27) prop-6-2)
        (= (position-space 28) utility-2)
        (= (position-space 29) prop-6-3)
        (= (position-space 30) corner-goto-jail)
        (= (position-space 31) prop-7-1)
        (= (position-space 32) prop-7-2)
        (= (position-space 33) chest-3)
        (= (position-space 34) prop-7-3)
        (= (position-space 35) railroad-4)
        (= (position-space 36) chance-3)
        (= (position-space 37) prop-8-1)
        (= (position-space 38) luxury-tax)
        (= (position-space 39) prop-8-2)

        (= (max-position) 40)

        (= (space-type corner-go)  GO)
        (= (space-type prop-1-1)	PROPERTY)
        (= (space-type chest-1)	CHEST)
        (= (space-type prop-1-2)	PROPERTY)
        (= (space-type income-tax)	TAX)
        (= (space-type railroad-1)	RAILROAD)
        (= (space-type prop-2-1)	PROPERTY)
        (= (space-type chance-1)	CHANCE)
        (= (space-type prop-2-2)	PROPERTY)
        (= (space-type prop-2-3)	PROPERTY)
        (= (space-type corner-visiting)	JUST_VISITING)
        (= (space-type prop-3-1)	PROPERTY)
        (= (space-type utility-1)	UTILITY)
        (= (space-type prop-3-2)	PROPERTY)
        (= (space-type prop-3-3)	PROPERTY)
        (= (space-type railroad-2)	RAILROAD)
        (= (space-type prop-4-1)	PROPERTY)
        (= (space-type chest-2)	CHEST)
        (= (space-type prop-4-2)	PROPERTY)
        (= (space-type prop-4-3)	PROPERTY)
        (= (space-type corner-free)	FREE_PARKING)
        (= (space-type prop-5-1)	PROPERTY)
        (= (space-type chance-2)	CHANCE)
        (= (space-type prop-5-2)	PROPERTY)
        (= (space-type prop-5-3)	PROPERTY)
        (= (space-type railroad-3)	RAILROAD)
        (= (space-type prop-6-1)	PROPERTY)
        (= (space-type prop-6-2)	PROPERTY)
        (= (space-type utility-2)	UTILITY)
        (= (space-type prop-6-3)	PROPERTY)
        (= (space-type corner-goto-jail)	GO_TO_JAIL)
        (= (space-type prop-7-1)	PROPERTY)
        (= (space-type prop-7-2)	PROPERTY)
        (= (space-type chest-3)	CHEST)
        (= (space-type prop-7-3)	PROPERTY)
        (= (space-type railroad-4)	RAILROAD)
        (= (space-type chance-3)	CHANCE)
        (= (space-type prop-8-1)	PROPERTY)
        (= (space-type luxury-tax)	TAX)
        (= (space-type prop-8-2)	PROPERTY)

        (= (space-color prop-1-1)	brown)
        (= (space-color prop-1-2)	brown)
        (= (space-color prop-2-1)	light_blue)
        (= (space-color prop-2-2)	light_blue)
        (= (space-color prop-2-3)	light_blue)
        (= (space-color prop-3-1)	purple)
        (= (space-color prop-3-2)	purple)
        (= (space-color prop-3-3)	purple)
        (= (space-color prop-4-1)	orange)
        (= (space-color prop-4-2)	orange)
        (= (space-color prop-4-3)	orange)
        (= (space-color prop-5-1)	red)
        (= (space-color prop-5-2)	red)
        (= (space-color prop-5-3)	red)
        (= (space-color prop-6-1)	yellow)
        (= (space-color prop-6-2)	yellow)
        (= (space-color prop-6-3)	yellow)
        (= (space-color prop-7-1)	green)
        (= (space-color prop-7-2)	green)
        (= (space-color prop-7-3)	green)
        (= (space-color prop-8-1)	dark_blue)
        (= (space-color prop-8-2)	dark_blue)
        
        (= (space-title prop-1-1) title-1-1)
        (= (space-title prop-1-2) title-1-2)
        (= (space-title prop-2-1) title-2-1)
        (= (space-title prop-2-2) title-2-2)
        (= (space-title prop-2-3) title-2-3)
        (= (space-title prop-3-1) title-3-1)
        (= (space-title prop-3-2) title-3-2)
        (= (space-title prop-3-3) title-3-3)
        (= (space-title prop-4-1) title-4-1)
        (= (space-title prop-4-2) title-4-2)
        (= (space-title prop-4-3) title-4-3)
        (= (space-title prop-5-1) title-5-1)
        (= (space-title prop-5-2) title-5-2)
        (= (space-title prop-5-3) title-5-3)
        (= (space-title prop-6-1) title-6-1)
        (= (space-title prop-6-2) title-6-2)
        (= (space-title prop-6-3) title-6-3)
        (= (space-title prop-7-1) title-7-1)
        (= (space-title prop-7-2) title-7-2)
        (= (space-title prop-7-3) title-7-3)
        (= (space-title prop-8-1) title-8-1)
        (= (space-title prop-8-2) title-8-2)
        
        (= (space-title railroad-1) title-r1)
        (= (space-title railroad-2) title-r2)
        (= (space-title railroad-3) title-r3)
        (= (space-title railroad-4) title-r4)
        
        (= (space-title utility-1) title-u1)
        (= (space-title utility-2) title-u2)

        (= (space-rent income-tax) 200)
        (= (space-rent luxury-tax) 100)
        
        (= (player-cash player1) 1500)
        (= (player-cash player2) 1500)
        
        (= (player-next player1) player2)
        (= (player-next player2) player1)
        
        (= (title-name title-1-1) Mediterranean_Avenue)
        (= (title-cost title-1-1) 60)
        (= (title-rent-unimproved title-1-1) 2)
        (= (title-rent-houses title-1-1 0) 4)
        (= (title-rent-houses title-1-1 1) 10)
        (= (title-rent-houses title-1-1 2) 30)
        (= (title-rent-houses title-1-1 3) 90)
        (= (title-rent-houses title-1-1 4) 160)
        (= (title-rent-houses title-1-1 5) 250)
        (= (title-mortgage-value title-1-1) 30)
        (= (title-house-cost title-1-1) 50)
        
        (= (title-name title-1-2) Baltic_Avenue)
        (= (title-cost title-1-2) 60)
        (= (title-rent-unimproved title-1-2) 4)
        (= (title-rent-houses title-1-2 0) 8)
        (= (title-rent-houses title-1-2 1) 20)
        (= (title-rent-houses title-1-2 2) 60)
        (= (title-rent-houses title-1-2 3) 180)
        (= (title-rent-houses title-1-2 4) 320)
        (= (title-rent-houses title-1-2 5) 450)
        (= (title-mortgage-value title-1-2) 30)
        (= (title-house-cost title-1-2) 50)
        
        
        (= (title-name title-2-1) Oriental_Avenue)
        (= (title-cost title-2-1) 100)
        (= (title-rent-unimproved title-2-1) 6)
        (= (title-rent-houses title-2-1 0) 12)
        (= (title-rent-houses title-2-1 1) 30)
        (= (title-rent-houses title-2-1 2) 90)
        (= (title-rent-houses title-2-1 3) 270)
        (= (title-rent-houses title-2-1 4) 400)
        (= (title-rent-houses title-2-1 5) 550)
        (= (title-mortgage-value title-2-1) 50)
        (= (title-house-cost title-2-1) 50)
        
        (= (title-name title-2-2) Vermont_Avenue)
        (= (title-cost title-2-2) 100)
        (= (title-rent-unimproved title-2-2) 6)
        (= (title-rent-houses title-2-2 0) 12)
        (= (title-rent-houses title-2-2 1) 30)
        (= (title-rent-houses title-2-2 2) 90)
        (= (title-rent-houses title-2-2 3) 270)
        (= (title-rent-houses title-2-2 4) 400)
        (= (title-rent-houses title-2-2 5) 550)
        (= (title-mortgage-value title-2-2) 50)
        (= (title-house-cost title-2-2) 50)

        (= (title-name title-2-3) Connecticut_Avenue)
        (= (title-cost title-2-3) 120)
        (= (title-rent-unimproved title-2-3) 8)
        (= (title-rent-houses title-2-3 0) 16)
        (= (title-rent-houses title-2-3 1) 40)
        (= (title-rent-houses title-2-3 2) 100)
        (= (title-rent-houses title-2-3 3) 300)
        (= (title-rent-houses title-2-3 4) 450)
        (= (title-rent-houses title-2-3 5) 600)
        (= (title-mortgage-value title-2-3) 60)
        (= (title-house-cost title-2-3) 50)

        
        (= (title-name title-3-1) St_Charles_Place)
        (= (title-cost title-3-1) 140)
        (= (title-rent-unimproved title-3-1) 10)
        (= (title-rent-houses title-3-1 0) 20)
        (= (title-rent-houses title-3-1 1) 50)
        (= (title-rent-houses title-3-1 2) 150)
        (= (title-rent-houses title-3-1 3) 450)
        (= (title-rent-houses title-3-1 4) 625)
        (= (title-rent-houses title-3-1 5) 750)
        (= (title-mortgage-value title-3-1) 70)
        (= (title-house-cost title-3-1) 100)
        
        (= (title-name title-3-2) States_Avenue)
        (= (title-cost title-3-2) 140)
        (= (title-rent-unimproved title-3-2) 10)
        (= (title-rent-houses title-3-2 0) 20)
        (= (title-rent-houses title-3-2 1) 50)
        (= (title-rent-houses title-3-2 2) 150)
        (= (title-rent-houses title-3-2 3) 450)
        (= (title-rent-houses title-3-2 4) 625)
        (= (title-rent-houses title-3-2 5) 750)
        (= (title-mortgage-value title-3-2) 70)
        (= (title-house-cost title-3-2) 100)

        (= (title-name title-3-3) Virginia_Avenue)
        (= (title-cost title-3-3) 160)
        (= (title-rent-unimproved title-3-3) 12)
        (= (title-rent-houses title-3-3 0) 24)
        (= (title-rent-houses title-3-3 1) 60)
        (= (title-rent-houses title-3-3 2) 180)
        (= (title-rent-houses title-3-3 3) 500)
        (= (title-rent-houses title-3-3 4) 700)
        (= (title-rent-houses title-3-3 5) 900)
        (= (title-mortgage-value title-3-3) 80)
        (= (title-house-cost title-3-3) 100)

        
        (= (title-name title-4-1) St_James_Place)
        (= (title-cost title-4-1) 180)
        (= (title-rent-unimproved title-4-1) 14)
        (= (title-rent-houses title-4-1 0) 28)
        (= (title-rent-houses title-4-1 1) 70)
        (= (title-rent-houses title-4-1 2) 200)
        (= (title-rent-houses title-4-1 3) 550)
        (= (title-rent-houses title-4-1 4) 750)
        (= (title-rent-houses title-4-1 5) 950)
        (= (title-mortgage-value title-4-1) 90)
        (= (title-house-cost title-4-1) 100)
        
        (= (title-name title-4-2) Tennessee_Avenue)
        (= (title-cost title-4-2) 180)
        (= (title-rent-unimproved title-4-2) 14)
        (= (title-rent-houses title-4-2 0) 28)
        (= (title-rent-houses title-4-2 1) 70)
        (= (title-rent-houses title-4-2 2) 200)
        (= (title-rent-houses title-4-2 3) 550)
        (= (title-rent-houses title-4-2 4) 750)
        (= (title-rent-houses title-4-2 5) 950)
        (= (title-mortgage-value title-4-2) 90)
        (= (title-house-cost title-4-2) 100)
        
        (= (title-name title-4-3) New_York_Avenue)
        (= (title-cost title-4-3) 200)
        (= (title-rent-unimproved title-4-3) 16)
        (= (title-rent-houses title-4-3 0) 28)
        (= (title-rent-houses title-4-3 1) 80)
        (= (title-rent-houses title-4-3 2) 220)
        (= (title-rent-houses title-4-3 3) 600)
        (= (title-rent-houses title-4-3 4) 800)
        (= (title-rent-houses title-4-3 5) 1000)
        (= (title-mortgage-value title-4-3) 100)
        (= (title-house-cost title-4-3) 100)

        
        (= (title-name title-5-1) Kentucky_Avenue)
        (= (title-cost title-5-1) 220)
        (= (title-rent-unimproved title-5-1) 18)
        (= (title-rent-houses title-5-1 0) 36)
        (= (title-rent-houses title-5-1 1) 90)
        (= (title-rent-houses title-5-1 2) 250)
        (= (title-rent-houses title-5-1 3) 700)
        (= (title-rent-houses title-5-1 4) 875)
        (= (title-rent-houses title-5-1 5) 1050)
        (= (title-mortgage-value title-5-1) 110)
        (= (title-house-cost title-5-1) 150)	
        
        (= (title-name title-5-2) Indiana_Avenue)
        (= (title-cost title-5-2) 220)
        (= (title-rent-unimproved title-5-2) 18)
        (= (title-rent-houses title-5-2 0) 36)
        (= (title-rent-houses title-5-2 1) 90)
        (= (title-rent-houses title-5-2 2) 250)
        (= (title-rent-houses title-5-2 3) 700)
        (= (title-rent-houses title-5-2 4) 875)
        (= (title-rent-houses title-5-2 5) 1050)
        (= (title-mortgage-value title-5-2) 110)
        (= (title-house-cost title-5-2) 150)	
        
        (= (title-name title-5-3) Illinois_Avenue)
        (= (title-cost title-5-3) 220)
        (= (title-rent-unimproved title-5-3) 20)
        (= (title-rent-houses title-5-3 0) 40)
        (= (title-rent-houses title-5-3 1) 100)
        (= (title-rent-houses title-5-3 2) 300)
        (= (title-rent-houses title-5-3 3) 750)
        (= (title-rent-houses title-5-3 4) 925)
        (= (title-rent-houses title-5-3 5) 1100)
        (= (title-mortgage-value title-5-3) 120)
        (= (title-house-cost title-5-3) 150)	
    
        
        (= (title-name title-6-1) Atlantic_Avenue)
        (= (title-cost title-6-1) 260)
        (= (title-rent-unimproved title-6-1) 22)
        (= (title-rent-houses title-6-1 0) 44)
        (= (title-rent-houses title-6-1 1) 110)
        (= (title-rent-houses title-6-1 2) 330)
        (= (title-rent-houses title-6-1 3) 800)
        (= (title-rent-houses title-6-1 4) 975)
        (= (title-rent-houses title-6-1 5) 1150)
        (= (title-mortgage-value title-6-1) 130)
        (= (title-house-cost title-6-1) 150)	    
        
        (= (title-name title-6-2) Ventnor_Avenue)
        (= (title-cost title-6-2) 260)
        (= (title-rent-unimproved title-6-2) 22)
        (= (title-rent-houses title-6-2 0) 44)
        (= (title-rent-houses title-6-2 1) 110)
        (= (title-rent-houses title-6-2 2) 330)
        (= (title-rent-houses title-6-2 3) 800)
        (= (title-rent-houses title-6-2 4) 975)
        (= (title-rent-houses title-6-2 5) 1150)
        (= (title-mortgage-value title-6-2) 130)
        (= (title-house-cost title-6-2) 150)	    
        
        (= (title-name title-6-3) Marvin_Gardens)
        (= (title-cost title-6-3) 280)
        (= (title-rent-unimproved title-6-3) 24)
        (= (title-rent-houses title-6-3 0) 48)
        (= (title-rent-houses title-6-3 1) 120)
        (= (title-rent-houses title-6-3 2) 360)
        (= (title-rent-houses title-6-3 3) 850)
        (= (title-rent-houses title-6-3 4) 1025)
        (= (title-rent-houses title-6-3 5) 1200)
        (= (title-mortgage-value title-6-3) 140)
        (= (title-house-cost title-6-3) 150)

        
        (= (title-name title-7-1) Pacific_Avenue)
        (= (title-cost title-7-1) 300)
        (= (title-rent-unimproved title-7-1) 26)
        (= (title-rent-houses title-7-1 0) 52)
        (= (title-rent-houses title-7-1 1) 130)
        (= (title-rent-houses title-7-1 2) 390)
        (= (title-rent-houses title-7-1 3) 900)
        (= (title-rent-houses title-7-1 4) 1100)
        (= (title-rent-houses title-7-1 5) 1275)
        (= (title-mortgage-value title-7-1) 150)
        (= (title-house-cost title-7-1) 200)
    
        (= (title-name title-7-2) North_Carolina_Avenue)
        (= (title-cost title-7-2) 300)
        (= (title-rent-unimproved title-7-2) 26)
        (= (title-rent-houses title-7-2 0) 52)
        (= (title-rent-houses title-7-2 1) 130)
        (= (title-rent-houses title-7-2 2) 390)
        (= (title-rent-houses title-7-2 3) 900)
        (= (title-rent-houses title-7-2 4) 1100)
        (= (title-rent-houses title-7-2 5) 1275)
        (= (title-mortgage-value title-7-2) 150)
        (= (title-house-cost title-7-2) 200)
    
        (= (title-name title-7-3) Pennsylvania_Avenue)
        (= (title-cost title-7-3) 300)
        (= (title-rent-unimproved title-7-3) 26)
        (= (title-rent-houses title-7-3 0) 52)
        (= (title-rent-houses title-7-3 1) 150)
        (= (title-rent-houses title-7-3 2) 450)
        (= (title-rent-houses title-7-3 3) 1000)
        (= (title-rent-houses title-7-3 4) 1200)
        (= (title-rent-houses title-7-3 5) 1400)
        (= (title-mortgage-value title-7-3) 160)
        (= (title-house-cost title-7-3) 200)


        (= (title-name title-8-1) Park_Place)
        (= (title-cost title-8-1) 350)
        (= (title-rent-unimproved title-8-1) 35)
        (= (title-rent-houses title-8-1 0) 70)
        (= (title-rent-houses title-8-1 1) 175)
        (= (title-rent-houses title-8-1 2) 500)
        (= (title-rent-houses title-8-1 3) 1100)
        (= (title-rent-houses title-8-1 4) 1300)
        (= (title-rent-houses title-8-1 5) 1500)
        (= (title-mortgage-value title-8-1) 175)
        (= (title-house-cost title-8-1) 200)

        (= (title-name title-8-2) Boardwalk)
        (= (title-cost title-8-2) 400)
        (= (title-rent-unimproved title-8-2) 50)
        (= (title-rent-houses title-8-2 0) 100)
        (= (title-rent-houses title-8-2 1) 200)
        (= (title-rent-houses title-8-2 2) 600)
        (= (title-rent-houses title-8-2 3) 1400)
        (= (title-rent-houses title-8-2 4) 1700)
        (= (title-rent-houses title-8-2 5) 2000)
        (= (title-mortgage-value title-8-2) 200)
        (= (title-house-cost title-8-2) 200)
    

        (= (title-name title-u1) Electric_Company)
        (= (title-cost title-u1) 150)
        (= (title-rent-unimproved title-u1) -1)
        (= (title-rent-houses title-u1 0) -1)
        (= (title-rent-houses title-u1 1) -1)
        (= (title-rent-houses title-u1 2) -1)
        (= (title-rent-houses title-u1 3) -1)
        (= (title-rent-houses title-u1 4) -1)
        (= (title-rent-houses title-u1 5) -1)
        (= (title-mortgage-value title-u1) 75)
        (= (title-house-cost title-u1) -1)

        (= (title-name title-u2) Water_Works)
        (= (title-cost title-u2) 150)
        (= (title-rent-unimproved title-u2) -1)
        (= (title-rent-houses title-u2 0) -1)
        (= (title-rent-houses title-u2 1) -1)
        (= (title-rent-houses title-u2 2) -1)
        (= (title-rent-houses title-u2 3) -1)
        (= (title-rent-houses title-u2 4) -1)
        (= (title-rent-houses title-u2 5) -1)
        (= (title-mortgage-value title-u2) 75)
        (= (title-house-cost title-u2) -1)
        

        (= (title-name title-r1) Reading_Railroad)
        (= (title-cost title-r1) 200)
        (= (title-rent-unimproved title-r1) -1)
        (= (title-rent-houses title-r1 0) -1)
        (= (title-rent-houses title-r1 1) -1)
        (= (title-rent-houses title-r1 2) -1)
        (= (title-rent-houses title-r1 3) -1)
        (= (title-rent-houses title-r1 4) -1)
        (= (title-rent-houses title-r1 5) -1)
        (= (title-mortgage-value title-r1) 100)
        (= (title-house-cost title-r1) -1)

        (= (title-name title-r2) B_O_Railroad)
        (= (title-cost title-r2) 200)
        (= (title-rent-unimproved title-r2) -1)
        (= (title-rent-houses title-r2 0) -1)
        (= (title-rent-houses title-r2 1) -1)
        (= (title-rent-houses title-r2 2) -1)
        (= (title-rent-houses title-r2 3) -1)
        (= (title-rent-houses title-r2 4) -1)
        (= (title-rent-houses title-r2 5) -1)
        (= (title-mortgage-value title-r2) 100)
        (= (title-house-cost title-r2) -1)

        (= (title-name title-r3) Pennsylvania_Railroad)
        (= (title-cost title-r3) 200)
        (= (title-rent-unimproved title-r3) -1)
        (= (title-rent-houses title-r3 0) -1)
        (= (title-rent-houses title-r3 1) -1)
        (= (title-rent-houses title-r3 2) -1)
        (= (title-rent-houses title-r3 3) -1)
        (= (title-rent-houses title-r3 4) -1)
        (= (title-rent-houses title-r3 5) -1)
        (= (title-mortgage-value title-r3) 100)
        (= (title-house-cost title-r3) -1)

        (= (title-name title-r4) Short_Line)
        (= (title-cost title-r4) 200)
        (= (title-rent-unimproved title-r4) -1)
        (= (title-rent-houses title-r4 0) -1)
        (= (title-rent-houses title-r4 1) -1)
        (= (title-rent-houses title-r4 2) -1)
        (= (title-rent-houses title-r4 3) -1)
        (= (title-rent-houses title-r4 4) -1)
        (= (title-rent-houses title-r4 5) -1)
        (= (title-mortgage-value title-r4) 100)
        (= (title-house-cost title-r4) -1)
        
        (= (just-visiting-position) 10)
      
        (= (available-houses) 32)
        (= (available-hotels) 12)
        
        (= (utilities-owned-multiplier 0) 0)
        (= (utilities-owned-multiplier 1) 4)
        (= (utilities-owned-multiplier 2) 10)
        
        (= (railroad-rent 0) 0)
        (= (railroad-rent 1) 25)
        (= (railroad-rent 2) 50)
        (= (railroad-rent 3) 100)
        (= (railroad-rent 4) 200)
        
        (= (current-player) player1)
        (= (current-performer) player1)
        (= (turn-stage) PRE_ROLL)
        (= (self) p1)
    )

    (:goal
        (or
            (and
                (= (self) p1)
                (> (player-cash p1) 0)
                (<= (player-cash p2) 0)
                (<= (player-cash p3) 0)
                (<= (player-cash p4) 0)
            )
            (and
                (= (self) p2)
                (> (player-cash p2) 0)
                (<= (player-cash p1) 0)
                (<= (player-cash p3) 0)
                (<= (player-cash p4) 0)
            )
            (and
                (= (self) p3)
                (> (player-cash p3) 0)
                (<= (player-cash p2) 0)
                (<= (player-cash p1) 0)
                (<= (player-cash p4) 0)
            )
            (and
                (= (self) p4)
                (> (player-cash p4) 0)
                (<= (player-cash p2) 0)
                (<= (player-cash p3) 0)
                (<= (player-cash p1) 0)
            )
        )
    )
)
