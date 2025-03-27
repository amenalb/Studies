#include <iostream>
using namespace std;

struct nodeBST {
	int val;
	nodeBST* R;
	nodeBST* L;
	nodeBST* par;
};

void add(nodeBST*& root, int x, nodeBST* parent)
{
	if (root == NULL)
	{
		nodeBST* p = new nodeBST;
		p->val = x;
		p->R = NULL;
		p->L = NULL;
		p->par = parent;
		root = p;
	}
	else
		if (x >= root->val)//wiekszelub rowne na prawo
		{
			add(root->R, x, root);
		}
		else
		{
			add(root->L, x, root);//mniejsze  na lewo
		}
}

void show(nodeBST* root)
{
	if (root != NULL)
	{
		show(root->L);
		cout << root->val << " ";
		show(root->R);
	}
}

nodeBST* min(nodeBST* root)//wyszukiwanie poprzednika na lewym poddrzewie
{

	if (root->L == NULL)
	{
		return root;
	}
	min(root->L);

}
nodeBST* max(nodeBST* root)//wyszukiwanie nastepnika na prawym poddrzewie
{
	if (root->R == NULL)
	{
		return root;

	}
	max(root->R);
}


nodeBST* poprzednik(nodeBST* root)
{
	if (root->L)// max na lewym poddrzewie
	{
		return max(root->L);
	}
	if (root->par != NULL)//w gore
	{
		nodeBST* pom;//poprzednikiem bedzie pierwszy ojciec od prawego syna
		while (root->par)
		{
			pom = root->par;
			if (pom->R == root)
			{
				return root;
			}
			else
				root = root->par;
		}//jesli root zawsze jest lewym synem to nie ma poprzednika
	}
	return NULL;
}

nodeBST* nastepnik(nodeBST* root)
{

	if (root->R)
	{
		return min(root->R);
	}
	if (root->par != NULL)//w gore
	{
		nodeBST* pom;
		while (root->par)
		{
			pom = root->par;
			if (pom->L == root)
			{
				return root;
			}
			else
				root = root->par;
		}
	}
	return NULL;
}

nodeBST* find(nodeBST*& root, int x)
{
	if (root == NULL) {
		return nullptr;
	}

	if (x < root->val)
	{
		find(root->L, x);
	}
	else
		if (x > root->val)
		{
			find(root->R, x);
		}
	if (x == root->val)
	{
		return root;
	}
}
void usuwanie(nodeBST*& root, int x)
{
	if (root == NULL) {
		return;
	}

	if (x < root->val)
	{
		usuwanie(root->L, x);
	}
	else
		if (x > root->val)
		{
			usuwanie(root->R, x);
		}
	if (x == root->val)//usuwamy ten
	{
		if (root->L == NULL && root->R == NULL)//usuwanie liscia
		{
			if (root->par != NULL) {
				if (root == root->par->L) //lewy syn
				{
					root->par->L = NULL;
				}
				else //prawy syn
				{
					root->par->R = NULL;
				}
			}
			delete root;
			return;
		}
		if (root->L == NULL || root->R == NULL)//wezel z jednym synem
		{
			if (root->L == NULL)//prawy wezel
			{
				root->R->par = root->par;
				root->par->R = root->R;
				delete root;
				return;

			}
			if (root->R == NULL)//lewy wezel
			{
				root->L->par = root->par;
				root->par->L = root->L;
				delete root;
				return;
			}
		}
		if (root->R && root->L)//wezel z dwoma synami
		{
			nodeBST* temp;

			temp = nastepnik(root);
			int y = root->val;
			root->val = temp->val;
			if (temp->par->L == temp)
			{
				temp->par->L = temp->L;// to bedzie null
			}
			else
			{
				temp->par->R = temp->R;
				if (temp->R)//to nie koniecznie null
					temp->R->par = temp->par;
			}
			delete temp;

		}

	}
}



int main()
{
	//f. wstawiajaca, wyszukiwanie poprzednika i nastepnika, wyszukiwanie wartosci, f. show, f. usuwajaca
	nodeBST* root = NULL;
	add(root, 10, NULL);
	add(root, 5, NULL);
	add(root, 11, NULL);
	add(root, 2, NULL);
	add(root, 10, NULL);
	add(root, 1, NULL);
	add(root, 12, NULL);
	add(root, 6, NULL);
	show(root);
	usuwanie(root, 5);
	show(root);
	min(root);
	max(root);


}
