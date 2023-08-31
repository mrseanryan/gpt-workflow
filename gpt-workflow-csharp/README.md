# gpt-workflow C#

C# client for gpt-workflow

## Capabilities:

- `Take natural langauge description from C# -> DOT from LLM -> write it to C# system`: take the DOT output of gpt-workflow and then allow C# code to visit it (Visitor pattern), in order to write back to some other C# system.
- `Take DOT from C# and retrieve natural language description from LLM`: allow a C# system to write its workflow to gpt-workflow, receiving back a natural language description.

## Dependencies

### DotLan (DOT AST for C#)

- https://github.com/abock/dotlang
- https://www.nuget.org/packages/Graphviz.DotLanguage/
