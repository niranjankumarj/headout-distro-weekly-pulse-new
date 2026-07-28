from pathlib import Path
import pandas as pd


class DashboardData:

    def __init__(self, folder):
        self.folder = Path(folder)
        self.datasets = {}

    # ---------------------------------------------------
    # Standard Metric CSV
    # ---------------------------------------------------

    def clean_metric_dataframe(self, df, dataset_name):

        # Metric names are stored in the first row
        metric_names = list(df.iloc[0])

        # Data starts from second row
        data = df.iloc[1:].copy()

        # Default to first Current Period column
        value_column = 1

        # If this CSV contains multiple Current Period columns,
        # select the one whose metric name matches the dataset.
        for i in range(1, len(metric_names)):
            metric = str(metric_names[i]).strip()

            if metric == dataset_name:
                value_column = i
                break

        cleaned = pd.DataFrame({
            "Period": pd.to_datetime(
                data.iloc[:, 0],
                errors="coerce"
            ),
            "Current Period": pd.to_numeric(
                data.iloc[:, value_column],
                errors="coerce"
            )
        })

        cleaned = cleaned[
            cleaned["Period"].notna()
        ].copy()

        cleaned.sort_values(
            "Period",
            inplace=True
        )

        cleaned.reset_index(
            drop=True,
            inplace=True
        )

        return cleaned

    # ---------------------------------------------------
    # Multi Metric CSV
    # ---------------------------------------------------

    def split_multi_metric_dataframe(self, df):

        metric_names = list(df.iloc[0])

        data = df.iloc[1:].copy()

        period = pd.to_datetime(
            data.iloc[:, 0],
            errors="coerce"
        )

        aliases = {
            "Partner Share": "Partner Share",
            "Revenue": "Revenue",
            "Direct Costs Usd": "Direct Costs",
            "CM1": "CM1",
            "Gross Bookings": "GBV",
            "Amount Distribution Partner Net Pric Usd": "Net Price",
            "CM2": "CM2",
        }

        datasets = {}

        for i in range(1, 8):

            metric_name = aliases.get(
                str(metric_names[i]).strip(),
                str(metric_names[i]).strip()
            )

            metric_df = pd.DataFrame({
                "Period": period,
                "Current Period": pd.to_numeric(
                    data.iloc[:, i],
                    errors="coerce"
                )
            })

            metric_df = metric_df[
                metric_df["Period"].notna()
            ].copy()

            metric_df.sort_values(
                "Period",
                inplace=True
            )

            metric_df.reset_index(
                drop=True,
                inplace=True
            )

            datasets[metric_name] = metric_df

        return datasets

    # ---------------------------------------------------
    # Loader
    # ---------------------------------------------------

    def load(self):

        csv_files = sorted(
            self.folder.rglob("*.csv")
        )

        print(
            f"\nLoading {len(csv_files)} CSV files from {self.folder.name}"
        )

        for file in csv_files:

            try:

                relative = file.relative_to(self.folder)

                if len(relative.parts) == 1:
                    dataset_name = file.stem
                else:
                    dataset_name = relative.parts[0]

                # -----------------------------
                # Standard CSV
                # -----------------------------

                if file.stem != "CM1":

                    df = pd.read_csv(file)

                    if (
                        len(df.columns) >= 2
                        and df.columns[0] == "Period"
                    ):
                        df = self.clean_metric_dataframe(
                            df,
                            dataset_name,
                        )

                    self.datasets[dataset_name] = df

                    print(f"✓ {dataset_name}")

                    continue

                # -----------------------------
                # Multi Metric CSV
                # -----------------------------

                df = pd.read_csv(file)

                split = self.split_multi_metric_dataframe(df)

                for name, metric_df in split.items():

                    if name in self.datasets:
                        continue

                    self.datasets[name] = metric_df

                    print(f"✓ {name}")

            except Exception as e:

                print(f"✗ {file}")
                print(e)

        return self.datasets