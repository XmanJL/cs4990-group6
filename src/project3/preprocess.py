# preprocessing pipeline for the population data
import pandas as pd

# aggregate populations from start_age to end_age (exclusive)
# then add the result as a new column in the dataframe
def aggregate_age_range(df, start_age, end_age):
    age_columns = [f"POP_{age}" for age in range(start_age, end_age)]
    return df[age_columns].sum(axis=1)

# preprocess the raw population data and return a cleaned dataframe
def preprocess(csv_path="./high_imm_pop.csv"):

    df = pd.read_csv(csv_path)
    df = df.drop(columns=["TOTAL_POP"])
    df = df[df["RACE"].isin([1, 2, 4])]

    age_groups = {
        "POP_0_19": (0, 20),
        "POP_20_39": (20, 40),
        "POP_40_59": (40, 60),
        "POP_60_79": (60, 80),
        "POP_80_100": (80, 101),
    }

    processed_df = df[["RACE", "YEAR"]].copy()
    for column_name, (start_age, end_age) in age_groups.items():
        processed_df[column_name] = aggregate_age_range(df, start_age, end_age)

    processed_df = processed_df.drop_duplicates(subset=["RACE", "YEAR"])
    processed_df.to_csv("./high_imm_pop_processed.csv", index=False)

    return processed_df

# testing purposes
if __name__ == "__main__":
    processed_df = preprocess("./high_imm_pop.csv")
    print(processed_df)