

import os
import json
import dash
from dash import html, dcc, Output, Input, State, ctx
import dash_bootstrap_components as dbc
from werkzeug.utils import secure_filename
import tempfile

from auto_resume.sdk.resume_templates.create_resume_v1 import create_resume
from auto_resume.engine_v1 import Engine as EngineV1
from auto_resume.engine_v2 import Engine as EngineV2


def create_app():
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    server = app.server  # for deployment if needed

    app.layout = dbc.Container([
        html.H2("AI Resume Generator", className="my-4"),

        dbc.Row([
            dbc.Col([
                dcc.Upload(
                    id='upload-resume',
                    children=html.Div([
                        'Drag and Drop or ',
                        html.A('Select Resume File (JSON)')
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
                html.Div(id='uploaded-filename', style={'margin-bottom': '10px', 'fontStyle': 'italic'}),
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
            ], width=6),
        ]),

        html.Hr(),

        dbc.Spinner(html.Div(id='output-metrics'), color="primary", fullscreen=False),
        html.Div(id='download-link')
    ])
    
    @app.callback(
        Output('uploaded-filename', 'children'),
        Input('upload-resume', 'filename'),
        prevent_initial_call=True
    )
    def update_uploaded_filename(filename):
        if filename:
            return f"Uploaded file: {filename}"
        return ""

    
    @app.callback(
        Output('output-metrics', 'children'),
        Output('download-link', 'children'),
        Input('generate-btn', 'n_clicks'),
        State('upload-resume', 'contents'),
        State('upload-resume', 'filename'),
        State('job-description', 'value'),
        State('job-link', 'value'),
        State('engine-version', 'value'),
        prevent_initial_call=True
    )
    def generate_resume(n_clicks, resume_content, resume_filename, job_desc, job_link, version):
        if not resume_content or not job_desc:
            return "Please upload a resume and enter a job description.", None

        # Parse uploaded file content
        import base64
        content_type, content_string = resume_content.split(',')
        decoded = base64.b64decode(content_string)
        base_resume = json.loads(decoded)

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

            return [html.Pre(json.dumps(metrics, indent=2))], download_component

    return app
