import os
import numpy as np
from scipy.optimize import differential_evolution

def read_binary_sequence_from_file(file_path):
    with open(file_path, 'rb') as file:
        return file.read().strip().decode('utf-8')

def write_binary_sequence_to_file(file_path, sequence):
    with open(file_path, 'w') as file:
        file.write(sequence)

def generate_noisy_sequence(sequence_length):
    return np.random.choice(['A', 'C', 'G', 'T'], size=sequence_length)

input_file_path = input("Enter the path of the file with the binary sequence: ")
noisy_dna_sequence = read_binary_sequence_from_file(input_file_path)
sequence_length = len(noisy_dna_sequence)

def custom_objective_function(nucleotides):
    return -np.sum([n1 != n2 for n1, n2 in zip(nucleotides, noisy_dna_sequence)])

nucleotide_bounds = [(0, 3)] * sequence_length  # 0 to 3 represent A, C, G, and T

result = differential_evolution(custom_objective_function, nucleotide_bounds, maxiter=100)

decoded_dna_sequence = result.x.astype(int)
decoded_dna_sequence_as_nucleotides = ''.join(['A', 'C', 'G', 'T'][x] for x in decoded_dna_sequence)

output_file_path = os.path.splitext(input_file_path)[0] + "_decoded.txt"
write_binary_sequence_to_file(output_file_path, decoded_dna_sequence_as_nucleotides)

print("Noisy DNA Sequence:", noisy_dna_sequence)
print("Decoded DNA Sequence:", decoded_dna_sequence_as_nucleotides)
print("Decoded DNA Sequence saved to:", output_file_path)
