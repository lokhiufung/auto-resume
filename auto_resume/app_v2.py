import os
import json
import dash
from dash import html, dcc, Output, Input, State, ctx
import dash_bootstrap_components as dbc
from werkzeug.utils import secure_filename
import tempfile
import base64

DEFAULT_RESUME_PATH = os.path.join(os.getenv('HOME'), '.auto-resume', 'base_resumes')

from auto_resume.sdk.resume_templates.create_resume_v1 import create_resume
from auto_resume.engine_v1 import Engine as EngineV1
from auto_resume.engine_v2 import Engine as EngineV2


def create_app():
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    app.config.suppress_callback_exceptions = True
    server = app.server  # for deployment if needed

    app.layout = dbc.Container([
        html.H2("📄 auto-resume © - An AI Resume Generator", className="my-4 text-center"),

        dbc.Row([
            dbc.Col([
                dbc.Row([
                    dbc.Col([
                        html.H5("Select or Upload Base Resume", className="mt-4"),
                        dcc.Dropdown(
                            id='base-resume-selector',
                            options=[],  # To be populated dynamically
                            placeholder="Select previously uploaded base resume",
                            style={'margin-bottom': '10px'}
                        ),
                        dcc.Upload(
                            id='upload-new-base-resume',
                            children=html.Div([
                                'Drag and Drop or ',
                                html.A('Upload New Base Resume (JSON)')
                            ]),
                            style={
                                'width': '100%',
                                'height': '60px',
                                'lineHeight': '60px',
                                'borderWidth': '1px',
                                'borderStyle': 'dashed',
                                'borderRadius': '5px',
                                'textAlign': 'center',
                                'margin-bottom': '10px'
                            },
                            multiple=False
                        ),
                        html.Div(id='base-resume-status', style={'margin-bottom': '10px', 'fontStyle': 'italic'}),
                        dcc.Textarea(
                            id='job-description',
                            placeholder='Paste Job Description here...',
                            style={'width': '100%', 'height': 200, 'margin-bottom': '10px'}
                        ),
                        dcc.Input(
                            id='job-link',
                            type='text',
                            placeholder='Optional: Job Posting Link',
                            style={'width': '100%', 'margin-bottom': '10px'}
                        ),
                        dcc.Dropdown(
                            id='engine-version',
                            options=[
                                {'label': 'Engine v1', 'value': 'v1'},
                                {'label': 'Engine v2', 'value': 'v2'}
                            ],
                            value='v1',
                            style={'margin-bottom': '10px'}
                        ),
                        dbc.Button("Generate Resume", id='generate-btn', color='primary', className='w-100 mt-2'),
                    ], width=6)
                ], justify='center'),
            ]),
        ]),

        html.Hr(),

        dbc.Spinner(html.Div(id='output-metrics'), color="primary", fullscreen=False),
        html.Div(id='download-link')
    ])
    
    @app.callback(
        Output('base-resume-status', 'children'),
        Input('upload-new-base-resume', 'contents'),
        State('upload-new-base-resume', 'filename'),
        prevent_initial_call=True
    )
    def save_new_base_resume(content, filename):
        if content:
            try:
                content_type, content_string = content.split(',')
                decoded = base64.b64decode(content_string)
                os.makedirs(DEFAULT_RESUME_PATH, exist_ok=True)
                with open(os.path.join(DEFAULT_RESUME_PATH, filename), 'wb') as f:
                    f.write(decoded)
                return f"Uploaded new base resume: {filename}"
            except Exception:
                return "Failed to upload base resume. Please ensure it is a valid JSON file."
        return ""

    @app.callback(
        Output('base-resume-selector', 'options'),
        Input('base-resume-selector', 'id')
    )
    def update_resume_list(_):
        resume_dir = DEFAULT_RESUME_PATH
        os.makedirs(resume_dir, exist_ok=True)
        resumes = os.listdir(resume_dir)
        return [{'label': name, 'value': name} for name in resumes]

    @app.callback(
        Output('output-metrics', 'children'),
        Output('download-link', 'children'),
        Input('generate-btn', 'n_clicks'),
        State('job-description', 'value'),
        State('job-link', 'value'),
        State('engine-version', 'value'),
        State('base-resume-selector', 'value'),
        prevent_initial_call=True
    )
    def generate_resume(n_clicks, job_desc, job_link, version, selected_resume_name):
        if not job_desc:
            return "Please enter a job description.", None

        base_resume_path = os.path.join(DEFAULT_RESUME_PATH, selected_resume_name or "")
        if selected_resume_name and os.path.exists(base_resume_path):
            with open(base_resume_path, 'r') as f:
                base_resume = json.load(f)
            resume_source = f"Using saved base resume: {selected_resume_name}"
        else:
            return "Please upload or select a base resume.", None

        with tempfile.TemporaryDirectory() as tmpdir:
            storage_path = os.path.join(tmpdir, "storage")
            os.makedirs(storage_path, exist_ok=True)

            engine_config = {
                'base_resume': base_resume,
                'job_description': job_desc
            }

            Engine = EngineV1 if version == "v1" else EngineV2
            engine = Engine(engine_config=engine_config, storage=storage_path)
            result = engine.start(save=True)

            metrics = result.get("metrics", {})
            resume_doc = create_resume(resume=result['result'])

            output_path = os.path.join(tmpdir, "resume-customized.docx")
            resume_doc.save(output_path)

            # Read back as base64 for download link
            with open(output_path, "rb") as f:
                resume_bytes = f.read()
                b64_resume = base64.b64encode(resume_bytes).decode()

            download_component = html.A(
                "Download Your Resume",
                href="data:application/vnd.openxmlformats-officedocument.wordprocessingml.document;base64," + b64_resume,
                download="resume_.docx",
                target="_blank",
                className="btn btn-success mt-3"
            )

            table_rows = []
            for key, value in metrics.items():
                table_rows.append(html.Tr([html.Td(key), html.Td(str(value))]))

            metrics_table = dbc.Table([
                html.Thead(html.Tr([html.Th("Metric"), html.Th("Value")])),
                html.Tbody(table_rows)
            ], bordered=True, hover=True, responsive=True, striped=True, className="mt-3")

            output_display = html.Div([
                html.P(resume_source, style={'fontStyle': 'italic', 'color': '#666'}),
                html.H5("Resume Metrics"),
                metrics_table
            ])
            return output_display, download_component

    return app
