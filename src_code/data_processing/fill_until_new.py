import pandas as pd

# Filsti til inputfilen
file_path = "TabellSVV_1990_97.csv"

# Funksjon for å fylle frem til ny verdi dukker opp
def fill_until_new(series):
    last_val = None
    result = []
    for val in series:
        if pd.notna(val) and str(val).strip() != "":
            last_val = val
        result.append(last_val)
    return result

# Les CSV med semikolon-separator
df = pd.read_csv(file_path, header=None, sep=";", engine="python")

# Velg rad 9 og nedover (indeks 8)
df_sub = df.iloc[8:].copy()

# Fyll kolonne 0 (Kommune) og kolonne 1 (Måned)
df_sub[0] = fill_until_new(df_sub[0])
df_sub[1] = fill_until_new(df_sub[1])

# Oppdater hoveddataframe
df.update(df_sub)

# Lagre til ny CSV
df.to_csv("TabellSVV_1990_97_converted.csv", index=False, header=False, sep=";")

print("✅ Ferdig! Fil lagret")
