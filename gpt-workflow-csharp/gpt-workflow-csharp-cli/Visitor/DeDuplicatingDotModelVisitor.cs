namespace Visitor;

// The AST visitor seems to visit same nodes multiple times. This visitor suppresses the duplicate visits.
public abstract class DeDuplicatingDotModelVisitor : IDotModelVisitor
{
    readonly VisitedStringTracker visited = new VisitedStringTracker();

    public void VisitEdge(Edge edge)
    {
        if (!visited.WasVisited(edge.ToString()))
            VisitEdgeImplementation(edge);
    }

    protected abstract void VisitEdgeImplementation(Edge edge);

    public void VisitNode(Node node)
    {
        if (!visited.WasVisited(node.ToString()))
            VisitNodeImplementation(node);
    }

    protected abstract void VisitNodeImplementation(Node node);

    public void VisitNodeLabel(Node node, string label)
    {
        if (!visited.WasVisited(node.ToString() + "--label:" + label))
            SetLabelForNode(node, label);
    }

    protected abstract void SetLabelForNode(Node node, string label);
}
