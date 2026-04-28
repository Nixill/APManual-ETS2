// A script to package up the apworld from the "src" folder.

// NOTE: This script expects to be run from the repository root level.
// If running directly from its folder, uncomment the SetCurrentDirectory
// line.

using System.IO.Compression;
using System.Text.Json.Nodes;

// Directory.SetCurrentDirectory("..");

// Get game info first
JsonObject obj = (JsonObject)JsonNode.Parse(File.ReadAllText("src/data/game.json"))!;

string gameName = (string)obj["game"]!;
string creator = (string)obj["creator"]!;
string timestamp = (string)obj["build"]!;

string filename = $"Manual_{gameName}_{creator}";

int buildNumber = File.ReadAllLines($"release/{filename}.build.log").Length;

File.Delete($"release/{filename}.apworld");
ZipArchive archive = ZipFile.Open($"release/{filename}.apworld", ZipArchiveMode.Create);

foreach (string path in Directory.EnumerateFiles("src", "*", new EnumerationOptions
{
  RecurseSubdirectories = true
}))
{
  archive.CreateEntryFromFile(path, $"{filename}/{path[4..].Replace("\\", "/")}");
}

var entry = archive.CreateEntry($"{filename}/data/version.txt");

using (var entryStream = entry.Open())
using (var streamWriter = new StreamWriter(entryStream))
{
  streamWriter.Write($"""
  JSON files generated at: {timestamp}
  Package built at: {DateTime.UtcNow:yyyy-MM-dd HH:mm:ss}
  Build number: {buildNumber + 1}
  """);
}

archive.Dispose();

File.AppendAllText($"release/{filename}.build.log", $"ver {timestamp} packaged at {DateTime.UtcNow:yyyy-MM-dd HH:mm:ss}"
  + $" with size of {new FileInfo($"release/{filename}.apworld").Length}\n");