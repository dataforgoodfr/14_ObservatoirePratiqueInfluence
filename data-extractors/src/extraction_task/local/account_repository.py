from typing import Self, cast
from pydantic import AwareDatetime, BaseModel
from extraction_task import social_network
from extraction_task.local import csv_repository


class Account(BaseModel):
    social_network: social_network.SocialNetwork
    account_id: str
    account_extraction_date: AwareDatetime
    description: str
    follower_count: int
    following_count: int
    post_count: int
    view_count: int
    like_count: int
    categories: list[str]

    @classmethod
    def from_csv_row(cls, csv_row: dict) -> Self:
        model_data = csv_row.copy()
        model_data["categories"] = model_data["categories"].split(",")
        return cast(Self, Account.model_validate(model_data))

    def to_csv_row(self) -> dict:
        row_data = self.model_dump()
        row_data["categories"] = ",".join(row_data["categories"])
        return row_data


class AccountRepository:
    _csv_repository: csv_repository.CsvRowRepository

    def __init__(self, csv_file: str):
        self._csv_repository = csv_repository.CsvRowRepository(
            csv_file, list(Account.model_fields.keys())
        )

    def upsertAccount(self, account: Account) -> None:
        def match_predicate(row: dict) -> bool:
            row_account = Account.from_csv_row(row)
            return (
                row_account.account_id == account.account_id
                and row_account.social_network == account.social_network
            )

        self._csv_repository._upsert_row(
            match_predicate,
            account.to_csv_row(),
        )
