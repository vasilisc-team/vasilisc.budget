from .data import BudgetDataAggregate
from .forecast import Forecast, ForecastData
from .ploting import PlotData, Plotter


class Analitic:
    def __init__(self) -> None:
        self._data_gen = BudgetDataAggregate.get()
        self.data = None
        self.plot = None
        self._tick()

    def _forecast(self) -> ForecastData:
        return Forecast.make(self.data)

    def _plot(self) -> PlotData:
        return Plotter.plot(self.data, self._forecast())

    def _tick(self) -> None:
        self.data = next(self._data_gen)
        self.plot = self._plot()

    def on_click(self):
        self._tick()
