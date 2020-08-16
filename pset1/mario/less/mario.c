#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int height;

    // prompts user for height of pyramid between 1 and 8
    do
    {
        height = get_int("Positive integer height for pyramid: ");
    }
    while (height < 1 || height > 8);

    // For loops specifying number of hashes, spaces, and lines
    for (int line = 0; line < height; line++)
    {
        // For loop specifying number of spaces
        for (int spaces = 0; spaces + line < height - 1; spaces++)
        {
            printf(" ");
        }
        // For loop specifying number of hashes
        for (int hashes = 0; hashes <= line; hashes++)
        {
            printf("#");
        }
        printf("\n");
    }
}
