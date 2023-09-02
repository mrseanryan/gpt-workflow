namespace Parser;

using Visitor;
using DotLang.CodeAnalysis.Syntax;
using System;

public class DotParser
{
    public void Parse(string dot, IDotModelVisitor visitor)
    {
        dot = RemoveComments(dot);
        var syntaxTree = new Parser(dot).Parse();
        syntaxTree.Accept(new DotVisitor(visitor));
    }

    string RemoveComments(string dot)
    {
        // Unfortunately, comments in the DOT mess up the parsing - seems bug in Nuget package.
        var lines = dot.Replace("\r", "").Split("\n");
        return string.Join("\n", lines.Where(l => !IsComment(l)));
    }

    bool IsComment(string line) => line.Trim().StartsWith("//") || line.Trim().StartsWith("#");
}

// ref: https://github.com/abock/dotlang/blob/master/src/DotLang/CodeAnalysis/Syntax/SyntaxVisitor.cs
class DotVisitor : SyntaxVisitor
{
    const string UNKOWN = "unknown";
    readonly IDotModelVisitor visitor;

    // The AST visitor seems to visit same nodes multiple times. This visitor suppresses the duplicate visits.
    readonly VisitedStringTracker visited = new VisitedStringTracker();

    public DotVisitor(IDotModelVisitor visitor)
    {
        this.visitor = visitor;
    }

    // Assumption: only Nodes will have labels
    // TODO: support Edges with labels, if needed

    public override bool VisitNodeStatementSyntax(NodeStatementSyntax nodeStatement, VisitKind visitKind)
    {
        var identifier = IdentifierFrom(nodeStatement.Identifier.IdentifierToken);
        var kind = NodeKindFrom(nodeStatement.Identifier.IdentifierToken.ToString());

        var node = new Node(kind, identifier);
        if (!visited.WasVisited(node.ToString()))
        {
            visitor.VisitNode(node);
        }

        var labelAttribute = nodeStatement.Attributes?.FirstOrDefault(a => a.NameToken.StringValue?.Trim() == "label");
        if (labelAttribute != null)
        {
            var label = labelAttribute.ValueToken.StringValue;
            if (!string.IsNullOrEmpty(label))
                visitor.VisitNodeLabel(node, label);
        }
        return true;
    }

    NodeKind NodeKindFrom(string identifier)
    {
        if (string.IsNullOrEmpty(identifier))
            return NodeKind.Other;
        identifier = identifier.Trim();
        if (IsComment(identifier)) {
            // handle comment like this: (seems to be bug in the parser - else the label gets lost!)
            //    // decision_down_payment
            //    decision_down_payment [shape=diamond, label="Down Payment > 20%?"];
            var commentedKind = NodeKindFrom(DeComment(identifier));
            if (commentedKind != NodeKind.Other)
                return commentedKind;

            return NodeKind.Comment;
        }

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

    string DeComment(string identifier)
    {
        identifier = identifier.Trim();
        if (identifier.StartsWith("//"))
            return identifier.Substring(2);
        if (identifier.StartsWith("#"))
            return identifier.Substring(1);
        return identifier;
    }

    public override bool VisitEdgeStatementSyntax(EdgeStatementSyntax edgeStatement, VisitKind visitKind)
    {
        // bug in parser?
        // Can get an edgeStatement like this: - messed up due to comments in DOT. For now, can filter out comment lines.
        /*
        // decision_features -> end_general_features
        decision_features -> end_general_features [label="No"]; 
        */

        var leftId = IdentifierFrom(edgeStatement.Left);
        var rightId = IdentifierFrom(edgeStatement.Right);

        var left = new Node(NodeKindFrom(ToStringOrUnknown(edgeStatement.Left)), leftId);
        var right = new Node(NodeKindFrom(ToStringOrUnknown(edgeStatement.Right)), rightId);

        // TODO try to parse label attribute

        var edge = new Edge(left, right);
        if (!visited.WasVisited(edge.ToString()))
            visitor.VisitEdge(edge);
        return true;
    }

    string ToStringOrUnknown(IEdgeVertexStatementSyntax edge) => edge.ToString()?.Replace(";", "") ?? UNKOWN;

    string IdentifierFrom(IEdgeVertexStatementSyntax edgeVertex) => IdentifierFrom(ToStringOrUnknown(edgeVertex));
    string IdentifierFrom(SyntaxToken identifierToken) => IdentifierFrom(identifierToken?.StringValue ?? UNKOWN);
    string IdentifierFrom(string identifier)
    {
        if (string.IsNullOrEmpty(identifier))
            return UNKOWN;

        var parts = identifier.Split("[");
        parts = parts[0].Split("_")
            .Select(p => p.Trim())
            .ToArray();
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
