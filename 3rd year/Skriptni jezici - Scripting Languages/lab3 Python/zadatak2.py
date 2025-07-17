import sys

def get_hypotheses(path):
    hypotheses = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            numbers = line.split(' ')
            hypotheses.append(numbers)
    return hypotheses

entry = sys.argv
path_hypotheses = entry[1]

hypotheses = get_hypotheses(path_hypotheses)
quantiles = []
for i in range(1, 10):
    quantiles.append(i/10)
i = 1
print('Hyp#Q10#Q20#Q30#Q40#Q50#Q60#Q70#Q80#Q90')
for sequence in hypotheses:
    sequence = sorted(sequence)
    length = len(sequence)
    measure_values_HD = []
    for q in quantiles:
        index = int(q * length)
        measure_values_HD.append(sequence[index-1])
    measure_values_HD_output = '#'.join(measure_values_HD)
    print(f"{i:03d}#{measure_values_HD_output}")
    i = i + 1
    

