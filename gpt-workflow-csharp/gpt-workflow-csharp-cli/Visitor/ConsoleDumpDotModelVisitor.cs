namespace Visitor;

// Default example implementation of IDotModelVisitor
public class ConsoleDumpDotModelVisitor : DeDuplicatingDotModelVisitor
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

    string ToString(Node node) => $"{node.Kind}[{node.Identifier}]";
}
