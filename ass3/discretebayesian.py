# discretebayesian.py
#
# Compute probabilities from Discrete Bayesian Networks.
#
# Author: Anthony Shackell - June 15, 2018

from pgmpy.models import BayesianModel
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination, BeliefPropagation


def main():
    # construct empty graph
    G = BayesianModel()
    # define nodes of graph
    G.add_nodes_from(['difficulty', 'musicianship', 'rating', 'exam', 'letter'])
    # define edges of graph
    G.add_edges_from([('difficulty', 'rating'), ('musicianship', 'rating'), ('musicianship', 'exam'), ('rating', 'letter')])

    # define Conditional Probability Distributions
    cpd_difficulty = TabularCPD(variable='difficulty', variable_card=2, values=[[0.6, 0.4]])
    cpd_musicianship = TabularCPD(variable='musicianship', variable_card=2, values=[[0.7, 0.3]])
    cpd_rating = TabularCPD(variable='rating', variable_card=3,
                   values=[[0.3, 0.05, 0.9,  0.5],
                           [0.4, 0.25, 0.08, 0.3],
                           [0.3, 0.7,  0.02, 0.2]],
                  evidence=['musicianship', 'difficulty'],
                  evidence_card=[2, 2])
    cpd_exam = TabularCPD(variable='exam', variable_card=2,
                   values=[[0.95, 0.2],
                           [0.05, 0.8]],
                   evidence=['musicianship'],
                   evidence_card=[2])
    cpd_letter = TabularCPD(variable='letter', variable_card=2,
                   values=[[0.1, 0.4, 0.99],
                           [0.9, 0.6, 0.01]],
                   evidence=['rating'],
                   evidence_card=[3])

    # add CPDs to graph
    G.add_cpds(cpd_difficulty, cpd_musicianship, cpd_rating, cpd_exam, cpd_letter)

    # construct inference object
    infer = VariableElimination(G)

    # Question 1
    print "Question 1:\n", infer.query(['letter'], evidence={'musicianship': 1, 'difficulty': 0, 'exam': 1, 'rating': 1}) ['letter']

    # Question 2
    print "\nQuestion 2 (no evidence):\n", infer.query(['letter']) ['letter']
    print "\nQuestion 2 (weak musician):\n", infer.query(['letter'], evidence={'musicianship': 0}) ['letter']

    # Question 3:
    print "\nRejection Sampling (100000 samples):\n"


if __name__ == '__main__':
    main()
