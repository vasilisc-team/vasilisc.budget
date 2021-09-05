import json
from dataclasses import dataclass

import numpy as np
import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from .data import BudgetDataAggregate
from .forecast import ForecastData


@dataclass
class PlotData:
    budget: str
    vat: str  # НДС
    pit: str  # НДФЛ
    forecast: str


class Plotter:
    @staticmethod
    def plot(data: BudgetDataAggregate, f_data: ForecastData) -> PlotData:
        return PlotData(
            Plotter.budget(data),
            Plotter.get_VAT(data),
            Plotter.get_PIT(data),
            Plotter.forecast(data, f_data),
        )

    @staticmethod
    def budget(data: BudgetDataAggregate) -> str:
        x_line = list(data.budgets_data)

        fig = make_subplots(rows=2, cols=1, subplot_titles=("Консолидированный бюджет", "Бюджет субъекта"))

        fig.add_trace(
            go.Scatter(
                x=x_line,  # линия x - у нас даты
                y=data.cons_data["cons_all_profit"],  # y - значения
                mode="lines",  # не трогай)
                name="Доходы",  # имя ряда - попадет в легенду
            ),
            row=1,  # положение в строках
            col=1,  # положение в столбцах
        )
        fig.add_trace(
            go.Scatter(
                x=x_line,
                y=data.cons_data["cons_all_loss"],
                mode="lines",
                name="Расходы",
            ),
            row=1,
            col=1,
        )
        fig.update_yaxes(title_text="10 млдр. руб")
        fig.update_xaxes(title_text="Год")

        fig.add_trace(
            go.Scatter(
                x=x_line,
                y=data.cons_data["subj_all_profit"],
                mode="lines",
                name="Доходы",
            ),
            row=2,
            col=1,
        )
        fig.add_trace(
            go.Scatter(
                x=x_line,
                y=data.cons_data["subj_all_loss"],
                mode="lines",
                name="Расходы",
            ),
            row=2,
            col=1,
        )

        fig.update_layout(title=go.layout.Title(text="Динамика бюджета", font=go.layout.title.Font(size=30)))

        return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    @staticmethod
    def get_VAT(data: BudgetDataAggregate) -> str:  # НДС
        x_line = list(data.budgets_data)

        fig = make_subplots(rows=1, cols=1, subplot_titles=("Налог на прибыль"))

        fig.add_trace(
            go.Bar(
                x=x_line,  # линия x - у нас даты
                y=data.cons_data["cons_income_tax"],  # y - значения
            ),
            row=1,  # положение в строках
            col=1,  # положение в столбцах
        )
        fig.update_yaxes(title_text="10 млдр. руб")
        fig.update_xaxes(title_text="Год")

        return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    @staticmethod
    def get_PIT(data: BudgetDataAggregate) -> str:  # НДФЛ
        fig = make_subplots(rows=1, cols=1, subplot_titles=("НДФЛ"))

        x_line = list(data.budgets_data)

        fig.add_trace(
            go.Bar(
                x=x_line,  # линия x - у нас даты
                y=data.cons_data["cons_income_ndfl"],  # y - значения
            ),
            row=1,  # положение в строках
            col=1,  # положение в столбцах
        )
        fig.update_yaxes(title_text="10 млдр. руб")
        fig.update_xaxes(title_text="Год")

        return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    @staticmethod
    def forecast(data: BudgetDataAggregate, f_data: ForecastData):
        x_line = list(data.budgets_data)
        x_line_f = x_line + [str(int(x_line[-1]) + 1)]
        y_line = data.cons_data["cons_all_profit"]

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=x_line,  # линия x - у нас даты
                y=y_line,  # y - значения
                mode="lines",  # не трогай)
                name="Отчет",  # имя ряда - попадет в легенду
            )
        )
        fig.add_trace(
            go.Scatter(
                x=x_line_f,
                y=y_line + [f_data.profit],
                mode="lines",
                name="Предсказание ARIMA",
            )
        )
        fig.add_trace(
            go.Scatter(
                x=x_line_f,
                y=y_line + [f_data.lrf],
                mode="lines",
                name="Предсказание многофакторной",
            )
        )
        fig.add_trace(
            go.Scatter(
                x=x_line_f,
                y=y_line + [f_data.nnf],
                mode="lines",
                name="Нейронная сеть",
            )
        )
        fig.update_layout(
            shapes=[
                dict(  # выделение региона с прогнозом
                    type="rect",
                    xref="x",
                    yref="paper",
                    x0=x_line[-1],  # левая граница
                    y0="0",
                    x1=x_line_f[-1],  # правая граница
                    y1="1",
                    fillcolor="LightSalmon",
                    opacity=0.4,
                    line_width=0,
                    layer="below",
                )
            ],
            title=go.layout.Title(text="Прогноз", font=go.layout.title.Font(size=30)),
        )
        fig.update_yaxes(title_text="10 млдр. руб")
        fig.update_xaxes(title_text="Год")
        return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
