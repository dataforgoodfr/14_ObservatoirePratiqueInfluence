from app.models import Account


async def get_accounts(
    account_handle: str,
) -> Account:
    return Account(
        handle=f"toto {account_handle}",
    )
