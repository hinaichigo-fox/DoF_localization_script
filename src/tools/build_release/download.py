from pathlib import Path
from aiofiles import open as aopen
import httpx


async def chunk_split(filesize: int, chunk: int = 2) -> list[list[int]]:
    """给大文件切片"""
    step = filesize // chunk
    arr = range(0, filesize, step)
    result = [[arr[i], arr[i + 1] - 1] for i in range(len(arr) - 1)]
    result[-1][-1] = filesize - 1
    return result


async def chunk_download(
    url: str,
    client: httpx.AsyncClient,
    start: int,
    end: int,
    save_path: Path,
    headers_: dict = None,
):
    """切片下载"""
    if not save_path.exists():
        with open(save_path, "wb") as fp:
            pass
    headers = (
        {"Range": f"bytes={start}-{end}"} | headers_
        if headers_
        else {"Range": f"bytes={start}-{end}"}
    )
    response = await client.get(url, headers=headers, follow_redirects=True, timeout=60)
    async with aopen(save_path, "rb+") as fp:
        await fp.seek(start)
        await fp.write(response.content)


__all__ = ["chunk_split", "chunk_download"]
