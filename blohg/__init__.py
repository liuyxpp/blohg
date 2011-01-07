# -*- coding: utf-8 -*-
"""
    blohg
    ~~~~~
    
    Main package.
    
    :copyright: (c) 2010-2011 by Rafael Goncalves Martins
    :license: GPL-2, see LICENSE for more details.
"""

import re

from flask import Flask, request, abort, render_template
from flaskext.babel import Babel

# import blohg stuff
from blohg.filters import rst2html, tag_name, append_title
from blohg.mercurial_content import setup_mercurial
from blohg.mercurial_theme import setup_theme
from blohg.version import version as __version__

# import blohg views
from blohg.views.atom import atom
from blohg.views.pages import pages
from blohg.views.posts import posts
from blohg.views.robots import robots
from blohg.views.sources import sources


# default locale (en_US)
_en_us_locale = {
    'locale': 'en_US',
    'name': 'English',
}


def create_app(repo_path=None):
    """Application factory.
    
    :param repo_path: the path to the mercurial repository.
    :return: the WSGI application (Flask instance).
    """
    
    # create the app object
    app = Flask(__name__)
    
    # register some sane default config values
    app.config.setdefault('AUTHOR', 'Your Name Here')
    app.config.setdefault('LOCALES', {'en-us': _en_us_locale})
    app.config.setdefault('MENU', {'en_US': []})
    app.config.setdefault('POSTS_PER_PAGE', 10)
    app.config.setdefault('REPO_PATH', repo_path)
    app.config.setdefault('SIDEBAR', {'en_US': []})
    app.config.setdefault('TAGLINE', {'en_US': u'Your cool tagline'})
    app.config.setdefault('TAGS', {})
    app.config.setdefault('TITLE', {'en_US': u'Your title'})
    app.config.setdefault('TITLE_HTML', {'en_US': u'Your HTML title'})
    app.config.setdefault('TEMPLATES_DIR', 'templates')
    app.config.setdefault('STATIC_DIR', 'static')
    
    # init mercurial stuff
    setup_mercurial(app)
    
    # setup extensions
    babel = Babel(app)
    setup_theme(app)
    
    # setup jinja2 filters
    app.jinja_env.filters.update(
        rst2html = rst2html,
        tag_name = tag_name,
        append_title = append_title,
    )
    
    def my_locale():
        match = re.match(r'/([^/]+).*', request.path)
        if match is not None:
            return match.group(1)
        return 'en-us'
    
    def current_path():
        match = re.match(r'/[^/]+/(.+)/', request.path)
        if match is not None:
            return match.group(1)
        return ''
    
    def active_page():
        return current_path().split('/')[0]
    
    def localized_config(key):
        config = app.config.get(key, None)
        if config is None:
            return None
        locale = get_locale()
        if locale in config:
            return config[locale]
        if type(config) == dict:
            values = config.values()
            if len(values) > 0:
                return config.values()[0]
            return None
        return config
    app.localized_config = localized_config
    
    @app.context_processor
    def setup_jinja2():
        return dict(
            version = __version__,
            localized_config = localized_config,
            is_post = lambda x: x.startswith('post/'),
            my_locale = my_locale(),
            current_path = current_path(),
            active_page = active_page(),
            tags = app.hg.get_tags(my_locale()),
        )

    @babel.localeselector
    def get_locale():
        return app.config['LOCALES'].get(my_locale(), _en_us_locale)['locale']
    
    @babel.timezoneselector
    def get_timezone():
        return localized_config('TIMEZONE')
    
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html'), 404
    
    app.register_module(robots)
    app.register_module(sources)
    app.register_module(posts)
    app.register_module(pages)
    app.register_module(atom)
    
    return app
