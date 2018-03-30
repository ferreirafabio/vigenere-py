# vigenere-py
Algorithm for deciphering a message encoded with the Vigenère cipher written in python 3.
The code runs the following steps:
1. it tries to find the length of the key word used to encode the message by applying the Friedman test method (according to the given upper and lower bound of the sum of letter frequencies)
2. once the key length has been determined, the letter distributions / relative frequency histograms of the cipher subsequences are used to deduce the key word (by using the autocorrelation method)
3. it decodes the cipher using the key word

An example cipher has been attached. For simplicity, only upper case characters of the English alphabet have been considered. See https://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher for more information.


