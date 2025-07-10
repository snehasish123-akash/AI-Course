#include <iostream>
#include <vector>
#include <climits>
#include <algorithm>

using namespace std;

int evaluate(int node_index, const vector<int>& scores) {
    return scores[node_index];
}

int alpha_beta(int depth, int node_index, bool is_max, 
               const vector<int>& scores, int h, 
               int alpha, int beta) {
    if (depth == h) {
        return evaluate(node_index, scores);
    }
    
    if (is_max) {
        int best = INT_MIN;
        for (int i = 0; i < 2; i++) {
            int val = alpha_beta(depth+1, node_index*2 + i, false, scores, h, alpha, beta);
            best = max(best, val);
            alpha = max(alpha, best);
            if (beta <= alpha) {
                break;
            }
        }
        return best;
    } 
    
    else {
        int best = INT_MAX;
        for (int i = 0; i < 2; i++) {
            int val = alpha_beta(depth+1, node_index*2 + i, true, scores, h, alpha, beta);
            best = min(best, val);
            beta = min(beta, best);
            if (beta <= alpha) {
                break;
            }
        }
        return best;
    }
}

int main() {
    int h;
    cout << "Enter height of the game tree: ";
    cin >> h;
    
    int leaf_nodes = 1 << h; // 2^height
    vector<int> scores(leaf_nodes);
    
    cout << "Enter " << leaf_nodes << " leaf node values:" << endl;
    for (int i = 0; i < leaf_nodes; i++) {
        cin >> scores[i];
    }
    
    int result = alpha_beta(0, 0, true, scores, h, INT_MIN, INT_MAX);
    cout << "Optimal value with alpha-beta pruning: " << result << endl;
    
    return 0;
}