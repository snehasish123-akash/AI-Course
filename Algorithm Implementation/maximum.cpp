#include <iostream>
#include <vector>
#include <climits>
#include <algorithm>

using namespace std;

int evaluate(int node_index, const vector<int>& scores) {
    return scores[node_index];
}

int minimax(int depth, int node_index, bool is_max, 
            const vector<int>& scores, int h) {


                // depth: current depth in the tree (starts at 0).

                // node_index: index of the current node in the binary tree representation.
                
                // is_max: true if it's MAX's turn, false if it's MIN's turn.
                
                // scores: vector of scores (only relevant at depth h).
                
                // h: height of the tree (total depth).
                

    if (depth == h) {
        return evaluate(node_index, scores);
    }
    
    if (is_max) {
        return max(minimax(depth+1, node_index*2, false, scores, h),
                   minimax(depth+1, node_index*2 + 1, false, scores, h));
    } else {
        return min(minimax(depth+1, node_index*2, true, scores, h),
                   minimax(depth+1, node_index*2 + 1, true, scores, h));
    }
}


int main() {
    int h;
    cout << "Enter height of the game tree: ";
    cin >> h;
    
    int leaf_nodes = 1 << h; 
    vector<int> scores(leaf_nodes);
    
    cout << "Enter " << leaf_nodes << " leaf node values:" << endl;
    for (int i = 0; i < leaf_nodes; i++) {
        cin >> scores[i];
    }
    

    /// 0 for strat ; 0 node_index,true :max player turn, vector array, h=2

    int result = minimax(0, 0, true, scores, h);
    cout << "Optimal value: " << result << endl;
    
    return 0;
}