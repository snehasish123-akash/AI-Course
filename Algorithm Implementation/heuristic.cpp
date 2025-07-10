#include <iostream>
#include <vector>
#include <queue>
#include <functional>
#include <stack>

using namespace std;

struct Node
{
    int id;
    int heuristic;
    vector<int> neighbors; 
};

int main()
{
    int n, e;
    cout << "Enter number of nodes and edges: ";
    cin >> n >> e;

    vector<Node> graph(n);
    cout << "Enter heuristic values for each node:\n";
    for (int i = 0; i < n; ++i)
    {
        cout << "Heuristic[" << i << "]: ";
        cin >> graph[i].heuristic;
    }

    cout << "Enter edges (u v):\n";
    for (int i = 0; i < e; ++i)
    {
        int u, v;
        cin >> u >> v;
        graph[u].neighbors.push_back(v);
        graph[v].neighbors.push_back(u); // For undirected graph
    }

    int start, goal;
    cout << "Enter start and goal node: ";
    cin >> start >> goal;

    priority_queue<pair<int, int>, vector<pair<int, int>>, greater<pair<int, int>>> pq;
    vector<bool> visited(n, false);
    vector<int> parent(n, -1); 
    pq.push(make_pair(graph[start].heuristic, start)); 

    while (!pq.empty())
    {
        pair<int, int> top = pq.top();
        pq.pop();
        int current = top.second;

        if (visited[current])
            continue;
        visited[current] = true;

        cout << "Visiting Node: " << current << " with Heuristic: " << graph[current].heuristic << "\n";

        if (current == goal)
        {
            cout << "Goal Node " << goal << " found!\n";

    
            stack<int> path;
            int node = goal;
            while (node != -1)
            {
                path.push(node);
                node = parent[node];
            }

            cout << "Path: ";
            while (!path.empty())
            {
                cout << path.top() << " ";
                path.pop();
            }
            cout << endl;

            return 0;
        }

        for (int neighbor : graph[current].neighbors)
        {
            if (!visited[neighbor])
            {
                pq.push(make_pair(graph[neighbor].heuristic, neighbor));
                parent[neighbor] = current;
            }
        }
    }

    cout << "Goal Node not reachable from Start Node.\n";
    return 0;
}
