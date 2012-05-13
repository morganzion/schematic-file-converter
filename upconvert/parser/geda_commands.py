class GEDAColor:
    """ Enumeration of gEDA colors """
    BACKGROUND_COLOR = 0
    PIN_COLOR = 1
    NET_ENDPOINT_COLOR = 2
    GRAPHIC_COLOR = 3
    NET_COLOR = 4
    ATTRIBUTE_COLOR = 5
    LOGIC_BUBBLE_COLOR = 6
    DOTS_GRID_COLOR = 7
    DETACHED_ATTRIBUTE_COLOR = 8
    TEXT_COLOR = 9
    BUS_COLOR = 10
    SELECT_COLOR = 11
    BOUNDINGBOX_COLOR = 12
    ZOOM_BOX_COLOR = 13
    STROKE_COLOR = 14
    LOCK_COLOR = 15


class GEDAParameter(object):
    TYPE = ''

    def __init__(self, name, datatype=int, default=None):
        self._name = name
        self.datatype = datatype
        self.default = default

    @property
    def name(self):
        return self._name


class GEDAStyleParameter(GEDAParameter):
    TYPE = 'style'

    @property
    def name(self):
        return "%s_%s" % (self.TYPE, self._name)


class GEDACommand(object):
    TYPE = None
    PARAMETERS = ()

    @classmethod
    def get_style_keywords(cls):
        return [p.name for p in cls.PARAMETERS]

    @classmethod
    def update_default_kwargs(cls, **kwargs):
        default_kwargs = {}
        for parameter in cls.PARAMETERS:
            default_kwargs[parameter.name] = parameter.default
        default_kwargs.update(kwargs)
        return default_kwargs

    @classmethod
    def generate_command(cls, **kwargs):
        kwargs = cls.update_default_kwargs(**kwargs)
        command = [cls.TYPE]
        for parameter in cls.PARAMETERS:
            command.append("%%(%s)s" % parameter.name)
        return [" ".join(command) % kwargs]


class GEDALineCommand(GEDACommand):
    TYPE = 'L'
    PARAMETERS = (
        GEDAParameter('x1'),
        GEDAParameter('y1'),
        GEDAParameter('x2'),
        GEDAParameter('y2'),
        GEDAStyleParameter('color', default=GEDAColor.GRAPHIC_COLOR),
        GEDAStyleParameter('width', default=10),
        GEDAStyleParameter('capstyle', default=0),
        GEDAStyleParameter('dashstyle', default=0),
        GEDAStyleParameter('dashlength', default=-1),
        GEDAStyleParameter('dashspace', default=-1),
    )


class GEDABoxCommand(GEDACommand):
    TYPE = "B"
    PARAMETERS = (
        GEDAParameter('x'),
        GEDAParameter('y'),
        GEDAParameter('width'),
        GEDAParameter('height'),
        GEDAStyleParameter('color', default=GEDAColor.GRAPHIC_COLOR),
        GEDAStyleParameter('width', default=10),
        GEDAStyleParameter('capstyle', default=0),
        GEDAStyleParameter('dashstyle', default=0),
        GEDAStyleParameter('dashlength', default=-1),
        GEDAStyleParameter('dashspace', default=-1),
        GEDAStyleParameter('filltype', default=0),
        GEDAStyleParameter('fillwidth', default=-1),
        GEDAStyleParameter('angle1', default=-1),
        GEDAStyleParameter('pitch1', default=-1),
        GEDAStyleParameter('angle2', default=-1),
        GEDAStyleParameter('pitch2', default=-1),
    )


class GEDACircleCommand(GEDACommand):
    TYPE = 'V'
    PARAMETERS = (
        GEDAParameter('x'),
        GEDAParameter('y'),
        GEDAParameter('radius'),
        GEDAStyleParameter('color', default=GEDAColor.GRAPHIC_COLOR),
        GEDAStyleParameter('width', default=10),
        GEDAStyleParameter('capstyle', default=0),
        GEDAStyleParameter('dashstyle', default=0),
        GEDAStyleParameter('dashlength', default=-1),
        GEDAStyleParameter('dashspace', default=-1),
        GEDAStyleParameter('filltype', default=0),
        GEDAStyleParameter('fillwidth', default=-1),
        GEDAStyleParameter('angle1', default=-1),
        GEDAStyleParameter('pitch1', default=-1),
        GEDAStyleParameter('angle2', default=-1),
        GEDAStyleParameter('pitch2', default=-1),
    )


class GEDAArcCommand(GEDACommand):
    TYPE = 'A'
    PARAMETERS = (
        GEDAParameter('x'),
        GEDAParameter('y'),
        GEDAParameter('radius'),
        GEDAParameter('startangle'),
        GEDAParameter('sweepangle'),
        GEDAStyleParameter('color', default=GEDAColor.GRAPHIC_COLOR),
        GEDAStyleParameter('width', default=10),
        GEDAStyleParameter('capstyle', default=0),
        GEDAStyleParameter('dashstyle', default=0),
        GEDAStyleParameter('dashlength', default=-1),
        GEDAStyleParameter('dashspace', default=-1),
    )


class GEDATextCommand(GEDACommand):
    TYPE = 'T'
    PARAMETERS = (
        GEDAParameter('x'),
        GEDAParameter('y'),
        GEDAStyleParameter('color', default=GEDAColor.TEXT_COLOR),
        GEDAStyleParameter('size', default=10),
        GEDAParameter('visibility', default=1),
        GEDAParameter('show_name_value', default=1),
        GEDAParameter('angle', default=0),
        GEDAParameter('alignment', default=0),
        GEDAParameter('num_lines', default=1),
    )


class GEDASegmentCommand(GEDACommand):
    TYPE = 'N'
    PARAMETERS = (
        GEDAParameter('x1'),
        GEDAParameter('y1'),
        GEDAParameter('x2'),
        GEDAParameter('y2'),
        GEDAStyleParameter('color', default=GEDAColor.NET_COLOR),
    )


class GEDAPinCommand(GEDACommand):
    TYPE = 'P'
    PARAMETERS = (
        GEDAParameter('x1'),
        GEDAParameter('y1'),
        GEDAParameter('x2'),
        GEDAParameter('y2'),
        GEDAStyleParameter('color', default=GEDAColor.PIN_COLOR),
        # pin type is always 0
        GEDAStyleParameter('pintype', default=0),
        # first point is active/connected pin
        GEDAParameter('whichend', default=0),
    )


class GEDAComponentCommand(GEDACommand):
    TYPE = 'C'
    PARAMETERS = (
        GEDAParameter('x'),
        GEDAParameter('y'),
        GEDAParameter('selectable', default=0),
        GEDAParameter('angle'),
        GEDAParameter('mirror'),
        GEDAParameter('basename', datatype=str),
    )


class GEDAPathCommand(GEDACommand):
    TYPE = "H"
    PARAMETERS = (
        GEDAStyleParameter('color', default=GEDAColor.GRAPHIC_COLOR),
        GEDAStyleParameter('width', default=10),
        GEDAStyleParameter('capstyle', default=0),
        GEDAStyleParameter('dashstyle', default=0),
        GEDAStyleParameter('dashlength', default=-1),
        GEDAStyleParameter('dashspace', default=-1),
        GEDAStyleParameter('filltype', default=0),
        GEDAStyleParameter('fillwidth', default=-1),
        GEDAStyleParameter('angle1', default=-1),
        GEDAStyleParameter('pitch1', default=-1),
        GEDAStyleParameter('angle2', default=-1),
        GEDAStyleParameter('pitch2', default=-1),
        GEDAParameter('num_lines'),
    )


class GEDAVersionCommand(GEDACommand):
    TYPE = 'v'
    PARAMETERS = (
        GEDAParameter('version'),
        GEDAParameter('fileformat_version'),
    )


class GEDABusCommand(GEDACommand):
    TYPE = 'U'
    PARAMETERS = (
        GEDAParameter('x1'),
        GEDAParameter('y1'),
        GEDAParameter('x2'),
        GEDAParameter('y2'),
        GEDAStyleParameter('color', default=GEDAColor.BUS_COLOR),
        GEDAParameter('ripperdir', default=0),
    )


class GEDAPictureCommand(GEDACommand):
    TYPE = 'G'
    PARAMETERS = ()


class GEDAEmbeddedEnvironmentCommand(GEDACommand):
    TYPE = '['
    PARAMETERS = ()


class GEDAAttributeEnvironmentCommand(GEDACommand):
    TYPE = '{'
    PARAMETERS = ()


class GEDACommand(GEDACommand):
    TYPE = 'U'
    PARAMETERS = ()
