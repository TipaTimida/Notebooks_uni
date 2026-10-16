#include <iostream>
#include <vector>

using namespace std;

int somma(vector<int> a, int i, int j){
    int risultato=0;
    for (int k=i; k<=j; ++k){
        risultato += a[k];
    }
    return risultato;
}


int segmax1(vector<int> a){   // O(n^3)
    int maxres {0}, maxi {0}, maxj {0};
    int n = a.size();
    for (int i = 0; i<n; i++){
        for (int j =i; j<n; j++){     // tutte le coppie [i,j] con 0<i<j<n
            int s = somma(a,i,j);
            if (s>maxres) {
                maxres = s;
                maxi = i;
                maxj = j;
        }
    }
    }
    cout << maxi << ' ' << maxj << endl; 
    return maxres;
}

int segmax2(const vector<int>& a) {   // O(n^2)
    int maxres{0}, maxi{0}, maxj{0};
    int n = a.size();

    for (int i = 0; i < n; i++) {
        int s = 0;

        for (int j = i; j < n; j++) {
            s += a[j];   // somma del segmento [i, j]

            if (s > maxres) {
                maxres = s;
                maxi = i;
                maxj = j;
            }
        }
    }

    cout << maxi << ' ' << maxj << endl;
    return maxres;
}


// nota che somma(a,i,j+1) = somma(a,i,j)+a[j+1]
// non devo ricalcoalre tutta la somma, ma solo aggiungere un elemeneto  
// parti da a[0] e aggiungi elementi
// poi parti da a[1] e aggiungi elementi  
// poi parti da a[2] e aggiungi elementi  


int main() {
    vector<int> a {4, -6, 3, 5, -2, 1, -4, 6};
    // cout << somma(a, 2, 5) << endl;
    cout << segmax2(a) << endl;
    return 1;
}


// in intellisense, put g++ 13