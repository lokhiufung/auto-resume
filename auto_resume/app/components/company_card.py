import dash_bootstrap_components as dbc
from dash import html


def CompanyCard(company_data):
    return dbc.Card(
        [
            dbc.CardHeader(company_data['company']),
            dbc.CardBody(
                [
                    dbc.ListGroup(
                        [
                            dbc.ListGroupItem(
                                [
                                    html.Div(exp['description'], className='mb-2'),  # Description above
                                    dbc.Badge(exp['title'], color="primary", className="me-1")  # Title as a badge below
                                ]
                            ) for exp in company_data['experiences']
                        ],
                        id={'type': 'experience-list', 'index': company_data['company']},
                        className="mb-3"
                    ),
                    dbc.Row(
                        dbc.Col(dbc.Input(id={'type': 'input-title', 'index': company_data['company']}, placeholder="Title"), width=12),
                        className="mb-2"
                    ),
                    dbc.Row(
                        dbc.Col(dbc.Textarea(id={'type': 'input-description', 'index': company_data['company']}, placeholder="Description", rows=5, value=''), width=12),
                        className="mb-2"
                    ),
                    dbc.Button("Add Experience", id={'type': 'add-experience', 'index': company_data['company']}, n_clicks=0, className="mt-2")
                ],
            ),
        ],
        className="mb-4",
    )
