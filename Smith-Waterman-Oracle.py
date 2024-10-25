import numpy as np

# Gap penalty
W = 2

# Similarity and mismatch scores
S = 3
M = -3


def smith_waterman_score_matrix(seqA, seqB):
    score_matrix = np.zeros((len(seqA) + 1, len(seqB) + 1), dtype=int)
    for i in range(score_matrix.shape[0]):
        for j in range(score_matrix.shape[1]):
            if i == 0 or j == 0:
                score_matrix[i][j] = 0
            else:
                similarity = S if seqA[i - 1] == seqB[j - 1] else M
                score_matrix[i][j] = max(
                    0,
                    score_matrix[i - 1][j - 1] + similarity,
                    max([score_matrix[a, j] - W * (i - a) for a in range(i)]),
                    max([score_matrix[i, b] - W * (j - b) for b in range(j)]),
                )

    return score_matrix


def backtrace(S, A, B):
    x, y = np.unravel_index(np.argmax(S), S.shape)
    A_aligned = []
    B_aligned = []

    while S[x, y] != 0:
        print(x, y)
        print(S[x, y])
        print(A[x - 1], B[y - 1])
        if S[x, y] == S[x - 1, y - 1] + (3 if A[x - 1] == B[y - 1] else -3):
            A_aligned.append(A[x - 1])
            B_aligned.append(B[y - 1])
            x -= 1
            y -= 1
        elif S[x, y] == S[x - 1, y] - W:
            A_aligned.append(A[x - 1])
            B_aligned.append("-")
            x -= 1
        else:
            A_aligned.append("-")
            B_aligned.append(B[y - 1])
            y -= 1

    return "".join(A_aligned[::-1]), "".join(B_aligned[::-1])


# example usage (From Wikipedia)
seqA = ["G", "G", "T", "T", "G", "A", "C", "T", "A"]
seqB = ["T", "G", "T", "T", "A", "C", "G", "G"]
matrix = smith_waterman_score_matrix(seqA, seqB)
print(matrix)

print(backtrace(matrix, seqA, seqB))
