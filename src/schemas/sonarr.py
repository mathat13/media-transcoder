from pydantic import BaseModel
from typing import List

class Image(BaseModel):
    coverType: str
    url: str
    remoteUrl: str


class OriginalLanguage(BaseModel):
    id: int
    name: str


class Series(BaseModel):
    id: int
    title: str
    titleSlug: str
    path: str
    tvdbId: int
    tvMazeId: int
    tmdbId: int
    imdbId: str
    type: str
    year: int
    genres: List[str]
    images: List[Image]
    tags: List
    originalLanguage: OriginalLanguage


class Episode(BaseModel):
    id: int
    episodeNumber: int
    seasonNumber: int
    title: str
    overview: str
    airDate: str
    airDateUtc: str
    seriesId: int
    tvdbId: int


class Language(BaseModel):
    id: int
    name: str


class SonarrMediaInfo(BaseModel):
    audioChannels: int
    audioCodec: str
    audioLanguages: List[str]
    height: int
    width: int
    subtitles: List
    videoCodec: str
    videoDynamicRange: str
    videoDynamicRangeType: str


class EpisodeFile(BaseModel):
    id: int
    relativePath: str
    path: str
    quality: str
    qualityVersion: int
    size: int
    dateAdded: str
    languages: List[Language]
    mediaInfo: SonarrMediaInfo
    sourcePath: str


class SonarrCustomFormatInfo(BaseModel):
    customFormats: List
    customFormatScore: int


class SonarrRelease(BaseModel):
    releaseType: str

class SonarrWebhookPayload(BaseModel):
    series: Series
    episodes: List[Episode]
    episodeFile: EpisodeFile
    isUpgrade: bool
    downloadClient: str
    downloadClientType: str
    downloadId: str
    customFormatInfo: SonarrCustomFormatInfo
    release: SonarrRelease
    eventType: str
    instanceName: str
    applicationUrl: str
