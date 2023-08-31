namespace Parser;

using Visitor;
using DotLang.CodeAnalysis.Syntax;
using System;

public class DotParser
{
    public void Parse(string dot, IDotModelVisitor visitor)
    {
        var syntaxTree = new Parser(dot).Parse();
        syntaxTree.Accept(new DotVisitor(visitor));
    }
}

// ref: https://github.com/abock/dotlang/blob/master/src/DotLang/CodeAnalysis/Syntax/SyntaxVisitor.cs
class DotVisitor : SyntaxVisitor
{
    const string UNKOWN = "(unknown)";
    readonly IDotModelVisitor visitor;

    public DotVisitor(IDotModelVisitor visitor)
    {
        this.visitor = visitor;
    }

    // Assumption: only Nodes will have labels
    // TODO: support Edges with labels, if needed
    Node? previousNode = null;

    public override bool VisitNodeIdentifierSyntax(NodeIdentifierSyntax nodeIdentifier, VisitKind visitKind)
    {
        var identifier = IdentifierFrom(nodeIdentifier.IdentifierToken);

        var node = new Node(NodeKindFrom(nodeIdentifier.IdentifierToken.ToString()), identifier);
        visitor.VisitNode(node);

        if (node.Kind != NodeKind.Comment)
            previousNode = node;

        return true;
    }

    public override bool VisitAttributeSyntax(AttributeSyntax attribute, VisitKind visitKind)
    {
        if (previousNode != null && attribute.NameToken.ToString().Trim() == "label")
        {
            var label = attribute.ValueToken.StringValue;
            if (!string.IsNullOrEmpty(label))
                visitor.VisitNodeLabel(previousNode, label);
        }

        return true;
    }

    NodeKind NodeKindFrom(string identifier)
    {
        if (string.IsNullOrEmpty(identifier))
            return NodeKind.Other;
        identifier = identifier.Trim();
        if (IsComment(identifier))
            return NodeKind.Comment;

        var parts = identifier.Split("_")
            .Select(p => p.Trim());
        var kind = parts.First().ToLower();

        switch (kind)
        {
            case "decision":
                return NodeKind.Decision;
            case "end":
                return NodeKind.End;
            case "start":
                return NodeKind.Start;
            default:
                return NodeKind.Other;
        }
    }

    bool IsComment(string identifier) => identifier.Trim().StartsWith("//") || identifier.Trim().StartsWith("#");

    public override bool VisitEdgeStatementSyntax(EdgeStatementSyntax edgeStatement, VisitKind visitKind)
    {
        var leftId = IdentifierFrom(edgeStatement.Left);
        var rightId = IdentifierFrom(edgeStatement.Right);

        var left = new Node(NodeKindFrom(ToStringOrUnknown(edgeStatement.Left)), leftId);
        var right = new Node(NodeKindFrom(ToStringOrUnknown(edgeStatement.Right)), rightId);
        visitor.VisitEdge(new Edge(left, right));
        return true;
    }

    string ToStringOrUnknown(IEdgeVertexStatementSyntax edge) => edge.ToString() ?? UNKOWN;

    string IdentifierFrom(IEdgeVertexStatementSyntax edgeVertex) => IdentifierFrom(ToStringOrUnknown(edgeVertex));
    string IdentifierFrom(SyntaxToken identifierToken) => IdentifierFrom(identifierToken?.StringValue ?? UNKOWN);
    string IdentifierFrom(string identifier)
    {
        if (string.IsNullOrEmpty(identifier))
            return UNKOWN;
        var parts = identifier.Split("_")
            .Select(p => p.Trim());
        if (parts.Count() == 1)
            return parts.First();

        // decision_down_payment -> DownPayment
        return string.Join("",
            parts.Skip(1)
            .Select(p => p[0].ToString().ToUpper() + string.Join("", p.Skip(1)))
        )
        .Replace(";", "");
    }
}
