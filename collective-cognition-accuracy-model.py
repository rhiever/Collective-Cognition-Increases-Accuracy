# Code for the model in the paper, "Accurate decisions in an uncertain world:
# collective cognition increases true positives while decreasing false positives."

# Copyright 2013 Randal S. Olson.
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with
# this program. If not, see http://www.gnu.org/licenses/.


# Model that computes a group's collective True Positive and False Positive rate
# based off of a given individual TP rate and FP rate, as well as a quorum decision
# threshold. The size of the group is also a tunable parameter.
def calcGroupAccuracy(TPRate, FPRate, QuorumThreshold, GroupSize):
    from numpy.random import rand
    
    """
    TPRate: correct "yes" classifications when "yes"
    FPRate: incorrect "yes" classifications when "no"
    QuorumThreshold: % of group that must say "yes" for it to be a "yes" classification
    GroupSize: # of agents in the group
    """
    
    # group performance measures
    NumberTimesGroupYesAndPredatorPresent = 0
    NumberTimesGroupYesAndPredatorNotPresent = 0
    NumberTimesGroupNoAndPredatorPresent = 0
    NumberTimesGroupNoAndPredatorNotPresent = 0

    Repeats = 20000
    
    for Rep in range(Repeats):
        if Rep < Repeats / 2:
            PredatorPresent = False
        else:
            PredatorPresent = True
            
        NumberYesVotes = 0
        NumberNoVotes = 0
        
        # get group votes based on individual information
        for i in range(GroupSize):
            if PredatorPresent:
                # True Positives
                if rand() < TPRate:
                    NumberYesVotes += 1
                # False Negatives
                else:
                    NumberNoVotes += 1
                    
            if not PredatorPresent:
                # False Positives
                if rand() < FPRate:
                    NumberYesVotes += 1
                # True Negatives
                else:
                    NumberNoVotes += 1
                
        # get group votes based on group information
        if (float(NumberYesVotes) / float(GroupSize)) >= QuorumThreshold:
            GroupThinksPredatorPresent = True
        else:
            GroupThinksPredatorPresent = False
        
        # group decision correct?
        if PredatorPresent:
            if GroupThinksPredatorPresent:
                NumberTimesGroupYesAndPredatorPresent += 1
            else:
                NumberTimesGroupNoAndPredatorPresent += 1
        if not PredatorPresent:
            if not GroupThinksPredatorPresent:
                NumberTimesGroupNoAndPredatorNotPresent += 1
            else:
                NumberTimesGroupYesAndPredatorNotPresent += 1
                
    GroupTPRate = float(NumberTimesGroupYesAndPredatorPresent) / float(NumberTimesGroupYesAndPredatorPresent + NumberTimesGroupNoAndPredatorPresent)
    GroupFPRate = (float(NumberTimesGroupYesAndPredatorNotPresent) / float(NumberTimesGroupYesAndPredatorNotPresent + NumberTimesGroupNoAndPredatorNotPresent))
    
    return GroupTPRate, GroupFPRate


# Generate data
GroupTPRates = []
GroupFPRates = []
GroupSizes = range(1, 101)

for GroupSize in GroupSizes:
    Result = calcGroupAccuracy(0.6, 0.3, 0.45, GroupSize)
    GroupTPRates.append(Result[0])
    GroupFPRates.append(Result[1])

# Generate figure
figure(figsize=(12, 7))
plot(GroupSizes, GroupTPRates, label="True Positive Rate", color="blue")
plot(GroupSizes, GroupFPRates, label="False Positive Rate", color="red")
plot(GroupSizes, [0.45] * len(GroupSizes), "--", color="black", label="Quorum Threshold")
xlabel("Group Size", fontsize=14)
ylim(-0.05, 1.05)
xticks(arange(0, 101, 10))
yticks(arange(0, 1.01, 0.1))
legend(bbox_to_anchor=(0.99, 0.9), loc=1)
