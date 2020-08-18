#include <cs50.h>
#include <math.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int count_letters(string text);     // returns number of letters
int count_words(string text);       // returns number of words
int count_sentences(string text);   // returns number of sentences
double coleman_index(string text);     // returns Coleman-Liau grade level index
double letters_conversion(int letters, int words);       // letters per 100 words conversion
double sentences_conversion(int words, int sentences);    // sentences per 100 words conversion


int main(void)
{
    string text = get_string("Text: ");

    int grade = round(coleman_index(text));    // returns coleman-liau grade level index
    if (grade >= 16)
    {
        printf("Grade 16+\n");
    }
    else if (grade < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %i\n", grade);
    }

    return 0;
}

int count_letters(string text)
{
    int letter_counter = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        if ((text[i] >= 'a' && 'z' >= text[i]) || (text[i] >= 'A' && 'Z' >= text[i]))
        {
            letter_counter++;
        }
    }
    return letter_counter;
}

int count_words(string text)
{
    int words_counter = 1;      // assumes there is always at least one word

    for (int i = 0; i < strlen(text); i++)
    {
        if (text[i] == 32)
        {
            words_counter++;
        }
    }
    return words_counter;
}

int count_sentences(string text)
{
    int sentences_counter = 0;

    for (int i = 0; i < strlen(text); i++)
    {
        if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            sentences_counter++;
        }
    }
    return sentences_counter;
}

// converts to letters per 100 words
double letters_conversion(int letters, int words)
{
    double conversion = (100.0 * letters) / words;   // formula to convert
    return conversion;
}

// converts to sentences per 100 words
double sentences_conversion(int words, int sentences)
{
    double conversion = (100.0 * sentences) / words;   // formula to convert
    return conversion;
}

// returns grade level using index = 0.0588 * L - 0.296 * S - 15.8
double coleman_index(string text)
{
    int letters = count_letters(text);   // number of letters in text
    int words = count_words(text);       // number of words in text
    int sentences = count_sentences(text);       // number of sentences in text

    double letters_convert = letters_conversion(letters, words);
    double sentences_convert = sentences_conversion(words, sentences);

    double unrounded_grade = 0.0588  * letters_convert - 0.296 * sentences_convert - 15.8;
    return unrounded_grade;
}
