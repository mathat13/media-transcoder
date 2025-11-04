from typing import List
from pydantic import BaseModel


class RadarrMovie(BaseModel):
    id: int
    title: str
    year: int
    releaseDate: str
    folderPath: str
    tmdbId: int
    imdbId: str
    overview: str
    tags: List[str]

class RadarrRemoteMovie(BaseModel):
    tmdbId: int
    imdbId: str
    title: str
    year: int

class RadarrMediaInfo(BaseModel):
    audioChannels: float
    audioCodec: str
    audioLanguages: List[str]
    height: int
    width: int
    subtitles: List[str]
    videoCodec: str
    videoDynamicRange: str
    videoDynamicRangeType: str

class RadarrMovieFile(BaseModel):
    id: int
    relativePath: str
    path: str
    quality: str
    qualityVersion: int
    releaseGroup: str
    sceneName: str
    indexerFlags: str
    size: int
    dateAdded: str
    mediaInfo: RadarrMediaInfo

class RadarrCustomFormatInfo(BaseModel):
    customFormats: List[str]
    customFormatScore: int

class RadarrRelease(BaseModel):
    size: int

class RadarrWebhookPayload(BaseModel):
    movie: RadarrMovie
    remoteMovie: RadarrRemoteMovie
    movieFile: RadarrMovieFile
    isUpgrade: bool
    downloadClient: str
    downloadClientType: str
    downloadId: str
    customFormatInfo: RadarrCustomFormatInfo
    release: RadarrRelease
    eventType: str
    instanceName: str
    applicationUrl: str