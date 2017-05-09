import numpy as np
from collections import OrderedDict
import requests
from collections import Counter
from string import ascii_uppercase

ENGLISH_LETTER_FREQUENCY_URL = 'http://practicalcryptography.com/media/cryptanalysis/files/english_monograms.txt'
LOWER_INDEX = ord('A')
UPPER_INDEX = ord('Z')
LOWER_BOUNDARY_KEY_SUM = 0.070
UPPER_BOUNDARY_KEY_SUM = 0.090


def to_unic(string):
    return np.asarray([ord(c) for c in string])

def to_string(unic_array):
    return "".join([chr(i) for i in unic_array])


def compute_key_length(cipher, print_key_probabilities = False):
    '''if lazy is set to true, the first key length which sum of probabilities lies within suspicious range (~.075) is
    returned'''

    key_length_found = False
    key_length = 0
    for key_length_iter in range(1, len(cipher)):
        sum = 0
        for C in ascii_uppercase:
            sub_cipher = cipher[::key_length_iter]
            frequency = compute_letter_frequency(sub_cipher, C)
            prob = compute_key_probability(sub_cipher, frequency)
            sum = sum + prob

        if print_key_probabilities:
            print("key stride:" + str(key_length) + " Sum of probs:" + str(sum))

        if not key_length_found and LOWER_BOUNDARY_KEY_SUM <= sum <= UPPER_BOUNDARY_KEY_SUM:
            key_length_found = True
            key_length = key_length_iter

    return key_length


def compute_letter_frequency(cipher, letter):
    return Counter(cipher).get(letter)


def compute_key_probability(cipher, frequency):
    if frequency is not None:
        return np.square(frequency / len(cipher))
    else:
        return 0


def language_frequency_dict(url):
    letters = [chr(i) for i in range(LOWER_INDEX, UPPER_INDEX + 1)]
    r = requests.get(url)
    frequency_dict = {}
    for line in r.content.decode("utf-8") .split('\n'):
        split = line.split(' ')
        if len(split) == 2 and split[0] in letters:
            frequency_dict[split[0]] = int(split[1])
    freq_sum  = np.sum(list(frequency_dict.values()))
    rel_frequency_dict = {}
    for key, abs_freq in frequency_dict.items():
        rel_frequency_dict[key] = abs_freq / float(freq_sum)
        rel_frequency_dict = OrderedDict(sorted(rel_frequency_dict.items(), key=lambda t: t[0]))
    return rel_frequency_dict


def compute_subsequence_occurrences(sub_cipher):
    letters = [chr(i) for i in range(LOWER_INDEX, UPPER_INDEX + 1)]
    cipher_frequency_dict = dict.fromkeys(letters, 0)

    for letter in sub_cipher:
        cipher_frequency_dict[letter] +=1

    return cipher_frequency_dict


def get_subsequence(cipher, subsequence_position, key_length):
    cipher_chunks = [cipher[i:i + key_length] for i in range(0, len(cipher), key_length)]
    sub_sequence = ""
    for c in cipher_chunks:
        if subsequence_position < len(c):
            sub_sequence += c[subsequence_position]
    return sub_sequence


def compute_subsequence_frequencies(dict):
    freq_sum = np.sum(list(dict.values()))
    return {k: v / freq_sum for k, v in dict.items()}


def compute_key_word(language_rel_freq, cipher, key_length):
    key = []
    for key_iter in range(key_length):
        distances = []
        sub_sequence = get_subsequence(cipher, key_iter, key_length)
        for i in range(26): #all letters
            rotated_sub_cipher = decode(sub_sequence, [i+1])
            occurences = compute_subsequence_occurrences(rotated_sub_cipher)
            subsequence_rel_freq = compute_subsequence_frequencies(occurences)
            distances.append(compute_distance(subsequence_rel_freq, language_rel_freq))

        key.append(np.argmin(distances)+1)
    return key

def compute_distance(rel_freq, lang_freq):
    assert len(rel_freq) == len(lang_freq)
    rel_freq_array = np.asarray(list(lang_freq.values()))
    lang_freq_array = np.asarray(list(rel_freq.values()))
    return np.sqrt(np.sum((rel_freq_array-lang_freq_array)**2))


def rotate_char(letter, position):
    return chr( (ord(letter) - LOWER_INDEX - position) % 26 + LOWER_INDEX)


def decode(cipher, key):
    return "".join([rotate_char(ciph_letter, key[i % len(key)]) for i, ciph_letter in enumerate(cipher)])


chiffre_file = 'vigenere_chiffre.txt'
with open(chiffre_file, 'r') as f:
    cipher = f.read().replace('\n', '')

cipher_text = to_string(to_unic(cipher))

key_length = compute_key_length(cipher_text, print_key_probabilities=False)
print("found key length: " + str(key_length))

english_dict_rel_freq = language_frequency_dict(ENGLISH_LETTER_FREQUENCY_URL)
key = compute_key_word(english_dict_rel_freq, cipher_text, key_length)
print("found key: " + str([ascii_uppercase[c] for c in key]))
message = decode(cipher_text, key)
print("decoded message: " + message)