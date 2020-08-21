#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int red = image[i][j].rgbtRed;
            int green = image[i][j].rgbtGreen;
            int blue = image[i][j].rgbtBlue;

            int average = round((red + green + blue) / 3.0);

            image[i][j].rgbtRed = average;
            image[i][j].rgbtGreen = average;
            image[i][j].rgbtBlue = average;
        }
    }

    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int old_red = image[i][j].rgbtRed;
            int old_green = image[i][j].rgbtGreen;
            int old_blue = image[i][j].rgbtBlue;

            int new_red = round(0.393 * old_red + 0.769 * old_green + 0.189 * old_blue);
            int new_green = round(0.349 * old_red + 0.686 * old_green + 0.168 * old_blue);
            int new_blue = round(0.272 * old_red + 0.534 * old_green + 0.131 * old_blue);

            if (new_red > 255)
            {
                new_red = 255;
            }
            if (new_green > 255)
            {
                new_green = 255;
            }
            if (new_blue > 255)
            {
                new_blue = 255;
            }

            image[i][j].rgbtRed = new_red;
            image[i][j].rgbtGreen = new_green;
            image[i][j].rgbtBlue = new_blue;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j++)
        {
            int temp_red = image[i][j].rgbtRed;
            int temp_green = image[i][j].rgbtGreen;
            int temp_blue = image[i][j].rgbtBlue;

            image[i][j].rgbtRed = image[i][width - j - 1].rgbtRed;  // reflect red in elements in each row
            image[i][j].rgbtGreen = image[i][width - j - 1].rgbtGreen;  // reflect green in elements in each row
            image[i][j].rgbtBlue = image[i][width - j - 1].rgbtBlue;    // reflect blue in elements in each row

            image[i][width - j - 1].rgbtRed = temp_red;
            image[i][width - j - 1].rgbtGreen = temp_green;
            image[i][width - j - 1].rgbtBlue = temp_blue;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp[height][width];

    for (int i = 0; i < height; i++)    // iterate through rows
    {
        for (int j = 0; j < width; j++)     // iterate through columns
        {
            int red = 0;
            int green = 0;
            int blue = 0;
            double count = 0.0;

            for (int k = -1; k < 2; k++)    // iterate through columns +/- 1 away from current pixel
            {
                for (int l = -1; l < 2; l++)    // iterate through rows +/- 1 away from current pixel
                {
                    if (j + k >= 0 && j + k < width &&
                        i + l >= 0 && i + l < height)
                    {
                        red += image[i + l][j + k].rgbtRed;
                        green += image[i + l][j + k].rgbtGreen;
                        blue += image[i + l][j + k].rgbtBlue;
                        count++;
                    }
                }
            }
            temp[i][j].rgbtRed = round(red / count);
            temp[i][j].rgbtGreen = round(green / count);
            temp[i][j].rgbtBlue = round(blue / count);
        }
    }

    for (int i = 0; i < height; i++)    // iterate through rows
    {
        for (int j = 0; j < width; j++)     // iterate through columns
        {
            image[i][j].rgbtRed = temp[i][j].rgbtRed;       // update colors with temp storage
            image[i][j].rgbtGreen = temp[i][j].rgbtGreen;
            image[i][j].rgbtBlue = temp[i][j].rgbtBlue;
        }
    }

    return;
}
