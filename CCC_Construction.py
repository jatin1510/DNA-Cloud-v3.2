"""
##########################################################################################
Improvised Version: DNA Cloud 3.2
Developers: Jaimin Satani, Jatin Ranpariya, Devarshi Joshi, Arpan Singhala, Chaitri Gudhka, Mukund Ladani, Nikhil Vaghasiya
Mentor: Prof. Manish K Gupta
Website: www.guptalab.org/dnacloud
This file will run on python 3.10.5
##########################################################################################
Author: Aayush Kapadia,Suparshva Mehta
Project: DNA Cloud 3
Graduate Mentor: Dixita Limbachya
Mentor: Prof. Manish K Gupta
Website: www.guptalab.org/dnacloud
##########################################################################################
"""

import itertools

def hamming_distance(s1, s2):
    return sum(c1 != c2 for c1, c2 in zip(s1, s2))

def generate_codeword(vectors, tau_i, tau_d):
    M = len(vectors)
    
    u = [list(vector) for vector in vectors]
    p = M - 1

    while p > 0:
        B = set()
        
        for i, j in itertools.combinations(range(p), 2):
            if hamming_distance(vectors[i], vectors[j]) <= tau_i and hamming_distance(u[i], u[j]) < tau_d:
                B.add((i, j))
        
        if not B:
            break
        
        i, j = B.pop()
        u[p] = [vectors[i][k] if k < int(M.bit_length()) else u[p][k] for k in range(len(u[p]))]
        B = {(i, j) for i, j in B if i < p}
        p = i
    
    vectors[M - 1] = [u[M - 1][k] if k < int(M.bit_length()) else 0 for k in range(len(u[M - 1]))]

    return vectors

M = int(input("Enter the number of vectors (M): "))

vectors = []
for i in range(M):
    vector_input = input(f"Enter vector {i + 1} as a binary string (e.g., 11010): ")
    vectors.append(list(vector_input))

tau_i = int(input("Enter the value of tau_i: "))
tau_d = int(input("Enter the value of tau_d: "))

codeword = generate_codeword(vectors, tau_i, tau_d)
print("Generated Codeword:", codeword)
