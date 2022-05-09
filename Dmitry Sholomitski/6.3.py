from string import ascii_lowercase


class Cipher:

    def __init__(self, code_phrase):
        self.code_alphabet = list(code_phrase.lower())
        self.code_list()
        print(self.code_alphabet)

    def code_list(self):
        for x in ascii_lowercase:
            if not x in self.code_alphabet:
                self.code_alphabet.append(x)

    def encode(self, phrase):
        result = ''
        for x in phrase:
            if x.isupper():
                if x.lower() in ascii_lowercase:
                    result += self.code_alphabet[ascii_lowercase.index(x.lower())].upper()
                else:
                    result += x
            else:
                if x in ascii_lowercase:
                    result += self.code_alphabet[ascii_lowercase.index(x)]
                else:
                    result += x
        return result

    def decode(self, phrase):
        result = ''
        for x in phrase:
            if x.isupper():
                if x.lower() in ascii_lowercase:
                    result += ascii_lowercase[self.code_alphabet.index(x.lower())].upper()
                else:
                    result += x
            else:
                if x in ascii_lowercase:
                    result += ascii_lowercase[self.code_alphabet.index(x)]
                else:
                    result += x
        return result


cipher = Cipher("crypto")

print(cipher.encode("Hello world"))
print("Btggj vjmgp")

print(cipher.decode("Fjedhc dn atidsn"))
print("Kojima is genius")
