#:package Nixill@0.15.0

#pragma warning disable IL2026
#pragma warning disable IL3050

namespace Nixill.Archipelago;

using System.Text.Json.Nodes;
using Nixill.Collections;

#region Type defs
public readonly record struct Region(string StateName, string DLCName)
{
  public override string ToString() => $"{StateName}/{DLCName}";
}

public readonly record struct Connection(Region Region1, Region Region2, bool FerryRequired);
public readonly record struct Check(string Name, Region Region, bool FerryRequired);
public readonly record struct CompanyName(string LatinName, string? CyrillicName, string? GreekName);
public readonly record struct Truck(string Make, string Model, string DLC);
#endregion

#region Data
public static class Data
{
  public const string CsvPath = "csvdata/{0}.csv";

  public const string CitiesFN = "cities";
  public static readonly CSVObjectDictionary<string, Check> Cities =
    CSVObjectDictionary.ParseObjectsFromFile(string.Format(CsvPath, CitiesFN), d => KeyValuePair.Create(
      d["City"]!,
      new Check(
        Name: d["City"]!,
        Region: new(
          DLCName: d["DLC"] ?? "",
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
      d => KeyValuePair.Create(d["Company"] ?? "", true));

  public const string CompanyLocationsFN = "company-locations";
  public static readonly CSVObjectCollection<Check> CompanyLocations =
    CSVObjectCollection.ParseObjectsFromFile(string.Format(CsvPath, CompanyLocationsFN), d => new Check(
      Name: d["Company"]!,
      Region: new(
        DLCName: d["DLC"] ?? "",
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
        DLCName: d["LeftDLC"] ?? "",
        StateName: d["Left"]!
      ),
      Region2: new(
        DLCName: d["RightDLC"] ?? "",
        StateName: d["Right"]!
      ),
      FerryRequired: d["IsFerry"] == "true"
    ));

  public const string DLCsFN = "dlcs";
  public static readonly CSVObjectDictionary<string, bool> DLCs =
    CSVObjectDictionary.ParseObjectsFromFile(string.Format(CsvPath, DLCsFN),
      d => KeyValuePair.Create(d["DLC"] ?? "", true));

  public const string PhotoTrophiesFN = "photo-trophies";
  public static readonly CSVObjectCollection<Check> PhotoTrophies =
    CSVObjectCollection.ParseObjectsFromFile(string.Format(CsvPath, PhotoTrophiesFN), d => new Check(
      Name: d["Trophy"]!,
      Region: new(
        DLCName: d["DLC"] ?? "",
        StateName: d["State"]!
      ),
      FerryRequired: d["FerryRequired"] == "true"
    ));

  public const string QuickTravelFN = "quick-travel";
  public static readonly CSVObjectCollection<Region> QuickTravel =
    CSVObjectCollection.ParseObjectsFromFile(string.Format(CsvPath, QuickTravelFN), d => new Region(
      StateName: d["State"]!,
      DLCName: d["DLC"] ?? ""
    ));

  public const string RegionsFN = "regions";
  public static readonly CSVObjectCollection<Region> Regions =
    CSVObjectCollection.ParseObjectsFromFile(string.Format(CsvPath, RegionsFN), d => new Region(
      StateName: d["State"]!,
      DLCName: d["DLC"] ?? ""
    ));

  public const string StatesFN = "states";
  public static readonly CSVObjectDictionary<string, bool> States =
    CSVObjectDictionary.ParseObjectsFromFile(string.Format(CsvPath, StatesFN), d => KeyValuePair.Create(d["State"]!, true));

  public const string TrucksFN = "trucks";
  public static readonly CSVObjectCollection<Truck> Trucks =
    CSVObjectCollection.ParseObjectsFromFile(string.Format(CsvPath, TrucksFN), d => new Truck(
      Make: d["Make"]!,
      Model: d["Model"]!,
      DLC: d["DLC"] ?? ""
    ));

  public const string TruckDealersFN = "truck-dealers";
  public static readonly CSVObjectCollection<Check> TruckDealers =
    CSVObjectCollection.ParseObjectsFromFile(string.Format(CsvPath, TruckDealersFN), d => new Check(
      Name: d["Make"]!,
      Region: new(
        DLCName: d["DLC"] ?? "",
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
        DLCName: d["DLC"] ?? "",
        StateName: d["State"]!
      ),
      FerryRequired: d["FerryRequired"] == "true"
    ));
}
#endregion

#region Json defs
// With a couple extra lines
// so that the region headers are spaced apart
public static class JsonDefs
{
  #region ├╴game.json
  public static JsonObject GetGameJson() => new()
  {
    ["game"] = "Euro Truck Simulator 2",
    ["creator"] = "Nixill",
    ["filler_item_name"] = "Spare Tire",
    ["death_link"] = true
  };
  #endregion

  #region ├╴regions.json
  public static IEnumerable<KeyValuePair<string, JsonObject>> GetRegions() => [
    GetStartRegion(),
    .. GetRegionRegions(),
    .. GetStarterStateRegions(),
    .. GetFerryConnectionRegions()
  ];

  public static KeyValuePair<string, JsonObject> GetStartRegion() => KeyValuePair.Create(
    "Start",
    new JsonObject
    {
      ["starting"] = true
    }
  );

  public static IEnumerable<KeyValuePair<string, JsonObject>> GetRegionRegions()
  {

  }

  public static IEnumerable<KeyValuePair<string, JsonObject>> GetStarterStateRegions()
  {
    foreach ((string state, _) in Data.States)
    {

    }
  }
  #endregion
}
#endregion

#region Program
public static class Program
{
  static void Main(string[] args)
  {

  }
}
#endregion