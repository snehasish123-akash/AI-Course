#include <iostream>
#include <queue>
#include <vector>
#include <unordered_map>
#include <climits>
#include <set>

using namespace std;

vector<int> a_star_search(
    unordered_map<int, vector<pair<int, int>>>& graph,
    int start, int goal,
    unordered_map<int, int>& heuristic) {


    typedef pair<int, vector<int>> PQElement;
    priority_queue<PQElement, vector<PQElement>, greater<PQElement>> pq;

    unordered_map<int, int> g_values;
    g_values[start] = 0;

    pq.push(make_pair(heuristic[start], vector<int>{start}));
    set<int> visited;

    while (!pq.empty()) {
        PQElement top = pq.top();
        pq.pop();

        int f_val = top.first;
        vector<int> path = top.second;
        int current = path.back();

        if (current == goal) {
            return path;
        }

        if (visited.find(current) != visited.end()) {
            continue;
        }
        visited.insert(current);

        for (int i = 0; i < graph[current].size(); ++i) {
            int neighbor = graph[current][i].first;
            int cost = graph[current][i].second;

            int tentative_g = g_values[current] + cost;

            if (g_values.find(neighbor) == g_values.end() || tentative_g < g_values[neighbor]) {
                g_values[neighbor] = tentative_g;
                int f = tentative_g + heuristic[neighbor];
                vector<int> new_path = path;
                new_path.push_back(neighbor);
                pq.push(make_pair(f, new_path));
            }
        }
    }

    return {}; 
}

int main() {
    unordered_map<int, vector<pair<int, int>>> graph;
    unordered_map<int, int> heuristic;
    int nodes, edges;

    cout << "Enter number of nodes: ";
    cin >> nodes;

    cout << "Enter heuristic values for each node:" << endl;
    for (int i = 0; i < nodes; i++) {
        int node, h;
        cout << "Node " << i + 1 << ": ";
        cin >> node >> h;
        heuristic[node] = h;
    }

    cout << "Enter number of edges: ";
    cin >> edges;

    cout << "Is the graph undirected? (1 for Yes, 0 for No): ";
    int undirected;
    cin >> undirected;

    cout << "Enter edges with cost (format: from to cost):" << endl;
    for (int i = 0; i < edges; i++) {
        int from, to, cost;
        cin >> from >> to >> cost;
        graph[from].push_back(make_pair(to, cost));
        if (undirected) {
            graph[to].push_back(make_pair(from, cost));
        }
    }

    int start, goal;
    cout << "Enter start node: ";
    cin >> start;
    cout << "Enter goal node: ";
    cin >> goal;

    vector<int> path = a_star_search(graph, start, goal, heuristic);

    if (path.empty()) {
        cout << "No path found from " << start << " to " << goal << "!" << endl;
    } else {
        cout << "A* Path from " << start << " to " << goal << ": ";
        for (int i = 0; i < path.size(); i++) {
            cout << path[i] << " ";
        }
        cout << endl;
    }

    return 0;
}
