# Levenshtein Distance Function
def minDistance(self, word1: str, word2: str) -> int:
        
    n = len(word1)
    m = len(word2)
    dp = [[-1 for i in range(m+1)] for i in range(n+1)]
        
    for i in range(n+1):
        dp[i][0] = i
        
    for j in range(m+1):
        dp[0][j] = j
            
    for i in range(1,n+1):
        for j in range(1,m+1):
            if(word1[i-1] == word2[j-1]):
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i-1][j-1],dp[i-1][j],dp[i][j-1])
    return dp[n][m]


# LCS Distance Function
def lcs_algo(S1, S2, m, n):
    L = [[0 for x in range(n+1)] for x in range(m+1)]

    # Building the matrix in bottom-up way
    for i in range(m+1):
        for j in range(n+1):
            if i == 0 or j == 0:
                L[i][j] = 0
            elif S1[i-1] == S2[j-1]:
                L[i][j] = L[i-1][j-1] + 1
            else:
                L[i][j] = max(L[i-1][j], L[i][j-1])

    index = L[m][n]

    lcs_algo = [""] * (index+1)
    lcs_algo[index] = ""

    i = m
    j = n
    while i > 0 and j > 0:

        if S1[i-1] == S2[j-1]:
            lcs_algo[index-1] = S1[i-1]
            i -= 1
            j -= 1
            index -= 1

        elif L[i-1][j] > L[i][j-1]:
            i -= 1
        else:
            j -= 1
            
    # Printing the sub sequences
    result = "".join(lcs_algo)
    return result




# -------------------------------------- SECTION_1 -------------------------------------- #


f1 = open("C:/Users/Admin/Documents/GitHub/Corpus/Languages/African/African.txt","r")
text1 = f1.readlines()
string1 = ""
for lines in text1:
    string1 += lines
#print(string1)
f1.close()

f2 = open("C:/Users/Admin/Documents/GitHub/Corpus/Languages/English/English.txt","r")
text2 = f2.readlines()
string2 = ""
for lines in text2:
    string2 += lines
#print(string2)
f2.close()

print("----------------------------------------------------------------")

# LCS Distance Function (btw corpuses)
result1 = lcs_algo(string1, string2, len(string1), len(string2))
#print(result1)
print("----------------------------------------------------------------")

# Levenshtein Distance Function
result2 = minDistance(string1,string2)
#print(result2)
print("----------------------------------------------------------------")

