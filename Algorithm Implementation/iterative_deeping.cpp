#include <iostream>
#include <vector>
using namespace std;

bool DLS(vector<vector<int>> &graph, int src, int goal, int limit, vector<bool> &visited)
{
    if (src == goal)
        return true;
    if (limit <= 0)
        return false;

    visited[src] = true;

    for (int neighbor : graph[src])
    {
        if (!visited[neighbor])
        {
            if (DLS(graph, neighbor, goal, limit - 1, visited))
                return true;
        }
    }
    return false;
}

bool IDS(vector<vector<int>> &graph, int src, int goal, int max_depth)
{
    for (int depth = 0; depth <= max_depth; ++depth)
    {
        vector<bool> visited(graph.size(), false);
        if (DLS(graph, src, goal, depth, visited))
        {
            cout << "Goal found at depth " << depth << endl;
            return true;
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
    cout << "Enter edges (u v):\n";
    for (int i = 0; i < e; ++i)
    {
        int u, v;
        cin >> u >> v;
        graph[u].push_back(v);
    }

    int start, goal;
    cout << "Enter start and goal node: ";
    cin >> start >> goal;

    int max_depth = 10;
    if (!IDS(graph, start, goal, max_depth))
    {
        cout << "Goal not found up to depth " << max_depth << endl;
    }
}
