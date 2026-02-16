import argparse
import datetime
import logging
from os import path

from dotenv import load_dotenv

from run_extract import ExtractConfig, run_extract

from extraction_task.social_network import SocialNetwork

from run_generate_task import GenerateTaskConfig, run_generate_task

from run_upload_to_noco import UploadToNocoConfig, run_upload_to_noco


def parse_date(date_str: str) -> datetime.datetime:
    return datetime.datetime.strptime(date_str, "%Y-%m-%d").replace(
        tzinfo=datetime.timezone.utc
    )


def main() -> None:
    load_dotenv()
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
        ],
    )

    parser = argparse.ArgumentParser(
        prog="data_extractors",
        description="Social network data extraction tool",
    )

    subparsers = parser.add_subparsers(dest="action", help="Available actions")

    # Add extract subcommand
    extract_parser = subparsers.add_parser(
        "extract", help="Extract data from social networks"
    )
    # Add extract arguments to the subparser
    extract_parser.add_argument(
        "-n",
        "--social-network",
        help="Social Network",
        type=SocialNetwork,
        dest="social_network",
        choices=list(SocialNetwork),
        default=SocialNetwork.YOUTUBE,
    )
    extract_parser.add_argument(
        "-p",
        "--polling-interval",
        dest="task_polling_interval",
        help="Task polling interval seconds",
        type=int,
        default=10,
    )
    extract_parser.add_argument(
        "-i",
        "--tasks-file",
        dest="tasks_file",
        help="Task csv file",
        default=path.join("data", "extraction_tasks.csv"),
    )
    extract_parser.add_argument(
        "-o",
        "--result-folder",
        dest="result_folder",
        help="Result folder",
        default=path.join("data", "results"),
    )
    extract_parser.add_argument(
        "-c",
        "--cache-folder",
        dest="cache_folder",
        help="Cache folder",
        default=path.join("data", ".cache"),
    )

    # Add generate-task subcommand
    generate_task_parser = subparsers.add_parser(
        "generate-task", help="Generate extraction tasks from account URLs"
    )
    generate_task_parser.add_argument(
        "--task-type",
        choices=["all", "account", "post-list"],
        default="all",
        dest="task_type",
        help="Which task types to generate (default: all)",
    )
    generate_task_parser.add_argument(
        "--published-after",
        type=str,
        default="2025-01-01",
        dest="published_after",
        help="Start date for post list extraction in YYYY-MM-DD format (default: 2025-01-01)",
    )
    generate_task_parser.add_argument(
        "--published-before",
        type=str,
        default="2026-01-01",
        dest="published_before",
        help="End date for post list extraction in YYYY-MM-DD format (default: 2026-01-01)",
    )
    generate_task_parser.add_argument(
        "--mode",
        choices=["replace", "append"],
        default="replace",
        dest="mode",
        help="Whether to replace existing tasks or append to them (default: replace)",
    )
    generate_task_parser.add_argument(
        "--urls-file",
        type=str,
        default="data/account_urls.csv",
        dest="urls_file",
        help="Path to the input CSV file with account URLs (default: data/account_urls.csv)",
    )
    generate_task_parser.add_argument(
        "--tasks-file",
        type=str,
        default="data/extraction_tasks.csv",
        dest="tasks_file",
        help="Path to the output CSV file for extraction tasks (default: data/extraction_tasks.csv)",
    )

    # Add upload-results subcommand
    upload_parser = subparsers.add_parser(
        "upload-results", help="Upload results to NocoDB"
    )

    upload_parser.add_argument(
        "-r",
        "--result-folder",
        dest="result_folder",
        help="Result folder containing CSV files",
        default=path.join("data", "results"),
    )

    args = parser.parse_args()

    if args.action == "extract":
        extract_config = ExtractConfig(
            social_network=args.social_network,
            task_polling_interval=args.task_polling_interval,
            tasks_file=args.tasks_file,
            result_folder=args.result_folder,
            cache_folder=args.cache_folder,
        )
        run_extract(extract_config)
    elif args.action == "generate-task":
        published_after = parse_date(args.published_after)
        published_before = parse_date(args.published_before)
        replace = args.mode == "replace"
        generate_task_config = GenerateTaskConfig(
            task_type=args.task_type,
            published_after=published_after,
            published_before=published_before,
            replace=replace,
            urls_file=args.urls_file,
            tasks_file=args.tasks_file,
        )
        run_generate_task(generate_task_config)
    elif args.action == "upload-results":
        upload_config = UploadToNocoConfig(
            result_folder=args.result_folder,
            accounts_csv=path.join(args.result_folder, "accounts.csv"),
            posts_csv=path.join(args.result_folder, "posts.csv"),
        )
        run_upload_to_noco(upload_config)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
