namespace Visitor;

class VisitedStringTracker
{
    readonly HashSet<string> visited = new ();

    public bool WasVisited(string name)
    {
        if (visited.Contains(name))
            return true;
        visited.Add(name);
        return false;
    }
}
