# Dashboard Development Example using Dash (Python)
# Deliverable: A fully functional dashboard with actionable insights

import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
from dash import dash_table

# Example custom dataset: Bhavana's Data (replace with your own data as needed)
# For demonstration, let's create a DataFrame with some sample data
# Bhavana's Students Score Data
students = ["Alice", "Bob", "Charlie", "David", "Eva"]
subjects = ["Math", "Science", "English", "History", "Art"]
scores_data = [
    [85, 90, 78, 92, 88],   # Alice
    [79, 85, 82, 80, 75],   # Bob
    [92, 88, 95, 91, 90],   # Charlie
    [70, 75, 68, 72, 74],   # David
    [88, 92, 85, 90, 91]    # Eva
]
df = pd.DataFrame(scores_data, columns=subjects, index=students).reset_index().rename(columns={'index': 'Student'})

# Calculate average per student and per subject
df['Average'] = df[subjects].mean(axis=1)
subject_avg = df[subjects].mean().reset_index()
subject_avg.columns = ['Subject', 'Average']

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.H1("🎓 Bhavana's Student Performance Dashboard🎓", style={
            'textAlign': 'center',
            'color': '#1e293b',
            'marginTop': '30px',
            'marginBottom': '10px',
            'fontFamily': 'Segoe UI, Arial, sans-serif',
            'fontWeight': 'bold',
            'letterSpacing': '2px',
            'textShadow': '1px 1px 2px #c7d2fe'
        }),
        html.Hr(style={'borderTop': '2px solid #6366f1', 'width': '60%', 'margin': 'auto'}),
        html.Div([
            html.Label("Select Student(s):", style={
                'fontWeight': 'bold',
                'fontSize': '18px',
                'color': '#334155',
                'marginBottom': '8px'
            }),
            dcc.Dropdown(
                id='student-dropdown',
                options=[{'label': s, 'value': s} for s in students],
                value=students,
                multi=True,
                style={
                    'backgroundColor': '#f1f5f9',
                    'color': '#334155',
                    'border': '1px solid #6366f1',
                    'borderRadius': '8px',
                    'fontSize': '16px'
                }
            ),
        ], style={
            'width': '40%',
            'margin': '30px auto 10px auto',
            'padding': '20px',
            'backgroundColor': '#f8fafc',
            'borderRadius': '16px',
            'boxShadow': '0 4px 16px rgba(99,102,241,0.10)'
        }),
        html.Div([
            dcc.Graph(id='student-bar', config={'displayModeBar': False}, style={
                'display': 'inline-block', 'width': '48%', 'verticalAlign': 'top', 'minWidth': '320px',
                'backgroundColor': '#fff', 'borderRadius': '12px', 'boxShadow': '0 2px 8px #e0e7ef'
            }),
            dcc.Graph(id='student-line', config={'displayModeBar': False}, style={
                'display': 'inline-block', 'width': '48%', 'verticalAlign': 'top', 'minWidth': '320px', 'marginLeft': '2%',
                'backgroundColor': '#fff', 'borderRadius': '12px', 'boxShadow': '0 2px 8px #e0e7ef'
            })
        ], style={'width': '100%', 'textAlign': 'center', 'margin': 'auto', 'marginTop': '10px'}),
        html.Div([
            dcc.Graph(id='subject-avg-bar', config={'displayModeBar': False}, style={
                'width': '60%', 'margin': 'auto',
                'backgroundColor': '#fff', 'borderRadius': '12px', 'boxShadow': '0 2px 8px #e0e7ef'
            })
        ], style={
            'marginTop': '30px',
            'marginBottom': '10px',
            'backgroundColor': '#f1f5f9',
            'borderRadius': '12px',
            'padding': '20px',
            'boxShadow': '0 2px 8px rgba(99,102,241,0.08)'
        }),
        html.Div(id='insights', style={
            'margin': '30px auto',
            'fontSize': 18,
            'width': '60%',
            'backgroundColor': '#f3f4f6',
            'borderRadius': '12px',
            'padding': '24px',
            'color': '#334155',
            'boxShadow': '0 4px 16px rgba(99,102,241,0.10)'
        })
    ], style={'backgroundColor': '#f8fafc', 'minHeight': '100vh'})
])

@app.callback(
    Output('student-bar', 'figure'),
    Output('student-line', 'figure'),
    Output('subject-avg-bar', 'figure'),
    Output('insights', 'children'),
    Input('student-dropdown', 'value'),
    Input('student-bar', 'clickData')
)
def update_dashboard(selected_students, clickData):
    filtered_df = df[df['Student'].isin(selected_students)]
    # Bar plot: Student vs Average
    bar_fig = px.bar(
        filtered_df, x='Student', y='Average',
        color='Student', text_auto='.2f',
        title="Average Score per Student",
        template='plotly_white',
        color_discrete_sequence=px.colors.sequential.Blues
    )
    bar_fig.update_layout(
        title_font=dict(size=22, color='#6366f1', family='Segoe UI, Arial, sans-serif'),
        plot_bgcolor='#f8fafc',
        paper_bgcolor='#f8fafc',
        margin=dict(l=20, r=20, t=60, b=40),
        height=400,
        showlegend=False,
        xaxis=dict(title_font=dict(size=16, color='#334155'), tickfont=dict(size=15, color='#334155')),
        yaxis=dict(title_font=dict(size=16, color='#334155'), tickfont=dict(size=15, color='#334155'))
    )
    bar_fig.update_traces(marker=dict(line=dict(width=1, color='#6366f1'), opacity=0.92))

    # Determine which student to highlight in the line plot
    highlight_student = None
    if clickData and 'points' in clickData and len(clickData['points']) > 0:
        highlight_student = clickData['points'][0]['x']

    # Line plot: Student's scores across subjects
    melted = filtered_df.melt(id_vars=['Student'], value_vars=subjects, var_name='Subject', value_name='Score')

    if highlight_student and highlight_student in melted['Student'].values:
        highlight_df = melted[melted['Student'] == highlight_student]
        line_fig = px.line(
            highlight_df, x='Subject', y='Score', color='Student', markers=True,
            title=None,
            template='plotly_white',
            color_discrete_sequence=['#f59e42']
        )
        line_fig.update_traces(
            marker=dict(size=18, color='#f59e42', line=dict(width=5, color='#fde68a')),
            line=dict(width=5, color='#f59e42')
        )
        line_title = (
            "<div style='margin-bottom: 36px;'></div>"
            "<span style='font-size:26px;color:#38bdf8;font-family:Segoe UI,Arial,sans-serif;font-weight:bold;'>"
            f"Scores by Subject for {highlight_student}</span>"
        )
    else:
        line_fig = px.line(
            melted, x='Subject', y='Score', color='Student', markers=True,
            title=None,
            template='plotly_white',
            color_discrete_sequence=['#38bdf8'] * len(filtered_df['Student'].unique())
        )
        line_fig.update_traces(
            marker=dict(size=14, color='#38bdf8', line=dict(width=3, color='#bae6fd')),
            line=dict(width=4, color='#38bdf8')
        )
        line_title = (
            "<span style='font-size:26px;color:#38bdf8;font-family:Segoe UI,Arial,sans-serif;font-weight:bold;'>"
            "Scores by Subject for Selected Students</span>"
        )

    line_fig.update_layout(
        title={
            'text': line_title,
            'x': 0.5,
            'y': 0.92,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(size=26, color='#38bdf8', family='Segoe UI, Arial, sans-serif')
        },
        plot_bgcolor='#f0f9ff',
        paper_bgcolor='#f0f9ff',
        margin=dict(l=30, r=30, t=120, b=50),
        height=420,
        legend=dict(
            title='Student',
            orientation='h',
            yanchor='bottom',
            y=1.08,
            xanchor='center',
            x=0.5,
            font=dict(size=17, color='#334155')
        ),
        xaxis=dict(
            title='Subject',
            title_font=dict(size=18, color='#334155'),
            tickfont=dict(size=16, color='#334155'),
            showgrid=True,
            gridcolor='#e0e7ef'
        ),
        yaxis=dict(
            title='Score',
            title_font=dict(size=18, color='#334155'),
            tickfont=dict(size=16, color='#334155'),
            showgrid=True,
            gridcolor='#e0e7ef'
        )
    )

    # Bar plot: Average per subject (always show for all students)
    avg_bar = px.bar(
        subject_avg, x='Subject', y='Average',
        text_auto='.2f',
        title="Average Score per Subject (All Students)",
        template='plotly_white',
        color_discrete_sequence=px.colors.sequential.Teal
    )
    avg_bar.update_layout(
        title_font=dict(size=22, color='#0f766e', family='Segoe UI, Arial, sans-serif'),
        plot_bgcolor='#f3f4f6',
        paper_bgcolor='#f3f4f6',
        margin=dict(l=20, r=20, t=60, b=40),
        height=350,
        showlegend=False,
        xaxis=dict(title_font=dict(size=16, color='#334155'), tickfont=dict(size=15, color='#334155')),
        yaxis=dict(title_font=dict(size=16, color='#334155'), tickfont=dict(size=15, color='#334155'))
    )
    avg_bar.update_traces(marker=dict(line=dict(width=1, color='#0f766e'), opacity=0.88))

    # Insights
    insight = html.Div([
        html.H4("📈 Dashboard Insights", style={
            'color': '#6366f1',
            'marginBottom': '18px',
            'fontWeight': 'bold',
            'fontSize': '22px',
            'letterSpacing': '1px'
        }),
        html.P(
            "🏅 Charlie achieved the highest overall average score among all students, demonstrating exceptional performance across all subjects.",
            style={'marginBottom': '14px', 'fontSize': '17px'}
        ),
        html.P(
            "📚 Science emerged as the subject with the highest average score, indicating strong proficiency and interest among the students in this area.",
            style={'marginBottom': '14px', 'fontSize': '17px'}
        ),
        html.P(
            "💡 Users can interact with the dashboard by selecting a student to view their performance across subjects or by using the dropdown menu to filter and compare student results.",
            style={ 'marginBottom': '14px', 'fontSize': '17px'}
        )
    ], style={'lineHeight': '1.8'})
    return bar_fig, line_fig, avg_bar, insight

if __name__ == '__main__':
    try:
        print("Dash dashboard running at http://127.0.0.1:8050")
        app.run(debug=True)
    except Exception as e:
        print("dashboard error:", e)