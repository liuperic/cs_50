// Implements a dictionary's functionality
#include <ctype.h>
#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#include <strings.h>
#include <stdlib.h>
#include "dictionary.h"


// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Word counter
unsigned long word_count = 0;

// Hash table
node *hashtable[HASHTABLE_SIZE];

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    // TODO
    int length = strlen(word);
    char copy[length + 1];

    for (int i = 0; i < length; i++)
    {
        copy[i] = tolower(word[i]);
    }

    // End string with null terminator
    copy[length] = '\0';

    // Node navigating linked list
    node *cursor = hashtable[hash(copy)];
    while (cursor != NULL)
    {
        if (strcasecmp(cursor->word, word) == 0)
        {
            return true;
        }
        cursor = cursor->next;
    }
    return false;
}

// Hashes word to a number
// Hash function by Dan Bernstein
unsigned long hash(const char *word)
{
    // TODO
    const char *_word = word;
    unsigned long hash = 5381;
    int c;

    while ((c = *_word++))
    {
        hash = ((hash << 5) + hash) + c; /* hash * 33 + c */
    }

    return hash % HASHTABLE_SIZE;
}


// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // TODO
    FILE *file = fopen(dictionary, "r");
    if (!file)
    {
        return false;
    }

    char word[LENGTH];
    while (fscanf(file, "%s", word) != EOF)
    {
        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
            unload();
            return false;
        }

        strcpy(n->word, word);
        unsigned long key = hash(n->word);
        n->next = hashtable[key];
        hashtable[key] = n;

        word_count++;
    }

    fclose(file);

    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    return word_count;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    // TODO
    for (int i = 0; i < HASHTABLE_SIZE; i++)
    {
        node *cursor = hashtable[i];
        // Free linked-lists
        while (cursor != NULL)
        {
            node *temp = cursor;
            cursor = cursor->next;
            free(temp);
        }
    }
    return true;
}
