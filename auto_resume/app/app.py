import json

import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, callback_context
from dash.dependencies import Input, Output, State, MATCH, ALL
from dash.exceptions import PreventUpdate

from auto_resume.app.components.company_card import CompanyCard
from auto_resume.app.db_utils import get_db_client

from auto_resume.app.api import job_history as JobHistoryApi
from auto_resume.app.api import company as CompanyApi



# # Sample data with companies and experiences
# sample_data = [
#     {"company": "Company A", "experiences": ["Led software development", "Managed a team of engineers"]},
#     {"company": "Company B", "experiences": ["Conducted market research", "Developed marketing strategies"]}
# ]

def get_data():
    db_client = get_db_client()
    companies = CompanyApi.get_companies(db_client)
    data = []
    for company in companies:
        data.append({
            'company': company.name,
            'experiences': [{'title': job_history.title.title, 'description': job_history.description} for job_history in company.job_histories]
        })
    db_client.close()
    return data


def create_app():
    # Initialize the Dash app with a bootstrap theme
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

    sample_data = get_data()
    # Initialize app layout with sample data
    app.layout = dbc.Container(
        [
            dbc.Row(dbc.Col(html.H1("Resume Editor"), className="mb-4")),
            dbc.Row(
                [
                    dbc.Col(
                        [CompanyCard(company) for company in sample_data],
                        id='companies-container'
                    )
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(dbc.Input(id="input-company", placeholder="Enter company name..."), width=8),
                    dbc.Col(dbc.Button("Add Company", id="add-company", color="primary", className="ms-2"), width=4)
                ],
                className="mb-4",
            ),
        ],
        fluid=True,
    )


    @app.callback(
        Output('companies-container', 'children'),
        Input({'type': 'add-experience', 'index': ALL}, 'n_clicks'),
        [State({'type': 'input-title', 'index': ALL}, 'value'),  # Title input state
         State({'type': 'input-description', 'index': ALL}, 'value'),  # Description input state
         State({'type': 'add-experience', 'index': ALL}, 'id')],  # To identify the company
        prevent_initial_call=True
    )
    def add_experience(n_clicks, titles, descriptions, btn_ids):
        ctx = callback_context
        if not ctx.triggered:
            raise PreventUpdate
        
        # Get the ID of the button that was clicked
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        button_id = json.loads(button_id)
        company_name = button_id['index']
        # Extract the title and description for the experience to be added
        for i, btn_id in enumerate(btn_ids):
            if btn_id['index'] == company_name:
                title = titles[i]
                description = descriptions[i]
                break
        else:
            raise PreventUpdate

        # Ensure both title and description are provided
        if not title or not description:
            raise PreventUpdate
        # Create a new job history entry in the database
        db_client = get_db_client()
        JobHistoryApi.create_job_history(db_client, company_name, title, description)
        db_client.close()

        # Refresh the data to reflect the new experience
        return [CompanyCard(company) for company in get_data()]

    return app


if __name__ == '__main__':
    app = create_app()
    app.run_server(debug=True)
