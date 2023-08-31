namespace Visitor;

public interface IDotModelVisitor
{
    void VisitNode(Node node);
    void VisitEdge(Edge edge);
}

// Matches the whitelist in the prompt sent to LLM
public enum NodeKind
{
    Start,
    Decision,
    End,
    While,
    ReadItemsFromStorage,
    WriteItemsToStorage,
    CreateListEnumerator,
    HasListEnumeratorMoreItems,
    GenNextItemFromEnumerator,
    Variable,
    Parameter,
    CallFlow,
    Other,
    Comment
}

public record Node(NodeKind Kind, string Identifier);

public record Edge(Node Start, Node End);
