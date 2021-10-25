from typing import Any


class Storage:
    def __init__(self):
        self.service_name: str = "s3"
        self.endpoint_url: str = aws_config["endpoint_url"]
        self.bucket: str = aws_config["storage_bucket_name"]
        self.aws_access_key_id: str = aws_config["access_key_id"]
        self.aws_secret_access_key: str = aws_config["secret_access_key"]

        self.session_options: dict[str, Any] = dict(
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
        )
        self.client_options: dict[str, Any] = dict(
            service_name=self.service_name,
            endpoint_url=self.endpoint_url,
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
        )
        self.resource_options: dict[str, Any] = dict(
            service_name=self.service_name,
            endpoint_url=self.endpoint_url,
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
        )

        self.session: Session = Session(**self.session_options)

    async def upload_file(self, file: Any, source: str) -> Union[str, None]:
        await file.seek(0)
        async with self.session.client(**self.client_options) as s3:
            await s3.upload_fileobj(file, self.bucket, source)
        return source

    async def delete_file(self, source: str) -> Union[str, None]:
        prefix: str = "/".join(source.split("/")[:-1])
        async with self.session.resource(**self.resource_options) as s3:
            bucket = await s3.Bucket(self.bucket)
            async for obj in bucket.objects.filter(Prefix=prefix):
                if obj.key == source:
                    await obj.delete()
        return source
