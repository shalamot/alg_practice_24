def rabin_karp(pattern, text):
    base = 31
    modulus = 10 ** 9 + 9
    pattern_length = len(pattern)
    text_length = len(text)

    def calculate_hash(s, length):
        h = 0
        for i in range(length):
            h = (h * base + ord(s[i]) - ord('a') + 1) % modulus
        return h

    pattern_hash = calculate_hash(pattern, pattern_length)
    text_hash = calculate_hash(text[:pattern_length], pattern_length)

    indices = []

    for i in range(text_length - pattern_length + 1):
        if text_hash == pattern_hash:
            if text[i:i + pattern_length] == pattern:
                indices.append(i)

        if i < text_length - pattern_length:
            text_hash = (text_hash * base - (ord(text[i]) - ord('a') + 1) * pow(base, pattern_length, modulus) + (
                        ord(text[i + pattern_length]) - ord('a') + 1)) % modulus
            if text_hash < 0:
                text_hash += modulus

    return indices


def cyclic_rabin_karp(pattern, text):
    doubled_text = text + text
    indices = rabin_karp(pattern, doubled_text)
    valid_indices = [i for i in indices if i < len(text)]
    return valid_indices

