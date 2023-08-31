using System.Text;
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
        var sb = new StringBuilder();
        sb.AppendLine("digraph G {");

        foreach(var node in nodes)
            sb.AppendLine($"  {GetNodeAsDot(node)}[shape={GetShape(node)}, label=\"{node.Identifier}\" ];");

        foreach(var edge in edges)
        {
            var edgeLabel = "";
            if (!string.IsNullOrEmpty(edge.Label))
            {
                edgeLabel = $" [label=\"{edge.Label}\"]";
            }
            sb.AppendLine($"  {GetNodeAsDot(edge.Start)} -> {GetNodeAsDot(edge.End)}{edgeLabel};");
        }

        sb.AppendLine("}");

        return sb.ToString();
    }

    string GetNodeAsDot(Node node) => $"{node.Kind}_{node.Identifier.Replace(" ", "_")}";

    string GetShape(Node node)
    {
        switch(node.Kind)
        {
            case NodeKind.Decision:
                return "Mdiamond";
            case NodeKind.End:
                return "rectangle";
            case NodeKind.Start:
                return "ellipse";
            default:
                return "Msquare";
        }
    }
}
