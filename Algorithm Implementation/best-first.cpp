#include <iostream>
#include <vector>
#include <queue>
#include <functional>
using namespace std;

int main()
{
    int n, e;
    cout << "Enter number of nodes and edges: ";
    cin >> n >> e;

    vector<vector<int>> graph(n);
    vector<int> heuristic(n);

    cout << "Enter heuristic values for each node:\n";
    for (int i = 0; i < n; ++i)
    {
        cout << "Heuristic[" << i << "]: ";
        cin >> heuristic[i];
    }

    cout << "Enter edges (u v):\n";
    for (int i = 0; i < e; ++i)
    {
        int u, v;
        cin >> u >> v;
        graph[u].push_back(v);
        // If the graph is undirected, add the reverse edge:
        // graph[v].push_back(u);
    }

    int start, goal;
    cout << "Enter start and goal node: ";
    cin >> start >> goal;

    priority_queue<pair<int, int>, vector<pair<int, int>>, greater<pair<int, int>>> pq;
    vector<bool> visited(n, false);

    pq.push(make_pair(heuristic[start], start));

    while (!pq.empty())
    {
        pair<int, int> top = pq.top();
        pq.pop();
        int h = top.first;
        int current = top.second;

        if (visited[current])
            continue;

        visited[current] = true;
        cout << "Visiting Node: " << current << " with Heuristic: " << h << "\n";

        if (current == goal)
        {
            cout << "Goal Node " << goal << " found!\n";
            return 0;
        }

        for (int neighbor : graph[current])
        {
            if (!visited[neighbor])
            {
                pq.push(make_pair(heuristic[neighbor], neighbor));
            }
        }
    }

    cout << "Goal Node not reachable from Start Node.\n";
    return 0;
}
