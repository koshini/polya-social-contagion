from collections import Counter

def main():
    # climbingLeaderboard([100, 100, 50, 40, 40, 20, 10], [5, 25, 40, 120])
    solution('', 4)

def solution(S, K):
    # write your code in Python 3.6
    S = '2-4A0r7-4k'
    s = S.replace('-','')
    r = len(s) % K
    g = (len(s) - r) / K
    d = g -1
    print(r)
    print(g)
    print(d)
    sA = []
    first = s[0:r]
    print(first)


if __name__ == '__main__':
    main()