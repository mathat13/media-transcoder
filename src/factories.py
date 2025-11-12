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

# ---------- Nested Factories ----------

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

# ---------- Root Webhook Factory ----------

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

# ---------- Nested Factories ----------

class ImageFactory(factory.Factory):
    class Meta:
        model = Image

    coverType = factory.LazyFunction(lambda: fake.random_element(["poster", "banner", "fanart"]))
    url = factory.LazyFunction(lambda: fake.image_url())
    remoteUrl = factory.LazyFunction(lambda: fake.image_url())


class OriginalLanguageFactory(factory.Factory):
    class Meta:
        model = OriginalLanguage

    id = factory.LazyFunction(lambda: fake.random_int(1, 9999))
    name = factory.LazyFunction(lambda: fake.language_name())


class SeriesFactory(factory.Factory):
    class Meta:
        model = Series

    id = factory.LazyFunction(lambda: fake.random_int(1, 9999))
    title = factory.LazyFunction(lambda: fake.sentence(nb_words=3))
    titleSlug = factory.LazyAttribute(lambda o: o.title.lower().replace(" ", "-"))
    path = factory.LazyFunction(lambda: fake.file_path(depth=3))
    tvdbId = factory.LazyFunction(lambda: fake.random_int(1, 999999))
    tvMazeId = factory.LazyFunction(lambda: fake.random_int(1, 999999))
    tmdbId = factory.LazyFunction(lambda: fake.random_int(1, 999999))
    imdbId = factory.LazyFunction(lambda: f"tt{fake.random_int(10000000, 99999999)}")
    type = "series"
    year = factory.LazyFunction(lambda: int(fake.year()))
    genres = factory.LazyFunction(lambda: fake.words(nb=3))
    images = factory.List([factory.SubFactory(ImageFactory)])
    tags = factory.LazyFunction(lambda: [])
    originalLanguage = factory.SubFactory(OriginalLanguageFactory)


class EpisodeFactory(factory.Factory):
    class Meta:
        model = Episode

    id = factory.LazyFunction(lambda: fake.random_int(1, 99999))
    episodeNumber = factory.LazyFunction(lambda: fake.random_int(1, 24))
    seasonNumber = factory.LazyFunction(lambda: fake.random_int(1, 10))
    title = factory.LazyFunction(lambda: fake.sentence(nb_words=4))
    overview = factory.LazyFunction(lambda: fake.paragraph())
    airDate = factory.LazyFunction(lambda: fake.date())
    airDateUtc = factory.LazyFunction(lambda: fake.iso8601())
    seriesId = factory.LazyFunction(lambda: fake.random_int(1, 99999))
    tvdbId = factory.LazyFunction(lambda: fake.random_int(1, 99999))


class LanguageFactory(factory.Factory):
    class Meta:
        model = Language

    id = factory.LazyFunction(lambda: fake.random_int(1, 99999))
    name = factory.LazyFunction(lambda: fake.language_name())


class SonarrMediaInfoFactory(factory.Factory):
    class Meta:
        model = SonarrMediaInfo

    audioChannels = factory.LazyFunction(lambda: fake.random_int(2, 8))
    audioCodec = factory.LazyFunction(lambda: fake.random_element(["AAC", "AC3", "DTS"]))
    audioLanguages = factory.LazyFunction(lambda: ["eng"])
    height = factory.LazyFunction(lambda: fake.random_element([720, 1080, 2160]))
    width = factory.LazyFunction(lambda: fake.random_element([1280, 1920, 3840]))
    subtitles = factory.LazyFunction(lambda: [])
    videoCodec = factory.LazyFunction(lambda: fake.random_element(["h264", "h265"]))
    videoDynamicRange = factory.LazyFunction(lambda: fake.random_element(["", "HDR"]))
    videoDynamicRangeType = factory.LazyFunction(lambda: fake.random_element(["", "PQ"]))


class EpisodeFileFactory(factory.Factory):
    class Meta:
        model = EpisodeFile

    id = factory.LazyFunction(lambda: fake.random_int(1, 99999))
    relativePath = factory.LazyFunction(lambda: fake.file_name(extension="mkv"))
    path = factory.LazyFunction(lambda: fake.file_path(depth=4))
    quality = factory.LazyFunction(lambda: fake.random_element(["WEBRip-1080p", "Bluray-2160p"]))
    qualityVersion = 1
    size = factory.LazyFunction(lambda: fake.random_int(1_000_000_000, 8_000_000_000))
    dateAdded = factory.LazyFunction(lambda: fake.iso8601())
    languages = factory.List([factory.SubFactory(LanguageFactory)])
    mediaInfo = factory.SubFactory(SonarrMediaInfoFactory)
    sourcePath = factory.LazyFunction(lambda: fake.file_path(depth=4))


class SonarrCustomFormatInfoFactory(factory.Factory):
    class Meta:
        model = SonarrCustomFormatInfo

    customFormats = factory.LazyFunction(lambda: [])
    customFormatScore = 0


class SonarrReleaseFactory(factory.Factory):
    class Meta:
        model = SonarrRelease

    releaseType = factory.LazyFunction(lambda: fake.random_element(["torrent", "usenet"]))


# ---------- Root Payload ----------
class SonarrWebhookPayloadFactory(factory.Factory):
    class Meta:
        model = SonarrWebhookPayload

    series = factory.SubFactory(SeriesFactory)
    episodes = factory.List([factory.SubFactory(EpisodeFactory)])
    episodeFile = factory.SubFactory(EpisodeFileFactory)
    isUpgrade = False
    downloadClient = factory.LazyFunction(lambda: fake.random_element(["qBittorrent", "NZBGet"]))
    downloadClientType = factory.LazyFunction(lambda: fake.random_element(["qBittorrent", "NZBGet"]))
    downloadId = factory.LazyFunction(lambda: fake.uuid4())
    customFormatInfo = factory.SubFactory(SonarrCustomFormatInfoFactory)
    release = factory.SubFactory(SonarrReleaseFactory)
    eventType = "Download"
    instanceName = "Sonarr"
    applicationUrl = "http://localhost:8989"