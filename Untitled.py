import pandas as pd
import data_tools as datatools
import plotly.express as px
if __name__ == "__main__":
    excel_path = "Données_Assurance_S1.2_S2.2.xlsx" 
    all_sheets = datatools.read_all_excel_sheets(excel_path)
    for sheet_name, df in all_sheets.items():
        print(f"\nSheet Name: {sheet_name}")
        print(f"DataFrame Shape: {df.shape}")
        print("Data quality assesment:")
        print(datatools.data_quality(df))
pm=all_sheets['personne_morale']
pm.info()
pp=all_sheets['personne_physique']
pp.info()

pm['TYPE_PERSONNE'] = 'MORALE'
pp['TYPE_PERSONNE'] = 'PHYSIQUE'

cols_pm = ['REF_PERSONNE','RAISON_SOCIALE','MATRICULE_FISCALE','VILLE','LIB_GOUVERNORAT','LIB_SECTEUR_ACTIVITE','LIB_ACTIVITE','VILLE_GOUVERNORAT','TYPE_PERSONNE']
cols_pp = ['REF_PERSONNE','NOM_PRENOM','DATE_NAISSANCE','CODE_SEXE','SITUATION_FAMILIALE','NUM_PIECE_IDENTITE','VILLE','LIB_GOUVERNORAT','LIB_SECTEUR_ACTIVITE','LIB_PROFESSION','VILLE_GOUVERNORAT','TYPE_PERSONNE']

client_table = pd.concat([pm[cols_pm], pp[cols_pp]], ignore_index=True)


client_table['REF_PERSONNE'].duplicated().sum()
client_table=datatools.clean_strings(client_table)
datatools.data_quality(client_table)
# Split VILLE_GOUVERNORAT into two columns
split_cols = client_table['VILLE_GOUVERNORAT'].str.split('–', n=1, expand=True)

# Only assign if split works
if split_cols.shape[1] == 2:
    client_table['VILLE_from_concat'] = split_cols[0].str.strip()
    client_table['LIB_GOUVERNORAT_from_concat'] = split_cols[1].str.strip()
    
    # Optional: fill empty VILLE/LIB_GOUVERNORAT from split
    client_table['VILLE'] = client_table['VILLE'].replace('-', '')  # temporarily empty string
    client_table['VILLE'] = client_table['VILLE'].mask(client_table['VILLE'] == '', client_table['VILLE_from_concat'])
    
    client_table['LIB_GOUVERNORAT'] = client_table['LIB_GOUVERNORAT'].replace('-', '')
    client_table['LIB_GOUVERNORAT'] = client_table['LIB_GOUVERNORAT'].mask(client_table['LIB_GOUVERNORAT'] == '', client_table['LIB_GOUVERNORAT_from_concat'])
    
    # Drop helper columns
    client_table.drop(['VILLE_from_concat', 'LIB_GOUVERNORAT_from_concat'], axis=1, inplace=True)

def print_unique_values(df, categorical_cols):
    for col in categorical_cols:
        if col in df.columns:
            unique_vals = df[col].dropna().unique()
            print(f"\nColumn: {col}")
            print(f"Unique values ({len(unique_vals)}):")
            print(unique_vals)
        else:
            print(f"\nColumn {col} not found in DataFrame")
sector_map = {
    "AUCUN": "NON RENSEIGNE",
    "": "NON RENSEIGNE",
    "-": "NON RENSEIGNE",
    "INTERMÉDIATION FINANCIÈRE": "FINANCE",
    "ASSURANCE": "FINANCE",
    "AUXILIAIRES FINANCIERS ET D ASSURANCE": "FINANCE",
    "ACTIVITES IARD TARIFIABLES": "FINANCE",
    "ACTIVITES MRP TARIFIABLES": "FINANCE",
    "SERVICES PERSONNELS": "SERVICES",
    "SERVICES DOMESTIQUES": "SERVICES",
    "SERVICES FOURNIS PRINCIPALEMENT AUX ENTREPRISES": "SERVICES AUX ENTREPRISES",
    "ACTIVITÉS INFORMATIQUES": "INFORMATIQUE",
    "RECHERCHE ET DÉVELOPPEMENT": "R&D",
    "AGRICULTURE, CHASSE, SERVICES ANNEXES": "AGRICULTURE",
    "SYLVICULTURE, EXPLOITATION FORESTIÈRE, SERVICES ANNEXES": "FORESTERIE",
    "PÊCHE, AQUACULTURE": "PÊCHE",
    "TRAVAIL DU BOIS ET FABRICATION D ARTICLES EN BOIS": "BOIS",
    "INDUSTRIES ALIMENTAIRES": "AGROALIMENTAIRE",
    "INDUSTRIE CHIMIQUE": "CHIMIE",
    "INDUSTRIE DU CAOUTCHOUC ET DES PLASTIQUES": "PLASTIQUE/CAOUTCHOUC",
    "INDUSTRIE TEXTILE": "TEXTILE",
    "INDUSTRIE DE L HABILLEMENT ET DES FOURRURES": "HABILLEMENT",
    "INDUSTRIE DU CUIR ET DE LA CHAUSSURE": "CUIR",
    "FABRICATION DE MEUBLES; INDUSTRIES DIVERSES": "AMEUBLEMENT",
    "FABRICATION D AUTRES PRODUITS MINÉRAUX NON MÉTALLIQUES": "MINÉRAUX NON MÉTALLIQUES",
    "MÉTALLURGIE": "MÉTALLURGIE",
    "TRAVAIL DES MÉTAUX": "MÉTALLURGIE",
    "INDUSTRIE AUTOMOBILE": "AUTOMOBILE",
    "FABRICATION D AUTRES MATÉRIELS DE TRANSPORT": "TRANSPORT",
    "FABRICATION D ÉQUIPEMENTS DE RADIO, TÉLÉVISION ET COMMUNICATION": "ÉLECTRONIQUE",
    "FABRICATION D INSTRUMENTS MÉDICAUX, DE PRÉCISION, D OPTIQUE ET D HORLOGERIE": "INSTRUMENTS DE PRÉCISION",
    "CONSTRUCTION": "BTP",
    "COMMERCE ET RÉPARATION AUTOMOBILE": "AUTOMOBILE",
    "COMMERCE DE GROS ET INTERMÉDIAIRES DU COMMERCE": "COMMERCE",
    "COMMERCE DE DÉTAIL ET RÉPARATION D ARTICLES DOMESTIQUES": "COMMERCE",
    "STATION DE SERVICE": "COMMERCE",
    "HÔTELS ET RESTAURANTS": "HÔTELLERIE/RESTAURATION",
    "TRANSPORTS TERRESTRES": "TRANSPORT",
    "TRANSPORTS AÉRIENS": "TRANSPORT",
    "SERVICES AUXILIAIRES DES TRANSPORTS": "TRANSPORT",
    "POSTES ET TÉLÉCOMMUNICATIONS": "TÉLÉCOMMUNICATIONS",
    "ÉDUCATION": "ÉDUCATION",
    "SANTÉ ET ACTION SOCIALE": "SANTÉ",
    "ADMINISTRATION PUBLIQUE": "ADMINISTRATION PUBLIQUE",
    "ACTIVITÉS IMMOBILIÈRES": "IMMOBILIER",
    "ACTIVITÉS RÉCRÉATIVES, CULTURELLES ET SPORTIVES": "LOISIRS/SPORT",
    "ACTIVITE SPORTIVE": "LOISIRS/SPORT",
    "PRODUCTION ET DISTRIBUTION D ÉLECTRICITÉ, DE GAZ ET DE CHALEUR": "ÉNERGIE",
    "COKÉFACTION, RAFFINAGE, INDUSTRIES NUCLÉAIRES": "ÉNERGIE",
    "ASSAINISSEMENT, VOIRIE ET GESTION DES DÉCHETS": "ENVIRONNEMENT",
    "LOCATION SANS OPÉRATEUR": "LOCATION",
    "AGENCES ET BUREAUX": "SERVICES AUX ENTREPRISES",
    "ACTIVITÉS ASSOCIATIVES": "ASSOCIATIONS",
    "CADRES ET PROFESSIONS INTELLECTUELLES SUPÉRIEURES": "CADRES SUPÉRIEURS",
    "ARTISANS, COMMERÇANTS ET CHEFS D ENTREPRISE": "ENTREPRENEURS",
    "PROFESSIONS INTERMÉDIAIRES": "PROFESSIONS INTERMÉDIAIRES",
    "OUVRIERS": "OUVRIERS",
    "EMPLOYÉS": "EMPLOYÉS",
    "RETRAITÉS": "RETRAITÉS",
    "AUTRES PERSONNES SANS ACTIVITÉ PROFESSIONNELLE": "SANS ACTIVITÉ"
}
profession_map = {
    # Abréviations et orthographe
    "DOC.": "DOCTEUR", "DR": "DOCTEUR", "STEWART": "HÔTESSE/STEWARD",
    "BH": "BANQUE", "OACA": "ADMINISTRATION", "STUSID": "BANQUE",
    "R&D": "RECHERCHE ET DÉVELOPPEMENT",
    
    # Regroupements thématiques
    "MÉDECIN": "SANTÉ", "INFIRMIER": "SANTÉ", "PHARMACIEN": "SANTÉ", 
    "DENTISTE": "SANTÉ", "SAGE-FEMME": "SANTÉ", "KINÉSITHÉRAPEUTE": "SANTÉ",
    "ANESTHÉSISTE": "SANTÉ", "BIOLOGISTE": "SANTÉ",
    "INGÉNIEUR": "INGÉNIEUR", "TECHNICIEN": "TECHNICIEN", 
    "PROFESSEUR": "ÉDUCATION", "ENSEIGNANT": "ÉDUCATION", "FORMATEUR": "ÉDUCATION",
    "INSTITUTEUR": "ÉDUCATION", "MAÎTRE": "ÉDUCATION",
    "COMMERCIAL": "COMMERCE", "VENDEUR": "COMMERCE", "GÉRANT": "COMMERCE",
    "COMPTABLE": "ADMINISTRATIF", "SECRÉTAIRE": "ADMINISTRATIF", 
    "ADMINISTRATEUR": "ADMINISTRATIF", "GESTIONNAIRE": "ADMINISTRATIF",
    "CADRE": "CADRE", "CHEF": "CADRE", "DIRECTEUR": "CADRE",
    "OUVRIER": "PRODUCTION", "ARTISAN": "PRODUCTION", "OPÉRATEUR": "PRODUCTION",
    "AGRICULTEUR": "AGRICULTURE", "ÉLEVEUR": "AGRICULTURE", "VITICULTEUR": "AGRICULTURE",
    "CHAUFFEUR": "TRANSPORT", "CONDUCTEUR": "TRANSPORT", "LIVREUR": "TRANSPORT",
    "AVOCAT": "JURIDIQUE", "NOTAIRE": "JURIDIQUE", "HUISSIER": "JURIDIQUE",
    "POLICIER": "SÉCURITÉ", "GENDARME": "SÉCURITÉ", "GARDIEN": "SÉCURITÉ",
    "CUISINIER": "HÔTELLERIE", "SERVEUR": "HÔTELLERIE", "RESTAURATEUR": "HÔTELLERIE",
    
    # Valeurs manquantes
    "": "NON RENSEIGNE", "-": "NON RENSEIGNE", "NON DEFINI": "NON RENSEIGNE",
    "AUCUN": "NON RENSEIGNE", "CHÔMEUR": "SANS ACTIVITÉ", 
    "RETRAITÉ": "RETRAITÉ", "ÉTUDIANT": "ÉTUDIANT"
}
activity_map = {
    "": "NON RENSEIGNE", "-": "NON RENSEIGNE", "NON DEFINI": "NON RENSEIGNE",
    "AUTRES SERVICES PERSONNELS": "SERVICES",
    "COMMERCE DE DÉTAIL": "VENTE", "COMMERCE DE GROS": "VENTE",
    "VENTE PAR CORRESPONDANCE": "VENTE", "VENTE AU DÉTAIL": "VENTE",
    "INDUSTRIES ALIMENTAIRES N.C.A.": "AGROALIMENTAIRE",
    "FABRICATION D ALIMENTS": "AGROALIMENTAIRE",
    "BOULANGERIE": "AGROALIMENTAIRE", "PÂTISSERIE": "AGROALIMENTAIRE",
    "RESTAURATION": "HÔTELLERIE/RESTAURATION",
    "HÔTELS": "HÔTELLERIE/RESTAURATION", "CAFÉS TABACS": "HÔTELLERIE/RESTAURATION",
    "CONSTRUCTION": "BTP", "MAÇONNERIE": "BTP", "TERRASSEMENT": "BTP",
    "ÉDITION, IMPRIMERIE": "MÉDIA", "TÉLÉCOMMUNICATIONS": "TÉLÉCOMMUNICATIONS",
    "RECHERCHE DÉVELOPPEMENT": "R&D", "ACTIVITÉS INFORMATIQUES": "INFORMATIQUE",
    "SANTÉ": "SANTÉ", "HÔPITAL": "SANTÉ", "CLINIQUE": "SANTÉ",
    "AGRICULTURE": "AGRICULTURE", "ÉLEVAGE": "AGRICULTURE", "PÊCHE": "PÊCHE",
    "TRANSPORT": "TRANSPORT", "MANUTENTION": "TRANSPORT",
    "ÉNERGIE": "ÉNERGIE", "EAU": "ENVIRONNEMENT", "DÉCHETS": "ENVIRONNEMENT",
    "BANQUE": "FINANCE", "ASSURANCE": "FINANCE", "CRÉDIT": "FINANCE",
    "ADMINISTRATION": "ADMINISTRATION", "DÉFENSE": "ADMINISTRATION PUBLIQUE",
    "ÉDUCATION": "ÉDUCATION", "ENSEIGNEMENT": "ÉDUCATION",
    "LOISIRS": "LOISIRS/SPORT", "SPORT": "LOISIRS/SPORT", "CULTURE": "LOISIRS/SPORT"
}
def mapping_accuracy(df, col='LIB_SECTEUR_ACTIVITE', mapping=sector_map):
    original_values = df[col].unique()
    mapped_values = df[col].map(mapping)
    # Count how many were mapped (not NaN)
    mapped_count = mapped_values.notna().sum()
    accuracy = mapped_count / len(df[col]) * 100
    
    # Unmapped values
    unmapped = df[~df[col].isin(mapping.keys())][col].value_counts().reset_index()
    unmapped.columns = ['Unmapped Value', 'Count']
    
    return accuracy, unmapped

accuracy, unmapped = mapping_accuracy(client_table,col='LIB_SECTEUR_ACTIVITE',mapping=sector_map)
print(f"Mapping accuracy: {accuracy:.2f}%")
print("Unmapped values:")
print(unmapped)


# #### LIB_PROFESSION mapping

# In[57]:


accuracy, unmapped = mapping_accuracy(client_table,col='LIB_PROFESSION',mapping=profession_map)
print(f"Mapping accuracy: {accuracy:.2f}%")
print("Unmapped values:")
print(unmapped)


# #### LIB_ACTIVITE mapping

# In[58]:


accuracy, unmapped = mapping_accuracy(client_table,col='LIB_ACTIVITE',mapping=activity_map)
print(f"Mapping accuracy: {accuracy:.2f}%")
print("Unmapped values:")
print(unmapped)


# #### Exporting client_table

# In[59]:


client_table.to_csv('client_table.csv')


# #### Distribution of client types (morale vs physique)

# In[60]:


client_type_counts = client_table["TYPE_PERSONNE"].value_counts().reset_index()
client_type_counts.columns = ["TYPE_PERSONNE", "count"]
fig = px.bar(
    client_type_counts,
    x="TYPE_PERSONNE", y="count",
    labels={"TYPE_PERSONNE": "Type de personne", "count": "Count"},
    title="Distribution of Client Types",color="TYPE_PERSONNE"
)
fig.show()


# #### Sectors for companies (LIB_SECTEUR_ACTIVITE)

# In[61]:


morale_sectors = (
client_table[client_table["TYPE_PERSONNE"]=="MORALE"]["LIB_SECTEUR_ACTIVITE"]
    .value_counts().head(15).reset_index()
)
morale_sectors.columns = ["LIB_SECTEUR_ACTIVITE", "count"]

fig = px.bar(
    morale_sectors,
    x="LIB_SECTEUR_ACTIVITE", y="count",
    title="Top 15 Sectors (Companies)"
)
fig.show()


# #### Professions for individuals (LIB_PROFESSION)

# 

# In[62]:


physique_profs = (
    client_table[client_table["TYPE_PERSONNE"]=="PHYSIQUE"]["LIB_PROFESSION"]
    .value_counts().head(10).reset_index()
)
physique_profs.columns = ["LIB_PROFESSION", "count"]

fig = px.bar(
    physique_profs,
    x="LIB_PROFESSION", y="count",
    title="Top 10 Professions (Individuals)"
)
fig.show()


# #### Geographic distribution (Governorate)
# 

# In[63]:


gov_counts = client_table["LIB_GOUVERNORAT"].value_counts().head(10).reset_index()
gov_counts.columns = ["LIB_GOUVERNORAT", "count"]

fig = px.bar(
    gov_counts,
    x="LIB_GOUVERNORAT", y="count",
    title="Top 10 Governorates"
)
fig.show()


# #### Age distribution

# In[64]:


from datetime import datetime
client_table["AGE"] = (
    (datetime.now() - pd.to_datetime(client_table["DATE_NAISSANCE"], errors="coerce")).dt.days // 365
)

fig = px.histogram(
    client_table, x="AGE", nbins=20,
    title="Age Distribution of Clients"
)
fig.show()


# #### Family situation

# In[65]:


fam_counts = client_table["SITUATION_FAMILIALE"].value_counts().reset_index()
fam_counts.columns = ["SITUATION_FAMILIALE", "count"]

fig = px.bar(
    fam_counts,
    x="SITUATION_FAMILIALE", y="count",
    title="Family Situation Distribution"
)
fig.show()


# #### Age by family situation

# In[66]:


fig = px.box(client_table, x="SITUATION_FAMILIALE", y="AGE", title="Age by Family Situation")
fig.show()


# #### Sector activity by governorate (heatmap-like)

# In[67]:


sector_gov = client_table.groupby(["LIB_GOUVERNORAT", "LIB_SECTEUR_ACTIVITE"]).size().reset_index(name="count")
fig = px.treemap(sector_gov, path=["LIB_GOUVERNORAT","LIB_SECTEUR_ACTIVITE"], values="count", title="Sector Activity by Governorate")
fig.show()


# #### Exploratory sanity check

# In[68]:


print(client_table["TYPE_PERSONNE"].value_counts())
print(client_table["LIB_SECTEUR_ACTIVITE"].value_counts().head(10))
print(client_table["AGE"].describe())
print(client_table["LIB_GOUVERNORAT"].value_counts().head(10))


# In[69]:


client_table[client_table['AGE']==client_table['AGE'].min()]


# ### After building the unified client profile in Step 1, the next step is to enrich these profiles with contractual information. By merging the Contrats dataset with the client_table, we can capture each client’s insurance behavior, including the number of contracts they hold, the types of branches and products they subscribe to, the total premiums paid, and the status of their contracts (active, terminated, suspended). This transformation turns static demographic data into dynamic behavioral profiles, forming the basis for deeper customer segmentation and recommendation strategies.

# #### Merging data

# In[70]:


contracts = all_sheets['Contrats']

# Clean strings for consistency
contracts = datatools.clean_strings(contracts)

# Merge contracts with client_table
client_contracts = contracts.merge(
    client_table[['REF_PERSONNE', 'TYPE_PERSONNE']],
    on="REF_PERSONNE",
    how="left"
)

agg_contracts = client_contracts.groupby("REF_PERSONNE").agg(
    contracts_count=("NUM_CONTRAT", "nunique"),
    branches_set=("branche", lambda x: list(set(x))),
    products_set=("LIB_PRODUIT", lambda x: list(set(x))),
    total_paid=("somme_quittances", "sum"),
    active_contracts=("LIB_ETAT_CONTRAT", lambda x: sum(x=="EN COURS")),
    expired_contracts=("LIB_ETAT_CONTRAT", lambda x: sum(x=="EXPIRE")),
    reduced_contracts=("LIB_ETAT_CONTRAT", lambda x: sum(x=="REDUIT")),
    instance_contracts=("LIB_ETAT_CONTRAT", lambda x: sum(x=="EN INSTANCE/DEVIS")),
    terminated_contracts=("LIB_ETAT_CONTRAT", lambda x: sum(x=="RESILIE")),
    suspended_contracts=("LIB_ETAT_CONTRAT", lambda x: sum(x=="SUSPENDU"))
).reset_index()

agg_contracts.head()
fig1 = px.histogram(
    agg_contracts,
    x="contracts_count",
    nbins=20,
    title="Distribution of Number of Contracts per Client",
    labels={"contracts_count": "Number of Contracts"}
)
fig1.show()


# #### 2. Total premiums paid per client (skewed → log scale)

# In[74]:


fig2 = px.histogram(
    agg_contracts,
    x="total_paid",
    nbins=50,
    title="Distribution of Total Premiums Paid",
    labels={"total_paid": "Total Paid"},
    log_y=True
)
fig2.show()


# #### 3. Active vs Resiliated vs Suspended contracts (global sums)

# In[75]:


status_summary = {
    "Active": agg_contracts["active_contracts"].sum(),
    "EXPIRED": agg_contracts["expired_contracts"].sum(),
    "REDUCED": agg_contracts["reduced_contracts"].sum(),
    "En Instance/Devise": agg_contracts["instance_contracts"].sum(),
    "Resiliated": agg_contracts["terminated_contracts"].sum(),
    "Suspended": agg_contracts["suspended_contracts"].sum()
}
fig3 = px.pie(
    names=list(status_summary.keys()),
    values=list(status_summary.values()),
    title="Contract Status Distribution"
)
fig3.show()


# In[76]:


df


# #### 4. Top branches subscribed (flatten list of branches)

# In[77]:


import itertools
all_branches = list(itertools.chain.from_iterable(agg_contracts["branches_set"]))
branch_counts = pd.Series(all_branches).value_counts().reset_index()
branch_counts.columns = ["Branch", "Count"]

fig4 = px.bar(
    branch_counts,
    x="Branch", y="Count",
    title="Insurance Branches Subscribed",
    text="Count"
)
fig4.show()


# In[78]:


print(branch_counts)


# #### 5. Top products subscribed (flatten list of products)

# In[79]:


all_products = list(itertools.chain.from_iterable(agg_contracts["products_set"]))
product_counts = pd.Series(all_products).value_counts().reset_index()
product_counts.columns = ["Product", "Count"]

fig5 = px.bar(
    product_counts.head(10),
    x="Product", y="Count",
    title="Top 10 Insurance Products Subscribed",
    text="Count"
)
fig5.show()


# #### Merging back into client_table

# In[80]:


client_table = client_table.merge(agg_contracts, on="REF_PERSONNE", how="left")

# Fill NaN for clients with no contracts
client_table[["contracts_count","total_paid","active_contracts",
              "terminated_contracts","suspended_contracts"]] = client_table[
    ["contracts_count","total_paid","active_contracts",
     "terminated_contracts","suspended_contracts"]
].fillna(0)


# #### Analysing claims data

# In[81]:


client_table.info()


# In[82]:


claims=all_sheets['sinistres']
print(datatools.data_quality(claims))


# #### Converting numeric columns

# In[83]:


claims['MONTANT_ENCAISSE'] = pd.to_numeric(claims['MONTANT_ENCAISSE'], errors='coerce')
claims['MONTANT_A_ENCAISSER'] = pd.to_numeric(claims['MONTANT_A_ENCAISSER'], errors='coerce')


# #### Converting date columns

# In[84]:


date_cols = ['DATE_OUVERTURE', 'DATE_SURVENANCE', 'DATE_DECLARATION']
for col in date_cols:
    claims[col] = pd.to_datetime(claims[col], errors='coerce')


# #### handling the missing categorical values and droping nearly-empty columns in claims dataset

# In[85]:


# Fill missing categorical values
claims['TAUX_RESPONSABILITE'] = claims['TAUX_RESPONSABILITE'].fillna('UNKNOWN')
claims['LIEU_ACCIDENT'] = claims['LIEU_ACCIDENT'].fillna('UNKNOWN')

# Drop nearly-empty columns
claims = claims.drop(columns=['MOTIF_REOUVERTURE'])

# check result
print(claims[['TAUX_RESPONSABILITE', 'LIEU_ACCIDENT']].isna().sum())
print(claims.head())


# In[86]:


claims_by_branch = claims.pivot_table(
    index='NUM_CONTRAT',
    columns='LIB_BRANCHE',
    values='NUM_SINISTRE',
    aggfunc='count',
    fill_value=0
)


# In[87]:


# Sum across all clients to get total claims per branch
total_claims_per_branch = claims_by_branch.sum().sort_values(ascending=False).reset_index()
total_claims_per_branch.columns = ['Branch', 'Claims']

# Plot
fig = px.bar(
    total_claims_per_branch,
    x='Branch',
    y='Claims',
    title='Total Claims per Insurance Branch',
    text='Claims',
    color='Claims',
    color_continuous_scale='Viridis'
)
fig.update_layout(xaxis_title='Branch', yaxis_title='Number of Claims')
fig.show()


# In[88]:


# Sample 50 clients for clarity
sample_claims = claims_by_branch.sample(50).reset_index()
sample_claims_melted = sample_claims.melt(id_vars='NUM_CONTRAT', var_name='Branch', value_name='Claims')

# Plot
fig = px.density_heatmap(
    sample_claims_melted,
    x='Branch',
    y='NUM_CONTRAT',
    z='Claims',
    text_auto=True,
    title='Claims Distribution Across Branches (Sample of 50 Clients)',
    color_continuous_scale='YlGnBu'
)
fig.show()


# In[89]:


fig = px.pie(
    total_claims_per_branch,
    names='Branch',
    values='Claims',
    title='Claims Distribution by Branch'
)
fig.show()


# In[90]:


recent_threshold = pd.Timestamp('2025-01-01')  # Adjust as needed
recent_claims = claims.groupby('NUM_CONTRAT')['DATE_SURVENANCE'].max()
has_recent_claim = ((recent_claims >= recent_threshold).astype(int).rename('has_recent_claim')).value_counts().reset_index()


# In[91]:


fig = px.bar(
    has_recent_claim,
    x="has_recent_claim", y="count",
    labels={"has_recent_claim": "has recent claim (1 : yes , 0 : no)", "count": "Count"},
    title="Distribution of recent claims",color="has_recent_claim"
)
fig.show()

claims = claims.merge(
    contracts[['NUM_CONTRAT', 'REF_PERSONNE']],
    on='NUM_CONTRAT',
    how='left'
)


# #### Total claims per client

# In[93]:


claims_count = claims.groupby('REF_PERSONNE').size().rename('claims_count')


# In[94]:


# Make sure claims has REF_PERSONNE
# Pivot table to get claims per branch per client
claims_by_branch = claims.pivot_table(
    index='REF_PERSONNE',      # use client ID instead of contract
    columns='LIB_BRANCHE',
    values='NUM_SINISTRE',
    aggfunc='count',
    fill_value=0
).reset_index()  # make REF_PERSONNE a column for merging


# #### Has recent claim (binary) (per client)

# In[95]:


recent_threshold = pd.Timestamp('2024-01-01')
has_recent_claim = claims.groupby('REF_PERSONNE')['DATE_SURVENANCE'].max()
has_recent_claim = (has_recent_claim >= recent_threshold).astype(int).rename('has_recent_claim')


# In[96]:


claims.head()


# #### Merging aggregated claims into client table

# In[97]:


# Merge into client_table
client_table = client_table.merge(claims_count, on='REF_PERSONNE', how='left')
client_table = client_table.merge(claims_by_branch, on='REF_PERSONNE', how='left')
client_table = client_table.merge(has_recent_claim, on='REF_PERSONNE', how='left')

# Fill NaNs for clients with no claims
client_table['claims_count'] = client_table['claims_count'].fillna(0)
client_table['has_recent_claim'] = client_table['has_recent_claim'].fillna(0)


# In[98]:


client_table.info()


# In[99]:


branch_columns = ['AUTOMOBILE', 'ENGINEERING', 'GROUPE-MALADIE', 
                  'INCENDIE', 'RISQUES DIVERS', 'TRANSPORT', 'VIE']
client_table[branch_columns] = client_table[branch_columns].fillna(0)
print(client_table[['claims_count', 'has_recent_claim'] + branch_columns].head(15))




# Replace NaN with empty lists
client_table['branches_set'] = client_table['branches_set'].apply(lambda x: x if isinstance(x, list) else [])

# Flatten the lists to get one row per branch
branch_counts = client_table['branches_set'].explode().value_counts().reset_index()
branch_counts.columns = ['Branch', 'Count']

# Plot top branches
fig = px.bar(branch_counts, x='Branch', y='Count', title='Top Subscribed Branches', color='Count')
fig.show()


# In[101]:


client_table['products_set'] = client_table['products_set'].apply(lambda x: x if isinstance(x, list) else [])
product_counts = client_table['products_set'].explode().value_counts().reset_index()
product_counts.columns = ['Product', 'Count']

fig = px.bar(product_counts, x='Product', y='Count', title='Top Subscribed Products', color='Count')
fig.show()


# #### Average Contracts per Client Type

# In[102]:


avg_contracts = client_table.groupby('TYPE_PERSONNE')['contracts_count'].mean().reset_index()

fig = px.bar(avg_contracts, x='TYPE_PERSONNE', y='contracts_count', 
             title='Average Contracts per Client Type', text='contracts_count', color='contracts_count')
fig.show()


# #### Claims Frequency vs Sector / Profession

# In[103]:


# Claims frequency by sector
sector_claims = client_table.groupby('LIB_SECTEUR_ACTIVITE')['claims_count'].mean().reset_index()
fig = px.bar(sector_claims, x='LIB_SECTEUR_ACTIVITE', y='claims_count', 
             title='Average Claims per Sector', color='claims_count')
fig.update_layout(xaxis_tickangle=-45)
fig.show()


# In[104]:


# Aggregate number of clients per sector and profession
prof_counts = client_table.groupby(
    ['LIB_SECTEUR_ACTIVITE', 'LIB_PROFESSION']
).size().reset_index(name='client_count')

# Sunburst plot
fig = px.sunburst(
    prof_counts,
    path=['LIB_SECTEUR_ACTIVITE', 'LIB_PROFESSION'],  # hierarchy
    values='client_count',                             # size of each slice
    color='client_count',                              # color by count
    color_continuous_scale='Viridis',
    title='Client Distribution by Sector and Profession'
)

fig.show()


# #### Age Distribution vs Insurance Type

# In[105]:


branch_columns = ['AUTOMOBILE', 'ENGINEERING', 'GROUPE-MALADIE', 
                  'INCENDIE', 'RISQUES DIVERS', 'TRANSPORT', 'VIE']

# Convert to long format for Plotly
age_claims = client_table.melt(
    id_vars=['REF_PERSONNE', 'AGE'],
    value_vars=branch_columns,
    var_name='Insurance_Type',
    value_name='Claims'
)

# Only include clients with at least one claim
age_claims = age_claims[age_claims['Claims'] > 0]

fig = px.box(age_claims, x='Insurance_Type', y='AGE', points='all', 
             title='Age Distribution vs Insurance Type')
fig.show()


# In[106]:


client_table.describe()


# In[107]:


client_table.info()


# ### Loading Garantie_contrat sheet

# In[108]:


garant_contrat=all_sheets['Garantie_contrat']
print(datatools.data_quality(garant_contrat))


# ### Merging Guarantees onto Contracts

# In[109]:


contracts.info()


# In[110]:


contracts_with_guarantees = contracts.merge(
    garant_contrat[['NUM_CONTRAT', 'CODE_GARANTIE', 'LIB_GARANTIE', 'CAPITAL_ASSURE']],
    on='NUM_CONTRAT',
    how='left'
)


# ### Aggregating per client
# 
# Each contract belongs to a client (REF_PERSONNE):

# In[111]:


client_guarantees = contracts_with_guarantees.groupby('REF_PERSONNE').agg(
    guarantees_set=('LIB_GARANTIE', lambda x: list(set(x.dropna()))),
    guarantees_count=('LIB_GARANTIE', lambda x: x.notna().sum())
).reset_index()


# In[112]:


client_guarantees


# ### Merging into client_table

# In[113]:


client_table = client_table.merge(client_guarantees, on='REF_PERSONNE', how='left')

# Fill missing guarantees
client_table['guarantees_set'] = client_table['guarantees_set'].apply(lambda x: x if isinstance(x, list) else [])
client_table['guarantees_count'] = client_table['guarantees_count'].fillna(0)


# In[114]:


client_table.info()


# In[115]:


client_table.to_csv('clients.csv')
prod_profile=pd.read_excel("../data/Mapping produits vs profils_cibles.xlsx")


# In[75]:


prod_profile.head()


# In[76]:


prod_profile.info()


# ### Preprocessing target profiles

# In[77]:


prod_profile['Profils_cibles_list'] = prod_profile['Profils cibles'].str.split(';').apply(lambda x: [p.strip() for p in x])


# In[78]:


prod_profile.head()


# ### Comparing client profile with target profiles

# Define a client “profile” (e.g., TYPE_PERSONNE, LIB_SECTEUR_ACTIVITE, LIB_PROFESSION, AGE group, etc.).
# For simplicity, let’s assume we just match TYPE_PERSONNE against Profils_cibles_list for now.

# In[79]:


# Split Profils cibles into separate rows
prod_profil_expanded = prod_profile.copy()
prod_profil_expanded['Profils cibles'] = prod_profil_expanded['Profils cibles'].str.split(';')
prod_profil_expanded = prod_profil_expanded.explode('Profils cibles')
prod_profil_expanded['Profils cibles'] = prod_profil_expanded['Profils cibles'].str.strip()


# ### For a given client, return all profiles from prod_profil that match
#     based on demographics (AGE, CODE_SEXE, LIB_SECTEUR_ACTIVITE, TYPE_PERSONNE)

# In[80]:


def match_profiles(client_row, all_profiles):
    """
    For a given client, return all profiles from prod_profil that match
    based on demographics (AGE, CODE_SEXE, LIB_SECTEUR_ACTIVITE, TYPE_PERSONNE).
    """
    matched_profiles = []
    
    # Loop over all profiles
    for profile in all_profiles:
        profile_lower = profile.lower()
        
        # Match AGE / senior/adult/young if words exist in profile
        if 'senior' in profile_lower or 'retraité' in profile_lower or 'personnes âgées' in profile_lower:
            if pd.notnull(client_row['AGE']) and client_row['AGE'] >= 60:
                matched_profiles.append(profile)
                continue
        if 'adulte' in profile_lower or 'famille' in profile_lower or 'prévoyant' in profile_lower:
            if pd.notnull(client_row['AGE']) and 25 <= client_row['AGE'] < 60:
                matched_profiles.append(profile)
                continue
        if 'étudiant' in profile_lower:
            if pd.notnull(client_row['AGE']) and client_row['AGE'] < 25:
                matched_profiles.append(profile)
                continue
        
        # Match SEXE
        if client_row['CODE_SEXE'] == 'M' and ('chef de famille' in profile_lower or 'homme' in profile_lower):
            matched_profiles.append(profile)
            continue
        if client_row['CODE_SEXE'] == 'F' and ('parent' in profile_lower or 'femme' in profile_lower):
            matched_profiles.append(profile)
            continue
        
        # Match TYPE_PERSONNE
        if client_row['TYPE_PERSONNE'] == 'MORALE' and ('entreprise' in profile_lower or 'société' in profile_lower):
            matched_profiles.append(profile)
            continue
        if client_row['TYPE_PERSONNE'] == 'PHYSIQUE' and ('particulier' in profile_lower or 'famille' in profile_lower):
            matched_profiles.append(profile)
            continue
        
        # Match secteur (LIB_SECTEUR_ACTIVITE)
        secteur = client_row['LIB_SECTEUR_ACTIVITE']
        if secteur is not None and secteur.lower() in profile_lower:
            matched_profiles.append(profile)
            continue
            
    return list(set(matched_profiles))


# ### Apply mapping to all clients

# In[81]:


all_unique_profiles = prod_profil_expanded['Profils cibles'].unique()
client_table['mapped_profiles'] = client_table.apply(
    lambda row: match_profiles(row, all_unique_profiles),
    axis=1
)


# In[82]:


client_table.info()


# ### Creating a Rule-based reccomendations

# In[83]:


# Ensure mapped_profiles is a list, not just a string
client_table["mapped_profiles"] = client_table["mapped_profiles"].apply(
    lambda x: [p.strip() for p in str(x).strip("[]").replace("'", "").split(",")]
)

# Loop through products and create match flags
for i, row in prod_profile.iterrows():
    product_name = row["LIB_PRODUIT"]
    target_profiles = [p.strip() for p in row["Profils cibles"].split(";")]

    col_name = f"match_{product_name.replace(' ', '_')}"
    client_table[col_name] = client_table["mapped_profiles"].apply(
        lambda client_profiles: int(any(tp in client_profiles for tp in target_profiles))
    )

# Now client_table has extra columns like match_TEMPORAIRE_DECES, match_ASSURANCE_VIE, etc.


# In[84]:


client_table.info()


# In[85]:


client_table.head()
clients = client_table[['REF_PERSONNE', 'AGE', 'CODE_SEXE', 'LIB_SECTEUR_ACTIVITE', 'TYPE_PERSONNE']].copy()
products = prod_profile[['LIB_PRODUIT']].drop_duplicates().copy()
# Create a key column in both to broadcast
clients['_key'] = 1
products['_key'] = 1
# Vectorized Cartesian product via merge
client_product_pairs = clients.merge(products, on='_key').drop(columns='_key')


# ### Adding rule-based flags

# In[87]:


# Step 1: Get all unique profiles
all_profiles = prod_profile['Profils cibles'].unique()

# Step 2: Convert mapped_profiles to sets
client_table['mapped_profiles_set'] = client_table['mapped_profiles'].apply(set)

# Step 3: Build all flags at once using a dictionary comprehension
flags_df = pd.DataFrame({
    f'match_{profile}': client_table['mapped_profiles_set'].apply(lambda x: int(profile in x))
    for profile in all_profiles
})

# Step 4: Concatenate all flags at once
client_table = pd.concat([client_table, flags_df], axis=1)

# Step 5: Drop helper set column
client_table.drop(columns=['mapped_profiles_set'], inplace=True)


# ### Adding target variable

# In[88]:


# Explode client_table so each product is a separate row
client_products_exploded = client_table[['REF_PERSONNE', 'products_set']].explode('products_set')

# Create a DataFrame with all client-product pairs (Cartesian product)
clients = client_table[['REF_PERSONNE']].copy()
products = prod_profile[['LIB_PRODUIT']].drop_duplicates().copy()

clients['_key'] = 1
products['_key'] = 1

client_product_pairs = clients.merge(products, on='_key').drop(columns='_key')

# Merge to flag target
client_product_pairs = client_product_pairs.merge(
    client_products_exploded.rename(columns={'products_set':'LIB_PRODUIT'}),
    on=['REF_PERSONNE','LIB_PRODUIT'],
    how='left',
    indicator='target_flag'
)

# 1 if client has product, 0 otherwise
client_product_pairs['target'] = (client_product_pairs['target_flag'] == 'both').astype(int)
client_product_pairs.drop(columns='target_flag', inplace=True)


# #### Adding client features to pairs

# In[89]:


# Select client features
client_features = client_table[['REF_PERSONNE', 'AGE', 'CODE_SEXE', 'TYPE_PERSONNE', 
                                'LIB_SECTEUR_ACTIVITE', 'contracts_count', 'guarantees_count']].copy()

# Merge features into client_product_pairs
client_product_pairs = client_product_pairs.merge(client_features, on='REF_PERSONNE', how='left')


# In[90]:


# Select numeric features from client_table
numeric_features = [
    'REF_PERSONNE',
    'active_contracts',
    'expired_contracts',
    'reduced_contracts',
    'instance_contracts',
    'terminated_contracts',
    'suspended_contracts',
    'claims_count',
    'AUTOMOBILE',
    'ENGINEERING',
    'GROUPE-MALADIE',
    'INCENDIE',
    'RISQUES DIVERS',
    'TRANSPORT',
    'VIE',
    'has_recent_claim'
]

# Merge into client_product_pairs
client_product_pairs = client_product_pairs.merge(
    client_table[numeric_features],
    on='REF_PERSONNE',
    how='left'
)


# In[91]:


profile_cols = [col for col in client_table.columns if col.startswith('match_')]

print(profile_cols)


# In[92]:


# Keep only the necessary columns from client_table
profile_flags = client_table[['REF_PERSONNE'] + profile_cols].copy()
profile_flags['profile_matches_count'] = profile_flags[profile_cols].sum(axis=1)
profile_flags['has_any_profile_match'] = (profile_flags['profile_matches_count'] > 0).astype(int)

# Reduce memory by keeping only aggregated columns
profile_flags_small = profile_flags[['REF_PERSONNE', 'profile_matches_count', 'has_any_profile_match']]

# Merge into client_product_pairs
client_product_pairs = client_product_pairs.merge(
    profile_flags_small,
    on='REF_PERSONNE',
    how='left'
)


# ### Aggregating profile flags

# In[93]:


# 1. Aggregate profile flags
profile_flags = client_table[['REF_PERSONNE'] + profile_cols].copy()
profile_flags['profile_matches_count'] = profile_flags[profile_cols].sum(axis=1)
profile_flags['has_any_profile_match'] = (profile_flags['profile_matches_count'] > 0).astype(int)

# 2. Keep only the aggregated columns to save memory
profile_flags_small = profile_flags[['REF_PERSONNE', 'profile_matches_count', 'has_any_profile_match']]

# 3. Merge aggregated flags into client_product_pairs
client_product_pairs = client_product_pairs.merge(
    profile_flags_small,
    on='REF_PERSONNE',
    how='left'
)

# 4. Confirm the columns exist
print(client_product_pairs.columns)


# ### Encoding categorical features

# In[94]:


categorical_cols = ['CODE_SEXE', 'TYPE_PERSONNE', 'LIB_SECTEUR_ACTIVITE']

for col in categorical_cols:
    client_product_pairs[col] = client_product_pairs[col].fillna('missing').astype('category').cat.codes


# ### Defining features & target

# In[96]:


features = [
    'AGE', 'CODE_SEXE', 'TYPE_PERSONNE', 
    'LIB_SECTEUR_ACTIVITE', 'contracts_count', 
    'guarantees_count', 'profile_matches_count'
]
X = client_product_pairs[features]
y = client_product_pairs['target']


# ### Train XGBoost

# In[98]:


import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score

# ----------------------------
# 1. Define features and target
# ----------------------------
features = [
    "AGE",
    "CODE_SEXE",
    "TYPE_PERSONNE",
    "LIB_SECTEUR_ACTIVITE",
    "contracts_count",
    "guarantees_count",
    "active_contracts",
    "expired_contracts",
    "reduced_contracts",
    "instance_contracts",
    "terminated_contracts",
    "suspended_contracts",
    "claims_count",
    "AUTOMOBILE",
    "ENGINEERING",
    "GROUPE-MALADIE",
    "INCENDIE",
    "RISQUES DIVERS",
    "TRANSPORT",
    "VIE",
    "has_recent_claim",
    "profile_matches_count_x",
    "has_any_profile_match_x",
    "profile_matches_count_y",
    "has_any_profile_match_y"
]

X = client_product_pairs[features]
y = client_product_pairs['target']

# ----------------------------
# 2. Train/test split
# ----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# ----------------------------
# 3. Create DMatrix for XGBoost
# ----------------------------
dtrain = xgb.DMatrix(X_train, label=y_train)
dtest = xgb.DMatrix(X_test, label=y_test)

# ----------------------------
# 4. Set parameters for GPU training
# ----------------------------
params = {
    'objective': 'binary:logistic',
    'eval_metric': 'auc',
    'max_depth': 6,
    'eta': 0.05,
    'subsample': 0.8,
    'colsample_bytree': 0.8,
    'tree_method': 'hist',   # recommended in XGBoost >=2.0 with GPU
    'device': 'cuda',        # use GPU
    'random_state': 42
}

# ----------------------------
# 5. Train the model with early stopping
# ----------------------------
evals = [(dtrain, 'train'), (dtest, 'eval')]

model = xgb.train(
    params,
    dtrain,
    num_boost_round=1000,
    evals=evals,
    early_stopping_rounds=20,
    verbose_eval=10
)

# ----------------------------
# 6. Predict and evaluate
# ----------------------------
#y_pred = model.predict(dtest)
#auc = roc_auc_score(y_test, y_pred)
#print(f'ROC-AUC: {auc:.4f}')

# ----------------------------
# 7. Save the model for later inference
# ----------------------------
model.save_model('xgb_hybrid_recommender.json')


# ### hyperparameter search

# In[99]:


import optuna
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score

# Split data
X = client_product_pairs[features]  # include all prepared features
y = client_product_pairs['target']
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Objective function for Optuna
def objective(trial):
    params = {
        'objective': 'binary:logistic',
        'eval_metric': 'auc',
        'max_depth': trial.suggest_int('max_depth', 3, 10),
        'learning_rate': trial.suggest_float('eta', 0.01, 0.3, log=True),
        'subsample': trial.suggest_float('subsample', 0.6, 1.0),
        'colsample_bytree': trial.suggest_float('colsample_bytree', 0.6, 1.0),
        'n_estimators': trial.suggest_int('n_estimators', 100, 1000),
        'tree_method': 'hist',  # if you have GPU
        'device' : "cuda",
        'random_state': 42
    }

    model = xgb.XGBClassifier(**params)
    model.fit(X_train, y_train, eval_set=[(X_test, y_test)], verbose=False)
    
    y_pred = model.predict_proba(X_test)[:,1]
    auc = roc_auc_score(y_test, y_pred)
    return auc

# Create study
study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=50)  # adjust n_trials for more search

print("Best trial:")
print(study.best_trial.params)


# ### Final training with optimized hyperparameters

# In[100]:


import joblib
import optuna
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score


# In[101]:


# ----------------------------
# Train final model
# ----------------------------
final_params = {
    'objective': 'binary:logistic',
    'eval_metric': 'auc',
    'max_depth': 7,
    'learning_rate': 0.022881962455075452,
    'subsample': 0.9685010797940659,
    'colsample_bytree': 0.6782796409177906,
    'n_estimators': 549,
    'device':'cuda',
    'tree_method': 'hist',  # GPU acceleration
    'random_state': 42
}

final_model = xgb.XGBClassifier(**final_params)
final_model.fit(X_train, y_train, eval_set=[(X_test, y_test)], verbose=True)

# ----------------------------
# Evaluate
# ----------------------------
y_pred = final_model.predict_proba(X_test)[:, 1]
auc = roc_auc_score(y_test, y_pred)
print(f'Final model ROC-AUC: {auc:.4f}')

# ----------------------------
# Save the model
# ----------------------------
joblib.dump(final_model, 'xgb_hybrid_recommender_model.pkl')
print("Model saved as 'xgb_hybrid_recommender_model.pkl'")


# In[132]:


# Pick the correct columns for client-level features
client_table = client_table.rename(columns={
    'profile_matches_count_x': 'profile_matches_count',
    'has_any_profile_match_x': 'has_any_profile_match'
})


# In[133]:


import xgboost as xgb
import pandas as pd

import xgboost as xgb
import pandas as pd

def recommend_products(client_id, client_product_pairs, prod_profile, booster_model, top_n=5):
    """
    Generate top-N product recommendations for a single client.
    
    Uses only features that were present in the training data.
    Rule-based matches are added to final_score separately.
    """
    
    # Candidate products
    candidates = prod_profile[['LIB_PRODUIT']].drop_duplicates().copy()
    client_df = pd.DataFrame({'LIB_PRODUIT': candidates['LIB_PRODUIT']})
    
    # Features used in training
    features_for_model = [
    'AGE', 'CODE_SEXE', 'TYPE_PERSONNE', 'LIB_SECTEUR_ACTIVITE',
    'contracts_count', 'guarantees_count', 'active_contracts', 'expired_contracts',
    'reduced_contracts', 'instance_contracts', 'terminated_contracts', 'suspended_contracts',
    'claims_count', 'AUTOMOBILE', 'ENGINEERING', 'GROUPE-MALADIE', 'INCENDIE',
    'RISQUES DIVERS', 'TRANSPORT', 'VIE', 'has_recent_claim', 'profile_matches_count_x',
    'has_any_profile_match_x', 'profile_matches_count_y', 'has_any_profile_match_y'
    ]
    
    # Extract client row
    client_row = client_product_pairs[client_product_pairs['REF_PERSONNE'] == client_id].iloc[0]
    
    # Broadcast client features
    for col in features_for_model:
        client_df[col] = client_row[col]

    
    # Prepare features for prediction
    X_candidates = client_df[features_for_model].copy()
    
    # Convert object columns to category codes (same as training preprocessing)
    for col in X_candidates.select_dtypes(include='object').columns:
        X_candidates[col] = X_candidates[col].astype('category').cat.codes
    
    # ✅ Directly predict with sklearn API
    client_df['pred_prob'] = booster_model.predict_proba(X_candidates)[:, 1]
    
    # Rule-based matches (products client already owns)
    owned_products = client_product_pairs[
        (client_product_pairs['REF_PERSONNE'] == client_id) & 
        (client_product_pairs['target'] == 1)
    ]['LIB_PRODUIT'].tolist()
    
    client_df['rule_match'] = client_df['LIB_PRODUIT'].apply(lambda x: int(x in owned_products))
    
    # Final score: combine ML + rule
    client_df['final_score'] = client_df['pred_prob'] + client_df['rule_match']
    
    return client_df.sort_values('final_score', ascending=False).head(top_n)[
        ['LIB_PRODUIT', 'rule_match', 'pred_prob', 'final_score']
    ]



# Example usage:
top_products = recommend_products('12145', client_product_pairs, prod_profile, final_model, top_n=5)
print(top_products)


# In[105]:


client_product_pairs.columns


# In[108]:


print(client_table[client_table['REF_PERSONNE']=='47836'].iloc[:, :20])


# In[109]:


client_product_pairs['REF_PERSONNE'].unique()[:10]


# In[127]:


# Rename columns to match the model's training data
rename_dict = {
    'profile_matches_count': 'profile_matches_count_x',
    'has_any_profile_match': 'has_any_profile_match_x'
}

client_product_pairs = client_product_pairs.rename(columns=rename_dict)


# In[129]:


import pandas as pd

def hybrid_recommend_all(client_table, prod_profile, booster_model, top_n=5):
    """
    Generate hybrid product recommendations for all clients.
    
    Combines ML predictions and rule-based flags.
    Automatically aligns feature names with the model.
    
    Args:
        client_table (DataFrame): Client info with features.
        prod_profile (DataFrame): Product info (at least 'LIB_PRODUIT').
        booster_model (XGBClassifier): Trained XGBoost model.
        top_n (int): Number of top products per client.
    
    Returns:
        DataFrame: Top-N product recommendations per client.
    """
    
    # ----------------------------
    # 1. Cartesian product: clients × products
    # ----------------------------
    clients = client_table[['REF_PERSONNE']].copy()
    products = prod_profile[['LIB_PRODUIT']].copy()
    clients['_key'] = 1
    products['_key'] = 1
    client_product_pairs = clients.merge(products, on='_key').drop(columns='_key')
    
    # ----------------------------
    # 2. Prepare client features
    # ----------------------------
    # If profile match columns exist without _x/_y suffix, rename to match training
    rename_dict = {}
    if 'profile_matches_count' in client_table.columns:
        rename_dict['profile_matches_count'] = 'profile_matches_count_x'
    if 'has_any_profile_match' in client_table.columns:
        rename_dict['has_any_profile_match'] = 'has_any_profile_match_x'
    client_table = client_table.rename(columns=rename_dict)
    
    # Features expected by model
    feature_cols = [
        'AGE', 'CODE_SEXE', 'TYPE_PERSONNE', 'LIB_SECTEUR_ACTIVITE',
        'contracts_count', 'guarantees_count', 'profile_matches_count_x', 
        'has_any_profile_match_x', 'active_contracts', 'expired_contracts', 
        'reduced_contracts', 'instance_contracts', 'terminated_contracts', 
        'suspended_contracts', 'claims_count', 'AUTOMOBILE', 'ENGINEERING', 
        'GROUPE-MALADIE', 'INCENDIE', 'RISQUES DIVERS', 'TRANSPORT', 'VIE', 
        'has_recent_claim'
    ]
    
    client_features = client_table[['REF_PERSONNE'] + feature_cols].copy()
    client_product_pairs = client_product_pairs.merge(client_features, on='REF_PERSONNE', how='left')
    
    # ----------------------------
    # 3. Encode categorical features
    # ----------------------------
    X = client_product_pairs[feature_cols].copy()
    for col in X.select_dtypes(include='object').columns:
        X[col] = X[col].astype('category').cat.codes
    
    # ----------------------------
    # 4. Predict probabilities
    # ----------------------------
    client_product_pairs['pred_prob'] = booster_model.predict_proba(X)[:, 1]
    
    # ----------------------------
    # 5. Rule-based matches
    # ----------------------------
    if 'products_set' in client_table.columns:
        exploded = client_table[['REF_PERSONNE', 'products_set']].explode('products_set')
        exploded = exploded.rename(columns={'products_set':'LIB_PRODUIT'})
        owned = exploded[['REF_PERSONNE', 'LIB_PRODUIT']].copy()
        owned['rule_match'] = 1
        client_product_pairs = client_product_pairs.merge(
            owned, on=['REF_PERSONNE','LIB_PRODUIT'], how='left'
        )
        client_product_pairs['rule_match'] = client_product_pairs['rule_match'].fillna(0).astype(int)
    else:
        client_product_pairs['rule_match'] = 0
    
    # ----------------------------
    # 6. Final score
    # ----------------------------
    client_product_pairs['final_score'] = client_product_pairs['pred_prob'] + client_product_pairs['rule_match']
    
    # ----------------------------
    # 7. Top-N products per client
    # ----------------------------
    top_per_client = client_product_pairs.sort_values(
        ['REF_PERSONNE','final_score'], ascending=[True, False]
    ).groupby('REF_PERSONNE').head(top_n)
    
    return top_per_client[['REF_PERSONNE', 'LIB_PRODUIT', 'rule_match', 'pred_prob', 'final_score']]


# In[130]:


# Generate hybrid recommendations for all clients
all_recommendations = hybrid_recommend_all(client_table, prod_profile, final_model, top_n=5)

# Show the top 5 recommendations per client
print(all_recommendations.head(20))


# In[ ]:


top5_per_client = all_recommendations.sort_values(
    ['REF_PERSONNE', 'final_score'], ascending=[True, False]
).groupby('REF_PERSONNE').head(5)

print(top5_per_client.head(10))


# In[ ]:


all_recommendations.sort_values('pred_prob', ascending=False).head(10)


# In[ ]:


top5_per_client = all_recommendations.sort_values(
    ['REF_PERSONNE', 'final_score'], ascending=[True, False]
).groupby('REF_PERSONNE').head(5)


# In[ ]:


all_recommendations.sort_values('pred_prob', ascending=False).head(10)


# In[ ]:


# Save client-product pairs
client_product_pairs.to_csv("client_product_pairs.csv")

# Save product profiles
prod_profile.to_csv("prod_profile.csv")
client_table.to_csv('client_table.csv')

print("✅ Datasets saved successfully: client_product_pairs.csv & prod_profile.csv")


#
train_data['LIB_PRODUIT']
client_table.columns
