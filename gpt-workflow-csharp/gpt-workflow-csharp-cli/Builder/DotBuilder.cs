using Visitor;

namespace Builder;

public class DotBuilder
{
    int next_id = 1;
    readonly List<Edge> edges = new();
    readonly List<Node> nodes = new();

    string NextId(NodeKind kind) => $"{kind}_{next_id++}";

    public Node AddNode(NodeKind kind, string identifier = "")
    {
        if (string.IsNullOrEmpty(identifier))
            identifier = NextId(kind);
        var node = new Node(kind, identifier);
        nodes.Add(node);
        return node;
    }

    public Edge AddEdge(Node one, Node two, string label = "")
    {
        var edge = new Edge(one, two, label);
        edges.Add(edge);
        return edge;
    }

    public string Build()
    {
        return "xxx";
    }
}
