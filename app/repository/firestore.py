import os
from app.repository.fb import storageBucket, ROOT_DIR, store_client
from app.schemas.test_result import Metric


class MyFirestoreClient:
    def __init__(self) -> None:
        self.collection = "metadata"

    def update_metadata(self, metric: Metric):
        raise NotImplementedError()
