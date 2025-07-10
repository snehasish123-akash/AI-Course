#include <iostream>
#include <vector>
#include <queue>
#include <unordered_set>
using namespace std;

bool bidirectional_search(vector<vector<int>> &graph, int start, int goal)
{
    unordered_set<int> visited_f, visited_b;
    queue<int> q_f, q_b;

    q_f.push(start);
    q_b.push(goal);
    visited_f.insert(start);
    visited_b.insert(goal);

    while (!q_f.empty() && !q_b.empty())
    {
        int f = q_f.front();
        q_f.pop();
        int b = q_b.front();
        q_b.pop();

        if (visited_b.count(f) || visited_f.count(b))
        {
            cout << "Path found (meeting point at " << f << " or " << b << ")\n";
            return true;
        }

        for (int neigh : graph[f])
        {
            if (!visited_f.count(neigh))
            {
                visited_f.insert(neigh);
                q_f.push(neigh);
            }
        }
        for (int neigh : graph[b])
        {
            if (!visited_b.count(neigh))
            {
                visited_b.insert(neigh);
                q_b.push(neigh);
            }
        }
    }

    return false;
}

int main()
{
    int n, e;
    cout << "Enter number of nodes and edges: ";
    cin >> n >> e;
    vector<vector<int>> graph(n);
    cout << "Enter edges:\n";
    for (int i = 0; i < e; ++i)
    {
        int u, v;
        cin >> u >> v;
        graph[u].push_back(v);
        graph[v].push_back(u); // undirected
    }

    int start, goal;
    cout << "Enter start and goal: ";
    cin >> start >> goal;

    if (!bidirectional_search(graph, start, goal))
    {
        cout << "No path found.\n";
    }
}
