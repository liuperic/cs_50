from cs50 import get_string


# Returns total number of letters in string
def count_letters(text):
    letters = 0
    for i in text:
        if i.isalpha():
            letters += 1
    return letters


# Returns total number of words in string
def count_words(text):
    return text.count(' ') + 1


# Returns total number of sentences in string
def count_sentences(text):
    num_sentences = text.count('.') + text.count('?') + text.count('!')
    return num_sentences


# returns coleman-liau index in rounded integer form
def coleman_index(letters, sentences):
    return round(0.0588 * letters - 0.296 * sentences - 15.8)


def main():
    text = get_string('Text: ')

    total_letters = count_letters(text)
    total_words = count_words(text)
    total_sentences = count_sentences(text)

    letters_per_hundred = 100 * total_letters / total_words     # Converts to letters per hundred words
    sentences_per_hundred = 100 * total_sentences / total_words     # Converts to sentences per hundred words
    index = coleman_index(letters_per_hundred, sentences_per_hundred)

    if index < 1:
        print('Before Grade 1')
    elif index >= 16:
        print('Grade 16+')
    else:
        print('Grade ' + str(index))


if __name__ == "__main__":
    main()


