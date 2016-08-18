#include <iostream>
#include <fstream>
using namespace std;

bool isSame(string a, string b){
	int i, j = -1, count, m;
		while(b[++j]){
			i = -1; count = 0; m = c = j - 1;
			for(int c = j - 1; c > -1; c--) if(b[j]==b[c]){count++; break;}
			if(!count){
				while(b[++m]) if(b[m]==b[j]) count++;
				while(a[++i]) if(a[i]==b[j]) count--;
				if(count) return false;
			}
		}return true;
}

int main(){
	string a, b; int c = 0;
	ifstream words("words.txt"); ofstream out("output.txt");
	while(!words.eof()){
		words >> a; ifstream list("wordlist.txt");
		while(!list.eof()){
			list >> b;
			if(a.length()==b.length()) if(isSame(a, b)) if(c) out << ',' << b; else{c++; out << b;}
		}list.close();
	}words.close(); out.close();
}
