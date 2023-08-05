"""Basic Checkpoint class implementation
"""

# main imports
import os
import logging
import numpy as np

# module imports
from .Checkpoint import Checkpoint


class BasicCheckpoint(Checkpoint):
    """
    BasicCheckpoint is used for loading previous computations and start again after loading checkpoit

    Attributes:
        algo: {Algorithm} -- main algorithm instance reference
        every: {int} -- checkpoint frequency used (based on number of evaluations)
        filepath: {str} -- file path where checkpoints will be saved
    """
    def __init__(self, _algo, _every, _filepath):
        self.algo = _algo
        self.every = _every
        self.filepath = _filepath

    def run(self):
        """
        Check if necessary to do backup based on `every` variable
        """
        # get current best solution
        solution = self.algo.bestSolution

        currentEvaluation = self.algo.getGlobalEvaluation()

        # backup if necessary
        if currentEvaluation % self.every == 0:

            logging.info("Checkpoint is done into " + self.filepath)

            solutionData = ""
            solutionSize = len(solution.data)

            for index, val in enumerate(solution.data):
                solutionData += str(val)

                if index < solutionSize - 1:
                    solutionData += ' '

            line = str(currentEvaluation) + ';' + solutionData + ';' + str(
                solution.fitness()) + ';\n'

            # check if file exists
            if not os.path.exists(self.filepath):
                with open(self.filepath, 'w') as f:
                    f.write(line)
            else:
                with open(self.filepath, 'a') as f:
                    f.write(line)

    def load(self):
        """
        Load last backup line of solution and set algorithm state (best solution and evaluations) at this backup
        """
        if os.path.exists(self.filepath):

            logging.info('Load best solution from last checkpoint')
            with open(self.filepath) as f:

                # get last line and read data
                lastline = f.readlines()[-1]
                data = lastline.split(';')

                # get evaluation  information
                globalEvaluation = int(data[0])

                if self.algo.parent is not None:
                    self.algo.parent.numberOfEvaluations = globalEvaluation
                else:
                    self.algo.numberOfEvaluations = globalEvaluation

                # get best solution data information
                solutionData = list(map(int, data[1].split(' ')))

                self.algo.bestSolution.data = np.array(solutionData)
                self.algo.bestSolution.score = float(data[2])
        else:
            print('No backup found... Start running')
            logging.info(
                "Can't load backup... Backup filepath not valid in Checkpoint")
