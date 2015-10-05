'''
Copyright (c) 2015 Will Dietz

plugin_pipeline

Pelican plugin that takes a list of 'plugins' and runs them
in the specified order consistently.

Defines new plugin interface, 'process' and 'initialized'.

The entire pipeline is executed after the signal for
'all_generators_finalized' has fired.  This is where pelican
currently recommends to run plugins that read or modify
content/summary information.

The reason this is needed is because pelican doesn't give us a way
to force plugins to run in a particular order, such as the various
plugins I have that run after a summary is computed for each article.

Anyway, YMMV and such :).
'''

import logging
import sys

from pelican import signals
from pelican.generators import ArticlesGenerator, PagesGenerator

PIPELINE_SETTING_KEY = 'PLUGIN_PIPELINE'

logger = logging.getLogger(__name__)

# Global (eep) list of plugins used in the processing pipeline
# XXX: Tie this to an appropriate context object for scope/lifetime
plugin_pipeline = []


def run_plugins(generators):
    logger.debug('[PP] Running plugin pipeline...')
    for stage in plugin_pipeline:
        logger.debug('[PP] Pipeline stage: `%s`', stage.__name__)
        for generator in generators:
            if isinstance(generator, ArticlesGenerator):
                for article in generator.articles:
                    stage.process(article)
            elif isinstance(generator, PagesGenerator):
                for page in generator.pages:
                    stage.process(page)


def build_pipeline(stages, plugin_paths):
    # Plugin loading logic taken from pelican source,
    # only we don't call 'register()' and only handle strings.
    plugins = []
    logger.debug('[PP] Temporarily adding PLUGIN_PATHS to system path')
    _sys_path = sys.path[:]
    for pluginpath in plugin_paths:
        sys.path.insert(0, pluginpath)
    for plugin in stages:
        logger.debug('[PP] Loading plugin `%s`', plugin)
        try:
            plugin = __import__(plugin, globals(), locals(),
                                str('module'))
        except ImportError as e:
            logger.error('[PP] Cannot load plugin `%s`\n%s', plugin, e)
            continue

        plugins.append(plugin)
    logger.debug('[PP] Restoring system path')
    sys.path = _sys_path
    return plugins


def initialized(pelican):
    if not pelican:
        raise Exception("No 'pelican' object found, when does this happen??")
    if PIPELINE_SETTING_KEY not in pelican.settings:
        raise Exception('No value found for "' + PIPELINE_SETTING_KEY +
                        '" in config!')

    stages = pelican.settings[PIPELINE_SETTING_KEY]
    logger.debug('[PP] Loading modules in pipeline: %s', stages)

    plugin_paths = pelican.settings['PLUGIN_PATHS']
    global plugin_pipeline
    plugin_pipeline = build_pipeline(stages, plugin_paths)

    # Give plugins chance to initialize if they implement 'initialized':
    logger.debug('[PP] Initializing plugins...')
    for stage in plugin_pipeline:
        if hasattr(stage, 'initialized'):
            logger.debug('[PP] Initializing plugin `%s`', stage.__name__)
            stage.initialized(pelican)
        else:
            logger.debug('[PP] Plugin `%s` has no initializer, skipping...',
                         stage.__name__)


def register():
    signals.initialized.connect(initialized)
    signals.all_generators_finalized.connect(run_plugins)
