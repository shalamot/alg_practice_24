def rabin_karp_palindrome_search(text):
    base = 31
    modulus = 10 ** 9 + 9

    def calculate_hash(s):
        h = 0
        for i in range(len(s)):
            h = (h * base + ord(s[i]) - ord('a') + 1) % modulus
        return h

    def is_palindrome(substring):
        reverse_substring = substring[::-1]
        return calculate_hash(substring) == calculate_hash(reverse_substring)

    length = len(text)
    palindromes = []

    for size in range(2, length + 1):
        for start in range(length - size + 1):
            end = start + size
            substring = text[start:end]
            if is_palindrome(substring):
                palindromes.append(substring)

    return palindromes
text = "aboba"
palindromes = rabin_karp_palindrome_search(text)
print(palindromes)
