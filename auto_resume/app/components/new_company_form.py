from dash import html
import dash_bootstrap_components as dbc

def NewCompanyForm():
    return dbc.Card(
        [
            dbc.CardHeader("Add New Company"),
            dbc.CardBody(
                [
                    # Company Name
                    dbc.Row(
                        dbc.Col(
                            [
                                dbc.Label("Company Name:", html_for="input-company-name"),
                                dbc.Input(id="input-company-name", placeholder="Enter company name", required=True),
                            ],
                            className="mb-3"
                        )
                    ),
                    # Start Date
                    dbc.Row(
                        dbc.Col(
                            [
                                dbc.Label("Start Date:", html_for="input-company-start"),
                                dbc.Input(id="input-company-start", placeholder="YYYY-MM-DD", type="date", required=True),
                            ],
                            className="mb-3"
                        )
                    ),
                    # End Date - Initially visible
                    dbc.Row(
                        dbc.Col(
                            [
                                dbc.Label("End Date:", html_for="input-company-end"),
                                dbc.Input(id="input-company-end", placeholder="YYYY-MM-DD", type="date"),
                            ],
                            className="mb-3"
                        ),
                        id="end-date-row",
                    ),
                    # Checkbox for "Current Job"
                    dbc.Row(
                        dbc.Col(
                            [
                                dbc.Label("Current job?", html_for="input-current-job"),
                                dbc.Checkbox(id="checkbox-current-job", className="form-check-input", value=False),
                            ],
                            width="auto"
                        ),
                        className="mb-3"
                    ),
                    # dbc.Row(dbc.Col(html.Label("This is my current job", htmlFor="checkbox-current-job"))),
                    # Input for Location
                    dbc.Row(
                        dbc.Col(
                            [
                                dbc.Label("Location:", html_for="input-company-location"),
                                dbc.Input(id="input-company-location", placeholder="Enter the company location", required=True),
                            ],
                            className="mb-3"
                        )
                    ),
                    # Textarea for Description
                    dbc.Row(
                        dbc.Col(
                            [
                                dbc.Label("Description:", html_for="input-company-description"),
                                dbc.Textarea(id="input-company-description", placeholder="Enter the company description", rows=5, required=False),
                            ],
                            className="mb-3"
                        )
                    ),
                    dbc.Row(
                        dbc.Col(dbc.Alert(id="success-message", color="success", is_open=False), width={"size": 6, "offset": 3}),
                        className="mb-2",
                    ),
                    # Button to Submit
                    dbc.Button("Submit", id="submit-new-company", color="primary", className="mt-3"),
                ]
            ),
        ],
        className="mb-4",
    )
