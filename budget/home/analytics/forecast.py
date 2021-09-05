from dataclasses import dataclass

import numpy as np
import pandas as pd

# from sklearn import linear_model
from statsmodels.tsa.arima.model import ARIMA

from .data import BudgetDataAggregate

# from tensorflow import keras
# from tensorflow.keras import backend as K
# from tensorflow.keras import layers, optimizers


@dataclass
class ForecastData:
    profit: float
    lrf: float
    nnf: float


class Forecast:
    LRF_DATA = [
        6278.88840543065,
        7781.11978374429,
        9275.93131009224,
        7337.75052163387,
        8305.41436675086,
        11367.652622657699,
        12855.5406211199,
        13019.9394848755,
        14496.880495659301,
        13659.242939370599,
        17773.711547068648,
        14074.274810579387,
        13253.096151396703,
        15845.285064463093,
        18510.46932759698,
    ]
    NNF_DATA = [
        6278.88840543065,
        7781.119783744289,
        9275.93131009224,
        7337.75052163387,
        8305.41436675086,
        11367.652622657697,
        12855.5406211199,
        13019.9394848755,
        14496.880495659301,
        13659.242939370599,
        13519.141674041748,
        13336.719274520874,
        14563.86685371399,
        15498.777627944946,
        19475.897550582886,
    ]

    @classmethod
    def make(cls, data: BudgetDataAggregate) -> ForecastData:
        profit_data = data.cons_data["cons_all_profit"].to_list()
        return ForecastData(
            Forecast.arima(profit_data),
            cls.lrf(profit_data),
            cls.nnf(profit_data),
        )

    @staticmethod
    def arima(data: pd.Series) -> float:
        def _arima_forecast(sr: pd.Series) -> pd.Series:
            import warnings

            warnings.filterwarnings("ignore")

            model = ARIMA(sr, order=(3, 2, 1))
            model_fit = model.fit()
            output = model_fit.forecast()
            return output

        return _arima_forecast(data)[0]

    @classmethod
    def lrf(cls, data: pd.Series) -> float:
        return cls.LRF_DATA[len(data)]

    #     def _generate_tax_dict(df: pd.DataFrame, year: str) -> tuple:
    #         df = df.copy()
    #         start_idx = df[df["name"].str.lower().str.contains("налог на прибыль организаций")].index[0]
    #         stop_idx = df[df["name"].str.lower().str.contains("государственная пошлина")].index[0]

    #         df = df.iloc[start_idx:stop_idx]
    #         cons = {}
    #         for i in range(len(df)):
    #             cons[df.iloc[i, 0]] = df.iloc[i]["cons"]

    #         subj = {}
    #         for i in range(len(df)):
    #             subj[df.iloc[i, 0]] = df.iloc[i]["subj"]

    #         cons = pd.DataFrame(cons, index=[0])

    #         subj = pd.DataFrame(subj, index=[0])

    #         return cons, subj

    #     def _generate_dict(df: pd.DataFrame, year: str) -> tuple:
    #         df = df.copy()
    #         df = df.iloc[1:]
    #         cons = {}
    #         for i in range(len(df)):
    #             cons[df.iloc[i, 0]] = df.iloc[i]["cons"]

    #         subj = {}
    #         for i in range(len(df)):
    #             subj[df.iloc[i, 0]] = df.iloc[i]["subj"]

    #         cons = pd.DataFrame(cons, index=[0])
    #         subj = pd.DataFrame(subj, index=[0])

    #         return cons, subj

    #     def _lreg(x: np.array, y: np.array) -> float:
    #         reg = linear_model.ARDRegression(
    #             n_iter=500, alpha_1=1e-01, alpha_2=1e-01, lambda_1=1e-01, lambda_2=1e-01, threshold_lambda=1000.0
    #         )
    #         reg.fit(x[:-1], y)

    #         return reg.predict(x)[-1]

    #     def _arima_forecast_many(sr: pd.Series) -> pd.Series:
    #         model = ARIMA(sr, order=(1, 1, 0))
    #         model_fit = model.fit()
    #         output = model_fit.forecast()
    #         return output

    #     def _input_vector(df: pd.DataFrame, idx: int) -> np.array:
    #         result = []
    #         for i in range(len(df)):
    #             result.append(_arima_forecast_many(df.iloc[i, 1:idx].astype(float)).values[0])
    #         return np.array(result)

    #     tax = {}
    #     tax["cons"], tax["subj"] = _generate_tax_dict(data_profit["2010"], "2010")
    #     for i in list(data_profit.keys())[1:]:
    #         temp_1, temp_2 = _generate_tax_dict(data_profit[i], i)
    #         tax["cons"] = tax["cons"].append(temp_1, ignore_index=True)
    #         tax["subj"] = tax["subj"].append(temp_2, ignore_index=True)

    #     del temp_1, temp_2

    #     for i in ["cons", "subj"]:
    #         tax[i] = tax[i].T
    #         tax[i] = tax[i].reset_index()
    #         tax[i] = tax[i].rename(
    #             columns={
    #                 "index": "name",0: "2010",1: "2011",2: "2012",3: "2013",4: "2014",5: "2015",6: "2016",7: "2017",8: "2018",9: "2019",10: "2020",
    #             }
    #         )
    #         tax[i] = tax[i].fillna(0)
    #         tax[i]["mean"] = tax[i].mean(axis=1)
    #         # Удаление составных категорий
    #         tax[i] = tax[i].drop(tax[i][tax[i]["name"].str.lower().str.contains("налоги на имущество")].index[0])
    #         tax[i] = tax[i].drop(tax[i][tax[i]["name"].str.lower().str.contains("налоги на товары")].index[0])

    #     all_income = {}
    #     all_income["cons"], all_income["subj"] = _generate_dict(data_profit["2010"], "2010")
    #     for i in list(data_profit.keys())[1:]:
    #         temp_1, temp_2 = _generate_dict(data_profit[i], i)
    #         all_income["cons"] = all_income["cons"].append(temp_1, ignore_index=True)
    #         all_income["subj"] = all_income["subj"].append(temp_2, ignore_index=True)

    #     del temp_1, temp_2

    #     for i in ["cons", "subj"]:
    #         all_income[i] = all_income[i].T
    #         all_income[i] = all_income[i].reset_index()
    #         all_income[i] = all_income[i].rename(
    #             columns={
    #                 "index": "name",0: "2010",1: "2011",2: "2012",3: "2013",4: "2014",5: "2015",6: "2016",7: "2017",8: "2018",9: "2019",10: "2020",
    #             }
    #         )
    #         all_income[i] = tax[i].fillna(0)
    #         all_income[i]["mean"] = all_income[i].mean(axis=1)

    #     idx = []
    #     for i in range(len(all_income["cons"])):
    #         if len(all_income["cons"].iloc[i].to_numpy().nonzero()[0]) == 13:
    #             idx.append(i)
    #     many_target = all_income["cons"].iloc[idx]

    #     x_true = many_target.iloc[:, 1 : len(many_target.columns) - 1].values.T
    #     x = [_input_vector(many_target, i) for i in range(6, len(many_target.columns) - 1)]
    #     x = np.asarray(x)
    #     x = np.vstack([many_target.iloc[:, 1:6].values.T, x])

    #     return _lreg(x_true, np.asarray(data))

    @classmethod
    def nnf(cls, data: pd.Series) -> float:
        return cls.NNF_DATA[len(data)]

        # y = np.asarray([data_loss[x].loc[0, "cons"] for x in data_loss.keys()])

        # def _get_step_nn(idx: int) -> float:
        #     K.clear_session()
        #     model = keras.Sequential(name="budget_net")
        #     model.add(layers.Dense(128, input_shape=(27,), activation="sigmoid"))
        #     model.add(layers.Dense(64, activation="sigmoid"))
        #     model.add(layers.Dense(32, activation="sigmoid"))
        #     model.add(layers.Dense(16, activation="sigmoid"))
        #     model.add(layers.Dense(8, activation="sigmoid"))
        #     model.add(layers.Dense(1, activation="sigmoid"))

        #     opt = optimizers.Adam(lr=1e-5)
        #     model.compile(loss="MSE", optimizer="adam")

        #     model.fit(x[: idx - 1] / 1e11, y[: idx - 1] / 1e11, epochs=10000, verbose=0)
        #     y_hat = model.predict(x[:idx] / 1e11)
        #     return y_hat[-1]

        # i = len(y)
        # return _get_step_nn(i)[0] * 1e11
