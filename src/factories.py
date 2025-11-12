import factory
from faker import Faker
from src.db import Job  # import your SQLAlchemy model
from src.schemas.radarr import (
    Movie,
    RemoteMovie,
    MovieFile,
    RadarrMediaInfo,
    RadarrCustomFormatInfo,
    RadarrRelease,
    RadarrWebhookPayload,
)

from src.schemas.sonarr import (
    Image,
    OriginalLanguage,
    Series,
    Episode,
    Language,
    EpisodeFile,
    SonarrMediaInfo,
    SonarrCustomFormatInfo,
    SonarrRelease,
    SonarrWebhookPayload
)

fake = Faker()

# Job factory

class JobFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Job
        sqlalchemy_session = None  # we will inject the test DB session
        sqlalchemy_session_persistence = "commit"

    path = factory.LazyFunction(lambda: fake.file_path(extension="mkv"))
    status = "pending"

# Radarr webhook payload factories

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
        model = MovieFile

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
        model = Movie

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
        model = RemoteMovie

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

# Sonarr webhook payload factories

class ImageFactory(factory.Factory):
    class Meta:
        model = Image

    coverType = "poster"
    url = factory.LazyFunction(lambda: fake.image_url())
    remoteurl = factory.LazyFunction(lambda: fake.image_url())

class OriginalLanguageFactory(factory.Factory):
    class Meta:
        model = OriginalLanguage

    id = factory.Sequence(lambda n: n + 1)
    name = factory.LazyFunction(lambda: fake.language_name())

class SeriesFactory(factory.Factory):
    class Meta:
        model = Series

    id = factory.Sequence(lambda n: n + 1)
    title = factory.LazyFunction(lambda: fake.sentence(nb_words=3))
    titleSlug = factory.LazyFunction(lambda: fake.slug())
    path = factory.LazyFunction(lambda: fake.file_path(depth=3))
    tvdbId = factory.LazyFunction(lambda: fake.random_int(min=10000, max=999999))
    imdbId = factory.LazyFunction(lambda: "tt" + str(fake.random_int(min=1000000, max=9999999)))
    overview = factory.LazyFunction(lambda: fake.text(max_nb_chars=200))
    images = [factory.SubFactory(ImageFactory) for _ in range(2)]
    originalLanguage = factory.SubFactory(OriginalLanguageFactory)

class EpisodeFactory(factory.Factory):
    class Meta:
        model = Episode

    id = factory.Sequence(lambda n: n + 1)
    seasonNumber = factory.LazyFunction(lambda: fake.random_int(min=1, max=10))
    episodeNumber = factory.LazyFunction(lambda: fake.random_int(min=1, max=24))
    title = factory.LazyFunction(lambda: fake.sentence(nb_words=3))
    overview = factory.LazyFunction(lambda: fake.text(max_nb_chars=200))
    airDate = factory.LazyFunction(lambda: fake.date())
    airDateUtc = factory.LazyFunction(lambda: fake.date())
    seriesId = factory.Sequence(lambda n: n + 1)
    tvdbId = factory.LazyFunction(lambda: fake.random_int(min=10000, max=999999))

class LanguageFactory(factory.Factory):
    class Meta:
        model = Language

    id = factory.Sequence(lambda n: n + 1)
    name = factory.LazyFunction(lambda: fake.language_name())

class SonarrMediaInfoFactory(factory.Factory):
    class Meta:
        model = SonarrMediaInfo

    audioChannels = 2
    audioCodec = "AAC"
    audioLanguages = ["eng"]
    height = 1080
    width = 1920
    subtitles = []
    videoCodec = "x264"
    videoDynamicRange = ""
    videoDynamicRangeType = ""

class EpisodeFileFactory(factory.Factory):
    class Meta:
        model = EpisodeFile

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
    mediaInfo = factory.SubFactory(SonarrMediaInfoFactory)

class SonarrCustomFormatFactory(factory.Factory):
    class Meta:
        model = SonarrCustomFormatInfo

    customFormats = []
    customFormatScore = 0

class SonarrReleaseFactory(factory.Factory):
    class Meta:
        model = SonarrRelease

    size = 0

class SonarrWebhookPayloadFactory(factory.Factory):
    class Meta:
        model = SonarrWebhookPayload

    series = factory.SubFactory(SeriesFactory)
    episode = factory.SubFactory(EpisodeFactory)
    episodeFile = factory.SubFactory(EpisodeFileFactory)
    isUpgrade = False
    downloadClient = "qBittorrent"
    downloadClientType = "qBittorrent"
    downloadId = factory.LazyFunction(lambda: fake.sha1())
    customFormatInfo = factory.SubFactory(SonarrCustomFormatFactory)
    release = factory.SubFactory(SonarrReleaseFactory)
    eventType = "Download"
    instanceName = "Sonarr"
    applicationUrl = ""