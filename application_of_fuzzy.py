import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

amoun=eval(input("enter the amount of the book"))

# antecedant and consequent range 
quality = ctrl.Antecedent(np.arange(0, 11, 1), 'quality')
oon = ctrl.Antecedent(np.arange(0, 11, 1), 'oon')
worth = ctrl.Consequent(np.arange(0, 26, 1), 'worth')

# quality explains whether the book is damaged or not in a scale of 0-10
quality['poor'] = fuzz.gaussmf(quality.universe, 0, 2)
quality['average'] = fuzz.gaussmf(quality.universe, 5,2)
quality['good'] = fuzz.gaussmf(quality.universe, 10,2)

# old or new (oon) explains how much old is the book is in a scale of 0-10
oon['old'] = fuzz.gaussmf(oon.universe, 0, 2)
oon['somewhat new'] = fuzz.gaussmf(oon.universe, 5,2)
oon['new'] = fuzz.gaussmf(oon.universe, 10,2)

# membership function for consequent worth
worth['low'] = fuzz.gaussmf(worth.universe, 0, 4.5)
worth['medium'] = fuzz.gaussmf(worth.universe, 12.5,4.5)
worth['high'] = fuzz.gaussmf(worth.universe, 25,4.5)

#view the MFs of antecedance and cosequent
worth.view()
oon.view()
quality.view()

#Defining rules
rule1 = ctrl.Rule(quality['poor'] | oon['old'], worth['low'])
rule2 = ctrl.Rule(oon['somewhat new'], worth['medium'])
rule3 = ctrl.Rule(oon['new'] | quality['good'], worth['high'])

#Creating a system with rules
worthping_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
worthping = ctrl.ControlSystemSimulation(worthping_ctrl)

#asking quality and the freshness of the book
worthping.input['quality'] = eval(input("enter the quality of the book in scale 0-10"))
worthping.input['oon'] = eval(input("enter the quality of the book in scale 0-10 (0 for too old, 10 for too new)"))

#computing worthiness
worthping.compute()

#plot worthiness
print(worthping.output['worth'])
worth.view(sim=worthping)

#calculate the amount of book
print("amount that can be paid for the book: "+str(round(amoun/25*worthping.output["worth"],2))+" INR")
