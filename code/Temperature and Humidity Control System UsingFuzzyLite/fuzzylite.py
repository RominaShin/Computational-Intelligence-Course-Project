#!/usr/bin/env python
# coding: utf-8

# In[13]:


import fuzzylite as fl
engine = fl.Engine(
    name="weatherestimator",
    description="(humidity and temperture) -> production of warmer/cooler weather"
)
engine.input_variables = [
    fl.InputVariable(
        name="temperture",
        description="difference between currunt and normal(neither hot nor cold) temperture",
        enabled=True,
        minimum=0.000,
        maximum=50.000,
        lock_range=False,
        terms=[
            fl.Trapezoid("Cool", 0.000,0.000, 22.500, 25.500),
            fl.Triangle("Normal", 22.500, 25.500, 32.500),
            fl.Trapezoid("Hot", 25.500, 32.500, 50.000 , 50.000)
        ]
    ),
    fl.InputVariable(
        name="humidity",
        description="difference between currunt and normal humidity",
        enabled=True,
        minimum=0.000,
        maximum=100.000,
        lock_range=False,
        terms=[
            fl.Trapezoid("Humid", 0.000,0.000, 50.000, 60.500),
            fl.Triangle("Normal", 50.000, 60.500, 85.500),
            fl.Trapezoid("Dry", 60.500, 85.500, 100.000 , 100.000)
        ]
    )
    
]
engine.output_variables = [
    fl.OutputVariable(
        name="control",
        description="control based on Mamdani inference",
        enabled=True,
        minimum=0.000,
        maximum=66.000,
        lock_range=False,
        aggregation=fl.Maximum(),
        defuzzifier=fl.Centroid(35.6),
        lock_previous=False,
        terms=[
            fl.Triangle("Cooler", 0.000, 6.000, 12.000),
            fl.Triangle("Normal", 18.000, 24.000, 30.000),
            fl.Triangle("lower_Warmer", 36.000, 42.000, 48.000),
            fl.Triangle("Warmer", 54.000, 60.000, 66.000)
        ]
    )
]
engine.rule_blocks = [
    fl.RuleBlock(
        name="rules",
        description="control temperture and humidity",
        enabled=True,
        conjunction=None,
        disjunction=None,
        implication=fl.Minimum(),
        activation=fl.General(),
        rules=[
            fl.Rule.create("if temperture is Hot and humidity is not Humid then control is Cooler", engine),
            #fl.Rule.create("If humidity is high and high temperture then Cooler", engine),
            fl.Rule.create("if temperture is Normal and humidity is Dry then control is Normal", engine),
            fl.Rule.create("if temperture is Normal and humidity is Humid then control is lower_Warmer", engine),
            fl.Rule.create("if temperture is Cool and humidity is Humid then control is Warmer", engine)
        ]
    )
]

