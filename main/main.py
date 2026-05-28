"""
This CSV contains thousands of chemical compounds physically tested in a lab 
to see how well they block a specific chemical.

COLUMNS:
1. molecule_chembl_id: The unique ID/barcode for the specific chemical.
2. canonical_smiles: The chemical structure written as text. Our Machine 
   Learning model will read this to learn what "shapes" make a good drug.
3. standard_value (IC50): "Half Maximal Inhibitory Concentration". 
   - Represents how much drug is needed to block 50% of the Aromatase.
   - LOWER NUMBER = BETTER (stronger drug, needs less concentration).
   - HIGHER NUMBER = WORSE (weak drug, needs massive concentration).
4. bioactivity_class: Our custom label for the ML model based on IC50:
   - 'active': IC50 <= 1000 (Great potential drug)
   - 'inactive': IC50 >= 10000 (Terrible at blocking)
   - 'intermediate': Anything in between.
"""

import pandas as pd
from chembl_webresource_client.new_client import new_client

target = new_client.target
target_query = target.search('aromatase')
targets = pd.DataFrame.from_dict(target_query)
targets

# Add these lines to see what's happening
print(f"Total results found: {len(targets)}")
print(targets[['target_chembl_id', 'pref_name']]) # Prints the IDs and names

# Your original line that is crashing
selected_target = targets.target_chembl_id[0]
selected_target
activity = new_client.activity
res = activity.filter(target_chembl_id=selected_target).filter(standard_type="IC50")

# 1. Print this right before the download starts
print("Downloading Aromatase data from ChEMBL... grab a snack, this might take 5+ minutes!")

# 2. This is the massive download step (Line 18)
df = pd.DataFrame.from_dict(res) 

# 3. Print this as soon as the download finishes
print("Download complete! Moving on to the next step...")
df.head(3)

df.standard_type.unique()
df.to_csv('bioactivity_data.csv', index=False)
df2 = df[df.standard_value.notna()]
df2

bioactivity_class = []
for i in df2.standard_value:
  if float(i) >= 10000:
    bioactivity_class.append("inactive")
  elif float(i) <= 1000:
    bioactivity_class.append("active")
  else:
    bioactivity_class.append("intermediate")

mol_cid = []
for i in df2.molecule_chembl_id:
  mol_cid.append(i)

canonical_smiles = []
for i in df2.canonical_smiles:
  canonical_smiles.append(i)

standard_value = []
for i in df2.standard_value:
  standard_value.append(i)

data_tuples = list(zip(mol_cid, canonical_smiles, bioactivity_class, standard_value))
df3 = pd.DataFrame(data_tuples, columns=['molecule_chembl_id', 'canonical_smiles', 'bioactivity_class', 'standard_value'])

# Save it to CSV!
df3.to_csv('bioactivity_preprocessed_data.csv', index=False)