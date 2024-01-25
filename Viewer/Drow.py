import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


class Drow():
    def __init__(self, Object):
        self.object = Object

    'Класс для отрисовки данных'

    def DrowFullCsvSpectr(self, df):
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df.index, y=df.r, name="r", line_color='red'))
        fig.add_trace(go.Scatter(x=df.index, y=df.g, name="g", line_color='green'))
        fig.add_trace(go.Scatter(x=df.index, y=df.b, name="b", line_color='blue'))
        fig.add_trace(go.Scatter(x=df.index, y=df.i, name="i", line_color='black'))
        fig.update_layout(
            title="Plot Title",
            xaxis_title="X Axis Title",
            yaxis_title="X Axis Title",
            legend_title="Legend Title",
            font=dict(
                family="Courier New, monospace",
                size=18,
                color="RebeccaPurple"
            )
        )
        fig.show()
        pass

    def DrowSpectr(self, df, name):
        fig = go.Figure()
        I = df.i / np.max(df.i)
        I = df.r+df.b+df.g
        I = I / np.max(I)
        nm = df.index * self.object.k + self.object.b
        if self.object.AddExample.value:
            example = f'{self.object.ChooseExample.value}'
            for df_tmp in self.object.df_list:
                if example in df_tmp.columns:
                    print(df_tmp)
                    yData = np.array(df_tmp[example]).astype(float)
                    xData = np.array(df_tmp['nm']).astype(float)
            yData = yData / np.max(yData)
            fig.add_trace(go.Scatter(x=nm, y=I,
                                     # mode='markers', marker={'color': nm[::-1], 'colorscale': 'Rainbow', 'size': 10},
                                     mode='lines',
                                     # fill = 'tozeroy',
                                     # fillcolor={'color': nm[::-1], 'colorscale': 'Rainbow', 'size': 10}

                                     # fillcolor=rainbow(10, s = 1, v = 1, start = 0, end = max(1, 10 - 1)/10, alpha = 1),#'green',
                                     # fillcolor='rainbow',

                                     # fillpattern=dict(fgcolor='red', fillmode='replace', shape="x")
                                     )
                          )  # ,name="r",line_color = 'red'))
            fig.add_trace(go.Scatter(x=xData, y=yData,
                                     name=example,
                                     # mode='markers', marker={'color': nm[::-1], 'colorscale': 'Rainbow', 'size': 10},
                                     mode='lines',
                                     # fill = 'tozeroy',
                                     # fillcolor={'color': nm[::-1], 'colorscale': 'Rainbow', 'size': 10}

                                     # fillcolor=rainbow(10, s = 1, v = 1, start = 0, end = max(1, 10 - 1)/10, alpha = 1),#'green',
                                     # fillcolor='rainbow',

                                     # fillpattern=dict(fgcolor='red', fillmode='replace', shape="x")
                                     )
                          )  # ,name="r",line_color = 'red'))
        else:
            fig.add_trace(go.Scatter(x=nm, y=I,
                                     # mode='markers', marker={'color': nm[::-1], 'colorscale': 'Rainbow', 'size': 10},
                                     mode='lines',
                                     # fill = 'tozeroy',
                                     # fillcolor={'color': nm[::-1], 'colorscale': 'Rainbow', 'size': 10}

                                     # fillcolor=rainbow(10, s = 1, v = 1, start = 0, end = max(1, 10 - 1)/10, alpha = 1),#'green',
                                     # fillcolor='rainbow',

                                     # fillpattern=dict(fgcolor='red', fillmode='replace', shape="x")
                                     )
                          )  # ,name="r",line_color = 'red'))
        fig.update_layout(
            title=name,
            xaxis_title="λ, нм",
            yaxis_title=" ",
            legend_title="Legend Title",
            font=dict(
                family="Courier New, monospace",
                size=18,
                color="RebeccaPurple"
            )

        )
        fig.show()

    def DrowSimplePlot(self):
        N = 100
        fig = go.Figure()
        x = np.linspace(0, 2 * np.pi, N)
        if self.object.ChooseFunction.value == 'Sin':
            y = np.sin(x) * float(self.object.InputA.value)
        elif self.object.ChooseFunction.value == 'Cos':
            y = np.cos(x) * float(self.object.InputA.value)
        else:
            raise ValueError('Функция не выбрана')
        fig.add_trace(go.Line(x=x, y=y))
        fig.show()
