# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Union
from . import _utilities, _tables


class Dashboard(pulumi.CustomResource):
    dashboard_url: pulumi.Output[str]
    """
    The URL for viewing the dashboard.
    """
    editable: pulumi.Output[str]
    """
    Determines who can edit the dashboard in an account. Valid values are `all`,  `editable_by_all`, `editable_by_owner`, or `read_only`.  Defaults to `editable_by_all`.
    """
    filter: pulumi.Output[dict]
    """
    A nested block that describes a dashboard filter.  Exactly one nested `filter` block is allowed. See Nested filter block below for details.

      * `attributes` (`list`)
      * `eventTypes` (`list`)
    """
    grid_column_count: pulumi.Output[float]
    """
    The number of columns to use when organizing and displaying widgets. New Relic One supports a 3 column grid and a 12 column grid. New Relic Insights supports a 3 column grid.
    """
    icon: pulumi.Output[str]
    """
    The icon for the dashboard.  Valid values are `adjust`, `archive`, `bar-chart`, `bell`, `bolt`, `bug`, `bullhorn`, `bullseye`, `clock-o`, `cloud`, `cog`, `comments-o`, `crosshairs`, `dashboard`, `envelope`, `fire`, `flag`, `flask`, `globe`, `heart`, `leaf`, `legal`, `life-ring`, `line-chart`, `magic`, `mobile`, `money`, `none`, `paper-plane`, `pie-chart`, `puzzle-piece`, `road`, `rocket`, `shopping-cart`, `sitemap`, `sliders`, `tablet`, `thumbs-down`, `thumbs-up`, `trophy`, `usd`, `user`, and `users`.  Defaults to `bar-chart`.
    """
    title: pulumi.Output[str]
    """
    The title of the dashboard.
    """
    visibility: pulumi.Output[str]
    """
    Determines who can see the dashboard in an account. Valid values are `all` or `owner`.  Defaults to `all`.
    """
    widgets: pulumi.Output[list]
    """
    A nested block that describes a visualization.  Up to 300 `widget` blocks are allowed in a dashboard definition.  See Nested widget blocks below for details.

      * `column` (`float`)
      * `compareWiths` (`list`)
        * `offsetDuration` (`str`)
        * `presentation` (`dict`)
          * `color` (`str`)
          * `name` (`str`)

      * `drilldownDashboardId` (`float`)
      * `duration` (`float`)
      * `endTime` (`float`)
      * `entityIds` (`list`)
      * `facet` (`str`)
      * `height` (`float`)
      * `limit` (`float`)
      * `metrics` (`list`)
        * `name` (`str`)
        * `scope` (`str`)
        * `units` (`str`)
        * `values` (`list`)

      * `notes` (`str`)
      * `nrql` (`str`)
      * `orderBy` (`str`)
      * `rawMetricName` (`str`)
      * `row` (`float`)
      * `source` (`str`)
      * `thresholdRed` (`float`)
      * `thresholdYellow` (`float`)
      * `title` (`str`) - The title of the dashboard.
      * `visualization` (`str`)
      * `widgetId` (`float`)
      * `width` (`float`)
    """
    def __init__(__self__, resource_name, opts=None, editable=None, filter=None, grid_column_count=None, icon=None, title=None, visibility=None, widgets=None, __props__=None, __name__=None, __opts__=None):
        """
        Use this resource to create and manage New Relic dashboards.

        ## Example Usage
        ### Create A New Relic Dashboard

        ```python
        import pulumi
        import pulumi_newrelic as newrelic

        my_application = newrelic.get_entity(name="My Application",
            type="APPLICATION",
            domain="APM")
        exampledash = newrelic.Dashboard("exampledash",
            title="New Relic Terraform Example",
            filter={
                "eventTypes": ["Transaction"],
                "attributes": [
                    "appName",
                    "name",
                ],
            },
            widgets=[
                {
                    "title": "Requests per minute",
                    "visualization": "billboard",
                    "nrql": "SELECT rate(count(*), 1 minute) FROM Transaction",
                    "row": 1,
                    "column": 1,
                },
                {
                    "title": "Error rate",
                    "visualization": "gauge",
                    "nrql": "SELECT percentage(count(*), WHERE error IS True) FROM Transaction",
                    "thresholdRed": 2.5,
                    "row": 1,
                    "column": 2,
                },
                {
                    "title": "Average transaction duration, by application",
                    "visualization": "facet_bar_chart",
                    "nrql": "SELECT average(duration) FROM Transaction FACET appName",
                    "row": 1,
                    "column": 3,
                },
                {
                    "title": "Apdex, top 5 by host",
                    "duration": 1800000,
                    "visualization": "metric_line_chart",
                    "entityIds": [data["newrelic_application"]["my_application"]["application_id"]],
                    "metrics": [{
                        "name": "Apdex",
                        "values": ["score"],
                    }],
                    "facet": "host",
                    "limit": 5,
                    "orderBy": "score",
                    "row": 2,
                    "column": 1,
                },
                {
                    "title": "Requests per minute, by transaction",
                    "visualization": "facet_table",
                    "nrql": "SELECT rate(count(*), 1 minute) FROM Transaction FACET name",
                    "row": 2,
                    "column": 2,
                },
                {
                    "title": "Dashboard Note",
                    "visualization": "markdown",
                    "source": \"\"\"### Helpful Links

        * [New Relic One](https://one.newrelic.com)
        * [Developer Portal](https://developer.newrelic.com)\"\"\",
                    "row": 2,
                    "column": 3,
                },
            ])
        ```
        ## Attribute Refence

        In addition to all arguments above, the following attributes are exported:

          * `dashboard_url` - The URL for viewing the dashboard.

        ### Nested `widget` blocks

        All nested `widget` blocks support the following common arguments:

          * `title` - (Required) A title for the widget.
          * `visualization` - (Required) How the widget visualizes data.  Valid values are `billboard`, `gauge`, `billboard_comparison`, `facet_bar_chart`, `faceted_line_chart`, `facet_pie_chart`, `facet_table`, `faceted_area_chart`, `heatmap`, `attribute_sheet`, `single_event`, `histogram`, `funnel`, `raw_json`, `event_feed`, `event_table`, `uniques_list`, `line_chart`, `comparison_line_chart`, `markdown`, and `metric_line_chart`.
          * `row` - (Required) Row position of widget from top left, starting at `1`.
          * `column` - (Required) Column position of widget from top left, starting at `1`.
          * `width` - (Optional) Width of the widget.  Valid values are `1` to `3` inclusive.  Defaults to `1`.
          * `height` - (Optional) Height of the widget.  Valid values are `1` to `3` inclusive.  Defaults to `1`.
          * `notes` - (Optional) Description of the widget.

        Each `visualization` type supports an additional set of arguments:

          * `billboard`, `billboard_comparison`:
            * `nrql` - (Required) Valid NRQL query string. See [Writing NRQL Queries](https://docs.newrelic.com/docs/insights/nrql-new-relic-query-language/using-nrql/introduction-nrql) for help.
            * `threshold_red` - (Optional) Threshold above which the displayed value will be styled with a red color.
            * `threshold_yellow` - (Optional) Threshold above which the displayed value will be styled with a yellow color.
          * `gauge`:
            * `nrql` - (Required) Valid NRQL query string. See [Writing NRQL Queries](https://docs.newrelic.com/docs/insights/nrql-new-relic-query-language/using-nrql/introduction-nrql) for help.
            * `threshold_red` - (Required) Threshold above which the displayed value will be styled with a red color.
            * `threshold_yellow` - (Optional) Threshold above which the displayed value will be styled with a yellow color.
          * `facet_bar_chart`, `facet_pie_chart`, `facet_table`, `faceted_area_chart`, `faceted_line_chart`, or `heatmap`:
            * `nrql` - (Required) Valid NRQL query string. See [Writing NRQL Queries](https://docs.newrelic.com/docs/insights/nrql-new-relic-query-language/using-nrql/introduction-nrql) for help.
            * `drilldown_dashboard_id` - (Optional) The ID of a dashboard to link to from the widget's facets.
          * `attribute_sheet`, `comparison_line_chart`, `event_feed`, `event_table`, `funnel`, `histogram`, `line_chart`, `raw_json`, `single_event`, or `uniques_list`:
            * `nrql` - (Required) Valid NRQL query string. See [Writing NRQL Queries](https://docs.newrelic.com/docs/insights/nrql-new-relic-query-language/using-nrql/introduction-nrql) for help.
          * `markdown`:
            * `source` - (Required) The markdown source to be rendered in the widget.
          * `metric_line_chart`:
            * `entity_ids` - (Required) A collection of entity ids to display data for.  These are typically application IDs.
            * `metric` - (Required) A nested block that describes a metric.  Nested `metric` blocks support the following arguments:
              * `name` - (Required) The metric name to display.
              * `values` - (Required) The metric values to display.
            * `duration` - (Required) The duration, in ms, of the time window represented in the chart.
            * `end_time` - (Optional) The end time of the time window represented in the chart in epoch time.  When not set, the time window will end at the current time.
            * `facet` - (Optional) Can be set to "host" to facet the metric data by host.
            * `limit` - (Optional) The limit of distinct data series to display.  Requires `order_by` to be set.
            * `order_by` - (Optional) Set the order of the results.  Required when using `limit`.
          * `application_breakdown`:
            * `entity_ids` - (Required) A collection of entity IDs to display data. These are typically application IDs.

        ### Nested `filter` block

        The optional filter block supports the following arguments:
          * `event_types` - (Optional) A list of event types to enable filtering for.
          * `attributes` - (Optional) A list of attributes belonging to the specified event types to enable filtering for.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] editable: Determines who can edit the dashboard in an account. Valid values are `all`,  `editable_by_all`, `editable_by_owner`, or `read_only`.  Defaults to `editable_by_all`.
        :param pulumi.Input[dict] filter: A nested block that describes a dashboard filter.  Exactly one nested `filter` block is allowed. See Nested filter block below for details.
        :param pulumi.Input[float] grid_column_count: The number of columns to use when organizing and displaying widgets. New Relic One supports a 3 column grid and a 12 column grid. New Relic Insights supports a 3 column grid.
        :param pulumi.Input[str] icon: The icon for the dashboard.  Valid values are `adjust`, `archive`, `bar-chart`, `bell`, `bolt`, `bug`, `bullhorn`, `bullseye`, `clock-o`, `cloud`, `cog`, `comments-o`, `crosshairs`, `dashboard`, `envelope`, `fire`, `flag`, `flask`, `globe`, `heart`, `leaf`, `legal`, `life-ring`, `line-chart`, `magic`, `mobile`, `money`, `none`, `paper-plane`, `pie-chart`, `puzzle-piece`, `road`, `rocket`, `shopping-cart`, `sitemap`, `sliders`, `tablet`, `thumbs-down`, `thumbs-up`, `trophy`, `usd`, `user`, and `users`.  Defaults to `bar-chart`.
        :param pulumi.Input[str] title: The title of the dashboard.
        :param pulumi.Input[str] visibility: Determines who can see the dashboard in an account. Valid values are `all` or `owner`.  Defaults to `all`.
        :param pulumi.Input[list] widgets: A nested block that describes a visualization.  Up to 300 `widget` blocks are allowed in a dashboard definition.  See Nested widget blocks below for details.

        The **filter** object supports the following:

          * `attributes` (`pulumi.Input[list]`)
          * `eventTypes` (`pulumi.Input[list]`)

        The **widgets** object supports the following:

          * `column` (`pulumi.Input[float]`)
          * `compareWiths` (`pulumi.Input[list]`)
            * `offsetDuration` (`pulumi.Input[str]`)
            * `presentation` (`pulumi.Input[dict]`)
              * `color` (`pulumi.Input[str]`)
              * `name` (`pulumi.Input[str]`)

          * `drilldownDashboardId` (`pulumi.Input[float]`)
          * `duration` (`pulumi.Input[float]`)
          * `endTime` (`pulumi.Input[float]`)
          * `entityIds` (`pulumi.Input[list]`)
          * `facet` (`pulumi.Input[str]`)
          * `height` (`pulumi.Input[float]`)
          * `limit` (`pulumi.Input[float]`)
          * `metrics` (`pulumi.Input[list]`)
            * `name` (`pulumi.Input[str]`)
            * `scope` (`pulumi.Input[str]`)
            * `units` (`pulumi.Input[str]`)
            * `values` (`pulumi.Input[list]`)

          * `notes` (`pulumi.Input[str]`)
          * `nrql` (`pulumi.Input[str]`)
          * `orderBy` (`pulumi.Input[str]`)
          * `rawMetricName` (`pulumi.Input[str]`)
          * `row` (`pulumi.Input[float]`)
          * `source` (`pulumi.Input[str]`)
          * `thresholdRed` (`pulumi.Input[float]`)
          * `thresholdYellow` (`pulumi.Input[float]`)
          * `title` (`pulumi.Input[str]`) - The title of the dashboard.
          * `visualization` (`pulumi.Input[str]`)
          * `widgetId` (`pulumi.Input[float]`)
          * `width` (`pulumi.Input[float]`)
        """
        if __name__ is not None:
            warnings.warn("explicit use of __name__ is deprecated", DeprecationWarning)
            resource_name = __name__
        if __opts__ is not None:
            warnings.warn("explicit use of __opts__ is deprecated, use 'opts' instead", DeprecationWarning)
            opts = __opts__
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = dict()

            __props__['editable'] = editable
            __props__['filter'] = filter
            __props__['grid_column_count'] = grid_column_count
            __props__['icon'] = icon
            if title is None:
                raise TypeError("Missing required property 'title'")
            __props__['title'] = title
            __props__['visibility'] = visibility
            __props__['widgets'] = widgets
            __props__['dashboard_url'] = None
        super(Dashboard, __self__).__init__(
            'newrelic:index/dashboard:Dashboard',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, dashboard_url=None, editable=None, filter=None, grid_column_count=None, icon=None, title=None, visibility=None, widgets=None):
        """
        Get an existing Dashboard resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] dashboard_url: The URL for viewing the dashboard.
        :param pulumi.Input[str] editable: Determines who can edit the dashboard in an account. Valid values are `all`,  `editable_by_all`, `editable_by_owner`, or `read_only`.  Defaults to `editable_by_all`.
        :param pulumi.Input[dict] filter: A nested block that describes a dashboard filter.  Exactly one nested `filter` block is allowed. See Nested filter block below for details.
        :param pulumi.Input[float] grid_column_count: The number of columns to use when organizing and displaying widgets. New Relic One supports a 3 column grid and a 12 column grid. New Relic Insights supports a 3 column grid.
        :param pulumi.Input[str] icon: The icon for the dashboard.  Valid values are `adjust`, `archive`, `bar-chart`, `bell`, `bolt`, `bug`, `bullhorn`, `bullseye`, `clock-o`, `cloud`, `cog`, `comments-o`, `crosshairs`, `dashboard`, `envelope`, `fire`, `flag`, `flask`, `globe`, `heart`, `leaf`, `legal`, `life-ring`, `line-chart`, `magic`, `mobile`, `money`, `none`, `paper-plane`, `pie-chart`, `puzzle-piece`, `road`, `rocket`, `shopping-cart`, `sitemap`, `sliders`, `tablet`, `thumbs-down`, `thumbs-up`, `trophy`, `usd`, `user`, and `users`.  Defaults to `bar-chart`.
        :param pulumi.Input[str] title: The title of the dashboard.
        :param pulumi.Input[str] visibility: Determines who can see the dashboard in an account. Valid values are `all` or `owner`.  Defaults to `all`.
        :param pulumi.Input[list] widgets: A nested block that describes a visualization.  Up to 300 `widget` blocks are allowed in a dashboard definition.  See Nested widget blocks below for details.

        The **filter** object supports the following:

          * `attributes` (`pulumi.Input[list]`)
          * `eventTypes` (`pulumi.Input[list]`)

        The **widgets** object supports the following:

          * `column` (`pulumi.Input[float]`)
          * `compareWiths` (`pulumi.Input[list]`)
            * `offsetDuration` (`pulumi.Input[str]`)
            * `presentation` (`pulumi.Input[dict]`)
              * `color` (`pulumi.Input[str]`)
              * `name` (`pulumi.Input[str]`)

          * `drilldownDashboardId` (`pulumi.Input[float]`)
          * `duration` (`pulumi.Input[float]`)
          * `endTime` (`pulumi.Input[float]`)
          * `entityIds` (`pulumi.Input[list]`)
          * `facet` (`pulumi.Input[str]`)
          * `height` (`pulumi.Input[float]`)
          * `limit` (`pulumi.Input[float]`)
          * `metrics` (`pulumi.Input[list]`)
            * `name` (`pulumi.Input[str]`)
            * `scope` (`pulumi.Input[str]`)
            * `units` (`pulumi.Input[str]`)
            * `values` (`pulumi.Input[list]`)

          * `notes` (`pulumi.Input[str]`)
          * `nrql` (`pulumi.Input[str]`)
          * `orderBy` (`pulumi.Input[str]`)
          * `rawMetricName` (`pulumi.Input[str]`)
          * `row` (`pulumi.Input[float]`)
          * `source` (`pulumi.Input[str]`)
          * `thresholdRed` (`pulumi.Input[float]`)
          * `thresholdYellow` (`pulumi.Input[float]`)
          * `title` (`pulumi.Input[str]`) - The title of the dashboard.
          * `visualization` (`pulumi.Input[str]`)
          * `widgetId` (`pulumi.Input[float]`)
          * `width` (`pulumi.Input[float]`)
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["dashboard_url"] = dashboard_url
        __props__["editable"] = editable
        __props__["filter"] = filter
        __props__["grid_column_count"] = grid_column_count
        __props__["icon"] = icon
        __props__["title"] = title
        __props__["visibility"] = visibility
        __props__["widgets"] = widgets
        return Dashboard(resource_name, opts=opts, __props__=__props__)

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop
