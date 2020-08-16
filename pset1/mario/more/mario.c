#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int height;

    // Prompts user for height of pyramid between 1 and 8
    do
    {
        height = get_int("Height of pyramid: ");
    }
    while (height < 1 || height > 8);

    // For loop to print adjacent pyramids with gap of 2 in between
    for (int row = 0; row < height; row++)
    {
        for (int spaces = 0; spaces + row < height - 1; spaces++)
        {
            printf(" ");
        }
        for (int pyramid1 = 0; pyramid1 <= row; pyramid1++)
        {
            printf("#");
        }
        for (int gap = 0; gap < 1; gap++)
        {
            printf("  ");
        }
        for (int pyramid2 = 0; pyramid2 <= row; pyramid2++)
        {
            printf("#");
        }
        printf("\n");
    }
}
