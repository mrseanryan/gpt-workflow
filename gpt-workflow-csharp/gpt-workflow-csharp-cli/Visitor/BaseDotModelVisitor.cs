namespace Visitor;

public abstract class BaseDotModelVisitor : IDotModelVisitor
{
    VisitedStringTracker visited = new();

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
        SetLabelForNode(node, label);
    }

    protected abstract void SetLabelForNode(Node node, string label);
}
