"""."""
import sys


class Solution:
    """."""

    def __init__(self, lista: [list, list] = []):
        """."""
        self.lista = lista
        self.fitness = sys.float_info.max

    def __str__(self):
        """."""
        return str(self.lista)

    def __repr__(self):
        """."""
        return self.__str__()

    def copy(self):
        """."""
        sol = Solution(list(self.lista))
        sol.fitness = self.fitness
        return sol
