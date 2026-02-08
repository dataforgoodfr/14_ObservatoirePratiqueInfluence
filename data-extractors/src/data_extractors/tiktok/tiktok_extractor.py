from data_extractors.data_extractor import DataExtractor
from extraction_task.extraction_task_config import (
    ExtractAccountTaskConfig,
    ExtractPostDetailsTaskConfig,
    ExtractPostListTaskConfig,
)
from extraction_task.extraction_task_result import (
    AccountExtractionResult,
    PostDetailsExtractionResult,
    PostListExtractionResult,
)


class TiktokExtractor(DataExtractor):
    def extract_account(
        self, task_config: ExtractAccountTaskConfig
    ) -> AccountExtractionResult:
        raise Exception("TiktokDataExtractor.extract_account not implemented yet")

    def extract_post_list(
        self, task_config: ExtractPostListTaskConfig
    ) -> PostListExtractionResult:
        raise Exception("TiktokDataExtractor.extract_post_list not implemented yet")

    def extract_post_details(
        self, task_config: ExtractPostDetailsTaskConfig
    ) -> PostDetailsExtractionResult:
        raise Exception("TiktokDataExtractor.extract_post_detail not implemented yet")
