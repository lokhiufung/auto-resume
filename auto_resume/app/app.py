import json

import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, callback_context
from dash.dependencies import Input, Output, State, ALL
from dash.exceptions import PreventUpdate

from auto_resume.app.components.company_card import CompanyCard
from auto_resume.app.db_utils import get_db_client

from auto_resume.app.api import job_history as JobHistoryApi
from auto_resume.app.api import company as CompanyApi
from auto_resume.app.api import resume as ResumeApi



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
            'start_date': company.startDate,
            'end_date': company.endDate,
            'location': company.location,
            'experiences': [{'title': job_history.title.title, 'description': job_history.description} for job_history in company.job_histories]
        })
    db_client.close()
    return data


def create_app():
    # Initialize the Dash app with a bootstrap theme
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

    initial_data = get_data()
    # Initialize app layout with sample data
    app.layout = dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(html.H1("Resume Editor"), className="mb-4"),
                    dbc.Col(
                        dbc.Button("Export to Doc", id="export-button", color="secondary", className="mb-4"),
                        width={"size": 2, "offset": 10},
                        style={"text-align": "right"}
                    )
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(id='companies-container')
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(dbc.Input(id="input-company", placeholder="Enter company name..."), width=8),
                    dbc.Col(dbc.Button("Add Company", id="add-company", color="primary", className="ms-2"), width=4)
                ],
                className="mb-4",
            ),
            # Hidden Div to store the sample data
            # dcc.Store(id='store-data', data=initial_data),
            dcc.Store(id='store-data', data=initial_data, storage_type='local'),
            dcc.Download(id='download-component'),
        ],
        fluid=True,
    )
    # app.clientside_callback(
    #     """
    #     function(n_clicks) {
    #         localStorage.clear();  // This clears everything in localStorage
    #         return '';  // Return whatever is needed to update the Output, if anything
    #     }
    #     """,
    #     Output('dummy-div', 'children'),  # Dummy output, adjust as necessary
    #     [Input('clear-storage-button', 'n_clicks')]
    # )


    @app.callback(
        Output('download-component', 'data'),
        Input('export-button', 'n_clicks'),
        [State('store-data', 'data')],
        prevent_initial_call=True
    )
    def export_resume_callback(n_clicks, current_data):
        if n_clicks:
            # data = get_data()  # Fetch your data
            file_path = ResumeApi.export_resume(data=current_data)  # Export the resume data to a .docx file
            return dcc.send_file(file_path)


    @app.callback(
        Output('store-data', 'data'),
        Input({'type': 'add-experience', 'index': ALL}, 'n_clicks'),
        [
            State({'type': 'input-title', 'index': ALL}, 'value'),  # Title input state
            State({'type': 'input-description', 'index': ALL}, 'value'),  # Description input state
            State({'type': 'add-experience', 'index': ALL}, 'id'), # To identify the company
            State('store-data', 'data'),  # current data
        ],  
        prevent_initial_call=True
    )
    def add_experience(n_clicks, titles, descriptions, btn_ids, current_data):
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

        # update current data
        for exp in current_data:
            if exp['company'] == company_name:
                exp['experiences'].append({'title': title, 'description': description})
        # Refresh the data to reflect the new experience
        return current_data
    
    @app.callback(
        Output('companies-container', 'children'),
        Input('store-data', 'data')  # Listen for changes in the store
    )
    def update_company_cards(current_data):
        return [CompanyCard(company) for company in current_data]


    return app


if __name__ == '__main__':
    app = create_app()
    app.run_server(debug=True)
