from pathlib import Path
from typing import Dict, List

import pandas as pd


class BudgetData:
    MERGE_PROFIT = ["2012"]

    MERGE_CONSUMPTION_1 = ["2012", "2013", "2014"]
    MERGE_CONSUMPTION_2 = ["2015"]
    MERGE_CONSUMPTION_3 = ["2016", "2017", "2018", "2019", "2020"]

    def __init__(self, file_path: Path):
        self.year = file_path.stem
        self.profit = self._read_profit(file_path)
        self.consumption = self._read_consumption(file_path)

    @staticmethod
    def _merge(data: pd.DataFrame, idx: List[int]) -> pd.DataFrame:
        """
        Unite specified string's fields to one
        """
        data["code"] = ""
        for i in idx:
            data[data.columns[i]] = data[data.columns[i]].astype(str)
            data["code"] = data["code"] + data.iloc[:, i]
        data = data.drop(columns=data.columns[idx])
        return data

    @classmethod
    def _read_profit(cls, path: Path) -> pd.DataFrame:
        year = path.stem

        if year not in cls.MERGE_PROFIT:
            data_profit = pd.read_excel(
                path, sheet_name=f"доходы (исполнено) {year}", skiprows=1, names=["name", "code", "cons", "subj"]
            )
        else:
            data_profit = pd.read_excel(path, sheet_name=f"доходы (исполнено) {year}", skiprows=1)
            data_profit = BudgetData._merge(data_profit, [1, 2])
            data_profit = data_profit.rename(columns={1: "name", 16: "cons", 18: "subj"})
        data_profit = data_profit.dropna(subset=["name"])

        return data_profit

    @classmethod
    def _read_consumption(cls, path: Path) -> pd.DataFrame:
        year = path.stem
        if year in cls.MERGE_CONSUMPTION_1:
            data_consumption = pd.read_excel(path, sheet_name=f"расходы (исполнено) {year}", skiprows=1)
            data_consumption = BudgetData._merge(data_consumption, [1, 2, 3, 4])
            data_consumption = data_consumption.rename(columns={1: "name", 16: "cons", 18: "subj"})

        elif year in cls.MERGE_CONSUMPTION_2:
            data_consumption = pd.read_excel(path, sheet_name=f"расходы (исполнено) {year}", skiprows=1)
            data_consumption = BudgetData._merge(data_consumption, [1, 2, 3, 4, 5])
            data_consumption = data_consumption.rename(columns={1: "name", 16: "cons", 18: "subj"})

        elif year in cls.MERGE_CONSUMPTION_3:
            data_consumption = pd.read_excel(path, sheet_name=f"расходы (исполнено) {year}", skiprows=1)
            data_consumption = BudgetData._merge(data_consumption, [1, 2])
            data_consumption = data_consumption.rename(columns={1: "name", 16: "cons", 18: "subj"})

        else:
            data_consumption = pd.read_excel(
                path, sheet_name=f"расходы (исполнено) {year}", skiprows=1, names=["name", "code", "cons", "subj"]
            )
        data_consumption = data_consumption.dropna(subset=["name"])

        return data_consumption


class BudgetDataAggregate:
    DATA_DIR = Path(__file__).parent / "data"
    IDX = 5

    # def __init__(self, data_dir: str):
    #     self.budgets_data = BudgetDataAggregate._read_all_data(data_dir)
    #     self.cons_data = BudgetDataAggregate._get_clear_df(self.budgets_data)

    # @staticmethod
    # def _read_all_data(data_dir: str) -> Dict[str, BudgetData]:
    #     return {path.stem: BudgetData(path) for path in Path(data_dir).glob("*.xls*")}

    def __init__(self, init_data: Dict[str, BudgetData]):
        self.budgets_data = init_data
        self.cons_data = BudgetDataAggregate._get_clear_df(self.budgets_data)

    @classmethod
    def get(cls) -> "BudgetDataAggregate":
        files = list(Path(cls.DATA_DIR).glob("*.xls*"))

        while True:
            yield BudgetDataAggregate({path.stem: BudgetData(path) for path in files[: cls.IDX]})
            cls.IDX += 1
            if cls.IDX > 11:
                cls.IDX = 5

    @staticmethod
    def _get_clear_df(all_data: Dict[str, BudgetData]) -> pd.DataFrame:
        return pd.DataFrame(
            {
                "year": list(all_data.keys()),
                "cons_all_profit": [x.profit.loc[0, "cons"] for x in all_data.values()],
                "cons_all_loss": [x.consumption.loc[0, "cons"] for x in all_data.values()],
                "subj_all_profit": [x.profit.loc[0, "cons"] for x in all_data.values()],
                "subj_all_loss": [x.consumption.loc[0, "subj"] for x in all_data.values()],
                "cons_income_tax": [
                    x.profit[x.profit["name"].str.lower().str.contains("налоги на прибыль")]["cons"].values[0]
                    for x in all_data.values()
                ],
                "subj_income_tax": [
                    x.profit[x.profit["name"].str.lower().str.contains("налоги на прибыль")]["subj"].values[0]
                    for x in all_data.values()
                ],
                "cons_income_ndfl": [
                    x.profit[
                        x.profit["name"]
                        .str.lower()
                        .str.contains("налог на доходы физических лиц с доходов, полученных физическими лицами")
                    ]["subj"].values[0]
                    for x in all_data.values()
                ],
            }
        )
