# Copyright (c) 2019 Microsoft Corporation
# Distributed under the MIT software license

from .dashboard import AppRunner
import sys

import logging
log = logging.getLogger(__name__)

this = sys.modules[__name__]
this.app_runner = None


def show(explanation, share_tables=None):
    try:
        # Initialize server if needed
        if this.app_runner is None:
            log.debug('Create app runner.')
            this.app_runner = AppRunner()
            this.app_runner.start()

        log.debug('Running existing app runner.')

        # Register
        this.app_runner.register(explanation, share_tables=share_tables)

        # Display
        open_link = isinstance(explanation, list)
        this.app_runner.display(explanation, open_link=open_link)
    except Exception as e:
        log.error(e, exc_info=True)
        raise e


def old_show(explanation, selector=None, index_map=None):
    from plotly.offline import iplot, init_notebook_mode
    init_notebook_mode(connected=True)
    # if not show.imported:
    #     show.imported = True

    if isinstance(selector, str):
        if index_map is None:
            print(
                "If selector is a string, a list or dictionary index_map must be passed.")
        if isinstance(index_map, list):
            selector = index_map.index(selector)
        elif isinstance(index_map, dict):
            selector = index_map[selector]
        else:
            print(
                "Not supported index_feature_map type. Use list or dictionary.")
            return None
    elif isinstance(selector, int):
        selector = selector
    elif selector is None:
        selector = None
    else:
        print("Argument 'selector' must be an int, string, or None.")
        return None

    fig = explanation.visualize(selector)
    if fig is not None:
        iplot(fig)
    else:
        print(
            "No overall graph for this explanation. Pass in a selector.")

# show.imported = False
