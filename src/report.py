from parser import DashboardData


class ReportBuilder:

    def __init__(self):

        self.datasets = {}

    # -----------------------------------
    # Load Dashboard
    # -----------------------------------

    def load_dashboard(self, name, folder):

        dashboard = DashboardData(folder)

        self.datasets[name] = dashboard.load()

    # -----------------------------------
    # Dataset
    # -----------------------------------

    def dataset(self, dashboard, dataset):

        return self.datasets[dashboard][dataset]