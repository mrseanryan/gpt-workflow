namespace Visitor;

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
}
