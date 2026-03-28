// Assumes run from reponsitory root!

var CountryDataDict = new Dictionary<string, CountryData>();

void AddCountryData(string name, string? dlc1, string? dlc2 = null, string? alias = null)
{
  CountryDataDict[name.ToLower()] = new(name, dlc1, dlc2);
  if (alias != null) CountryDataDict[alias.ToLower()] = new(name, dlc1, dlc2);
}

AddCountryData("Portugal", "Iberia");
AddCountryData("Spain", "Iberia");
AddCountryData("France", null, "Vive la France !");
AddCountryData("United Kingdom", null, alias: "UK");
AddCountryData("Belgium", null);
AddCountryData("Netherlands", null);
AddCountryData("Germany", null);
AddCountryData("Luxembourg", null);
AddCountryData("Denmark", "Scandinavia");
AddCountryData("Norway", "Scandinavia", "Nordic Horizons");
AddCountryData("Sweden", "Scandinavia", "Nordic Horizons");
AddCountryData("Finland", "Beyond the Baltic Sea", "Nordic Horizons");
AddCountryData("Russia", "Beyond the Baltic Sea");
AddCountryData("Estonia", "Beyond the Baltic Sea");
AddCountryData("Latvia", "Beyond the Baltic Sea");
AddCountryData("Lithuania", "Beyond the Baltic Sea");
AddCountryData("Kaliningrad", "Beyond the Baltic Sea");
AddCountryData("Poland", null, "Going East");
AddCountryData("Czech Republic", null, "Going East", "Czech");
AddCountryData("Slovakia", null, "Going East");
AddCountryData("Austria", null);
AddCountryData("Hungary", "Going East");
AddCountryData("Romania", "Road to the Black Sea");
AddCountryData("Bulgaria", "Road to the Black Sea");
AddCountryData("Turkiye", "Road to the Black Sea", alias: "Turkiye");
AddCountryData("Greece", "Greece");
AddCountryData("Albania", "West Balkans");
AddCountryData("North Macedonia", "West Balkans");
AddCountryData("Kosovo", "West Balkans");
AddCountryData("Serbia", "West Balkans");
AddCountryData("Montenegro", "West Balkans");
AddCountryData("Bosnia and Herzegovina", "West Balkans", alias: "Bosnia");
AddCountryData("Croatia", "West Balkans");
AddCountryData("Slovenia", "West Balkans");
AddCountryData("Italy", null, "Italia");
AddCountryData("Switzerland", null);

using var stream = new FileStream("../csvdata/companies.csv", FileMode.Append, FileAccess.Write, FileShare.ReadWrite,
  4096, FileOptions.WriteThrough);
using var writer = new StreamWriter(stream);
writer.AutoFlush = true;

string lastName = "";

string csvEscape(string input)
{
  if (input.Contains(",") || input.Contains("\"")) return $"\"{input.Replace("\"", "\"\"")}\"";
  else return input;
}

while (true)
{
  Console.WriteLine("Enter company or country name (q to quit)");
  Console.Write("> ");
  string input = Console.ReadLine()!;
  if (input == "q" || input == "Q") break;

  if (CountryDataDict.TryGetValue(input.ToLower(), out CountryData country))
  {
    if (lastName == "")
    {
      Console.WriteLine("Enter a company name first!");
      continue;
    }

    string? dlc1 = country.DLC1;
    string? dlc2 = country.DLC2;

    if (dlc2 == null)
    {
      writer.WriteLine($"{csvEscape(lastName)},{dlc1 ?? "-"},{country.Name}");
    }

    else if (dlc1 == null)
    {
      while (true)
      {
        Console.WriteLine("Select the DLC:");
        Console.WriteLine("1) Base game (or both)");
        Console.WriteLine($"2) {dlc2}");
        Console.WriteLine("c) Cancel");
        Console.Write("> ");
        string pick = Console.ReadLine()!;

        if (pick == "1")
          writer.WriteLine($"{csvEscape(lastName)},-,{country.Name}");
        if (pick == "2")
          writer.WriteLine($"{csvEscape(lastName)},{dlc2},{country.Name}");
        if (pick == "c" || pick == "C" || pick == "1" || pick == "2") break;
      }
    }

    else
    {
      while (true)
      {
        Console.WriteLine("Select the DLC:");
        Console.WriteLine($"1) {dlc1}");
        Console.WriteLine($"2) {dlc2}");
        Console.WriteLine($"3) Both of the above");
        Console.WriteLine("c) Cancel");
        Console.Write("> ");
        string pick = Console.ReadLine()!;

        if (pick == "1" || pick == "3")
          writer.WriteLine($"{csvEscape(lastName)},{dlc1},{country.Name}");
        if (pick == "2" || pick == "3")
          writer.WriteLine($"{csvEscape(lastName)},{dlc2},{country.Name}");
        if (pick == "c" || pick == "C" || pick == "1" || pick == "2" || pick == "3")
          break;
      }
    }
  }
  else lastName = input;
}

readonly record struct CountryData(string Name, string? DLC1, string? DLC2 = null);
