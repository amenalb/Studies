#include <iostream>

using namespace std;

struct node
{
    int val;
    node* next;
};
void show(node* H)
{
    cout << "H->";
    node* p = H;
    while (p != NULL)
    {
        cout << p->val << "->";
        p = p->next;
    }
    cout << "NULL" << endl;
}
void add(int x, node*& H)
{
    node* p = new node;
    p->val = x;
    p->next = H;
    H = p;
}


void split(node*& H, node*& H1, node*& H2)
{
    if (H != NULL)
    {
        node* p;
        while (H != NULL)
        {
            p = H;
            H = H->next;
            p->next = H1;
            H1 = p;
            if (H != NULL)
            {
                p = H;
                H = H->next;
                p->next = H2;
                H2 = p;
            }
        }
    }
}
void merge(node*& H, node*& H1, node*& H2)
{
    if (H1 != NULL && H2 != NULL)
    {
        H = NULL;
        node* pom1, pom2;
        pom1 = H1;
        pom2 = H2;
        while (H1 != NULL || H2 != NULL)
        {
            //mniejszy wstawiamy do h
        }
        //jak jakas lista sie konczy to przepinamy wsk
    }
}
void mergesort(node*& H)
{
    node* H1 = NULL;
    node* H2 = NULL;
    split(H, H1, H2);
    mergesort(H1);
    mergesort(H2);
    merge(H, H1, H2);

}

int main()
{
    node* H = NULL;
    node* H1 = NULL;
    node* H2 = NULL;
    add(6, H);
    add(2, H);
    add(3, H);
    add(-2, H);
    add(8, H);
    add(1, H);
    mergesort(H);
    split(H, H1, H2);
    show(H);
    show(H1);
    show(H2);


