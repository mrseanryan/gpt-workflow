
using System.Diagnostics;
using System.Text;
using Builder;
using Visitor;

switch (args.Length)
{
    case 1:
    {
        var cmd = args[0];
        if (cmd == "create-example-dot")
        {
            CreateExampleDot();
            return 0;
        }
        else ShowUsage();
        return 6661;
    }
    case 2:
    {
        var cmd = args[0];
        if (cmd == "parse")
        {
            ParseAndDumpDotFile(args[1]);
            return 0;
        }
        else ShowUsage();
        return 6662;
    }
    default:
    {
        ShowUsage();
        return 666;
    }
}

void CreateExampleDot()
{
    var builder = new DotBuilder();
    var start = builder.AddNode(NodeKind.Start);
    var decideExperience = builder.AddNode(NodeKind.Decision, "Experience");
    var decideEducation = builder.AddNode(NodeKind.Decision, "Education");
    var decideSkills = builder.AddNode(NodeKind.Decision, "Skills");

    var end_recommend = builder.AddNode(NodeKind.End, "Recommend");
    var end_not_recommend = builder.AddNode(NodeKind.End, "Not_Recommend");

    builder.AddEdge(start, decideExperience);
    builder.AddEdge(decideExperience, decideEducation, "true");
    builder.AddEdge(decideExperience, end_not_recommend, "false");

    builder.AddEdge(decideEducation, decideSkills, "true");
    builder.AddEdge(decideEducation, end_not_recommend, "false");

    builder.AddEdge(decideSkills, end_recommend, "true");
    builder.AddEdge(decideSkills, end_not_recommend, "false");

    Console.WriteLine(builder.Build());
}

void ShowUsage()
{
    var processName = Process.GetCurrentProcess().ProcessName;
    Console.WriteLine($"USAGE: {processName} parse <path to DOT file>");
    Console.WriteLine($"USAGE: {processName} create-example-dot");
}

void ParseAndDumpDotFile(string pathToDotFile)
{
    Console.WriteLine($"Parsing DOT file {pathToDotFile}");

    var dot = File.ReadAllText(pathToDotFile, Encoding.UTF8);
    var parser = new Parser.DotParser();
    parser.Parse(dot, new ConsoleDumpDotModelVisitor());
}
