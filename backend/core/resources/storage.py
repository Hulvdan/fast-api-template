from typing import Any, Union

from aioboto3 import Session


class StorageResource:
    def __init__(
        self,
        *,
        s3_endpoint_url: str,
        s3_storage_bucket_name: str,
        s3_access_key_id: str,
        s3_secret_access_key: str,
    ):
        self._service_name: str = "s3"
        self._endpoint_url = s3_endpoint_url
        self._bucket = s3_storage_bucket_name
        self._aws_access_key_id = s3_access_key_id
        self._aws_secret_access_key = s3_secret_access_key

        self._session_options: dict[str, Any] = dict(
            aws_access_key_id=self._aws_access_key_id,
            aws_secret_access_key=self._aws_secret_access_key,
        )
        self._client_options: dict[str, Any] = dict(
            service_name=self._service_name,
            endpoint_url=self._endpoint_url,
            aws_access_key_id=self._aws_access_key_id,
            aws_secret_access_key=self._aws_secret_access_key,
        )
        self._resource_options: dict[str, Any] = dict(
            service_name=self._service_name,
            endpoint_url=self._endpoint_url,
            aws_access_key_id=self._aws_access_key_id,
            aws_secret_access_key=self._aws_secret_access_key,
        )

        self._session = Session(**self._session_options)

    async def upload_file(self, file: Any, source: str) -> Union[str, None]:
        await file.seek(0)
        async with self._session.client(**self._client_options) as storage_bucket:
            await storage_bucket.upload_fileobj(file, self._bucket, source)
        return source

    async def delete_file(self, source: str) -> Union[str, None]:
        prefix: str = "/".join(source.split("/")[:-1])
        async with self._session.resource(**self._resource_options) as storage_bucket:
            bucket = await storage_bucket.Bucket(self._bucket)
            async for obj in bucket.objects.filter(Prefix=prefix):
                if obj.key == source:
                    await obj.delete()
        return source
