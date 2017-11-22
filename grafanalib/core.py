"""Low-level functions for building Grafana dashboards.

The functions in this module don't enforce Weaveworks policy, and only mildly
encourage it by way of some defaults. Rather, they are ways of building
arbitrary Grafana JSON.
"""

import attr
from attr.validators import instance_of, in_
import itertools
import math
from numbers import Number
import warnings
import re


class ParseJsonException(Exception):
    pass


@attr.s
class RGBA(object):
    r = attr.ib(validator=instance_of(int))
    g = attr.ib(validator=instance_of(int))
    b = attr.ib(validator=instance_of(int))
    a = attr.ib(validator=instance_of(float))

    def to_json_data(self):
        return "rgba({}, {}, {}, {})".format(self.r, self.g, self.b, self.a)

    REGEX = re.compile("^rgba\((\d+), (\d+), (\d+), (\d*(?:\.\d+)(?:e-\d\d)?)\)$")

    @classmethod
    def parse_json_data(cls, data):
        match = RGBA.REGEX.match(data)

        if match is not None:
            return cls(
                int(match.group(1)),
                int(match.group(2)),
                int(match.group(3)),
                float(match.group(4))
            )

        raise ParseJsonException("Unable to parse RGBA: {}".format(data))


@attr.s
class RGB(object):
    r = attr.ib(validator=instance_of(int))
    g = attr.ib(validator=instance_of(int))
    b = attr.ib(validator=instance_of(int))

    def to_json_data(self):
        return "rgb({}, {}, {})".format(self.r, self.g, self.b)

    REGEX = re.compile("^rgb\((\d+), (\d+), (\d+)\)$")

    @classmethod
    def parse_json_data(cls, data):
        match = RGB.REGEX.match(data)

        if match is not None:
            return cls(int(match.group(1)), int(match.group(2)),
                       int(match.group(3)))

        raise ParseJsonException("Unable to parse RGB: {}".format(data))


@attr.s
class Pixels(object):
    num = attr.ib(validator=instance_of(int))

    def to_json_data(self):
        return '{}px'.format(self.num)

    REGEX = re.compile("^(\d+)(?:px)?$")

    @classmethod
    def parse_json_data(cls, data):
        if isinstance(data, int):
            return cls(num=data)

        match = Pixels.REGEX.match(data)

        if match is not None:
            return cls(num=int(match.group(1)))

        if data == "":
            return None

        raise ParseJsonException("Unable to parse Pixels {}".format(data))


@attr.s
class Percent(object):
    num = attr.ib(default=100, validator=instance_of(Number))

    def to_json_data(self):
        return '{}%'.format(self.num)

    REGEX = re.compile("^(\d+)%$")

    @classmethod
    def parse_json_data(cls, data):
        match = Percent.REGEX.match(data)

        if match is not None:
            return cls(int(match.group(1)))

        raise ParseJsonException("Unable to parse Percent {}".format(data))


GREY1 = RGBA(216, 200, 27, 0.27)
GREY2 = RGBA(234, 112, 112, 0.22)
BLUE_RGBA = RGBA(31, 118, 189, 0.18)
BLUE_RGB = RGB(31, 120, 193)
GREEN = RGBA(50, 172, 45, 0.97)
ORANGE = RGBA(237, 129, 40, 0.89)
RED = RGBA(245, 54, 54, 0.9)
BLANK = RGBA(0, 0, 0, 0.0)

INDIVIDUAL = 'individual'
CUMULATIVE = 'cumulative'

NULL_CONNECTED = 'connected'
NULL_AS_ZERO = 'null as zero'
NULL_AS_NULL = 'null'

FLOT = 'flot'

ABSOLUTE_TYPE = 'absolute'
DASHBOARD_TYPE = 'dashboard'
GRAPH_TYPE = 'graph'
SINGLESTAT_TYPE = 'singlestat'
TABLE_TYPE = 'table'
TEXT_TYPE = 'text'
ALERTLIST_TYPE = "alertlist"
TABLE_TYPE = 'table'

DEFAULT_FILL = 1
DEFAULT_REFRESH = '10s'
DEFAULT_ROW_HEIGHT = Pixels(250)
DEFAULT_LINE_WIDTH = 2
DEFAULT_POINT_RADIUS = 5
DEFAULT_RENDERER = FLOT
DEFAULT_STEP = 10
DEFAULT_LIMIT = 10
TOTAL_SPAN = 12

DARK_STYLE = 'dark'
LIGHT_STYLE = 'light'

UTC = 'utc'

SCHEMA_VERSION = 12

# Y Axis formats
DURATION_FORMAT = "dtdurations"
NO_FORMAT = "none"
OPS_FORMAT = "ops"
PERCENT_UNIT_FORMAT = "percentunit"
DAYS_FORMAT = "d"
HOURS_FORMAT = "h"
MINUTES_FORMAT = "m"
SECONDS_FORMAT = "s"
MILLISECONDS_FORMAT = "ms"
SHORT_FORMAT = "short"
BYTES_FORMAT = "bytes"
BITS_PER_SEC_FORMAT = "bps"
BYTES_PER_SEC_FORMAT = "Bps"

# Alert rule state
STATE_NO_DATA = "no_data"
STATE_ALERTING = "alerting"
STATE_KEEP_LAST_STATE = "keep_state"

# Evaluator
EVAL_GT = "gt"
EVAL_LT = "lt"
EVAL_WITHIN_RANGE = "within_range"
EVAL_OUTSIDE_RANGE = "outside_range"
EVAL_NO_VALUE = "no_value"

# Reducer Type avg/min/max/sum/count/last/median
RTYPE_AVG = "avg"
RTYPE_MIN = "min"
RTYPE_MAX = "max"
RTYPE_SUM = "sum"
RTYPE_COUNT = "count"
RTYPE_LAST = "last"
RTYPE_MEDIAN = "median"

# Condition Type
CTYPE_QUERY = "query"

# Operator
OP_AND = "and"
OP_OR = "or"

# Text panel modes
TEXT_MODE_MARKDOWN = "markdown"
TEXT_MODE_HTML = "html"
TEXT_MODE_TEXT = "text"

# Inputs
DATASOURCE_TYPE = "datasource"
CONSTANT_TYPE = "constant"

# Datasource plugins
PLUGIN_ID_GRAPHITE = "graphite"
PLUGIN_ID_PROMETHEUS = "prometheus"
PLUGIN_ID_INFLUXDB = "influxdb"
PLUGIN_ID_OPENTSDB = "opentsdb"
PLUGIN_ID_ELASTICSEARCH = "elasticsearch"
PLUGIN_ID_CLOUDWATCH = "cloudwatch"

# Target formats
TIME_SERIES_TARGET_FORMAT = "time_series"
TABLE_TARGET_FORMAT = "table"

# Table Transforms
AGGREGATIONS_TRANSFORM = "timeseries_aggregations"
ANNOTATIONS_TRANSFORM = "annotations"
COLUMNS_TRANSFORM = "timeseries_to_columns"
JSON_TRANSFORM = "json"
ROWS_TRANSFORM = "timeseries_to_rows"
TABLE_TRANSFORM = "table"

# AlertList show selections
ALERTLIST_SHOW_CURRENT = "current"
ALERTLIST_SHOW_CHANGES = "changes"

# AlertList state filter options
ALERTLIST_STATE_OK = "ok"
ALERTLIST_STATE_PAUSED = "paused"
ALERTLIST_STATE_NO_DATA = "no_data"
ALERTLIST_STATE_EXECUTION_ERROR = "execution_error"
ALERTLIST_STATE_ALERTING = "alerting"

# Display Sort Order
SORT_ASC = 1
SORT_DESC = 2
SORT_IMPORTANCE = 3


@attr.s
class Mapping(object):

    name = attr.ib()
    value = attr.ib(validator=instance_of(int))

    def to_json_data(self):
        return {
            'name': self.name,
            'value': self.value,
        }

    @classmethod
    def parse_json_data(cls, data):
        return cls(**data)


MAPPING_TYPE_VALUE_TO_TEXT = 1
MAPPING_TYPE_RANGE_TO_TEXT = 2

MAPPING_VALUE_TO_TEXT = Mapping("value to text", MAPPING_TYPE_VALUE_TO_TEXT)
MAPPING_RANGE_TO_TEXT = Mapping("range to text", MAPPING_TYPE_RANGE_TO_TEXT)


# Value types min/max/avg/current/total/name/first/delta/range
VTYPE_MIN = "min"
VTYPE_MAX = "max"
VTYPE_AVG = "avg"
VTYPE_CURR = "current"
VTYPE_TOTAL = "total"
VTYPE_NAME = "name"
VTYPE_FIRST = "first"
VTYPE_DELTA = "delta"
VTYPE_RANGE = "range"
VTYPE_DEFAULT = VTYPE_AVG


@attr.s
class Grid(object):

    threshold1 = attr.ib(default=None)
    threshold1Color = attr.ib(
        default=attr.Factory(lambda: GREY1),
        validator=instance_of(RGBA),
    )
    threshold2 = attr.ib(default=None)
    threshold2Color = attr.ib(
        default=attr.Factory(lambda: GREY2),
        validator=instance_of(RGBA),
    )
    leftLogBase = attr.ib(default=None)
    rightLogBase = attr.ib(default=None)
    rightMin = attr.ib(default=None)
    rightMax = attr.ib(default=None)
    leftMin = attr.ib(default=None)
    leftMax = attr.ib(default=None)

    def to_json_data(self):
        return {
            'threshold1': self.threshold1,
            'threshold1Color': self.threshold1Color,
            'threshold2': self.threshold2,
            'threshold2Color': self.threshold2Color,
            'leftLogBase': self.leftLogBase,
            'rightLogBase': self.rightLogBase,
            'rightMin': self.rightMin,
            'rightMax': self.rightMax,
            'leftMin': self.leftMin,
            'leftMax': self.leftMax,
        }

    @classmethod
    def parse_json_data(cls, data):
        if 'threshold1Color' in data:
            data['threshold1Color'] = RGBA.parse_json_data(
                data['threshold1Color'])
        if 'threshold2Color' in data:
            data['threshold2Color'] = RGBA.parse_json_data(
                data['threshold2Color'])

        return cls(**data)


@attr.s
class Legend(object):
    avg = attr.ib(default=False, validator=instance_of(bool))
    current = attr.ib(default=False, validator=instance_of(bool))
    max = attr.ib(default=False, validator=instance_of(bool))
    min = attr.ib(default=False, validator=instance_of(bool))
    show = attr.ib(default=True, validator=instance_of(bool))
    total = attr.ib(default=False, validator=instance_of(bool))
    values = attr.ib(default=None)
    alignAsTable = attr.ib(default=False, validator=instance_of(bool))
    hideEmpty = attr.ib(default=False, validator=instance_of(bool))
    hideZero = attr.ib(default=False, validator=instance_of(bool))
    rightSide = attr.ib(default=False, validator=instance_of(bool))
    sideWidth = attr.ib(default=None)
    sort = attr.ib(default=None)
    sortDesc = attr.ib(default=None)

    def to_json_data(self):
        values = ((self.avg or self.current or self.max or self.min)
                  if self.values is None else self.values)

        return {
            'avg': self.avg,
            'current': self.current,
            'max': self.max,
            'min': self.min,
            'show': self.show,
            'total': self.total,
            'values': values,
            'alignAsTable': self.alignAsTable,
            'hideEmpty': self.hideEmpty,
            'hideZero': self.hideZero,
            'rightSide': self.rightSide,
            'sideWidth': self.sideWidth,
            'sort': self.sort,
            'sortDesc': self.sortDesc,
        }

    @classmethod
    def parse_json_data(cls, data):
        return cls(**data)


@attr.s
class Target(object):

    expr = attr.ib()
    format = attr.ib(default=TIME_SERIES_TARGET_FORMAT)
    legendFormat = attr.ib(default="")
    interval = attr.ib(default="", validator=instance_of(str))
    intervalFactor = attr.ib(default=2)
    metric = attr.ib(default="")
    refId = attr.ib(default="")
    step = attr.ib(default=DEFAULT_STEP)
    instant = attr.ib(validator=instance_of(bool), default=False)
    datasource = attr.ib(default="")
    hide = attr.ib(default=False)
    format = attr.ib(default=None)
    calculatedInterval = attr.ib(default=None)
    datasourceErrors = attr.ib(default=None)
    errors = attr.ib(default=None)
    interval = attr.ib(default=None)
    target = attr.ib(default=None)
    alias = attr.ib(default=None)
    dimensions = attr.ib(default=None)
    metricName = attr.ib(default=None)
    namespace = attr.ib(default=None)
    period = attr.ib(default=None)
    region = attr.ib(default=None)
    statistics = attr.ib(default=None)

    def to_json_data(self):
        return {
            'expr': self.expr,
            'format': self.format,
            'interval': self.interval,
            'intervalFactor': self.intervalFactor,
            'legendFormat': self.legendFormat,
            'metric': self.metric,
            'refId': self.refId,
            'step': self.step,
            'instant': self.instant,
            'datasource': self.datasource,
            'hide': self.hide,
            'format': self.format,
            'calculatedInterval': self.calculatedInterval,
            'datasourceErrors': self.datasourceErrors,
            'errors': self.errors,
            'interval': self.interval,
            'target': self.target,
            'alias': self.alias,
            'dimensions': self.dimensions,
            'metricName': self.metricName,
            'namespace': self.namespace,
            'period': self.period,
            'region': self.region,
            'statistics': self.statistics,
        }

    @classmethod
    def parse_json_data(cls, data):
        return cls(**data)


@attr.s
class Tooltip(object):

    msResolution = attr.ib(default=True, validator=instance_of(bool))
    shared = attr.ib(default=True, validator=instance_of(bool))
    sort = attr.ib(default=0)
    valueType = attr.ib(default=CUMULATIVE)

    def to_json_data(self):
        return {
            'msResolution': self.msResolution,
            'shared': self.shared,
            'sort': self.sort,
            'value_type': self.valueType,
        }

    @classmethod
    def parse_json_data(cls, data):
        if 'value_type' in data:
            data['valueType'] = data.pop('value_type')

        return cls(**data)


def is_valid_xaxis_mode(instance, attribute, value):
    XAXIS_MODES = ("time", "series")
    if value not in XAXIS_MODES:
        raise ValueError("{attr} should be one of {choice}".format(
            attr=attribute, choice=XAXIS_MODES))


@attr.s
class XAxis(object):

    mode = attr.ib(default="time", validator=is_valid_xaxis_mode)
    name = attr.ib(default=None)
    values = attr.ib(default=attr.Factory(list))
    show = attr.ib(validator=instance_of(bool), default=True)
    buckets = attr.ib(default=None)

    def to_json_data(self):
        return {
            'show': self.show,
        }

    @classmethod
    def parse_json_data(cls, data):
        return cls(**data)


@attr.s
class YAxis(object):
    """A single Y axis.

    Grafana graphs have two Y axes: one on the left and one on the right.
    """
    decimals = attr.ib(default=None)
    format = attr.ib(default=None)
    label = attr.ib(default=None)
    logBase = attr.ib(default=1)
    max = attr.ib(default=None)
    min = attr.ib(default=0)
    show = attr.ib(default=True, validator=instance_of(bool))

    def to_json_data(self):
        return {
            'decimals': self.decimals,
            'format': self.format,
            'label': self.label,
            'logBase': self.logBase,
            'max': self.max,
            'min': self.min,
            'show': self.show,
        }

    @classmethod
    def parse_json_data(cls, data):
        return cls(**data)


@attr.s
class YAxes(object):
    """The pair of Y axes on a Grafana graph.

    Each graph has two Y Axes, a left one and a right one.
    """
    left = attr.ib(default=attr.Factory(lambda: YAxis(format=SHORT_FORMAT)),
                   validator=instance_of(YAxis))
    right = attr.ib(default=attr.Factory(lambda: YAxis(format=SHORT_FORMAT)),
                    validator=instance_of(YAxis))

    def to_json_data(self):
        return [
            self.left,
            self.right,
        ]

    @classmethod
    def parse_json_data(cls, data):
        return cls(left=YAxis(**data[0]), right=YAxis(**data[1]))


def single_y_axis(**kwargs):
    """Specify that a graph has a single Y axis.

    Parameters are those passed to `YAxis`. Returns a `YAxes` object (i.e. a
    pair of axes) that can be used as the yAxes parameter of a graph.
    """
    axis = YAxis(**kwargs)
    return YAxes(left=axis)


def to_y_axes(data):
    """Backwards compatibility for 'YAxes'.

    In grafanalib 0.1.2 and earlier, Y axes were specified as a list of two
    elements. Now, we have a dedicated `YAxes` type.

    This function converts a list of two `YAxis` values to a `YAxes` value,
    silently passes through `YAxes` values, warns about doing things the old
    way, and errors when there are invalid values.
    """
    if isinstance(data, YAxes):
        return data
    if not isinstance(data, (list, tuple)):
        raise ValueError(
            "Y axes must be either YAxes or a list of two values, got %r"
            % data)
    if len(data) != 2:
        raise ValueError(
            "Must specify exactly two YAxes, got %d: %r"
            % (len(data), data))
    warnings.warn(
        "Specify Y axes using YAxes or single_y_axis, rather than a "
        "list/tuple",
        DeprecationWarning, stacklevel=3)
    return YAxes(left=data[0], right=data[1])


def _balance_panels(panels):
    """Resize panels so they are evenly spaced."""
    allotted_spans = sum(panel.span if panel.span else 0 for panel in panels)
    no_span_set = [panel for panel in panels if panel.span is None]
    auto_span = math.ceil(
        (TOTAL_SPAN - allotted_spans) / (len(no_span_set) or 1))
    return [
        attr.assoc(panel, span=auto_span) if panel.span is None else panel
        for panel in panels
    ]


@attr.s
class Row(object):
    # TODO: jml would like to separate the balancing behaviour from this
    # layer.
    panels = attr.ib(default=attr.Factory(list), convert=_balance_panels)
    collapse = attr.ib(
        default=False, validator=instance_of(bool),
    )
    editable = attr.ib(
        default=True, validator=instance_of(bool),
    )
    height = attr.ib(
        default=attr.Factory(lambda: DEFAULT_ROW_HEIGHT),
        validator=instance_of(Pixels),
    )
    showTitle = attr.ib(default=None)
    title = attr.ib(default=None)
    repeat = attr.ib(default=None)
    repeatIteration = attr.ib(default=None)
    repeatRowId = attr.ib(default=None)
    titleSize = attr.ib(default="h6")

    def _iter_panels(self):
        return iter(self.panels)

    def _map_panels(self, f):
        return attr.assoc(self, panels=list(map(f, self.panels)))

    def to_json_data(self):
        showTitle = False
        title = "New row"
        if self.title is not None:
            showTitle = True
            title = self.title
        if self.showTitle is not None:
            showTitle = self.showTitle
        return {
            'collapse': self.collapse,
            'editable': self.editable,
            'height': self.height,
            'panels': self.panels,
            'showTitle': showTitle,
            'title': title,
            'repeat': self.repeat,
            'repeatIteration': self.repeatIteration,
            'repeatRowId': self.repeatRowId,
            'titleSize': self.titleSize,
        }

    @classmethod
    def parse_json_data(cls, data):
        if 'panels' in data:
            data['panels'] = parse_panels(data['panels'])
        if 'height' in data:
            data['height'] = Pixels.parse_json_data(data['height'])

        return cls(**data)


@attr.s
class Annotations(object):
    list = attr.ib(default=attr.Factory(list))

    def to_json_data(self):
        return {
            'list': self.list,
        }

    @classmethod
    def parse_json_data(cls, data):
        return cls(**data)


def parse_input(data):
    object_type = data.get('type')

    if object_type == DATASOURCE_TYPE:
        return DataSourceInput.parse_json_data(data)
    elif object_type == CONSTANT_TYPE:
        return ConstantInput.parse_json_data(data)

    raise ParseJsonException("Unknown input type {}".format(object_type))


def parse_inputs(inputs):
    return [parse_input(data) for data in inputs]


@attr.s
class DataSourceInput(object):
    name = attr.ib()
    label = attr.ib()
    pluginId = attr.ib()
    pluginName = attr.ib()
    description = attr.ib(default="", validator=instance_of(str))
    type = attr.ib(default=DATASOURCE_TYPE)

    def to_json_data(self):
        return {
            "description": self.description,
            "label": self.label,
            "name": self.name,
            "pluginId": self.pluginId,
            "pluginName": self.pluginName,
            "type": DATASOURCE_TYPE,
        }

    @classmethod
    def parse_json_data(cls, data):
        return cls(**data)


@attr.s
class ConstantInput(object):
    name = attr.ib()
    label = attr.ib()
    value = attr.ib()
    description = attr.ib(default="", validator=instance_of(str))
    type = attr.ib(default=CONSTANT_TYPE)

    def to_json_data(self):
        return {
            "description": self.description,
            "label": self.label,
            "name": self.name,
            "type": CONSTANT_TYPE,
            "value": self.value,
        }

    @classmethod
    def parse_json_data(cls, data):
        return cls(**data)


@attr.s
class DashboardLink(object):
    dashboard = attr.ib(default=None)
    uri = attr.ib(default=None)
    keepTime = attr.ib(
        default=True,
        validator=instance_of(bool),
    )
    title = attr.ib(default=None)
    type = attr.ib(default=DASHBOARD_TYPE)
    asDropdown = attr.ib(default=None)
    icon = attr.ib(default=None)
    includeVars = attr.ib(default=None)
    tags = attr.ib(default=attr.Factory(list))
    targetBlank = attr.ib(default=None)
    url = attr.ib(default=None)

    def to_json_data(self):
        title = self.dashboard if self.title is None else self.title
        return {
            "dashUri": self.uri,
            "dashboard": self.dashboard,
            "keepTime": self.keepTime,
            "title": title,
            "type": self. type,
            "url": self.uri,
            "icon": self.icon,
            "includeVars": self.includeVars,
            "tags": self.tags,
            "targetBlank": self.targetBlank,
            "asDropdown": self.asDropdown,
        }

    @classmethod
    def parse_json_data(cls, data):
        if 'dashUri' in data:
            data['uri'] = data.pop('dashUri')

        # TODO: fix url/uri/dashUriw
        data.pop('url')
        return cls(**data)


@attr.s
class Template(object):
    """Template create a new 'variable' for the dashboard, defines the variable
    name, human name, query to fetch the values and the default value.

        :param default: the default value for the variable
        :param dataSource: where to fetch the values for the variable from
        :param label: the variable's human label
        :param name: the variable's name
        :param query: the query users to fetch the valid values of the variable
        :param allValue: specify a custom all value with regex,
            globs or lucene syntax.
        :param includeAll: Add a special All option whose value includes
            all options.
        :param regex: Regex to filter or capture specific parts of the names
            return by your data source query.
        :param multi: If enabled, the variable will support the selection of
            multiple options at the same time.
    """

    default = attr.ib()
    dataSource = attr.ib()
    name = attr.ib()
    query = attr.ib()
    label = attr.ib(default=None)
    allValue = attr.ib(default=None)
    includeAll = attr.ib(
        default=False,
        validator=instance_of(bool),
    )
    multi = attr.ib(
        default=False,
        validator=instance_of(bool),
    )
    regex = attr.ib(default=None)
    useTags = attr.ib(
        default=False,
        validator=instance_of(bool),
    )
    tagsQuery = attr.ib(default=None)
    tagValuesQuery = attr.ib(default=None)
    type = attr.ib(default='query')
    hide = attr.ib(default=1)
    options = attr.ib(default=attr.Factory(list))
    refresh = attr.ib(default=1)
    sort = attr.ib(default=1)
    tagValuesQuery = attr.ib(default=None)
    tagsQuery = attr.ib(default=None)

    def to_json_data(self):
        return {
            'allValue': self.allValue,
            'current': {
                'text': self.default,
                'value': self.default,
                'tags': [],
            },
            'datasource': self.dataSource,
            'hide': self.hide,
            'includeAll': self.includeAll,
            'label': self.label,
            'multi': self.multi,
            'name': self.name,
            'options': self.options,
            'query': self.query,
            'refresh': self.refresh,
            'regex': self.regex,
            'sort': self.sort,
            'type': 'query',
            'useTags': self.useTags,
            'tagsQuery': self.tagsQuery,
            'tagValuesQuery': self.tagValuesQuery,
        }

    @classmethod
    def parse_json_data(cls, data):
        if 'current' in data:
            current = data.pop('current')
            if 'text' in current:
                data['default'] = current['text']
            elif 'value' in current:
                data['default'] = current['value']
        if 'datasource' in data:
            data['dataSource'] = data.pop('datasource')

        return cls(**data)


@attr.s
class Templating(object):
    list = attr.ib(default=attr.Factory(list))

    def to_json_data(self):
        return {
            'list': self.list,
        }

    @classmethod
    def parse_json_data(cls, data):
        return cls(**data)


@attr.s
class Time(object):
    start = attr.ib()
    end = attr.ib()

    def to_json_data(self):
        return {
            'from': self.start,
            'to': self.end,
        }

    @classmethod
    def parse_json_data(cls, data):
        data['start'] = data.pop('from')
        data['end'] = data.pop('to')
        return cls(**data)


DEFAULT_TIME = Time('now-1h', 'now')


@attr.s
class TimePicker(object):
    refreshIntervals = attr.ib()
    timeOptions = attr.ib()
    collapse = attr.ib(default=False)
    enable = attr.ib(default=None)
    notice = attr.ib(default=None)
    now = attr.ib(default=None)
    status = attr.ib(default=None)
    type = attr.ib(default=None)

    def to_json_data(self):
        return {
            'refresh_intervals': self.refreshIntervals,
            'time_options': self.timeOptions,
            'collapse': self.collapse,
            'enable': self.enable,
            'notice': self.notice,
            'now': self.now,
            'status': self.status,
        }

    @classmethod
    def parse_json_data(cls, data):
        if 'refresh_intervals' in data:
            data['refreshIntervals'] = data.pop('refresh_intervals')
        if 'time_options' in data:
            data['timeOptions'] = data.pop('time_options')

        return cls(**data)


DEFAULT_TIME_PICKER = TimePicker(
    refreshIntervals=[
        "5s",
        "10s",
        "30s",
        "1m",
        "5m",
        "15m",
        "30m",
        "1h",
        "2h",
        "1d"
    ],
    timeOptions=[
        "5m",
        "15m",
        "1h",
        "6h",
        "12h",
        "24h",
        "2d",
        "7d",
        "30d"
    ]
)


@attr.s
class Evaluator(object):
    type = attr.ib()
    params = attr.ib()

    def to_json_data(self):
        return {
            "type": self.type,
            "params": self.params,
        }

    @classmethod
    def parse_json_data(cls, data):
        return cls(**data)


def GreaterThan(value):
    return Evaluator(EVAL_GT, [value])


def LowerThan(value):
    return Evaluator(EVAL_LT, [value])


def WithinRange(from_value, to_value):
    return Evaluator(EVAL_WITHIN_RANGE, [from_value, to_value])


def OutsideRange(from_value, to_value):
    return Evaluator(EVAL_OUTSIDE_RANGE, [from_value, to_value])


def NoValue():
    return Evaluator(EVAL_NO_VALUE, [])


@attr.s
class TimeRange(object):
    """A time range for an alert condition.

    A condition has to hold for this length of time before triggering.

    :param str from_time: Either a number + unit (s: second, m: minute,
        h: hour, etc)  e.g. ``"5m"`` for 5 minutes, or ``"now"``.
    :param str to_time: Either a number + unit (s: second, m: minute,
        h: hour, etc)  e.g. ``"5m"`` for 5 minutes, or ``"now"``.
    """

    from_time = attr.ib()
    to_time = attr.ib()

    def to_json_data(self):
        return [self.from_time, self.to_time]

    @classmethod
    def parse_json_data(cls, data):
        return cls(
            from_time=Time.parse_json_data(data[0]),
            to_time=Time.parse_json_data(data[1])
        )


@attr.s
class AlertCondition(object):
    """
    A condition on an alert.

    :param Target target: Metric the alert condition is based on.
    :param Evaluator evaluator: How we decide whether we should alert on the
        metric. e.g. ``GreaterThan(5)`` means the metric must be greater than 5
        to trigger the condition. See ``GreaterThan``, ``LowerThan``,
        ``WithinRange``, ``OutsideRange``, ``NoValue``.
    :param TimeRange timeRange: How long the condition must be true for before
        we alert.
    :param operator: One of ``OP_AND`` or ``OP_OR``. How this condition
        combines with other conditions.
    :param reducerType: RTYPE_*
    :param type: CTYPE_*
    """

    target = attr.ib(validator=instance_of(Target))
    evaluator = attr.ib(validator=instance_of(Evaluator))
    timeRange = attr.ib(validator=instance_of(TimeRange))
    operator = attr.ib()
    reducerType = attr.ib()
    type = attr.ib(default=CTYPE_QUERY)

    def to_json_data(self):
        queryParams = [
            self.target.refId, self.timeRange.from_time, self.timeRange.to_time
        ]
        return {
            "evaluator": self.evaluator,
            "operator": {
                "type": self.operator,
            },
            "query": {
                "model": self.target,
                "params": queryParams,
            },
            "reducer": {
                "params": [],
                "type": self.reducerType,
            },
            "type": self.type,
        }

    @classmethod
    def parse_json_data(cls, data):
        if 'evaluator' in data:
            data['evaluator'] = Evaluator.parse_json_data(data['evaluator'])

        if 'operator' in data:
            data['operator'] = data.pop('operator')['type']

        if 'query' in data:
            query = data.pop('query')
            data['target'] = Target.parse_json_data(query['model'])
            refId, *timeRange = query['params']
            data['target'].refId = refId
            data['timeRange'] = TimeRange.parse_json_data(timeRange)

        if 'reducer' in data:
            data['reducerType'] = data.pop('reducer')['type']

        return cls(**data)


@attr.s
class Alert(object):

    name = attr.ib()
    message = attr.ib()
    alertConditions = attr.ib()
    executionErrorState = attr.ib(default=STATE_ALERTING)
    frequency = attr.ib(default="60s")
    handler = attr.ib(default=1)
    noDataState = attr.ib(default=STATE_NO_DATA)
    notifications = attr.ib(default=attr.Factory(list))

    def to_json_data(self):
        return {
            "conditions": self.alertConditions,
            "executionErrorState": self.executionErrorState,
            "frequency": self.frequency,
            "handler": self.handler,
            "message": self.message,
            "name": self.name,
            "noDataState": self.noDataState,
            "notifications": self.notifications,
        }

    @classmethod
    def parse_json_data(cls, data):
        if 'conditions' in data:
            data['alertConditions'] = data.pop('conditions')
        return cls(**data)


@attr.s
class Dashboard(object):

    title = attr.ib()
    rows = attr.ib()
    annotations = attr.ib(
        default=attr.Factory(Annotations),
        validator=instance_of(Annotations),
    )
    editable = attr.ib(
        default=True,
        validator=instance_of(bool),
    )
    gnetId = attr.ib(default=None)
    hideControls = attr.ib(
        default=False,
        validator=instance_of(bool),
    )
    id = attr.ib(default=None)
    inputs = attr.ib(default=attr.Factory(list))
    links = attr.ib(default=attr.Factory(list))
    refresh = attr.ib(default=DEFAULT_REFRESH)
    schemaVersion = attr.ib(default=SCHEMA_VERSION)
    sharedCrosshair = attr.ib(
        default=False,
        validator=instance_of(bool),
    )
    style = attr.ib(default=DARK_STYLE)
    tags = attr.ib(default=attr.Factory(list))
    templating = attr.ib(
        default=attr.Factory(Templating),
        validator=instance_of(Templating),
    )
    time = attr.ib(
        default=attr.Factory(lambda: DEFAULT_TIME),
        validator=instance_of(Time),
    )
    timePicker = attr.ib(
        default=attr.Factory(lambda: DEFAULT_TIME_PICKER),
        validator=instance_of(TimePicker),
    )
    timezone = attr.ib(default=UTC)
    version = attr.ib(default=0)
    graphTooltip = attr.ib(default=0)

    def _iter_panels(self):
        for row in self.rows:
            for panel in row._iter_panels():
                yield panel

    def _map_panels(self, f):
        return attr.assoc(self, rows=[r._map_panels(f) for r in self.rows])

    def auto_panel_ids(self):
        """Give unique IDs all the panels without IDs.

        Returns a new ``Dashboard`` that is the same as this one, except all
        of the panels have their ``id`` property set. Any panels which had an
        ``id`` property set will keep that property, all others will have
        auto-generated IDs provided for them.
        """
        ids = set([panel.id for panel in self._iter_panels() if panel.id])
        auto_ids = (i for i in itertools.count(1) if i not in ids)

        def set_id(panel):
            return panel if panel.id else attr.assoc(panel, id=next(auto_ids))
        return self._map_panels(set_id)

    def to_json_data(self):
        return {
            '__inputs': self.inputs,
            'annotations': self.annotations,
            'editable': self.editable,
            'gnetId': self.gnetId,
            'hideControls': self.hideControls,
            'id': self.id,
            'links': self.links,
            'refresh': self.refresh,
            'rows': self.rows,
            'schemaVersion': self.schemaVersion,
            'sharedCrosshair': self.sharedCrosshair,
            'style': self.style,
            'tags': self.tags,
            'templating': self.templating,
            'title': self.title,
            'time': self.time,
            'timepicker': self.timePicker,
            'timezone': self.timezone,
            'version': self.version,
            'graphTooltip': self.graphTooltip,
        }

    @classmethod
    def parse_json_data(cls, data):
        if '__inputs' in data:
            data['inputs'] = parse_inputs(data.pop('__inputs'))
        if 'annotations' in data:
            data['annotations'] = Annotations.parse_json_data(
                data['annotations'])
        if 'templating' in data:
            data['templating'] = Templating.parse_json_data(data['templating'])
        if 'rows' in data:
            data['rows'] = [Row.parse_json_data(row) for row in data['rows']]
        if 'time' in data:
            data['time'] = Time.parse_json_data(data['time'])
        if 'timepicker' in data:
            data['timePicker'] = TimePicker.parse_json_data(
                data.pop('timepicker'))
        if 'links' in data:
            data['links'] = [DashboardLink.parse_json_data(link)
                             for link in data['links']]

        return cls(**data)


def parse_panel(panel):
    panel_type = panel.get('type')

    if panel_type == GRAPH_TYPE:
        return Graph.parse_json_data(panel)
    elif panel_type == TEXT_TYPE:
        return Text.parse_json_data(panel)
    elif panel_type == SINGLESTAT_TYPE:
        return SingleStat.parse_json_data(panel)
    elif panel_type == TABLE_TYPE:
        return Table.parse_json_data(panel)

    raise ParseJsonException("Unknown panel type {}".format(panel_type))


def parse_panels(panels):
    return [parse_panel(panel) for panel in panels]


@attr.s
class Graph(object):

    title = attr.ib()
    dataSource = attr.ib()
    targets = attr.ib()
    aliasColors = attr.ib(default=attr.Factory(dict))
    bars = attr.ib(default=False, validator=instance_of(bool))
    description = attr.ib(default=None)
    editable = attr.ib(default=True, validator=instance_of(bool))
    error = attr.ib(default=False, validator=instance_of(bool))
    fill = attr.ib(default=1, validator=instance_of(int))
    grid = attr.ib(default=attr.Factory(Grid), validator=instance_of(Grid))
    id = attr.ib(default=None)
    isNew = attr.ib(default=True, validator=instance_of(bool))
    legend = attr.ib(
        default=attr.Factory(Legend),
        validator=instance_of(Legend),
    )
    lines = attr.ib(default=True, validator=instance_of(bool))
    lineWidth = attr.ib(default=DEFAULT_LINE_WIDTH)
    links = attr.ib(default=attr.Factory(list))
    nullPointMode = attr.ib(default=NULL_CONNECTED)
    percentage = attr.ib(default=False, validator=instance_of(bool))
    pointRadius = attr.ib(default=DEFAULT_POINT_RADIUS)
    points = attr.ib(default=False, validator=instance_of(bool))
    renderer = attr.ib(default=DEFAULT_RENDERER)
    seriesOverrides = attr.ib(default=attr.Factory(list))
    span = attr.ib(default=None)
    stack = attr.ib(default=False, validator=instance_of(bool))
    steppedLine = attr.ib(default=False, validator=instance_of(bool))
    timeFrom = attr.ib(default=None)
    timeShift = attr.ib(default=None)
    tooltip = attr.ib(
        default=attr.Factory(Tooltip),
        validator=instance_of(Tooltip),
    )
    transparent = attr.ib(default=False, validator=instance_of(bool))
    xAxis = attr.ib(default=attr.Factory(XAxis), validator=instance_of(XAxis))
    # XXX: This isn't a *good* default, rather it's the default Grafana uses.
    yAxes = attr.ib(
        default=attr.Factory(YAxes),
        convert=to_y_axes,
        validator=instance_of(YAxes),
    )
    alert = attr.ib(default=None)
    dashLength = attr.ib(default=10)
    dashes = attr.ib(default=False)
    spaceLength = attr.ib(default=10)
    decimals = attr.ib(default=None)
    minSpan = attr.ib(default=None)
    repeat = attr.ib(default=None)
    scopedVars = attr.ib(default=None)
    repeatIteration = attr.ib(default=None)
    repeatPanelId = attr.ib(default=None)
    hideTimeOverride = attr.ib(default=None)
    x_axis = attr.ib(default=None)
    y_axis = attr.ib(default=None)
    y_formats = attr.ib(default=None)
    type = attr.ib(default=GRAPH_TYPE)

    def to_json_data(self):
        graphObject = {
            'aliasColors': self.aliasColors,
            'bars': self.bars,
            'datasource': self.dataSource,
            'description': self.description,
            'editable': self.editable,
            'error': self.error,
            'fill': self.fill,
            'grid': self.grid,
            'id': self.id,
            'isNew': self.isNew,
            'legend': self.legend,
            'lines': self.lines,
            'linewidth': self.lineWidth,
            'links': self.links,
            'nullPointMode': self.nullPointMode,
            'percentage': self.percentage,
            'pointradius': self.pointRadius,
            'points': self.points,
            'renderer': self.renderer,
            'seriesOverrides': self.seriesOverrides,
            'span': self.span,
            'stack': self.stack,
            'steppedLine': self.steppedLine,
            'targets': self.targets,
            'timeFrom': self.timeFrom,
            'timeShift': self.timeShift,
            'title': self.title,
            'tooltip': self.tooltip,
            'transparent': self.transparent,
            'type': GRAPH_TYPE,
            'xaxis': self.xAxis,
            'yaxes': self.yAxes,
            'dashLength': self.dashLength,
            'dashes': self.dashes,
            'spaceLength': self.spaceLength,
            'decimals': self.decimals,
            'minSpan': self.minSpan,
            'repeat': self.repeat,
            'scopedVars': self.scopedVars,
            'repeatIteration': self.repeatIteration,
            'repeatPanelId': self.repeatPanelId,
            'hideTimeOverride': self.hideTimeOverride,
            'x-axis': self.x_axis,
            'y-axis': self.y_axis,
            'y_formats': self.y_formats,
        }
        if self.alert:
            graphObject['alert'] = self.alert
        return graphObject

    @classmethod
    def parse_json_data(cls, data):
        data['dataSource'] = data.pop('datasource')
        if 'linewidth' in data:
            data['lineWidth'] = data.pop('linewidth')
        if 'pointradius' in data:
            data['pointRadius'] = data.pop('pointradius')
        if 'xaxis' in data:
            data['xAxis'] = XAxis.parse_json_data(data.pop('xaxis'))
        if 'yaxes' in data:
            data['yAxes'] = YAxes.parse_json_data(data.pop('yaxes'))
        if 'grid' in data:
            data['grid'] = Grid.parse_json_data(data['grid'])
        if 'legend' in data:
            data['legend'] = Legend.parse_json_data(data['legend'])
        if 'tooltip' in data:
            data['tooltip'] = Tooltip.parse_json_data(data['tooltip'])
        if 'targets' in data:
            data['targets'] = [Target.parse_json_data(target)
                               for target in data['targets']]
        if 'x-axis' in data:
            data['x_axis'] = data.pop('x-axis')
        if 'y-axis' in data:
            data['y_axis'] = data.pop('y-axis')
        if 'links' in data:
            data['links'] = [DashboardLink.parse_json_data(link)
                             for link in data['links']]
        if 'alert' in data:
            data['alert'] = Alert.parse_json_data(data['alert'])

        return cls(**data)


@attr.s
class SparkLine(object):
    fillColor = attr.ib(
        default=attr.Factory(lambda: BLUE_RGBA),
        validator=instance_of(RGBA),
    )
    full = attr.ib(default=False, validator=instance_of(bool))
    lineColor = attr.ib(
        default=attr.Factory(lambda: BLUE_RGB),
        validator=instance_of(RGB),
    )
    show = attr.ib(default=False, validator=instance_of(bool))

    def to_json_data(self):
        return {
            'fillColor': self.fillColor,
            'full': self.full,
            'lineColor': self.lineColor,
            'show': self.show,
        }

    @classmethod
    def parse_json_data(cls, data):
        if 'fillColor' in data:
            data['fillColor'] = RGBA.parse_json_data(data['fillColor'])
        if 'lineColor' in data:
            data['lineColor'] = RGB.parse_json_data(data['lineColor'])
        return cls(**data)


@attr.s
class ValueMap(object):
    op = attr.ib()
    text = attr.ib()
    value = attr.ib()

    def to_json_data(self):
        return {
            'op': self.op,
            'text': self.text,
            'value': self.value,
        }

    @classmethod
    def parse_json_data(cls, data):
        return cls(**data)


@attr.s
class RangeMap(object):
    start = attr.ib()
    end = attr.ib()
    text = attr.ib()

    def to_json_data(self):
        return {
            'start': self.start,
            'end': self.end,
            'text': self.text,
        }

    @classmethod
    def parse_json_data(cls, data):
        return cls(**data)


@attr.s
class Gauge(object):

    minValue = attr.ib(default=0, validator=instance_of(int))
    maxValue = attr.ib(default=100, validator=instance_of(int))
    show = attr.ib(default=False, validator=instance_of(bool))
    thresholdLabels = attr.ib(default=False, validator=instance_of(bool))
    thresholdMarkers = attr.ib(default=True, validator=instance_of(bool))

    def to_json_data(self):
        return {
            'maxValue': self.maxValue,
            'minValue': self.minValue,
            'show': self.show,
            'thresholdLabels': self.thresholdLabels,
            'thresholdMarkers': self.thresholdMarkers,
        }

    @classmethod
    def parse_json_data(cls, data):
        return cls(**data)


@attr.s
class Text(object):
    """Generates a Text panel."""

    content = attr.ib()
    editable = attr.ib(default=True, validator=instance_of(bool))
    error = attr.ib(default=False, validator=instance_of(bool))
    height = attr.ib(default=None)
    id = attr.ib(default=None)
    links = attr.ib(default=attr.Factory(list))
    mode = attr.ib(default=TEXT_MODE_MARKDOWN)
    span = attr.ib(default=None)
    title = attr.ib(default="")
    transparent = attr.ib(default=False, validator=instance_of(bool))
    dataSource = attr.ib(default=None)
    style = attr.ib(default=None)
    isNew = attr.ib(default=None)
    type = attr.ib(default=TEXT_TYPE)

    def to_json_data(self):
        return {
            'content': self.content,
            'editable': self.editable,
            'error': self.error,
            'height': self.height,
            'id': self.id,
            'links': self.links,
            'mode': self.mode,
            'span': self.span,
            'title': self.title,
            'transparent': self.transparent,
            'type': TEXT_TYPE,
            'datasource': self.dataSource,
            'style': self.style,
            'isNew': self.isNew,
        }

    @classmethod
    def parse_json_data(cls, data):
        if 'datasource' in data:
            data['dataSource'] = data.pop('datasource')
        if 'links' in data:
            data['links'] = [DashboardLink.parse_json_data(link)
                             for link in data['links']]

        return cls(**data)


@attr.s
class AlertList(object):
    """Generates the AlertList Panel."""

    description = attr.ib(default="")
    id = attr.ib(default=None)
    limit = attr.ib(default=DEFAULT_LIMIT)
    links = attr.ib(default=attr.Factory(list))
    onlyAlertsOnDashboard = attr.ib(default=True, validator=instance_of(bool))
    show = attr.ib(default=ALERTLIST_SHOW_CURRENT)
    sortOrder = attr.ib(default=SORT_ASC, validator=in_([1, 2, 3]))
    stateFilter = attr.ib(default=attr.Factory(list))
    title = attr.ib(default="")
    transparent = attr.ib(default=False, validator=instance_of(bool))

    def to_json_data(self):
        return {
            'description': self.description,
            'id': self.id,
            'limit': self.limit,
            'links': self.links,
            'onlyAlertsOnDashboard': self.onlyAlertsOnDashboard,
            'show': self.show,
            'sortOrder': self.sortOrder,
            'stateFilter': self.stateFilter,
            'title': self.title,
            'transparent': self.transparent,
            'type': ALERTLIST_TYPE,
        }


@attr.s
class SingleStat(object):
    """Generates Single Stat panel json structure

    Grafana doc on singlestat: http://docs.grafana.org/reference/singlestat/

    :param dataSource: Grafana datasource name
    :param targets: list of metric requests for chosen datasource
    :param title: panel title
    :param cacheTimeout: metric query result cache ttl
    :param colors: the list of colors that can be used for coloring
        panel value or background. Additional info on coloring in docs:
        http://docs.grafana.org/reference/singlestat/#coloring
    :param colorBackground: defines if grafana will color panel background
    :param colorValue: defines if grafana will color panel value
    :param description: optional panel description
    :param decimals: override automatic decimal precision for legend/tooltips
    :param editable: defines if panel is editable via web interfaces
    :param format: defines value units
    :param gauge: draws and additional speedometer-like gauge based
    :param height: defines panel height
    :param hideTimeOverride: hides time overrides
    :param id: panel id
    :param interval: defines time interval between metric queries
    :param links: additional web links
    :param mappingType: defines panel mapping type.
        Additional info can be found in docs:
        http://docs.grafana.org/reference/singlestat/#value-to-text-mapping
    :param mappingTypes: the list of available mapping types for panel
    :param maxDataPoints: maximum metric query results,
        that will be used for rendering
    :param minSpan: minimum span number
    :param nullText: defines what to show if metric query result is undefined
    :param nullPointMode: defines how to render undefined values
    :param postfix: defines postfix that will be attached to value
    :param postfixFontSize: defines postfix font size
    :param prefix: defines prefix that will be attached to value
    :param prefixFontSize: defines prefix font size
    :param rangeMaps: the list of value to text mappings
    :param span: defines the number of spans that will be used for panel
    :param sparkline: defines if grafana should draw an additional sparkline.
        Sparkline grafana documentation:
        http://docs.grafana.org/reference/singlestat/#spark-lines
    :param thresholds: single stat thresholds
    :param transparent: defines if panel should be transparent
    :param valueFontSize: defines value font size
    :param valueName: defines value type. possible values are:
        min, max, avg, current, total, name, first, delta, range
    :param valueMaps: the list of value to text mappings
    :param timeFrom: time range that Override relative time
    """

    dataSource = attr.ib()
    targets = attr.ib()
    title = attr.ib()
    cacheTimeout = attr.ib(default=None)
    colors = attr.ib(default=attr.Factory(lambda: [GREEN, ORANGE, RED]))
    colorBackground = attr.ib(default=False, validator=instance_of(bool))
    colorValue = attr.ib(default=False, validator=instance_of(bool))
    description = attr.ib(default=None)
    decimals = attr.ib(default=None)
    editable = attr.ib(default=True, validator=instance_of(bool))
    format = attr.ib(default="none")
    gauge = attr.ib(default=attr.Factory(Gauge),
                    validator=instance_of(Gauge))
    height = attr.ib(default=None)
    hideTimeOverride = attr.ib(default=False, validator=instance_of(bool))
    id = attr.ib(default=None)
    interval = attr.ib(default=None)
    links = attr.ib(default=attr.Factory(list))
    mappingType = attr.ib(default=MAPPING_TYPE_VALUE_TO_TEXT)
    mappingTypes = attr.ib(
        default=attr.Factory(lambda: [
            MAPPING_VALUE_TO_TEXT,
            MAPPING_RANGE_TO_TEXT,
        ]),
    )
    maxDataPoints = attr.ib(default=100)
    minSpan = attr.ib(default=None)
    nullText = attr.ib(default=None)
    nullPointMode = attr.ib(default="connected")
    postfix = attr.ib(default="")
    postfixFontSize = attr.ib(default="50%")
    prefix = attr.ib(default="")
    prefixFontSize = attr.ib(default="50%")
    rangeMaps = attr.ib(default=attr.Factory(list))
    repeat = attr.ib(default=None)
    span = attr.ib(default=6)
    sparkline = attr.ib(
        default=attr.Factory(SparkLine),
        validator=instance_of(SparkLine),
    )
    thresholds = attr.ib(default="")
    transparent = attr.ib(default=False, validator=instance_of(bool))
    valueFontSize = attr.ib(default="80%")
    valueName = attr.ib(default=VTYPE_DEFAULT)
    valueMaps = attr.ib(default=attr.Factory(list))
    timeFrom = attr.ib(default=None)
    tableColumn = attr.ib(default="")
    error = attr.ib(default=None)
    timeFrom = attr.ib(default=None)
    timeShift = attr.ib(default=None)
    type = attr.ib(default=SINGLESTAT_TYPE)

    def to_json_data(self):
        return {
            'cacheTimeout': self.cacheTimeout,
            'colorBackground': self.colorBackground,
            'colorValue': self.colorValue,
            'colors': self.colors,
            'datasource': self.dataSource,
            'decimals': self.decimals,
            'description': self.description,
            'editable': self.editable,
            'format': self.format,
            'gauge': self.gauge,
            'id': self.id,
            'interval': self.interval,
            'links': self.links,
            'height': self.height,
            'hideTimeOverride': self.hideTimeOverride,
            'mappingType': self.mappingType,
            'mappingTypes': self.mappingTypes,
            'maxDataPoints': self.maxDataPoints,
            'minSpan': self.minSpan,
            'nullPointMode': self.nullPointMode,
            'nullText': self.nullText,
            'postfix': self.postfix,
            'postfixFontSize': self.postfixFontSize,
            'prefix': self.prefix,
            'prefixFontSize': self.prefixFontSize,
            'rangeMaps': self.rangeMaps,
            'repeat': self.repeat,
            'span': self.span,
            'sparkline': self.sparkline,
            'targets': self.targets,
            'thresholds': self.thresholds,
            'title': self.title,
            'transparent': self.transparent,
            'type': SINGLESTAT_TYPE,
            'valueFontSize': self.valueFontSize,
            'valueMaps': self.valueMaps,
            'valueName': self.valueName,
            'timeFrom': self.timeFrom,
        }


@attr.s
class DateColumnStyleType(object):
    TYPE = 'date'

    dateFormat = attr.ib(default="YYYY-MM-DD HH:mm:ss")

    def to_json_data(self):
        return {
            'dateFormat': self.dateFormat,
            'type': self.TYPE,
        }


@attr.s
class NumberColumnStyleType(object):
    TYPE = 'number'

    colorMode = attr.ib(default=None)
    colors = attr.ib(default=attr.Factory(lambda: [GREEN, ORANGE, RED]))
    thresholds = attr.ib(default=attr.Factory(list))
    decimals = attr.ib(default=2, validator=instance_of(int))
    unit = attr.ib(default=SHORT_FORMAT)

    def to_json_data(self):
        return {
            'colorMode': self.colorMode,
            'colors': self.colors,
            'decimals': self.decimals,
            'thresholds': self.thresholds,
            'type': self.TYPE,
            'unit': self.unit,
        }


@attr.s
class StringColumnStyleType(object):
    TYPE = 'string'

    preserveFormat = attr.ib(validator=instance_of(bool))
    sanitize = attr.ib(validator=instance_of(bool))

    def to_json_data(self):
        return {
            'preserveFormat': self.preserveFormat,
            'sanitize': self.sanitize,
            'type': self.TYPE,
        }


@attr.s
class HiddenColumnStyleType(object):
    TYPE = 'hidden'

    def to_json_data(self):
        return {
            'type': self.TYPE,
        }


@attr.s
class ColumnStyle(object):

    alias = attr.ib(default="")
    pattern = attr.ib(default="")
    type = attr.ib(
        default=attr.Factory(NumberColumnStyleType),
        validator=instance_of((
            DateColumnStyleType,
            HiddenColumnStyleType,
            NumberColumnStyleType,
            StringColumnStyleType,
        ))
    )

    def to_json_data(self):
        data = {
            'alias': self.alias,
            'pattern': self.pattern,
        }
        data.update(self.type.to_json_data())
        return data


@attr.s
class ColumnSort(object):
    col = attr.ib(default=None)
    desc = attr.ib(default=False, validator=instance_of(bool))

    def to_json_data(self):
        return {
            'col': self.col,
            'desc': self.desc,
        }


@attr.s
class Column(object):
    """Details of an aggregation column in a table panel.

    :param text: name of column
    :param value: aggregation function
    """

    text = attr.ib(default="Avg")
    value = attr.ib(default="avg")

    def to_json_data(self):
        return {
            'text': self.text,
            'value': self.value,
        }


def _style_columns(columns):
    """Generate a list of column styles given some styled columns.

    The 'Table' object in Grafana separates column definitions from column
    style definitions. However, when defining dashboards it can be very useful
    to define the style next to the column. This function helps that happen.

    :param columns: A list of (Column, ColumnStyle) pairs. The associated
        ColumnStyles must not have a 'pattern' specified. You can also provide
       'None' if you want to use the default styles.
    :return: A list of ColumnStyle values that can be used in a Grafana
        definition.
    """
    new_columns = []
    styles = []
    for column, style in columns:
        new_columns.append(column)
        if not style:
            continue
        if style.pattern and style.pattern != column.text:
            raise ValueError(
                "ColumnStyle pattern (%r) must match the column name (%r) if "
                "specified" % (style.pattern, column.text))
        styles.append(attr.evolve(style, pattern=column.text))
    return new_columns, styles


@attr.s
class Table(object):
    """Generates Table panel json structure

    Grafana doc on table: http://docs.grafana.org/reference/table_panel/

    :param columns: table columns for Aggregations view
    :param dataSource: Grafana datasource name
    :param description: optional panel description
    :param editable: defines if panel is editable via web interfaces
    :param fontSize: defines value font size
    :param height: defines panel height
    :param hideTimeOverride: hides time overrides
    :param id: panel id
    :param links: additional web links
    :param minSpan: minimum span number
    :param pageSize: rows per page (None is unlimited)
    :param scroll: scroll the table instead of displaying in full
    :param showHeader: show the table header
    :param span: defines the number of spans that will be used for panel
    :param styles: defines formatting for each column
    :param targets: list of metric requests for chosen datasource
    :param title: panel title
    :param transform: table style
    :param transparent: defines if panel should be transparent
    """

    dataSource = attr.ib()
    targets = attr.ib()
    title = attr.ib()
    columns = attr.ib(default=attr.Factory(list))
    description = attr.ib(default=None)
    editable = attr.ib(default=True, validator=instance_of(bool))
    fontSize = attr.ib(default="100%")
    height = attr.ib(default=None)
    hideTimeOverride = attr.ib(default=False, validator=instance_of(bool))
    id = attr.ib(default=None)
    links = attr.ib(default=attr.Factory(list))
    minSpan = attr.ib(default=None)
    pageSize = attr.ib(default=None)
    repeat = attr.ib(default=None)
    scroll = attr.ib(default=True, validator=instance_of(bool))
    showHeader = attr.ib(default=True, validator=instance_of(bool))
    span = attr.ib(default=6)
    sort = attr.ib(
        default=attr.Factory(ColumnSort), validator=instance_of(ColumnSort))
    styles = attr.ib()

    transform = attr.ib(default=COLUMNS_TRANSFORM)
    transparent = attr.ib(default=False, validator=instance_of(bool))

    @styles.default
    def styles_default(self):
        return [
            ColumnStyle(
                alias="Time",
                pattern="time",
                type=DateColumnStyleType(),
            ),
            ColumnStyle(
                pattern="/.*/",
            ),
        ]

    @classmethod
    def with_styled_columns(cls, columns, styles=None, **kwargs):
        """Construct a table where each column has an associated style.

        :param columns: A list of (Column, ColumnStyle) pairs, where the
            ColumnStyle is the style for the column and does **not** have a
            pattern set (or the pattern is set to exactly the column name).
            The ColumnStyle may also be None.
        :param styles: An optional list of extra column styles that will be
            appended to the table's list of styles.
        :param **kwargs: Other parameters to the Table constructor.
        :return: A Table.
        """
        extraStyles = styles if styles else []
        columns, styles = _style_columns(columns)
        return cls(columns=columns, styles=styles + extraStyles, **kwargs)

    def to_json_data(self):
        return {
            'columns': self.columns,
            'datasource': self.dataSource,
            'description': self.description,
            'editable': self.editable,
            'fontSize': self.fontSize,
            'height': self.height,
            'hideTimeOverride': self.hideTimeOverride,
            'id': self.id,
            'links': self.links,
            'minSpan': self.minSpan,
            'pageSize': self.pageSize,
            'repeat': self.repeat,
            'scroll': self.scroll,
            'showHeader': self.showHeader,
            'span': self.span,
            'sort': self.sort,
            'styles': self.styles,
            'targets': self.targets,
            'title': self.title,
            'transform': self.transform,
            'transparent': self.transparent,
            'type': TABLE_TYPE,
            'tableColumn': self.tableColumn,
            'error': self.error,
            'timeFrom': self.timeFrom,
            'timeShift': self.timeShift,
        }

    @classmethod
    def parse_json_data(cls, data):
        if 'colors' in data:
            data['colors'] = [RGBA.parse_json_data(color)
                              for color in data['colors']]
        if 'datasource' in data:
            data['dataSource'] = data.pop('datasource')
        if 'targets' in data:
            data['targets'] = [Target.parse_json_data(target)
                               for target in data['targets']]
        if 'gauge' in data:
            data['gauge'] = Gauge.parse_json_data(data['gauge'])
        if 'sparkline' in data:
            data['sparkline'] = SparkLine.parse_json_data(data['sparkline'])
        if 'mappingTypes' in data:
            data['mappingTypes'] = [Mapping.parse_json_data(map_type)
                                    for map_type in data['mappingTypes']]
        if 'height' in data:
            data['height'] = Pixels.parse_json_data(data['height'])
        if 'links' in data:
            data['links'] = [DashboardLink.parse_json_data(link)
                             for link in data['links']]
        if 'rangeMaps' in data:
            data['rangeMaps'] = [RangeMap.parse_json_data(rmap)
                                 for rmap in data['rangeMaps']]
        if 'valueMaps' in data:
            data['valueMaps'] = [ValueMap.parse_json_data(vmap)
                                 for vmap in data['valueMaps']]

        return cls(**data)


@attr.s
class Table(object):
    columns = attr.ib(default=None)
    dataSource = attr.ib(default=None)
    editable = attr.ib(default=None)
    error = attr.ib(default=None)
    fontSize = attr.ib(default=None)
    height = attr.ib(default=None)
    hideTimeOverride = attr.ib(default=None)
    id = attr.ib(default=None)
    links = attr.ib(default=attr.Factory(list))
    pageSize = attr.ib(default=None)
    scroll = attr.ib(default=None)
    showHeader = attr.ib(default=None)
    sort = attr.ib(default=None)
    span = attr.ib(default=None)
    styles = attr.ib(default=None)
    targets = attr.ib(default=None)
    timeFrom = attr.ib(default=None)
    title = attr.ib(default=None)
    transform = attr.ib(default=None)
    transparent = attr.ib(default=None)
    filterNull = attr.ib(default=None)
    type = attr.ib(default=TABLE_TYPE)

    def to_json_data(self):
        return {
            'columns': self.columns,
            'datasource': self.dataSource,
            'editable': self.editable,
            'error': self.error,
            'fontSize': self.fontSize,
            'height': self.height,
            'hideTimeOverride': self.hideTimeOverride,
            'id': self.id,
            'links': self.links,
            'pageSize': self.pageSize,
            'scroll': self.scroll,
            'showHeader': self.showHeader,
            'sort': self.sort,
            'span': self.span,
            'styles': self.styles,
            'targets': self.targets,
            'timeFrom': self.timeFrom,
            'title': self.title,
            'transform': self.transform,
            'transparent': self.transparent,
            'type': TABLE_TYPE,
            'filterNull': self.filterNull,
        }

    @classmethod
    def parse_json_data(cls, data):
        if 'datasource' in data:
            data['dataSource'] = data.pop('datasource')
        if 'targets' in data:
            data['targets'] = [Target.parse_json_data(target)
                               for target in data['targets']]
        if 'height' in data:
            data['height'] = Pixels.parse_json_data(data['height'])
        if 'links' in data:
            data['links'] = [DashboardLink.parse_json_data(link)
                             for link in data['links']]

        return cls(**data)
