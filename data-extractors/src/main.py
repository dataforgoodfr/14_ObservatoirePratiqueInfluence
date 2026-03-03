import logging

from pydantic_settings import BaseSettings, CliApp, CliSubCommand, SettingsConfigDict

from run_extract import ExtractSettings, run_extract
from run_generate_task import GenerateTaskSettings, run_generate_task
from run_upload_to_noco import UploadToNocoSettings, run_upload_to_noco


class DataExtractorsCli(BaseSettings):
    """CLI for social network data extraction tool."""

    model_config = SettingsConfigDict(
        # Read from CLI only at this level
        # CliSubCommand models are configured to read
        # from env to avoid sub-command prefix.
        cli_parse_args=True,
        cli_hide_none_type=False,
        cli_kebab_case=True,
        cli_avoid_json=True,
    )

    extract: CliSubCommand[ExtractSettings]
    generate_task: CliSubCommand[GenerateTaskSettings]
    upload_results: CliSubCommand[UploadToNocoSettings]

    def cli_cmd(self) -> None:
        if self.extract:
            run_extract(self.extract)
        elif self.generate_task:
            run_generate_task(self.generate_task)
        elif self.upload_results:
            run_upload_to_noco(self.upload_results)


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
        ],
    )

    CliApp.run(DataExtractorsCli)


if __name__ == "__main__":
    main()
