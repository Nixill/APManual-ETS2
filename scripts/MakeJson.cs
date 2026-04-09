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
          DLCName: d["DLC"] ?? Str.DLC.BaseGame,
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
      d => KeyValuePair.Create(d["Company"] ?? Str.DLC.BaseGame, true));

  public const string CompanyLocationsFN = "company-locations";
  public static readonly CSVObjectCollection<Check> CompanyLocations =
    CSVObjectCollection.ParseObjectsFromFile(string.Format(CsvPath, CompanyLocationsFN), d => new Check(
      Name: d["Company"]!,
      Region: new(
        DLCName: d["DLC"] ?? Str.DLC.BaseGame,
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
        DLCName: d["LeftDLC"] ?? Str.DLC.BaseGame,
        StateName: d["Left"]!
      ),
      Region2: new(
        DLCName: d["RightDLC"] ?? Str.DLC.BaseGame,
        StateName: d["Right"]!
      ),
      FerryRequired: d["IsFerry"] == "true"
    ));

  public const string DLCsFN = "dlcs";
  public static readonly CSVObjectDictionary<string, bool> DLCs =
    CSVObjectDictionary.ParseObjectsFromFile(string.Format(CsvPath, DLCsFN),
      d => KeyValuePair.Create(d["DLC"] ?? Str.DLC.BaseGame, true));

  public const string PhotoTrophiesFN = "photo-trophies";
  public static readonly CSVObjectCollection<Check> PhotoTrophies =
    CSVObjectCollection.ParseObjectsFromFile(string.Format(CsvPath, PhotoTrophiesFN), d => new Check(
      Name: d["Trophy"]!,
      Region: new(
        DLCName: d["DLC"] ?? Str.DLC.BaseGame,
        StateName: d["State"]!
      ),
      FerryRequired: d["FerryRequired"] == "true"
    ));

  public const string QuickTravelFN = "quick-travel";
  public static readonly CSVObjectCollection<Region> QuickTravel =
    CSVObjectCollection.ParseObjectsFromFile(string.Format(CsvPath, QuickTravelFN), d => new Region(
      StateName: d["State"]!,
      DLCName: d["DLC"] ?? Str.DLC.BaseGame
    ));

  public const string RegionsFN = "regions";
  public static readonly CSVObjectCollection<Region> Regions =
    CSVObjectCollection.ParseObjectsFromFile(string.Format(CsvPath, RegionsFN), d => new Region(
      StateName: d["State"]!,
      DLCName: d["DLC"] ?? Str.DLC.BaseGame
    ));

  public const string StatesFN = "states";
  public static readonly CSVObjectDictionary<string, bool> States =
    CSVObjectDictionary.ParseObjectsFromFile(string.Format(CsvPath, StatesFN), d => KeyValuePair.Create(d["State"]!, true));

  public const string TrucksFN = "trucks";
  public static readonly CSVObjectCollection<Truck> Trucks =
    CSVObjectCollection.ParseObjectsFromFile(string.Format(CsvPath, TrucksFN), d => new Truck(
      Make: d["Make"]!,
      Model: d["Model"]!,
      DLC: d["DLC"] ?? Str.DLC.BaseGame
    ));

  public const string TruckDealersFN = "truck-dealers";
  public static readonly CSVObjectCollection<Check> TruckDealers =
    CSVObjectCollection.ParseObjectsFromFile(string.Format(CsvPath, TruckDealersFN), d => new Check(
      Name: d["Make"]!,
      Region: new(
        DLCName: d["DLC"] ?? Str.DLC.BaseGame,
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

#region Consistency Class
// ensure I'm using consistent names by declaring them as consts or methods
public static class Str
{
  public static class Category
  {
    public const string City = "City";
    public const string Company = "Company";
    public const string Level = "Player Level";
    public const string PhotoTrophy = "Photo Trophy";
    public const string RecruitmentAgent = "Recruitment Agency Branch";
    public const string SecretDeliveries = "Secret Delivery";
    public const string SecretDeliveryCompletions = "Secret Delivery Completions";
    public const string SecretDeliveryInstructions = "Secret Delivery Instructions";
    public const string SkillPoint = "Skill Point";
    public const string StateKey = "State Key";
    public const string StateStarterKey = "State Starter Key";
    public const string TruckContract = "Truck Purchase Contract";
    public const string TruckDealer = "Truck Dealer";
    public const string Viewpoint = "Viewpoint";
  }

  public static class DLC
  {
    public const string BaseGame = "Base Game";
  }

  public static class Event
  {
    public static string RegionReachable(string input) => new($"{input} Reachable");
  }

  public static class GameInfo
  {
    public const string Creator = "Nixill";
    public const string Filler = "Spare Tire";
    public const string Name = "ETS2";
  }

  public static class Item
  {
    public const string BankLoan = "Bank Loan Approval";
    public const string Camera = "Camera";
    public const string DeliveryToken = "Delivery Token";
    public const string FerryTicket = "Ferry Ticket";
    public const string LevelItem = "Player Level";
    public const string QuickTravelTicket = "Quick Travel Ticket";
    public const string SecretDeliveryCompletion = $"Secret Delivery Completion";
    public static string SecretDeliveryInstruction(int i) => $"Piece of Secret Delivery #{i} Instructions";
    public static string StateKey(string name) => $"{name} Key";
    public static string StateStarterKey(string name) => $"{name} Starter Key";
    public static string TruckContract(string name) => $"{name} Trucks Purchase Contract";
    public const string Television = "TV";
    public const string TrailerContract = "Trailer Contract";
  }

  public static class Location
  {
    public static string CheckConst(string checkType, string checkName) => $"{checkType}: {checkName}";
    public static string ExternalLevel(int i) => $"Player Level {i} (External)";
    public static string InternalLevel(int i) => $"Player Level {i} (Internal)";
    public static string SecretDeliveryCompleted(int i) => $"Secret Delivery #{i} Completed";
    public static string SkillLevel(int i) => $"Player Level {i} (Skill)";
  }

  public static class Option
  {
    public const string BankLoanItem = "bank_loan_approval_item";
    public const string Citysanity = "enable_citysanity";
    public const string Companysanity = "enable_companysanity";
    public const string Dealersanity = "enable_dealersanity";
    public const string DeliveryTokensAvailable = "delivery_tokens_available";
    public const string DeliveryTokensRequired = "delivery_tokens_required";
    public const string Disabled = "disabled";
    public static string DLC(string dlc) => $"enable_dlc_{SnakeCase(dlc)}";
    public const string FerryTicketItem = "ferry_ticket_item";
    public const string ItemInPool = "in_item_pool";
    public const string ItemInStartingInventory = "in_starting_inventory";
    public const string LevelChecks = "player_level_checks";
    public const string Photosanity = "enable_photosanity";
    public const string PhotosanityFindCamera = "find_camera";
    public const string PhotosanityStartWithCamera = "start_with_camera";
    public const string QuickTravelTicketItem = "quick_travel_item";
    public const string Recruitmentsanity = "enable_recruitmentsanity";
    public const string SecretDeliveriesAvailable = "secret_deliveries_available";
    public const string SecretDeliveriesRequired = "secret_deliveries_required";
    public const string SecretDeliveryInstructionParts = "secret_delivery_instruction_parts";
    public const string SkillScatter = "skill_scatter";
    public const string SkillScatterCondensed = "condensed";
    public const string SkillScatterSpread = "spread";
    public const string TrailerContractItem = "trailer_contract_item";
    public const string Viewpointsanity = "enable_viewpointsanity";
    public const string ViewpointsanityFindTV = "find_tv";
    public const string ViewpointsanityStartWithTV = "start_with_tv";
  }

  public static class OptionGroup
  {
    public const string DeliveryTokens = "Delivery Tokens";
  }

  public static class Region
  {
    public const string QuickTravel = "Quick Travel";
    public const string Start = "Start";
    public static string StartRegion(string name) => $"Start through {name}";
  }

  public static class Syntax
  {
    // Non-standard keys
    public const string DLCList = "dlc_list";
    public const string GrantIfOption = "grant_if_option";
    public const string RequireOption = "require_option";
    public const string RequireOptionValue = "require_option_value";
    public const string SecretDeliveryCounter = "secret_delivery_number";
    public const string SecretDeliveryPartCounter = "secret_delivery_part_number";

    // Standard keys
    public const string Category = "category";
    public const string CategoryHidden = "hidden";
    public const string CategoryYamlOption = "yaml_option";
    public const string GameInfoCreator = "creator";
    public const string GameInfoDeathLink = "death_link";
    public const string GameInfoFillerItem = "filler_item";
    public const string GameInfoGame = "game";
    public const string ItemClassProgression = "progression";
    public const string ItemClassUseful = "useful";
    public const string ItemCount = "count";
    public const string ItemEarly = "early";
    public const string LocationPlaceItem = "place_item";
    public const string LocationPlaceItemCategory = "place_item_category";
    public const string LocationVictory = "victory";
    public const string Name = "name";
    public const string OptionAliases = "aliases";
    public const string OptionAllowCustomValue = "allow_custom_value";
    public const string OptionDescription = "description";
    public const string OptionDisplayName = "display_name";
    public const string OptionDefaultValue = "default";
    public const string OptionGroup = "group";
    public const string OptionRangeStart = "range_start";
    public const string OptionRangeEnd = "range_end";
    public const string OptionType = "type";
    public const string OptionTypeChoice = "choice";
    public const string OptionTypeRange = "range";
    public const string OptionTypeToggle = "toggle";
    public const string OptionValues = "values";
    public const string OptionVisibility = "visibility";
    public const string OptionVisibilityComplexUI = "complex_ui";
    public const string OptionVisibilitySimpleUI = "simple_ui";
    public const string OptionVisibilitySpoiler = "spoiler";
    public const string OptionVisibilityTemplate = "template";
    public const string OptionsCore = "core";
    public const string OptionsUser = "user";
    public const string CoreOptionDeathlink = "death_link";
    public const string CoreOptionGoal = "goal";
    public const string Region = "region";
    public const string RegionConnectsTo = "connects_to";
    public const string RegionEntranceRequires = "entrance_requires";
    public const string RegionExitRequires = "exit_requires";
    public const string RegionStarting = "starting";
    public const string Requires = "requires";

    // Functions
    public static string OptionCount(string itemName, string optionName)
      => $"{{OptionCount({itemName}, {optionName})}}";
    public static string YamlCompare(string left, string oper, string right)
      => $"{{YamlCompare({left} {oper} {right})}}";
  }

  public static class Victory
  {
    public const string DeliveryTokensCollected = "All Delivery Tokens Collected";
    public const string SecretDeliveriesCompleted = "All Secret Deliveries Completed";
    public const string PlayerLevelReached = "Max Player Level Check Reached";
  }

  public static string SnakeCase(string input) => new([.. SnakeCaseE(input)]);

  static IEnumerable<char> SnakeCaseE(string input)
  {
    bool output = false;
    bool space = false;
    foreach (char c in input.ToLower())
    {
      if (c >= 'a' && c <= 'z')
      {
        if (space) { yield return '_'; space = false; }
        yield return c;
        output = true;
      }

      else if (c == ' ' || c == '_' || c == '-')
      {
        if (output) space = true;
      }
    }
  }

}
#endregion

#region Json defs
// With a couple extra lines
// so that the region headers are spaced apart
public static class JsonDefs
{
  #region ├╴generic methods
  static JsonObject WithIf(this JsonObject input, bool condition, string key, JsonNode? value)
  {
    if (condition) input[key] = value;
    return input;
  }

  static JsonArray AddIf(this JsonArray input, bool condition, JsonNode? value)
  {
    if (condition) input.Add(value);
    return input;
  }

  static KeyValuePair<string, JsonNode?> KVP(string key, JsonNode? value) => new(key, value);
  static KeyValuePair<string, JsonNode?> KVPO(string key, JsonObject obj) => new(key, obj);
  static KeyValuePair<string, JsonNode?> KVPA(string key, JsonArray arr) => new(key, arr);
  static JsonObject Obj(JsonObject obj) => obj;
  static JsonArray Arr(JsonArray arr) => arr;
  #endregion

  #region ├╴game.json
  public static JsonObject GetGameJson() => new()
  {
    [Str.Syntax.GameInfoGame] = Str.GameInfo.Name,
    [Str.Syntax.GameInfoCreator] = Str.GameInfo.Creator,
    [Str.Syntax.GameInfoFillerItem] = Str.GameInfo.Filler,
    [Str.Syntax.GameInfoDeathLink] = true
  };
  #endregion

  #region ├╴regions.json
  public static JsonObject GetRegionsJson() => [
    GetStartRegion(),
    .. GetRegionRegions()
  ];

  public static KeyValuePair<string, JsonNode?> GetStartRegion() => KVPO(Str.Region.Start, [
    KVP(Str.Syntax.RegionStarting, true),
    KVPO(Str.Syntax.RegionExitRequires, [.. GetStarterExitRequirements()])
  ]);

  public static IEnumerable<KeyValuePair<string, JsonNode?>> GetStarterExitRequirements()
  {
    foreach (var region in Data.Regions)
    {
      if (Data.QuickTravel.Contains(region)) yield return KVP($"{region}",
        $"|{Str.Item.StateStarterKey(region.StateName)}| or |{Str.Item.QuickTravelTicket}|");
      else yield return KVP($"{region}", $"|{Str.Item.StateStarterKey(region.StateName)}|");
    }
  }

  public static IEnumerable<KeyValuePair<string, JsonNode?>> GetRegionRegions()
  {
    // first let's form a couple lists of connections
    var allConnections = Data.Connections
      .SelectMany<Connection, Connection>(c => [c, new(c.Region2, c.Region1, c.FerryRequired)])
      .GroupBy(conn => conn.Region1)
      .ToDictionary(grp => grp.Key, grp => grp.Select(conn => conn.Region2).ToArray());

    var ferryConnections = Data.Connections
      .Where(conn => conn.FerryRequired)
      .SelectMany<Connection, Connection>(c => [c, new(c.Region2, c.Region1, true)])
      .GroupBy(conn => conn.Region1)
      .ToDictionary(grp => grp.Key, grp => grp.Select(conn => conn.Region2).ToArray());

    // then we'll export the regions
    foreach (Region region in Data.Regions)
    {
      Region[] connections = allConnections[region];
      Region[] ferries = ferryConnections[region];

      JsonObject obj = [
        KVP(Str.Syntax.Requires,
          $"|{Str.Item.StateKey(region.StateName)}| or |{Str.Item.StateStarterKey(region.StateName)}|"),
        KVPA(Str.Syntax.RegionConnectsTo, [Str.Region.StartRegion(region.StateName), .. connections.Select(r => $"{r}")])
      ];

      if (ferries.Length > 0)
      {
        obj[Str.Syntax.RegionExitRequires]
          = new JsonObject([.. ferries.Select(fc => KVP($"{fc}", $"|{Str.Item.FerryTicket}|"))]);
      }

      yield return KVP(region.ToString(), obj);
    }
  }
  #endregion

  #region ├╴locations.json
  public static JsonArray GetLocationsJson() => [
    .. GetCityLocations(),
    .. GetPhotoTrophyLocations(),
    .. GetViewpointLocations(),
    .. GetCompanyLocations(),
    .. GetInternalLevelLocations(),
    .. GetExternalLevelLocations(),
    .. GetSecretDeliveryLocations(),
    .. GetVictoryLocations()
  ];

  public static IEnumerable<JsonNode?> GetCheckLocations(string name, IEnumerable<Check> checks,
    string? globalRequire = null)
  {
    foreach (Check check in checks)
    {
      yield return Obj([
        KVP(Str.Syntax.Name, Str.Location.CheckConst(name, check.Name)),
        KVPA(Str.Syntax.Category, [
          name,
          check.Region.StateName,
          check.Region.DLCName
        ]),
        KVP(Str.Syntax.Region, check.Region.ToString())
      ]).WithIf(globalRequire != null && check.FerryRequired, Str.Syntax.Requires,
        $"({globalRequire}) and |{Str.Item.FerryTicket}|")
      .WithIf(globalRequire == null && check.FerryRequired, Str.Syntax.Requires, $"|{Str.Item.FerryTicket}|")
      .WithIf(globalRequire != null && !check.FerryRequired, Str.Syntax.Requires, globalRequire);
    }
  }

  public static IEnumerable<JsonNode?> GetCityLocations() => GetCheckLocations(Str.Category.City, Data.Cities.Values);
  public static IEnumerable<JsonNode?> GetPhotoTrophyLocations()
    => GetCheckLocations(Str.Category.PhotoTrophy, Data.PhotoTrophies, $"|{Str.Item.Camera}|");
  public static IEnumerable<JsonNode?> GetViewpointLocations()
    => GetCheckLocations(Str.Category.Viewpoint, Data.Viewpoints, $"|{Str.Item.Television}|");

  public static IEnumerable<JsonNode?> GetCompanyLocations()
  {
    Dictionary<string, Region[]> locations = Data.CompanyLocations.GroupBy(c => c.Name)
      .Select(grp => KeyValuePair.Create(grp.Key, grp.Select(c => c.Region).ToArray()))
      .ToDictionary();

    foreach (string company in Data.Companies.Keys)
    {
      var thisCoLoc = locations[company];

      var requires = string.Join(" or ", thisCoLoc.Select(r => $"|{Str.Event.RegionReachable(r.ToString())}|"));
      JsonNode dlcList = thisCoLoc.Any(r => r.DLCName == Str.DLC.BaseGame)
        ? false
        : (JsonArray)([.. thisCoLoc.Select(r => Str.SnakeCase(r.DLCName)).Distinct()]);

      yield return Obj([
        KVP(Str.Syntax.Name, Str.Location.CheckConst(Str.Category.Company, company)),
        KVPA(Str.Syntax.Category, [ Str.Category.Company ]),
        KVP(Str.Syntax.Requires, requires),
        KVP(Str.Syntax.DLCList, dlcList)
      ]);
    }
  }

  public static IEnumerable<JsonNode?> GetInternalLevelLocations()
    => Enumerable.Range(1, 36).Select<int, JsonObject>(i => [
      KVP(Str.Syntax.Name, Str.Location.InternalLevel(i)),
      KVPA(Str.Syntax.Category, [ Str.Category.Level ]),
      KVP(Str.Syntax.Requires, $"|{Str.Item.LevelItem}:{i-1}|"),
      KVPA(Str.Syntax.LocationPlaceItem, [ Str.Item.LevelItem ])
    ]);

  public static IEnumerable<JsonNode?> GetExternalLevelLocations()
    => Enumerable.Range(1, 36).Select<int, JsonObject>(i => [
      KVP(Str.Syntax.Name, Str.Location.ExternalLevel(i)),
      KVPA(Str.Syntax.Category, [ Str.Category.Level ]),
      KVP(Str.Syntax.Requires, $"|{Str.Item.LevelItem}:{i-1}|"),
      KVP(Str.Syntax.LocationPlaceItem, Str.Item.LevelItem)
    ]);

  public static IEnumerable<JsonNode?> GetSkillLevelLocations()
    => Enumerable.Range(1, 36).Select<int, JsonObject>(i => [
      KVP(Str.Syntax.Name, Str.Location.SkillLevel(i)),
      KVPA(Str.Syntax.Category, [ Str.Category.Level ]),
      KVP(Str.Syntax.Requires, $"|{Str.Item.LevelItem}:{i-1}|"),
      KVPA(Str.Syntax.LocationPlaceItemCategory, [ Str.Category.SkillPoint ]),
      KVP(Str.Syntax.RequireOption, Str.Option.SkillScatter),
      KVP(Str.Syntax.RequireOptionValue, Str.Option.SkillScatterCondensed)
    ]);

  public static IEnumerable<JsonNode?> GetSecretDeliveryLocations()
  {
    foreach (int i in Enumerable.Range(1, 20))
    {
      yield return Obj([
        KVP(Str.Syntax.Name, Str.Location.SecretDeliveryCompleted(i)),
        KVPA(Str.Syntax.Category, [ Str.Category.SecretDeliveries ]),
        KVP(Str.Syntax.Requires, Str.Syntax.OptionCount(Str.Item.SecretDeliveryInstruction(i),
          Str.Option.SecretDeliveryInstructionParts)),
        KVP(Str.Syntax.LocationPlaceItem, Str.Item.SecretDeliveryCompletion),
        KVP(Str.Syntax.SecretDeliveryCounter, i)
      ]);
    }
  }

  public static IEnumerable<JsonNode?> GetVictoryLocations() => [
    Obj([
      KVP(Str.Syntax.Name, Str.Victory.SecretDeliveriesCompleted),
      KVP(Str.Syntax.Requires, Str.Syntax.OptionCount(Str.Item.SecretDeliveryCompletion,
        Str.Option.SecretDeliveriesRequired)),
      KVP(Str.Syntax.LocationVictory, true)
    ]),

    Obj([
      KVP(Str.Syntax.Name, Str.Victory.DeliveryTokensCollected),
      KVP(Str.Syntax.Requires, Str.Syntax.OptionCount(Str.Item.DeliveryToken, Str.Option.DeliveryTokensRequired)),
      KVP(Str.Syntax.LocationVictory, true)
    ]),

    Obj([
      KVP(Str.Syntax.Name, Str.Victory.PlayerLevelReached),
      KVP(Str.Syntax.Requires, Str.Syntax.OptionCount(Str.Item.LevelItem, Str.Option.LevelChecks))
    ])
  ];
  #endregion

  #region ├╴items.json
  public static JsonArray GetItemsJson() => [
    .. GetStateKeyItems(),
    .. GetStarterKeyItems(),
    .. GetTruckContractItems(),
    .. GetSecretDeliveryInstructionItems(),
    .. GetSecretDeliveryCompletionItems(),
    .. GetSingleItems()
  ];

  public static IEnumerable<JsonNode?> GetStateKeyItems()
  {
    Dictionary<string, string[]> regions = Data.Regions.GroupBy(c => c.StateName)
      .Select(grp => KeyValuePair.Create(grp.Key, grp.Select(c => c.DLCName).ToArray()))
      .ToDictionary();

    foreach (var state in Data.States.Keys)
    {
      JsonNode dlcList = regions[state].Any(r => r == Str.DLC.BaseGame)
        ? false
        : (JsonArray)([.. regions[state].Select(r => Str.SnakeCase(r)).Distinct()]);

      yield return Obj([
        KVP(Str.Syntax.Name, Str.Item.StateKey(state)),
        KVPA(Str.Syntax.Category, [Str.Category.StateKey]),
        KVP(Str.Syntax.DLCList, dlcList),
        KVP(Str.Syntax.ItemClassProgression, true)
      ]);
    }
  }

  public static IEnumerable<JsonNode?> GetStarterKeyItems()
  {
    Dictionary<string, string[]> regions = Data.Regions.GroupBy(c => c.StateName)
      .Select(grp => KeyValuePair.Create(grp.Key, grp.Select(c => c.DLCName).ToArray()))
      .ToDictionary();

    foreach (var state in Data.States.Keys)
    {
      JsonNode dlcList = regions[state].Any(r => r == Str.DLC.BaseGame)
        ? false
        : (JsonArray)([.. regions[state].Select(r => Str.SnakeCase(r)).Distinct()]);

      yield return Obj([
        KVP(Str.Syntax.Name, Str.Item.StateStarterKey(state)),
        KVPA(Str.Syntax.Category, [Str.Category.StateStarterKey]),
        KVP(Str.Syntax.DLCList, dlcList),
        KVP(Str.Syntax.ItemClassProgression, true)
      ]);
    }
  }

  public static IEnumerable<JsonNode?> GetTruckContractItems()
    => Data.TruckMakes.Keys.Select(truck => Obj([
        KVP(Str.Syntax.Name, Str.Item.TruckContract(truck)),
        KVPA(Str.Syntax.Category, [Str.Category.TruckContract]),
        KVP(Str.Syntax.ItemClassUseful, true)
      ]));

  public static IEnumerable<JsonNode?> GetSecretDeliveryInstructionItems()
    => Enumerable.Range(1, 20).Select(i => Obj([
      KVP(Str.Syntax.Name, Str.Item.SecretDeliveryInstruction(i)),
      KVPA(Str.Syntax.Category, [Str.Category.SecretDeliveryInstructions]),
      KVP(Str.Syntax.ItemClassProgression, true),
      KVP(Str.Syntax.ItemCount, 5),
      KVP(Str.Syntax.SecretDeliveryCounter, i)
    ]));

  public static IEnumerable<JsonNode?> GetSecretDeliveryCompletionItems()
    => [Obj([
      KVP(Str.Syntax.Name, Str.Item.SecretDeliveryCompletion),
      KVPA(Str.Syntax.Category, [Str.Category.SecretDeliveryCompletions]),
      KVP(Str.Syntax.ItemClassProgression, true),
      KVP(Str.Syntax.ItemCount, 20)
    ])];

  public static IEnumerable<JsonNode?> GetSingleItems() => [
    Obj([
      KVP(Str.Syntax.Name, Str.Item.DeliveryToken),
      KVP(Str.Syntax.ItemClassProgression, true),
      KVP(Str.Syntax.ItemCount, 100)
    ]),

    Obj([
      KVP(Str.Syntax.Name, Str.Item.FerryTicket),
      KVP(Str.Syntax.ItemClassProgression, true),
      KVPO(Str.Syntax.GrantIfOption, [
        KVP(Str.Option.FerryTicketItem, Str.Option.ItemInStartingInventory)
      ])
    ]),

    Obj([
      KVP(Str.Syntax.Name, Str.Item.Camera),
      KVPA(Str.Syntax.Category, [Str.Category.PhotoTrophy]),
      KVP(Str.Syntax.ItemClassProgression, true),
      KVPO(Str.Syntax.GrantIfOption, [
        KVP(Str.Option.Photosanity, Str.Option.PhotosanityStartWithCamera)
      ])
    ]),

    Obj([
      KVP(Str.Syntax.Name, Str.Item.Television),
      KVPA(Str.Syntax.Category, [Str.Category.Viewpoint]),
      KVP(Str.Syntax.ItemClassProgression, true),
      KVPO(Str.Syntax.GrantIfOption, [
        KVP(Str.Option.Viewpointsanity, Str.Option.ViewpointsanityStartWithTV)
      ])
    ]),

    Obj([
      KVP(Str.Syntax.Name, Str.Item.BankLoan),
      KVP(Str.Syntax.ItemClassProgression, true),
      KVPO(Str.Syntax.GrantIfOption, [
        KVP(Str.Option.BankLoanItem, Str.Option.ItemInStartingInventory)
      ])
    ]),

    Obj([
      KVP(Str.Syntax.Name, Str.Item.TrailerContract),
      KVP(Str.Syntax.ItemClassUseful, true),
      KVPO(Str.Syntax.GrantIfOption, [
        KVP(Str.Option.TrailerContractItem, Str.Option.ItemInStartingInventory)
      ])
    ]),

    Obj([
      KVP(Str.Syntax.Name, Str.Item.QuickTravelTicket),
      KVP(Str.Syntax.ItemClassProgression, true),
      KVPO(Str.Syntax.GrantIfOption, [
        KVP(Str.Option.QuickTravelTicketItem, Str.Option.ItemInStartingInventory)
      ])
    ])
  ];
  #endregion

  #region ├╴categories.json
  public static JsonObject GetCategoriesJson() => [
    .. GetStateCategories(),
    .. GetDLCCategories(),
    .. GetTypeCategories()
  ];

  public static IEnumerable<KeyValuePair<string, JsonNode?>> GetStateCategories()
    => Data.States.Keys.Select(s => KVP(s, new JsonObject()));

  public static IEnumerable<KeyValuePair<string, JsonNode?>> GetDLCCategories()
    => Data.DLCs.Keys.Except([Str.DLC.BaseGame])
      .Select(d => KVP(d, new JsonObject
      {
        [Str.Syntax.CategoryHidden] = true,
        [Str.Syntax.CategoryYamlOption] = new JsonArray([Str.Option.DLC(d)])
      }));

  public static IEnumerable<KeyValuePair<string, JsonNode?>> GetTypeCategories() => [
    GetTypeCategory(Str.Category.City),
    GetTypeCategory(Str.Category.Viewpoint, Str.Option.Viewpointsanity),
    GetTypeCategory(Str.Category.PhotoTrophy, Str.Option.Photosanity),
    GetTypeCategory(Str.Category.Company, Str.Option.Companysanity),
    GetTypeCategory(Str.Category.RecruitmentAgent, Str.Option.Recruitmentsanity),
    GetTypeCategory(Str.Category.TruckDealer, Str.Option.Dealersanity)
  ];

  public static KeyValuePair<string, JsonNode?> GetTypeCategory(string name, string? option = null)
    => new(name, new JsonObject().WithIf(option != null, Str.Syntax.CategoryYamlOption, new JsonArray([option])));
  #endregion

  #region ├╴events.json
  public static JsonArray GetEventsJson() => [
    .. GetRegionEvents()
  ];

  public static IEnumerable<JsonNode?> GetRegionEvents()
  {
    foreach (Region region in Data.Regions)
    {
      yield return new JsonObject
      {
        [Str.Syntax.Name] = Str.Event.RegionReachable(region.ToString()),
        [Str.Syntax.Category] = new JsonArray
        {
          region.StateName,
          region.DLCName
        },
        [Str.Syntax.Region] = region.ToString()
      };
    }
  }
  #endregion

  #region └╴options.json
  public static JsonObject GetOptionsJson() => [
    KVP(Str.Syntax.OptionsCore, GetCoreOptions()),
    KVP(Str.Syntax.OptionsUser, GetUserOptions())
  ];

  public static JsonObject GetCoreOptions() => [
    KVP(Str.Syntax.CoreOptionDeathlink, Obj([
      KVPA(Str.Syntax.OptionDescription, [
        "Enable or disable death link support. If enabled:",
        "* Upon receiving a death, the player must get towed or navigate to the nearest service station.",
        "* Upon being towed to a service station or completing a delivery with over 5% damage, the player must send a death."
      ])
    ])),
    KVP(Str.Syntax.CoreOptionGoal, Obj([
      KVPA(Str.Syntax.OptionDescription, [
        "Goal condition:",
        $"* {Str.Victory.DeliveryTokensCollected}: Collect a certain number of delivery tokens (see the",
        "  \"Delivery Tokens\" group of the options), then activate the win button to win.",
        $"* {Str.Victory.SecretDeliveriesCompleted}: Collect instructions for your secret deliveries (see the",
        "  \"Secret Deliveries\" group of the options, and the patch file from the multiworld host), then follow",
        "  those instructions to win.",
        $"* {Str.Victory.PlayerLevelReached}: Reach a certain level in career progression (see the \"{Str.Option.LevelChecks}\"",
        "  option), then activate the win button to win."
      ])
    ]))
  ];

  public static JsonObject GetUserOptions() => [
    .. GetDeliveryTokensOptions(),
    .. GetSecretDeliveryOptions(),
    .. GetDLCOptions(),
    .. GetChecksOptions(),
    .. GetItemRequiresOptions(),
    .. GetChecksReductionOptions()
  ];

  public static IEnumerable<KeyValuePair<string, JsonNode?>> GetDeliveryTokensOptions() => [
    KVPO(Str.Option.DeliveryTokensAvailable, [
      KVP(Str.Syntax.OptionDisplayName, "Available Delivery Tokens"),
      KVPA(Str.Syntax.OptionDescription, [
        "Number of Delivery Tokens available in the multiworld item pool.",
        "",
        "If the number of items exceeds the number of checks, this value may be reduced to accommodate. If so, the",
        $"{Str.Option.DeliveryTokensRequired} option will be reduced proportionally."
      ]),
      KVP(Str.Syntax.OptionType, Str.Syntax.OptionTypeRange),
      KVP(Str.Syntax.OptionRangeStart, 1),
      KVP(Str.Syntax.OptionRangeEnd, 100),
      KVP(Str.Syntax.OptionGroup, Str.OptionGroup.DeliveryTokens)
    ]),

    KVPO(Str.Option.DeliveryTokensRequired, [
      KVP(Str.Syntax.OptionDisplayName, "Required Delivery Tokens"),
      KVPA(Str.Syntax.OptionDescription, [
        $"Number of Delivery Tokens needed to win. This value must not exceed {Str.Option.DeliveryTokensAvailable}, and",
        "will automatically be reduced to that value if applicable.",
        "",
        $"If the number of items exceeds the number of checks, {Str.Option.DeliveryTokensAvailable} may be reduced to",
        "accommodate. If so, this option will be reduced proportionally."
      ]),
      KVP(Str.Syntax.OptionType, Str.Syntax.OptionTypeRange),
      KVP(Str.Syntax.OptionRangeStart, 1),
      KVP(Str.Syntax.OptionRangeEnd, 100),
      KVP(Str.Syntax.OptionGroup, Str.OptionGroup.DeliveryTokens)
    ])
  ];

  public static IEnumerable<KeyValuePair<string, JsonNode?>> GetSecretDeliveryOptions() => [
    KVPO(Str.Option.SecretDeliveriesAvailable, [
      KVP(Str.Syntax.OptionDisplayName, "Secret Deliveries Available"),
      KVPA(Str.Syntax.OptionDescription, [
        "Number of total secret deliveries available.",
        "",
        "If the number of items exceeds the number of checks, this option may be reduced to accommodate. If so,",
        $"{Str.Option.SecretDeliveriesRequired} will be reduced proportionally. {Str.Option.SecretDeliveryInstructionParts}",
        "will not be reduced."
      ]),

    ])
  ]
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