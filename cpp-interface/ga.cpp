#include "iostream"
#include "functional"
#include "vector"
#include "algorithm"
using namespace std;
#define Shuffle(a) random_shuffle((a).begin(),(a).end())
#define ForEach(a, f) {for(int i_dx=0; i_dx < (a).size() ; i_dx++) {f(a[i_dx]);}}
#define ForEachSet(a, b ,f){for(int i_dx=0; i_dx < (a).size() ; i_dx++) {v[i_idx] = f(a[i_dx]);}}



void test(){
	printf("111\n");
}
class range {
 public:
   class iterator {
      friend class range;
    public:
      long int operator *() const { return i_; }
      const iterator &operator ++() { ++i_; return *this; }
      iterator operator ++(int) { iterator copy(*this); ++i_; return copy; }

      bool operator ==(const iterator &other) const { return i_ == other.i_; }
      bool operator !=(const iterator &other) const { return i_ != other.i_; }
    protected:
   iterator(long int start) : i_ (start) { }
    private:
      unsigned long i_;
   };
   iterator begin() const { return begin_; }
   iterator end() const { return end_; }
   range(long int  begin, long int end) : begin_(begin), end_(end) {}
private:
   iterator begin_;
   iterator end_;
};

double rnd(){
	return (rand()%1000)/999.0;
}

vector<int> permutation(int n){
	auto vec = vector<int>(n);
	for(int i=0; i<n; i++){
		vec[i] = i;
	}
	Shuffle(vec);
	return vec;
}




vector<int> gen_chromo(int length){
	return permutation(length);
}

vector<vector<int>> gen_popu(int size, int length){
	vector<vector<int>> popu = vector<vector<int>>(size);
	for(int i=0; i<size ; i++){
		popu[i] = gen_chromo(length);
	}
	return popu;
}


bool comp(tuple<vector<int>, double> x, tuple<vector<int>, double> y)
{
    return get<1>(x)>get<1>(y);
}

vector<vector<int>> gen_score_and_sort(vector<vector<int>> popu, std::function<double(vector<int>)> by){
	vector<tuple<vector<int>, double>> ret = vector<tuple<vector<int>, double>>(popu.size());
	
	for(int i = 0; i<popu.size(); i++){
		ret[i] = make_tuple(popu[i], by(popu[i]));
	}
	sort(ret.begin(), ret.end(), comp);
	for(int i=0; i<ret.size(); i++){
		popu[i] = get<0>(ret[i]); 
	}

	return popu;
}

void mutate(double mutate_rate, int chromo_size, vector<vector<int>>& popu){
		
		int tmp;
		for(int idx = 0; idx<popu.size(); idx++){
			int last = -1;
	    	
	    	for(int i=0; i<chromo_size; i++){
	    		if (mutate_rate > rnd()){
	    			if(last == -1){
	    				last = i;
	    			}
	    			else{
	    				int tmp = popu[idx][last];
						popu[idx][last] = popu[idx][i]; 
	    				popu[idx][i] = tmp; 
	    				last = -1;
	    			}
	    		}
	    	}	
		}
}

auto genetic_algorithm_by_group(vector<vector<int>>& popu, std::function<double(vector<int>)> fit_func, double mutate_rate=0.3, double crossover_rate=0.1){

    
	int popu_size = popu.size();
    int chromo_size = popu[0].size();

    for (int i=0; i<100; i++){
    	mutate(mutate_rate, chromo_size, popu);
    	popu = gen_score_and_sort(popu, fit_func);
    }
    return popu[0];
}


int main(){
	std::function<double(vector<int>)> f = [](vector<int> x){
		return (x[0]==1) && (x[1]==2) && (x[2]==0);
	};
	vector<vector<int>> popu = gen_popu(100, 3);
	auto res = genetic_algorithm_by_group(popu, f);
	ForEach(res, [](int i){cout<<i;});
}