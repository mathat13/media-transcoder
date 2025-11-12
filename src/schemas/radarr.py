from pydantic import BaseModel
from typing import List

class Movie(BaseModel):
    id: int
    title: str
    year: int
    releaseDate: str
    folderPath: str
    tmdbId: int
    imdbId: str
    overview: str
    tags: List

class RemoteMovie(BaseModel):
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
    subtitles: List
    videoCodec: str
    videoDynamicRange: str
    videoDynamicRangeType: str

class MovieFile(BaseModel):
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
    customFormats: List
    customFormatScore: int

class RadarrRelease(BaseModel):
    size: int

class RadarrWebhookPayload(BaseModel):
    movie: Movie
    remoteMovie: RemoteMovie
    movieFile: MovieFile
    isUpgrade: bool
    downloadClient: str
    downloadClientType: str
    downloadId: str
    customFormatInfo: RadarrCustomFormatInfo
    release: RadarrRelease
    eventType: str
    instanceName: str
    applicationUrl: str
