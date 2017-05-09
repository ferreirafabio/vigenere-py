# vigenere-py
Algorithm for deciphering a message encoded with Vigenère cipher written in python 3
The code runs the following steps:
1. try to find the key length by using the Friedman test method (according to the given upper and lower bound of the sum of letter frequencies)
2. once the key length is known, use the letter distribution / relative frequency histograms of the cipher subsequences to decode the deduce the key word (autocorrelation method)
3. decode the cipher using the key word

An example cipher has been attached. For simplicity, only upper case characters of the English alphabet have been considered. See https://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher for more information.
