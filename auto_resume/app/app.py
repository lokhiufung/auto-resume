import json
from datetime import datetime

import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, callback_context
from dash.dependencies import Input, Output, State, ALL
from dash.exceptions import PreventUpdate

from auto_resume.app.components.company_card import CompanyCard
from auto_resume.app.components.new_company_form import NewCompanyForm
from auto_resume.app.db_utils import get_db_client

from auto_resume.app.api import job_history as JobHistoryApi
from auto_resume.app.api import company as CompanyApi
from auto_resume.app.api import resume as ResumeApi
from auto_resume.app.api import job_ad as JobAdApi
from auto_resume.sdk.metrics import get_keyword_score


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
    # Initialize app layout with the new structure
    app.layout = dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(html.H1("Resume Editor"), className="mb-4", style={'text-align': 'center'}, width=12),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(dbc.Button("Export to Doc", id="export-button", color="secondary", className="mb-4"), width={"size": 2, "offset": 10}, style={"text-align": "right"})
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        # All existing components will be inside this column
                        [
                            dbc.Row(dbc.Col(id='companies-container')),
                            dbc.Row(dbc.Col([NewCompanyForm()], width=12), className="mb-4"),
                            dcc.Store(id='store-data', data=initial_data),
                            dcc.Download(id='download-component'),
                        ],
                        md=6,  # Set the size of the left column
                    ),
                    dbc.Col(
                        # New components for job advertisement textarea and button
                        [
                            dbc.Textarea(id="job-ad-text", className="mb-4", style={'width': '100%', 'height': '500px'}),
                            dbc.Button("Show Top Matched Experiences", id="send-job-ad-button", color="primary", className="mb-4"),
                            html.Div(id='job-ad-response')  # Element to display the response
                        ],
                        md=6,  # Set the size of the right column
                    ),
                ]
            ),
        ],
        fluid=True,
        style={'width': '90%', 'marginTop': '30px'}  # Adjust the width as necessary
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
        Output("end-date-row", "style"),
        [Input("checkbox-current-job", "value")]
    )
    def toggle_end_date_visibility(current_job_checked):
        if current_job_checked:
            return {"display": "none"}  # End Date field is hidden
        else:
            return {}  # End Date field is shown normally

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

    @app.callback(
        Output('success-message', 'children'),  # Assuming you want to display a confirmation or error message
        Output('success-message', 'is_open'), 
        Input('submit-new-company', 'n_clicks'),  # The button the user clicks to submit the form
        [State('input-company-name', 'value'),
        State('input-company-description', 'value'),
        State('input-company-start', 'value'),
        State('input-company-end', 'value'),
        State('input-company-location', 'value'),
        State('checkbox-current-job', 'value')],  # Assuming the name of your checkbox id is `checkbox-current-job`
        prevent_initial_call=True
    )
    def add_company(n_clicks, name, description, start_date, end_date, location, is_current_job):
        if n_clicks is None:
            return "Please fill in the form to add a company."
        start_date = datetime.strptime(start_date, "%Y-%m-%d").strftime("%b %Y")
        db_client = get_db_client()
        # Assuming you have a database session 'db_session' accessible within this function
        # Adjust logic based on your 'create_company' signature and your form's 'is_current_job' handling
        if is_current_job:
            end_date = 'Now'  # or any logic you want to apply for the 'current job'
        # Call the DB function
        try:
            CompanyApi.create_company(db_client, name, description, start_date, end_date, location)
            return "Company successfully added!", True
        except Exception as e:
            print(e)  # For debugging, consider a more robust error handling/logging
            return "Failed to add company. Please try again.", True
        finally:
            db_client.close()
    
    @app.callback(
        Output('companies-container', 'children', allow_duplicate=True),  # Update the companies container to show the most relevant experiences
        Input('send-job-ad-button', 'n_clicks'),
        State('job-ad-text', 'value'),  # The value of the text area where the job ad is input
        State('store-data', 'data'),  # The existing job experiences stored in the app
        prevent_initial_call=True
    )
    def update_relavent_experience(n_clicks, job_ad_text, experiences_data):
        if not job_ad_text:
            return "Please enter a job advertisement text."
        
        # Extract keywords from the job ad
        keywords = JobAdApi.extract_keywords(job_ad_text)['keywords']

        # Calculate scores for each job experience and sort them within each company
        for company_data in experiences_data:
            # Calculate score for each experience
            for experience in company_data['experiences']:
                experience_description = experience['description']
                experience_score = get_keyword_score(experience_description, keywords)
                experience['score'] = experience_score  # Add score to each experience

            # Sort experiences within each company based on score, keep only top 3
            company_data['experiences'] = sorted(company_data['experiences'], key=lambda x: x['score'], reverse=True)[:3]

            # Calculate total score for each company as sum of top 3 experiences (after sorting)
            company_data['total_score'] = sum(exp['score'] for exp in company_data['experiences'])

        # Sort the companies based on the total score of their top 3 experiences
        sorted_experiences_data = sorted(experiences_data, key=lambda x: x['total_score'], reverse=True)

        # Now update the layout to show these sorted and filtered experiences
        return [CompanyCard(company) for company in sorted_experiences_data]


    return app


if __name__ == '__main__':
    app = create_app()
    app.run_server(debug=True)
