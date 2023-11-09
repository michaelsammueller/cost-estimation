# cost-estimation
SEPM Assignment 2 Project Cost Estimation Project


## Cost Estimation Techniques
Several types of cost estimation techniques are used within the industry, such as:

- COCOMO
- Delphi
- Expert Judgement
- Halstead's software science

For the software aspect of this project, "COCOMO" seems to be the most applicable estimation method. However, "COCOMO" relies heavily on **LOC** (Lines of Code) to estimate cost - information which we do not have.

A basic implementation of "COCOMO" can be found in the `cocomo.py` file within this repository. The code will have to be adjusted to fit our project, depending on which factors we would like to consider.

However, since we are given information about financial cost (for both components and staff), as well as required person-weeks for design and manufacture, I doubt that using a common estimation algorithm would bring any benefit, as such algorithms are mainly used to estimate the amount of time needed to complete such project. It would make more sense to adopt parts of this algorithm and customize it so that we can accept user input in terms of person-weeks, hardware & software components and their costs, and then calculate a total time, total cost, and total difficulty associated with the project. @Team, let me know what you think.

## UML Class Diagram
This is a proposed class structure for the cost estimator. Note that in this design, we define a HardwareComponent class, a SoftwareComponent class, a StaffMember class, and a ProjectEstimator class.
![project_cost_estimator_v3](https://github.com/michaelsammueller/cost-estimation/assets/34138597/de70003b-d9e1-4873-aaf3-3a140760fcf1)
