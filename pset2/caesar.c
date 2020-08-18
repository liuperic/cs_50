#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>


const int upper_idx = 65;
const int lower_idx = 97;

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    // validate commandline key as numbers
    for (int i = 0; i < strlen(argv[1]); i++)
    {
        if (argv[1][i] < '0' || argv[1][i] > '9') 
        {
            printf("Usage: ./caesar key\n");
            return 1;
        }
    }
    int key = atoi(argv[1]);

    string text = get_string("plaintext: ");    // prompt user for plain-text


    for (int i = 0; i < strlen(text); i++)
    {
        if (isupper(text[i]))
        {
            int index = text[i] - upper_idx;   // convert string to alphabet index
            int new_index = (index + key) % 26;     // implement key for new index
            text[i] = new_index + upper_idx;    // update array to new char
        }
        else if (islower(text[i])) 
        {
            int index = text[i] - lower_idx;   // convert string to alphabet index
            int new_index = (index + key) % 26;     // implement key for new index
            text[i] = new_index + lower_idx;    // update array to new char
        }
        else {}
    }
    
    printf("ciphertext: %s\n", text);

    return 0;
}
