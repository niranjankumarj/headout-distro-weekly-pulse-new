from parser import DashboardData

datasets = DashboardData("downloads/api_agent_test").load()

print("\n" + "=" * 60)
print("GBV")
print("=" * 60)

df = datasets["GBV"]

print(df.head())

print()

print("Rows :", len(df))
print("First:", df["Period"].min())
print("Last :", df["Period"].max())