import crypto_utils
import random
import math


# ****************SUPERKLASSE CIPHER (KRYPTERINGS-ALGORITMER)****************
class Cipher:
    def __init__(self):
        return

    alfabet = [' ', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4',
               '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?', '@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
               'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '[', "\\", ']', '^',
               '_', '`', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
               't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~']

    # Dummy-metoder
    def encode(self, key, message):
        return
    def decode(self, key, message):
        return
    def generate_keys(self):
        return
    def possible_keys(self):
        return
    def verify(self, key, message):
        return

# ****************CAESAR_CIPHER****************
# Nøkkelen er et hemmelig heltall. Hvert ASCII-tegn har et tilhørende tall, fra 0 til 94.
# Kryptert verdi er beregnet som original tallverdi av ASCII-tegnet pluss verdien av nøkkelen modulo 95
# MERK: ASCII-tegnets tilhørende tall er ikke dets ASCII-verdi, men sin index i alfabet-listen over.
# Gitt nøkkel-verdi lik 2..
# Da vil 'A', som har index 33, få kryptert verdi 35 som tilsvarer 'C', 'B' -> 'D', 'H' -> 'J' osv.
# F. eks. "HEI" -> "JGK"

class Caesar(Cipher):
    def __init__(self):
        Cipher.__init__(self)

    def encode(self, key, message):
        crypted_message = ""
        for char in message:
            new_index = (self.alfabet.index(char) + key) % 95
            crypted_char = self.alfabet[new_index]
            crypted_message += crypted_char
        return crypted_message

    def decode(self, key, message):
        decrypted_message = ""
        for char in message:
            new_index = (self.alfabet.index(char) + key) % 95
            decrypted_char = self.alfabet[new_index]
            decrypted_message += decrypted_char
        return decrypted_message

    def generate_keys(self):
        sender_key = random.randint(0,95)
        receiver_key = 95 - sender_key
        return [sender_key, receiver_key]

    def verify(self, keys, message):
        crypted_message = self.encode(keys[0], message)
        decrypted_message = self.decode(keys[1], crypted_message)
        return message == decrypted_message

    def possible_keys(self):
        return list(range(95))

# ****************MULTIPLICATIVE_CIPHER****************
class Multiplicative(Cipher):
    def __init__(self):
        Cipher.__init__(self)

    def encode(self, key, message):
        crypted_message = ""
        for char in message:
            new_index = (self.alfabet.index(char)*key) % 95
            crypted_char = self.alfabet[new_index]
            crypted_message += crypted_char
        return crypted_message

    def decode(self, key, message):
        decrypted_message = ""
        for char in message:
            new_index = (self.alfabet.index(char)*key) % 95
            decrypted_char = self.alfabet[new_index]
            decrypted_message += decrypted_char
        return decrypted_message

    def generate_keys(self):
        sender_key = random.randint(0, 95)
        receiver_key = crypto_utils.modular_inverse(sender_key, 95)
        while not receiver_key:
            sender_key = random.randint(0, 95)
            receiver_key = crypto_utils.modular_inverse(sender_key, 95)
        return [sender_key, receiver_key]

    def possible_keys(self):
        return list(range(95))

    def verify(self, keys, message):
        crypted_message = self.encode(keys[0], message)
        decrypted_message = self.decode(keys[1], crypted_message)
        return message == decrypted_message

# ****************AFFINE_CIPHER****************
class Affine(Cipher):
    def __init__(self):
        Cipher.__init__(self)

    def encode(self, key, message):
        crypted_message = ""
        for char in message:
            mult_index = (self.alfabet.index(char)*key[0]) % 95
            new_index = (mult_index + key[1]) % 95
            crypted_char = self.alfabet[new_index]
            crypted_message += crypted_char
        return crypted_message

    def decode(self, key, message):
        decrypted_message = ""
        for char in message:
            add_index = (self.alfabet.index(char) + key[1]) % 95
            mult_index = (add_index*key[0]) % 95
            new_index = mult_index
            decrypted_char = self.alfabet[new_index]
            decrypted_message += decrypted_char
        return decrypted_message

    def generate_keys(self):
        sender_add_key = random.randint(0, 95)
        receiver_add_key = 95 - sender_add_key
        sender_mult_key = random.randint(0, 95)
        receiver_mult_key = crypto_utils.modular_inverse(sender_mult_key, 95)
        while not receiver_mult_key:
            sender_mult_key = random.randint(0, 95)
            receiver_mult_key = crypto_utils.modular_inverse(sender_mult_key, 95)
        return [(sender_mult_key, sender_add_key), (receiver_mult_key, receiver_add_key)]

    def possible_keys(self):
        return list(range(95))

    def verify(self, keys, message):
        crypted_message = self.encode(keys[0], message)
        decrypted_message = self.decode(keys[1], crypted_message)
        return message == decrypted_message


# ****************UNBREAKABLE_CIPHER****************
class Unbreakable(Cipher):
    def __init__(self):
        Cipher.__init__(self)
        file = open("english_words.txt", 'r')
        self.english_words = {}
        key = 0
        for line in file:
            self.english_words[key] = line.strip()
            key += 1
        file.close()

    def encode(self, key, message):
        crypted_message = ""
        for i in range(len(message)):
            char = key[i % len(key)]
            key_index = self.alfabet.index(char)
            new_index = (self.alfabet.index(message[i]) + key_index) % 95
            crypted_char = self.alfabet[new_index]
            crypted_message += crypted_char
        return crypted_message

    def decode(self, key, message):
        decrypted_message = ""
        for i in range(len(message)):
            char = key[i % len(key)]
            key_index = self.alfabet.index(char)
            new_index = (self.alfabet.index(message[i]) + key_index) % 95
            decrypted_char = self.alfabet[new_index]
            decrypted_message += decrypted_char
        return decrypted_message


    def generate_keys(self):
        sender_key = input("Velg nøkkelord (må være et ord fra den engelske ordboka): ")
        if sender_key == "default":
            sender_key = self.english_words[random.randint(0, len(self.english_words) - 1)]
        else:
            while not self.isValidKey(sender_key):
                sender_key = input("Ikke gyldig nøkkelord. Prøv på nytt:")
        print("Nøkkelordet '" + sender_key + "' var gyldig.")
        receiver_key = ""
        for char in sender_key:
            new_index = (95 - self.alfabet.index(char)) % 95
            receiver_key += self.alfabet[new_index]
        return [sender_key, receiver_key]

    def isValidKey(self, key):
        for t in self.english_words:
            if self.english_words[t] == key:
                return True
        return False

    def possible_keys(self):
        return self.english_words

    def verify(self, keys, message):
        crypted_message = self.encode(keys[0], message)
        decrypted_message = self.decode(keys[1], crypted_message)
        return message == decrypted_message



# ****************RSA_CIPHER****************
class RSA(Cipher):
    def __init__(self):
        Cipher.__init__(self)

    def encode(self, key, message):
        numbers = crypto_utils.blocks_from_text(message, 2)
        crypted_numbers = []
        for number in numbers:
            crypted_number = pow(number, key[1], key[0])
            crypted_numbers.append(crypted_number)
        return crypted_numbers

    def decode(self, key, message):
        decrypted_numbers = []
        for number in message:
            decrypted_number = pow(number, key[1], key[0])
            decrypted_numbers.append(decrypted_number)
        decrypted_text = crypto_utils.text_from_blocks(decrypted_numbers, 8)
        return decrypted_text

    def generate_keys(self):
        p = crypto_utils.generate_random_prime(8)
        q = -1
        while q == p or q == -1:
            q = crypto_utils.generate_random_prime(8)
        n = p*q
        o = (p - 1)*(q - 1)
        e = random.randint(3, o - 1)
        d = crypto_utils.modular_inverse(e, o)
        while not d:
            p = crypto_utils.generate_random_prime(8)
            q = -1
            while q == p or q == -1:
                q = crypto_utils.generate_random_prime(8)
            n = p * q
            o = (p - 1) * (q - 1)
            e = random.randint(3, o - 1)
            d = crypto_utils.modular_inverse(e, o)
        # (n,e) brukes av sender, (n,d) brukes av mottaker
        # (n,e) offentlig, (n,d) er hemmelig
        return [(n, e), (n, d)]

    def verify(self, keys, message):
        crypted_message = self.encode(keys[0], message)
        decrypted_message = self.decode(keys[1], crypted_message)
        return message == decrypted_message



# ****************SUPERKLASSE PERSON****************
# Har tre "personer": En som sender meldingen, en som mottar den, og en som forsøker å hacke meldingen
class Person:
    def __init__(self, cipher):
        self._key = None
        self._cipher = cipher

    def set_key(self, key):
        self._key = key

    def get_key(self):
        return self._key

    def set_cipher(self, cipher):
        self._cipher = cipher

    def get_cipher(self):
        return self._cipher

    def operate_cipher(self, message):
        return

# ****************SENDER_PERSON****************
class Sender(Person):
    def __init__(self, cipher):
        Person.__init__(self, cipher)

    #Sender sin operate_cipher skal kryptere meldingen
    def operate_cipher(self, message):
        return self.get_cipher().encode(self.get_key(), message)

# ****************RECEIVER_PERSON****************
class Receiver(Person):
    def __init__(self, cipher):
        Person.__init__(self, cipher)

    #Receiver sin operate_cipher skal dekryptere meldingen
    def operate_cipher(self, message):
        return self.get_cipher().decode(self.get_key(), message)


# ****************HACKER_PERSON****************
class Hacker(Receiver):
    def __init__(self, cipher = None):
        Receiver.__init__(self, cipher)
        file = open("english_words.txt", 'r')
        read = file.read()
        self.english_words = set(read.split('\n'))
        file.close()


    def hack_text(self, cr_text, cipher):
        self.set_cipher(cipher)

        # Samme metode kan brukes for caesar og multiplicative
        if isinstance(cipher, Caesar) or isinstance(cipher, Multiplicative):
            return self.brute_force_decode(cr_text)

        # For affine må metoden endres noe, da den tar ikke tar inn ett men to tall (tuppel) som nøkkel
        # Her må derfor alle kombinasjoner av både multiplikasjons-faktoren og addisjons-faktoren testes
        # Vi får derfor et dobbel for-løkke som begge itererer over de mulige nøklene til affine
        elif isinstance(cipher, Affine):
            return self.brute_force_decode_affine(cr_text)

        # For unbreakable må jeg prøve å dekryptere meldingen med dekrypteringsordet til hvert av ordene i den engelske ordlista
        # Dette skal fungere da jeg har gitt som krav til en unbreakbale-sender at nøkkelordet må være i ordlisten
        elif isinstance(cipher, Unbreakable):
            return self.brute_force_decode_unbreakable(cr_text)

    def brute_force_decode(self, cr_text):
        best_text = ""
        most_number_of_english_words = 0
        for key in self.get_cipher().possible_keys():
            self.set_key(key)
            dcr_text = self.operate_cipher(cr_text)
            dcr_words = dcr_text.split()
            number_of_english_words = 0
            for word in dcr_words:
                if word in self.english_words:
                    number_of_english_words += 1
            if number_of_english_words > most_number_of_english_words:
                best_text = ''.join(word for word in dcr_text)
                most_number_of_english_words = number_of_english_words
        return best_text

    def brute_force_decode_affine(self, cr_text):
        best_text = ""
        most_number_of_english_words = 0
        for key1 in self.get_cipher().possible_keys():
            for key2 in self.get_cipher().possible_keys():
                self.set_key((key1, key2))
                dcr_text = self.operate_cipher(cr_text)
                dcr_words = dcr_text.split()
                number_of_english_words = 0
                for word in dcr_words:
                    if word in self.english_words:
                        number_of_english_words += 1
                if number_of_english_words > most_number_of_english_words:
                    best_text = ''.join(word for word in dcr_text)
                    most_number_of_english_words = number_of_english_words
        return best_text


    def brute_force_decode_unbreakable(self, cr_text):
        best_text = ""
        most_number_of_english_words = 0
        keys = self.get_cipher().possible_keys()
        for key in keys:
            word = keys[key]
            dcr_key = self.generate_unbreakable_dcrkey(word)
            self.set_key(dcr_key)
            dcr_text = self.operate_cipher(cr_text)
            dcr_words = dcr_text.split()
            number_of_english_words = 0
            for word in dcr_words:
                if word in self.english_words:
                    number_of_english_words += 1
            if number_of_english_words > most_number_of_english_words:
                best_text = ''.join(word for word in dcr_text)
                most_number_of_english_words = number_of_english_words
        return best_text

    def generate_unbreakable_dcrkey(self, sender_key):
        receiver_key = ""
        for char in sender_key:
            new_index = (95 - self.get_cipher().alfabet.index(char)) % 95
            receiver_key += self.get_cipher().alfabet[new_index]
        return receiver_key


# ****************TESTING****************
def caesar():
    cipher = Caesar()
    keys = cipher.generate_keys()
    print("----------------SENDER_CAESAR---------------------")
    sender = Sender(cipher)
    sender.set_key(keys[0])
    print("Sender har nøkkel: " + str(sender.get_key()))
    melding = "Hei, hva skjer? hilsen Axel"
    crm = sender.operate_cipher(melding)
    print("Sender følgende melding: " + melding)
    print("Kryptert melding: "+ crm)
    print("----------------RECEIVER_CAESAR-------------------")
    receiver = Receiver(cipher)
    receiver.set_key(keys[1])
    print("Receiver har nøkkel: " + str(receiver.get_key()))
    print("Receiver har mottat følgende kryptert melding: " + crm)
    mottatt_melding = receiver.operate_cipher(crm)
    print("Dekryptert melding: " + mottatt_melding)
    print("Er kryptering/dekryptering vertifisert? " + str(cipher.verify(keys, melding)))
    print()

def multi():
    cipher = Multiplicative()
    keys = cipher.generate_keys()
    print("----------------SENDER_MULTIPLICATIVE---------------------")
    sender = Sender(cipher)
    sender.set_key(keys[0])
    print("Sender har nøkkel: " + str(sender.get_key()))
    melding = "Testing testing 123--;''#&?"
    crm = sender.operate_cipher(melding)
    print("Sender følgende melding: " + melding)
    print("Kryptert melding: " + crm)
    print("----------------RECEIVER_MULTIPLICATIVE-------------------")
    receiver = Receiver(cipher)
    receiver.set_key(keys[1])
    print("Receiver har nøkkel: " + str(receiver.get_key()))
    print("Receiver har mottat følgende kryptert melding: " + crm)
    mottatt_melding = receiver.operate_cipher(crm)
    print("Dekryptert melding: " + mottatt_melding)
    print("Er kryptering/dekryptering verifisert? " + str(cipher.verify(keys, melding)))
    print()

def affine():
    cipher = Affine()
    keys = cipher.generate_keys()
    print("----------------SENDER_AFFINE---------------------")
    sender = Sender(cipher)
    sender.set_key(keys[0])
    print("Sender har nøkkel: " + str(sender.get_key()))
    melding = "heihei, dette er Simen! skjer?"
    crm = sender.operate_cipher(melding)
    print("Sender følgende melding: " + melding)
    print("Kryptert melding: " + crm)
    print("----------------RECEIVER_AFFINE-------------------")
    receiver = Receiver(cipher)
    receiver.set_key(keys[1])
    print("Receiver har nøkkel: " + str(receiver.get_key()))
    print("Receiver har mottat følgende kryptert melding: " + crm)
    mottatt_melding = receiver.operate_cipher(crm)
    print("Dekryptert melding: " + mottatt_melding)
    print("Er kryptering/dekryptering verifisert? " + str(cipher.verify(keys, melding)))
    print()

def unbreakable():
    cipher = Unbreakable()
    print("----------------SENDER_UNBREAKABLE---------------------")
    keys = cipher.generate_keys()
    print(keys)
    sender = Sender(cipher)
    sender.set_key(keys[0])
    print("Sender har nøkkel: " + str(sender.get_key()))
    melding = "IM PICKLE RICK!!!!!"
    crm = sender.operate_cipher(melding)
    print("Sender følgende melding: " + melding)
    print("Kryptert melding: " + crm)
    print("----------------RECEIVER_UNBREAKABLE-------------------")
    receiver = Receiver(cipher)
    receiver.set_key(keys[1])
    print("Receiver har nøkkel: " + str(receiver.get_key()))
    print("Receiver har mottat følgende kryptert melding: " + crm)
    mottatt_melding = receiver.operate_cipher(crm)
    print("Dekryptert melding: " + mottatt_melding)
    print("Er kryptering/dekryptering verifisert? " + str(cipher.verify(keys, melding)))
    print()

def rsa():
    cipher = RSA()
    print("----------------SENDER_RSA---------------------")
    keys = cipher.generate_keys()
    sender = Sender(cipher)
    sender.set_key(keys[0])
    print("Sender har nøkkel: " + str(sender.get_key()))
    melding = "Dette ER en TEST!????"
    crm = sender.operate_cipher(melding)
    print("Sender følgende melding: " + melding)
    print("Kryptert melding: " + str(crm))
    print("----------------RECEIVER_RSA-------------------")
    receiver = Receiver(cipher)
    receiver.set_key(keys[1])
    print("Receiver har nøkkel: " + str(receiver.get_key()))
    print("Receiver har mottat følgende kryptert melding: " + str(crm))
    mottatt_melding = receiver.operate_cipher(crm)
    print("Dekryptert melding: " + mottatt_melding)
    print("Er kryptering/dekryptering verifisert? " + str(cipher.verify(keys, melding)))
    print()

def hacker():
    print("----------------HACKER-----------------------")
    hacker = Hacker()
    cipher = Unbreakable()
    sender = Sender(cipher)
    keys = cipher.generate_keys()
    sender.set_key(keys[0])
    melding = "what is going on now hello hello"
    cr_text = sender.operate_cipher(melding)
    print("Sender sender følgende melding: " + melding)
    hacked_text = hacker.hack_text(cr_text, cipher)
    print("Hacker hacket meldingen og fikk følgende melding: " + hacked_text)



def main():
    caesar()
    multi()
    affine()
    unbreakable()
    rsa()
    hacker()

main()