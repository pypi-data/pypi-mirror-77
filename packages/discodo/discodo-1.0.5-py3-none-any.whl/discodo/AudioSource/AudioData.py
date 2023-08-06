import aiohttp

from ..extractor import clear_cache, extract
from .AudioSource import AudioSource


class AudioData:
    def __init__(self, data, planner=None, IPAddress=None):
        self.planner = planner
        self.IPAddress = IPAddress

        self.id = data.get("id")
        self.title = data.get("title")

        if data.get("_type") == "url" and data.get("ie_key") == "Youtube":
            self.webpage_url = f"https://www.youtube.com/watch?v={self.id}"
            self.thumbnail = f"https://i.ytimg.com/vi/{self.id}/hqdefault.jpg"
            self.stream_url = None
        else:
            self.webpage_url = data.get("webpage_url")
            self.thumbnail = data.get("thumbnail")
            self.stream_url = data.get("url")

        self.lyrics = (
            {
                lang: [
                    LyricsData["url"]
                    for LyricsData in lyrics
                    if LyricsData["ext"] == "srv1"
                ][0]
                for lang, lyrics in data["subtitles"].items()
            }
            if "subtitles" in data
            else {}
        )
        self.duration = data.get("duration")
        self.is_live = data.get("is_live", False)

        self.uploader = data.get("uploader")
        self.description = data.get("description")
        self.subtitles = data.get("subtitles")

        self.playlist = data.get("playlist")

        self._source = None

    @classmethod
    async def create(cls, query: str, planner=None):
        IPAddress = planner.get() if planner else None
        Data = await extract(query, IPAddress)

        if isinstance(Data, list):
            return [cls(Item) for Item in Data]

        return cls(Data, planner, IPAddress)

    async def gather(self):
        self.IPAddress = self.planner.get() if self.planner else None

        Data = await extract(self.webpage_url, self.planner)
        self.__init__(Data, self.planner, self.IPAddress)

        return self

    async def source(
        self, *args, _retry: int = 0, _limited=False, **kwargs
    ) -> AudioSource:
        if not self.stream_url or _limited:
            await self.gather()

        if not self._source:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.stream_url) as request:
                    Status = request.status

            if Status == 403:
                if _retry == 0:
                    return await self.source(*args, _retry=_retry + 1, **kwargs)
                elif _retry == 1:
                    await clear_cache()
                    return await self.source(*args, _retry=_retry + 1, **kwargs)
            if Status == 429 and self.planner:
                if self.IPAddress:
                    self.IPAddress.givePenalty()

                return await self.source(*args, _retry=_retry, _limited=True, **kwargs)

            self._source = AudioSource(self.stream_url, *args, AudioData=self, **kwargs)

        return self._source

    def toDict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "webpage_url": self.webpage_url,
            "thumbnail": self.thumbnail,
            "duration": self.duration,
            "is_live": self.is_live,
            "uploader": self.uploader,
            "description": self.description,
            "playlist": self.playlist,
        }

    @classmethod
    def fromDict(cls, Data):
        return cls(Data)
