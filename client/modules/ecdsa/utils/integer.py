from random import SystemRandom

class RandomInteger: 

    @classmethod
    def between(self, min, max): 
        """
        Return integer x in the range: min <= x <= max
s
        :param min: minimum value of the integer
        :param max: maximum value of the integer
        :return:
        """

        return SystemRandom().randrange(min, max + 1)