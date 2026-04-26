#:package Nixill@0.15.0
#:package Newtonsoft.Json@13.0.4

namespace Nixill.Archipelago;

// using System.Text.Json.Nodes;
using Nixill.Collections;
using Newtonsoft.Json.Linq;
using Nixill.Utils;

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
  public const string CsvPath = "src/data/csv/{0}.csv";

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

  public const string DLCConnectionsFN = "dlc-connections";
  public static readonly CSVObjectCollection<(string Left, string Right)> DLCConnections =
    CSVObjectCollection.ParseObjectsFromFile(string.Format(CsvPath, DLCConnectionsFN), d => (
      d["DLC1"]! ?? Str.DLC.BaseGame,
      d["DLC2"]! ?? Str.DLC.BaseGame
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

  public const string TerminologyFN = "terminology";
  public static readonly CSVObjectDictionary<string, string> Terminology =
    CSVObjectDictionary.ParseObjectsFromFile(string.Format(CsvPath, TerminologyFN),
      d => KeyValuePair.Create(d["Term"]!, d["Use"]!));

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

#region Data Counters
public static class DataCounters
{
  public const int MaxLevel = 36;
  public readonly static int TotalStates = Data.States.Count;
  public readonly static int TotalChecks = Data.Cities.Count + Data.Companies.Count + Data.PhotoTrophies.Count +
    Data.Viewpoints.Count + MaxLevel;
  public readonly static int MaxChecksByState = Data.States.Keys.Max(s =>
    Data.Cities.Count(c => c.Value.Region.StateName == s)
    + Data.CompanyLocations.Where(cl => cl.Region.StateName == s).DistinctBy(cl => cl.Name).Count()
    + Data.PhotoTrophies.Count(pt => pt.Region.StateName == s)
    + Data.Viewpoints.Count(vp => vp.Region.StateName == s)
  );
}
#endregion

#region Consistency Class
// ensure I'm using consistent names by declaring them as consts or methods
public static class Str
{
  public static string StateCountry => Data.Terminology["State"];
  public static string StateCountryLC => Data.Terminology["state"];
  public static string StatesCountries => Data.Terminology["States"];
  public static string StatesCountriesLC => Data.Terminology["states"];

  public static class Category
  {
    public const string City = "City";
    public const string Company = "Company";
    public const string DeliveryTokens = "Delivery Tokens";
    public static string DLC(string dlcName) => $"{dlcName} (DLC)";
    public const string Level = "Player Level";
    public const string PhotoTrophy = "Photo Trophy";
    public const string PlayerSkill = "Skill";
    // public const string RecruitmentAgent = "Recruitment Agency Branch";
    public const string RegionReachableEvent = "Regions Reachable";
    public const string SecretDeliveries = "Secret Delivery";
    public const string SecretDeliveryCompletions = "Secret Delivery Completions";
    public const string SecretDeliveryInstructions = "Secret Delivery Instructions";
    public static string State(string stateName) => stateName;
    public static string StateCheck(string stateName) => $"{stateName} (Checks)";
    public static string StateKey => $"{StateCountry} Key";
    public const string StateKeyConst = "State Key";
    public static string StateStarterKey => $"{StateCountry} Starter Key";
    public const string StateStarterKeyConst = "State Starter Key";
    public const string TruckContract = "Truck Purchase Contract";
    // public const string TruckDealer = "Truck Dealer";
    public const string Viewpoint = "Viewpoint";
    public const string VisibleCompany = "(1) Companies";
    public const string VisibleLevelUp = "(2) Level Ups";
    public const string VisibleSecretDeliveryInstructions = "(2) Secret Delivery Instructions";
    public static string VisibleStateKeys => $"(1) {StateCountry} Keys";
    public const string VisiblePlayerSkills = "(3) Player Skills";
    public const string VisibleMiscItems = "(4) Misc Items";
  }

  public static class DLC
  {
    public const string BaseGame = "Base Game";
  }

  public static class Event
  {
    public static string RegionReachable(string input) => new($"{input} Reachable");
  }

  public static class ExtraData
  {
    public static class Key
    {
      public const string DLC = "dlc";
      public const string DLCList = "dlc_list";
      public const string GrantingOption = "granting_option";
      public const string PlayerLevel = "player_level";
      public const string RegionList = "region_list";
      public const string RequireOption = "require_option";
      public const string RequireOptionValue = "require_option_value";
      public const string SecretDeliveryCounter = "secret_delivery_number";
      public const string SecretDeliveryPartCounter = "secret_delivery_part_number";
      public const string State = "state";
      public const string StateList = "state_list";
      public const string Type = "type";
      public const string Which = "which";
    }

    public static class Value
    {
      public const string DLC = "dlc";
      public const string PlayerLevelExternal = "player_level_external";
      public const string PlayerLevelInternal = "player_level_internal";
      public const string PlayerLevelSkill = "player_level_skill";
      public const string RegionReachable = "region_reachable";
      public const string SecretDeliveryLocation = "secret_delivery_location";
      public const string State = "state";
      public const string StateChecks = "state_checks";
      public const string TypeCategories = "type_categories";
      public const string Victory = "victory";
    }
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
    public static string SkillPoint(string name) => $"Skill Point - {name}";
    public static string StateKey(string name) => $"{name} Key";
    public static string StateStarterKey(string name) => $"{name} Starter Key";
    public static string TruckContract(string name) => $"{name} Trucks Purchase Contract";
    public const string Television = "TV";
    public const string TrailerContract = "Trailer Contract";
  }

  public static class Location
  {
    public static string CheckConst(string checkType, string checkName) => $"{checkType} - {checkName}";
    public static string ExternalLevel(int i) => $"Player Level {i} - External";
    public static string InternalLevel(int i) => $"Player Level {i} - Internal";
    public static string SecretDeliveryCompleted(int i) => $"Secret Delivery {i} Completed";
    public static string SkillLevel(int i) => $"Player Level {i} - Skill";
  }

  public static class Option
  {
    public const string BankLoanItem = "bank_loan_approval_item";
    public const string ChecksMaxOverallCount = "checks_max_count";
    public static string ChecksMaxStateCount => $"checks_{StateCountryLC}_count_max";
    public static string ChecksMaxWithinState => $"checks_within_{StateCountryLC}_max";
    public static string ChecksPercentStateCount => $"checks_{StateCountryLC}_chance_percent";
    public const string ChecksPercentWithinState = "checks_chance_percent";
    public const string Citysanity = "enable_citysanity";
    public const string Companysanity = "enable_companysanity";
    public const string Dealersanity = "enable_dealersanity";
    public const string DeliveryTokensAvailable = "delivery_tokens_available";
    public const string DeliveryTokensRequired = "delivery_tokens_required";
    public const string Disabled = "disabled";
    public static string DLC(string dlc) => $"enable_dlc_{SnakeCase(dlc)}";
    public const string EarlyTruckBrand = "early_truck_brand";
    public const string FerryTicketItem = "ferry_ticket_item";
    public const string ItemInPool = "in_item_pool";
    public const string ItemInPoolEarly = "in_item_pool_early";
    public const string ItemInStartingInventory = "in_starting_inventory";
    public const string LevelChecks = "player_level_checks";
    public const string Photosanity = "enable_photosanity";
    public const string PhotosanityFindCamera = "find_camera";
    public const string PhotosanityFindCameraEarly = "find_camera_early";
    public const string PhotosanityStartWithCamera = "start_with_camera";
    public const string QuickTravelTicketItem = "quick_travel_item";
    public const string Random = "random";
    public const string Recruitmentsanity = "enable_recruitmentsanity";
    public const string SecretDeliveriesAvailable = "secret_deliveries_available";
    public const string SecretDeliveriesRequired = "secret_deliveries_required";
    public const string SecretDeliveryInstructionParts = "secret_delivery_instruction_parts";
    public const string SkillScatter = "skill_scatter";
    public const string SkillScatterCondensed = "condensed";
    public const string SkillScatterSpread = "spread";
    public static string State(string state) => $"enable_state_{SnakeCase(state)}";
    public static string StartingState => $"starting_{StateCountryLC}";
    public const string TruckContractItems = "truck_contract_items";
    public const string TruckContractsAllEarly = "all_in_item_pool_early";
    public const string TruckContractsAllRandom = "all_in_item_pool";
    public const string TruckContractsAllStart = "all_in_starting_inventory";
    public static string TruckContractsBrandEarly(string brand) => $"{SnakeCase(brand)}_in_item_pool_early";
    public static string TruckContractsBrandStart(string brand) => $"{SnakeCase(brand)}_in_starting_inventory";
    public const string TruckContractsRandomEarly = "random_in_item_pool_early";
    public const string TruckContractsRandomStart = "random_in_starting_inventory";
    public const string TrailerContractItem = "trailer_contract_item";
    public const string Viewpointsanity = "enable_viewpointsanity";
    public const string ViewpointsanityFindTV = "find_tv";
    public const string ViewpointsanityFindTVEarly = "find_tv_early";
    public const string ViewpointsanityStartWithTV = "start_with_tv";
  }

  public static class OptionGroup
  {
    public const string CheckReduction = "Check Reduction";
    public const string CheckToggles = "Check/Sanity Toggles";
    public const string DLCs = "DLC Toggles";
    public const string DeliveryTokens = "Delivery Tokens";
    public const string ItemRequirements = "Item Requirements";
    public const string PlayerLevels = "Player Levels";
    public const string SecretDeliveries = "Secret Deliveries";
    public const string StartingLocation = "Starting Location";
    public static string States => $"{StateCountry} Toggles";
  }

  public static class Region
  {
    public const string Start = "Start";
  }

  public static class Syntax
  {
    // Non-standard keys
    public const string ExtraData = "extra_data";

    // Standard keys
    public const string Category = "category";
    public const string CategoryHidden = "hidden";
    public const string CategoryYamlOption = "yaml_option";
    public const string CoreOptionDeathlink = "death_link";
    public const string CoreOptionGoal = "goal";
    public const string GameInfoBuild = "build";
    public const string GameInfoCreator = "creator";
    public const string GameInfoDeathLink = "death_link";
    public const string GameInfoFillerItem = "filler_item_name";
    public const string GameInfoGame = "game";
    public const string ItemClassProgression = "progression";
    public const string ItemClassUseful = "useful";
    public const string ItemClassificationCount = "classification_count";
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
    public const string OptionTypeChoice = "Choice";
    public const string OptionTypeRange = "Range";
    public const string OptionTypeToggle = "Toggle";
    public const string OptionValues = "values";
    public const string OptionVisibility = "visibility";
    public const string OptionVisibilityComplexUI = "complex_ui";
    public const string OptionVisibilitySimpleUI = "simple_ui";
    public const string OptionVisibilitySpoiler = "spoiler";
    public const string OptionVisibilityTemplate = "template";
    public const string OptionsCore = "core";
    public const string OptionsUser = "user";
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
    public static string RegionsCheck(int n)
      => $"{{playerLevelRegionsCheck({n})}}";
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
  static JObject WithIf(this JObject input, bool condition, string key, JToken value)
  {
    if (condition) input[key] = value;
    return input;
  }

  static JArray AddIf(this JArray input, bool condition, JToken value)
  {
    if (condition) input.Add(value);
    return input;
  }

  static JProperty KVP(string key, JToken value) => new(key, value);
  static JProperty KVPO(string key) => KVPO(key, new JObject());
  static JProperty KVPO(string key, JObject obj) => new(key, obj);
  static JProperty KVPA(string key, JArray arr) => new(key, arr);
  static JProperty KVPO(string key, IEnumerable<JProperty> obj) => new(key, new JObject(obj));
  static JObject Obj(JObject obj) => obj;
  static JObject Obj(IEnumerable<JProperty> obj) => new(obj);
  static JArray Arr(JArray arr) => arr;

  static JArray Split(string input) => [.. Split1(input)];

  const int YamlWidth = 100;

  static IEnumerable<string> Split1(string input)
  {
    string[] lines = [.. input.Split("\n\n").Select(l => l.Replace("\n", " "))];
    bool isSplit = false;

    foreach (string protoline in lines)
    {
      if (isSplit) yield return "";
      foreach (string line in protoline.Split("\\n"))
      {
        foreach (string lineOut in Split2(line))
        {
          yield return lineOut;
        }
      }
      isSplit = true;
    }
  }

  static IEnumerable<string> Split2(string input)
  {
    while (input.Length > YamlWidth)
    {
      int index;
      if ((index = input.LastIndexOf(' ', YamlWidth)) > -1 || (index = input.IndexOf(' ')) > -1)
      {
        yield return input[..index];
        input = input[(index + 1)..];
      }
      else
      {
        yield return input;
        input = "";
      }
    }
    yield return input;
  }
  #endregion

  #region ├╴game.json
  public static JObject GetGameJson() => new()
  {
    [Str.Syntax.GameInfoGame] = Data.GameInfo["game"],
    [Str.Syntax.GameInfoCreator] = Data.GameInfo["creator"],
    [Str.Syntax.GameInfoFillerItem] = Data.GameInfo["filler_item"],
    [Str.Syntax.GameInfoDeathLink] = true,
    [Str.Syntax.GameInfoBuild] = DateTime.UtcNow.ToString("yyyy-MM-dd HH:mm:ss")
  };
  #endregion

  #region ├╴regions.json
  public static JObject GetRegionsJson() => Obj([
    GetStartRegion(),
    .. GetRegionRegions()
  ]);

  public static JProperty GetStartRegion() => KVPO(Str.Region.Start, [
    KVP(Str.Syntax.RegionStarting, true),
    KVPA(Str.Syntax.RegionConnectsTo, [.. Data.Regions.Select(r => r.ToString())]),
    KVPO(Str.Syntax.RegionExitRequires, [.. GetStarterExitRequirements()])
  ]);

  public static IEnumerable<JProperty> GetStarterExitRequirements()
  {
    foreach (var region in Data.Regions)
    {
      if (Data.QuickTravel.Contains(region)) yield return KVP($"{region}",
        $"|{Str.Item.StateStarterKey(region.StateName)}| or |{Str.Item.QuickTravelTicket}|");
      else yield return KVP($"{region}", $"|{Str.Item.StateStarterKey(region.StateName)}|");
    }
  }

  public static IEnumerable<JProperty> GetRegionRegions()
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
      Region[] ferries = ferryConnections.GetValueOrDefault(region, []);

      JObject obj = Obj([
        KVP(Str.Syntax.Requires,
          $"|{Str.Item.StateKey(region.StateName)}| or |{Str.Item.StateStarterKey(region.StateName)}|"),
        KVPA(Str.Syntax.RegionConnectsTo, [.. connections.Select(r => $"{r}")])
      ]);

      if (ferries.Length > 0)
      {
        obj[Str.Syntax.RegionExitRequires]
          = Obj([.. ferries.Select(fc => KVP($"{fc}", $"|{Str.Item.FerryTicket}|"))]);
      }

      yield return KVP(region.ToString(), obj);
    }
  }
  #endregion

  #region ├╴locations.json
  public static JArray GetLocationsJson() => [
    .. GetCityLocations(),
    .. GetPhotoTrophyLocations(),
    .. GetViewpointLocations(),
    .. GetCompanyLocations(),
    .. GetInternalLevelLocations(),
    .. GetExternalLevelLocations(),
    .. GetSkillLevelLocations(),
    .. GetSecretDeliveryLocations(),
    .. GetVictoryLocations()
  ];

  public static IEnumerable<JToken> GetCheckLocations(string name, IEnumerable<Check> checks,
    string? globalRequire = null)
  {
    foreach (Check check in checks)
    {
      yield return Obj([
        KVP(Str.Syntax.Name, Str.Location.CheckConst(name, check.Name)),
        KVPA(Str.Syntax.Category, [
          name,
          Str.Category.State(check.Region.StateName),
          Str.Category.StateCheck(check.Region.StateName),
          Str.Category.DLC(check.Region.DLCName)
        ]),
        KVPO(Str.Syntax.ExtraData, [
          KVP(Str.ExtraData.Key.Type, Str.SnakeCase(name)),
          KVP(Str.ExtraData.Key.Which, check.Name)
        ]),
        KVP(Str.Syntax.Region, check.Region.ToString())
      ]).WithIf(globalRequire != null && check.FerryRequired, Str.Syntax.Requires,
        $"({globalRequire}) and |{Str.Item.FerryTicket}|")
      .WithIf(globalRequire == null && check.FerryRequired, Str.Syntax.Requires, $"|{Str.Item.FerryTicket}|")
      .WithIf(globalRequire != null && !check.FerryRequired, Str.Syntax.Requires, globalRequire);
    }
  }

  public static IEnumerable<JToken> GetCityLocations() => GetCheckLocations(Str.Category.City, Data.Cities.Values);
  public static IEnumerable<JToken> GetPhotoTrophyLocations()
    => GetCheckLocations(Str.Category.PhotoTrophy, Data.PhotoTrophies, $"|{Str.Item.Camera}|");
  public static IEnumerable<JToken> GetViewpointLocations()
    => GetCheckLocations(Str.Category.Viewpoint, Data.Viewpoints, $"|{Str.Item.Television}|");

  public static IEnumerable<JToken> GetCompanyLocations()
  {
    Dictionary<string, Region[]> locations = Data.CompanyLocations.GroupBy(c => c.Name)
      .Select(grp => KeyValuePair.Create(grp.Key, grp.Select(c => c.Region).ToArray()))
      .ToDictionary();

    foreach (string company in Data.Companies.Keys)
    {
      var thisCoLoc = locations[company];

      var requires = string.Join(" or ", thisCoLoc.Select(r => $"|{Str.Event.RegionReachable(r.ToString())}|"));
      JToken dlcList = thisCoLoc.Any(r => r.DLCName == Str.DLC.BaseGame)
        ? false
        : (JArray)([.. thisCoLoc.Select(r => Str.SnakeCase(r.DLCName)).Distinct()]);

      yield return Obj([
        KVP(Str.Syntax.Name, Str.Location.CheckConst(Str.Category.Company, company)),
        KVPA(Str.Syntax.Category, [
          Str.Category.Company,
          Str.Category.VisibleCompany
        ]),
        KVP(Str.Syntax.Requires, requires),
        KVPO(Str.Syntax.ExtraData, [
          KVP(Str.ExtraData.Key.Type, Str.SnakeCase(Str.Category.Company)),
          KVP(Str.ExtraData.Key.Which, company),
          KVP(Str.ExtraData.Key.DLCList, dlcList),
          KVPA(Str.ExtraData.Key.StateList, [.. thisCoLoc.Select(r => r.StateName).Distinct()]),
          KVPA(Str.ExtraData.Key.RegionList, [.. thisCoLoc.Select(r => Obj([
            KVP(Str.ExtraData.Key.DLC, r.DLCName),
            KVP(Str.ExtraData.Key.State, r.StateName)
          ]))])
        ])
      ]);
    }
  }

  public static IEnumerable<JToken> GetInternalLevelLocations()
    => Enumerable.Range(1, 36).Select(i => Obj([
      KVP(Str.Syntax.Name, Str.Location.InternalLevel(i)),
      KVP(Str.Syntax.Requires, $"|{Str.Item.LevelItem}:{i-1}| and {Str.Syntax.RegionsCheck(i)}"),
      KVPA(Str.Syntax.Category, [Str.Category.VisibleLevelUp]),
      KVPA(Str.Syntax.LocationPlaceItem, [ Str.Item.LevelItem ]),
      KVPO(Str.Syntax.ExtraData, [
        KVP(Str.ExtraData.Key.Type, Str.ExtraData.Value.PlayerLevelInternal),
        KVP(Str.ExtraData.Key.PlayerLevel, i)
      ])
    ]));

  public static IEnumerable<JToken> GetExternalLevelLocations()
    => Enumerable.Range(1, 36).Select(i => Obj([
      KVP(Str.Syntax.Name, Str.Location.ExternalLevel(i)),
      KVP(Str.Syntax.Requires, $"|{Str.Item.LevelItem}:{i-1}| and {Str.Syntax.RegionsCheck(i)}"),
      KVPA(Str.Syntax.Category, [Str.Category.VisibleLevelUp]),
      KVPO(Str.Syntax.ExtraData, [
        KVP(Str.ExtraData.Key.Type, Str.ExtraData.Value.PlayerLevelExternal),
        KVP(Str.ExtraData.Key.PlayerLevel, i)
      ])
    ]));

  public static IEnumerable<JToken> GetSkillLevelLocations()
    => Enumerable.Range(1, 36).Select(i => Obj([
      KVP(Str.Syntax.Name, Str.Location.SkillLevel(i)),
      KVP(Str.Syntax.Requires, $"|{Str.Item.LevelItem}:{i-1}| and {Str.Syntax.RegionsCheck(i)}"),
      KVPA(Str.Syntax.Category, [Str.Category.VisibleLevelUp]),
      KVPA(Str.Syntax.LocationPlaceItemCategory, [ Str.Category.PlayerSkill ]),
      KVPO(Str.Syntax.ExtraData, [
        KVP(Str.ExtraData.Key.Type, Str.ExtraData.Value.PlayerLevelSkill),
        KVP(Str.ExtraData.Key.PlayerLevel, i)
      ])
    ]));

  public static IEnumerable<JToken> GetSecretDeliveryLocations()
  {
    foreach (int i in Enumerable.Range(1, 20))
    {
      yield return Obj([
        KVP(Str.Syntax.Name, Str.Location.SecretDeliveryCompleted(i)),
        KVPA(Str.Syntax.Category, [ Str.Category.SecretDeliveries ]),
        KVP(Str.Syntax.Requires, Str.Syntax.OptionCount(Str.Item.SecretDeliveryInstruction(i),
          Str.Option.SecretDeliveryInstructionParts)),
        KVPA(Str.Syntax.LocationPlaceItem, [Str.Item.SecretDeliveryCompletion]),
        KVPO(Str.Syntax.ExtraData, [
          KVP(Str.ExtraData.Key.Type, Str.ExtraData.Value.SecretDeliveryLocation),
          KVP(Str.ExtraData.Key.SecretDeliveryCounter, i)
        ])
      ]);
    }
  }

  public static IEnumerable<JToken> GetVictoryLocations() => [
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
      KVP(Str.Syntax.Requires, Str.Syntax.OptionCount(Str.Item.LevelItem, Str.Option.LevelChecks)),
      KVP(Str.Syntax.LocationVictory, true)
    ])
  ];
  #endregion

  #region ├╴items.json
  public static JArray GetItemsJson() => [
    .. GetStateKeyItems(),
    .. GetStarterKeyItems(),
    .. GetTruckContractItems(),
    .. GetSecretDeliveryInstructionItems(),
    .. GetSecretDeliveryCompletionItems(),
    .. GetPlayerSkillItems(),
    .. GetSingleItems()
  ];

  public static IEnumerable<JToken> GetStateKeyItems()
  {
    Dictionary<string, string[]> regions = Data.Regions.GroupBy(c => c.StateName)
      .Select(grp => KeyValuePair.Create(grp.Key, grp.Select(c => c.DLCName).ToArray()))
      .ToDictionary();

    foreach (var state in Data.States.Keys)
    {
      JToken dlcList = regions[state].Any(r => r == Str.DLC.BaseGame)
        ? false
        : (JArray)([.. regions[state].Select(r => Str.SnakeCase(r)).Distinct()]);

      yield return Obj([
        KVP(Str.Syntax.Name, Str.Item.StateKey(state)),
        KVPA(Str.Syntax.Category, [
          Str.Category.StateKey,
          Str.Category.State(state),
          Str.Category.VisibleStateKeys
        ]),
        KVPO(Str.Syntax.ExtraData, [
          KVP(Str.ExtraData.Key.Type, Str.SnakeCase(Str.Category.StateKeyConst)),
          KVP(Str.ExtraData.Key.Which, state),
          KVP(Str.ExtraData.Key.DLCList, dlcList)
        ]),
        KVP(Str.Syntax.ItemClassProgression, true)
      ]);
    }
  }

  public static IEnumerable<JToken> GetStarterKeyItems()
  {
    Dictionary<string, string[]> regions = Data.Regions.GroupBy(c => c.StateName)
      .Select(grp => KeyValuePair.Create(grp.Key, grp.Select(c => c.DLCName).ToArray()))
      .ToDictionary();

    foreach (var state in Data.States.Keys)
    {
      JToken dlcList = regions[state].Any(r => r == Str.DLC.BaseGame)
        ? false
        : (JArray)([.. regions[state].Select(r => Str.SnakeCase(r)).Distinct()]);

      yield return Obj([
        KVP(Str.Syntax.Name, Str.Item.StateStarterKey(state)),
        KVPA(Str.Syntax.Category, [
          Str.Category.StateStarterKey,
          Str.Category.StateCheck(state)
        ]),
        KVPO(Str.Syntax.ExtraData, [
          KVP(Str.ExtraData.Key.Type, Str.SnakeCase(Str.Category.StateStarterKeyConst)),
          KVP(Str.ExtraData.Key.Which, state),
          KVP(Str.ExtraData.Key.DLCList, dlcList)
        ]),
        KVP(Str.Syntax.ItemClassProgression, true)
      ]);
    }
  }

  public static IEnumerable<JToken> GetTruckContractItems()
    => Data.TruckMakes.Keys.Select(truck => Obj([
        KVP(Str.Syntax.Name, Str.Item.TruckContract(truck)),
        KVPA(Str.Syntax.Category, [
          Str.Category.TruckContract,
          Str.Category.VisibleMiscItems
        ]),
        KVPO(Str.Syntax.ExtraData, [
          KVP(Str.ExtraData.Key.Type, Str.SnakeCase(Str.Category.TruckContract)),
          KVP(Str.ExtraData.Key.Which, truck)
        ]),
        KVP(Str.Syntax.ItemClassUseful, true)
      ]));

  public static IEnumerable<JToken> GetSecretDeliveryInstructionItems()
    => Enumerable.Range(1, 20).Select(i => Obj([
      KVP(Str.Syntax.Name, Str.Item.SecretDeliveryInstruction(i)),
      KVPA(Str.Syntax.Category, [
        Str.Category.SecretDeliveries,
        Str.Category.SecretDeliveryInstructions,
        Str.Category.VisibleSecretDeliveryInstructions
      ]),
      KVPO(Str.Syntax.ExtraData, [
        KVP(Str.ExtraData.Key.Type, Str.SnakeCase(Str.Category.SecretDeliveryInstructions)),
        KVP(Str.ExtraData.Key.SecretDeliveryCounter, i)
      ]),
      KVP(Str.Syntax.ItemClassProgression, true),
      KVP(Str.Syntax.ItemCount, 5)
    ]));

  public static IEnumerable<JToken> GetSecretDeliveryCompletionItems()
    => [Obj([
      KVP(Str.Syntax.Name, Str.Item.SecretDeliveryCompletion),
      KVPA(Str.Syntax.Category, [
        Str.Category.SecretDeliveries,
        Str.Category.SecretDeliveryCompletions
      ]),
      KVP(Str.Syntax.ItemClassProgression, true),
      KVP(Str.Syntax.ItemCount, 20),
      KVPO(Str.Syntax.ExtraData, [
        KVP(Str.ExtraData.Key.Type, Str.SnakeCase(Str.Category.SecretDeliveryCompletions))
      ])
    ])];

  public static IEnumerable<JToken> GetPlayerSkillItems()
    => Sequence.Of<(string Name, int Progression, int Useful, string Type)>(
      ("ADR Class 1 (Explosives)", 1, 0, "adr"),
      ("ADR Class 2 (Gases)", 1, 0, "adr"),
      ("ADR Class 3 (Flammable Liquids)", 1, 0, "adr"),
      ("ADR Class 4 (Flammable Solids)", 1, 0, "adr"),
      ("ADR Class 6 (Toxic/Infectious Substances)", 1, 0, "adr"),
      ("ADR Class 8 (Corrosive Substances)", 1, 0, "adr"),
      ("Long Distance", 6, 0, "long_distance"),
      ("High Value Cargo", 1, 5, "high_value"),
      ("Fragile Cargo", 1, 5, "fragile"),
      ("Just-In-Time Delivery", 2, 4, "just_in_time"),
      ("Eco-Driving", 0, 6, "eco_driving")
    ).Select(t => Obj([
      KVP(Str.Syntax.Name, Str.Item.SkillPoint(t.Name)),
      KVPO(Str.Syntax.ItemClassificationCount, [
        KVP(Str.Syntax.ItemClassProgression, t.Progression),
        KVP(Str.Syntax.ItemClassUseful, t.Useful)
      ]),
      KVPA(Str.Syntax.Category, [
        Str.Category.PlayerSkill,
        Str.Category.VisiblePlayerSkills
      ]),
      KVPO(Str.Syntax.ExtraData, [
        KVP(Str.ExtraData.Key.Type, Str.SnakeCase(Str.Category.PlayerSkill)),
        KVP(Str.ExtraData.Key.Which, t.Type)
      ])
    ]));

  public static IEnumerable<JToken> GetSingleItems() => [
    Obj([
      KVP(Str.Syntax.Name, Str.Item.DeliveryToken),
      KVPA(Str.Syntax.Category, [
        Str.Category.DeliveryTokens,
        Str.Category.VisibleMiscItems
      ]),
      KVP(Str.Syntax.ItemClassProgression, true),
      KVP(Str.Syntax.ItemCount, 100),
      KVPO(Str.Syntax.ExtraData, [
        KVP(Str.ExtraData.Key.Type, Str.SnakeCase(Str.Item.DeliveryToken))
      ])
    ]),

    Obj([
      KVP(Str.Syntax.Name, Str.Item.LevelItem),
      KVPA(Str.Syntax.Category, [Str.Category.Level]),
      KVP(Str.Syntax.ItemClassProgression, true),
      KVP(Str.Syntax.ItemCount, 36),
      KVPO(Str.Syntax.ExtraData, [
        KVP(Str.ExtraData.Key.Type, Str.SnakeCase(Str.Item.LevelItem))
      ])
    ]),

    Obj([
      KVP(Str.Syntax.Name, Str.Item.FerryTicket),
      KVPA(Str.Syntax.Category, [Str.Category.VisibleMiscItems]),
      KVP(Str.Syntax.ItemClassProgression, true),
      KVPO(Str.Syntax.ExtraData, [
        KVP(Str.ExtraData.Key.Type, Str.SnakeCase(Str.Item.FerryTicket)),
        KVP(Str.ExtraData.Key.GrantingOption, Str.Option.FerryTicketItem)
      ])
    ]),

    Obj([
      KVP(Str.Syntax.Name, Str.Item.Camera),
      KVPA(Str.Syntax.Category, [
        Str.Category.PhotoTrophy,
        Str.Category.VisibleMiscItems
      ]),
      KVP(Str.Syntax.ItemClassProgression, true),
      KVPO(Str.Syntax.ExtraData, [
        KVP(Str.ExtraData.Key.Type, Str.SnakeCase(Str.Category.PhotoTrophy)),
        KVP(Str.ExtraData.Key.GrantingOption, Str.Option.Photosanity)
      ])
    ]),

    Obj([
      KVP(Str.Syntax.Name, Str.Item.Television),
      KVPA(Str.Syntax.Category, [
        Str.Category.Viewpoint,
        Str.Category.VisibleMiscItems
      ]),
      KVP(Str.Syntax.ItemClassProgression, true),
      KVPO(Str.Syntax.ExtraData, [
        KVP(Str.ExtraData.Key.Type, Str.SnakeCase(Str.Category.Viewpoint)),
        KVP(Str.ExtraData.Key.GrantingOption, Str.Option.Viewpointsanity)
      ])
    ]),

    Obj([
      KVP(Str.Syntax.Name, Str.Item.BankLoan),
      KVPA(Str.Syntax.Category, [Str.Category.VisibleMiscItems]),
      KVP(Str.Syntax.ItemClassProgression, true),
      KVPO(Str.Syntax.ExtraData, [
        KVP(Str.ExtraData.Key.Type, Str.SnakeCase(Str.Item.BankLoan)),
        KVP(Str.ExtraData.Key.GrantingOption, Str.Option.BankLoanItem)
      ])
    ]),

    Obj([
      KVP(Str.Syntax.Name, Str.Item.TrailerContract),
      KVPA(Str.Syntax.Category, [Str.Category.VisibleMiscItems]),
      KVP(Str.Syntax.ItemClassUseful, true),
      KVPO(Str.Syntax.ExtraData, [
        KVP(Str.ExtraData.Key.Type, Str.SnakeCase(Str.Item.TrailerContract)),
        KVP(Str.ExtraData.Key.GrantingOption, Str.Option.TrailerContractItem)
      ])
    ]),

    Obj([
      KVP(Str.Syntax.Name, Str.Item.QuickTravelTicket),
      KVPA(Str.Syntax.Category, [Str.Category.VisibleMiscItems]),
      KVP(Str.Syntax.ItemClassProgression, true),
      KVPO(Str.Syntax.ExtraData, [
        KVP(Str.ExtraData.Key.Type, Str.SnakeCase(Str.Item.QuickTravelTicket)),
        KVP(Str.ExtraData.Key.GrantingOption, Str.Option.QuickTravelTicketItem)
      ])
    ])
  ];
  #endregion

  #region ├╴categories.json
  public static JObject GetCategoriesJson() => Obj([
    .. GetVictoryCategories(),
    .. GetStateCategories(),
    .. GetStateCheckCategories(),
    .. GetDLCCategories(),
    .. GetTypeCategories(),
    .. GetVisibleItemCategories()
  ]);

  public static IEnumerable<JProperty> GetVictoryCategories() => [
    KVPO(Str.Category.DeliveryTokens, [
      KVPO(Str.Syntax.ExtraData, [
        KVP(Str.ExtraData.Key.Type, Str.ExtraData.Value.Victory),
        KVP(Str.ExtraData.Key.Which, Str.SnakeCase(Str.Category.DeliveryTokens))
      ])
    ]),

    KVPO(Str.Category.SecretDeliveries, [
      KVPO(Str.Syntax.ExtraData, [
        KVP(Str.ExtraData.Key.Type, Str.ExtraData.Value.Victory),
        KVP(Str.ExtraData.Key.Which, Str.SnakeCase(Str.Category.SecretDeliveries))
      ])
    ]),

    KVPO(Str.Category.SecretDeliveryCompletions, [
      KVP(Str.Syntax.CategoryHidden, true),
      KVPO(Str.Syntax.ExtraData, [
        KVP(Str.ExtraData.Key.Type, Str.ExtraData.Value.Victory),
        KVP(Str.ExtraData.Key.Which, Str.SnakeCase(Str.Category.SecretDeliveries))
      ])
    ]),

    KVPO(Str.Category.SecretDeliveryInstructions, [
      KVP(Str.Syntax.CategoryHidden, true),
      KVPO(Str.Syntax.ExtraData, [
        KVP(Str.ExtraData.Key.Type, Str.ExtraData.Value.Victory),
        KVP(Str.ExtraData.Key.Which, Str.SnakeCase(Str.Category.SecretDeliveries))
      ])
    ]),
  ];

  public static IEnumerable<JProperty> GetStateCategories()
    => Data.States.Keys.Select(s => KVPO(Str.Category.State(s), [
      KVPO(Str.Syntax.ExtraData, [
        KVP(Str.ExtraData.Key.Type, Str.ExtraData.Value.State),
        KVP(Str.ExtraData.Key.Which, s),
        KVP(Str.ExtraData.Key.DLCList, Data.Regions.Any(r => r.StateName == s && r.DLCName == Str.DLC.BaseGame)
          ? false : Arr([.. Data.Regions.Where(r => r.StateName == s).Select(r => r.DLCName)]))
      ])
    ]));

  public static IEnumerable<JProperty> GetDLCCategories()
    => Data.DLCs.Keys
      .Select(d => KVPO(Str.Category.DLC(d), [
        KVP(Str.Syntax.CategoryHidden, true),
        KVPO(Str.Syntax.ExtraData, [
          KVP(Str.ExtraData.Key.Type, Str.ExtraData.Value.DLC),
          KVP(Str.ExtraData.Key.Which, d)
        ])
      ]));

  public static IEnumerable<JProperty> GetStateCheckCategories()
    => Data.States.Keys.Select(s => KVPO(Str.Category.StateCheck(s), [
      KVP(Str.Syntax.CategoryHidden, true),
      KVPO(Str.Syntax.ExtraData, [
        KVP(Str.ExtraData.Key.Type, Str.ExtraData.Value.StateChecks),
        KVP(Str.ExtraData.Key.Which, s),
        KVP(Str.ExtraData.Key.DLCList, Data.Regions.Any(r => r.StateName == s && r.DLCName == Str.DLC.BaseGame)
          ? false : Arr([.. Data.Regions.Where(r => r.StateName == s).Select(r => r.DLCName)]))
      ])
    ]));

  public static IEnumerable<JProperty> GetTypeCategories() => [
    GetTypeCategory(Str.Category.City, Str.Option.Citysanity),
    GetTypeCategory(Str.Category.Viewpoint, Str.Option.Viewpointsanity),
    GetTypeCategory(Str.Category.PhotoTrophy, Str.Option.Photosanity),
    GetTypeCategory(Str.Category.Company, Str.Option.Companysanity)/* ,
    // GetTypeCategory(Str.Category.RecruitmentAgent, Str.Option.Recruitmentsanity),
    // GetTypeCategory(Str.Category.TruckDealer, Str.Option.Dealersanity) */,
    GetTypeCategory(Str.Category.Level),
    GetTypeCategory(Str.Category.PlayerSkill),
    GetTypeCategory(Str.Category.StateKey),
    GetTypeCategory(Str.Category.StateStarterKey),
    GetTypeCategory(Str.Category.TruckContract),
    GetTypeCategory(Str.Category.RegionReachableEvent)
  ];

  public static JProperty GetTypeCategory(string name, string? option = null, bool hidden = true)
    => new(name, Obj([
        KVP(Str.Syntax.CategoryHidden, hidden),
        KVPO(Str.Syntax.ExtraData, [
          KVP(Str.ExtraData.Key.Type, Str.ExtraData.Value.TypeCategories),
          KVP(Str.ExtraData.Key.Which, Str.SnakeCase(name))
        ])
      ]).WithIf(option != null, Str.Syntax.CategoryYamlOption, new JArray([option])));

  public static IEnumerable<JProperty> GetVisibleItemCategories() => [
    KVPO(Str.Category.VisibleStateKeys),
    KVPO(Str.Category.VisibleSecretDeliveryInstructions),
    KVPO(Str.Category.VisiblePlayerSkills),
    KVPO(Str.Category.VisibleMiscItems),
    KVPO(Str.Category.VisibleCompany),
    KVPO(Str.Category.VisibleLevelUp)
  ];
  #endregion

  #region ├╴events.json
  public static JArray GetEventsJson() => [
    .. GetRegionEvents()
  ];

  public static IEnumerable<JToken> GetRegionEvents()
    => Data.Regions.Select(r => Obj([
      KVP(Str.Syntax.Name, Str.Event.RegionReachable(r.ToString())),
      KVPA(Str.Syntax.Category, [
        Str.Category.State(r.StateName),
        Str.Category.DLC(r.DLCName),
        Str.Category.RegionReachableEvent
      ]),
      KVP(Str.Syntax.Region, r.ToString()),
      KVPO(Str.Syntax.ExtraData, [
        KVP(Str.ExtraData.Key.Type, Str.ExtraData.Value.RegionReachable),
        KVP(Str.ExtraData.Key.State, r.StateName),
        KVP(Str.ExtraData.Key.DLC, r.DLCName)
      ])
    ]));
  #endregion

  #region └╴options.json
  // public static JObject GetOptionsJson() => Obj([
  //   KVP(Str.Syntax.OptionsCore, GetCoreOptions()),
  //   KVP(Str.Syntax.OptionsUser, GetUserOptions())
  // ]);

  // public static JObject GetCoreOptions() => Obj([
  //   KVP(Str.Syntax.CoreOptionDeathlink, Obj([
  //     KVPA(Str.Syntax.OptionDescription, Split($"""
  //       Enable or disable death link support. If enabled:

  //       Upon receiving a death, the player must get towed or navigate to
  //       the nearest service station.

  //       Upon being towed to a service station or completing a delivery
  //       with over 5% cargo damage, the player must send a death.
  //       """))
  //   ])),
  //   KVP(Str.Syntax.CoreOptionGoal, Obj([
  //     KVPA(Str.Syntax.OptionDescription, Split($"""
  //       Goal condition:

  //       {Str.Victory.DeliveryTokensCollected}: Collect a certain number of
  //       Delivery Tokens (see the "{Str.OptionGroup.DeliveryTokens}" group
  //       of the options), then activate the win button to win.

  //       {Str.Victory.SecretDeliveriesCompleted}: Collect instructions for
  //       secret deliveries (see the "{Str.OptionGroup.SecretDeliveries}"
  //       group of the options, and the patch file from the multiworld
  //       host), then follow those instructions to win.

  //       {Str.Victory.PlayerLevelReached}: Reach a certain level in career
  //       progression (see the "{Str.Option.LevelChecks}" option), then
  //       activate the win button to win.
  //       """))
  //   ]))
  // ]);

  // public static JObject GetUserOptions() => Obj([
  //   .. GetStartingLocationOption(),
  //   .. GetDeliveryTokensOptions(),
  //   .. GetSecretDeliveryOptions(),
  //   .. GetDLCOptions(),
  //   .. GetStateOptions(),
  //   .. GetChecksOptions(),
  //   .. GetLevelsOptions(),
  //   .. GetItemRequiresOptions(),
  //   .. GetChecksReductionOptions()
  // ]);

  // static JProperty ToggleOption(string name, string displayName, string description,
  //   bool defaultValue) => KVPO(name, [
  //     KVP(Str.Syntax.OptionDisplayName, displayName),
  //     KVPA(Str.Syntax.OptionDescription, Split(description)),
  //     KVP(Str.Syntax.OptionType, Str.Syntax.OptionTypeToggle),
  //     KVP(Str.Syntax.OptionDefaultValue, defaultValue)
  //   ]);

  // static JProperty RangeOption(string name, string displayName, string description,
  //   int rangeStart, int rangeEnd, int defaultValue, params (string Name, int Value)[] values) => KVPO(name, Obj([
  //     KVP(Str.Syntax.OptionDisplayName, displayName),
  //     KVPA(Str.Syntax.OptionDescription, Split(description)),
  //     KVP(Str.Syntax.OptionType, Str.Syntax.OptionTypeRange),
  //     KVP(Str.Syntax.OptionRangeStart, rangeStart),
  //     KVP(Str.Syntax.OptionRangeEnd, rangeEnd),
  //     KVP(Str.Syntax.OptionDefaultValue, defaultValue)
  //   ]).WithIf(values.Length > 0, Str.Syntax.OptionValues, Obj([.. values.Select(t => KVP(t.Name, t.Value))])));

  // static JProperty ChoiceOption(string name, string displayName, string description,
  //   int defaultValue, params (string Name, int Value)[] values) => KVPO(name, [
  //     KVP(Str.Syntax.OptionDisplayName, displayName),
  //     KVPA(Str.Syntax.OptionDescription, Split(description)),
  //     KVP(Str.Syntax.OptionType, Str.Syntax.OptionTypeChoice),
  //     KVPO(Str.Syntax.OptionValues, [.. values.Select(t => KVP(t.Name, t.Value))]),
  //     KVP(Str.Syntax.OptionDefaultValue, defaultValue)
  //   ]);

  // static IEnumerable<JProperty> OptionGroup(string group,
  //   params IEnumerable<JProperty> options)
  // {
  //   foreach (JProperty prop in options)
  //   {
  //     if (prop.Value is JObject obj) obj[Str.Syntax.OptionGroup] = group;
  //   }
  //   return options;
  // }

  // public static IEnumerable<JProperty> GetStartingLocationOption() => OptionGroup(
  //   Str.OptionGroup.StartingLocation,

  //   ChoiceOption(Str.Option.StartingState, $"Starting {Str.StateCountry}", $"""
  //     Which {Str.StateCountryLC} should the player start in?

  //     If that {Str.StateCountryLC} doesn't exist because of disabled DLC,
  //     this option gets set to random. If the selected {Str.StateCountryLC}'s
  //     checks are disabled, they are re-enabled.
  //     """, 0, [.. Sequence.Of([
  //       Str.Option.Random,
  //       .. Data.States.Keys.Select(s => Str.SnakeCase(s))
  //     ]).Select((s, i) => (s, i))])
  // );

  // public static IEnumerable<JProperty> GetDeliveryTokensOptions() => OptionGroup(
  //   Str.OptionGroup.DeliveryTokens,

  //   RangeOption(Str.Option.DeliveryTokensAvailable, "Available Delivery Tokens", $"""
  //     Number of Delivery Tokens available in the multiworld item pool.

  //     If the number of items exceeds the number of locations, this value
  //     may be reduced to accommodate. If so, the {Str.Option.DeliveryTokensRequired}
  //     option will be reduced proportionally.
  //     """, 1, 100, 25),

  //   RangeOption(Str.Option.DeliveryTokensRequired, "Required Delivery Tokens", $"""
  //     Number of Delivery Tokens needed to win. This value must not exceed
  //     {Str.Option.DeliveryTokensAvailable}, and this value will
  //     automatically be reduced to that value if applicable.

  //     If the number of items exceeds the number of locations,
  //     {Str.Option.DeliveryTokensAvailable} may be reduced to accommodate.
  //     If so, this option will be reduced proportionally.
  //     """, 1, 100, 25)
  // );

  // public static IEnumerable<JProperty> GetSecretDeliveryOptions() => OptionGroup(
  //   Str.OptionGroup.SecretDeliveries,

  //   RangeOption(Str.Option.SecretDeliveriesAvailable, "Secret Deliveries Available", $"""
  //     Number of total Secret Deliveries available.

  //     If the number of items exceeds the number of locations, this option
  //     may be reduced to accommodate. If so, {Str.Option.SecretDeliveriesRequired}
  //     will be reduced proportionally. {Str.Option.SecretDeliveryInstructionParts}
  //     will not be reduced.
  //     """, 1, 20, 10),

  //   RangeOption(Str.Option.SecretDeliveriesRequired, "Secret Deliveries Required", $"""
  //     Number of Secret Deliveries that must be completed to goal. Must not
  //     exceed {Str.Option.SecretDeliveriesAvailable}, and this value will
  //     automatically be reduced to that value if applicable.

  //     If the number of items exceeds the number of locations,
  //     {Str.Option.SecretDeliveriesAvailable} may be reduced to
  //     accommodate. If so, this option will be reduced proportionally.
  //     {Str.Option.SecretDeliveryInstructionParts} will not be reduced.
  //     """, 1, 20, 10),

  //   RangeOption(Str.Option.SecretDeliveryInstructionParts, "Secret Delivery Instruction Parts", $"""
  //     Number of separate parts to the instructions of each Secret
  //     Delivery.

  //     Not all parts must be found in order to perform a Secret Delivery;
  //     once the instructions are decipherable, the delivery may be
  //     performed.

  //     This option will not be affected by location truncation.
  //     """, 1, 5, 2)
  // );

  // public static IEnumerable<JProperty> GetDLCOptions() => OptionGroup(
  //   Str.OptionGroup.DLCs,

  //   Data.DLCs.Keys.Select(dlc => ToggleOption(Str.Option.DLC(dlc), $"Enable {dlc} DLC", $"""
  //     Whether or not the {dlc} DLC, and all the checks within its
  //     bounds, should be enabled for this AP.
  //     """, false))
  // );

  // public static IEnumerable<JProperty> GetStateOptions() => OptionGroup(
  //   Str.OptionGroup.States,

  //   Data.States.Keys.Select(state => ToggleOption(Str.Option.State(state), $"Enable the {Str.StateCountry} of {state}",
  //     $"""
  //     Whether or not the {Str.StateCountry} of {state}, and all checks
  //     within its bounds, as well as its starter key, should be enabled for
  //     this AP.

  //     Regardless of the value below, the {Str.Item.StateKey(state)} will
  //     still spawn, and be required before traveling within this {Str.StateCountryLC}.
  //     """, true))
  // );

  // public static IEnumerable<JProperty> GetChecksOptions() => OptionGroup(
  //   Str.OptionGroup.CheckToggles,

  //   ToggleOption(Str.Option.Citysanity, "Enable Citysanity", $"""
  //     Whether or not cities should be checks. If so, the check is
  //     performed by driving into the city; the check may be cleared when
  //     the "(City Name) Discovered" popup appears.
  //     """, true),

  //   ToggleOption(Str.Option.Companysanity, "Enable Companysanity", $"""
  //     Whether or not companies should be checks. If so, the player may
  //     choose one of the following:\n
  //     - A check is performed when driving onto any of that company's
  //     depots. (The check may be cleared when the map tile turns yellow.)\n
  //     - A check is performed when performing a delivery to that company.
  //     (The check may be cleared when the results screen appears.)\n
  //     - A check is performed when performing a delivery to or for that
  //     company. (The checm kay be cleared when the results screen appears.)
  //     """, false),

  //   ChoiceOption(Str.Option.Photosanity, "Enable Photosanity", $"""
  //     Whether or not photo trophies should be checks. If so, the check is
  //     performed when you take the photo with the name of the monument on
  //     the screen.

  //     The {Str.Item.Camera} item is required before you can take photos,
  //     but you can choose to start with it in your inventory.
  //     """, 0, [
  //       (Str.Option.Disabled, 0),
  //       (Str.Option.PhotosanityStartWithCamera, 1),
  //       (Str.Option.PhotosanityFindCameraEarly, 2),
  //       (Str.Option.PhotosanityFindCamera, 3)
  //     ]),

  //   ChoiceOption(Str.Option.Viewpointsanity, "Enable Viewpointsanity", $"""
  //     Whether or not viewpoints should be checks. If so, the check is
  //     performed when you finish watching the viewpoint cutscene and
  //     control is returned to the player.

  //     The {Str.Item.Television} item is required before you can watch
  //     viewpoints, but you can choose to start with it in your inventory.
  //     """, 0, [
  //       (Str.Option.Disabled, 0),
  //       (Str.Option.ViewpointsanityStartWithTV, 1),
  //       (Str.Option.ViewpointsanityFindTVEarly, 2),
  //       (Str.Option.ViewpointsanityFindTV, 3)
  //     ])/* ,

  //   ToggleOption(Str.Option.Dealersanity, "Enable Dealersanity", $"""
  //     Whether or not truck dealers should be checks. If so, the check is
  //     performed when the "(Brand) Truck Dealer Discovered" message appears
  //     and the ? icon on the map changes to a truck icon. Entering the
  //     truck dealer property is not required.
  //     """, false),

  //   ToggleOption(Str.Option.Recruitmentsanity, "Enable Recruitsanity", $"""
  //     Whether or not recruitment agencies should be checks. If so, the
  //     check is performed when the "You have discovered a recruitment
  //     agency" message appears and the ? icon on the map changes to a
  //     magnifying glass icon. Entering the recruitment agency property is
  //     not required.
  //     """, false) */
  // );

  // public static IEnumerable<JProperty> GetLevelsOptions() => OptionGroup(
  //   Str.OptionGroup.PlayerLevels,

  //   RangeOption(Str.Option.LevelChecks, "Player Level Checks", $"""
  //     How many player levels should be checks? All levels from 1 to the
  //     specified number will be included. The check is performed when the
  //     level shown on the left side of the bar is at least the level being
  //     checked.

  //     If this is set to 0, no level checks apply.

  //     If the goal is set to {Str.Victory.PlayerLevelReached}, this option
  //     must have a value of at least 1.
  //     """, 0, DataCounters.MaxLevel, 0),

  //   ChoiceOption(Str.Option.SkillScatter, "Skill Scattering Method", $"""
  //     How should player skills be handled?

  //     {Str.Option.Disabled}: Do not scatter skill options. When you level
  //     up, you have free rein to choose where you put your skill points.

  //     {Str.Option.SkillScatterSpread}: Scatter skill options throughout
  //     the multiworld item pool. You may not use skill points upon leveling
  //     up unless you have the relevant skill option item.

  //     {Str.Option.SkillScatterCondensed}: Randomize skill options within
  //     level-up checks. For each level-up check, a random skill item will
  //     be granted, which must be applied immediately. Once you exceed the
  //     last level-up check, you have free choice on how to spend your
  //     remaining skill points. If {Str.Option.LevelChecks} is 0, this has
  //     no effect.
  //     """, 0,
  //     [(Str.Option.Disabled, 0), (Str.Option.SkillScatterSpread, 1), (Str.Option.SkillScatterCondensed, 2)])
  // );

  // public static IEnumerable<JProperty> GetItemRequiresOptions() => OptionGroup(
  //   Str.OptionGroup.ItemRequirements,

  //   ChoiceOption(Str.Option.BankLoanItem, "Bank Loan Approval", $"""
  //     A {Str.Item.BankLoan} is required before you can take any loans
  //     from the bank. Should it be part of the multiworld item pool,
  //     requiring you to find it, or should it be part of your starting
  //     inventory and always be available?

  //     If it is part of the multiworld item pool, it will be considered an
  //     "early" item.
  //     """, 0, [
  //       (Str.Option.ItemInStartingInventory, 0),
  //       (Str.Option.ItemInPoolEarly, 1),
  //       (Str.Option.ItemInPool, 2)
  //     ]),

  //   ChoiceOption(Str.Option.TruckContractItems, "Truck Contracts", $"""
  //     Truck Contracts are required before you can buy any trucks from
  //     truck dealers. Should they be part of the multiworld item pool,
  //     requiring you to find them, or should they be part of your starting
  //     inventory and always be available?

  //     The options have the following meaning:\n
  //     - all_in_starting_inventory: All truck contracts are in the starting
  //     inventory, and do not need to be found in the multiworld.\n
  //     - all_in_item_pool_early: All truck contracts are in sphere 1.\n
  //     - all_in_item_pool: All truck contracts can be anywhere in the
  //     multiworld.\n
  //     - random_in_starting_inventory: A randomly selected truck contract
  //     is in the starting inventory. The rest can be anywhere in the
  //     multiworld.\n
  //     - random_in_item_pool_early: A randomly selected truck contract is
  //     in sphere 1. The rest can be anywhere in the multiworld.\n
  //     - (brand)_in_starting_inventory: The specified brand's truck
  //     contract is in the starting inventory. The rest can be anywhere in
  //     the multiworld.\n
  //     - (brand)_in_item_pool_early: The specified brand's truck contract
  //     is in sphere 1. The rest can be anywhere in the multiworld.
  //     """, 0, [
  //       (Str.Option.TruckContractsAllStart, 0),
  //       (Str.Option.TruckContractsAllEarly, 1),
  //       (Str.Option.TruckContractsAllRandom, 2),
  //       (Str.Option.TruckContractsRandomStart, 3),
  //       (Str.Option.TruckContractsRandomEarly, 4),
  //       .. Data.TruckMakes.Keys.SelectMany((m, i) => Sequence.Of(
  //         (Str.Option.TruckContractsBrandStart(m), 5 + 2 * i),
  //         (Str.Option.TruckContractsBrandEarly(m), 6 + 2 * i)
  //       ))
  //     ]),

  //   ChoiceOption(Str.Option.TrailerContractItem, "Trailer Contract", $"""
  //     A {Str.Item.TrailerContract} is required before you can purchase any
  //     trailers. Should it be part of the multiworld item pool, requiring
  //     you to find it, or should it be part of your starting inventory and
  //     always be available?
  //     """, 0, [
  //       (Str.Option.ItemInStartingInventory, 0),
  //       (Str.Option.ItemInPoolEarly, 1),
  //       (Str.Option.ItemInPool, 2)
  //     ]),

  //   ChoiceOption(Str.Option.QuickTravelTicketItem, "Quick Travel Ticket", $"""
  //     A {Str.Item.QuickTravelTicket} is required before you can quick
  //     travel to an undiscovered city (whether through its DLC opening or
  //     through Convoy). Should it be part of the multiworld item pool,
  //     requiring you to find it, or should it be part of your starting
  //     inventory and always be available? 

  //     It can be disabled outright, such that quick traveling is never in
  //     logic, so long as all the enabled DLCs are connected to each other
  //     (otherwise, this will be set to {Str.Option.ItemInStartingInventory}).
  //     """, 1, [
  //       (Str.Option.Disabled, 0),
  //       (Str.Option.ItemInStartingInventory, 1),
  //       (Str.Option.ItemInPoolEarly, 2),
  //       (Str.Option.ItemInPool, 3)
  //     ])
  // );

  // public static IEnumerable<JProperty> GetChecksReductionOptions() => OptionGroup(
  //   Str.OptionGroup.CheckReduction,
  //   RangeOption(Str.Option.ChecksPercentStateCount, $"% of {Str.StatesCountries} containing Checks", $"""
  //     What percent of {Str.StatesCountriesLC} should contain locations?
  //     Note that other {Str.StatesCountriesLC} will still have Keys, and
  //     you must obtain those Keys before driving in those {Str.StatesCountriesLC}.

  //     The options in this category are applied in the following order:
  //     {Str.Option.ChecksPercentStateCount}, {Str.Option.ChecksMaxStateCount},
  //     {Str.Option.ChecksPercentWithinState}, {Str.Option.ChecksMaxWithinState},
  //     {Str.Option.ChecksMaxOverallCount}.
  //     """, 1, 100, 100),

  //   RangeOption(Str.Option.ChecksMaxStateCount, $"# of {Str.StatesCountries} Containing Checks", $"""
  //     How many {Str.StatesCountriesLC} should contain locations? Note that
  //     other accessible {Str.StatesCountriesLC} will still have Keys , and
  //     you must obtain those Keys before driving in those {Str.StatesCountriesLC}.

  //     Setting this higher than the number of {Str.StatesCountriesLC} that
  //     exist has no effect besides future-proofing your yaml. The default
  //     value is the number of {Str.StatesCountriesLC} that exist so far.
  //     """, 1, 100, DataCounters.TotalStates),

  //   RangeOption(Str.Option.ChecksPercentWithinState, "% Chance of Each Check", $"""
  //     What should the chance be of each location appearing in the AP?
  //     """, 1, 100, 100),

  //   RangeOption(Str.Option.ChecksMaxWithinState, "# of Checks Per State", $"""
  //     What is the maximum number of checks that should appear in each
  //     {Str.StateCountryLC}? Companies are considered {Str.StateCountryLC}less
  //     and are not affected by this option.

  //     Setting this higher than the number of checks per {Str.StateCountryLC}
  //     that exist has no effect besides future-proofing your yaml. The
  //     default value is the highest max number per {Str.StateCountryLC}.
  //     """, 1, 1000, DataCounters.MaxChecksByState),

  //   RangeOption(Str.Option.ChecksMaxOverallCount, "# of Checks", $"""
  //     What is the maximum number of checks that should be present in the
  //     multiworld?

  //     Setting this higher than the number of checks that exists has no
  //     effect besides future-proofing your yaml. The default value is the
  //     highest existing number so far.
  //     """, 1, 10000, DataCounters.TotalChecks)
  // );
  #endregion
}
#endregion

#region Program
public static class Program
{
  static void Main(string[] args)
  {
    (string FileName, JToken Contents)[] Values = [
      ("game", JsonDefs.GetGameJson()),
      ("regions", JsonDefs.GetRegionsJson()),
      ("locations", JsonDefs.GetLocationsJson()),
      ("items", JsonDefs.GetItemsJson()),
      ("categories", JsonDefs.GetCategoriesJson()),
      ("events", JsonDefs.GetEventsJson())/* ,
      ("options", JsonDefs.GetOptionsJson()) */
    ];

    foreach ((string file, JToken content) in Values)
    {
      File.WriteAllText($"src/data/{file}.json", content.ToString());
      Console.WriteLine($"Wrote {file}.json");
    }

    Console.WriteLine("Done!");
  }
}
#endregion