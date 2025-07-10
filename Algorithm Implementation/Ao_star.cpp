
#include <iostream>
#include <vector>
#include <limits>
using namespace std;

int main()
{
    int n;
    cout << "Enter number of nodes: ";
    cin >> n;

    vector<int> heuristic(n);
    vector<vector<int>> graph(n);

    cout << "Enter heuristic values:\n";
    for (int i = 0; i < n; ++i)
    {
        cin >> heuristic[i];
    }

    int e;
    cout << "Enter number of edges: ";
    cin >> e;

    cout << "Enter edges (u v):\n";
    for (int i = 0; i < e; ++i)
    {
        int u, v;
        cin >> u >> v;
        graph[u].push_back(v);
    }

    int current;
    cout << "Enter start node: ";
    cin >> current;

    while (true)
    {
        cout << "Current: " << current << " with h=" << heuristic[current] << endl;

        int best = current;
        for (int neighbor : graph[current])
        {
            if (heuristic[neighbor] < heuristic[best])
            {
                best = neighbor;
            }
        }

        if (best == current)
        {
            cout << "Reached peak at node: " << current << endl;
            break;
        }

        current = best;
    }

    return 0;
}
