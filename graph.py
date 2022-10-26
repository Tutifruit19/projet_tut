import plotly.graph_objs as go
import numpy as np

Q_10_ARP = np.genfromtxt('/home/mpma/henona/Q_10_ARP.txt')
run_deterministe_ARP = np.genfromtxt('/home/mpma/henona/run_determiste_ARP.txt')
Q_90_ARP = np.genfromtxt('/home/mpma/henona/Q_10_ARP.txt')
Q_10_ARO = np.genfromtxt('/home/mpma/henona/Q_10_ARO.txt')
run_deterministe_ARO = np.genfromtxt('/home/mpma/henona/run_determiste_ARO.txt')
Q_90_ARO = np.genfromtxt('/home/mpma/henona/Q_90_ARO.txt')

fig = go.Figure([
    go.Scatter(
        name='run deterministe',
        x=list_timerun_aro,
        y=run_deterministe_ARO,
        mode='lines',
        line=dict(color='rgb(31, 119, 180)'),
    ),
    go.Scatter(
        name='Q 90',
        x=list_timerun_aro,
        y=Q_90_ARO,
        mode='lines',
        marker=dict(color="#444"),
        line=dict(width=0),
        showlegend=False
    ),
    go.Scatter(
        name='Q_10',
        x=list_timerun_aro,
        y=Q_10_ARO,
        marker=dict(color="#444"),
        line=dict(width=0),
        mode='lines',
        fillcolor='rgba(68, 68, 68, 0.3)',
        fill='tonexty',
        showlegend=False
    )
])
fig.update_layout(
    yaxis_title='temperature en Kelvin',
    title='Evolution des runs AROME',
    hovermode="x"
)
fig.show()
fig.write_html('/home/mpma/henona/graph_test.html')
