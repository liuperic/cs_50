#include <stdio.h>
#include <math.h>
#include <cs50.h>
#include <string.h>

int SumAllDigits(int number);
int SumProduct(long long credit);
int SumLastDigits(long long credit);
bool Valid(int number);
int GetDigits(long long credit);
string StartingNumberCheck(long long credit);
void CreditMerchant(long long credit);

// Determining what credit card and authenticating as real or fake
int main()
{
    // Prompt user for credit card number
    long long number;
    do
    {
        number = get_long_long("Number :");
    }
    while (number < 0);

    CreditMerchant(number);

    /*
        Leaving these as commented out in case want to test each individual function
        int luhn_sum = SumProduct(number) + SumLastDigits(number);
        printf("GetDigits: %i\n", GetDigits(number));
        printf("Valid: %s\n", Valid(luhn_sum) ? "true" : "false");
        printf("SumProduct(number): %i\n", SumProduct(number));
        printf("SumLastDigits(number): %i\n", SumLastDigits(number));
        printf("luhn_sum: %i\n", luhn_sum);
        printf("SumAllDigits: %i\n", SumAllDigits(14));
        printf("Starting Number Check: %s\n", StartingNumberCheck(number));
    */
}


// returns sum of all individual digits
int SumAllDigits(int number)
{
    int digit = 0;
    int sum = 0;

    while (number > 0)
    {
        digit = number % 10;
        sum += digit;
        number /= 10;
    }
    return sum;
}

// gets sum of products' digits of every other digit multiplied by 2
// from starting from second to last digit
int SumProduct(long long credit)
{
    int iteration = 1;
    int sum = 0;
    int digit = 0;

    while (credit > 0)
    {
        credit /= pow(10, iteration);
        digit = (credit % 10) * 2;      // get second to last digit * 2
        if (iteration == 1)     // iteration = 1 only on initial iteration
        {
            iteration = 2;      // iteration = 2 to get to every other digit after
        }
        sum += SumAllDigits(digit);
    }
    return sum;
}

// Sum of every other digit beginning with last digit
int SumLastDigits(long long credit)
{
    int iteration = 0;
    int sum = 0;
    int digit = 0;

    while (credit > 0)
    {
        credit /= pow(10, iteration);
        digit = (credit % 10);      // get last digit
        sum += digit;
        if (iteration == 0)     // iteration = 0 only on initial iteration
        {
            iteration = 2;      // iteration = 2 to get to every other digit after
        }
    }
    return sum;
}

// checks if last digit is 0 (valid credit card)
bool Valid(int number)
{
    return number % 10 == 0;
}

int GetDigits(long long credit)
{
    int counter = 0;
    while (credit > 0)
    {
        credit /= 10;
        counter ++;
    }
    return counter;
}

string StartingNumberCheck(long long credit)
{
    int start_number = 0;
    string vendor;
    // while credit is 3 digits or more
    while (credit > 99)
    {
        credit /= 10;
    }
    // AMEX starting digit check
    if (credit == 34 || credit == 37)
    {
        return vendor = "AMEX";
    }
    // Mastercard starting digit check
    else if (credit == 51 || credit == 52 || credit == 53 || credit == 54 || credit == 55)
    {
        return vendor = "MASTERCARD";
    }
    else
    {
        credit /= 10;
        if (credit == 4)
        {
            return vendor = "VISA";
        }
        else
        {
            return vendor = "NONE";
        }
    }
    return vendor = "NONE";
}

void CreditMerchant(long long credit)
{
    int luhn_sum = SumProduct(credit) + SumLastDigits(credit);

    // Visa check - 13 or 16 digits AND valid luhn's #
    if ((GetDigits(credit) == 13 || GetDigits(credit) == 16)
        && Valid(luhn_sum) && strcmp(StartingNumberCheck(credit), "VISA") == 0)
    {
        printf("VISA\n");
    }
    // Amex check
    else if (GetDigits(credit) == 15 && Valid(luhn_sum) && strcmp(StartingNumberCheck(credit), "AMEX") == 0)
    {
        printf("AMEX\n");
    }
    // Mastercard check
    else if (GetDigits(credit) == 16 && Valid(luhn_sum) && strcmp(StartingNumberCheck(credit), "MASTERCARD") == 0)
    {
        printf("MASTERCARD\n");
    }
    else
    {
        printf("INVALID\n");
    }
}
