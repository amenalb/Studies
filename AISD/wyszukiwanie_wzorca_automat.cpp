
#include <iostream>
#include<string>
using namespace std;

int policzLitery(string s)
{
    int l = 0;
    int tab[256];
    for (int i = 1; i <= 255; i++)
    {
        tab[i] = 0;
    }
    for (int i = 0; i < s.size(); i++)
    {
        tab[i]++;
    }
    for (int i = 1; i <= 255; i++)
    {
        if (tab[i] != 0)
            l++;
    }
    return l;
}
int main()
{
    string klucz;
    string napis;
    int l = policzLitery(klucz);//kolumny


    int** tab = new int* [1 + klucz.size()];//rzedy
    for (int i = 0; i <= klucz.size(); i++)
    {
        tab[i] = new int[l];
    }
    for (int i = 0; i <= klucz.size(); i++)
    {
        for (int j = 0; i <= l; j++)
        {

        }
    }
    for (int i = 0; i <= klucz.size(); i++)
        delete[] tab;
    return 0;



}
