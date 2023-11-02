using System.Net;
using System.Web;

namespace Client;

public class GptWorkflowClient
{
    readonly int port;
    readonly string hostname;

    public GptWorkflowClient(string hostname, int port)
    {
        this.port = port;
        this.hostname = hostname;
    }

    HttpClient CreateClient() => new HttpClient () { BaseAddress = new Uri($"http://{host}:{port}") };

    async Task<string> GetResponse(string request)
    {
        using(var webClient = CreateClient())
        {
            var rsp = await webClient.GetAsync(request);
            rsp.EnsureSuccessStatusCode()
                .WriteRequestToConsole();
    
            return await rsp.Content.ReadAsStringAsync();
        }
    }

    string Encode(string text)
        => HttpUtility.UrlPathEncode(text);

    public async Task<string> DescribeDot(string dot)
        => await GetResponse($"describe-dot?p={Encode(dot)}");

    public async Task<(string description, string dot)> GenerateDot(string description)
    {
        var rsp = await GetResponse($"generate-dot?p={Encode(description)}");

        var rspParts = rsp.Split("======");
        var generatedDescription = rspParts[0];
        var dot = rspParts[1];
        return (generatedDescription, dot);
    }
}
