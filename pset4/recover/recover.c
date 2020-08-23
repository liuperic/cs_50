#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>

#define BLOCK_SIZE 512

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }

    FILE *f = fopen("card.raw", "r'");
    if (f == NULL)
    {
        printf("File could not be opened\n");
        return 2;
    }

    typedef uint8_t  BYTE;
    BYTE buffer[512];

    FILE *outptr = NULL;
    int count = 0;
    char jpeg_name[8];

    while (true)
    {
        size_t read_block = fread(buffer, sizeof(BYTE), BLOCK_SIZE, f);     // start reading from file

        if (read_block == 0 && feof(f))     // break when EOF
        {
            break;
        }

        bool jpeg_header = buffer[0] == 0xff && buffer[1] == 0xd8
                           && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0;     // valid jpeg header check

        if (jpeg_header && outptr != NULL)      // if valid jpeg; close file
        {
            fclose(outptr);
            count++;
        }

        if (jpeg_header)    // open file and write
        {
            sprintf(jpeg_name, "%03i.jpg", count);
            outptr = fopen(jpeg_name, "w");
        }

        if (outptr != NULL)     // write whenever file is open
        {
            fwrite(buffer, sizeof(BYTE), read_block, outptr);
        }

    }

    fclose(outptr);
    fclose(f);

    return 0;
}
