from parser import DashboardData


def load_dashboard(folder):

    dashboard = DashboardData(folder)

    return dashboard.load()