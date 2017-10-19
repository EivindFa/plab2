import os
import re
from operator import itemgetter
import math

# -----------------------READER-KLASSE-----------------------------------------
# Reader-klassen tar inn stien til anmeldelsene + liste over filnavnene til anmeldelsene
# Disse tas inn som en tuppel på formen: (path til pos/neg reviews, listen over pos/neg reviews(filnavn)
# Tar også inn en reader-type ("training_data" eller "test_data")
# Training_data-typen må analysere en rekke ting, mens test_data-typen ikke trenger dette
class Reader:
    def __init__(self, pos_path_and_reviews, neg_path_and_reviews, reader_type):
        self.pos_path = pos_path_and_reviews[0] # Pathen til positive reviews
        self.pos_review_list = pos_path_and_reviews[1] # Pathen til negative reviews
        self.neg_path = neg_path_and_reviews[0] # Liste over alle de positive filnavnene
        self.neg_review_list = neg_path_and_reviews[1] # Liste over alle de negative filnavnene

        # Antall positive og negative reviews
        self.number_of_pos_reviews = len(self.pos_review_list)
        self.number_of_neg_reviews = len(self.neg_review_list)
        self.stop_words = self.get_stop_words()
        self.n = 3

        if reader_type == "training_data":
            self.pos_word_count = self.get_word_count("pos")
            self.neg_word_count = self.get_word_count("neg")
            self.top_pos_words = self.get_most_used_words("pos")
            self.top_neg_words = self.get_most_used_words("neg")
            self.pos_informative_words = self.most_informative_words("pos")
            self.neg_informative_words = self.most_informative_words("neg")


    def read_from_file(self, filepath):
        file = open(filepath, encoding='utf-8')
        r = file.read()
        review = re.sub("[.,#+()-:?!&<´>/;\"'^*]", '', r.lower().replace("br", "").replace(" br", "")).split()
        file.close()
        for i in range(len(review) - self.n + 1):
            if self.n == 2:
                review.append(review[i] + "_" + review[i+1])
            elif self.n == 3:
                review.append(review[i] + "_" + review[i+1])
                review.append(review[i] + "_" + review[i+1] + "_" + review[i+2])
        #Fjerner duplikater
        review = set(review)
        # Fjerner stopord
        self.remove_stop_words(review)
        return review

    def get_word_count(self, type):
        word_counter = {}
        if type == "pos":
            path = self.pos_path
            review_list = self.pos_review_list
        else:
            path = self.neg_path
            review_list = self.neg_review_list
        # Går gjennom hver fil i oppgitte review-typen (pos eller neg)
        for file in review_list:
            # Leser av og samler alle ordene (maks 1 forekomst) i et set
            review = self.read_from_file(path + file)
            # Går gjennom settet med ord og plusser på 1 forekomst for hvert ord
            for word in review:
                if word in word_counter:
                    word_counter[word] += 1
                else:
                    word_counter[word] = 1
        return word_counter

    def get_most_used_words(self, type):
        if type == "pos":
            word_counter = self.pos_word_count
        else:
            word_counter = self.neg_word_count
        return self.sort_dict(word_counter, 25)

    def sort_dict(self, dicti, end):
        # Sorterer etter value i dict, gir liste med tupler
        most_common_words = sorted(dicti.items(), key=itemgetter(1))
        most_common_words.reverse()
        most_common_words = most_common_words[:end]
        # Lager dict på formen {word: count, ...}
        # Vil ha dict fremfor liste med tupler, pga. senere søk
        return dict(most_common_words)

    def most_informative_words(self, type):
        # Sjekker om jeg skal finne informasjonsverdien til ord fra positive eller negative anmeldelser
        if type == "pos":
            this = self.pos_word_count
            other = self.neg_word_count
        elif type == "neg":
            this = self.neg_word_count
            other = self.pos_word_count

        most_informative_words = {}
        for word in this:
            this_word_count = this[word]
            if word in other:
                other_word_count = other[word]
            else:
                other_word_count = 0
            # Pruner ordet, dvs. fjerner ordet dersom det ikke inngår i minst 0.15 % av anmeldelsene
            if self.valid_prune_value(this_word_count):
                informativ_value = this_word_count / (this_word_count + other_word_count)
                most_informative_words[word] = informativ_value-0.00001
        # Sorterer dict, tar kun med 1/8 av ordene
        return self.sort_dict(most_informative_words, len(most_informative_words)//8)

    def valid_prune_value(self, this_word_count):
        return this_word_count/(self.number_of_pos_reviews + self.number_of_neg_reviews) > 0.0015

    def get_popularity(self, word, top_words, number_of_reviews):
        return top_words[word] / number_of_reviews

    def remove_stop_words(self, words):
        for stop_word in self.stop_words:
            if stop_word in words:
                words.remove(stop_word)
        return words

    def get_stop_words(self):
        file = open("data\data\stop_words.txt", 'r')
        r = file.read()
        words = r.split()
        file.close()
        return words

# -----------------------CLASIFICATION-KLASSE-----------------------------------------
# Klassen skal analysere en anmeldelse og plassere det i positiv eller negativ "bunke"
# Henter data fra test_data og gjør sammenligner med data fra training_data
class Clasification():
    def __init__(self, training_data, test_data):
        self.training_data = training_data
        self.test_data = test_data

    def read_from_file(self, filepath):
        return self.training_data.read_from_file(filepath)

    def is_positive_review(self, review):
        pos_value = 0
        neg_value = 0
        pos_info_words = self.training_data.pos_informative_words
        neg_info_words = self.training_data.neg_informative_words
        for word in review:
            pos_info_has_word = word in pos_info_words
            neg_info_has_word = word in neg_info_words
            if pos_info_has_word and neg_info_has_word:
                if pos_info_words[word] > neg_info_words[word]:
                    pos_value += math.log2(pos_info_words[word])
                else:
                    neg_value += math.log2(neg_info_words[word])
            elif pos_info_has_word and not neg_info_has_word:
                pos_value += math.log2(pos_info_words[word])
                neg_value += math.log2(0.03)
            elif neg_info_has_word and not pos_info_has_word:
                neg_value += math.log2(neg_info_words[word])
                pos_value += math.log2(0.03)

        return pos_value > neg_value

#---------------------------TESTFUNKSJONER----------------------------
def analyze_training_set(training_data):
    print("---------------------------------DEL 1------------------------------------")
    # DEL 1 - Lag funksjonalitet for å lese et dokument i trenings-settet fra fil
    pos_first_review = training_data.pos_review_list[0]
    neg_first_review = training_data.neg_review_list[0]
    pos_review = training_data.read_from_file(training_data.pos_path + pos_first_review)
    neg_review = training_data.read_from_file(training_data.neg_path + neg_first_review)
    print("List of words from first positive review:")
    print(pos_review)
    print("List of words from first negative review:")
    print(neg_review)

    print("------------------------------DEL 2/DEL 3------------------------------------")
    # DEL 2 - Utvid koden til å lese alle filene i trenings-settet. Analyser representasjonen
    # så du finner de 25 mest populære ordene for hhv. positive og negative anmeldelser.
    # Popularitet = antall pos/neg anmeldelser med <ord> / antall pos/neg anmeldelser totalt
    # Utvid systemet til å fjerne alle stopp-ord
    print(training_data.top_pos_words)
    print(training_data.top_neg_words)
    word = "movie"
    print(word + " has popularity of " + str(training_data.get_popularity(word, training_data.top_pos_words,
                                                                          training_data.number_of_pos_reviews)) + " in the positive reviews")
    print(word + " has popularity of " + str(training_data.get_popularity(word, training_data.top_neg_words,
                                                                          training_data.number_of_neg_reviews)) + " in the negative reviews")

    print("---------------------------------DEL 4/ DEL 5/ DEL 6------------------------------------")
    # Utvid systemet til å finne informasjonsverdien av ord.
    # Skriv ut de mest informative ordene for positive og negative anmeldelser
    # Prun vekk ord som ikke forekommer i minst 0.15 % av alle anmeldelsene
    # Implementer n-grams
    print("Most informativ words for the positive reviews:")
    print(training_data.pos_informative_words)
    print("Most informativ words for the negative reviews:")
    print(training_data.neg_informative_words)


def analyze_test_set(training_data, test_data):
    print("-----------------------------DEL 7------------------------------------------")
    c = Clasification(training_data, test_data)
    print("Reading files...")
    pos_reviews = 0
    for file in test_data.pos_review_list:
        review = test_data.read_from_file(test_data.pos_path + file)
        if c.is_positive_review(review):
            pos_reviews += 1

    neg_reviews = 0
    for file in test_data.neg_review_list:
        review = test_data.read_from_file(test_data.neg_path + file)
        if not c.is_positive_review(review):
            neg_reviews += 1

    print("Out of a totalt of " + str(test_data.number_of_pos_reviews) + " positive reviews, " +
          str(pos_reviews) + " were analyzed to be positive")
    print("Out of a totalt of " + str(test_data.number_of_neg_reviews) + " negative reviews, " +
          str(neg_reviews) + " were analyzed to be negative")
    print("% correct: " + str(
        (pos_reviews + neg_reviews) / (test_data.number_of_pos_reviews + test_data.number_of_neg_reviews) * 100))

#-------------------------------------MAIN----------------------------------
def main():
    print("Reading files..")
    training_data = Reader(("data\data\\alle\\train\\pos\\", os.listdir("data\data\\alle\\train\\pos\\")),
                           ("data\data\\alle\\train\\neg\\", os.listdir("data\data\\alle\\train\\neg\\")), "training_data")
    analyze_training_set(training_data)

    test_data = Reader(("data\data\\alle\\test\\pos\\", os.listdir("data\data\\alle\\test\\pos\\")),
                       ("data\data\\alle\\test\\neg\\", os.listdir("data\data\\alle\\test\\neg\\")), "test_data")
    analyze_test_set(training_data, test_data)
    # Gir 87.5 % riktig

main()

