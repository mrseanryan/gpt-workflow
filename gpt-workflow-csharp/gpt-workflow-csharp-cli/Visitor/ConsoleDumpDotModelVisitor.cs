namespace Visitor;

// Default example implementation of IDotModelVisitor
public class ConsoleDumpDotModelVisitor : BaseDotModelVisitor
{
    protected override void VisitEdgeImplementation(Edge edge)
    {
        Console.WriteLine($"{ToString(edge.Start)} --> {ToString(edge.End)}");
    }

    protected override void VisitNodeImplementation(Node node)
    {
        if (node.Kind == NodeKind.Comment)
            return;

        Console.WriteLine(ToString(node));
    }

    protected override void SetLabelForNode(Node node, string label)
    {
        Console.WriteLine($"// node '{ToString(node)}' has label '{label}'");
    }

    string ToString(Node node) => $"{node.Kind}[{node.Identifier}]";
}
