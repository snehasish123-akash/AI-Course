#include <iostream>
#include <vector>
#include <queue>
#include <algorithm>
using namespace std;

int main()
{
    int n, e;
    cout << "Enter number of nodes and edges: ";
    cin >> n >> e;

    vector<int> heuristic(n);
    vector<vector<int>> graph(n);

    cout << "Enter heuristic values:\n";
    for (int i = 0; i < n; ++i)
    {
        cin >> heuristic[i];
    }

    cout << "Enter edges (u v):\n";
    for (int i = 0; i < e; ++i)
    {
        int u, v;
        cin >> u >> v;
        graph[u].push_back(v);
    }

    int start, goal, beam_width;
    cout << "Enter start, goal, and beam width: ";
    cin >> start >> goal >> beam_width;

    queue<int> q;
    q.push(start);

    while (!q.empty())
    {
        vector<int> next_level;
        while (!q.empty())
        {
            int node = q.front();
            q.pop();
            if (node == goal)
            {
                cout << "Goal found at node " << node << endl;
                return 0;
            }
            next_level.insert(next_level.end(), graph[node].begin(), graph[node].end());
        }

        sort(next_level.begin(), next_level.end(), [&](int a, int b)
             { return heuristic[a] < heuristic[b]; });

        q = queue<int>();
        for (int i = 0; i < min(beam_width, (int)next_level.size()); ++i)
        {
            q.push(next_level[i]);
        }
    }

    cout << "Goal not found within beam width.\n";
    return 0;
}
