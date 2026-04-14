// assumes run from repository root!
#:package Nixill@0.15.0

namespace Nixill.Archipelago;

using System.Numerics;
using Nixill.Collections;
using Nixill.Utils.Extensions;

#region Type defs
public readonly record struct Region(string StateName, string DLCName) : IComparable<Region>
{
  public int CompareTo(Region other) => this.ToString().CompareTo(other.ToString(),
    StringComparison.InvariantCultureIgnoreCase);

  public override string ToString() => $"{StateName} {DLCName}";
}

public readonly record struct Connection(Region Region1, Region Region2, bool FerryRequired);
public readonly record struct Check(string Name, Region Region, bool FerryRequired);
public readonly record struct CompanyName(string LatinName, string? CyrillicName, string? GreekName);
public readonly record struct Truck(string Make, string Model, string DLC);
#endregion

#region Data
public static class Data
{
  public const string CsvPath = "data/csv/{0}.csv";

  public const string CitiesFN = "cities";
  public static readonly CSVObjectDictionary<string, Check> Cities =
    CSVObjectDictionary.ParseObjectsFromFile(string.Format(CsvPath, CitiesFN), d => KeyValuePair.Create(
      d["City"]!,
      new Check(
        Name: d["City"]!,
        Region: new(
          DLCName: d["DLC"] ?? "Base Game",
          StateName: d["State"]!
        ),
        FerryRequired: d["FerryRequired"] == "true"
      )
    ));

  public const string CityAliasesFN = "city-aliases";
  public static readonly CSVObjectDictionary<string, string> CityAliases =
    CSVObjectDictionary.ParseObjectsFromFile(string.Format(CsvPath, CityAliasesFN),
      d => KeyValuePair.Create(d["LocalName"]!, d["City"]!));

  public const string CompaniesFN = "companies";
  public static readonly CSVObjectDictionary<string, bool> Companies =
    CSVObjectDictionary.ParseObjectsFromFile(string.Format(CsvPath, CompaniesFN),
      d => KeyValuePair.Create(d["Company"]!, true));

  public const string CompanyLocationsFN = "company-locations";
  public static readonly CSVObjectCollection<Check> CompanyLocations =
    CSVObjectCollection.ParseObjectsFromFile(string.Format(CsvPath, CompanyLocationsFN), d => new Check(
      Name: d["Company"]!,
      Region: new(
        DLCName: d["DLC"] ?? "Base Game",
        StateName: d["State"]!
      ),
      FerryRequired: d["FerryRequired"] == "true"
    ));

  public const string CompanyNamesFN = "company-names";
  public static readonly CSVObjectCollection<CompanyName> CompanyNames =
    CSVObjectCollection.ParseObjectsFromFile(string.Format(CsvPath, CompanyNamesFN), d => new CompanyName(
      LatinName: d["Latin"]!,
      CyrillicName: d["Cyrillic"],
      GreekName: d["Greek"]
    ));

  public const string ConnectionsFN = "connections";
  public static readonly CSVObjectCollection<Connection> Connections =
    CSVObjectCollection.ParseObjectsFromFile(string.Format(CsvPath, ConnectionsFN), d => new Connection(
      Region1: new(
        DLCName: d["LeftDLC"] ?? "Base Game",
        StateName: d["Left"]!
      ),
      Region2: new(
        DLCName: d["RightDLC"] ?? "Base Game",
        StateName: d["Right"]!
      ),
      FerryRequired: d["IsFerry"] == "true"
    ));

  public const string DLCsFN = "dlcs";
  public static readonly CSVObjectDictionary<string, bool> DLCs =
    CSVObjectDictionary.ParseObjectsFromFile(string.Format(CsvPath, DLCsFN),
      d => KeyValuePair.Create(d["DLC"] ?? "Base Game", true));

  public const string DLCConnectionsFN = "dlc-connections";
  public static readonly CSVObjectCollection<(string Left, string Right)> DLCConnections =
    CSVObjectCollection.ParseObjectsFromFile(string.Format(CsvPath, DLCConnectionsFN), d => (
      d["DLC1"]! ?? "Base Game",
      d["DLC2"]! ?? "Base Game"
    ));

  public const string GameInfoFN = "game-info";
  public static readonly CSVObjectDictionary<string, string> GameInfo =
    CSVObjectDictionary.ParseObjectsFromFile(string.Format(CsvPath, GameInfoFN),
      d => KeyValuePair.Create(d["Key"]!, d["Value"]!));

  public const string PhotoTrophiesFN = "photo-trophies";
  public static readonly CSVObjectCollection<Check> PhotoTrophies =
    CSVObjectCollection.ParseObjectsFromFile(string.Format(CsvPath, PhotoTrophiesFN), d => new Check(
      Name: d["Trophy"]!,
      Region: new(
        DLCName: d["DLC"] ?? "Base Game",
        StateName: d["State"]!
      ),
      FerryRequired: d["FerryRequired"] == "true"
    ));

  public const string QuickTravelFN = "quick-travel";
  public static readonly CSVObjectCollection<Region> QuickTravel =
    CSVObjectCollection.ParseObjectsFromFile(string.Format(CsvPath, QuickTravelFN), d => new Region(
      StateName: d["State"]!,
      DLCName: d["DLC"] ?? "Base Game"
    ));

  public const string RegionsFN = "regions";
  public static readonly CSVObjectCollection<Region> Regions =
    CSVObjectCollection.ParseObjectsFromFile(string.Format(CsvPath, RegionsFN), d => new Region(
      StateName: d["State"]!,
      DLCName: d["DLC"] ?? "Base Game"
    ));

  public const string StatesFN = "states";
  public static readonly CSVObjectDictionary<string, bool> States =
    CSVObjectDictionary.ParseObjectsFromFile(string.Format(CsvPath, StatesFN), d => KeyValuePair.Create(d["State"]!, true));

  public const string TerminologyFN = "terminology";
  public static readonly CSVObjectDictionary<string, string> Terminology =
    CSVObjectDictionary.ParseObjectsFromFile(string.Format(CsvPath, TerminologyFN),
      d => KeyValuePair.Create(d["Term"]!, d["Use"]!));

  public const string TrucksFN = "trucks";
  public static readonly CSVObjectCollection<Truck> Trucks =
    CSVObjectCollection.ParseObjectsFromFile(string.Format(CsvPath, TrucksFN), d => new Truck(
      Make: d["Make"]!,
      Model: d["Model"]!,
      DLC: d["DLC"] ?? "Base Game"
    ));

  public const string TruckDealersFN = "truck-dealers";
  public static readonly CSVObjectCollection<Check> TruckDealers =
    CSVObjectCollection.ParseObjectsFromFile(string.Format(CsvPath, TruckDealersFN), d => new Check(
      Name: d["Make"]!,
      Region: new(
        DLCName: d["DLC"] ?? "Base Game",
        StateName: d["State"]!
      ),
      FerryRequired: d["FerryRequired"] == "true"
    ));

  public const string TruckDealersByCityFN = "truck-dealers-by-city";
  public static readonly CSVObjectDictionary<string, string> TruckDealersByCity =
    CSVObjectDictionary.ParseObjectsFromFile(string.Format(CsvPath, TruckDealersByCityFN), d => KeyValuePair.Create(
      d["City"]!,
      d["Make"]!
    ));

  public const string TruckMakesFN = "truck-makes";
  public static readonly CSVObjectDictionary<string, bool> TruckMakes =
    CSVObjectDictionary.ParseObjectsFromFile(string.Format(CsvPath, TruckMakesFN),
      d => KeyValuePair.Create(d["Make"]!, true));

  public const string ViewpointsFN = "viewpoints";
  public static readonly CSVObjectCollection<Check> Viewpoints =
    CSVObjectCollection.ParseObjectsFromFile(string.Format(CsvPath, ViewpointsFN), d => new Check(
      Name: d["Viewpoint"]!,
      Region: new(
        DLCName: d["DLC"] ?? "Base Game",
        StateName: d["State"]!
      ),
      FerryRequired: d["FerryRequired"] == "true"
    ));
}
#endregion

#region Program
public static class Program
{
  static void Main()
  {
    using FileStream stream = File.Open("csvdata/consistency.md", FileMode.Create);
    using StreamWriter writer = new(stream);

    Dictionary<string, string[]> fileErrors = [];

    // For the list of companies, make sure no non-ASCII characters are in
    // their names.
    fileErrors[Data.CompaniesFN] = [.. Data.Companies.SelectLineErrors(name => [
      (name.Key.Any(c => c >= 128), $"Non-ASCII characters in Company name: {name}")
    ])];

    // Same for the list of DLCs...
    fileErrors[Data.DLCsFN] = [.. Data.DLCs.SelectLineErrors(name => [
      (name.Key.Any(c => c >= 128), $"Non-ASCII characters in DLC name: {name}")
    ])];

    // ... and states...
    fileErrors[Data.StatesFN] = [.. Data.States.SelectLineErrors(name => [
      (name.Key.Any(c => c >= 128), $"Non-ASCII characters in State name: {name}")
    ])];

    // ... and truck makes.
    fileErrors[Data.TruckMakesFN] = [.. Data.TruckMakes.SelectLineErrors(name => [
      (name.Key.Any(c => c >= 128), $"Non-ASCII characters in Truck make: {name}")
    ])];

    // For the list of regions, make sure no unrecognized DLC or State
    // exists.
    fileErrors[Data.RegionsFN] = [.. Data.Regions.SelectLineErrors(region => [
      (!Data.States.ContainsKey(region.StateName), $"Unrecognized state: {region.StateName}"),
      (!Data.DLCs.ContainsKey(region.DLCName), $"Unrecognized DLC: {region.DLCName}")
    ])];

    // For the list of quick travels, make sure no unrecognized region
    // exists.
    fileErrors[Data.QuickTravelFN] = [.. Data.QuickTravel.SelectLineErrors(region => [
      (!Data.Regions.Contains(region), $"Unrecognized Region: {region}")
    ])];

    // For the list of connections, make sure no unrecognized region
    // exists.
    fileErrors[Data.ConnectionsFN] = [.. Data.Connections.SelectLineErrors(conn => [
      (!Data.Regions.Contains(conn.Region1), $"Unrecognized Left Region: {conn.Region1}"),
      (!Data.Regions.Contains(conn.Region2), $"Unrecognized Right Region: {conn.Region2}"),
      (conn.Region1 == conn.Region2, $"Region connects to itself: {conn.Region1}"),
      (conn.Region1.CompareTo(conn.Region2) > 0, $"Reversed connection: {conn.Region1} => {conn.Region2}")
    ])];

    // For the list of DLC Connections, make sure no unrecognized DLC
    // exists, and that connections are alphabetical.
    fileErrors[Data.DLCConnectionsFN] = [.. Data.DLCConnections.SelectLineErrors(conn => [
      (!Data.DLCs.ContainsKey(conn.Left), $"Unrecognized Left DLC: {conn.Left}"),
      (!Data.DLCs.ContainsKey(conn.Right), $"Unrecognized Right DLC: {conn.Right}"),
      (conn.Left == conn.Right, $"DLC connects to itself: {conn.Left}"),
      (conn.Left.CompareTo(conn.Right) > 0 && conn.Left != "Base Game", $"Reversed connection: {conn.Left} => {conn.Right}")
    ])];

    // For the list of cities, make sure no unrecognized region (country +
    // DLC) exists, and no non-ASCII characters are added.
    fileErrors[Data.CitiesFN] = [.. Data.Cities.SelectLineErrors(cityKvp => [
      (cityKvp.Key.Any(c => c >= 128), $"Non-ASCII characters in city name: {cityKvp.Key}"),
      (!Data.Regions.Contains(cityKvp.Value.Region), $"Unrecognized Region: {cityKvp.Value.Region}")
    ])];

    // Same as above for the lists of viewpoints...
    fileErrors[Data.ViewpointsFN] = [.. Data.Viewpoints.SelectLineErrors(vp => [
      (vp.Name.Any(c => c >= 128), $"Non-ASCII characters in viewpoint name: {vp.Name}"),
      (!Data.Regions.Contains(vp.Region), $"Unrecognized Region: {vp.Region}")
    ])];

    // ... and photo trophies...
    fileErrors[Data.PhotoTrophiesFN] = [.. Data.PhotoTrophies.SelectLineErrors(pt => [
      (pt.Name.Any(c => c >= 128), $"Non-ASCII characters in photo trophy name: {pt.Name}"),
      (!Data.Regions.Contains(pt.Region), $"Unrecognized Region: {pt.Region}")
    ])];

    // For the list of company locations, make sure no unrecognized
    // company names or regions are used.
    fileErrors[Data.CompanyLocationsFN] = [.. Data.CompanyLocations.SelectLineErrors(loc => [
      (!Data.Companies.ContainsKey(loc.Name), $"Unrecognized Company: {loc.Name}"),
      (!Data.Regions.Contains(loc.Region), $"Unrecognized Region: {loc.Region}")
    ])];

    // Same as above for truck dealers (with truck makes).
    fileErrors[Data.TruckDealersFN] = [.. Data.TruckDealers.SelectLineErrors(td => [
      (!Data.TruckMakes.ContainsKey(td.Name), $"Unrecognized Company: {td.Name}"),
      (!Data.Regions.Contains(td.Region), $"Unrecognized Region: {td.Region}")
    ])];

    // For the list of city aliases, make sure the alias (dict key) has
    // no non-ASCII characters, and the English name (dict value) is
    // a recognized city name.
    fileErrors[Data.CityAliasesFN] = [.. Data.CityAliases.SelectLineErrors(aliasKvp => [
      (aliasKvp.Key.Any(c => c >= 128), $"Non-ASCII characters in local city name: {aliasKvp.Key}"),
      (!Data.Cities.ContainsKey(aliasKvp.Value), $"Unrecognized city name: {aliasKvp.Value}")
    ])];

    // For the list of company names, make sure the Latin name of the
    // company is a recognized name from the companies list.
    fileErrors[Data.CompanyNamesFN] = [.. Data.CompanyNames.SelectLineErrors(c => [
      (!Data.Companies.ContainsKey(c.LatinName), $"Unrecognized Latin company name: {c.LatinName}")
    ])];

    // For the list of trucks, make sure the names of the make and model
    // don't contain any non-ASCII characters, and that the DLC name is
    // recognized if any.
    fileErrors[Data.TrucksFN] = [.. Data.Trucks.SelectLineErrors(t => [
      (!Data.TruckMakes.ContainsKey(t.Make), $"Unrecognized truck make: {t.Make}"),
      (t.Model.Any(c => c >= 128), $"Non-ASCII characters in truck model: {t.Model}"),
      (!Data.DLCs.ContainsKey(t.DLC), $"Unrecognized DLC: {t.DLC}")
    ])];

    // For the list of truck dealers by city, make sure the truck make and
    // the city name (local or English) exists.
    fileErrors[Data.TruckDealersByCityFN] = [.. Data.TruckDealersByCity.SelectLineErrors(tdbc => [
      (!Data.TruckMakes.ContainsKey(tdbc.Value), $"Unrecognized truck make: {tdbc.Value}"),
      (!Data.Cities.ContainsKey(tdbc.Key) && !Data.CityAliases.ContainsKey(tdbc.Key),
        $"Unrecognized city: {tdbc.Key}")
    ])];

    // Now write them all out!
    foreach ((string fileName, string[] errors) in fileErrors)
    {
      writer.WriteLine($"# {fileName}.csv");
      if (errors.Length > 0) errors.Do(e => writer.WriteLine(e));
      else writer.WriteLine("No errors found.");
      writer.WriteLine();
    }

    // That's a wrap!
    writer.Flush();
    writer.Close();
    stream.Close();
  }
}

internal static class Extensions
{
  public static IEnumerable<string> SelectLineErrors<T>(this IEnumerable<T> items,
    Func<T, IEnumerable<(bool IsError, string ErrorText)>> results)
  {
    foreach ((int index, T item) in items.Index())
    {
      foreach ((bool isError, string errorText) in results(item))
      {
        if (isError) yield return $"- Line {index + 2}: {errorText}";
      }
    }
  }
}
#endregion