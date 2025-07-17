from abc import ABC, abstractmethod
import random


class number_generation(ABC):
    @abstractmethod
    def generate(self, *params):
        pass


class sequential_number_generation(number_generation):
    def generate(self, start, end, step):
        sequence = []
        for number in range(start, end, step):
            sequence.append(number)
        return sequence


class random_number_generation(number_generation):
    def generate(self, mean, stddev, n):
        random_numbers = []
        for i in range(n):
            number = int(random.gauss(mean, stddev))
            random_numbers.append(number)
        return random_numbers

class fibonacci_number_generation(number_generation):
    def generate(self, n):
        fibonacci = [0, 1]
        while len(fibonacci) < n:
            next_number = fibonacci[-1] + fibonacci[-2]
            fibonacci.append(next_number)
        return fibonacci

class calculation_percentile(ABC):
    @abstractmethod
    def calculate(self, array, p):
        pass
    
class nearest_percentile(calculation_percentile):
    def calculate(self, array, p):
        array.sort()
        N = len(array)
        n_p = p * N / 100 + 0.5
        index = int(round(n_p))
        percentile = array[index - 1]
        return percentile
            
class interpolated_percentile(calculation_percentile):
    def calculate(self, array, p):
        array.sort()
        N = len(array)
        p_v = []
        for i in range(1, N + 1):
            p_v_i = 100 * (i - 0.5) / N
            p_v.append(p_v_i)

        if p <= p_v[0]:
            return array[0]
        elif p >= p_v[N-1]:
            return array[N-1]

        for i in range(N - 1):
            if p_v[i] <= p < p_v[i + 1]:
                v_i = array[i]
                v_i_2 = array[i]
                p_v_i = p_v[i]
                percentile = v_i + N * (p - p_v_i) * (v_i_2 - v_i) / 100
                return percentile
                

class DistributionTester:
    def __init__(self, number_generation, calculation_percentile):
        self.number_generation = number_generation
        self.calculation_percentile = calculation_percentile

    def set_number_generation(self, number_generation):
        self.number_generation = number_generation

    def set_calculation_percentile(self, calculation_percentile):
        self.calculation_percentile = calculation_percentile

    def tester(self, *params):
        generated_numbers = self.number_generation.generate(*params)
        #print(generated_numbers)
        for p in range(10, 100, 10):
            percentile = self.calculation_percentile.calculate(generated_numbers, p)
            print(f"{p} -> percentile: {percentile}")


sequential_generation = sequential_number_generation()
random_generation = random_number_generation()
fibonacci_generation = fibonacci_number_generation()

nearest_p = nearest_percentile()
interpolated_p = interpolated_percentile()

print('Sequential + nearest')
test1 = DistributionTester(sequential_generation, nearest_p)
test1.tester(10, 100, 10)

print('Sequential + interpolated')
test1.set_calculation_percentile(interpolated_p)
test1.tester(10, 100, 10)

print('==================================================')

print('Random + nearest')
test2 = DistributionTester(random_generation, nearest_p)
test2.tester(10, 100, 10)

print('Random + interpolated')
test2 = DistributionTester(random_generation, interpolated_p)
test2.tester(10, 100, 10)

print('==================================================')

print('Fibonacci + nearest')
test3 = DistributionTester(fibonacci_generation, nearest_p)
test3.tester(10)

print('Fibonacci + interpolated')
test3 = DistributionTester(fibonacci_generation, interpolated_p)
test3.tester(10)
