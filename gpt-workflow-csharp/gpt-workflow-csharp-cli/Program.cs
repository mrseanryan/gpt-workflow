
using System.Diagnostics;
using System.Text;
using Visitor;

if (args.Length != 1)
{
    ShowUsage();
    return 666;
}

void ShowUsage()
{
    Console.WriteLine($"USAGE: {Process.GetCurrentProcess().ProcessName} <path to DOT file>");
}

void ParseAndDumpDotFile(string pathToDotFile)
{
    var dot = File.ReadAllText(pathToDotFile, Encoding.UTF8);
    var parser = new Parser.DotParser();
    parser.Parse(dot, new ConsoleDumpDotModelVisitor());
}

var dotFilePath = args[0];
Console.WriteLine($"Parsing DOT file {dotFilePath}");
ParseAndDumpDotFile(dotFilePath);
return 0;
