#include <iostream>
using namespace std;

const int maxi = 1000;
int adj[maxi][maxi];
bool visited[maxi];

void dfs(int V, int root)
{
    visited[root] = true;
    cout << root << " ";
    for (int i = 0; i < V; ++i){
        if (adj[root][i] == 1 && !visited[i]){
            dfs(V, i);
        }
    }
}

int main()
{
    int V, E;
    cout << "Enter the number of vertices: ";
    cin >> V;

    cout << "Enter the number of edges: ";
    cin >> E;

    // Initialize adjacency matrix
    for (int i = 0; i < V; ++i)
    {
        for (int j = 0; j < V; ++j)
        {
            adj[i][j] = 0;
        }
    }

    // Input edges

    cout << "Enter the edges (node1 node2):\n";
    for (int i = 0; i < E; ++i)
    {
        int node1, node2;
        cin >> node1 >> node2;
        adj[node1][node2] = 1;
        adj[node2][node1] = 1; // Assuming undirected graph
    }

    // Initialize visited array
    for (int i = 0; i < V; ++i)
    {
        visited[i] = false;
    }

    // Input root node
    int root;
    cout << "Enter the root node: ";
    cin >> root;

    // Perform DFS from the root
    cout << "DFS traversal starting from node " << root << ": ";
    dfs(V, root);
    cout << endl;

    return 0;
}
