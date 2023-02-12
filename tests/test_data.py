from viztest import main


def test_data():
    print()
    jdata = main.read_data_file()
    dframes = main.convert_json_to_dataframes(jdata)
    print(dframes["teams"])

def test_cds():
    print("Testing CDS")
    teams_cds = main.get_column_data_source()
    print(teams_cds.data)

def test_datatable():
    cds = main.get_column_data_source()
    table = main.get_datatable(cds)
