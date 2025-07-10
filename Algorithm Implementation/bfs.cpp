#include <bits/stdc++.h>
using namespace std;
int adj[1000][1000];

void bfs(int no_vrtticies, int root)
{
    int visited[no_vrtticies];
    queue<int> q;

    for (int i = 0; i < no_vrtticies; ++i)
    {
        visited[i] = 0;
    }

    q.push(root);
    visited[root] = 1;

    while (!q.empty())
    {
        int s = q.front();
        cout << s << " ";
        q.pop();

        for (int i = 0; i < no_vrtticies; ++i)
        {
            if (adj[s][i] == 1 && visited[i] == 0)
            {
                q.push(i);
                visited[i] = 1;
            }
        }
    }
}
int main()
{
    int V, E;
    cout << "Enter the number of Vertex's::";
    cin >> V;
    cout << "Enter the number of Edges::";
    cin >> E;

    for (int i = 0; i < V; i++)
    {
        for (int j = 0; j < V; j++)
        {
            adj[i][j] = 0;
        }
    }

    cout << "Enter the Edge's::";
    for (int i = 0; i < E; i++)
    {
        int node1, node2;
        cin >> node1 >> node2;

        adj[node1][node2] = 1;
        adj[node2][node1] = 1;
    }

    int root;
    cout << "Enter the root node::";
    cin >> root;
    bfs(V, root);
}