import factory
from faker import Faker
from src.db import Job  # import your SQLAlchemy model
from src.schemas.radarr import (
    RadarrMovie,
    RadarrRemoteMovie,
    RadarrMovieFile,
    RadarrMediaInfo,
    RadarrCustomFormatInfo,
    RadarrRelease,
    RadarrWebhookPayload,
)

fake = Faker()

class JobFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Job
        sqlalchemy_session = None  # we will inject the test DB session
        sqlalchemy_session_persistence = "commit"

    path = factory.LazyFunction(lambda: fake.file_path(extension="mkv"))
    status = "pending"


class RadarrMediaInfoFactory(factory.Factory):
    class Meta:
        model = RadarrMediaInfo

    audioChannels = 2.0
    audioCodec = "AAC"
    audioLanguages = ["eng"]
    height = 1080
    width = 1920
    subtitles = []
    videoCodec = "x264"
    videoDynamicRange = ""
    videoDynamicRangeType = ""

class RadarrMovieFileFactory(factory.Factory):
    class Meta:
        model = RadarrMovieFile

    id = factory.Sequence(lambda n: n + 1)
    relativePath = factory.LazyFunction(lambda: fake.file_name(extension="mkv"))
    path = factory.LazyFunction(lambda: fake.file_path(extension="mkv"))
    quality = "Bluray-1080p"
    qualityVersion = 1
    releaseGroup = "YIFY"
    sceneName = factory.LazyFunction(lambda: fake.sentence(nb_words=3))
    indexerFlags = "0"
    size = factory.LazyFunction(lambda: fake.random_int(min=700_000_000, max=5_000_000_000))
    dateAdded = factory.LazyFunction(lambda: fake.iso8601())
    mediaInfo = factory.SubFactory(RadarrMediaInfoFactory)

class RadarrMovieFactory(factory.Factory):
    class Meta:
        model = RadarrMovie

    id = factory.Sequence(lambda n: n + 1)
    title = factory.LazyFunction(lambda: fake.sentence(nb_words=3))
    year = factory.LazyFunction(lambda: fake.random_int(min=1980, max=2025))
    releaseDate = factory.LazyFunction(lambda: fake.date())
    folderPath = factory.LazyFunction(lambda: fake.file_path(depth=3))
    tmdbId = factory.LazyFunction(lambda: fake.random_int(min=1000, max=999999))
    imdbId = factory.LazyFunction(lambda: "tt" + str(fake.random_int(min=1000000, max=9999999)))
    overview = factory.LazyFunction(lambda: fake.text(max_nb_chars=200))
    tags = []

class RadarrRemoteMovieFactory(factory.Factory):
    class Meta:
        model = RadarrRemoteMovie

    tmdbId = factory.LazyFunction(lambda: fake.random_int(min=1000, max=999999))
    imdbId = factory.LazyFunction(lambda: "tt" + str(fake.random_int(min=1000000, max=9999999)))
    title = factory.LazyFunction(lambda: fake.sentence(nb_words=3))
    year = factory.LazyFunction(lambda: fake.random_int(min=1980, max=2025))


class RadarrCustomFormatFactory(factory.Factory):
    class Meta:
        model = RadarrCustomFormatInfo

    customFormats = []
    customFormatScore = 0


class RadarrReleaseFactory(factory.Factory):
    class Meta:
        model = RadarrRelease

    size = 0

class RadarrWebhookPayloadFactory(factory.Factory):
    class Meta:
        model = RadarrWebhookPayload

    movie = factory.SubFactory(RadarrMovieFactory)
    remoteMovie = factory.SubFactory(RadarrRemoteMovieFactory)
    movieFile = factory.SubFactory(RadarrMovieFileFactory)
    isUpgrade = False
    downloadClient = "qBittorrent"
    downloadClientType = "qBittorrent"
    downloadId = factory.LazyFunction(lambda: fake.sha1())
    customFormatInfo = factory.SubFactory(RadarrCustomFormatFactory)
    release = factory.SubFactory(RadarrReleaseFactory)
    eventType = "Download"
    instanceName = "Radarr"
    applicationUrl = ""