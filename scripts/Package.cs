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

string filename = $"Manual_{gameName}_{creator}";

File.Delete($"release/{filename}.apworld");
ZipArchive archive = ZipFile.Open($"release/{filename}.apworld", ZipArchiveMode.Create);

foreach (string path in Directory.EnumerateFiles("src", "*", new EnumerationOptions
{
  RecurseSubdirectories = true
}))
{
  archive.CreateEntryFromFile(path, $"{filename}/{path[4..].Replace("\\", "/")}");
}

archive.Dispose();