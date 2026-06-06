from os import getcwd

from Functions import group
from DataFiles import regions, company_locations
from DataClasses import Check

# Do some grouping
states_with_dlcs: dict[str, set[str]] = group(regions, lambda r: r.state_name, lambda r: r.dlc_name, lambda _, l: set(l))
locations_by_state: dict[str, dict[str, dict[str, bool]]] = group(
  company_locations,
  lambda cl: cl.region.state_name,
  lambda cl: cl,
  lambda _, company_state_list: group(
    company_state_list,
    lambda ck: ck.name,
    lambda ck: (ck.region.dlc_name, ck.ferry_required),
    lambda _, company_dlc_list: {k: v for k, v in company_dlc_list}
  ))

# Write output file
if (getcwd().endswith('scripts')):
  _prefix: str = '../'
else:
  _prefix: str = ''

def get_dlc_text(state_dlcs: set[str], company_dlc_names: set[str]):
  if 'Base Game' in company_dlc_names:
    return ''
  elif company_dlc_names == state_dlcs:
    return ''
  else:
    return ', '.join(company_dlc_names)

with open(f'{_prefix}docs/Company Locations.md', 'wt', encoding='utf8') as file:
  for state, state_dlcs in states_with_dlcs.items():
    # file.write(f'# {state}\n')
    file.write(f"""
# {state}
| Company | DLC req'd. | Ferry req'd. |
| :- | :- | :-: |
""")
    companies_in_state = locations_by_state[state]

    for company, company_dlcs in companies_in_state.items():
      file.write(f'| {company} | {get_dlc_text(state_dlcs, company_dlcs.keys())} | {'✓' if False not in company_dlcs.values() else ''} |\n')

    file.write('\n')
  file.flush()
  file.close()
