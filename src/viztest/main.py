import pathlib
import json
import os

import bokeh.layouts
import bokeh.models
import bokeh.plotting

import numpy as np
import pandas as pd

APP_FOLDER = pathlib.Path(__file__).parent

def hello():
    return "hello!"

def read_data_file() -> dict[str, pd.DataFrame]:
    with open(APP_FOLDER / "viewer_data.json", "rt") as pfile:
        return json.load(pfile)

def convert_json_to_dataframes(jdata):
    """Converts JSON string from Flask server into dict of DataFrames
    
    Args: jdata can be a JSON string, or a Python data strcuture created
        by json.load() or json.loads().

    Returns: A dictionary of four pandas DataFrames
    """

    if isinstance(jdata, str):
        jdata = json.loads(jdata)
        
    measures =  (
        pd.DataFrame(jdata["measures"])
        .sort_values(["match", "phase", "task", "team_number"])
        .reset_index(drop=True)
        .loc[:, ["match", "team_number", "phase", "task", "measure_type", "measure1", "measure2"]]
    )
    
    teams = (
        pd.DataFrame(jdata["teams"])
        .sort_values(["team_number"])
        .reset_index(drop=True)
        .loc[:, ["team_number", "team_name", "city", "state", "country"]]
    )
    
    matches = (
        pd.DataFrame(jdata["matches"])
        .sort_values(["match", "alliance", "station"])
        .reset_index(drop=True)
        .loc[:, ["match", "alliance", "station", "team_number"]]
    )
    
    status = (
        pd.DataFrame(jdata["status"])
        .reset_index(drop=True)
    )
    return {
        "measures": measures,
        "matches": matches,
        "status": status ,
        "teams": teams,
    }

def get_column_data_source():
    dframes = convert_json_to_dataframes(read_data_file())
    # print(dframes["teams"])
    teams = bokeh.models.ColumnDataSource(dframes["teams"])

    return teams

def get_datatable(cds):
    columns = [
        bokeh.models.TableColumn(field="team_number"),
        bokeh.models.TableColumn(field="team_name"),
        bokeh.models.TableColumn(field="city"),
        bokeh.models.TableColumn(field="state"),
    ]
    table = bokeh.models.DataTable(source=cds, columns=columns)
    return table

cds = get_column_data_source()
table = get_datatable(cds)
column_layout = bokeh.layouts.column(children=[
    bokeh.models.Div(text="<h1>Teams Table Test 2</h1>"),
    table
])

bokeh.plotting.curdoc().add_root(column_layout)

