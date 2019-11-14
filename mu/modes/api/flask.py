"""
Contains definitions for Python 3 APIs so they can be used in the editor for
autocomplete and call tips.

Copyright (c) 2015-2017 Nicholas H.Tollervey and others (see the AUTHORS file).

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""


FLASK_APIS = [
    _(
        "AppContext(app) \nThe application context binds an application object implicitly\nto the current thread or greenlet, similar to how the\nRequestContext binds request information.  The application\ncontext is also implicitly created if a request context is created\nbut the application is not on top of the individual application\ncontext.\n\n"
    ),
    _(
        "AppContext(app) \nThe application context binds an application object implicitly\nto the current thread or greenlet, similar to how the\nRequestContext binds request information.  The application\ncontext is also implicitly created if a request context is created\nbut the application is not on top of the individual application\ncontext.\n\n"
    ),
    _("AppContext.pop(exc=&lt;object object&gt;) \nPops the app context.\n"),
    _("AppContext.pop(exc=&lt;object object&gt;) \nPops the app context.\n"),
    _("AppContext.push() \nBinds the app context to the current context.\n"),
    _("AppContext.push() \nBinds the app context to the current context.\n"),
    _(
        "AppGroup(name=None, commands=None, **attrs) \nThis works similar to a regular click Group but it\nchanges the behavior of the command() decorator so that it\nautomatically wraps the functions in with_appcontext().\n\nNot to be confused with FlaskGroup.\n\n"
    ),
    _(
        "AppGroup(name=None, commands=None, **attrs) \nThis works similar to a regular click Group but it\nchanges the behavior of the command() decorator so that it\nautomatically wraps the functions in with_appcontext().\n\nNot to be confused with FlaskGroup.\n\n"
    ),
    _(
        "AppGroup.command(*args, **kwargs) \nThis works exactly like the method of the same name on a regular\nclick.Group but it wraps callbacks in with_appcontext()\nunless it’s disabled by passing with_appcontext=False.\n"
    ),
    _(
        "AppGroup.command(*args, **kwargs) \nThis works exactly like the method of the same name on a regular\nclick.Group but it wraps callbacks in with_appcontext()\nunless it’s disabled by passing with_appcontext=False.\n"
    ),
    _(
        "AppGroup.group(*args, **kwargs) \nThis works exactly like the method of the same name on a regular\nclick.Group but it defaults the group class to\nAppGroup.\n"
    ),
    _(
        "AppGroup.group(*args, **kwargs) \nThis works exactly like the method of the same name on a regular\nclick.Group but it defaults the group class to\nAppGroup.\n"
    ),
    _(
        "Blueprint(name, import_name, static_folder=None, static_url_path=None, template_folder=None, url_prefix=None, subdomain=None, url_defaults=None, root_path=None) \nRepresents a blueprint.  A blueprint is an object that records\nfunctions that will be called with the\nBlueprintSetupState later to register functions\nor other things on the main application.  See Modular Applications with Blueprints for more\ninformation.\n\n"
    ),
    _(
        "Blueprint(name, import_name, static_folder=None, static_url_path=None, template_folder=None, url_prefix=None, subdomain=None, url_defaults=None, root_path=None) \nRepresents a blueprint.  A blueprint is an object that records\nfunctions that will be called with the\nBlueprintSetupState later to register functions\nor other things on the main application.  See Modular Applications with Blueprints for more\ninformation.\n\n"
    ),
    _(
        "Blueprint.add_app_template_filter(f, name=None) \nRegister a custom template filter, available application wide.  Like\nFlask.add_template_filter() but for a blueprint.  Works exactly\nlike the app_template_filter() decorator.\n\n\n\n\nParameters:name -- the optional name of the filter, otherwise the\nfunction name will be used.\n\n\n\n"
    ),
    _(
        "Blueprint.add_app_template_filter(f, name=None) \nRegister a custom template filter, available application wide.  Like\nFlask.add_template_filter() but for a blueprint.  Works exactly\nlike the app_template_filter() decorator.\n\n\n\n\nParameters:name -- the optional name of the filter, otherwise the\nfunction name will be used.\n\n\n\n"
    ),
    _(
        "Blueprint.add_app_template_global(f, name=None) \nRegister a custom template global, available application wide.  Like\nFlask.add_template_global() but for a blueprint.  Works exactly\nlike the app_template_global() decorator.\n\nChangelog\nNew in version 0.10.\n\n\n\n\n\nParameters:name -- the optional name of the global, otherwise the\nfunction name will be used.\n\n\n\n"
    ),
    _(
        "Blueprint.add_app_template_global(f, name=None) \nRegister a custom template global, available application wide.  Like\nFlask.add_template_global() but for a blueprint.  Works exactly\nlike the app_template_global() decorator.\n\nChangelog\nNew in version 0.10.\n\n\n\n\n\nParameters:name -- the optional name of the global, otherwise the\nfunction name will be used.\n\n\n\n"
    ),
    _(
        "Blueprint.add_app_template_test(f, name=None) \nRegister a custom template test, available application wide.  Like\nFlask.add_template_test() but for a blueprint.  Works exactly\nlike the app_template_test() decorator.\n\nChangelog\nNew in version 0.10.\n\n\n\n\n\nParameters:name -- the optional name of the test, otherwise the\nfunction name will be used.\n\n\n\n"
    ),
    _(
        "Blueprint.add_app_template_test(f, name=None) \nRegister a custom template test, available application wide.  Like\nFlask.add_template_test() but for a blueprint.  Works exactly\nlike the app_template_test() decorator.\n\nChangelog\nNew in version 0.10.\n\n\n\n\n\nParameters:name -- the optional name of the test, otherwise the\nfunction name will be used.\n\n\n\n"
    ),
    _(
        "Blueprint.add_url_rule(rule, endpoint=None, view_func=None, **options) \nLike Flask.add_url_rule() but for a blueprint.  The endpoint for\nthe url_for() function is prefixed with the name of the blueprint.\n"
    ),
    _(
        "Blueprint.add_url_rule(rule, endpoint=None, view_func=None, **options) \nLike Flask.add_url_rule() but for a blueprint.  The endpoint for\nthe url_for() function is prefixed with the name of the blueprint.\n"
    ),
    _(
        "Blueprint.after_app_request(f) \nLike Flask.after_request() but for a blueprint.  Such a function\nis executed after each request, even if outside of the blueprint.\n"
    ),
    _(
        "Blueprint.after_app_request(f) \nLike Flask.after_request() but for a blueprint.  Such a function\nis executed after each request, even if outside of the blueprint.\n"
    ),
    _(
        "Blueprint.after_request(f) \nLike Flask.after_request() but for a blueprint.  This function\nis only executed after each request that is handled by a function of\nthat blueprint.\n"
    ),
    _(
        "Blueprint.after_request(f) \nLike Flask.after_request() but for a blueprint.  This function\nis only executed after each request that is handled by a function of\nthat blueprint.\n"
    ),
    _(
        "Blueprint.app_context_processor(f) \nLike Flask.context_processor() but for a blueprint.  Such a\nfunction is executed each request, even if outside of the blueprint.\n"
    ),
    _(
        "Blueprint.app_context_processor(f) \nLike Flask.context_processor() but for a blueprint.  Such a\nfunction is executed each request, even if outside of the blueprint.\n"
    ),
    _(
        "Blueprint.app_errorhandler(code) \nLike Flask.errorhandler() but for a blueprint.  This\nhandler is used for all requests, even if outside of the blueprint.\n"
    ),
    _(
        "Blueprint.app_errorhandler(code) \nLike Flask.errorhandler() but for a blueprint.  This\nhandler is used for all requests, even if outside of the blueprint.\n"
    ),
    _(
        "Blueprint.app_template_filter(name=None) \nRegister a custom template filter, available application wide.  Like\nFlask.template_filter() but for a blueprint.\n\n\n\n\nParameters:name -- the optional name of the filter, otherwise the\nfunction name will be used.\n\n\n\n"
    ),
    _(
        "Blueprint.app_template_filter(name=None) \nRegister a custom template filter, available application wide.  Like\nFlask.template_filter() but for a blueprint.\n\n\n\n\nParameters:name -- the optional name of the filter, otherwise the\nfunction name will be used.\n\n\n\n"
    ),
    _(
        "Blueprint.app_template_global(name=None) \nRegister a custom template global, available application wide.  Like\nFlask.template_global() but for a blueprint.\n\nChangelog\nNew in version 0.10.\n\n\n\n\n\nParameters:name -- the optional name of the global, otherwise the\nfunction name will be used.\n\n\n\n"
    ),
    _(
        "Blueprint.app_template_global(name=None) \nRegister a custom template global, available application wide.  Like\nFlask.template_global() but for a blueprint.\n\nChangelog\nNew in version 0.10.\n\n\n\n\n\nParameters:name -- the optional name of the global, otherwise the\nfunction name will be used.\n\n\n\n"
    ),
    _(
        "Blueprint.app_template_test(name=None) \nRegister a custom template test, available application wide.  Like\nFlask.template_test() but for a blueprint.\n\nChangelog\nNew in version 0.10.\n\n\n\n\n\nParameters:name -- the optional name of the test, otherwise the\nfunction name will be used.\n\n\n\n"
    ),
    _(
        "Blueprint.app_template_test(name=None) \nRegister a custom template test, available application wide.  Like\nFlask.template_test() but for a blueprint.\n\nChangelog\nNew in version 0.10.\n\n\n\n\n\nParameters:name -- the optional name of the test, otherwise the\nfunction name will be used.\n\n\n\n"
    ),
    _(
        "Blueprint.app_url_defaults(f) \nSame as url_defaults() but application wide.\n"
    ),
    _(
        "Blueprint.app_url_defaults(f) \nSame as url_defaults() but application wide.\n"
    ),
    _(
        "Blueprint.app_url_value_preprocessor(f) \nSame as url_value_preprocessor() but application wide.\n"
    ),
    _(
        "Blueprint.app_url_value_preprocessor(f) \nSame as url_value_preprocessor() but application wide.\n"
    ),
    _(
        "Blueprint.before_app_first_request(f) \nLike Flask.before_first_request().  Such a function is\nexecuted before the first request to the application.\n"
    ),
    _(
        "Blueprint.before_app_first_request(f) \nLike Flask.before_first_request().  Such a function is\nexecuted before the first request to the application.\n"
    ),
    _(
        "Blueprint.before_app_request(f) \nLike Flask.before_request().  Such a function is executed\nbefore each request, even if outside of a blueprint.\n"
    ),
    _(
        "Blueprint.before_app_request(f) \nLike Flask.before_request().  Such a function is executed\nbefore each request, even if outside of a blueprint.\n"
    ),
    _(
        "Blueprint.before_request(f) \nLike Flask.before_request() but for a blueprint.  This function\nis only executed before each request that is handled by a function of\nthat blueprint.\n"
    ),
    _(
        "Blueprint.before_request(f) \nLike Flask.before_request() but for a blueprint.  This function\nis only executed before each request that is handled by a function of\nthat blueprint.\n"
    ),
    _(
        "Blueprint.context_processor(f) \nLike Flask.context_processor() but for a blueprint.  This\nfunction is only executed for requests handled by a blueprint.\n"
    ),
    _(
        "Blueprint.context_processor(f) \nLike Flask.context_processor() but for a blueprint.  This\nfunction is only executed for requests handled by a blueprint.\n"
    ),
    _(
        "Blueprint.endpoint(endpoint) \nLike Flask.endpoint() but for a blueprint.  This does not\nprefix the endpoint with the blueprint name, this has to be done\nexplicitly by the user of this method.  If the endpoint is prefixed\nwith a . it will be registered to the current blueprint, otherwise\nit’s an application independent endpoint.\n"
    ),
    _(
        "Blueprint.endpoint(endpoint) \nLike Flask.endpoint() but for a blueprint.  This does not\nprefix the endpoint with the blueprint name, this has to be done\nexplicitly by the user of this method.  If the endpoint is prefixed\nwith a . it will be registered to the current blueprint, otherwise\nit’s an application independent endpoint.\n"
    ),
    _(
        "Blueprint.errorhandler(code_or_exception) \nRegisters an error handler that becomes active for this blueprint\nonly.  Please be aware that routing does not happen local to a\nblueprint so an error handler for 404 usually is not handled by\na blueprint unless it is caused inside a view function.  Another\nspecial case is the 500 internal server error which is always looked\nup from the application.\nOtherwise works as the errorhandler() decorator\nof the Flask object.\n"
    ),
    _(
        "Blueprint.errorhandler(code_or_exception) \nRegisters an error handler that becomes active for this blueprint\nonly.  Please be aware that routing does not happen local to a\nblueprint so an error handler for 404 usually is not handled by\na blueprint unless it is caused inside a view function.  Another\nspecial case is the 500 internal server error which is always looked\nup from the application.\nOtherwise works as the errorhandler() decorator\nof the Flask object.\n"
    ),
    _(
        "Blueprint.get_send_file_max_age(filename) \nProvides default cache_timeout for the send_file() functions.\nBy default, this function returns SEND_FILE_MAX_AGE_DEFAULT from\nthe configuration of current_app.\nStatic file functions such as send_from_directory() use this\nfunction, and send_file() calls this function on\ncurrent_app when the given cache_timeout is None. If a\ncache_timeout is given in send_file(), that timeout is used;\notherwise, this method is called.\nThis allows subclasses to change the behavior when sending files based\non the filename.  For example, to set the cache timeout for .js files\nto 60 seconds:\nclass MyFlask(flask.Flask):\n    def get_send_file_max_age(self, name):\n        if name.lower().endswith('.js'):\n            return 60\n        return flask.Flask.get_send_file_max_age(self, name)\n\n\n\nChangelog\nNew in version 0.9.\n\n"
    ),
    _(
        "Blueprint.get_send_file_max_age(filename) \nProvides default cache_timeout for the send_file() functions.\nBy default, this function returns SEND_FILE_MAX_AGE_DEFAULT from\nthe configuration of current_app.\nStatic file functions such as send_from_directory() use this\nfunction, and send_file() calls this function on\ncurrent_app when the given cache_timeout is None. If a\ncache_timeout is given in send_file(), that timeout is used;\notherwise, this method is called.\nThis allows subclasses to change the behavior when sending files based\non the filename.  For example, to set the cache timeout for .js files\nto 60 seconds:\nclass MyFlask(flask.Flask):\n    def get_send_file_max_age(self, name):\n        if name.lower().endswith('.js'):\n            return 60\n        return flask.Flask.get_send_file_max_age(self, name)\n\n\n\nChangelog\nNew in version 0.9.\n\n"
    ),
    _(
        "Blueprint.has_static_folder() \nThis is True if the package bound object’s container has a\nfolder for static files.\n\nChangelog\nNew in version 0.5.\n\n"
    ),
    _(
        "Blueprint.has_static_folder() \nThis is True if the package bound object’s container has a\nfolder for static files.\n\nChangelog\nNew in version 0.5.\n\n"
    ),
    _(
        "Blueprint.import_name() \nThe name of the package or module that this app belongs to. Do not\nchange this once it is set by the constructor.\n"
    ),
    _(
        "Blueprint.import_name() \nThe name of the package or module that this app belongs to. Do not\nchange this once it is set by the constructor.\n"
    ),
    _(
        "Blueprint.jinja_loader() \nThe Jinja loader for this package bound object.\n\nChangelog\nNew in version 0.5.\n\n"
    ),
    _(
        "Blueprint.jinja_loader() \nThe Jinja loader for this package bound object.\n\nChangelog\nNew in version 0.5.\n\n"
    ),
    _(
        "Blueprint.json_decoder() \nBlueprint local JSON decoder class to use.\nSet to None to use the app’s json_decoder.\n"
    ),
    _(
        "Blueprint.json_decoder() \nBlueprint local JSON decoder class to use.\nSet to None to use the app’s json_decoder.\n"
    ),
    _(
        "Blueprint.json_encoder() \nBlueprint local JSON decoder class to use.\nSet to None to use the app’s json_encoder.\n"
    ),
    _(
        "Blueprint.json_encoder() \nBlueprint local JSON decoder class to use.\nSet to None to use the app’s json_encoder.\n"
    ),
    _(
        "Blueprint.make_setup_state(app, options, first_registration=False) \nCreates an instance of BlueprintSetupState()\nobject that is later passed to the register callback functions.\nSubclasses can override this to return a subclass of the setup state.\n"
    ),
    _(
        "Blueprint.make_setup_state(app, options, first_registration=False) \nCreates an instance of BlueprintSetupState()\nobject that is later passed to the register callback functions.\nSubclasses can override this to return a subclass of the setup state.\n"
    ),
    _(
        "Blueprint.open_resource(resource, mode='rb') \nOpens a resource from the application’s resource folder.  To see\nhow this works, consider the following folder structure:\n/myapplication.py\n/schema.sql\n/static\n    /style.css\n/templates\n    /layout.html\n    /index.html\n\n\nIf you want to open the schema.sql file you would do the\nfollowing:\nwith app.open_resource('schema.sql') as f:\n    contents = f.read()\n    do_something_with(contents)\n\n\n\n\n\n\nParameters:\nresource -- the name of the resource.  To access resources within\nsubfolders use forward slashes as separator.\nmode -- resource file opening mode, default is ‘rb’.\n\n\n\n\n\n"
    ),
    _(
        "Blueprint.open_resource(resource, mode='rb') \nOpens a resource from the application’s resource folder.  To see\nhow this works, consider the following folder structure:\n/myapplication.py\n/schema.sql\n/static\n    /style.css\n/templates\n    /layout.html\n    /index.html\n\n\nIf you want to open the schema.sql file you would do the\nfollowing:\nwith app.open_resource('schema.sql') as f:\n    contents = f.read()\n    do_something_with(contents)\n\n\n\n\n\n\nParameters:\nresource -- the name of the resource.  To access resources within\nsubfolders use forward slashes as separator.\nmode -- resource file opening mode, default is ‘rb’.\n\n\n\n\n\n"
    ),
    _(
        "Blueprint.record(func) \nRegisters a function that is called when the blueprint is\nregistered on the application.  This function is called with the\nstate as argument as returned by the make_setup_state()\nmethod.\n"
    ),
    _(
        "Blueprint.record(func) \nRegisters a function that is called when the blueprint is\nregistered on the application.  This function is called with the\nstate as argument as returned by the make_setup_state()\nmethod.\n"
    ),
    _(
        "Blueprint.record_once(func) \nWorks like record() but wraps the function in another\nfunction that will ensure the function is only called once.  If the\nblueprint is registered a second time on the application, the\nfunction passed is not called.\n"
    ),
    _(
        "Blueprint.record_once(func) \nWorks like record() but wraps the function in another\nfunction that will ensure the function is only called once.  If the\nblueprint is registered a second time on the application, the\nfunction passed is not called.\n"
    ),
    _(
        "Blueprint.register(app, options, first_registration=False) \nCalled by Flask.register_blueprint() to register all views\nand callbacks registered on the blueprint with the application. Creates\na BlueprintSetupState and calls each record() callback\nwith it.\n\n\n\n\nParameters:\napp -- The application this blueprint is being registered with.\noptions -- Keyword arguments forwarded from\nregister_blueprint().\nfirst_registration -- Whether this is the first time this\nblueprint has been registered on the application.\n\n\n\n\n\n"
    ),
    _(
        "Blueprint.register(app, options, first_registration=False) \nCalled by Flask.register_blueprint() to register all views\nand callbacks registered on the blueprint with the application. Creates\na BlueprintSetupState and calls each record() callback\nwith it.\n\n\n\n\nParameters:\napp -- The application this blueprint is being registered with.\noptions -- Keyword arguments forwarded from\nregister_blueprint().\nfirst_registration -- Whether this is the first time this\nblueprint has been registered on the application.\n\n\n\n\n\n"
    ),
    _(
        "Blueprint.register_error_handler(code_or_exception, f) \nNon-decorator version of the errorhandler() error attach\nfunction, akin to the register_error_handler()\napplication-wide function of the Flask object but\nfor error handlers limited to this blueprint.\n\nChangelog\nNew in version 0.11.\n\n"
    ),
    _(
        "Blueprint.register_error_handler(code_or_exception, f) \nNon-decorator version of the errorhandler() error attach\nfunction, akin to the register_error_handler()\napplication-wide function of the Flask object but\nfor error handlers limited to this blueprint.\n\nChangelog\nNew in version 0.11.\n\n"
    ),
    _(
        "Blueprint.root_path() \nAbsolute path to the package on the filesystem. Used to look up\nresources contained in the package.\n"
    ),
    _(
        "Blueprint.root_path() \nAbsolute path to the package on the filesystem. Used to look up\nresources contained in the package.\n"
    ),
    _(
        "Blueprint.route(rule, **options) \nLike Flask.route() but for a blueprint.  The endpoint for the\nurl_for() function is prefixed with the name of the blueprint.\n"
    ),
    _(
        "Blueprint.route(rule, **options) \nLike Flask.route() but for a blueprint.  The endpoint for the\nurl_for() function is prefixed with the name of the blueprint.\n"
    ),
    _(
        "Blueprint.send_static_file(filename) \nFunction used internally to send static files from the static\nfolder to the browser.\n\nChangelog\nNew in version 0.5.\n\n"
    ),
    _(
        "Blueprint.send_static_file(filename) \nFunction used internally to send static files from the static\nfolder to the browser.\n\nChangelog\nNew in version 0.5.\n\n"
    ),
    _(
        "Blueprint.static_folder() \nThe absolute path to the configured static folder.\n"
    ),
    _(
        "Blueprint.static_folder() \nThe absolute path to the configured static folder.\n"
    ),
    _(
        "Blueprint.static_url_path() \nThe URL prefix that the static route will be registered for.\n"
    ),
    _(
        "Blueprint.static_url_path() \nThe URL prefix that the static route will be registered for.\n"
    ),
    _(
        "Blueprint.teardown_app_request(f) \nLike Flask.teardown_request() but for a blueprint.  Such a\nfunction is executed when tearing down each request, even if outside of\nthe blueprint.\n"
    ),
    _(
        "Blueprint.teardown_app_request(f) \nLike Flask.teardown_request() but for a blueprint.  Such a\nfunction is executed when tearing down each request, even if outside of\nthe blueprint.\n"
    ),
    _(
        "Blueprint.teardown_request(f) \nLike Flask.teardown_request() but for a blueprint.  This\nfunction is only executed when tearing down requests handled by a\nfunction of that blueprint.  Teardown request functions are executed\nwhen the request context is popped, even when no actual request was\nperformed.\n"
    ),
    _(
        "Blueprint.teardown_request(f) \nLike Flask.teardown_request() but for a blueprint.  This\nfunction is only executed when tearing down requests handled by a\nfunction of that blueprint.  Teardown request functions are executed\nwhen the request context is popped, even when no actual request was\nperformed.\n"
    ),
    _(
        "Blueprint.template_folder() \nLocation of the template files to be added to the template lookup.\nNone if templates should not be added.\n"
    ),
    _(
        "Blueprint.template_folder() \nLocation of the template files to be added to the template lookup.\nNone if templates should not be added.\n"
    ),
    _(
        "Blueprint.url_defaults(f) \nCallback function for URL defaults for this blueprint.  It’s called\nwith the endpoint and values and should update the values passed\nin place.\n"
    ),
    _(
        "Blueprint.url_defaults(f) \nCallback function for URL defaults for this blueprint.  It’s called\nwith the endpoint and values and should update the values passed\nin place.\n"
    ),
    _(
        "Blueprint.url_value_preprocessor(f) \nRegisters a function as URL value preprocessor for this\nblueprint.  It’s called before the view functions are called and\ncan modify the url values provided.\n"
    ),
    _(
        "Blueprint.url_value_preprocessor(f) \nRegisters a function as URL value preprocessor for this\nblueprint.  It’s called before the view functions are called and\ncan modify the url values provided.\n"
    ),
    _(
        "BlueprintSetupState(blueprint, app, options, first_registration) \nTemporary holder object for registering a blueprint with the\napplication.  An instance of this class is created by the\nmake_setup_state() method and later passed\nto all register callback functions.\n\n"
    ),
    _(
        "BlueprintSetupState(blueprint, app, options, first_registration) \nTemporary holder object for registering a blueprint with the\napplication.  An instance of this class is created by the\nmake_setup_state() method and later passed\nto all register callback functions.\n\n"
    ),
    _(
        "BlueprintSetupState.add_url_rule(rule, endpoint=None, view_func=None, **options) \nA helper method to register a rule (and optionally a view function)\nto the application.  The endpoint is automatically prefixed with the\nblueprint’s name.\n"
    ),
    _(
        "BlueprintSetupState.add_url_rule(rule, endpoint=None, view_func=None, **options) \nA helper method to register a rule (and optionally a view function)\nto the application.  The endpoint is automatically prefixed with the\nblueprint’s name.\n"
    ),
    _("BlueprintSetupState.app() \na reference to the current application\n"),
    _("BlueprintSetupState.app() \na reference to the current application\n"),
    _(
        "BlueprintSetupState.blueprint() \na reference to the blueprint that created this setup state.\n"
    ),
    _(
        "BlueprintSetupState.blueprint() \na reference to the blueprint that created this setup state.\n"
    ),
    _(
        "BlueprintSetupState.first_registration() \nas blueprints can be registered multiple times with the\napplication and not everything wants to be registered\nmultiple times on it, this attribute can be used to figure\nout if the blueprint was registered in the past already.\n"
    ),
    _(
        "BlueprintSetupState.first_registration() \nas blueprints can be registered multiple times with the\napplication and not everything wants to be registered\nmultiple times on it, this attribute can be used to figure\nout if the blueprint was registered in the past already.\n"
    ),
    _(
        "BlueprintSetupState.options() \na dictionary with all options that were passed to the\nregister_blueprint() method.\n"
    ),
    _(
        "BlueprintSetupState.options() \na dictionary with all options that were passed to the\nregister_blueprint() method.\n"
    ),
    _(
        "BlueprintSetupState.subdomain() \nThe subdomain that the blueprint should be active for, None\notherwise.\n"
    ),
    _(
        "BlueprintSetupState.subdomain() \nThe subdomain that the blueprint should be active for, None\notherwise.\n"
    ),
    _(
        "BlueprintSetupState.url_defaults() \nA dictionary with URL defaults that is added to each and every\nURL that was defined with the blueprint.\n"
    ),
    _(
        "BlueprintSetupState.url_defaults() \nA dictionary with URL defaults that is added to each and every\nURL that was defined with the blueprint.\n"
    ),
    _(
        "BlueprintSetupState.url_prefix() \nThe prefix that should be used for all URLs defined on the\nblueprint.\n"
    ),
    _(
        "BlueprintSetupState.url_prefix() \nThe prefix that should be used for all URLs defined on the\nblueprint.\n"
    ),
    _(
        "Config(root_path, defaults=None) \nWorks exactly like a dict but provides ways to fill it from files\nor special dictionaries.  There are two common patterns to populate the\nconfig.\n\nEither you can fill the config from a config file:\n\nOr alternatively you can define the configuration options in the\nmodule that calls from_object() or provide an import path to\na module that should be loaded.  It is also possible to tell it to\nuse the same module and with that provide the configuration values\njust before the call:\n\nIn both cases (loading from any Python file or loading from modules),\nonly uppercase keys are added to the config.  This makes it possible to use\nlowercase values in the config file for temporary values that are not added\nto the config or to define the config keys in the same file that implements\nthe application.\n\nProbably the most interesting way to load configurations is from an\nenvironment variable pointing to a file:\n\nIn this case before launching the application you have to set this\nenvironment variable to the file you want to use.  On Linux and OS X\nuse the export statement:\n\nOn windows use set instead.\n\n\nParameters:\nroot_path -- path to which files are read relative from.  When the\nconfig object is created by the application, this is\nthe application’s root_path.\ndefaults -- an optional dictionary of default values"
    ),
    _(
        "Config(root_path, defaults=None) \nWorks exactly like a dict but provides ways to fill it from files\nor special dictionaries.  There are two common patterns to populate the\nconfig.\n\nEither you can fill the config from a config file:\n\nOr alternatively you can define the configuration options in the\nmodule that calls from_object() or provide an import path to\na module that should be loaded.  It is also possible to tell it to\nuse the same module and with that provide the configuration values\njust before the call:\n\nIn both cases (loading from any Python file or loading from modules),\nonly uppercase keys are added to the config.  This makes it possible to use\nlowercase values in the config file for temporary values that are not added\nto the config or to define the config keys in the same file that implements\nthe application.\n\nProbably the most interesting way to load configurations is from an\nenvironment variable pointing to a file:\n\nIn this case before launching the application you have to set this\nenvironment variable to the file you want to use.  On Linux and OS X\nuse the export statement:\n\nOn windows use set instead.\n\n\nParameters:\nroot_path -- path to which files are read relative from.  When the\nconfig object is created by the application, this is\nthe application’s root_path.\ndefaults -- an optional dictionary of default values"
    ),
    _(
        "Config.from_envvar(variable_name, silent=False) \nLoads a configuration from an environment variable pointing to\na configuration file.  This is basically just a shortcut with nicer\nerror messages for this line of code:\napp.config.from_pyfile(os.environ['YOURAPPLICATION_SETTINGS'])\n\n\n\n\n\n\nParameters:\nvariable_name -- name of the environment variable\nsilent -- set to True if you want silent failure for missing\nfiles.\n\n\n\nReturns:bool. True if able to load config, False otherwise.\n\n\n\n\n"
    ),
    _(
        "Config.from_envvar(variable_name, silent=False) \nLoads a configuration from an environment variable pointing to\na configuration file.  This is basically just a shortcut with nicer\nerror messages for this line of code:\napp.config.from_pyfile(os.environ['YOURAPPLICATION_SETTINGS'])\n\n\n\n\n\n\nParameters:\nvariable_name -- name of the environment variable\nsilent -- set to True if you want silent failure for missing\nfiles.\n\n\n\nReturns:bool. True if able to load config, False otherwise.\n\n\n\n\n"
    ),
    _(
        "Config.from_json(filename, silent=False) \nUpdates the values in the config from a JSON file. This function\nbehaves as if the JSON object was a dictionary and passed to the\nfrom_mapping() function.\n\n\n\n\nParameters:\nfilename -- the filename of the JSON file.  This can either be an\nabsolute filename or a filename relative to the\nroot path.\nsilent -- set to True if you want silent failure for missing\nfiles.\n\n\n\n\n\n\nChangelog\nNew in version 0.11.\n\n"
    ),
    _(
        "Config.from_json(filename, silent=False) \nUpdates the values in the config from a JSON file. This function\nbehaves as if the JSON object was a dictionary and passed to the\nfrom_mapping() function.\n\n\n\n\nParameters:\nfilename -- the filename of the JSON file.  This can either be an\nabsolute filename or a filename relative to the\nroot path.\nsilent -- set to True if you want silent failure for missing\nfiles.\n\n\n\n\n\n\nChangelog\nNew in version 0.11.\n\n"
    ),
    _(
        "Config.from_mapping(*mapping, **kwargs) \nUpdates the config like update() ignoring items with non-upper\nkeys.\n\nChangelog\nNew in version 0.11.\n\n"
    ),
    _(
        "Config.from_mapping(*mapping, **kwargs) \nUpdates the config like update() ignoring items with non-upper\nkeys.\n\nChangelog\nNew in version 0.11.\n\n"
    ),
    _(
        "Config.from_object(obj) \nUpdates the values from the given object.  An object can be of one\nof the following two types:\n\na string: in this case the object with that name will be imported\nan actual object reference: that object is used directly\n\nObjects are usually either modules or classes. from_object()\nloads only the uppercase attributes of the module/class. A dict\nobject will not work with from_object() because the keys of a\ndict are not attributes of the dict class.\nExample of module-based configuration:\napp.config.from_object('yourapplication.default_config')\nfrom yourapplication import default_config\napp.config.from_object(default_config)\n\n\nYou should not use this function to load the actual configuration but\nrather configuration defaults.  The actual config should be loaded\nwith from_pyfile() and ideally from a location not within the\npackage because the package might be installed system wide.\nSee Development / Production for an example of class-based configuration\nusing from_object().\n\n\n\n\nParameters:obj -- an import name or object\n\n\n\n"
    ),
    _(
        "Config.from_object(obj) \nUpdates the values from the given object.  An object can be of one\nof the following two types:\n\na string: in this case the object with that name will be imported\nan actual object reference: that object is used directly\n\nObjects are usually either modules or classes. from_object()\nloads only the uppercase attributes of the module/class. A dict\nobject will not work with from_object() because the keys of a\ndict are not attributes of the dict class.\nExample of module-based configuration:\napp.config.from_object('yourapplication.default_config')\nfrom yourapplication import default_config\napp.config.from_object(default_config)\n\n\nYou should not use this function to load the actual configuration but\nrather configuration defaults.  The actual config should be loaded\nwith from_pyfile() and ideally from a location not within the\npackage because the package might be installed system wide.\nSee Development / Production for an example of class-based configuration\nusing from_object().\n\n\n\n\nParameters:obj -- an import name or object\n\n\n\n"
    ),
    _(
        "Config.from_pyfile(filename, silent=False) \nUpdates the values in the config from a Python file.  This function\nbehaves as if the file was imported as module with the\nfrom_object() function.\n\n\n\n\nParameters:\nfilename -- the filename of the config.  This can either be an\nabsolute filename or a filename relative to the\nroot path.\nsilent -- set to True if you want silent failure for missing\nfiles.\n\n\n\n\n\n\nChangelog\nNew in version 0.7: silent parameter.\n\n"
    ),
    _(
        "Config.from_pyfile(filename, silent=False) \nUpdates the values in the config from a Python file.  This function\nbehaves as if the file was imported as module with the\nfrom_object() function.\n\n\n\n\nParameters:\nfilename -- the filename of the config.  This can either be an\nabsolute filename or a filename relative to the\nroot path.\nsilent -- set to True if you want silent failure for missing\nfiles.\n\n\n\n\n\n\nChangelog\nNew in version 0.7: silent parameter.\n\n"
    ),
    _(
        "Config.get_namespace(namespace, lowercase=True, trim_namespace=True) \nReturns a dictionary containing a subset of configuration options\nthat match the specified namespace/prefix. Example usage:\napp.config['IMAGE_STORE_TYPE'] = 'fs'\napp.config['IMAGE_STORE_PATH'] = '/var/app/images'\napp.config['IMAGE_STORE_BASE_URL'] = 'http://img.website.com'\nimage_store_config = app.config.get_namespace('IMAGE_STORE_')\n\n\nThe resulting dictionary image_store_config would look like:\n{\n    'type': 'fs',\n    'path': '/var/app/images',\n    'base_url': 'http://img.website.com'\n}\n\n\nThis is often useful when configuration options map directly to\nkeyword arguments in functions or class constructors.\n\n\n\n\nParameters:\nnamespace -- a configuration namespace\nlowercase -- a flag indicating if the keys of the resulting\ndictionary should be lowercase\ntrim_namespace -- a flag indicating if the keys of the resulting\ndictionary should not include the namespace\n\n\n\n\n\n\nChangelog\nNew in version 0.11.\n\n"
    ),
    _(
        "Config.get_namespace(namespace, lowercase=True, trim_namespace=True) \nReturns a dictionary containing a subset of configuration options\nthat match the specified namespace/prefix. Example usage:\napp.config['IMAGE_STORE_TYPE'] = 'fs'\napp.config['IMAGE_STORE_PATH'] = '/var/app/images'\napp.config['IMAGE_STORE_BASE_URL'] = 'http://img.website.com'\nimage_store_config = app.config.get_namespace('IMAGE_STORE_')\n\n\nThe resulting dictionary image_store_config would look like:\n{\n    'type': 'fs',\n    'path': '/var/app/images',\n    'base_url': 'http://img.website.com'\n}\n\n\nThis is often useful when configuration options map directly to\nkeyword arguments in functions or class constructors.\n\n\n\n\nParameters:\nnamespace -- a configuration namespace\nlowercase -- a flag indicating if the keys of the resulting\ndictionary should be lowercase\ntrim_namespace -- a flag indicating if the keys of the resulting\ndictionary should not include the namespace\n\n\n\n\n\n\nChangelog\nNew in version 0.11.\n\n"
    ),
    _(
        "Flask(import_name, static_url_path=None, static_folder='static', static_host=None, host_matching=False, subdomain_matching=False, template_folder='templates', instance_path=None, instance_relative_config=False, root_path=None) \nThe flask object implements a WSGI application and acts as the central\nobject.  It is passed the name of the module or package of the\napplication.  Once it is created it will act as a central registry for\nthe view functions, the URL rules, template configuration and much more.\n\nThe name of the package is used to resolve resources from inside the\npackage or the folder the module is contained in depending on if the\npackage parameter resolves to an actual python package (a folder with\nan __init__.py file inside) or a standard module (just a .py file).\n\nFor more information about resource loading, see open_resource().\n\nUsually you create a Flask instance in your main module or\nin the __init__.py file of your package like this:\n\n\nParameters:\nimport_name -- the name of the application package\nstatic_url_path -- can be used to specify a different path for the\nstatic files on the web.  Defaults to the name\nof the static_folder folder.\nstatic_folder -- the folder with static files that should be served\nat static_url_path.  Defaults to the 'static'\nfolder in the root path of the application.\nstatic_host -- the host to use when adding the static route.\nDefaults to None. Required when using host_matching=True\nwith a static_folder configured.\nhost_matching -- set url_map.host_matching attribute.\nDefaults to False.\nsubdomain_matching -- consider the subdomain relative to\nSERVER_NAME when matching routes. Defaults to False.\ntemplate_folder -- the folder that contains the templates that should\nbe used by the application.  Defaults to\n'templates' folder in the root path of the\napplication.\ninstance_path -- An alternative instance path for the application.\nBy default the folder 'instance' next to the\npackage or module is assumed to be the instance\npath.\ninstance_relative_config -- if set to True relative filenames\nfor loading the config are assumed to\nbe relative to the instance path instead\nof the application root.\nroot_path -- Flask by default will automatically calculate the path\nto the root of the application.  In certain situations\nthis cannot be achieved (for instance if the package\nis a Python 3 namespace package) and needs to be\nmanually defined."
    ),
    _(
        "Flask(import_name, static_url_path=None, static_folder='static', static_host=None, host_matching=False, subdomain_matching=False, template_folder='templates', instance_path=None, instance_relative_config=False, root_path=None) \nThe flask object implements a WSGI application and acts as the central\nobject.  It is passed the name of the module or package of the\napplication.  Once it is created it will act as a central registry for\nthe view functions, the URL rules, template configuration and much more.\n\nThe name of the package is used to resolve resources from inside the\npackage or the folder the module is contained in depending on if the\npackage parameter resolves to an actual python package (a folder with\nan __init__.py file inside) or a standard module (just a .py file).\n\nFor more information about resource loading, see open_resource().\n\nUsually you create a Flask instance in your main module or\nin the __init__.py file of your package like this:\n\n\nParameters:\nimport_name -- the name of the application package\nstatic_url_path -- can be used to specify a different path for the\nstatic files on the web.  Defaults to the name\nof the static_folder folder.\nstatic_folder -- the folder with static files that should be served\nat static_url_path.  Defaults to the 'static'\nfolder in the root path of the application.\nstatic_host -- the host to use when adding the static route.\nDefaults to None. Required when using host_matching=True\nwith a static_folder configured.\nhost_matching -- set url_map.host_matching attribute.\nDefaults to False.\nsubdomain_matching -- consider the subdomain relative to\nSERVER_NAME when matching routes. Defaults to False.\ntemplate_folder -- the folder that contains the templates that should\nbe used by the application.  Defaults to\n'templates' folder in the root path of the\napplication.\ninstance_path -- An alternative instance path for the application.\nBy default the folder 'instance' next to the\npackage or module is assumed to be the instance\npath.\ninstance_relative_config -- if set to True relative filenames\nfor loading the config are assumed to\nbe relative to the instance path instead\nof the application root.\nroot_path -- Flask by default will automatically calculate the path\nto the root of the application.  In certain situations\nthis cannot be achieved (for instance if the package\nis a Python 3 namespace package) and needs to be\nmanually defined."
    ),
    _(
        "Flask.add_template_filter(f, name=None) \nRegister a custom template filter.  Works exactly like the\ntemplate_filter() decorator.\n\n\n\n\nParameters:name -- the optional name of the filter, otherwise the\nfunction name will be used.\n\n\n\n"
    ),
    _(
        "Flask.add_template_filter(f, name=None) \nRegister a custom template filter.  Works exactly like the\ntemplate_filter() decorator.\n\n\n\n\nParameters:name -- the optional name of the filter, otherwise the\nfunction name will be used.\n\n\n\n"
    ),
    _(
        "Flask.add_template_global(f, name=None) \nRegister a custom template global function. Works exactly like the\ntemplate_global() decorator.\n\nChangelog\nNew in version 0.10.\n\n\n\n\n\nParameters:name -- the optional name of the global function, otherwise the\nfunction name will be used.\n\n\n\n"
    ),
    _(
        "Flask.add_template_global(f, name=None) \nRegister a custom template global function. Works exactly like the\ntemplate_global() decorator.\n\nChangelog\nNew in version 0.10.\n\n\n\n\n\nParameters:name -- the optional name of the global function, otherwise the\nfunction name will be used.\n\n\n\n"
    ),
    _(
        "Flask.add_template_test(f, name=None) \nRegister a custom template test.  Works exactly like the\ntemplate_test() decorator.\n\nChangelog\nNew in version 0.10.\n\n\n\n\n\nParameters:name -- the optional name of the test, otherwise the\nfunction name will be used.\n\n\n\n"
    ),
    _(
        "Flask.add_template_test(f, name=None) \nRegister a custom template test.  Works exactly like the\ntemplate_test() decorator.\n\nChangelog\nNew in version 0.10.\n\n\n\n\n\nParameters:name -- the optional name of the test, otherwise the\nfunction name will be used.\n\n\n\n"
    ),
    _(
        "Flask.add_url_rule(rule, endpoint=None, view_func=None, provide_automatic_options=None, **options) \nConnects a URL rule.  Works exactly like the route()\ndecorator.  If a view_func is provided it will be registered with the\nendpoint.\nBasically this example:\n@app.route('/')\ndef index():\n    pass\n\n\nIs equivalent to the following:\ndef index():\n    pass\napp.add_url_rule('/', 'index', index)\n\n\nIf the view_func is not provided you will need to connect the endpoint\nto a view function like so:\napp.view_functions['index'] = index\n\n\nInternally route() invokes add_url_rule() so if you want\nto customize the behavior via subclassing you only need to change\nthis method.\nFor more information refer to URL Route Registrations.\n\nChangelog\nChanged in version 0.6: OPTIONS is added automatically as method.\n\n\nChanged in version 0.2: view_func parameter added.\n\n\n\n\n\nParameters:\nrule -- the URL rule as string\nendpoint -- the endpoint for the registered URL rule.  Flask\nitself assumes the name of the view function as\nendpoint\nview_func -- the function to call when serving a request to the\nprovided endpoint\nprovide_automatic_options -- controls whether the OPTIONS\nmethod should be added automatically. This can also be controlled\nby setting the view_func.provide_automatic_options = False\nbefore adding the rule.\noptions -- the options to be forwarded to the underlying\nRule object.  A change\nto Werkzeug is handling of method options.  methods\nis a list of methods this rule should be limited\nto (GET, POST etc.).  By default a rule\njust listens for GET (and implicitly HEAD).\nStarting with Flask 0.6, OPTIONS is implicitly\nadded and handled by the standard request handling.\n\n\n\n\n\n"
    ),
    _(
        "Flask.add_url_rule(rule, endpoint=None, view_func=None, provide_automatic_options=None, **options) \nConnects a URL rule.  Works exactly like the route()\ndecorator.  If a view_func is provided it will be registered with the\nendpoint.\nBasically this example:\n@app.route('/')\ndef index():\n    pass\n\n\nIs equivalent to the following:\ndef index():\n    pass\napp.add_url_rule('/', 'index', index)\n\n\nIf the view_func is not provided you will need to connect the endpoint\nto a view function like so:\napp.view_functions['index'] = index\n\n\nInternally route() invokes add_url_rule() so if you want\nto customize the behavior via subclassing you only need to change\nthis method.\nFor more information refer to URL Route Registrations.\n\nChangelog\nChanged in version 0.6: OPTIONS is added automatically as method.\n\n\nChanged in version 0.2: view_func parameter added.\n\n\n\n\n\nParameters:\nrule -- the URL rule as string\nendpoint -- the endpoint for the registered URL rule.  Flask\nitself assumes the name of the view function as\nendpoint\nview_func -- the function to call when serving a request to the\nprovided endpoint\nprovide_automatic_options -- controls whether the OPTIONS\nmethod should be added automatically. This can also be controlled\nby setting the view_func.provide_automatic_options = False\nbefore adding the rule.\noptions -- the options to be forwarded to the underlying\nRule object.  A change\nto Werkzeug is handling of method options.  methods\nis a list of methods this rule should be limited\nto (GET, POST etc.).  By default a rule\njust listens for GET (and implicitly HEAD).\nStarting with Flask 0.6, OPTIONS is implicitly\nadded and handled by the standard request handling.\n\n\n\n\n\n"
    ),
    _(
        "Flask.after_request(f) \nRegister a function to be run after each request.\nYour function must take one parameter, an instance of\nresponse_class and return a new response object or the\nsame (see process_response()).\nAs of Flask 0.7 this function might not be executed at the end of the\nrequest in case an unhandled exception occurred.\n"
    ),
    _(
        "Flask.after_request(f) \nRegister a function to be run after each request.\nYour function must take one parameter, an instance of\nresponse_class and return a new response object or the\nsame (see process_response()).\nAs of Flask 0.7 this function might not be executed at the end of the\nrequest in case an unhandled exception occurred.\n"
    ),
    _(
        "Flask.after_request_funcs() \nA dictionary with lists of functions that should be called after\neach request.  The key of the dictionary is the name of the blueprint\nthis function is active for, None for all requests.  This can for\nexample be used to close database connections. To register a function\nhere, use the after_request() decorator.\n"
    ),
    _(
        "Flask.after_request_funcs() \nA dictionary with lists of functions that should be called after\neach request.  The key of the dictionary is the name of the blueprint\nthis function is active for, None for all requests.  This can for\nexample be used to close database connections. To register a function\nhere, use the after_request() decorator.\n"
    ),
    _(
        "Flask.app_context() \nCreate an AppContext. Use as a with\nblock to push the context, which will make current_app\npoint at this application.\nAn application context is automatically pushed by\nRequestContext.push()\nwhen handling a request, and when running a CLI command. Use\nthis to manually create a context outside of these situations.\nwith app.app_context():\n    init_db()\n\n\nSee The Application Context.\n\nChangelog\nNew in version 0.9.\n\n"
    ),
    _(
        "Flask.app_context() \nCreate an AppContext. Use as a with\nblock to push the context, which will make current_app\npoint at this application.\nAn application context is automatically pushed by\nRequestContext.push()\nwhen handling a request, and when running a CLI command. Use\nthis to manually create a context outside of these situations.\nwith app.app_context():\n    init_db()\n\n\nSee The Application Context.\n\nChangelog\nNew in version 0.9.\n\n"
    ),
    _("Flask.app_ctx_globals_class() \nalias of flask.ctx._AppCtxGlobals\n"),
    _("Flask.app_ctx_globals_class() \nalias of flask.ctx._AppCtxGlobals\n"),
    _(
        "Flask.auto_find_instance_path() \nTries to locate the instance path if it was not provided to the\nconstructor of the application class.  It will basically calculate\nthe path to a folder named instance next to your main file or\nthe package.\n\nChangelog\nNew in version 0.8.\n\n"
    ),
    _(
        "Flask.auto_find_instance_path() \nTries to locate the instance path if it was not provided to the\nconstructor of the application class.  It will basically calculate\nthe path to a folder named instance next to your main file or\nthe package.\n\nChangelog\nNew in version 0.8.\n\n"
    ),
    _(
        "Flask.before_first_request(f) \nRegisters a function to be run before the first request to this\ninstance of the application.\nThe function will be called without any arguments and its return\nvalue is ignored.\n\nChangelog\nNew in version 0.8.\n\n"
    ),
    _(
        "Flask.before_first_request(f) \nRegisters a function to be run before the first request to this\ninstance of the application.\nThe function will be called without any arguments and its return\nvalue is ignored.\n\nChangelog\nNew in version 0.8.\n\n"
    ),
    _(
        "Flask.before_first_request_funcs() \nA list of functions that will be called at the beginning of the\nfirst request to this instance. To register a function, use the\nbefore_first_request() decorator.\n\nChangelog\nNew in version 0.8.\n\n"
    ),
    _(
        "Flask.before_first_request_funcs() \nA list of functions that will be called at the beginning of the\nfirst request to this instance. To register a function, use the\nbefore_first_request() decorator.\n\nChangelog\nNew in version 0.8.\n\n"
    ),
    _(
        "Flask.before_request(f) \nRegisters a function to run before each request.\nFor example, this can be used to open a database connection, or to load\nthe logged in user from the session.\nThe function will be called without any arguments. If it returns a\nnon-None value, the value is handled as if it was the return value from\nthe view, and further request handling is stopped.\n"
    ),
    _(
        "Flask.before_request(f) \nRegisters a function to run before each request.\nFor example, this can be used to open a database connection, or to load\nthe logged in user from the session.\nThe function will be called without any arguments. If it returns a\nnon-None value, the value is handled as if it was the return value from\nthe view, and further request handling is stopped.\n"
    ),
    _(
        "Flask.before_request_funcs() \nA dictionary with lists of functions that will be called at the\nbeginning of each request. The key of the dictionary is the name of\nthe blueprint this function is active for, or None for all\nrequests. To register a function, use the before_request()\ndecorator.\n"
    ),
    _(
        "Flask.before_request_funcs() \nA dictionary with lists of functions that will be called at the\nbeginning of each request. The key of the dictionary is the name of\nthe blueprint this function is active for, or None for all\nrequests. To register a function, use the before_request()\ndecorator.\n"
    ),
    _(
        "Flask.blueprints() \nall the attached blueprints in a dictionary by name.  Blueprints\ncan be attached multiple times so this dictionary does not tell\nyou how often they got attached.\n\nChangelog\nNew in version 0.7.\n\n"
    ),
    _(
        "Flask.blueprints() \nall the attached blueprints in a dictionary by name.  Blueprints\ncan be attached multiple times so this dictionary does not tell\nyou how often they got attached.\n\nChangelog\nNew in version 0.7.\n\n"
    ),
    _(
        "Flask.cli() \nThe click command line context for this application.  Commands\nregistered here show up in the flask command once the\napplication has been discovered.  The default commands are\nprovided by Flask itself and can be overridden.\nThis is an instance of a click.Group object.\n"
    ),
    _(
        "Flask.cli() \nThe click command line context for this application.  Commands\nregistered here show up in the flask command once the\napplication has been discovered.  The default commands are\nprovided by Flask itself and can be overridden.\nThis is an instance of a click.Group object.\n"
    ),
    _(
        "Flask.config() \nThe configuration dictionary as Config.  This behaves\nexactly like a regular dictionary but supports additional methods\nto load a config from files.\n"
    ),
    _(
        "Flask.config() \nThe configuration dictionary as Config.  This behaves\nexactly like a regular dictionary but supports additional methods\nto load a config from files.\n"
    ),
    _("Flask.config_class() \nalias of flask.config.Config\n"),
    _("Flask.config_class() \nalias of flask.config.Config\n"),
    _(
        "Flask.context_processor(f) \nRegisters a template context processor function.\n"
    ),
    _(
        "Flask.context_processor(f) \nRegisters a template context processor function.\n"
    ),
    _(
        "Flask.create_global_jinja_loader() \nCreates the loader for the Jinja2 environment.  Can be used to\noverride just the loader and keeping the rest unchanged.  It’s\ndiscouraged to override this function.  Instead one should override\nthe jinja_loader() function instead.\nThe global loader dispatches between the loaders of the application\nand the individual blueprints.\n\nChangelog\nNew in version 0.7.\n\n"
    ),
    _(
        "Flask.create_global_jinja_loader() \nCreates the loader for the Jinja2 environment.  Can be used to\noverride just the loader and keeping the rest unchanged.  It’s\ndiscouraged to override this function.  Instead one should override\nthe jinja_loader() function instead.\nThe global loader dispatches between the loaders of the application\nand the individual blueprints.\n\nChangelog\nNew in version 0.7.\n\n"
    ),
    _(
        "Flask.create_jinja_environment() \nCreates the Jinja2 environment based on jinja_options\nand select_jinja_autoescape().  Since 0.7 this also adds\nthe Jinja2 globals and filters after initialization.  Override\nthis function to customize the behavior.\n\nChangelog\nChanged in version 0.11: Environment.auto_reload set in accordance with\nTEMPLATES_AUTO_RELOAD configuration option.\n\n\nNew in version 0.5.\n\n"
    ),
    _(
        "Flask.create_jinja_environment() \nCreates the Jinja2 environment based on jinja_options\nand select_jinja_autoescape().  Since 0.7 this also adds\nthe Jinja2 globals and filters after initialization.  Override\nthis function to customize the behavior.\n\nChangelog\nChanged in version 0.11: Environment.auto_reload set in accordance with\nTEMPLATES_AUTO_RELOAD configuration option.\n\n\nNew in version 0.5.\n\n"
    ),
    _(
        "Flask.create_url_adapter(request) \nCreates a URL adapter for the given request. The URL adapter\nis created at a point where the request context is not yet set\nup so the request is passed explicitly.\n\nChanged in version 1.0: SERVER_NAME no longer implicitly enables subdomain\nmatching. Use subdomain_matching instead.\n\n\nChangelog\nChanged in version 0.9: This can now also be called without a request object when the\nURL adapter is created for the application context.\n\n\nNew in version 0.6.\n\n"
    ),
    _(
        "Flask.create_url_adapter(request) \nCreates a URL adapter for the given request. The URL adapter\nis created at a point where the request context is not yet set\nup so the request is passed explicitly.\n\nChanged in version 1.0: SERVER_NAME no longer implicitly enables subdomain\nmatching. Use subdomain_matching instead.\n\n\nChangelog\nChanged in version 0.9: This can now also be called without a request object when the\nURL adapter is created for the application context.\n\n\nNew in version 0.6.\n\n"
    ),
    _(
        "Flask.debug() \nWhether debug mode is enabled. When using flask run to start\nthe development server, an interactive debugger will be shown for\nunhandled exceptions, and the server will be reloaded when code\nchanges. This maps to the DEBUG config key. This is\nenabled when env is 'development' and is overridden\nby the FLASK_DEBUG environment variable. It may not behave as\nexpected if set in code.\nDo not enable debug mode when deploying in production.\nDefault: True if env is 'development', or\nFalse otherwise.\n"
    ),
    _(
        "Flask.debug() \nWhether debug mode is enabled. When using flask run to start\nthe development server, an interactive debugger will be shown for\nunhandled exceptions, and the server will be reloaded when code\nchanges. This maps to the DEBUG config key. This is\nenabled when env is 'development' and is overridden\nby the FLASK_DEBUG environment variable. It may not behave as\nexpected if set in code.\nDo not enable debug mode when deploying in production.\nDefault: True if env is 'development', or\nFalse otherwise.\n"
    ),
    _("Flask.default_config() \nDefault configuration parameters.\n"),
    _("Flask.default_config() \nDefault configuration parameters.\n"),
    _(
        "Flask.dispatch_request() \nDoes the request dispatching.  Matches the URL and returns the\nreturn value of the view or error handler.  This does not have to\nbe a response object.  In order to convert the return value to a\nproper response object, call make_response().\n\nChangelog\nChanged in version 0.7: This no longer does the exception handling, this code was\nmoved to the new full_dispatch_request().\n\n"
    ),
    _(
        "Flask.dispatch_request() \nDoes the request dispatching.  Matches the URL and returns the\nreturn value of the view or error handler.  This does not have to\nbe a response object.  In order to convert the return value to a\nproper response object, call make_response().\n\nChangelog\nChanged in version 0.7: This no longer does the exception handling, this code was\nmoved to the new full_dispatch_request().\n\n"
    ),
    _(
        "Flask.do_teardown_appcontext(exc=&lt;object object&gt;) \nCalled right before the application context is popped.\nWhen handling a request, the application context is popped\nafter the request context. See do_teardown_request().\nThis calls all functions decorated with\nteardown_appcontext(). Then the\nappcontext_tearing_down signal is sent.\nThis is called by\nAppContext.pop().\n\nChangelog\nNew in version 0.9.\n\n"
    ),
    _(
        "Flask.do_teardown_appcontext(exc=&lt;object object&gt;) \nCalled right before the application context is popped.\nWhen handling a request, the application context is popped\nafter the request context. See do_teardown_request().\nThis calls all functions decorated with\nteardown_appcontext(). Then the\nappcontext_tearing_down signal is sent.\nThis is called by\nAppContext.pop().\n\nChangelog\nNew in version 0.9.\n\n"
    ),
    _(
        "Flask.do_teardown_request(exc=&lt;object object&gt;) \nCalled after the request is dispatched and the response is\nreturned, right before the request context is popped.\nThis calls all functions decorated with\nteardown_request(), and Blueprint.teardown_request()\nif a blueprint handled the request. Finally, the\nrequest_tearing_down signal is sent.\nThis is called by\nRequestContext.pop(),\nwhich may be delayed during testing to maintain access to\nresources.\n\n\n\n\nParameters:exc -- An unhandled exception raised while dispatching the\nrequest. Detected from the current exception information if\nnot passed. Passed to each teardown function.\n\n\n\n\nChangelog\nChanged in version 0.9: Added the exc argument.\n\n"
    ),
    _(
        "Flask.do_teardown_request(exc=&lt;object object&gt;) \nCalled after the request is dispatched and the response is\nreturned, right before the request context is popped.\nThis calls all functions decorated with\nteardown_request(), and Blueprint.teardown_request()\nif a blueprint handled the request. Finally, the\nrequest_tearing_down signal is sent.\nThis is called by\nRequestContext.pop(),\nwhich may be delayed during testing to maintain access to\nresources.\n\n\n\n\nParameters:exc -- An unhandled exception raised while dispatching the\nrequest. Detected from the current exception information if\nnot passed. Passed to each teardown function.\n\n\n\n\nChangelog\nChanged in version 0.9: Added the exc argument.\n\n"
    ),
    _(
        "Flask.endpoint(endpoint) \nA decorator to register a function as an endpoint.\nExample:\n@app.endpoint('example.endpoint')\ndef example():\n    return \"example\"\n\n\n\n\n\n\nParameters:endpoint -- the name of the endpoint\n\n\n\n"
    ),
    _(
        "Flask.endpoint(endpoint) \nA decorator to register a function as an endpoint.\nExample:\n@app.endpoint('example.endpoint')\ndef example():\n    return \"example\"\n\n\n\n\n\n\nParameters:endpoint -- the name of the endpoint\n\n\n\n"
    ),
    _(
        "Flask.env() \nWhat environment the app is running in. Flask and extensions may\nenable behaviors based on the environment, such as enabling debug\nmode. This maps to the ENV config key. This is set by the\nFLASK_ENV environment variable and may not behave as\nexpected if set in code.\nDo not enable development when deploying in production.\nDefault: 'production'\n"
    ),
    _(
        "Flask.env() \nWhat environment the app is running in. Flask and extensions may\nenable behaviors based on the environment, such as enabling debug\nmode. This maps to the ENV config key. This is set by the\nFLASK_ENV environment variable and may not behave as\nexpected if set in code.\nDo not enable development when deploying in production.\nDefault: 'production'\n"
    ),
    _(
        "Flask.error_handler_spec() \nA dictionary of all registered error handlers.  The key is None\nfor error handlers active on the application, otherwise the key is\nthe name of the blueprint.  Each key points to another dictionary\nwhere the key is the status code of the http exception.  The\nspecial key None points to a list of tuples where the first item\nis the class for the instance check and the second the error handler\nfunction.\nTo register an error handler, use the errorhandler()\ndecorator.\n"
    ),
    _(
        "Flask.error_handler_spec() \nA dictionary of all registered error handlers.  The key is None\nfor error handlers active on the application, otherwise the key is\nthe name of the blueprint.  Each key points to another dictionary\nwhere the key is the status code of the http exception.  The\nspecial key None points to a list of tuples where the first item\nis the class for the instance check and the second the error handler\nfunction.\nTo register an error handler, use the errorhandler()\ndecorator.\n"
    ),
    _(
        "Flask.errorhandler(code_or_exception) \nRegister a function to handle errors by code or exception class.\nA decorator that is used to register a function given an\nerror code.  Example:\n@app.errorhandler(404)\ndef page_not_found(error):\n    return 'This page does not exist', 404\n\n\nYou can also register handlers for arbitrary exceptions:\n@app.errorhandler(DatabaseError)\ndef special_exception_handler(error):\n    return 'Database connection failed', 500\n\n\n\nChangelog\nNew in version 0.7: Use register_error_handler() instead of modifying\nerror_handler_spec directly, for application wide error\nhandlers.\n\n\nNew in version 0.7: One can now additionally also register custom exception types\nthat do not necessarily have to be a subclass of the\nHTTPException class.\n\n\n\n\n\nParameters:code_or_exception -- the code as integer for the handler, or\nan arbitrary exception\n\n\n\n"
    ),
    _(
        "Flask.errorhandler(code_or_exception) \nRegister a function to handle errors by code or exception class.\nA decorator that is used to register a function given an\nerror code.  Example:\n@app.errorhandler(404)\ndef page_not_found(error):\n    return 'This page does not exist', 404\n\n\nYou can also register handlers for arbitrary exceptions:\n@app.errorhandler(DatabaseError)\ndef special_exception_handler(error):\n    return 'Database connection failed', 500\n\n\n\nChangelog\nNew in version 0.7: Use register_error_handler() instead of modifying\nerror_handler_spec directly, for application wide error\nhandlers.\n\n\nNew in version 0.7: One can now additionally also register custom exception types\nthat do not necessarily have to be a subclass of the\nHTTPException class.\n\n\n\n\n\nParameters:code_or_exception -- the code as integer for the handler, or\nan arbitrary exception\n\n\n\n"
    ),
    _(
        "Flask.extensions() \na place where extensions can store application specific state.  For\nexample this is where an extension could store database engines and\nsimilar things.  For backwards compatibility extensions should register\nthemselves like this:\nif not hasattr(app, 'extensions'):\n    app.extensions = {}\napp.extensions['extensionname'] = SomeObject()\n\n\nThe key must match the name of the extension module. For example in\ncase of a “Flask-Foo” extension in flask_foo, the key would be\n'foo'.\n\nChangelog\nNew in version 0.7.\n\n"
    ),
    _(
        "Flask.extensions() \na place where extensions can store application specific state.  For\nexample this is where an extension could store database engines and\nsimilar things.  For backwards compatibility extensions should register\nthemselves like this:\nif not hasattr(app, 'extensions'):\n    app.extensions = {}\napp.extensions['extensionname'] = SomeObject()\n\n\nThe key must match the name of the extension module. For example in\ncase of a “Flask-Foo” extension in flask_foo, the key would be\n'foo'.\n\nChangelog\nNew in version 0.7.\n\n"
    ),
    _(
        "Flask.full_dispatch_request() \nDispatches the request and on top of that performs request\npre and postprocessing as well as HTTP exception catching and\nerror handling.\n\nChangelog\nNew in version 0.7.\n\n"
    ),
    _(
        "Flask.full_dispatch_request() \nDispatches the request and on top of that performs request\npre and postprocessing as well as HTTP exception catching and\nerror handling.\n\nChangelog\nNew in version 0.7.\n\n"
    ),
    _(
        "Flask.get_send_file_max_age(filename) \nProvides default cache_timeout for the send_file() functions.\nBy default, this function returns SEND_FILE_MAX_AGE_DEFAULT from\nthe configuration of current_app.\nStatic file functions such as send_from_directory() use this\nfunction, and send_file() calls this function on\ncurrent_app when the given cache_timeout is None. If a\ncache_timeout is given in send_file(), that timeout is used;\notherwise, this method is called.\nThis allows subclasses to change the behavior when sending files based\non the filename.  For example, to set the cache timeout for .js files\nto 60 seconds:\nclass MyFlask(flask.Flask):\n    def get_send_file_max_age(self, name):\n        if name.lower().endswith('.js'):\n            return 60\n        return flask.Flask.get_send_file_max_age(self, name)\n\n\n\nChangelog\nNew in version 0.9.\n\n"
    ),
    _(
        "Flask.get_send_file_max_age(filename) \nProvides default cache_timeout for the send_file() functions.\nBy default, this function returns SEND_FILE_MAX_AGE_DEFAULT from\nthe configuration of current_app.\nStatic file functions such as send_from_directory() use this\nfunction, and send_file() calls this function on\ncurrent_app when the given cache_timeout is None. If a\ncache_timeout is given in send_file(), that timeout is used;\notherwise, this method is called.\nThis allows subclasses to change the behavior when sending files based\non the filename.  For example, to set the cache timeout for .js files\nto 60 seconds:\nclass MyFlask(flask.Flask):\n    def get_send_file_max_age(self, name):\n        if name.lower().endswith('.js'):\n            return 60\n        return flask.Flask.get_send_file_max_age(self, name)\n\n\n\nChangelog\nNew in version 0.9.\n\n"
    ),
    _(
        "Flask.got_first_request() \nThis attribute is set to True if the application started\nhandling the first request.\n\nChangelog\nNew in version 0.8.\n\n"
    ),
    _(
        "Flask.got_first_request() \nThis attribute is set to True if the application started\nhandling the first request.\n\nChangelog\nNew in version 0.8.\n\n"
    ),
    _(
        "Flask.handle_exception(e) \nDefault exception handling that kicks in when an exception\noccurs that is not caught.  In debug mode the exception will\nbe re-raised immediately, otherwise it is logged and the handler\nfor a 500 internal server error is used.  If no such handler\nexists, a default 500 internal server error message is displayed.\n\nChangelog\nNew in version 0.3.\n\n"
    ),
    _(
        "Flask.handle_exception(e) \nDefault exception handling that kicks in when an exception\noccurs that is not caught.  In debug mode the exception will\nbe re-raised immediately, otherwise it is logged and the handler\nfor a 500 internal server error is used.  If no such handler\nexists, a default 500 internal server error message is displayed.\n\nChangelog\nNew in version 0.3.\n\n"
    ),
    _(
        "Flask.handle_http_exception(e) \nHandles an HTTP exception.  By default this will invoke the\nregistered error handlers and fall back to returning the\nexception as response.\n\nChangelog\nNew in version 0.3.\n\n"
    ),
    _(
        "Flask.handle_http_exception(e) \nHandles an HTTP exception.  By default this will invoke the\nregistered error handlers and fall back to returning the\nexception as response.\n\nChangelog\nNew in version 0.3.\n\n"
    ),
    _(
        "Flask.handle_url_build_error(error, endpoint, values) \nHandle BuildError on url_for().\n"
    ),
    _(
        "Flask.handle_url_build_error(error, endpoint, values) \nHandle BuildError on url_for().\n"
    ),
    _(
        "Flask.handle_user_exception(e) \nThis method is called whenever an exception occurs that should be\nhandled.  A special case are\nHTTPExceptions which are forwarded by\nthis function to the handle_http_exception() method.  This\nfunction will either return a response value or reraise the\nexception with the same traceback.\n\nChanged in version 1.0: Key errors raised from request data like form show the the bad\nkey in debug mode rather than a generic bad request message.\n\n\nChangelog\nNew in version 0.7.\n\n"
    ),
    _(
        "Flask.handle_user_exception(e) \nThis method is called whenever an exception occurs that should be\nhandled.  A special case are\nHTTPExceptions which are forwarded by\nthis function to the handle_http_exception() method.  This\nfunction will either return a response value or reraise the\nexception with the same traceback.\n\nChanged in version 1.0: Key errors raised from request data like form show the the bad\nkey in debug mode rather than a generic bad request message.\n\n\nChangelog\nNew in version 0.7.\n\n"
    ),
    _(
        "Flask.has_static_folder() \nThis is True if the package bound object’s container has a\nfolder for static files.\n\nChangelog\nNew in version 0.5.\n\n"
    ),
    _(
        "Flask.has_static_folder() \nThis is True if the package bound object’s container has a\nfolder for static files.\n\nChangelog\nNew in version 0.5.\n\n"
    ),
    _(
        "Flask.import_name() \nThe name of the package or module that this app belongs to. Do not\nchange this once it is set by the constructor.\n"
    ),
    _(
        "Flask.import_name() \nThe name of the package or module that this app belongs to. Do not\nchange this once it is set by the constructor.\n"
    ),
    _(
        "Flask.inject_url_defaults(endpoint, values) \nInjects the URL defaults for the given endpoint directly into\nthe values dictionary passed.  This is used internally and\nautomatically called on URL building.\n\nChangelog\nNew in version 0.7.\n\n"
    ),
    _(
        "Flask.inject_url_defaults(endpoint, values) \nInjects the URL defaults for the given endpoint directly into\nthe values dictionary passed.  This is used internally and\nautomatically called on URL building.\n\nChangelog\nNew in version 0.7.\n\n"
    ),
    _(
        "Flask.instance_path() \nHolds the path to the instance folder.\n\nChangelog\nNew in version 0.8.\n\n"
    ),
    _(
        "Flask.instance_path() \nHolds the path to the instance folder.\n\nChangelog\nNew in version 0.8.\n\n"
    ),
    _(
        "Flask.iter_blueprints() \nIterates over all blueprints by the order they were registered.\n\nChangelog\nNew in version 0.11.\n\n"
    ),
    _(
        "Flask.iter_blueprints() \nIterates over all blueprints by the order they were registered.\n\nChangelog\nNew in version 0.11.\n\n"
    ),
    _("Flask.jinja_env() \nThe Jinja2 environment used to load templates.\n"),
    _("Flask.jinja_env() \nThe Jinja2 environment used to load templates.\n"),
    _("Flask.jinja_environment() \nalias of flask.templating.Environment\n"),
    _("Flask.jinja_environment() \nalias of flask.templating.Environment\n"),
    _(
        "Flask.jinja_loader() \nThe Jinja loader for this package bound object.\n\nChangelog\nNew in version 0.5.\n\n"
    ),
    _(
        "Flask.jinja_loader() \nThe Jinja loader for this package bound object.\n\nChangelog\nNew in version 0.5.\n\n"
    ),
    _(
        "Flask.jinja_options() \nOptions that are passed directly to the Jinja2 environment.\n"
    ),
    _(
        "Flask.jinja_options() \nOptions that are passed directly to the Jinja2 environment.\n"
    ),
    _("Flask.json_decoder() \nalias of flask.json.JSONDecoder\n"),
    _("Flask.json_decoder() \nalias of flask.json.JSONDecoder\n"),
    _("Flask.json_encoder() \nalias of flask.json.JSONEncoder\n"),
    _("Flask.json_encoder() \nalias of flask.json.JSONEncoder\n"),
    _(
        "Flask.log_exception(exc_info) \nLogs an exception.  This is called by handle_exception()\nif debugging is disabled and right before the handler is called.\nThe default implementation logs the exception as error on the\nlogger.\n\nChangelog\nNew in version 0.8.\n\n"
    ),
    _(
        "Flask.log_exception(exc_info) \nLogs an exception.  This is called by handle_exception()\nif debugging is disabled and right before the handler is called.\nThe default implementation logs the exception as error on the\nlogger.\n\nChangelog\nNew in version 0.8.\n\n"
    ),
    _(
        "Flask.logger() \nThe 'flask.app' logger, a standard Python\nLogger.\nIn debug mode, the logger’s level will be set\nto DEBUG.\nIf there are no handlers configured, a default handler will be added.\nSee Logging for more information.\n\nChanged in version 1.0: Behavior was simplified. The logger is always named\nflask.app. The level is only set during configuration, it\ndoesn’t check app.debug each time. Only one format is used,\nnot different ones depending on app.debug. No handlers are\nremoved, and a handler is only added if no handlers are already\nconfigured.\n\n\nChangelog\nNew in version 0.3.\n\n"
    ),
    _(
        "Flask.logger() \nThe 'flask.app' logger, a standard Python\nLogger.\nIn debug mode, the logger’s level will be set\nto DEBUG.\nIf there are no handlers configured, a default handler will be added.\nSee Logging for more information.\n\nChanged in version 1.0: Behavior was simplified. The logger is always named\nflask.app. The level is only set during configuration, it\ndoesn’t check app.debug each time. Only one format is used,\nnot different ones depending on app.debug. No handlers are\nremoved, and a handler is only added if no handlers are already\nconfigured.\n\n\nChangelog\nNew in version 0.3.\n\n"
    ),
    _(
        "Flask.make_config(instance_relative=False) \nUsed to create the config attribute by the Flask constructor.\nThe instance_relative parameter is passed in from the constructor\nof Flask (there named instance_relative_config) and indicates if\nthe config should be relative to the instance path or the root path\nof the application.\n\nChangelog\nNew in version 0.8.\n\n"
    ),
    _(
        "Flask.make_config(instance_relative=False) \nUsed to create the config attribute by the Flask constructor.\nThe instance_relative parameter is passed in from the constructor\nof Flask (there named instance_relative_config) and indicates if\nthe config should be relative to the instance path or the root path\nof the application.\n\nChangelog\nNew in version 0.8.\n\n"
    ),
    _(
        "Flask.make_default_options_response() \nThis method is called to create the default OPTIONS response.\nThis can be changed through subclassing to change the default\nbehavior of OPTIONS responses.\n\nChangelog\nNew in version 0.7.\n\n"
    ),
    _(
        "Flask.make_default_options_response() \nThis method is called to create the default OPTIONS response.\nThis can be changed through subclassing to change the default\nbehavior of OPTIONS responses.\n\nChangelog\nNew in version 0.7.\n\n"
    ),
    _(
        "Flask.make_null_session() \nCreates a new instance of a missing session.  Instead of overriding\nthis method we recommend replacing the session_interface.\n\nChangelog\nNew in version 0.7.\n\n"
    ),
    _(
        "Flask.make_null_session() \nCreates a new instance of a missing session.  Instead of overriding\nthis method we recommend replacing the session_interface.\n\nChangelog\nNew in version 0.7.\n\n"
    ),
    _(
        "Flask.make_response(rv) \nConvert the return value from a view function to an instance of\nresponse_class.\n\n\n\n\nParameters:rv -- the return value from the view function. The view function\nmust return a response. Returning None, or the view ending\nwithout returning, is not allowed. The following types are allowed\nfor view_rv:\n\nstr (unicode in Python 2)\nA response object is created with the string encoded to UTF-8\nas the body.\nbytes (str in Python 2)\nA response object is created with the bytes as the body.\ntuple\nEither (body, status, headers), (body, status), or\n(body, headers), where body is any of the other types\nallowed here, status is a string or an integer, and\nheaders is a dictionary or a list of (key, value)\ntuples. If body is a response_class instance,\nstatus overwrites the exiting value and headers are\nextended.\nresponse_class\nThe object is returned unchanged.\nother Response class\nThe object is coerced to response_class.\ncallable()\nThe function is called as a WSGI application. The result is\nused to create a response object.\n\n\n\n\n\n\nChangelog\nChanged in version 0.9: Previously a tuple was interpreted as the arguments for the\nresponse object.\n\n"
    ),
    _(
        "Flask.make_response(rv) \nConvert the return value from a view function to an instance of\nresponse_class.\n\n\n\n\nParameters:rv -- the return value from the view function. The view function\nmust return a response. Returning None, or the view ending\nwithout returning, is not allowed. The following types are allowed\nfor view_rv:\n\nstr (unicode in Python 2)\nA response object is created with the string encoded to UTF-8\nas the body.\nbytes (str in Python 2)\nA response object is created with the bytes as the body.\ntuple\nEither (body, status, headers), (body, status), or\n(body, headers), where body is any of the other types\nallowed here, status is a string or an integer, and\nheaders is a dictionary or a list of (key, value)\ntuples. If body is a response_class instance,\nstatus overwrites the exiting value and headers are\nextended.\nresponse_class\nThe object is returned unchanged.\nother Response class\nThe object is coerced to response_class.\ncallable()\nThe function is called as a WSGI application. The result is\nused to create a response object.\n\n\n\n\n\n\nChangelog\nChanged in version 0.9: Previously a tuple was interpreted as the arguments for the\nresponse object.\n\n"
    ),
    _(
        "Flask.make_shell_context() \nReturns the shell context for an interactive shell for this\napplication.  This runs all the registered shell context\nprocessors.\n\nChangelog\nNew in version 0.11.\n\n"
    ),
    _(
        "Flask.make_shell_context() \nReturns the shell context for an interactive shell for this\napplication.  This runs all the registered shell context\nprocessors.\n\nChangelog\nNew in version 0.11.\n\n"
    ),
    _(
        "Flask.name() \nThe name of the application.  This is usually the import name\nwith the difference that it’s guessed from the run file if the\nimport name is main.  This name is used as a display name when\nFlask needs the name of the application.  It can be set and overridden\nto change the value.\n\nChangelog\nNew in version 0.8.\n\n"
    ),
    _(
        "Flask.name() \nThe name of the application.  This is usually the import name\nwith the difference that it’s guessed from the run file if the\nimport name is main.  This name is used as a display name when\nFlask needs the name of the application.  It can be set and overridden\nto change the value.\n\nChangelog\nNew in version 0.8.\n\n"
    ),
    _(
        "Flask.open_instance_resource(resource, mode='rb') \nOpens a resource from the application’s instance folder\n(instance_path).  Otherwise works like\nopen_resource().  Instance resources can also be opened for\nwriting.\n\n\n\n\nParameters:\nresource -- the name of the resource.  To access resources within\nsubfolders use forward slashes as separator.\nmode -- resource file opening mode, default is ‘rb’.\n\n\n\n\n\n"
    ),
    _(
        "Flask.open_instance_resource(resource, mode='rb') \nOpens a resource from the application’s instance folder\n(instance_path).  Otherwise works like\nopen_resource().  Instance resources can also be opened for\nwriting.\n\n\n\n\nParameters:\nresource -- the name of the resource.  To access resources within\nsubfolders use forward slashes as separator.\nmode -- resource file opening mode, default is ‘rb’.\n\n\n\n\n\n"
    ),
    _(
        "Flask.open_resource(resource, mode='rb') \nOpens a resource from the application’s resource folder.  To see\nhow this works, consider the following folder structure:\n/myapplication.py\n/schema.sql\n/static\n    /style.css\n/templates\n    /layout.html\n    /index.html\n\n\nIf you want to open the schema.sql file you would do the\nfollowing:\nwith app.open_resource('schema.sql') as f:\n    contents = f.read()\n    do_something_with(contents)\n\n\n\n\n\n\nParameters:\nresource -- the name of the resource.  To access resources within\nsubfolders use forward slashes as separator.\nmode -- resource file opening mode, default is ‘rb’.\n\n\n\n\n\n"
    ),
    _(
        "Flask.open_resource(resource, mode='rb') \nOpens a resource from the application’s resource folder.  To see\nhow this works, consider the following folder structure:\n/myapplication.py\n/schema.sql\n/static\n    /style.css\n/templates\n    /layout.html\n    /index.html\n\n\nIf you want to open the schema.sql file you would do the\nfollowing:\nwith app.open_resource('schema.sql') as f:\n    contents = f.read()\n    do_something_with(contents)\n\n\n\n\n\n\nParameters:\nresource -- the name of the resource.  To access resources within\nsubfolders use forward slashes as separator.\nmode -- resource file opening mode, default is ‘rb’.\n\n\n\n\n\n"
    ),
    _(
        "Flask.open_session(request) \nCreates or opens a new session.  Default implementation stores all\nsession data in a signed cookie.  This requires that the\nsecret_key is set.  Instead of overriding this method\nwe recommend replacing the session_interface.\n\n\n\n\nParameters:request -- an instance of request_class.\n\n\n\n"
    ),
    _(
        "Flask.open_session(request) \nCreates or opens a new session.  Default implementation stores all\nsession data in a signed cookie.  This requires that the\nsecret_key is set.  Instead of overriding this method\nwe recommend replacing the session_interface.\n\n\n\n\nParameters:request -- an instance of request_class.\n\n\n\n"
    ),
    _(
        "Flask.permanent_session_lifetime() \nA timedelta which is used to set the expiration\ndate of a permanent session.  The default is 31 days which makes a\npermanent session survive for roughly one month.\nThis attribute can also be configured from the config with the\nPERMANENT_SESSION_LIFETIME configuration key.  Defaults to\ntimedelta(days=31)\n"
    ),
    _(
        "Flask.permanent_session_lifetime() \nA timedelta which is used to set the expiration\ndate of a permanent session.  The default is 31 days which makes a\npermanent session survive for roughly one month.\nThis attribute can also be configured from the config with the\nPERMANENT_SESSION_LIFETIME configuration key.  Defaults to\ntimedelta(days=31)\n"
    ),
    _(
        "Flask.preprocess_request() \nCalled before the request is dispatched. Calls\nurl_value_preprocessors registered with the app and the\ncurrent blueprint (if any). Then calls before_request_funcs\nregistered with the app and the blueprint.\nIf any before_request() handler returns a non-None value, the\nvalue is handled as if it was the return value from the view, and\nfurther request handling is stopped.\n"
    ),
    _(
        "Flask.preprocess_request() \nCalled before the request is dispatched. Calls\nurl_value_preprocessors registered with the app and the\ncurrent blueprint (if any). Then calls before_request_funcs\nregistered with the app and the blueprint.\nIf any before_request() handler returns a non-None value, the\nvalue is handled as if it was the return value from the view, and\nfurther request handling is stopped.\n"
    ),
    _(
        "Flask.preserve_context_on_exception() \nReturns the value of the PRESERVE_CONTEXT_ON_EXCEPTION\nconfiguration value in case it’s set, otherwise a sensible default\nis returned.\n\nChangelog\nNew in version 0.7.\n\n"
    ),
    _(
        "Flask.preserve_context_on_exception() \nReturns the value of the PRESERVE_CONTEXT_ON_EXCEPTION\nconfiguration value in case it’s set, otherwise a sensible default\nis returned.\n\nChangelog\nNew in version 0.7.\n\n"
    ),
    _(
        "Flask.process_response(response) \nCan be overridden in order to modify the response object\nbefore it’s sent to the WSGI server.  By default this will\ncall all the after_request() decorated functions.\n\nChangelog\nChanged in version 0.5: As of Flask 0.5 the functions registered for after request\nexecution are called in reverse order of registration.\n\n\n\n\n\nParameters:response -- a response_class object.\n\nReturns:a new response object or the same, has to be an\ninstance of response_class.\n\n\n\n"
    ),
    _(
        "Flask.process_response(response) \nCan be overridden in order to modify the response object\nbefore it’s sent to the WSGI server.  By default this will\ncall all the after_request() decorated functions.\n\nChangelog\nChanged in version 0.5: As of Flask 0.5 the functions registered for after request\nexecution are called in reverse order of registration.\n\n\n\n\n\nParameters:response -- a response_class object.\n\nReturns:a new response object or the same, has to be an\ninstance of response_class.\n\n\n\n"
    ),
    _(
        "Flask.propagate_exceptions() \nReturns the value of the PROPAGATE_EXCEPTIONS configuration\nvalue in case it’s set, otherwise a sensible default is returned.\n\nChangelog\nNew in version 0.7.\n\n"
    ),
    _(
        "Flask.propagate_exceptions() \nReturns the value of the PROPAGATE_EXCEPTIONS configuration\nvalue in case it’s set, otherwise a sensible default is returned.\n\nChangelog\nNew in version 0.7.\n\n"
    ),
    _(
        "Flask.register_blueprint(blueprint, **options) \nRegister a Blueprint on the application. Keyword\narguments passed to this method will override the defaults set on the\nblueprint.\nCalls the blueprint’s register() method after\nrecording the blueprint in the application’s blueprints.\n\n\n\n\nParameters:\nblueprint -- The blueprint to register.\nurl_prefix -- Blueprint routes will be prefixed with this.\nsubdomain -- Blueprint routes will match on this subdomain.\nurl_defaults -- Blueprint routes will use these default values for\nview arguments.\noptions -- Additional keyword arguments are passed to\nBlueprintSetupState. They can be\naccessed in record() callbacks.\n\n\n\n\n\n\nChangelog\nNew in version 0.7.\n\n"
    ),
    _(
        "Flask.register_blueprint(blueprint, **options) \nRegister a Blueprint on the application. Keyword\narguments passed to this method will override the defaults set on the\nblueprint.\nCalls the blueprint’s register() method after\nrecording the blueprint in the application’s blueprints.\n\n\n\n\nParameters:\nblueprint -- The blueprint to register.\nurl_prefix -- Blueprint routes will be prefixed with this.\nsubdomain -- Blueprint routes will match on this subdomain.\nurl_defaults -- Blueprint routes will use these default values for\nview arguments.\noptions -- Additional keyword arguments are passed to\nBlueprintSetupState. They can be\naccessed in record() callbacks.\n\n\n\n\n\n\nChangelog\nNew in version 0.7.\n\n"
    ),
    _(
        "Flask.register_error_handler(code_or_exception, f) \nAlternative error attach function to the errorhandler()\ndecorator that is more straightforward to use for non decorator\nusage.\n\nChangelog\nNew in version 0.7.\n\n"
    ),
    _(
        "Flask.register_error_handler(code_or_exception, f) \nAlternative error attach function to the errorhandler()\ndecorator that is more straightforward to use for non decorator\nusage.\n\nChangelog\nNew in version 0.7.\n\n"
    ),
    _("Flask.request_class() \nalias of flask.wrappers.Request\n"),
    _("Flask.request_class() \nalias of flask.wrappers.Request\n"),
    _(
        "Flask.request_context(environ) \nCreate a RequestContext representing a\nWSGI environment. Use a with block to push the context,\nwhich will make request point at this request.\nSee The Request Context.\nTypically you should not call this from your own code. A request\ncontext is automatically pushed by the wsgi_app() when\nhandling a request. Use test_request_context() to create\nan environment and context instead of this method.\n\n\n\n\nParameters:environ -- a WSGI environment\n\n\n\n"
    ),
    _(
        "Flask.request_context(environ) \nCreate a RequestContext representing a\nWSGI environment. Use a with block to push the context,\nwhich will make request point at this request.\nSee The Request Context.\nTypically you should not call this from your own code. A request\ncontext is automatically pushed by the wsgi_app() when\nhandling a request. Use test_request_context() to create\nan environment and context instead of this method.\n\n\n\n\nParameters:environ -- a WSGI environment\n\n\n\n"
    ),
    _("Flask.response_class() \nalias of flask.wrappers.Response\n"),
    _("Flask.response_class() \nalias of flask.wrappers.Response\n"),
    _(
        "Flask.root_path() \nAbsolute path to the package on the filesystem. Used to look up\nresources contained in the package.\n"
    ),
    _(
        "Flask.root_path() \nAbsolute path to the package on the filesystem. Used to look up\nresources contained in the package.\n"
    ),
    _(
        "Flask.route(rule, **options) \nA decorator that is used to register a view function for a\ngiven URL rule.  This does the same thing as add_url_rule()\nbut is intended for decorator usage:\n@app.route('/')\ndef index():\n    return 'Hello World'\n\n\nFor more information refer to URL Route Registrations.\n\n\n\n\nParameters:\nrule -- the URL rule as string\nendpoint -- the endpoint for the registered URL rule.  Flask\nitself assumes the name of the view function as\nendpoint\noptions -- the options to be forwarded to the underlying\nRule object.  A change\nto Werkzeug is handling of method options.  methods\nis a list of methods this rule should be limited\nto (GET, POST etc.).  By default a rule\njust listens for GET (and implicitly HEAD).\nStarting with Flask 0.6, OPTIONS is implicitly\nadded and handled by the standard request handling.\n\n\n\n\n\n"
    ),
    _(
        "Flask.route(rule, **options) \nA decorator that is used to register a view function for a\ngiven URL rule.  This does the same thing as add_url_rule()\nbut is intended for decorator usage:\n@app.route('/')\ndef index():\n    return 'Hello World'\n\n\nFor more information refer to URL Route Registrations.\n\n\n\n\nParameters:\nrule -- the URL rule as string\nendpoint -- the endpoint for the registered URL rule.  Flask\nitself assumes the name of the view function as\nendpoint\noptions -- the options to be forwarded to the underlying\nRule object.  A change\nto Werkzeug is handling of method options.  methods\nis a list of methods this rule should be limited\nto (GET, POST etc.).  By default a rule\njust listens for GET (and implicitly HEAD).\nStarting with Flask 0.6, OPTIONS is implicitly\nadded and handled by the standard request handling.\n\n\n\n\n\n"
    ),
    _(
        "Flask.run(host=None, port=None, debug=None, load_dotenv=True, **options) \nRuns the application on a local development server.\nDo not use run() in a production setting. It is not intended to\nmeet security and performance requirements for a production server.\nInstead, see Deployment Options for WSGI server recommendations.\nIf the debug flag is set the server will automatically reload\nfor code changes and show a debugger in case an exception happened.\nIf you want to run the application in debug mode, but disable the\ncode execution on the interactive debugger, you can pass\nuse_evalex=False as parameter.  This will keep the debugger’s\ntraceback screen active, but disable code execution.\nIt is not recommended to use this function for development with\nautomatic reloading as this is badly supported.  Instead you should\nbe using the flask command line script’s run support.\n\nKeep in Mind\nFlask will suppress any server error with a generic error page\nunless it is in debug mode.  As such to enable just the\ninteractive debugger without the code reloading, you have to\ninvoke run() with debug=True and use_reloader=False.\nSetting use_debugger to True without being in debug mode\nwon’t catch any exceptions because there won’t be any to\ncatch.\n\n\n\n\n\nParameters:\nhost -- the hostname to listen on. Set this to '0.0.0.0' to\nhave the server available externally as well. Defaults to\n'127.0.0.1' or the host in the SERVER_NAME config variable\nif present.\nport -- the port of the webserver. Defaults to 5000 or the\nport defined in the SERVER_NAME config variable if present.\ndebug -- if given, enable or disable debug mode. See\ndebug.\nload_dotenv -- Load the nearest .env and .flaskenv\nfiles to set environment variables. Will also change the working\ndirectory to the directory containing the first file found.\noptions -- the options to be forwarded to the underlying Werkzeug\nserver. See werkzeug.serving.run_simple() for more\ninformation.\n\n\n\n\n\n\nChanged in version 1.0: If installed, python-dotenv will be used to load environment\nvariables from .env and .flaskenv files.\nIf set, the FLASK_ENV and FLASK_DEBUG\nenvironment variables will override env and\ndebug.\nThreaded mode is enabled by default.\n\n\nChangelog\nChanged in version 0.10: The default port is now picked from the SERVER_NAME\nvariable.\n\n"
    ),
    _(
        "Flask.run(host=None, port=None, debug=None, load_dotenv=True, **options) \nRuns the application on a local development server.\nDo not use run() in a production setting. It is not intended to\nmeet security and performance requirements for a production server.\nInstead, see Deployment Options for WSGI server recommendations.\nIf the debug flag is set the server will automatically reload\nfor code changes and show a debugger in case an exception happened.\nIf you want to run the application in debug mode, but disable the\ncode execution on the interactive debugger, you can pass\nuse_evalex=False as parameter.  This will keep the debugger’s\ntraceback screen active, but disable code execution.\nIt is not recommended to use this function for development with\nautomatic reloading as this is badly supported.  Instead you should\nbe using the flask command line script’s run support.\n\nKeep in Mind\nFlask will suppress any server error with a generic error page\nunless it is in debug mode.  As such to enable just the\ninteractive debugger without the code reloading, you have to\ninvoke run() with debug=True and use_reloader=False.\nSetting use_debugger to True without being in debug mode\nwon’t catch any exceptions because there won’t be any to\ncatch.\n\n\n\n\n\nParameters:\nhost -- the hostname to listen on. Set this to '0.0.0.0' to\nhave the server available externally as well. Defaults to\n'127.0.0.1' or the host in the SERVER_NAME config variable\nif present.\nport -- the port of the webserver. Defaults to 5000 or the\nport defined in the SERVER_NAME config variable if present.\ndebug -- if given, enable or disable debug mode. See\ndebug.\nload_dotenv -- Load the nearest .env and .flaskenv\nfiles to set environment variables. Will also change the working\ndirectory to the directory containing the first file found.\noptions -- the options to be forwarded to the underlying Werkzeug\nserver. See werkzeug.serving.run_simple() for more\ninformation.\n\n\n\n\n\n\nChanged in version 1.0: If installed, python-dotenv will be used to load environment\nvariables from .env and .flaskenv files.\nIf set, the FLASK_ENV and FLASK_DEBUG\nenvironment variables will override env and\ndebug.\nThreaded mode is enabled by default.\n\n\nChangelog\nChanged in version 0.10: The default port is now picked from the SERVER_NAME\nvariable.\n\n"
    ),
    _(
        "Flask.save_session(session, response) \nSaves the session if it needs updates.  For the default\nimplementation, check open_session().  Instead of overriding this\nmethod we recommend replacing the session_interface.\n\n\n\n\nParameters:\nsession -- the session to be saved (a\nSecureCookie\nobject)\nresponse -- an instance of response_class\n\n\n\n\n\n"
    ),
    _(
        "Flask.save_session(session, response) \nSaves the session if it needs updates.  For the default\nimplementation, check open_session().  Instead of overriding this\nmethod we recommend replacing the session_interface.\n\n\n\n\nParameters:\nsession -- the session to be saved (a\nSecureCookie\nobject)\nresponse -- an instance of response_class\n\n\n\n\n\n"
    ),
    _(
        "Flask.secret_key() \nIf a secret key is set, cryptographic components can use this to\nsign cookies and other things. Set this to a complex random value\nwhen you want to use the secure cookie for instance.\nThis attribute can also be configured from the config with the\nSECRET_KEY configuration key. Defaults to None.\n"
    ),
    _(
        "Flask.secret_key() \nIf a secret key is set, cryptographic components can use this to\nsign cookies and other things. Set this to a complex random value\nwhen you want to use the secure cookie for instance.\nThis attribute can also be configured from the config with the\nSECRET_KEY configuration key. Defaults to None.\n"
    ),
    _(
        "Flask.select_jinja_autoescape(filename) \nReturns True if autoescaping should be active for the given\ntemplate name. If no template name is given, returns True.\n\nChangelog\nNew in version 0.5.\n\n"
    ),
    _(
        "Flask.select_jinja_autoescape(filename) \nReturns True if autoescaping should be active for the given\ntemplate name. If no template name is given, returns True.\n\nChangelog\nNew in version 0.5.\n\n"
    ),
    _(
        "Flask.send_file_max_age_default() \nA timedelta which is used as default cache_timeout\nfor the send_file() functions. The default is 12 hours.\nThis attribute can also be configured from the config with the\nSEND_FILE_MAX_AGE_DEFAULT configuration key. This configuration\nvariable can also be set with an integer value used as seconds.\nDefaults to timedelta(hours=12)\n"
    ),
    _(
        "Flask.send_file_max_age_default() \nA timedelta which is used as default cache_timeout\nfor the send_file() functions. The default is 12 hours.\nThis attribute can also be configured from the config with the\nSEND_FILE_MAX_AGE_DEFAULT configuration key. This configuration\nvariable can also be set with an integer value used as seconds.\nDefaults to timedelta(hours=12)\n"
    ),
    _(
        "Flask.send_static_file(filename) \nFunction used internally to send static files from the static\nfolder to the browser.\n\nChangelog\nNew in version 0.5.\n\n"
    ),
    _(
        "Flask.send_static_file(filename) \nFunction used internally to send static files from the static\nfolder to the browser.\n\nChangelog\nNew in version 0.5.\n\n"
    ),
    _(
        "Flask.session_cookie_name() \nThe secure cookie uses this for the name of the session cookie.\nThis attribute can also be configured from the config with the\nSESSION_COOKIE_NAME configuration key.  Defaults to 'session'\n"
    ),
    _(
        "Flask.session_cookie_name() \nThe secure cookie uses this for the name of the session cookie.\nThis attribute can also be configured from the config with the\nSESSION_COOKIE_NAME configuration key.  Defaults to 'session'\n"
    ),
    _(
        "Flask.session_interface() \nthe session interface to use.  By default an instance of\nSecureCookieSessionInterface is used here.\n\nChangelog\nNew in version 0.8.\n\n"
    ),
    _(
        "Flask.session_interface() \nthe session interface to use.  By default an instance of\nSecureCookieSessionInterface is used here.\n\nChangelog\nNew in version 0.8.\n\n"
    ),
    _(
        "Flask.shell_context_processor(f) \nRegisters a shell context processor function.\n\nChangelog\nNew in version 0.11.\n\n"
    ),
    _(
        "Flask.shell_context_processor(f) \nRegisters a shell context processor function.\n\nChangelog\nNew in version 0.11.\n\n"
    ),
    _(
        "Flask.shell_context_processors() \nA list of shell context processor functions that should be run\nwhen a shell context is created.\n\nChangelog\nNew in version 0.11.\n\n"
    ),
    _(
        "Flask.shell_context_processors() \nA list of shell context processor functions that should be run\nwhen a shell context is created.\n\nChangelog\nNew in version 0.11.\n\n"
    ),
    _(
        "Flask.should_ignore_error(error) \nThis is called to figure out if an error should be ignored\nor not as far as the teardown system is concerned.  If this\nfunction returns True then the teardown handlers will not be\npassed the error.\n\nChangelog\nNew in version 0.10.\n\n"
    ),
    _(
        "Flask.should_ignore_error(error) \nThis is called to figure out if an error should be ignored\nor not as far as the teardown system is concerned.  If this\nfunction returns True then the teardown handlers will not be\npassed the error.\n\nChangelog\nNew in version 0.10.\n\n"
    ),
    _(
        "Flask.static_folder() \nThe absolute path to the configured static folder.\n"
    ),
    _(
        "Flask.static_folder() \nThe absolute path to the configured static folder.\n"
    ),
    _(
        "Flask.static_url_path() \nThe URL prefix that the static route will be registered for.\n"
    ),
    _(
        "Flask.static_url_path() \nThe URL prefix that the static route will be registered for.\n"
    ),
    _(
        "Flask.teardown_appcontext(f) \nRegisters a function to be called when the application context\nends.  These functions are typically also called when the request\ncontext is popped.\nExample:\nctx = app.app_context()\nctx.push()\n...\nctx.pop()\n\n\nWhen ctx.pop() is executed in the above example, the teardown\nfunctions are called just before the app context moves from the\nstack of active contexts.  This becomes relevant if you are using\nsuch constructs in tests.\nSince a request context typically also manages an application\ncontext it would also be called when you pop a request context.\nWhen a teardown function was called because of an unhandled exception\nit will be passed an error object. If an errorhandler() is\nregistered, it will handle the exception and the teardown will not\nreceive it.\nThe return values of teardown functions are ignored.\n\nChangelog\nNew in version 0.9.\n\n"
    ),
    _(
        "Flask.teardown_appcontext(f) \nRegisters a function to be called when the application context\nends.  These functions are typically also called when the request\ncontext is popped.\nExample:\nctx = app.app_context()\nctx.push()\n...\nctx.pop()\n\n\nWhen ctx.pop() is executed in the above example, the teardown\nfunctions are called just before the app context moves from the\nstack of active contexts.  This becomes relevant if you are using\nsuch constructs in tests.\nSince a request context typically also manages an application\ncontext it would also be called when you pop a request context.\nWhen a teardown function was called because of an unhandled exception\nit will be passed an error object. If an errorhandler() is\nregistered, it will handle the exception and the teardown will not\nreceive it.\nThe return values of teardown functions are ignored.\n\nChangelog\nNew in version 0.9.\n\n"
    ),
    _(
        "Flask.teardown_appcontext_funcs() \nA list of functions that are called when the application context\nis destroyed.  Since the application context is also torn down\nif the request ends this is the place to store code that disconnects\nfrom databases.\n\nChangelog\nNew in version 0.9.\n\n"
    ),
    _(
        "Flask.teardown_appcontext_funcs() \nA list of functions that are called when the application context\nis destroyed.  Since the application context is also torn down\nif the request ends this is the place to store code that disconnects\nfrom databases.\n\nChangelog\nNew in version 0.9.\n\n"
    ),
    _(
        "Flask.teardown_request(f) \nRegister a function to be run at the end of each request,\nregardless of whether there was an exception or not.  These functions\nare executed when the request context is popped, even if not an\nactual request was performed.\nExample:\nctx = app.test_request_context()\nctx.push()\n...\nctx.pop()\n\n\nWhen ctx.pop() is executed in the above example, the teardown\nfunctions are called just before the request context moves from the\nstack of active contexts.  This becomes relevant if you are using\nsuch constructs in tests.\nGenerally teardown functions must take every necessary step to avoid\nthat they will fail.  If they do execute code that might fail they\nwill have to surround the execution of these code by try/except\nstatements and log occurring errors.\nWhen a teardown function was called because of an exception it will\nbe passed an error object.\nThe return values of teardown functions are ignored.\n\nDebug Note\nIn debug mode Flask will not tear down a request on an exception\nimmediately.  Instead it will keep it alive so that the interactive\ndebugger can still access it.  This behavior can be controlled\nby the PRESERVE_CONTEXT_ON_EXCEPTION configuration variable.\n\n"
    ),
    _(
        "Flask.teardown_request(f) \nRegister a function to be run at the end of each request,\nregardless of whether there was an exception or not.  These functions\nare executed when the request context is popped, even if not an\nactual request was performed.\nExample:\nctx = app.test_request_context()\nctx.push()\n...\nctx.pop()\n\n\nWhen ctx.pop() is executed in the above example, the teardown\nfunctions are called just before the request context moves from the\nstack of active contexts.  This becomes relevant if you are using\nsuch constructs in tests.\nGenerally teardown functions must take every necessary step to avoid\nthat they will fail.  If they do execute code that might fail they\nwill have to surround the execution of these code by try/except\nstatements and log occurring errors.\nWhen a teardown function was called because of an exception it will\nbe passed an error object.\nThe return values of teardown functions are ignored.\n\nDebug Note\nIn debug mode Flask will not tear down a request on an exception\nimmediately.  Instead it will keep it alive so that the interactive\ndebugger can still access it.  This behavior can be controlled\nby the PRESERVE_CONTEXT_ON_EXCEPTION configuration variable.\n\n"
    ),
    _(
        "Flask.teardown_request_funcs() \nA dictionary with lists of functions that are called after\neach request, even if an exception has occurred. The key of the\ndictionary is the name of the blueprint this function is active for,\nNone for all requests. These functions are not allowed to modify\nthe request, and their return values are ignored. If an exception\noccurred while processing the request, it gets passed to each\nteardown_request function. To register a function here, use the\nteardown_request() decorator.\n\nChangelog\nNew in version 0.7.\n\n"
    ),
    _(
        "Flask.teardown_request_funcs() \nA dictionary with lists of functions that are called after\neach request, even if an exception has occurred. The key of the\ndictionary is the name of the blueprint this function is active for,\nNone for all requests. These functions are not allowed to modify\nthe request, and their return values are ignored. If an exception\noccurred while processing the request, it gets passed to each\nteardown_request function. To register a function here, use the\nteardown_request() decorator.\n\nChangelog\nNew in version 0.7.\n\n"
    ),
    _(
        "Flask.template_context_processors() \nA dictionary with list of functions that are called without argument\nto populate the template context.  The key of the dictionary is the\nname of the blueprint this function is active for, None for all\nrequests.  Each returns a dictionary that the template context is\nupdated with.  To register a function here, use the\ncontext_processor() decorator.\n"
    ),
    _(
        "Flask.template_context_processors() \nA dictionary with list of functions that are called without argument\nto populate the template context.  The key of the dictionary is the\nname of the blueprint this function is active for, None for all\nrequests.  Each returns a dictionary that the template context is\nupdated with.  To register a function here, use the\ncontext_processor() decorator.\n"
    ),
    _(
        "Flask.template_filter(name=None) \nA decorator that is used to register custom template filter.\nYou can specify a name for the filter, otherwise the function\nname will be used. Example:\n@app.template_filter()\ndef reverse(s):\n    return s[::-1]\n\n\n\n\n\n\nParameters:name -- the optional name of the filter, otherwise the\nfunction name will be used.\n\n\n\n"
    ),
    _(
        "Flask.template_filter(name=None) \nA decorator that is used to register custom template filter.\nYou can specify a name for the filter, otherwise the function\nname will be used. Example:\n@app.template_filter()\ndef reverse(s):\n    return s[::-1]\n\n\n\n\n\n\nParameters:name -- the optional name of the filter, otherwise the\nfunction name will be used.\n\n\n\n"
    ),
    _(
        "Flask.template_folder() \nLocation of the template files to be added to the template lookup.\nNone if templates should not be added.\n"
    ),
    _(
        "Flask.template_folder() \nLocation of the template files to be added to the template lookup.\nNone if templates should not be added.\n"
    ),
    _(
        "Flask.template_global(name=None) \nA decorator that is used to register a custom template global function.\nYou can specify a name for the global function, otherwise the function\nname will be used. Example:\n@app.template_global()\ndef double(n):\n    return 2 * n\n\n\n\nChangelog\nNew in version 0.10.\n\n\n\n\n\nParameters:name -- the optional name of the global function, otherwise the\nfunction name will be used.\n\n\n\n"
    ),
    _(
        "Flask.template_global(name=None) \nA decorator that is used to register a custom template global function.\nYou can specify a name for the global function, otherwise the function\nname will be used. Example:\n@app.template_global()\ndef double(n):\n    return 2 * n\n\n\n\nChangelog\nNew in version 0.10.\n\n\n\n\n\nParameters:name -- the optional name of the global function, otherwise the\nfunction name will be used.\n\n\n\n"
    ),
    _(
        "Flask.template_test(name=None) \nA decorator that is used to register custom template test.\nYou can specify a name for the test, otherwise the function\nname will be used. Example:\n@app.template_test()\ndef is_prime(n):\n    if n == 2:\n        return True\n    for i in range(2, int(math.ceil(math.sqrt(n))) + 1):\n        if n % i == 0:\n            return False\n    return True\n\n\n\nChangelog\nNew in version 0.10.\n\n\n\n\n\nParameters:name -- the optional name of the test, otherwise the\nfunction name will be used.\n\n\n\n"
    ),
    _(
        "Flask.template_test(name=None) \nA decorator that is used to register custom template test.\nYou can specify a name for the test, otherwise the function\nname will be used. Example:\n@app.template_test()\ndef is_prime(n):\n    if n == 2:\n        return True\n    for i in range(2, int(math.ceil(math.sqrt(n))) + 1):\n        if n % i == 0:\n            return False\n    return True\n\n\n\nChangelog\nNew in version 0.10.\n\n\n\n\n\nParameters:name -- the optional name of the test, otherwise the\nfunction name will be used.\n\n\n\n"
    ),
    _(
        "Flask.templates_auto_reload() \nReload templates when they are changed. Used by\ncreate_jinja_environment().\nThis attribute can be configured with TEMPLATES_AUTO_RELOAD. If\nnot set, it will be enabled in debug mode.\n\nNew in version 1.0: This property was added but the underlying config and behavior\nalready existed.\n\n\nChangelog"
    ),
    _(
        "Flask.templates_auto_reload() \nReload templates when they are changed. Used by\ncreate_jinja_environment().\nThis attribute can be configured with TEMPLATES_AUTO_RELOAD. If\nnot set, it will be enabled in debug mode.\n\nNew in version 1.0: This property was added but the underlying config and behavior\nalready existed.\n\n\nChangelog"
    ),
    _(
        "Flask.test_cli_runner(**kwargs) \nCreate a CLI runner for testing CLI commands.\nSee Testing CLI Commands.\nReturns an instance of test_cli_runner_class, by default\nFlaskCliRunner. The Flask app object is\npassed as the first argument.\n\nNew in version 1.0.\n\n\nChangelog"
    ),
    _(
        "Flask.test_cli_runner(**kwargs) \nCreate a CLI runner for testing CLI commands.\nSee Testing CLI Commands.\nReturns an instance of test_cli_runner_class, by default\nFlaskCliRunner. The Flask app object is\npassed as the first argument.\n\nNew in version 1.0.\n\n\nChangelog"
    ),
    _(
        "Flask.test_cli_runner_class() \nThe CliRunner subclass, by default\nFlaskCliRunner that is used by\ntest_cli_runner(). Its __init__ method should take a\nFlask app object as the first argument.\n\nNew in version 1.0.\n\n\nChangelog"
    ),
    _(
        "Flask.test_cli_runner_class() \nThe CliRunner subclass, by default\nFlaskCliRunner that is used by\ntest_cli_runner(). Its __init__ method should take a\nFlask app object as the first argument.\n\nNew in version 1.0.\n\n\nChangelog"
    ),
    _(
        "Flask.test_client(use_cookies=True, **kwargs) \nCreates a test client for this application.  For information\nabout unit testing head over to Testing Flask Applications.\nNote that if you are testing for assertions or exceptions in your\napplication code, you must set app.testing = True in order for the\nexceptions to propagate to the test client.  Otherwise, the exception\nwill be handled by the application (not visible to the test client) and\nthe only indication of an AssertionError or other exception will be a\n500 status code response to the test client.  See the testing\nattribute.  For example:\napp.testing = True\nclient = app.test_client()\n\n\nThe test client can be used in a with block to defer the closing down\nof the context until the end of the with block.  This is useful if\nyou want to access the context locals for testing:\nwith app.test_client() as c:\n    rv = c.get('/?vodka=42')\n    assert request.args['vodka'] == '42'\n\n\nAdditionally, you may pass optional keyword arguments that will then\nbe passed to the application’s test_client_class constructor.\nFor example:\nfrom flask.testing import FlaskClient\n\nclass CustomClient(FlaskClient):\n    def __init__(self, *args, **kwargs):\n        self._authentication = kwargs.pop(\"authentication\")\n        super(CustomClient,self).__init__( *args, **kwargs)\n\napp.test_client_class = CustomClient\nclient = app.test_client(authentication='Basic ....')\n\n\nSee FlaskClient for more information.\n\nChangelog\nChanged in version 0.11: Added **kwargs to support passing additional keyword arguments to\nthe constructor of test_client_class.\n\n\nNew in version 0.7: The use_cookies parameter was added as well as the ability\nto override the client to be used by setting the\ntest_client_class attribute.\n\n\nChanged in version 0.4: added support for with block usage for the client.\n\n"
    ),
    _(
        "Flask.test_client(use_cookies=True, **kwargs) \nCreates a test client for this application.  For information\nabout unit testing head over to Testing Flask Applications.\nNote that if you are testing for assertions or exceptions in your\napplication code, you must set app.testing = True in order for the\nexceptions to propagate to the test client.  Otherwise, the exception\nwill be handled by the application (not visible to the test client) and\nthe only indication of an AssertionError or other exception will be a\n500 status code response to the test client.  See the testing\nattribute.  For example:\napp.testing = True\nclient = app.test_client()\n\n\nThe test client can be used in a with block to defer the closing down\nof the context until the end of the with block.  This is useful if\nyou want to access the context locals for testing:\nwith app.test_client() as c:\n    rv = c.get('/?vodka=42')\n    assert request.args['vodka'] == '42'\n\n\nAdditionally, you may pass optional keyword arguments that will then\nbe passed to the application’s test_client_class constructor.\nFor example:\nfrom flask.testing import FlaskClient\n\nclass CustomClient(FlaskClient):\n    def __init__(self, *args, **kwargs):\n        self._authentication = kwargs.pop(\"authentication\")\n        super(CustomClient,self).__init__( *args, **kwargs)\n\napp.test_client_class = CustomClient\nclient = app.test_client(authentication='Basic ....')\n\n\nSee FlaskClient for more information.\n\nChangelog\nChanged in version 0.11: Added **kwargs to support passing additional keyword arguments to\nthe constructor of test_client_class.\n\n\nNew in version 0.7: The use_cookies parameter was added as well as the ability\nto override the client to be used by setting the\ntest_client_class attribute.\n\n\nChanged in version 0.4: added support for with block usage for the client.\n\n"
    ),
    _(
        "Flask.test_client_class() \nthe test client that is used with when test_client is used.\n\nChangelog\nNew in version 0.7.\n\n"
    ),
    _(
        "Flask.test_client_class() \nthe test client that is used with when test_client is used.\n\nChangelog\nNew in version 0.7.\n\n"
    ),
    _(
        "Flask.test_request_context(*args, **kwargs) \nCreate a RequestContext for a WSGI\nenvironment created from the given values. This is mostly useful\nduring testing, where you may want to run a function that uses\nrequest data without dispatching a full request.\nSee The Request Context.\nUse a with block to push the context, which will make\nrequest point at the request for the created\nenvironment.\nwith test_request_context(...):\n    generate_report()\n\n\nWhen using the shell, it may be easier to push and pop the\ncontext manually to avoid indentation.\nctx = app.test_request_context(...)\nctx.push()\n...\nctx.pop()\n\n\nTakes the same arguments as Werkzeug’s\nEnvironBuilder, with some defaults from\nthe application. See the linked Werkzeug docs for most of the\navailable arguments. Flask-specific behavior is listed here.\n\n\n\n\nParameters:\npath -- URL path being requested.\nbase_url -- Base URL where the app is being served, which\npath is relative to. If not given, built from\nPREFERRED_URL_SCHEME, subdomain,\nSERVER_NAME, and APPLICATION_ROOT.\nsubdomain -- Subdomain name to append to\nSERVER_NAME.\nurl_scheme -- Scheme to use instead of\nPREFERRED_URL_SCHEME.\ndata -- The request body, either as a string or a dict of\nform keys and values.\njson -- If given, this is serialized as JSON and passed as\ndata. Also defaults content_type to\napplication/json.\nargs -- other positional arguments passed to\nEnvironBuilder.\nkwargs -- other keyword arguments passed to\nEnvironBuilder.\n\n\n\n\n\n"
    ),
    _(
        "Flask.test_request_context(*args, **kwargs) \nCreate a RequestContext for a WSGI\nenvironment created from the given values. This is mostly useful\nduring testing, where you may want to run a function that uses\nrequest data without dispatching a full request.\nSee The Request Context.\nUse a with block to push the context, which will make\nrequest point at the request for the created\nenvironment.\nwith test_request_context(...):\n    generate_report()\n\n\nWhen using the shell, it may be easier to push and pop the\ncontext manually to avoid indentation.\nctx = app.test_request_context(...)\nctx.push()\n...\nctx.pop()\n\n\nTakes the same arguments as Werkzeug’s\nEnvironBuilder, with some defaults from\nthe application. See the linked Werkzeug docs for most of the\navailable arguments. Flask-specific behavior is listed here.\n\n\n\n\nParameters:\npath -- URL path being requested.\nbase_url -- Base URL where the app is being served, which\npath is relative to. If not given, built from\nPREFERRED_URL_SCHEME, subdomain,\nSERVER_NAME, and APPLICATION_ROOT.\nsubdomain -- Subdomain name to append to\nSERVER_NAME.\nurl_scheme -- Scheme to use instead of\nPREFERRED_URL_SCHEME.\ndata -- The request body, either as a string or a dict of\nform keys and values.\njson -- If given, this is serialized as JSON and passed as\ndata. Also defaults content_type to\napplication/json.\nargs -- other positional arguments passed to\nEnvironBuilder.\nkwargs -- other keyword arguments passed to\nEnvironBuilder.\n\n\n\n\n\n"
    ),
    _(
        "Flask.testing() \nThe testing flag.  Set this to True to enable the test mode of\nFlask extensions (and in the future probably also Flask itself).\nFor example this might activate test helpers that have an\nadditional runtime cost which should not be enabled by default.\nIf this is enabled and PROPAGATE_EXCEPTIONS is not changed from the\ndefault it’s implicitly enabled.\nThis attribute can also be configured from the config with the\nTESTING configuration key.  Defaults to False.\n"
    ),
    _(
        "Flask.testing() \nThe testing flag.  Set this to True to enable the test mode of\nFlask extensions (and in the future probably also Flask itself).\nFor example this might activate test helpers that have an\nadditional runtime cost which should not be enabled by default.\nIf this is enabled and PROPAGATE_EXCEPTIONS is not changed from the\ndefault it’s implicitly enabled.\nThis attribute can also be configured from the config with the\nTESTING configuration key.  Defaults to False.\n"
    ),
    _(
        "Flask.trap_http_exception(e) \nChecks if an HTTP exception should be trapped or not.  By default\nthis will return False for all exceptions except for a bad request\nkey error if TRAP_BAD_REQUEST_ERRORS is set to True.  It\nalso returns True if TRAP_HTTP_EXCEPTIONS is set to True.\nThis is called for all HTTP exceptions raised by a view function.\nIf it returns True for any exception the error handler for this\nexception is not called and it shows up as regular exception in the\ntraceback.  This is helpful for debugging implicitly raised HTTP\nexceptions.\n\nChanged in version 1.0: Bad request errors are not trapped by default in debug mode.\n\n\nChangelog\nNew in version 0.8.\n\n"
    ),
    _(
        "Flask.trap_http_exception(e) \nChecks if an HTTP exception should be trapped or not.  By default\nthis will return False for all exceptions except for a bad request\nkey error if TRAP_BAD_REQUEST_ERRORS is set to True.  It\nalso returns True if TRAP_HTTP_EXCEPTIONS is set to True.\nThis is called for all HTTP exceptions raised by a view function.\nIf it returns True for any exception the error handler for this\nexception is not called and it shows up as regular exception in the\ntraceback.  This is helpful for debugging implicitly raised HTTP\nexceptions.\n\nChanged in version 1.0: Bad request errors are not trapped by default in debug mode.\n\n\nChangelog\nNew in version 0.8.\n\n"
    ),
    _(
        "Flask.update_template_context(context) \nUpdate the template context with some commonly used variables.\nThis injects request, session, config and g into the template\ncontext as well as everything template context processors want\nto inject.  Note that the as of Flask 0.6, the original values\nin the context will not be overridden if a context processor\ndecides to return a value with the same key.\n\n\n\n\nParameters:context -- the context as a dictionary that is updated in place\nto add extra variables.\n\n\n\n"
    ),
    _(
        "Flask.update_template_context(context) \nUpdate the template context with some commonly used variables.\nThis injects request, session, config and g into the template\ncontext as well as everything template context processors want\nto inject.  Note that the as of Flask 0.6, the original values\nin the context will not be overridden if a context processor\ndecides to return a value with the same key.\n\n\n\n\nParameters:context -- the context as a dictionary that is updated in place\nto add extra variables.\n\n\n\n"
    ),
    _(
        "Flask.url_build_error_handlers() \nA list of functions that are called when url_for() raises a\nBuildError.  Each function registered here\nis called with error, endpoint and values.  If a function\nreturns None or raises a BuildError the next function is\ntried.\n\nChangelog\nNew in version 0.9.\n\n"
    ),
    _(
        "Flask.url_build_error_handlers() \nA list of functions that are called when url_for() raises a\nBuildError.  Each function registered here\nis called with error, endpoint and values.  If a function\nreturns None or raises a BuildError the next function is\ntried.\n\nChangelog\nNew in version 0.9.\n\n"
    ),
    _(
        "Flask.url_default_functions() \nA dictionary with lists of functions that can be used as URL value\npreprocessors.  The key None here is used for application wide\ncallbacks, otherwise the key is the name of the blueprint.\nEach of these functions has the chance to modify the dictionary\nof URL values before they are used as the keyword arguments of the\nview function.  For each function registered this one should also\nprovide a url_defaults() function that adds the parameters\nautomatically again that were removed that way.\n\nChangelog\nNew in version 0.7.\n\n"
    ),
    _(
        "Flask.url_default_functions() \nA dictionary with lists of functions that can be used as URL value\npreprocessors.  The key None here is used for application wide\ncallbacks, otherwise the key is the name of the blueprint.\nEach of these functions has the chance to modify the dictionary\nof URL values before they are used as the keyword arguments of the\nview function.  For each function registered this one should also\nprovide a url_defaults() function that adds the parameters\nautomatically again that were removed that way.\n\nChangelog\nNew in version 0.7.\n\n"
    ),
    _(
        "Flask.url_defaults(f) \nCallback function for URL defaults for all view functions of the\napplication.  It’s called with the endpoint and values and should\nupdate the values passed in place.\n"
    ),
    _(
        "Flask.url_defaults(f) \nCallback function for URL defaults for all view functions of the\napplication.  It’s called with the endpoint and values and should\nupdate the values passed in place.\n"
    ),
    _(
        "Flask.url_map() \nThe Map for this instance.  You can use\nthis to change the routing converters after the class was created\nbut before any routes are connected.  Example:\nfrom werkzeug.routing import BaseConverter\n\nclass ListConverter(BaseConverter):\n    def to_python(self, value):\n        return value.split(',')\n    def to_url(self, values):\n        return ','.join(super(ListConverter, self).to_url(value)\n                        for value in values)\n\napp = Flask(__name__)\napp.url_map.converters['list'] = ListConverter\n\n\n"
    ),
    _(
        "Flask.url_map() \nThe Map for this instance.  You can use\nthis to change the routing converters after the class was created\nbut before any routes are connected.  Example:\nfrom werkzeug.routing import BaseConverter\n\nclass ListConverter(BaseConverter):\n    def to_python(self, value):\n        return value.split(',')\n    def to_url(self, values):\n        return ','.join(super(ListConverter, self).to_url(value)\n                        for value in values)\n\napp = Flask(__name__)\napp.url_map.converters['list'] = ListConverter\n\n\n"
    ),
    _("Flask.url_rule_class() \nalias of werkzeug.routing.Rule\n"),
    _("Flask.url_rule_class() \nalias of werkzeug.routing.Rule\n"),
    _(
        "Flask.url_value_preprocessor(f) \nRegister a URL value preprocessor function for all view\nfunctions in the application. These functions will be called before the\nbefore_request() functions.\nThe function can modify the values captured from the matched url before\nthey are passed to the view. For example, this can be used to pop a\ncommon language code value and place it in g rather than pass it to\nevery view.\nThe function is passed the endpoint name and values dict. The return\nvalue is ignored.\n"
    ),
    _(
        "Flask.url_value_preprocessor(f) \nRegister a URL value preprocessor function for all view\nfunctions in the application. These functions will be called before the\nbefore_request() functions.\nThe function can modify the values captured from the matched url before\nthey are passed to the view. For example, this can be used to pop a\ncommon language code value and place it in g rather than pass it to\nevery view.\nThe function is passed the endpoint name and values dict. The return\nvalue is ignored.\n"
    ),
    _(
        "Flask.url_value_preprocessors() \nA dictionary with lists of functions that are called before the\nbefore_request_funcs functions. The key of the dictionary is\nthe name of the blueprint this function is active for, or None\nfor all requests. To register a function, use\nurl_value_preprocessor().\n\nChangelog\nNew in version 0.7.\n\n"
    ),
    _(
        "Flask.url_value_preprocessors() \nA dictionary with lists of functions that are called before the\nbefore_request_funcs functions. The key of the dictionary is\nthe name of the blueprint this function is active for, or None\nfor all requests. To register a function, use\nurl_value_preprocessor().\n\nChangelog\nNew in version 0.7.\n\n"
    ),
    _(
        "Flask.use_x_sendfile() \nEnable this if you want to use the X-Sendfile feature.  Keep in\nmind that the server has to support this.  This only affects files\nsent with the send_file() method.\n\nChangelog\nNew in version 0.2.\n\nThis attribute can also be configured from the config with the\nUSE_X_SENDFILE configuration key.  Defaults to False.\n"
    ),
    _(
        "Flask.use_x_sendfile() \nEnable this if you want to use the X-Sendfile feature.  Keep in\nmind that the server has to support this.  This only affects files\nsent with the send_file() method.\n\nChangelog\nNew in version 0.2.\n\nThis attribute can also be configured from the config with the\nUSE_X_SENDFILE configuration key.  Defaults to False.\n"
    ),
    _(
        "Flask.view_functions() \nA dictionary of all view functions registered.  The keys will\nbe function names which are also used to generate URLs and\nthe values are the function objects themselves.\nTo register a view function, use the route() decorator.\n"
    ),
    _(
        "Flask.view_functions() \nA dictionary of all view functions registered.  The keys will\nbe function names which are also used to generate URLs and\nthe values are the function objects themselves.\nTo register a view function, use the route() decorator.\n"
    ),
    _(
        "Flask.wsgi_app(environ, start_response) \nThe actual WSGI application. This is not implemented in\n__call__() so that middlewares can be applied without\nlosing a reference to the app object. Instead of doing this:\napp = MyMiddleware(app)\n\n\nIt’s a better idea to do this instead:\napp.wsgi_app = MyMiddleware(app.wsgi_app)\n\n\nThen you still have the original application object around and\ncan continue to call methods on it.\n\nChangelog\nChanged in version 0.7: Teardown events for the request and app contexts are called\neven if an unhandled error occurs. Other events may not be\ncalled depending on when an error occurs during dispatch.\nSee Callbacks and Errors.\n\n\n\n\n\nParameters:\nenviron -- A WSGI environment.\nstart_response -- A callable accepting a status code,\na list of headers, and an optional exception context to\nstart the response.\n\n\n\n\n\n"
    ),
    _(
        "Flask.wsgi_app(environ, start_response) \nThe actual WSGI application. This is not implemented in\n__call__() so that middlewares can be applied without\nlosing a reference to the app object. Instead of doing this:\napp = MyMiddleware(app)\n\n\nIt’s a better idea to do this instead:\napp.wsgi_app = MyMiddleware(app.wsgi_app)\n\n\nThen you still have the original application object around and\ncan continue to call methods on it.\n\nChangelog\nChanged in version 0.7: Teardown events for the request and app contexts are called\neven if an unhandled error occurs. Other events may not be\ncalled depending on when an error occurs during dispatch.\nSee Callbacks and Errors.\n\n\n\n\n\nParameters:\nenviron -- A WSGI environment.\nstart_response -- A callable accepting a status code,\na list of headers, and an optional exception context to\nstart the response.\n\n\n\n\n\n"
    ),
    _(
        "FlaskCliRunner(app, **kwargs) \nA CliRunner for testing a Flask app’s\nCLI commands. Typically created using\ntest_cli_runner(). See Testing CLI Commands.\n\n"
    ),
    _(
        "FlaskCliRunner(app, **kwargs) \nA CliRunner for testing a Flask app’s\nCLI commands. Typically created using\ntest_cli_runner(). See Testing CLI Commands.\n\n"
    ),
    _(
        "FlaskCliRunner.invoke(cli=None, args=None, **kwargs) \nInvokes a CLI command in an isolated environment. See\nCliRunner.invoke for\nfull method documentation. See Testing CLI Commands for examples.\nIf the obj argument is not given, passes an instance of\nScriptInfo that knows how to load the Flask\napp being tested.\n\n\n\n\nParameters:\ncli -- Command object to invoke. Default is the app’s\ncli group.\nargs -- List of strings to invoke the command with.\n\n\n\nReturns:a Result object.\n\n\n\n\n"
    ),
    _(
        "FlaskCliRunner.invoke(cli=None, args=None, **kwargs) \nInvokes a CLI command in an isolated environment. See\nCliRunner.invoke for\nfull method documentation. See Testing CLI Commands for examples.\nIf the obj argument is not given, passes an instance of\nScriptInfo that knows how to load the Flask\napp being tested.\n\n\n\n\nParameters:\ncli -- Command object to invoke. Default is the app’s\ncli group.\nargs -- List of strings to invoke the command with.\n\n\n\nReturns:a Result object.\n\n\n\n\n"
    ),
    _(
        "FlaskClient(*args, **kwargs) \nWorks like a regular Werkzeug test client but has some knowledge about\nhow Flask works to defer the cleanup of the request context stack to the\nend of a with body when used in a with statement.  For general\ninformation about how to use this class refer to\nwerkzeug.test.Client.\n\nBasic usage is outlined in the Testing Flask Applications chapter.\n\n"
    ),
    _(
        "FlaskClient(*args, **kwargs) \nWorks like a regular Werkzeug test client but has some knowledge about\nhow Flask works to defer the cleanup of the request context stack to the\nend of a with body when used in a with statement.  For general\ninformation about how to use this class refer to\nwerkzeug.test.Client.\n\nBasic usage is outlined in the Testing Flask Applications chapter.\n\n"
    ),
    _(
        "FlaskClient.open(*args, **kwargs) \nTakes the same arguments as the EnvironBuilder class with\nsome additions:  You can provide a EnvironBuilder or a WSGI\nenvironment as only argument instead of the EnvironBuilder\narguments and two optional keyword arguments (as_tuple, buffered)\nthat change the type of the return value or the way the application is\nexecuted.\n\nChangelog\nChanged in version 0.5: If a dict is provided as file in the dict for the data parameter\nthe content type has to be called content_type now instead of\nmimetype.  This change was made for consistency with\nwerkzeug.FileWrapper.\n\nThe follow_redirects parameter was added to open().\n\nAdditional parameters:\n\n\n\n\nParameters:\nas_tuple -- Returns a tuple in the form (environ, result)\nbuffered -- Set this to True to buffer the application run.\nThis will automatically close the application for\nyou as well.\nfollow_redirects -- Set this to True if the Client should\nfollow HTTP redirects.\n\n\n\n\n\n"
    ),
    _(
        "FlaskClient.open(*args, **kwargs) \nTakes the same arguments as the EnvironBuilder class with\nsome additions:  You can provide a EnvironBuilder or a WSGI\nenvironment as only argument instead of the EnvironBuilder\narguments and two optional keyword arguments (as_tuple, buffered)\nthat change the type of the return value or the way the application is\nexecuted.\n\nChangelog\nChanged in version 0.5: If a dict is provided as file in the dict for the data parameter\nthe content type has to be called content_type now instead of\nmimetype.  This change was made for consistency with\nwerkzeug.FileWrapper.\n\nThe follow_redirects parameter was added to open().\n\nAdditional parameters:\n\n\n\n\nParameters:\nas_tuple -- Returns a tuple in the form (environ, result)\nbuffered -- Set this to True to buffer the application run.\nThis will automatically close the application for\nyou as well.\nfollow_redirects -- Set this to True if the Client should\nfollow HTTP redirects.\n\n\n\n\n\n"
    ),
    _(
        "FlaskClient.session_transaction(*args, **kwargs) \nWhen used in combination with a with statement this opens a\nsession transaction.  This can be used to modify the session that\nthe test client uses.  Once the with block is left the session is\nstored back.\nwith client.session_transaction() as session:\n    session['value'] = 42\n\n\nInternally this is implemented by going through a temporary test\nrequest context and since session handling could depend on\nrequest variables this function accepts the same arguments as\ntest_request_context() which are directly\npassed through.\n"
    ),
    _(
        "FlaskClient.session_transaction(*args, **kwargs) \nWhen used in combination with a with statement this opens a\nsession transaction.  This can be used to modify the session that\nthe test client uses.  Once the with block is left the session is\nstored back.\nwith client.session_transaction() as session:\n    session['value'] = 42\n\n\nInternally this is implemented by going through a temporary test\nrequest context and since session handling could depend on\nrequest variables this function accepts the same arguments as\ntest_request_context() which are directly\npassed through.\n"
    ),
    _(
        "FlaskGroup(add_default_commands=True, create_app=None, add_version_option=True, load_dotenv=True, **extra) \nSpecial subclass of the AppGroup group that supports\nloading more commands from the configured Flask app.  Normally a\ndeveloper does not have to interface with this class but there are\nsome very advanced use cases for which it makes sense to create an\ninstance of this.\n\nFor information as of why this is useful see Custom Scripts.\n\n\nParameters:\nadd_default_commands -- if this is True then the default run and\nshell commands wil be added.\nadd_version_option -- adds the --version option.\ncreate_app -- an optional callback that is passed the script info and\nreturns the loaded app.\nload_dotenv -- Load the nearest .env and .flaskenv\nfiles to set environment variables. Will also change the working\ndirectory to the directory containing the first file found."
    ),
    _(
        "FlaskGroup(add_default_commands=True, create_app=None, add_version_option=True, load_dotenv=True, **extra) \nSpecial subclass of the AppGroup group that supports\nloading more commands from the configured Flask app.  Normally a\ndeveloper does not have to interface with this class but there are\nsome very advanced use cases for which it makes sense to create an\ninstance of this.\n\nFor information as of why this is useful see Custom Scripts.\n\n\nParameters:\nadd_default_commands -- if this is True then the default run and\nshell commands wil be added.\nadd_version_option -- adds the --version option.\ncreate_app -- an optional callback that is passed the script info and\nreturns the loaded app.\nload_dotenv -- Load the nearest .env and .flaskenv\nfiles to set environment variables. Will also change the working\ndirectory to the directory containing the first file found."
    ),
    _(
        "FlaskGroup.get_command(ctx, name) \nGiven a context and a command name, this returns a\nCommand object if it exists or returns None.\n"
    ),
    _(
        "FlaskGroup.get_command(ctx, name) \nGiven a context and a command name, this returns a\nCommand object if it exists or returns None.\n"
    ),
    _(
        "FlaskGroup.list_commands(ctx) \nReturns a list of subcommand names in the order they should\nappear.\n"
    ),
    _(
        "FlaskGroup.list_commands(ctx) \nReturns a list of subcommand names in the order they should\nappear.\n"
    ),
    _(
        'FlaskGroup.main(*args, **kwargs) \nThis is the way to invoke a script with all the bells and\nwhistles as a command line application.  This will always terminate\nthe application after a call.  If this is not wanted, SystemExit\nneeds to be caught.\nThis method is also available by directly calling the instance of\na Command.\n\nNew in version 3.0: Added the standalone_mode flag to control the standalone mode.\n\n\nChangelog\n\n\n\nParameters:\nargs -- the arguments that should be used for parsing.  If not\nprovided, sys.argv[1:] is used.\nprog_name -- the program name that should be used.  By default\nthe program name is constructed by taking the file\nname from sys.argv[0].\ncomplete_var -- the environment variable that controls the\nbash completion support.  The default is\n"_<prog_name>_COMPLETE" with prog name in\nuppercase.\nstandalone_mode -- the default behavior is to invoke the script\nin standalone mode.  Click will then\nhandle exceptions and convert them into\nerror messages and the function will never\nreturn but shut down the interpreter.  If\nthis is set to False they will be\npropagated to the caller and the return\nvalue of this function is the return value\nof invoke().\nextra -- extra keyword arguments are forwarded to the context\nconstructor.  See Context for more information.\n\n\n\n\n\n'
    ),
    _(
        'FlaskGroup.main(*args, **kwargs) \nThis is the way to invoke a script with all the bells and\nwhistles as a command line application.  This will always terminate\nthe application after a call.  If this is not wanted, SystemExit\nneeds to be caught.\nThis method is also available by directly calling the instance of\na Command.\n\nNew in version 3.0: Added the standalone_mode flag to control the standalone mode.\n\n\nChangelog\n\n\n\nParameters:\nargs -- the arguments that should be used for parsing.  If not\nprovided, sys.argv[1:] is used.\nprog_name -- the program name that should be used.  By default\nthe program name is constructed by taking the file\nname from sys.argv[0].\ncomplete_var -- the environment variable that controls the\nbash completion support.  The default is\n"_<prog_name>_COMPLETE" with prog name in\nuppercase.\nstandalone_mode -- the default behavior is to invoke the script\nin standalone mode.  Click will then\nhandle exceptions and convert them into\nerror messages and the function will never\nreturn but shut down the interpreter.  If\nthis is set to False they will be\npropagated to the caller and the return\nvalue of this function is the return value\nof invoke().\nextra -- extra keyword arguments are forwarded to the context\nconstructor.  See Context for more information.\n\n\n\n\n\n'
    ),
    _(
        "JSONDecoder(*, object_hook=None, parse_float=None, parse_int=None, parse_constant=None, strict=True, object_pairs_hook=None) \nThe default JSON decoder.  This one does not change the behavior from\nthe default simplejson decoder.  Consult the json documentation\nfor more information.  This decoder is not only used for the load\nfunctions of this module but also Request.\n\n"
    ),
    _(
        "JSONDecoder(*, object_hook=None, parse_float=None, parse_int=None, parse_constant=None, strict=True, object_pairs_hook=None) \nThe default JSON decoder.  This one does not change the behavior from\nthe default simplejson decoder.  Consult the json documentation\nfor more information.  This decoder is not only used for the load\nfunctions of this module but also Request.\n\n"
    ),
    _(
        "JSONEncoder(*, skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True, sort_keys=False, indent=None, separators=None, default=None) \nThe default Flask JSON encoder.  This one extends the default simplejson\nencoder by also supporting datetime objects, UUID as well as\nMarkup objects which are serialized as RFC 822 datetime strings (same\nas the HTTP date format).  In order to support more data types override the\ndefault() method.\n\n"
    ),
    _(
        "JSONEncoder(*, skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True, sort_keys=False, indent=None, separators=None, default=None) \nThe default Flask JSON encoder.  This one extends the default simplejson\nencoder by also supporting datetime objects, UUID as well as\nMarkup objects which are serialized as RFC 822 datetime strings (same\nas the HTTP date format).  In order to support more data types override the\ndefault() method.\n\n"
    ),
    _(
        "JSONEncoder.default(o) \nImplement this method in a subclass such that it returns a\nserializable object for o, or calls the base implementation (to\nraise a TypeError).\nFor example, to support arbitrary iterators, you could implement\ndefault like this:\ndef default(self, o):\n    try:\n        iterable = iter(o)\n    except TypeError:\n        pass\n    else:\n        return list(iterable)\n    return JSONEncoder.default(self, o)\n\n\n"
    ),
    _(
        "JSONEncoder.default(o) \nImplement this method in a subclass such that it returns a\nserializable object for o, or calls the base implementation (to\nraise a TypeError).\nFor example, to support arbitrary iterators, you could implement\ndefault like this:\ndef default(self, o):\n    try:\n        iterable = iter(o)\n    except TypeError:\n        pass\n    else:\n        return list(iterable)\n    return JSONEncoder.default(self, o)\n\n\n"
    ),
    _(
        "JSONTag(serializer) \nBase class for defining type tags for TaggedJSONSerializer.\n\n"
    ),
    _(
        "JSONTag(serializer) \nBase class for defining type tags for TaggedJSONSerializer.\n\n"
    ),
    _(
        "JSONTag.check(value) \nCheck if the given value should be tagged by this tag.\n"
    ),
    _(
        "JSONTag.check(value) \nCheck if the given value should be tagged by this tag.\n"
    ),
    _(
        "JSONTag.key() \nThe tag to mark the serialized object with. If None, this tag is\nonly used as an intermediate step during tagging.\n"
    ),
    _(
        "JSONTag.key() \nThe tag to mark the serialized object with. If None, this tag is\nonly used as an intermediate step during tagging.\n"
    ),
    _(
        "JSONTag.tag(value) \nConvert the value to a valid JSON type and add the tag structure\naround it.\n"
    ),
    _(
        "JSONTag.tag(value) \nConvert the value to a valid JSON type and add the tag structure\naround it.\n"
    ),
    _(
        "JSONTag.to_json(value) \nConvert the Python object to an object that is a valid JSON type.\nThe tag will be added later.\n"
    ),
    _(
        "JSONTag.to_json(value) \nConvert the Python object to an object that is a valid JSON type.\nThe tag will be added later.\n"
    ),
    _(
        "JSONTag.to_python(value) \nConvert the JSON representation back to the correct type. The tag\nwill already be removed.\n"
    ),
    _(
        "JSONTag.to_python(value) \nConvert the JSON representation back to the correct type. The tag\nwill already be removed.\n"
    ),
    _(
        "Markup() \nMarks a string as being safe for inclusion in HTML/XML output without\nneeding to be escaped.  This implements the __html__ interface a couple\nof frameworks and web applications use.  Markup is a direct\nsubclass of unicode and provides all the methods of unicode just that\nit escapes arguments passed and always returns Markup.\n\nThe escape function returns markup objects so that double escaping can’t\nhappen.\n\nThe constructor of the Markup class can be used for three\ndifferent things:  When passed an unicode object it’s assumed to be safe,\nwhen passed an object with an HTML representation (has an __html__\nmethod) that representation is used, otherwise the object passed is\nconverted into a unicode string and then assumed to be safe:\n\nIf you want object passed being always treated as unsafe you can use the\nescape() classmethod to create a Markup object:\n\nOperations on a markup string are markup aware which means that all\narguments are passed through the escape() function:\n\n"
    ),
    _(
        "Markup() \nMarks a string as being safe for inclusion in HTML/XML output without\nneeding to be escaped.  This implements the __html__ interface a couple\nof frameworks and web applications use.  Markup is a direct\nsubclass of unicode and provides all the methods of unicode just that\nit escapes arguments passed and always returns Markup.\n\nThe escape function returns markup objects so that double escaping can’t\nhappen.\n\nThe constructor of the Markup class can be used for three\ndifferent things:  When passed an unicode object it’s assumed to be safe,\nwhen passed an object with an HTML representation (has an __html__\nmethod) that representation is used, otherwise the object passed is\nconverted into a unicode string and then assumed to be safe:\n\nIf you want object passed being always treated as unsafe you can use the\nescape() classmethod to create a Markup object:\n\nOperations on a markup string are markup aware which means that all\narguments are passed through the escape() function:\n\n"
    ),
    _(
        "Markup.striptags() \nUnescape markup into an text_type string and strip all tags.  This\nalso resolves known HTML4 and XHTML entities.  Whitespace is\nnormalized to one:\n>>> Markup(\"Main &raquo;  <em>About</em>\").striptags()\nu'Main \\xbb About'\n\n\n"
    ),
    _(
        "Markup.striptags() \nUnescape markup into an text_type string and strip all tags.  This\nalso resolves known HTML4 and XHTML entities.  Whitespace is\nnormalized to one:\n>>> Markup(\"Main &raquo;  <em>About</em>\").striptags()\nu'Main \\xbb About'\n\n\n"
    ),
    _(
        "Markup.unescape() \nUnescape markup again into an text_type string.  This also resolves\nknown HTML4 and XHTML entities:\n>>> Markup(\"Main &raquo; <em>About</em>\").unescape()\nu'Main \\xbb <em>About</em>'\n\n\n"
    ),
    _(
        "Markup.unescape() \nUnescape markup again into an text_type string.  This also resolves\nknown HTML4 and XHTML entities:\n>>> Markup(\"Main &raquo; <em>About</em>\").unescape()\nu'Main \\xbb <em>About</em>'\n\n\n"
    ),
    _(
        "MethodView() \nA class-based view that dispatches request methods to the corresponding\nclass methods. For example, if you implement a get method, it will be\nused to handle GET requests.\n\n"
    ),
    _(
        "MethodView() \nA class-based view that dispatches request methods to the corresponding\nclass methods. For example, if you implement a get method, it will be\nused to handle GET requests.\n\n"
    ),
    _(
        "MethodView.dispatch_request(*args, **kwargs) \nSubclasses have to override this method to implement the\nactual view function code.  This method is called with all\nthe arguments from the URL rule.\n"
    ),
    _(
        "MethodView.dispatch_request(*args, **kwargs) \nSubclasses have to override this method to implement the\nactual view function code.  This method is called with all\nthe arguments from the URL rule.\n"
    ),
    _(
        "Namespace() \nAn alias for blinker.base.Namespace if blinker is available,\notherwise a dummy class that creates fake signals.  This class is\navailable for Flask extensions that want to provide the same fallback\nsystem as Flask itself.\n\n"
    ),
    _(
        "Namespace() \nAn alias for blinker.base.Namespace if blinker is available,\notherwise a dummy class that creates fake signals.  This class is\navailable for Flask extensions that want to provide the same fallback\nsystem as Flask itself.\n\n"
    ),
    _(
        "Namespace.signal(name, doc=None) \nCreates a new signal for this namespace if blinker is available,\notherwise returns a fake signal that has a send method that will\ndo nothing but will fail with a RuntimeError for all other\noperations, including connecting.\n"
    ),
    _(
        "Namespace.signal(name, doc=None) \nCreates a new signal for this namespace if blinker is available,\notherwise returns a fake signal that has a send method that will\ndo nothing but will fail with a RuntimeError for all other\noperations, including connecting.\n"
    ),
    _(
        "NullSession(initial=None) \nClass used to generate nicer error messages if sessions are not\navailable.  Will still allow read-only access to the empty session\nbut fail on setting.\n\n"
    ),
    _(
        "NullSession(initial=None) \nClass used to generate nicer error messages if sessions are not\navailable.  Will still allow read-only access to the empty session\nbut fail on setting.\n\n"
    ),
    _(
        "Request(environ, populate_request=True, shallow=False) \nThe request object used by default in Flask.  Remembers the\nmatched endpoint and view arguments.\n\nIt is what ends up as request.  If you want to replace\nthe request object used you can subclass this and set\nrequest_class to your subclass.\n\nThe request object is a Request subclass and\nprovides all of the attributes Werkzeug defines plus a few Flask\nspecific ones.\n\n"
    ),
    _(
        "Request(environ, populate_request=True, shallow=False) \nThe request object used by default in Flask.  Remembers the\nmatched endpoint and view arguments.\n\nIt is what ends up as request.  If you want to replace\nthe request object used you can subclass this and set\nrequest_class to your subclass.\n\nThe request object is a Request subclass and\nprovides all of the attributes Werkzeug defines plus a few Flask\nspecific ones.\n\n"
    ),
    _(
        "Request.accept_charsets() \nList of charsets this client supports as\nCharsetAccept object.\n"
    ),
    _(
        "Request.accept_charsets() \nList of charsets this client supports as\nCharsetAccept object.\n"
    ),
    _(
        "Request.accept_encodings() \nList of encodings this client accepts.  Encodings in a HTTP term\nare compression encodings such as gzip.  For charsets have a look at\naccept_charset.\n"
    ),
    _(
        "Request.accept_encodings() \nList of encodings this client accepts.  Encodings in a HTTP term\nare compression encodings such as gzip.  For charsets have a look at\naccept_charset.\n"
    ),
    _(
        "Request.accept_languages() \nList of languages this client accepts as\nLanguageAccept object.\n"
    ),
    _(
        "Request.accept_languages() \nList of languages this client accepts as\nLanguageAccept object.\n"
    ),
    _(
        "Request.accept_mimetypes() \nList of mimetypes this client supports as\nMIMEAccept object.\n"
    ),
    _(
        "Request.accept_mimetypes() \nList of mimetypes this client supports as\nMIMEAccept object.\n"
    ),
    _(
        "Request.access_route() \nIf a forwarded header exists this is a list of all ip addresses\nfrom the client ip to the last proxy server.\n"
    ),
    _(
        "Request.access_route() \nIf a forwarded header exists this is a list of all ip addresses\nfrom the client ip to the last proxy server.\n"
    ),
    _(
        "Request.args() \nThe parsed URL parameters (the part in the URL after the question\nmark).\nBy default an\nImmutableMultiDict\nis returned from this function.  This can be changed by setting\nparameter_storage_class to a different type.  This might\nbe necessary if the order of the form data is important.\n"
    ),
    _(
        "Request.args() \nThe parsed URL parameters (the part in the URL after the question\nmark).\nBy default an\nImmutableMultiDict\nis returned from this function.  This can be changed by setting\nparameter_storage_class to a different type.  This might\nbe necessary if the order of the form data is important.\n"
    ),
    _("Request.authorization() \nThe Authorization object in parsed form.\n"),
    _("Request.authorization() \nThe Authorization object in parsed form.\n"),
    _("Request.base_url() \n"),
    _(
        "Request.base_url() \nLike url but without the querystring\nSee also: trusted_hosts.\n"
    ),
    _("Request.base_url() \n"),
    _(
        "Request.base_url() \nLike url but without the querystring\nSee also: trusted_hosts.\n"
    ),
    _("Request.blueprint() \nThe name of the current blueprint\n"),
    _("Request.blueprint() \nThe name of the current blueprint\n"),
    _(
        "Request.cache_control() \nA RequestCacheControl object\nfor the incoming cache control headers.\n"
    ),
    _(
        "Request.cache_control() \nA RequestCacheControl object\nfor the incoming cache control headers.\n"
    ),
    _(
        "Request.close() \nCloses associated resources of this request object.  This\ncloses all file handles explicitly.  You can also use the request\nobject in a with statement which will automatically close it.\n\nChangelog\nNew in version 0.9.\n\n"
    ),
    _(
        "Request.close() \nCloses associated resources of this request object.  This\ncloses all file handles explicitly.  You can also use the request\nobject in a with statement which will automatically close it.\n\nChangelog\nNew in version 0.9.\n\n"
    ),
    _(
        "Request.content_encoding() \nThe Content-Encoding entity-header field is used as a modifier to the\nmedia-type.  When present, its value indicates what additional content\ncodings have been applied to the entity-body, and thus what decoding\nmechanisms must be applied in order to obtain the media-type\nreferenced by the Content-Type header field.\n\nChangelog\nNew in version 0.9.\n\n"
    ),
    _(
        "Request.content_encoding() \nThe Content-Encoding entity-header field is used as a modifier to the\nmedia-type.  When present, its value indicates what additional content\ncodings have been applied to the entity-body, and thus what decoding\nmechanisms must be applied in order to obtain the media-type\nreferenced by the Content-Type header field.\n\nChangelog\nNew in version 0.9.\n\n"
    ),
    _(
        "Request.content_length() \nThe Content-Length entity-header field indicates the size of the\nentity-body in bytes or, in the case of the HEAD method, the size of\nthe entity-body that would have been sent had the request been a\nGET.\n"
    ),
    _(
        "Request.content_length() \nThe Content-Length entity-header field indicates the size of the\nentity-body in bytes or, in the case of the HEAD method, the size of\nthe entity-body that would have been sent had the request been a\nGET.\n"
    ),
    _(
        "Request.content_md5() \n\nThe Content-MD5 entity-header field, as defined in RFC 1864, is an\nMD5 digest of the entity-body for the purpose of providing an\nend-to-end message integrity check (MIC) of the entity-body.  (Note:\na MIC is good for detecting accidental modification of the\nentity-body in transit, but is not proof against malicious attacks.)\n\nChangelog\nNew in version 0.9.\n\n"
    ),
    _(
        "Request.content_md5() \n\nThe Content-MD5 entity-header field, as defined in RFC 1864, is an\nMD5 digest of the entity-body for the purpose of providing an\nend-to-end message integrity check (MIC) of the entity-body.  (Note:\na MIC is good for detecting accidental modification of the\nentity-body in transit, but is not proof against malicious attacks.)\n\nChangelog\nNew in version 0.9.\n\n"
    ),
    _(
        "Request.content_type() \nThe Content-Type entity-header field indicates the media type of\nthe entity-body sent to the recipient or, in the case of the HEAD\nmethod, the media type that would have been sent had the request\nbeen a GET.\n"
    ),
    _(
        "Request.content_type() \nThe Content-Type entity-header field indicates the media type of\nthe entity-body sent to the recipient or, in the case of the HEAD\nmethod, the media type that would have been sent had the request\nbeen a GET.\n"
    ),
    _(
        "Request.cookies() \nA dict with the contents of all cookies transmitted with\nthe request.\n"
    ),
    _(
        "Request.cookies() \nA dict with the contents of all cookies transmitted with\nthe request.\n"
    ),
    _(
        "Request.data() \nContains the incoming request data as string in case it came with\na mimetype Werkzeug does not handle.\n"
    ),
    _(
        "Request.data() \nContains the incoming request data as string in case it came with\na mimetype Werkzeug does not handle.\n"
    ),
    _(
        "Request.date() \nThe Date general-header field represents the date and time at which\nthe message was originated, having the same semantics as orig-date\nin RFC 822.\n"
    ),
    _(
        "Request.date() \nThe Date general-header field represents the date and time at which\nthe message was originated, having the same semantics as orig-date\nin RFC 822.\n"
    ),
    _(
        "Request.dict_storage_class() \nalias of werkzeug.datastructures.ImmutableTypeConversionDict\n"
    ),
    _(
        "Request.dict_storage_class() \nalias of werkzeug.datastructures.ImmutableTypeConversionDict\n"
    ),
    _(
        "Request.endpoint() \nThe endpoint that matched the request.  This in combination with\nview_args can be used to reconstruct the same or a\nmodified URL.  If an exception happened when matching, this will\nbe None.\n"
    ),
    _(
        "Request.endpoint() \nThe endpoint that matched the request.  This in combination with\nview_args can be used to reconstruct the same or a\nmodified URL.  If an exception happened when matching, this will\nbe None.\n"
    ),
    _("Request.environ() \nThe underlying WSGI environment.\n"),
    _("Request.environ() \nThe underlying WSGI environment.\n"),
    _(
        'Request.files() \nMultiDict object containing\nall uploaded files.  Each key in files is the name from the\n<input type="file" name="">.  Each value in files is a\nWerkzeug FileStorage object.\nIt basically behaves like a standard file object you know from Python,\nwith the difference that it also has a\nsave() function that can\nstore the file on the filesystem.\nNote that files will only contain data if the request method was\nPOST, PUT or PATCH and the <form> that posted to the request had\nenctype="multipart/form-data".  It will be empty otherwise.\nSee the MultiDict /\nFileStorage documentation for\nmore details about the used data structure.\n'
    ),
    _(
        'Request.files() \nMultiDict object containing\nall uploaded files.  Each key in files is the name from the\n<input type="file" name="">.  Each value in files is a\nWerkzeug FileStorage object.\nIt basically behaves like a standard file object you know from Python,\nwith the difference that it also has a\nsave() function that can\nstore the file on the filesystem.\nNote that files will only contain data if the request method was\nPOST, PUT or PATCH and the <form> that posted to the request had\nenctype="multipart/form-data".  It will be empty otherwise.\nSee the MultiDict /\nFileStorage documentation for\nmore details about the used data structure.\n'
    ),
    _(
        "Request.form() \nThe form parameters.  By default an\nImmutableMultiDict\nis returned from this function.  This can be changed by setting\nparameter_storage_class to a different type.  This might\nbe necessary if the order of the form data is important.\nPlease keep in mind that file uploads will not end up here, but instead\nin the files attribute.\n\nChangelog\nChanged in version 0.9: Previous to Werkzeug 0.9 this would only contain form data for POST\nand PUT requests.\n\n"
    ),
    _(
        "Request.form() \nThe form parameters.  By default an\nImmutableMultiDict\nis returned from this function.  This can be changed by setting\nparameter_storage_class to a different type.  This might\nbe necessary if the order of the form data is important.\nPlease keep in mind that file uploads will not end up here, but instead\nin the files attribute.\n\nChangelog\nChanged in version 0.9: Previous to Werkzeug 0.9 this would only contain form data for POST\nand PUT requests.\n\n"
    ),
    _(
        "Request.form_data_parser_class() \nalias of werkzeug.formparser.FormDataParser\n"
    ),
    _(
        "Request.form_data_parser_class() \nalias of werkzeug.formparser.FormDataParser\n"
    ),
    _("Request.full_path() \n"),
    _(
        "Request.full_path() \nRequested path as unicode, including the query string.\n"
    ),
    _("Request.full_path() \n"),
    _(
        "Request.full_path() \nRequested path as unicode, including the query string.\n"
    ),
    _(
        "Request.get_data(cache=True, as_text=False, parse_form_data=False) \nThis reads the buffered incoming data from the client into one\nbytestring.  By default this is cached but that behavior can be\nchanged by setting cache to False.\nUsually it’s a bad idea to call this method without checking the\ncontent length first as a client could send dozens of megabytes or more\nto cause memory problems on the server.\nNote that if the form data was already parsed this method will not\nreturn anything as form data parsing does not cache the data like\nthis method does.  To implicitly invoke form data parsing function\nset parse_form_data to True.  When this is done the return value\nof this method will be an empty string if the form parser handles\nthe data.  This generally is not necessary as if the whole data is\ncached (which is the default) the form parser will used the cached\ndata to parse the form data.  Please be generally aware of checking\nthe content length first in any case before calling this method\nto avoid exhausting server memory.\nIf as_text is set to True the return value will be a decoded\nunicode string.\n\nChangelog\nNew in version 0.9.\n\n"
    ),
    _(
        "Request.get_data(cache=True, as_text=False, parse_form_data=False) \nThis reads the buffered incoming data from the client into one\nbytestring.  By default this is cached but that behavior can be\nchanged by setting cache to False.\nUsually it’s a bad idea to call this method without checking the\ncontent length first as a client could send dozens of megabytes or more\nto cause memory problems on the server.\nNote that if the form data was already parsed this method will not\nreturn anything as form data parsing does not cache the data like\nthis method does.  To implicitly invoke form data parsing function\nset parse_form_data to True.  When this is done the return value\nof this method will be an empty string if the form parser handles\nthe data.  This generally is not necessary as if the whole data is\ncached (which is the default) the form parser will used the cached\ndata to parse the form data.  Please be generally aware of checking\nthe content length first in any case before calling this method\nto avoid exhausting server memory.\nIf as_text is set to True the return value will be a decoded\nunicode string.\n\nChangelog\nNew in version 0.9.\n\n"
    ),
    _(
        'Request.get_json(force=False, silent=False, cache=True, <em class="mimetype">application/json) \nParse and return the data as JSON. If the mimetype does not\nindicate JSON (application/json, see\nis_json()), this returns None unless force is\ntrue. If parsing fails, on_json_loading_failed() is called\nand its return value is used as the return value.\n\n\n\n\nParameters:\nforce -- Ignore the mimetype and always try to parse JSON.\nsilent -- Silence parsing errors and return None\ninstead.\ncache -- Store the parsed JSON to return for subsequent\ncalls.\n\n\n\n\n\n'
    ),
    _(
        'Request.get_json(force=False, silent=False, cache=True, <em class="mimetype">application/json) \nParse and return the data as JSON. If the mimetype does not\nindicate JSON (application/json, see\nis_json()), this returns None unless force is\ntrue. If parsing fails, on_json_loading_failed() is called\nand its return value is used as the return value.\n\n\n\n\nParameters:\nforce -- Ignore the mimetype and always try to parse JSON.\nsilent -- Silence parsing errors and return None\ninstead.\ncache -- Store the parsed JSON to return for subsequent\ncalls.\n\n\n\n\n\n'
    ),
    _(
        "Request.headers() \nThe headers from the WSGI environ as immutable\nEnvironHeaders.\n"
    ),
    _(
        "Request.headers() \nThe headers from the WSGI environ as immutable\nEnvironHeaders.\n"
    ),
    _(
        "Request.host() \nJust the host including the port if available.\nSee also: trusted_hosts.\n"
    ),
    _(
        "Request.host() \nJust the host including the port if available.\nSee also: trusted_hosts.\n"
    ),
    _(
        "Request.host_url() \nJust the host with scheme as IRI.\nSee also: trusted_hosts.\n"
    ),
    _(
        "Request.host_url() \nJust the host with scheme as IRI.\nSee also: trusted_hosts.\n"
    ),
    _(
        "Request.if_match() \nAn object containing all the etags in the If-Match header.\n\n\n\n\nReturn type:ETags\n\n\n\n"
    ),
    _(
        "Request.if_match() \nAn object containing all the etags in the If-Match header.\n\n\n\n\nReturn type:ETags\n\n\n\n"
    ),
    _(
        "Request.if_modified_since() \nThe parsed If-Modified-Since header as datetime object.\n"
    ),
    _(
        "Request.if_modified_since() \nThe parsed If-Modified-Since header as datetime object.\n"
    ),
    _(
        "Request.if_none_match() \nAn object containing all the etags in the If-None-Match header.\n\n\n\n\nReturn type:ETags\n\n\n\n"
    ),
    _(
        "Request.if_none_match() \nAn object containing all the etags in the If-None-Match header.\n\n\n\n\nReturn type:ETags\n\n\n\n"
    ),
    _(
        "Request.if_range() \nThe parsed If-Range header.\n\nChangelog\nNew in version 0.7.\n\n\n\n\n\nReturn type:IfRange\n\n\n\n"
    ),
    _(
        "Request.if_range() \nThe parsed If-Range header.\n\nChangelog\nNew in version 0.7.\n\n\n\n\n\nReturn type:IfRange\n\n\n\n"
    ),
    _(
        "Request.if_unmodified_since() \nThe parsed If-Unmodified-Since header as datetime object.\n"
    ),
    _(
        "Request.if_unmodified_since() \nThe parsed If-Unmodified-Since header as datetime object.\n"
    ),
    _(
        "Request.is_json() \nCheck if the mimetype indicates JSON data, either\napplication/json or application/*+json.\n\nChangelog\nNew in version 0.11.\n\n"
    ),
    _(
        "Request.is_json() \nCheck if the mimetype indicates JSON data, either\napplication/json or application/*+json.\n\nChangelog\nNew in version 0.11.\n\n"
    ),
    _(
        "Request.is_multiprocess() \nboolean that is True if the application is served by\na WSGI server that spawns multiple processes.\n"
    ),
    _(
        "Request.is_multiprocess() \nboolean that is True if the application is served by\na WSGI server that spawns multiple processes.\n"
    ),
    _(
        "Request.is_multithread() \nboolean that is True if the application is served by\na multithreaded WSGI server.\n"
    ),
    _(
        "Request.is_multithread() \nboolean that is True if the application is served by\na multithreaded WSGI server.\n"
    ),
    _(
        "Request.is_run_once() \nboolean that is True if the application will be executed only\nonce in a process lifetime.  This is the case for CGI for example,\nbut it’s not guaranteed that the execution only happens one time.\n"
    ),
    _(
        "Request.is_run_once() \nboolean that is True if the application will be executed only\nonce in a process lifetime.  This is the case for CGI for example,\nbut it’s not guaranteed that the execution only happens one time.\n"
    ),
    _("Request.is_secure() \nTrue if the request is secure.\n"),
    _("Request.is_secure() \nTrue if the request is secure.\n"),
    _(
        "Request.is_xhr() \nTrue if the request was triggered via a JavaScript XMLHttpRequest.\nThis only works with libraries that support the X-Requested-With\nheader and set it to “XMLHttpRequest”.  Libraries that do that are\nprototype, jQuery and Mochikit and probably some more.\n\nDeprecated since version 0.13: X-Requested-With is not standard and is unreliable.\n\n\nChangelog"
    ),
    _(
        "Request.is_xhr() \nTrue if the request was triggered via a JavaScript XMLHttpRequest.\nThis only works with libraries that support the X-Requested-With\nheader and set it to “XMLHttpRequest”.  Libraries that do that are\nprototype, jQuery and Mochikit and probably some more.\n\nDeprecated since version 0.13: X-Requested-With is not standard and is unreliable.\n\n\nChangelog"
    ),
    _(
        "Request.json() \nThis will contain the parsed JSON data if the mimetype indicates\nJSON (application/json, see is_json()), otherwise it\nwill be None.\n"
    ),
    _(
        "Request.json() \nThis will contain the parsed JSON data if the mimetype indicates\nJSON (application/json, see is_json()), otherwise it\nwill be None.\n"
    ),
    _(
        "Request.list_storage_class() \nalias of werkzeug.datastructures.ImmutableList\n"
    ),
    _(
        "Request.list_storage_class() \nalias of werkzeug.datastructures.ImmutableList\n"
    ),
    _(
        "Request.make_form_data_parser() \nCreates the form data parser. Instantiates the\nform_data_parser_class with some parameters.\n\nChangelog\nNew in version 0.8.\n\n"
    ),
    _(
        "Request.make_form_data_parser() \nCreates the form data parser. Instantiates the\nform_data_parser_class with some parameters.\n\nChangelog\nNew in version 0.8.\n\n"
    ),
    _(
        "Request.max_content_length() \nRead-only view of the MAX_CONTENT_LENGTH config key.\n"
    ),
    _(
        "Request.max_content_length() \nRead-only view of the MAX_CONTENT_LENGTH config key.\n"
    ),
    _(
        "Request.max_forwards() \nThe Max-Forwards request-header field provides a mechanism with the\nTRACE and OPTIONS methods to limit the number of proxies or gateways\nthat can forward the request to the next inbound server.\n"
    ),
    _(
        "Request.max_forwards() \nThe Max-Forwards request-header field provides a mechanism with the\nTRACE and OPTIONS methods to limit the number of proxies or gateways\nthat can forward the request to the next inbound server.\n"
    ),
    _(
        "Request.method() \nThe request method. (For example 'GET' or 'POST').\n"
    ),
    _(
        "Request.method() \nThe request method. (For example 'GET' or 'POST').\n"
    ),
    _(
        "Request.mimetype() \nLike content_type, but without parameters (eg, without\ncharset, type etc.) and always lowercase.  For example if the content\ntype is text/HTML; charset=utf-8 the mimetype would be\n'text/html'.\n"
    ),
    _(
        "Request.mimetype() \nLike content_type, but without parameters (eg, without\ncharset, type etc.) and always lowercase.  For example if the content\ntype is text/HTML; charset=utf-8 the mimetype would be\n'text/html'.\n"
    ),
    _(
        "Request.mimetype_params() \nThe mimetype parameters as dict.  For example if the content\ntype is text/html; charset=utf-8 the params would be\n{'charset': 'utf-8'}.\n"
    ),
    _(
        "Request.mimetype_params() \nThe mimetype parameters as dict.  For example if the content\ntype is text/html; charset=utf-8 the params would be\n{'charset': 'utf-8'}.\n"
    ),
    _(
        "Request.on_json_loading_failed(e) \nCalled if get_json() parsing fails and isn’t silenced. If\nthis method returns a value, it is used as the return value for\nget_json(). The default implementation raises a\nBadRequest exception.\n\nChangelog\nChanged in version 0.10: Raise a BadRequest error instead of returning an error\nmessage as JSON. If you want that behavior you can add it by\nsubclassing.\n\n\nNew in version 0.8.\n\n"
    ),
    _(
        "Request.on_json_loading_failed(e) \nCalled if get_json() parsing fails and isn’t silenced. If\nthis method returns a value, it is used as the return value for\nget_json(). The default implementation raises a\nBadRequest exception.\n\nChangelog\nChanged in version 0.10: Raise a BadRequest error instead of returning an error\nmessage as JSON. If you want that behavior you can add it by\nsubclassing.\n\n\nNew in version 0.8.\n\n"
    ),
    _(
        "Request.parameter_storage_class() \nalias of werkzeug.datastructures.ImmutableMultiDict\n"
    ),
    _(
        "Request.parameter_storage_class() \nalias of werkzeug.datastructures.ImmutableMultiDict\n"
    ),
    _("Request.path() \n"),
    _(
        "Request.path() \nRequested path as unicode.  This works a bit like the regular path\ninfo in the WSGI environment but will always include a leading slash,\neven if the URL root is accessed.\n"
    ),
    _("Request.path() \n"),
    _(
        "Request.path() \nRequested path as unicode.  This works a bit like the regular path\ninfo in the WSGI environment but will always include a leading slash,\neven if the URL root is accessed.\n"
    ),
    _(
        "Request.pragma() \nThe Pragma general-header field is used to include\nimplementation-specific directives that might apply to any recipient\nalong the request/response chain.  All pragma directives specify\noptional behavior from the viewpoint of the protocol; however, some\nsystems MAY require that behavior be consistent with the directives.\n"
    ),
    _(
        "Request.pragma() \nThe Pragma general-header field is used to include\nimplementation-specific directives that might apply to any recipient\nalong the request/response chain.  All pragma directives specify\noptional behavior from the viewpoint of the protocol; however, some\nsystems MAY require that behavior be consistent with the directives.\n"
    ),
    _("Request.query_string() \nThe URL parameters as raw bytestring.\n"),
    _("Request.query_string() \nThe URL parameters as raw bytestring.\n"),
    _(
        "Request.range() \nThe parsed Range header.\n\nChangelog\nNew in version 0.7.\n\n\n\n\n\nReturn type:Range\n\n\n\n"
    ),
    _(
        "Request.range() \nThe parsed Range header.\n\nChangelog\nNew in version 0.7.\n\n\n\n\n\nReturn type:Range\n\n\n\n"
    ),
    _(
        "Request.referrer() \nThe Referer[sic] request-header field allows the client to specify,\nfor the server’s benefit, the address (URI) of the resource from which\nthe Request-URI was obtained (the “referrer”, although the header\nfield is misspelled).\n"
    ),
    _(
        "Request.referrer() \nThe Referer[sic] request-header field allows the client to specify,\nfor the server’s benefit, the address (URI) of the resource from which\nthe Request-URI was obtained (the “referrer”, although the header\nfield is misspelled).\n"
    ),
    _("Request.remote_addr() \nThe remote address of the client.\n"),
    _("Request.remote_addr() \nThe remote address of the client.\n"),
    _(
        "Request.remote_user() \nIf the server supports user authentication, and the script is\nprotected, this attribute contains the username the user has\nauthenticated as.\n"
    ),
    _(
        "Request.remote_user() \nIf the server supports user authentication, and the script is\nprotected, this attribute contains the username the user has\nauthenticated as.\n"
    ),
    _(
        "Request.routing_exception() \nIf matching the URL failed, this is the exception that will be\nraised / was raised as part of the request handling.  This is\nusually a NotFound exception or\nsomething similar.\n"
    ),
    _(
        "Request.routing_exception() \nIf matching the URL failed, this is the exception that will be\nraised / was raised as part of the request handling.  This is\nusually a NotFound exception or\nsomething similar.\n"
    ),
    _(
        "Request.scheme() \nURL scheme (http or https).\n\nChangelog\nNew in version 0.7.\n\n"
    ),
    _(
        "Request.scheme() \nURL scheme (http or https).\n\nChangelog\nNew in version 0.7.\n\n"
    ),
    _("Request.script_root() \n"),
    _(
        "Request.script_root() \nThe root path of the script without the trailing slash.\n"
    ),
    _("Request.script_root() \n"),
    _(
        "Request.script_root() \nThe root path of the script without the trailing slash.\n"
    ),
    _(
        "Request.stream() \nIf the incoming form data was not encoded with a known mimetype\nthe data is stored unmodified in this stream for consumption.  Most\nof the time it is a better idea to use data which will give\nyou that data as a string.  The stream only returns the data once.\nUnlike input_stream this stream is properly guarded that you\ncan’t accidentally read past the length of the input.  Werkzeug will\ninternally always refer to this stream to read data which makes it\npossible to wrap this object with a stream that does filtering.\n\nChangelog\nChanged in version 0.9: This stream is now always available but might be consumed by the\nform parser later on.  Previously the stream was only set if no\nparsing happened.\n\n"
    ),
    _(
        "Request.stream() \nIf the incoming form data was not encoded with a known mimetype\nthe data is stored unmodified in this stream for consumption.  Most\nof the time it is a better idea to use data which will give\nyou that data as a string.  The stream only returns the data once.\nUnlike input_stream this stream is properly guarded that you\ncan’t accidentally read past the length of the input.  Werkzeug will\ninternally always refer to this stream to read data which makes it\npossible to wrap this object with a stream that does filtering.\n\nChangelog\nChanged in version 0.9: This stream is now always available but might be consumed by the\nform parser later on.  Previously the stream was only set if no\nparsing happened.\n\n"
    ),
    _("Request.url() \n"),
    _(
        "Request.url() \nThe reconstructed current URL as IRI.\nSee also: trusted_hosts.\n"
    ),
    _("Request.url() \n"),
    _(
        "Request.url() \nThe reconstructed current URL as IRI.\nSee also: trusted_hosts.\n"
    ),
    _(
        "Request.url_charset() \nThe charset that is assumed for URLs.  Defaults to the value\nof charset.\n\nChangelog\nNew in version 0.6.\n\n"
    ),
    _(
        "Request.url_charset() \nThe charset that is assumed for URLs.  Defaults to the value\nof charset.\n\nChangelog\nNew in version 0.6.\n\n"
    ),
    _(
        "Request.url_root() \nProvides different ways to look at the current IRI.  Imagine your application is\nlistening on the following application root:\nhttp://www.example.com/myapplication\n\n\nAnd a user requests the following URI:\nhttp://www.example.com/myapplication/%CF%80/page.html?x=y\n\n\nIn this case the values of the above mentioned attributes would be\nthe following:\n\n\n\n\n\n\npath\nu'/π/page.html'\n\nfull_path\nu'/π/page.html?x=y'\n\nscript_root\nu'/myapplication'\n\nbase_url\nu'http://www.example.com/myapplication/π/page.html'\n\nurl\nu'http://www.example.com/myapplication/π/page.html?x=y'\n\nurl_root\nu'http://www.example.com/myapplication/'\n\n\n\n"
    ),
    _(
        "Request.url_root() \nThe full URL root (with hostname), this is the application\nroot as IRI.\nSee also: trusted_hosts.\n"
    ),
    _(
        "Request.url_root() \nProvides different ways to look at the current IRI.  Imagine your application is\nlistening on the following application root:\nhttp://www.example.com/myapplication\n\n\nAnd a user requests the following URI:\nhttp://www.example.com/myapplication/%CF%80/page.html?x=y\n\n\nIn this case the values of the above mentioned attributes would be\nthe following:\n\n\n\n\n\n\npath\nu'/π/page.html'\n\nfull_path\nu'/π/page.html?x=y'\n\nscript_root\nu'/myapplication'\n\nbase_url\nu'http://www.example.com/myapplication/π/page.html'\n\nurl\nu'http://www.example.com/myapplication/π/page.html?x=y'\n\nurl_root\nu'http://www.example.com/myapplication/'\n\n\n\n"
    ),
    _(
        "Request.url_root() \nThe full URL root (with hostname), this is the application\nroot as IRI.\nSee also: trusted_hosts.\n"
    ),
    _(
        "Request.url_rule() \nThe internal URL rule that matched the request.  This can be\nuseful to inspect which methods are allowed for the URL from\na before/after handler (request.url_rule.methods) etc.\nThough if the request’s method was invalid for the URL rule,\nthe valid list is available in routing_exception.valid_methods\ninstead (an attribute of the Werkzeug exception MethodNotAllowed)\nbecause the request was never internally bound.\n\nChangelog\nNew in version 0.6.\n\n"
    ),
    _(
        "Request.url_rule() \nThe internal URL rule that matched the request.  This can be\nuseful to inspect which methods are allowed for the URL from\na before/after handler (request.url_rule.methods) etc.\nThough if the request’s method was invalid for the URL rule,\nthe valid list is available in routing_exception.valid_methods\ninstead (an attribute of the Werkzeug exception MethodNotAllowed)\nbecause the request was never internally bound.\n\nChangelog\nNew in version 0.6.\n\n"
    ),
    _("Request.user_agent() \nThe current user agent.\n"),
    _("Request.user_agent() \nThe current user agent.\n"),
    _(
        "Request.values() \nA werkzeug.datastructures.CombinedMultiDict that combines\nargs and form.\n"
    ),
    _(
        "Request.values() \nA werkzeug.datastructures.CombinedMultiDict that combines\nargs and form.\n"
    ),
    _(
        "Request.view_args() \nA dict of view arguments that matched the request.  If an exception\nhappened when matching, this will be None.\n"
    ),
    _(
        "Request.view_args() \nA dict of view arguments that matched the request.  If an exception\nhappened when matching, this will be None.\n"
    ),
    _(
        "Request.want_form_data_parsed() \nReturns True if the request method carries content.  As of\nWerkzeug 0.9 this will be the case if a content type is transmitted.\n\nChangelog\nNew in version 0.8.\n\n"
    ),
    _(
        "Request.want_form_data_parsed() \nReturns True if the request method carries content.  As of\nWerkzeug 0.9 this will be the case if a content type is transmitted.\n\nChangelog\nNew in version 0.8.\n\n"
    ),
    _(
        "RequestContext(app, environ, request=None) \nThe request context contains all request relevant information.  It is\ncreated at the beginning of the request and pushed to the\n_request_ctx_stack and removed at the end of it.  It will create the\nURL adapter and request object for the WSGI environment provided.\n\nDo not attempt to use this class directly, instead use\ntest_request_context() and\nrequest_context() to create this object.\n\nWhen the request context is popped, it will evaluate all the\nfunctions registered on the application for teardown execution\n(teardown_request()).\n\nThe request context is automatically popped at the end of the request\nfor you.  In debug mode the request context is kept around if\nexceptions happen so that interactive debuggers have a chance to\nintrospect the data.  With 0.4 this can also be forced for requests\nthat did not fail and outside of DEBUG mode.  By setting\n'flask._preserve_context' to True on the WSGI environment the\ncontext will not pop itself at the end of the request.  This is used by\nthe test_client() for example to implement the\ndeferred cleanup functionality.\n\nYou might find this helpful for unittests where you need the\ninformation from the context local around for a little longer.  Make\nsure to properly pop() the stack yourself in\nthat situation, otherwise your unittests will leak memory.\n\n"
    ),
    _(
        "RequestContext(app, environ, request=None) \nThe request context contains all request relevant information.  It is\ncreated at the beginning of the request and pushed to the\n_request_ctx_stack and removed at the end of it.  It will create the\nURL adapter and request object for the WSGI environment provided.\n\nDo not attempt to use this class directly, instead use\ntest_request_context() and\nrequest_context() to create this object.\n\nWhen the request context is popped, it will evaluate all the\nfunctions registered on the application for teardown execution\n(teardown_request()).\n\nThe request context is automatically popped at the end of the request\nfor you.  In debug mode the request context is kept around if\nexceptions happen so that interactive debuggers have a chance to\nintrospect the data.  With 0.4 this can also be forced for requests\nthat did not fail and outside of DEBUG mode.  By setting\n'flask._preserve_context' to True on the WSGI environment the\ncontext will not pop itself at the end of the request.  This is used by\nthe test_client() for example to implement the\ndeferred cleanup functionality.\n\nYou might find this helpful for unittests where you need the\ninformation from the context local around for a little longer.  Make\nsure to properly pop() the stack yourself in\nthat situation, otherwise your unittests will leak memory.\n\n"
    ),
    _(
        "RequestContext.copy() \nCreates a copy of this request context with the same request object.\nThis can be used to move a request context to a different greenlet.\nBecause the actual request object is the same this cannot be used to\nmove a request context to a different thread unless access to the\nrequest object is locked.\n\nChangelog\nNew in version 0.10.\n\n"
    ),
    _(
        "RequestContext.copy() \nCreates a copy of this request context with the same request object.\nThis can be used to move a request context to a different greenlet.\nBecause the actual request object is the same this cannot be used to\nmove a request context to a different thread unless access to the\nrequest object is locked.\n\nChangelog\nNew in version 0.10.\n\n"
    ),
    _(
        "RequestContext.match_request() \nCan be overridden by a subclass to hook into the matching\nof the request.\n"
    ),
    _(
        "RequestContext.match_request() \nCan be overridden by a subclass to hook into the matching\nof the request.\n"
    ),
    _(
        "RequestContext.pop(exc=&lt;object object&gt;) \nPops the request context and unbinds it by doing that.  This will\nalso trigger the execution of functions registered by the\nteardown_request() decorator.\n\nChangelog\nChanged in version 0.9: Added the exc argument.\n\n"
    ),
    _(
        "RequestContext.pop(exc=&lt;object object&gt;) \nPops the request context and unbinds it by doing that.  This will\nalso trigger the execution of functions registered by the\nteardown_request() decorator.\n\nChangelog\nChanged in version 0.9: Added the exc argument.\n\n"
    ),
    _(
        "RequestContext.push() \nBinds the request context to the current context.\n"
    ),
    _(
        "RequestContext.push() \nBinds the request context to the current context.\n"
    ),
    _(
        "Response(response=None, status=None, headers=None, mimetype=None, content_type=None, direct_passthrough=False) \nThe response object that is used by default in Flask.  Works like the\nresponse object from Werkzeug but is set to have an HTML mimetype by\ndefault.  Quite often you don’t have to create this object yourself because\nmake_response() will take care of that for you.\n\nIf you want to replace the response object used you can subclass this and\nset response_class to your subclass.\n\n"
    ),
    _(
        "Response(response=None, status=None, headers=None, mimetype=None, content_type=None, direct_passthrough=False) \nThe response object that is used by default in Flask.  Works like the\nresponse object from Werkzeug but is set to have an HTML mimetype by\ndefault.  Quite often you don’t have to create this object yourself because\nmake_response() will take care of that for you.\n\nIf you want to replace the response object used you can subclass this and\nset response_class to your subclass.\n\n"
    ),
    _(
        "Response.data() \nA descriptor that calls get_data() and set_data().  This\nshould not be used and will eventually get deprecated.\n"
    ),
    _(
        "Response.data() \nA descriptor that calls get_data() and set_data().  This\nshould not be used and will eventually get deprecated.\n"
    ),
    _(
        'Response.get_json(force=False, silent=False, cache=True, <em class="mimetype">application/json) \nParse and return the data as JSON. If the mimetype does not\nindicate JSON (application/json, see\nis_json()), this returns None unless force is\ntrue. If parsing fails, on_json_loading_failed() is called\nand its return value is used as the return value.\n\n\n\n\nParameters:\nforce -- Ignore the mimetype and always try to parse JSON.\nsilent -- Silence parsing errors and return None\ninstead.\ncache -- Store the parsed JSON to return for subsequent\ncalls.\n\n\n\n\n\n'
    ),
    _(
        'Response.get_json(force=False, silent=False, cache=True, <em class="mimetype">application/json) \nParse and return the data as JSON. If the mimetype does not\nindicate JSON (application/json, see\nis_json()), this returns None unless force is\ntrue. If parsing fails, on_json_loading_failed() is called\nand its return value is used as the return value.\n\n\n\n\nParameters:\nforce -- Ignore the mimetype and always try to parse JSON.\nsilent -- Silence parsing errors and return None\ninstead.\ncache -- Store the parsed JSON to return for subsequent\ncalls.\n\n\n\n\n\n'
    ),
    _(
        "Response.headers() \nA Headers object representing the response headers.\n"
    ),
    _(
        "Response.headers() \nA Headers object representing the response headers.\n"
    ),
    _(
        "Response.is_json() \nCheck if the mimetype indicates JSON data, either\napplication/json or application/*+json.\n\nChangelog\nNew in version 0.11.\n\n"
    ),
    _(
        "Response.is_json() \nCheck if the mimetype indicates JSON data, either\napplication/json or application/*+json.\n\nChangelog\nNew in version 0.11.\n\n"
    ),
    _(
        "Response.max_cookie_size() \nRead-only view of the MAX_COOKIE_SIZE config key.\nSee max_cookie_size in\nWerkzeug’s docs.\n"
    ),
    _(
        "Response.max_cookie_size() \nRead-only view of the MAX_COOKIE_SIZE config key.\nSee max_cookie_size in\nWerkzeug’s docs.\n"
    ),
    _(
        "Response.mimetype() \nThe mimetype (content type without charset etc.)\n"
    ),
    _(
        "Response.mimetype() \nThe mimetype (content type without charset etc.)\n"
    ),
    _(
        "Response.set_cookie(key, value='', max_age=None, expires=None, path='/', domain=None, secure=False, httponly=False, samesite=None) \nSets a cookie. The parameters are the same as in the cookie Morsel\nobject in the Python standard library but it accepts unicode data, too.\nA warning is raised if the size of the cookie header exceeds\nmax_cookie_size, but the header will still be set.\n\n\n\n\nParameters:\nkey -- the key (name) of the cookie to be set.\nvalue -- the value of the cookie.\nmax_age -- should be a number of seconds, or None (default) if\nthe cookie should last only as long as the client’s\nbrowser session.\nexpires -- should be a datetime object or UNIX timestamp.\npath -- limits the cookie to a given path, per default it will\nspan the whole domain.\ndomain -- if you want to set a cross-domain cookie.  For example,\ndomain=\".example.com\" will set a cookie that is\nreadable by the domain www.example.com,\nfoo.example.com etc.  Otherwise, a cookie will only\nbe readable by the domain that set it.\nsecure -- If True, the cookie will only be available via HTTPS\nhttponly -- disallow JavaScript to access the cookie.  This is an\nextension to the cookie standard and probably not\nsupported by all browsers.\nsamesite -- Limits the scope of the cookie such that it will only\nbe attached to requests if those requests are\n“same-site”.\n\n\n\n\n\n"
    ),
    _(
        "Response.set_cookie(key, value='', max_age=None, expires=None, path='/', domain=None, secure=False, httponly=False, samesite=None) \nSets a cookie. The parameters are the same as in the cookie Morsel\nobject in the Python standard library but it accepts unicode data, too.\nA warning is raised if the size of the cookie header exceeds\nmax_cookie_size, but the header will still be set.\n\n\n\n\nParameters:\nkey -- the key (name) of the cookie to be set.\nvalue -- the value of the cookie.\nmax_age -- should be a number of seconds, or None (default) if\nthe cookie should last only as long as the client’s\nbrowser session.\nexpires -- should be a datetime object or UNIX timestamp.\npath -- limits the cookie to a given path, per default it will\nspan the whole domain.\ndomain -- if you want to set a cross-domain cookie.  For example,\ndomain=\".example.com\" will set a cookie that is\nreadable by the domain www.example.com,\nfoo.example.com etc.  Otherwise, a cookie will only\nbe readable by the domain that set it.\nsecure -- If True, the cookie will only be available via HTTPS\nhttponly -- disallow JavaScript to access the cookie.  This is an\nextension to the cookie standard and probably not\nsupported by all browsers.\nsamesite -- Limits the scope of the cookie such that it will only\nbe attached to requests if those requests are\n“same-site”.\n\n\n\n\n\n"
    ),
    _("Response.status() \nA string with a response status.\n"),
    _("Response.status() \nA string with a response status.\n"),
    _("Response.status_code() \nThe response status as integer.\n"),
    _("Response.status_code() \nThe response status as integer.\n"),
    _(
        "ScriptInfo(app_import_path=None, create_app=None) \nHelp object to deal with Flask applications.  This is usually not\nnecessary to interface with as it’s used internally in the dispatching\nto click.  In future versions of Flask this object will most likely play\na bigger role.  Typically it’s created automatically by the\nFlaskGroup but you can also manually create it and pass it\nonwards as click object.\n\n"
    ),
    _(
        "ScriptInfo(app_import_path=None, create_app=None) \nHelp object to deal with Flask applications.  This is usually not\nnecessary to interface with as it’s used internally in the dispatching\nto click.  In future versions of Flask this object will most likely play\na bigger role.  Typically it’s created automatically by the\nFlaskGroup but you can also manually create it and pass it\nonwards as click object.\n\n"
    ),
    _(
        "ScriptInfo.app_import_path() \nOptionally the import path for the Flask application.\n"
    ),
    _(
        "ScriptInfo.app_import_path() \nOptionally the import path for the Flask application.\n"
    ),
    _(
        "ScriptInfo.create_app() \nOptionally a function that is passed the script info to create\nthe instance of the application.\n"
    ),
    _(
        "ScriptInfo.create_app() \nOptionally a function that is passed the script info to create\nthe instance of the application.\n"
    ),
    _(
        "ScriptInfo.data() \nA dictionary with arbitrary data that can be associated with\nthis script info.\n"
    ),
    _(
        "ScriptInfo.data() \nA dictionary with arbitrary data that can be associated with\nthis script info.\n"
    ),
    _(
        "ScriptInfo.load_app() \nLoads the Flask app (if not yet loaded) and returns it.  Calling\nthis multiple times will just result in the already loaded app to\nbe returned.\n"
    ),
    _(
        "ScriptInfo.load_app() \nLoads the Flask app (if not yet loaded) and returns it.  Calling\nthis multiple times will just result in the already loaded app to\nbe returned.\n"
    ),
    _(
        "SecureCookieSession(initial=None) \nBase class for sessions based on signed cookies.\n\nThis session backend will set the modified and\naccessed attributes. It cannot reliably track whether a\nsession is new (vs. empty), so new remains hard coded to\nFalse.\n\n"
    ),
    _(
        "SecureCookieSession(initial=None) \nBase class for sessions based on signed cookies.\n\nThis session backend will set the modified and\naccessed attributes. It cannot reliably track whether a\nsession is new (vs. empty), so new remains hard coded to\nFalse.\n\n"
    ),
    _(
        "SecureCookieSession.accessed() \nheader, which allows caching proxies to cache different pages for\ndifferent users.\n"
    ),
    _(
        "SecureCookieSession.accessed() \nheader, which allows caching proxies to cache different pages for\ndifferent users.\n"
    ),
    _("SecureCookieSession.get(k, d) \n"),
    _("SecureCookieSession.get(k, d) \n"),
    _(
        "SecureCookieSession.modified() \nWhen data is changed, this is set to True. Only the session\ndictionary itself is tracked; if the session contains mutable\ndata (for example a nested dict) then this must be set to\nTrue manually when modifying that data. The session cookie\nwill only be written to the response if this is True.\n"
    ),
    _(
        "SecureCookieSession.modified() \nWhen data is changed, this is set to True. Only the session\ndictionary itself is tracked; if the session contains mutable\ndata (for example a nested dict) then this must be set to\nTrue manually when modifying that data. The session cookie\nwill only be written to the response if this is True.\n"
    ),
    _("SecureCookieSession.setdefault(k, d) \n"),
    _("SecureCookieSession.setdefault(k, d) \n"),
    _(
        "SecureCookieSessionInterface() \nThe default session interface that stores sessions in signed cookies\nthrough the itsdangerous module.\n\n"
    ),
    _(
        "SecureCookieSessionInterface() \nThe default session interface that stores sessions in signed cookies\nthrough the itsdangerous module.\n\n"
    ),
    _(
        "SecureCookieSessionInterface.key_derivation() \nthe name of the itsdangerous supported key derivation.  The default\nis hmac.\n"
    ),
    _(
        "SecureCookieSessionInterface.key_derivation() \nthe name of the itsdangerous supported key derivation.  The default\nis hmac.\n"
    ),
    _(
        "SecureCookieSessionInterface.open_session(app, request) \nThis method has to be implemented and must either return None\nin case the loading failed because of a configuration error or an\ninstance of a session object which implements a dictionary like\ninterface + the methods and attributes on SessionMixin.\n"
    ),
    _(
        "SecureCookieSessionInterface.open_session(app, request) \nThis method has to be implemented and must either return None\nin case the loading failed because of a configuration error or an\ninstance of a session object which implements a dictionary like\ninterface + the methods and attributes on SessionMixin.\n"
    ),
    _(
        "SecureCookieSessionInterface.salt() \nthe salt that should be applied on top of the secret key for the\nsigning of cookie based sessions.\n"
    ),
    _(
        "SecureCookieSessionInterface.salt() \nthe salt that should be applied on top of the secret key for the\nsigning of cookie based sessions.\n"
    ),
    _(
        "SecureCookieSessionInterface.save_session(app, session, response) \nThis is called for actual sessions returned by open_session()\nat the end of the request.  This is still called during a request\ncontext so if you absolutely need access to the request you can do\nthat.\n"
    ),
    _(
        "SecureCookieSessionInterface.save_session(app, session, response) \nThis is called for actual sessions returned by open_session()\nat the end of the request.  This is still called during a request\ncontext so if you absolutely need access to the request you can do\nthat.\n"
    ),
    _(
        "SecureCookieSessionInterface.serializer() \nA python serializer for the payload.  The default is a compact\nJSON derived serializer with support for some extra Python types\nsuch as datetime objects or tuples.\n"
    ),
    _(
        "SecureCookieSessionInterface.serializer() \nA python serializer for the payload.  The default is a compact\nJSON derived serializer with support for some extra Python types\nsuch as datetime objects or tuples.\n"
    ),
    _(
        "SecureCookieSessionInterface.session_class() \nalias of SecureCookieSession\n"
    ),
    _(
        "SecureCookieSessionInterface.session_class() \nalias of SecureCookieSession\n"
    ),
    _(
        "SessionInterface() \nThe basic interface you have to implement in order to replace the\ndefault session interface which uses werkzeug’s securecookie\nimplementation.  The only methods you have to implement are\nopen_session() and save_session(), the others have\nuseful defaults which you don’t need to change.\n\nThe session object returned by the open_session() method has to\nprovide a dictionary like interface plus the properties and methods\nfrom the SessionMixin.  We recommend just subclassing a dict\nand adding that mixin:\n\nIf open_session() returns None Flask will call into\nmake_null_session() to create a session that acts as replacement\nif the session support cannot work because some requirement is not\nfulfilled.  The default NullSession class that is created\nwill complain that the secret key was not set.\n\nTo replace the session interface on an application all you have to do\nis to assign flask.Flask.session_interface:\n\n"
    ),
    _(
        "SessionInterface() \nThe basic interface you have to implement in order to replace the\ndefault session interface which uses werkzeug’s securecookie\nimplementation.  The only methods you have to implement are\nopen_session() and save_session(), the others have\nuseful defaults which you don’t need to change.\n\nThe session object returned by the open_session() method has to\nprovide a dictionary like interface plus the properties and methods\nfrom the SessionMixin.  We recommend just subclassing a dict\nand adding that mixin:\n\nIf open_session() returns None Flask will call into\nmake_null_session() to create a session that acts as replacement\nif the session support cannot work because some requirement is not\nfulfilled.  The default NullSession class that is created\nwill complain that the secret key was not set.\n\nTo replace the session interface on an application all you have to do\nis to assign flask.Flask.session_interface:\n\n"
    ),
    _(
        "SessionInterface.get_cookie_domain(app) \nReturns the domain that should be set for the session cookie.\nUses SESSION_COOKIE_DOMAIN if it is configured, otherwise\nfalls back to detecting the domain based on SERVER_NAME.\nOnce detected (or if not set at all), SESSION_COOKIE_DOMAIN is\nupdated to avoid re-running the logic.\n"
    ),
    _(
        "SessionInterface.get_cookie_domain(app) \nReturns the domain that should be set for the session cookie.\nUses SESSION_COOKIE_DOMAIN if it is configured, otherwise\nfalls back to detecting the domain based on SERVER_NAME.\nOnce detected (or if not set at all), SESSION_COOKIE_DOMAIN is\nupdated to avoid re-running the logic.\n"
    ),
    _(
        "SessionInterface.get_cookie_httponly(app) \nReturns True if the session cookie should be httponly.  This\ncurrently just returns the value of the SESSION_COOKIE_HTTPONLY\nconfig var.\n"
    ),
    _(
        "SessionInterface.get_cookie_httponly(app) \nReturns True if the session cookie should be httponly.  This\ncurrently just returns the value of the SESSION_COOKIE_HTTPONLY\nconfig var.\n"
    ),
    _(
        "SessionInterface.get_cookie_path(app) \nReturns the path for which the cookie should be valid.  The\ndefault implementation uses the value from the SESSION_COOKIE_PATH\nconfig var if it’s set, and falls back to APPLICATION_ROOT or\nuses / if it’s None.\n"
    ),
    _(
        "SessionInterface.get_cookie_path(app) \nReturns the path for which the cookie should be valid.  The\ndefault implementation uses the value from the SESSION_COOKIE_PATH\nconfig var if it’s set, and falls back to APPLICATION_ROOT or\nuses / if it’s None.\n"
    ),
    _(
        "SessionInterface.get_cookie_samesite(app) \nReturn 'Strict' or 'Lax' if the cookie should use the\nSameSite attribute. This currently just returns the value of\nthe SESSION_COOKIE_SAMESITE setting.\n"
    ),
    _(
        "SessionInterface.get_cookie_samesite(app) \nReturn 'Strict' or 'Lax' if the cookie should use the\nSameSite attribute. This currently just returns the value of\nthe SESSION_COOKIE_SAMESITE setting.\n"
    ),
    _(
        "SessionInterface.get_cookie_secure(app) \nReturns True if the cookie should be secure.  This currently\njust returns the value of the SESSION_COOKIE_SECURE setting.\n"
    ),
    _(
        "SessionInterface.get_cookie_secure(app) \nReturns True if the cookie should be secure.  This currently\njust returns the value of the SESSION_COOKIE_SECURE setting.\n"
    ),
    _(
        "SessionInterface.get_expiration_time(app, session) \nA helper method that returns an expiration date for the session\nor None if the session is linked to the browser session.  The\ndefault implementation returns now + the permanent session\nlifetime configured on the application.\n"
    ),
    _(
        "SessionInterface.get_expiration_time(app, session) \nA helper method that returns an expiration date for the session\nor None if the session is linked to the browser session.  The\ndefault implementation returns now + the permanent session\nlifetime configured on the application.\n"
    ),
    _(
        "SessionInterface.is_null_session(obj) \nChecks if a given object is a null session.  Null sessions are\nnot asked to be saved.\nThis checks if the object is an instance of null_session_class\nby default.\n"
    ),
    _(
        "SessionInterface.is_null_session(obj) \nChecks if a given object is a null session.  Null sessions are\nnot asked to be saved.\nThis checks if the object is an instance of null_session_class\nby default.\n"
    ),
    _(
        "SessionInterface.make_null_session(app) \nCreates a null session which acts as a replacement object if the\nreal session support could not be loaded due to a configuration\nerror.  This mainly aids the user experience because the job of the\nnull session is to still support lookup without complaining but\nmodifications are answered with a helpful error message of what\nfailed.\nThis creates an instance of null_session_class by default.\n"
    ),
    _(
        "SessionInterface.make_null_session(app) \nCreates a null session which acts as a replacement object if the\nreal session support could not be loaded due to a configuration\nerror.  This mainly aids the user experience because the job of the\nnull session is to still support lookup without complaining but\nmodifications are answered with a helpful error message of what\nfailed.\nThis creates an instance of null_session_class by default.\n"
    ),
    _(
        "SessionInterface.null_session_class() \nmake_null_session() will look here for the class that should\nbe created when a null session is requested.  Likewise the\nis_null_session() method will perform a typecheck against\nthis type.\nalias of NullSession\n"
    ),
    _(
        "SessionInterface.null_session_class() \nmake_null_session() will look here for the class that should\nbe created when a null session is requested.  Likewise the\nis_null_session() method will perform a typecheck against\nthis type.\nalias of NullSession\n"
    ),
    _(
        "SessionInterface.open_session(app, request) \nThis method has to be implemented and must either return None\nin case the loading failed because of a configuration error or an\ninstance of a session object which implements a dictionary like\ninterface + the methods and attributes on SessionMixin.\n"
    ),
    _(
        "SessionInterface.open_session(app, request) \nThis method has to be implemented and must either return None\nin case the loading failed because of a configuration error or an\ninstance of a session object which implements a dictionary like\ninterface + the methods and attributes on SessionMixin.\n"
    ),
    _(
        "SessionInterface.pickle_based() \nA flag that indicates if the session interface is pickle based.\nThis can be used by Flask extensions to make a decision in regards\nto how to deal with the session object.\n\nChangelog\nNew in version 0.10.\n\n"
    ),
    _(
        "SessionInterface.pickle_based() \nA flag that indicates if the session interface is pickle based.\nThis can be used by Flask extensions to make a decision in regards\nto how to deal with the session object.\n\nChangelog\nNew in version 0.10.\n\n"
    ),
    _(
        "SessionInterface.save_session(app, session, response) \nThis is called for actual sessions returned by open_session()\nat the end of the request.  This is still called during a request\ncontext so if you absolutely need access to the request you can do\nthat.\n"
    ),
    _(
        "SessionInterface.save_session(app, session, response) \nThis is called for actual sessions returned by open_session()\nat the end of the request.  This is still called during a request\ncontext so if you absolutely need access to the request you can do\nthat.\n"
    ),
    _(
        "SessionInterface.should_set_cookie(app, session) \nUsed by session backends to determine if a Set-Cookie header\nshould be set for this session cookie for this response. If the session\nhas been modified, the cookie is set. If the session is permanent and\nthe SESSION_REFRESH_EACH_REQUEST config is true, the cookie is\nalways set.\nThis check is usually skipped if the session was deleted.\n\nChangelog\nNew in version 0.11.\n\n"
    ),
    _(
        "SessionInterface.should_set_cookie(app, session) \nUsed by session backends to determine if a Set-Cookie header\nshould be set for this session cookie for this response. If the session\nhas been modified, the cookie is set. If the session is permanent and\nthe SESSION_REFRESH_EACH_REQUEST config is true, the cookie is\nalways set.\nThis check is usually skipped if the session was deleted.\n\nChangelog\nNew in version 0.11.\n\n"
    ),
    _(
        "SessionMixin() \nExpands a basic dictionary with session attributes.\n\n"
    ),
    _(
        "SessionMixin() \nExpands a basic dictionary with session attributes.\n\n"
    ),
    _(
        "SessionMixin.accessed() \nSome implementations can detect when session data is read or\nwritten and set this when that happens. The mixin default is hard\ncoded to True.\n"
    ),
    _(
        "SessionMixin.accessed() \nSome implementations can detect when session data is read or\nwritten and set this when that happens. The mixin default is hard\ncoded to True.\n"
    ),
    _(
        "SessionMixin.modified() \nSome implementations can detect changes to the session and set\nthis when that happens. The mixin default is hard coded to\nTrue.\n"
    ),
    _(
        "SessionMixin.modified() \nSome implementations can detect changes to the session and set\nthis when that happens. The mixin default is hard coded to\nTrue.\n"
    ),
    _(
        "SessionMixin.permanent() \nThis reflects the '_permanent' key in the dict.\n"
    ),
    _(
        "SessionMixin.permanent() \nThis reflects the '_permanent' key in the dict.\n"
    ),
    _(
        "TaggedJSONSerializer() \nSerializer that uses a tag system to compactly represent objects that\nare not JSON types. Passed as the intermediate serializer to\nitsdangerous.Serializer.\n\nThe following extra types are supported:\n\n"
    ),
    _(
        "TaggedJSONSerializer() \nSerializer that uses a tag system to compactly represent objects that\nare not JSON types. Passed as the intermediate serializer to\nitsdangerous.Serializer.\n\nThe following extra types are supported:\n\n"
    ),
    _(
        "TaggedJSONSerializer.default_tags() \nTag classes to bind when creating the serializer. Other tags can be\nadded later using register().\n"
    ),
    _(
        "TaggedJSONSerializer.default_tags() \nTag classes to bind when creating the serializer. Other tags can be\nadded later using register().\n"
    ),
    _(
        "TaggedJSONSerializer.dumps(value) \nTag the value and dump it to a compact JSON string.\n"
    ),
    _(
        "TaggedJSONSerializer.dumps(value) \nTag the value and dump it to a compact JSON string.\n"
    ),
    _(
        "TaggedJSONSerializer.loads(value) \nLoad data from a JSON string and deserialized any tagged objects.\n"
    ),
    _(
        "TaggedJSONSerializer.loads(value) \nLoad data from a JSON string and deserialized any tagged objects.\n"
    ),
    _(
        "TaggedJSONSerializer.register(tag_class, force=False, index=None) \nRegister a new tag with this serializer.\n\n\n\n\nParameters:\ntag_class -- tag class to register. Will be instantiated with this\nserializer instance.\nforce -- overwrite an existing tag. If false (default), a\nKeyError is raised.\nindex -- index to insert the new tag in the tag order. Useful when\nthe new tag is a special case of an existing tag. If None\n(default), the tag is appended to the end of the order.\n\n\n\nRaises:KeyError -- if the tag key is already registered and force is\nnot true.\n\n\n\n\n"
    ),
    _(
        "TaggedJSONSerializer.register(tag_class, force=False, index=None) \nRegister a new tag with this serializer.\n\n\n\n\nParameters:\ntag_class -- tag class to register. Will be instantiated with this\nserializer instance.\nforce -- overwrite an existing tag. If false (default), a\nKeyError is raised.\nindex -- index to insert the new tag in the tag order. Useful when\nthe new tag is a special case of an existing tag. If None\n(default), the tag is appended to the end of the order.\n\n\n\nRaises:KeyError -- if the tag key is already registered and force is\nnot true.\n\n\n\n\n"
    ),
    _(
        "TaggedJSONSerializer.tag(value) \nConvert a value to a tagged representation if necessary.\n"
    ),
    _(
        "TaggedJSONSerializer.tag(value) \nConvert a value to a tagged representation if necessary.\n"
    ),
    _(
        "TaggedJSONSerializer.untag(value) \nConvert a tagged representation back to the original type.\n"
    ),
    _(
        "TaggedJSONSerializer.untag(value) \nConvert a tagged representation back to the original type.\n"
    ),
    _(
        "View() \nAlternative way to use view functions.  A subclass has to implement\ndispatch_request() which is called with the view arguments from\nthe URL routing system.  If methods is provided the methods\ndo not have to be passed to the add_url_rule()\nmethod explicitly:\n\nWhen you want to decorate a pluggable view you will have to either do that\nwhen the view function is created (by wrapping the return value of\nas_view()) or you can use the decorators attribute:\n\nThe decorators stored in the decorators list are applied one after another\nwhen the view function is created.  Note that you can not use the class\nbased decorators since those would decorate the view class and not the\ngenerated view function!\n\n"
    ),
    _(
        "View() \nAlternative way to use view functions.  A subclass has to implement\ndispatch_request() which is called with the view arguments from\nthe URL routing system.  If methods is provided the methods\ndo not have to be passed to the add_url_rule()\nmethod explicitly:\n\nWhen you want to decorate a pluggable view you will have to either do that\nwhen the view function is created (by wrapping the return value of\nas_view()) or you can use the decorators attribute:\n\nThe decorators stored in the decorators list are applied one after another\nwhen the view function is created.  Note that you can not use the class\nbased decorators since those would decorate the view class and not the\ngenerated view function!\n\n"
    ),
    _(
        "View.decorators() \nThe canonical way to decorate class-based views is to decorate the\nreturn value of as_view().  However since this moves parts of the\nlogic from the class declaration to the place where it’s hooked\ninto the routing system.\nYou can place one or more decorators in this list and whenever the\nview function is created the result is automatically decorated.\n\nChangelog\nNew in version 0.8.\n\n"
    ),
    _(
        "View.decorators() \nThe canonical way to decorate class-based views is to decorate the\nreturn value of as_view().  However since this moves parts of the\nlogic from the class declaration to the place where it’s hooked\ninto the routing system.\nYou can place one or more decorators in this list and whenever the\nview function is created the result is automatically decorated.\n\nChangelog\nNew in version 0.8.\n\n"
    ),
    _(
        "View.dispatch_request() \nSubclasses have to override this method to implement the\nactual view function code.  This method is called with all\nthe arguments from the URL rule.\n"
    ),
    _(
        "View.dispatch_request() \nSubclasses have to override this method to implement the\nactual view function code.  This method is called with all\nthe arguments from the URL rule.\n"
    ),
    _("View.methods() \nA list of methods this view can handle.\n"),
    _("View.methods() \nA list of methods this view can handle.\n"),
    _(
        "View.provide_automatic_options() \nSetting this disables or force-enables the automatic options handling.\n"
    ),
    _(
        "View.provide_automatic_options() \nSetting this disables or force-enables the automatic options handling.\n"
    ),
    _(
        "_AppCtxGlobals() \nA plain object. Used as a namespace for storing data during an\napplication context.\n\nCreating an app context automatically creates this object, which is\nmade available as the g proxy.\n\n"
    ),
    _(
        "_AppCtxGlobals() \nA plain object. Used as a namespace for storing data during an\napplication context.\n\nCreating an app context automatically creates this object, which is\nmade available as the g proxy.\n\n"
    ),
    _(
        "_AppCtxGlobals.get(name, default=None) \nGet an attribute by name, or a default value. Like\ndict.get().\n\n\n\n\nParameters:\nname -- Name of attribute to get.\ndefault -- Value to return if the attribute is not present.\n\n\n\n\n\n\nChangelog\nNew in version 0.10.\n\n"
    ),
    _(
        "_AppCtxGlobals.get(name, default=None) \nGet an attribute by name, or a default value. Like\ndict.get().\n\n\n\n\nParameters:\nname -- Name of attribute to get.\ndefault -- Value to return if the attribute is not present.\n\n\n\n\n\n\nChangelog\nNew in version 0.10.\n\n"
    ),
    _(
        "_AppCtxGlobals.pop(name, default=&lt;object object&gt;) \nGet and remove an attribute by name. Like dict.pop().\n\n\n\n\nParameters:\nname -- Name of attribute to pop.\ndefault -- Value to return if the attribute is not present,\ninstead of raise a KeyError.\n\n\n\n\n\n\nChangelog\nNew in version 0.11.\n\n"
    ),
    _(
        "_AppCtxGlobals.pop(name, default=&lt;object object&gt;) \nGet and remove an attribute by name. Like dict.pop().\n\n\n\n\nParameters:\nname -- Name of attribute to pop.\ndefault -- Value to return if the attribute is not present,\ninstead of raise a KeyError.\n\n\n\n\n\n\nChangelog\nNew in version 0.11.\n\n"
    ),
    _(
        "_AppCtxGlobals.setdefault(name, default=None) \nGet the value of an attribute if it is present, otherwise\nset and return a default value. Like dict.setdefault().\n\n\n\n\nParameters:name -- Name of attribute to get.\n\nParam:default: Value to set and return if the attribute is not\npresent.\n\n\n\n\nChangelog\nNew in version 0.11.\n\n"
    ),
    _(
        "_AppCtxGlobals.setdefault(name, default=None) \nGet the value of an attribute if it is present, otherwise\nset and return a default value. Like dict.setdefault().\n\n\n\n\nParameters:name -- Name of attribute to get.\n\nParam:default: Value to set and return if the attribute is not\npresent.\n\n\n\n\nChangelog\nNew in version 0.11.\n\n"
    ),
    _(
        "abort(status, *args, **kwargs) \nRaises an HTTPException for the given status code or WSGI\napplication:\nabort(404)  # 404 Not Found\nabort(Response('Hello World'))\n\n\nCan be passed a WSGI application or a status code.  If a status code is\ngiven it’s looked up in the list of exceptions and will raise that\nexception, if passed a WSGI application it will wrap it in a proxy WSGI\nexception and raise that:\nabort(404)\nabort(Response('Hello World'))\n\n\n"
    ),
    _(
        "abort(status, *args, **kwargs) \nRaises an HTTPException for the given status code or WSGI\napplication:\nabort(404)  # 404 Not Found\nabort(Response('Hello World'))\n\n\nCan be passed a WSGI application or a status code.  If a status code is\ngiven it’s looked up in the list of exceptions and will raise that\nexception, if passed a WSGI application it will wrap it in a proxy WSGI\nexception and raise that:\nabort(404)\nabort(Response('Hello World'))\n\n\n"
    ),
    _(
        "after_this_request(f) \nExecutes a function after this request.  This is useful to modify\nresponse objects.  The function is passed the response object and has\nto return the same or a new one.\nExample:\n@app.route('/')\ndef index():\n    @after_this_request\n    def add_header(response):\n        response.headers['X-Foo'] = 'Parachute'\n        return response\n    return 'Hello World!'\n\n\nThis is more useful if a function other than the view function wants to\nmodify a response.  For instance think of a decorator that wants to add\nsome headers without converting the return value into a response object.\n\nChangelog\nNew in version 0.9.\n\n"
    ),
    _(
        "after_this_request(f) \nExecutes a function after this request.  This is useful to modify\nresponse objects.  The function is passed the response object and has\nto return the same or a new one.\nExample:\n@app.route('/')\ndef index():\n    @after_this_request\n    def add_header(response):\n        response.headers['X-Foo'] = 'Parachute'\n        return response\n    return 'Hello World!'\n\n\nThis is more useful if a function other than the view function wants to\nmodify a response.  For instance think of a decorator that wants to add\nsome headers without converting the return value into a response object.\n\nChangelog\nNew in version 0.9.\n\n"
    ),
    _(
        "copy_current_request_context(f) \nA helper function that decorates a function to retain the current\nrequest context.  This is useful when working with greenlets.  The moment\nthe function is decorated a copy of the request context is created and\nthen pushed when the function is called.\nExample:\nimport gevent\nfrom flask import copy_current_request_context\n\n@app.route('/')\ndef index():\n    @copy_current_request_context\n    def do_some_work():\n        # do some work here, it can access flask.request like you\n        # would otherwise in the view function.\n        ...\n    gevent.spawn(do_some_work)\n    return 'Regular response'\n\n\n\nChangelog\nNew in version 0.10.\n\n"
    ),
    _(
        "copy_current_request_context(f) \nA helper function that decorates a function to retain the current\nrequest context.  This is useful when working with greenlets.  The moment\nthe function is decorated a copy of the request context is created and\nthen pushed when the function is called.\nExample:\nimport gevent\nfrom flask import copy_current_request_context\n\n@app.route('/')\ndef index():\n    @copy_current_request_context\n    def do_some_work():\n        # do some work here, it can access flask.request like you\n        # would otherwise in the view function.\n        ...\n    gevent.spawn(do_some_work)\n    return 'Regular response'\n\n\n\nChangelog\nNew in version 0.10.\n\n"
    ),
    _(
        "dump(obj, fp, **kwargs) \nLike dumps() but writes into a file object.\n"
    ),
    _(
        "dump(obj, fp, **kwargs) \nLike dumps() but writes into a file object.\n"
    ),
    _(
        "dumps(obj, **kwargs) \nSerialize obj to a JSON formatted str by using the application’s\nconfigured encoder (json_encoder) if there is an\napplication on the stack.\nThis function can return unicode strings or ascii-only bytestrings by\ndefault which coerce into unicode strings automatically.  That behavior by\ndefault is controlled by the JSON_AS_ASCII configuration variable\nand can be overridden by the simplejson ensure_ascii parameter.\n"
    ),
    _(
        "dumps(obj, **kwargs) \nSerialize obj to a JSON formatted str by using the application’s\nconfigured encoder (json_encoder) if there is an\napplication on the stack.\nThis function can return unicode strings or ascii-only bytestrings by\ndefault which coerce into unicode strings automatically.  That behavior by\ndefault is controlled by the JSON_AS_ASCII configuration variable\nand can be overridden by the simplejson ensure_ascii parameter.\n"
    ),
    _(
        "escape(s) \nConvert the characters &, <, >, ‘, and ” in string s to HTML-safe\nsequences.  Use this if you need to display text that might contain\nsuch characters in HTML.  Marks return value as markup string.\n"
    ),
    _(
        "escape(s) \nConvert the characters &, <, >, ‘, and ” in string s to HTML-safe\nsequences.  Use this if you need to display text that might contain\nsuch characters in HTML.  Marks return value as markup string.\n"
    ),
    _(
        "flash(message, category='message') \nFlashes a message to the next request.  In order to remove the\nflashed message from the session and to display it to the user,\nthe template has to call get_flashed_messages().\n\nChangelog\nChanged in version 0.3: category parameter added.\n\n\n\n\n\nParameters:\nmessage -- the message to be flashed.\ncategory -- the category for the message.  The following values\nare recommended: 'message' for any kind of message,\n'error' for errors, 'info' for information\nmessages and 'warning' for warnings.  However any\nkind of string can be used as category.\n\n\n\n\n\n"
    ),
    _(
        "flash(message, category='message') \nFlashes a message to the next request.  In order to remove the\nflashed message from the session and to display it to the user,\nthe template has to call get_flashed_messages().\n\nChangelog\nChanged in version 0.3: category parameter added.\n\n\n\n\n\nParameters:\nmessage -- the message to be flashed.\ncategory -- the category for the message.  The following values\nare recommended: 'message' for any kind of message,\n'error' for errors, 'info' for information\nmessages and 'warning' for warnings.  However any\nkind of string can be used as category.\n\n\n\n\n\n"
    ),
    _(
        "get_flashed_messages(with_categories=False, category_filter=[]) \nPulls all flashed messages from the session and returns them.\nFurther calls in the same request to the function will return\nthe same messages.  By default just the messages are returned,\nbut when with_categories is set to True, the return value will\nbe a list of tuples in the form (category, message) instead.\nFilter the flashed messages to one or more categories by providing those\ncategories in category_filter.  This allows rendering categories in\nseparate html blocks.  The with_categories and category_filter\narguments are distinct:\n\nwith_categories controls whether categories are returned with message\ntext (True gives a tuple, where False gives just the message text).\ncategory_filter filters the messages down to only those matching the\nprovided categories.\n\nSee Message Flashing for examples.\n\nChangelog\nChanged in version 0.9: category_filter parameter added.\n\n\nChanged in version 0.3: with_categories parameter added.\n\n\n\n\n\nParameters:\nwith_categories -- set to True to also receive categories.\ncategory_filter -- whitelist of categories to limit return values\n\n\n\n\n\n"
    ),
    _(
        "get_flashed_messages(with_categories=False, category_filter=[]) \nPulls all flashed messages from the session and returns them.\nFurther calls in the same request to the function will return\nthe same messages.  By default just the messages are returned,\nbut when with_categories is set to True, the return value will\nbe a list of tuples in the form (category, message) instead.\nFilter the flashed messages to one or more categories by providing those\ncategories in category_filter.  This allows rendering categories in\nseparate html blocks.  The with_categories and category_filter\narguments are distinct:\n\nwith_categories controls whether categories are returned with message\ntext (True gives a tuple, where False gives just the message text).\ncategory_filter filters the messages down to only those matching the\nprovided categories.\n\nSee Message Flashing for examples.\n\nChangelog\nChanged in version 0.9: category_filter parameter added.\n\n\nChanged in version 0.3: with_categories parameter added.\n\n\n\n\n\nParameters:\nwith_categories -- set to True to also receive categories.\ncategory_filter -- whitelist of categories to limit return values\n\n\n\n\n\n"
    ),
    _(
        "get_template_attribute(template_name, attribute) \nLoads a macro (or variable) a template exports.  This can be used to\ninvoke a macro from within Python code.  If you for example have a\ntemplate named _cider.html with the following contents:\n{% macro hello(name) %}Hello {{ name }}!{% endmacro %}\n\n\nYou can access this from Python code like this:\nhello = get_template_attribute('_cider.html', 'hello')\nreturn hello('World')\n\n\n\nChangelog\nNew in version 0.2.\n\n\n\n\n\nParameters:\ntemplate_name -- the name of the template\nattribute -- the name of the variable of macro to access\n\n\n\n\n\n"
    ),
    _(
        "get_template_attribute(template_name, attribute) \nLoads a macro (or variable) a template exports.  This can be used to\ninvoke a macro from within Python code.  If you for example have a\ntemplate named _cider.html with the following contents:\n{% macro hello(name) %}Hello {{ name }}!{% endmacro %}\n\n\nYou can access this from Python code like this:\nhello = get_template_attribute('_cider.html', 'hello')\nreturn hello('World')\n\n\n\nChangelog\nNew in version 0.2.\n\n\n\n\n\nParameters:\ntemplate_name -- the name of the template\nattribute -- the name of the variable of macro to access\n\n\n\n\n\n"
    ),
    _(
        "has_app_context() \nWorks like has_request_context() but for the application\ncontext.  You can also just do a boolean check on the\ncurrent_app object instead.\n\nChangelog\nNew in version 0.9.\n\n"
    ),
    _(
        "has_app_context() \nWorks like has_request_context() but for the application\ncontext.  You can also just do a boolean check on the\ncurrent_app object instead.\n\nChangelog\nNew in version 0.9.\n\n"
    ),
    _(
        "has_request_context() \nIf you have code that wants to test if a request context is there or\nnot this function can be used.  For instance, you may want to take advantage\nof request information if the request object is available, but fail\nsilently if it is unavailable.\nclass User(db.Model):\n\n    def __init__(self, username, remote_addr=None):\n        self.username = username\n        if remote_addr is None and has_request_context():\n            remote_addr = request.remote_addr\n        self.remote_addr = remote_addr\n\n\nAlternatively you can also just test any of the context bound objects\n(such as request or g for truthness):\nclass User(db.Model):\n\n    def __init__(self, username, remote_addr=None):\n        self.username = username\n        if remote_addr is None and request:\n            remote_addr = request.remote_addr\n        self.remote_addr = remote_addr\n\n\n\nChangelog\nNew in version 0.7.\n\n"
    ),
    _(
        "has_request_context() \nIf you have code that wants to test if a request context is there or\nnot this function can be used.  For instance, you may want to take advantage\nof request information if the request object is available, but fail\nsilently if it is unavailable.\nclass User(db.Model):\n\n    def __init__(self, username, remote_addr=None):\n        self.username = username\n        if remote_addr is None and has_request_context():\n            remote_addr = request.remote_addr\n        self.remote_addr = remote_addr\n\n\nAlternatively you can also just test any of the context bound objects\n(such as request or g for truthness):\nclass User(db.Model):\n\n    def __init__(self, username, remote_addr=None):\n        self.username = username\n        if remote_addr is None and request:\n            remote_addr = request.remote_addr\n        self.remote_addr = remote_addr\n\n\n\nChangelog\nNew in version 0.7.\n\n"
    ),
    _(
        'jsonify(*args, **kwargs) \nThis function wraps dumps() to add a few enhancements that make\nlife easier.  It turns the JSON output into a Response\nobject with the application/json mimetype.  For convenience, it\nalso converts multiple arguments into an array or multiple keyword arguments\ninto a dict.  This means that both jsonify(1,2,3) and\njsonify([1,2,3]) serialize to [1,2,3].\nFor clarity, the JSON serialization behavior has the following differences\nfrom dumps():\n\nSingle argument: Passed straight through to dumps().\nMultiple arguments: Converted to an array before being passed to\ndumps().\nMultiple keyword arguments: Converted to a dict before being passed to\ndumps().\nBoth args and kwargs: Behavior undefined and will throw an exception.\n\nExample usage:\nfrom flask import jsonify\n\n@app.route(\'/_get_current_user\')\ndef get_current_user():\n    return jsonify(username=g.user.username,\n                   email=g.user.email,\n                   id=g.user.id)\n\n\nThis will send a JSON response like this to the browser:\n{\n    "username": "admin",\n    "email": "admin@localhost",\n    "id": 42\n}\n\n\n\nChangelog\nChanged in version 0.11: Added support for serializing top-level arrays. This introduces a\nsecurity risk in ancient browsers. See JSON Security for details.\n\nThis function’s response will be pretty printed if the\nJSONIFY_PRETTYPRINT_REGULAR config parameter is set to True or the\nFlask app is running in debug mode. Compressed (not pretty) formatting\ncurrently means no indents and no spaces after separators.\n\nChangelog\nNew in version 0.2.\n\n'
    ),
    _(
        'jsonify(*args, **kwargs) \nThis function wraps dumps() to add a few enhancements that make\nlife easier.  It turns the JSON output into a Response\nobject with the application/json mimetype.  For convenience, it\nalso converts multiple arguments into an array or multiple keyword arguments\ninto a dict.  This means that both jsonify(1,2,3) and\njsonify([1,2,3]) serialize to [1,2,3].\nFor clarity, the JSON serialization behavior has the following differences\nfrom dumps():\n\nSingle argument: Passed straight through to dumps().\nMultiple arguments: Converted to an array before being passed to\ndumps().\nMultiple keyword arguments: Converted to a dict before being passed to\ndumps().\nBoth args and kwargs: Behavior undefined and will throw an exception.\n\nExample usage:\nfrom flask import jsonify\n\n@app.route(\'/_get_current_user\')\ndef get_current_user():\n    return jsonify(username=g.user.username,\n                   email=g.user.email,\n                   id=g.user.id)\n\n\nThis will send a JSON response like this to the browser:\n{\n    "username": "admin",\n    "email": "admin@localhost",\n    "id": 42\n}\n\n\n\nChangelog\nChanged in version 0.11: Added support for serializing top-level arrays. This introduces a\nsecurity risk in ancient browsers. See JSON Security for details.\n\nThis function’s response will be pretty printed if the\nJSONIFY_PRETTYPRINT_REGULAR config parameter is set to True or the\nFlask app is running in debug mode. Compressed (not pretty) formatting\ncurrently means no indents and no spaces after separators.\n\nChangelog\nNew in version 0.2.\n\n'
    ),
    _("load(fp, **kwargs) \nLike loads() but reads from a file object.\n"),
    _("load(fp, **kwargs) \nLike loads() but reads from a file object.\n"),
    _(
        "load_dotenv(path=None) \nLoad “dotenv” files in order of precedence to set environment variables.\nIf an env var is already set it is not overwritten, so earlier files in the\nlist are preferred over later files.\nChanges the current working directory to the location of the first file\nfound, with the assumption that it is in the top level project directory\nand will be where the Python path should import local packages from.\nThis is a no-op if python-dotenv is not installed.\n\n\n\n\nParameters:path -- Load the file at this location instead of searching.\n\nReturns:True if a file was loaded.\n\n\n\n\nNew in version 1.0.\n\n\nChangelog"
    ),
    _(
        "load_dotenv(path=None) \nLoad “dotenv” files in order of precedence to set environment variables.\nIf an env var is already set it is not overwritten, so earlier files in the\nlist are preferred over later files.\nChanges the current working directory to the location of the first file\nfound, with the assumption that it is in the top level project directory\nand will be where the Python path should import local packages from.\nThis is a no-op if python-dotenv is not installed.\n\n\n\n\nParameters:path -- Load the file at this location instead of searching.\n\nReturns:True if a file was loaded.\n\n\n\n\nNew in version 1.0.\n\n\nChangelog"
    ),
    _(
        "loads(s, **kwargs) \nUnserialize a JSON object from a string s by using the application’s\nconfigured decoder (json_decoder) if there is an\napplication on the stack.\n"
    ),
    _(
        "loads(s, **kwargs) \nUnserialize a JSON object from a string s by using the application’s\nconfigured decoder (json_decoder) if there is an\napplication on the stack.\n"
    ),
    _(
        "make_response(*args) \nSometimes it is necessary to set additional headers in a view.  Because\nviews do not have to return response objects but can return a value that\nis converted into a response object by Flask itself, it becomes tricky to\nadd headers to it.  This function can be called instead of using a return\nand you will get a response object which you can use to attach headers.\nIf view looked like this and you want to add a new header:\ndef index():\n    return render_template('index.html', foo=42)\n\n\nYou can now do something like this:\ndef index():\n    response = make_response(render_template('index.html', foo=42))\n    response.headers['X-Parachutes'] = 'parachutes are cool'\n    return response\n\n\nThis function accepts the very same arguments you can return from a\nview function.  This for example creates a response with a 404 error\ncode:\nresponse = make_response(render_template('not_found.html'), 404)\n\n\nThe other use case of this function is to force the return value of a\nview function into a response which is helpful with view\ndecorators:\nresponse = make_response(view_function())\nresponse.headers['X-Parachutes'] = 'parachutes are cool'\n\n\nInternally this function does the following things:\n\nif no arguments are passed, it creates a new response argument\nif one argument is passed, flask.Flask.make_response()\nis invoked with it.\nif more than one argument is passed, the arguments are passed\nto the flask.Flask.make_response() function as tuple.\n\n\nChangelog\nNew in version 0.6.\n\n"
    ),
    _(
        "make_response(*args) \nSometimes it is necessary to set additional headers in a view.  Because\nviews do not have to return response objects but can return a value that\nis converted into a response object by Flask itself, it becomes tricky to\nadd headers to it.  This function can be called instead of using a return\nand you will get a response object which you can use to attach headers.\nIf view looked like this and you want to add a new header:\ndef index():\n    return render_template('index.html', foo=42)\n\n\nYou can now do something like this:\ndef index():\n    response = make_response(render_template('index.html', foo=42))\n    response.headers['X-Parachutes'] = 'parachutes are cool'\n    return response\n\n\nThis function accepts the very same arguments you can return from a\nview function.  This for example creates a response with a 404 error\ncode:\nresponse = make_response(render_template('not_found.html'), 404)\n\n\nThe other use case of this function is to force the return value of a\nview function into a response which is helpful with view\ndecorators:\nresponse = make_response(view_function())\nresponse.headers['X-Parachutes'] = 'parachutes are cool'\n\n\nInternally this function does the following things:\n\nif no arguments are passed, it creates a new response argument\nif one argument is passed, flask.Flask.make_response()\nis invoked with it.\nif more than one argument is passed, the arguments are passed\nto the flask.Flask.make_response() function as tuple.\n\n\nChangelog\nNew in version 0.6.\n\n"
    ),
    _(
        "pass_script_info(f) \nMarks a function so that an instance of ScriptInfo is passed\nas first argument to the click callback.\n"
    ),
    _(
        "pass_script_info(f) \nMarks a function so that an instance of ScriptInfo is passed\nas first argument to the click callback.\n"
    ),
    _(
        "redirect(location, code=302, Response=None) \nReturns a response object (a WSGI application) that, if called,\nredirects the client to the target location.  Supported codes are 301,\n302, 303, 305, and 307.  300 is not supported because it’s not a real\nredirect and 304 because it’s the answer for a request with a request\nwith defined If-Modified-Since headers.\n\nChangelog\nNew in version 0.10: The class used for the Response object can now be passed in.\n\n\nNew in version 0.6: The location can now be a unicode string that is encoded using\nthe iri_to_uri() function.\n\n\n\n\n\nParameters:\nlocation -- the location the response should redirect to.\ncode -- the redirect status code. defaults to 302.\nResponse (class) -- a Response class to use when instantiating a\nresponse. The default is werkzeug.wrappers.Response if\nunspecified.\n\n\n\n\n\n"
    ),
    _(
        "redirect(location, code=302, Response=None) \nReturns a response object (a WSGI application) that, if called,\nredirects the client to the target location.  Supported codes are 301,\n302, 303, 305, and 307.  300 is not supported because it’s not a real\nredirect and 304 because it’s the answer for a request with a request\nwith defined If-Modified-Since headers.\n\nChangelog\nNew in version 0.10: The class used for the Response object can now be passed in.\n\n\nNew in version 0.6: The location can now be a unicode string that is encoded using\nthe iri_to_uri() function.\n\n\n\n\n\nParameters:\nlocation -- the location the response should redirect to.\ncode -- the redirect status code. defaults to 302.\nResponse (class) -- a Response class to use when instantiating a\nresponse. The default is werkzeug.wrappers.Response if\nunspecified.\n\n\n\n\n\n"
    ),
    _(
        "render_template(template_name_or_list, **context) \nRenders a template from the template folder with the given\ncontext.\n\n\n\n\nParameters:\ntemplate_name_or_list -- the name of the template to be\nrendered, or an iterable with template names\nthe first one existing will be rendered\ncontext -- the variables that should be available in the\ncontext of the template.\n\n\n\n\n\n"
    ),
    _(
        "render_template(template_name_or_list, **context) \nRenders a template from the template folder with the given\ncontext.\n\n\n\n\nParameters:\ntemplate_name_or_list -- the name of the template to be\nrendered, or an iterable with template names\nthe first one existing will be rendered\ncontext -- the variables that should be available in the\ncontext of the template.\n\n\n\n\n\n"
    ),
    _(
        "render_template_string(source, **context) \nRenders a template from the given template source string\nwith the given context. Template variables will be autoescaped.\n\n\n\n\nParameters:\nsource -- the source code of the template to be\nrendered\ncontext -- the variables that should be available in the\ncontext of the template.\n\n\n\n\n\n"
    ),
    _(
        "render_template_string(source, **context) \nRenders a template from the given template source string\nwith the given context. Template variables will be autoescaped.\n\n\n\n\nParameters:\nsource -- the source code of the template to be\nrendered\ncontext -- the variables that should be available in the\ncontext of the template.\n\n\n\n\n\n"
    ),
    _(
        "safe_join(directory, *pathnames) \nSafely join directory and zero or more untrusted pathnames\ncomponents.\nExample usage:\n@app.route('/wiki/<path:filename>')\ndef wiki_page(filename):\n    filename = safe_join(app.config['WIKI_FOLDER'], filename)\n    with open(filename, 'rb') as fd:\n        content = fd.read()  # Read and process the file content...\n\n\n\n\n\n\nParameters:\ndirectory -- the trusted base directory.\npathnames -- the untrusted pathnames relative to that directory.\n\n\n\nRaises:NotFound if one or more passed\npaths fall out of its boundaries.\n\n\n\n\n"
    ),
    _(
        "safe_join(directory, *pathnames) \nSafely join directory and zero or more untrusted pathnames\ncomponents.\nExample usage:\n@app.route('/wiki/<path:filename>')\ndef wiki_page(filename):\n    filename = safe_join(app.config['WIKI_FOLDER'], filename)\n    with open(filename, 'rb') as fd:\n        content = fd.read()  # Read and process the file content...\n\n\n\n\n\n\nParameters:\ndirectory -- the trusted base directory.\npathnames -- the untrusted pathnames relative to that directory.\n\n\n\nRaises:NotFound if one or more passed\npaths fall out of its boundaries.\n\n\n\n\n"
    ),
    _(
        "send_file(filename_or_fp, mimetype=None, as_attachment=False, attachment_filename=None, add_etags=True, cache_timeout=None, conditional=False, last_modified=None) \nSends the contents of a file to the client.  This will use the\nmost efficient method available and configured.  By default it will\ntry to use the WSGI server’s file_wrapper support.  Alternatively\nyou can set the application’s use_x_sendfile attribute\nto True to directly emit an X-Sendfile header.  This however\nrequires support of the underlying webserver for X-Sendfile.\nBy default it will try to guess the mimetype for you, but you can\nalso explicitly provide one.  For extra security you probably want\nto send certain files as attachment (HTML for instance).  The mimetype\nguessing requires a filename or an attachment_filename to be\nprovided.\nETags will also be attached automatically if a filename is provided. You\ncan turn this off by setting add_etags=False.\nIf conditional=True and filename is provided, this method will try to\nupgrade the response stream to support range requests.  This will allow\nthe request to be answered with partial content response.\nPlease never pass filenames to this function from user sources;\nyou should use send_from_directory() instead.\n\nChanged in version 1.0: UTF-8 filenames, as specified in RFC 2231, are supported.\n\n\nChangelog\nChanged in version 0.12: The filename is no longer automatically inferred from file objects. If\nyou want to use automatic mimetype and etag support, pass a filepath via\nfilename_or_fp or attachment_filename.\n\n\nChanged in version 0.12: The attachment_filename is preferred over filename for MIME-type\ndetection.\n\n\nChanged in version 0.9: cache_timeout pulls its default from application config, when None.\n\n\nChanged in version 0.7: mimetype guessing and etag support for file objects was\ndeprecated because it was unreliable.  Pass a filename if you are\nable to, otherwise attach an etag yourself.  This functionality\nwill be removed in Flask 1.0\n\n\nNew in version 0.5: The add_etags, cache_timeout and conditional parameters were\nadded.  The default behavior is now to attach etags.\n\n\nNew in version 0.2.\n\n\n\n\n\nParameters:\nfilename_or_fp -- the filename of the file to send.\nThis is relative to the root_path\nif a relative path is specified.\nAlternatively a file object might be provided in\nwhich case X-Sendfile might not work and fall\nback to the traditional method.  Make sure that the\nfile pointer is positioned at the start of data to\nsend before calling send_file().\nmimetype -- the mimetype of the file if provided. If a file path is\ngiven, auto detection happens as fallback, otherwise an\nerror will be raised.\nas_attachment -- set to True if you want to send this file with\na Content-Disposition: attachment header.\nattachment_filename -- the filename for the attachment if it\ndiffers from the file’s filename.\nadd_etags -- set to False to disable attaching of etags.\nconditional -- set to True to enable conditional responses.\ncache_timeout -- the timeout in seconds for the headers. When None\n(default), this value is set by\nget_send_file_max_age() of\ncurrent_app.\nlast_modified -- set the Last-Modified header to this value,\na datetime or timestamp.\nIf a file was passed, this overrides its mtime.\n\n\n\n\n\n"
    ),
    _(
        "send_file(filename_or_fp, mimetype=None, as_attachment=False, attachment_filename=None, add_etags=True, cache_timeout=None, conditional=False, last_modified=None) \nSends the contents of a file to the client.  This will use the\nmost efficient method available and configured.  By default it will\ntry to use the WSGI server’s file_wrapper support.  Alternatively\nyou can set the application’s use_x_sendfile attribute\nto True to directly emit an X-Sendfile header.  This however\nrequires support of the underlying webserver for X-Sendfile.\nBy default it will try to guess the mimetype for you, but you can\nalso explicitly provide one.  For extra security you probably want\nto send certain files as attachment (HTML for instance).  The mimetype\nguessing requires a filename or an attachment_filename to be\nprovided.\nETags will also be attached automatically if a filename is provided. You\ncan turn this off by setting add_etags=False.\nIf conditional=True and filename is provided, this method will try to\nupgrade the response stream to support range requests.  This will allow\nthe request to be answered with partial content response.\nPlease never pass filenames to this function from user sources;\nyou should use send_from_directory() instead.\n\nChanged in version 1.0: UTF-8 filenames, as specified in RFC 2231, are supported.\n\n\nChangelog\nChanged in version 0.12: The filename is no longer automatically inferred from file objects. If\nyou want to use automatic mimetype and etag support, pass a filepath via\nfilename_or_fp or attachment_filename.\n\n\nChanged in version 0.12: The attachment_filename is preferred over filename for MIME-type\ndetection.\n\n\nChanged in version 0.9: cache_timeout pulls its default from application config, when None.\n\n\nChanged in version 0.7: mimetype guessing and etag support for file objects was\ndeprecated because it was unreliable.  Pass a filename if you are\nable to, otherwise attach an etag yourself.  This functionality\nwill be removed in Flask 1.0\n\n\nNew in version 0.5: The add_etags, cache_timeout and conditional parameters were\nadded.  The default behavior is now to attach etags.\n\n\nNew in version 0.2.\n\n\n\n\n\nParameters:\nfilename_or_fp -- the filename of the file to send.\nThis is relative to the root_path\nif a relative path is specified.\nAlternatively a file object might be provided in\nwhich case X-Sendfile might not work and fall\nback to the traditional method.  Make sure that the\nfile pointer is positioned at the start of data to\nsend before calling send_file().\nmimetype -- the mimetype of the file if provided. If a file path is\ngiven, auto detection happens as fallback, otherwise an\nerror will be raised.\nas_attachment -- set to True if you want to send this file with\na Content-Disposition: attachment header.\nattachment_filename -- the filename for the attachment if it\ndiffers from the file’s filename.\nadd_etags -- set to False to disable attaching of etags.\nconditional -- set to True to enable conditional responses.\ncache_timeout -- the timeout in seconds for the headers. When None\n(default), this value is set by\nget_send_file_max_age() of\ncurrent_app.\nlast_modified -- set the Last-Modified header to this value,\na datetime or timestamp.\nIf a file was passed, this overrides its mtime.\n\n\n\n\n\n"
    ),
    _(
        "send_from_directory(directory, filename, **options) \nSend a file from a given directory with send_file().  This\nis a secure way to quickly expose static files from an upload folder\nor something similar.\nExample usage:\n@app.route('/uploads/<path:filename>')\ndef download_file(filename):\n    return send_from_directory(app.config['UPLOAD_FOLDER'],\n                               filename, as_attachment=True)\n\n\n\nSending files and Performance\nIt is strongly recommended to activate either X-Sendfile support in\nyour webserver or (if no authentication happens) to tell the webserver\nto serve files for the given path on its own without calling into the\nweb application for improved performance.\n\n\nChangelog\nNew in version 0.5.\n\n\n\n\n\nParameters:\ndirectory -- the directory where all the files are stored.\nfilename -- the filename relative to that directory to\ndownload.\noptions -- optional keyword arguments that are directly\nforwarded to send_file().\n\n\n\n\n\n"
    ),
    _(
        "send_from_directory(directory, filename, **options) \nSend a file from a given directory with send_file().  This\nis a secure way to quickly expose static files from an upload folder\nor something similar.\nExample usage:\n@app.route('/uploads/<path:filename>')\ndef download_file(filename):\n    return send_from_directory(app.config['UPLOAD_FOLDER'],\n                               filename, as_attachment=True)\n\n\n\nSending files and Performance\nIt is strongly recommended to activate either X-Sendfile support in\nyour webserver or (if no authentication happens) to tell the webserver\nto serve files for the given path on its own without calling into the\nweb application for improved performance.\n\n\nChangelog\nNew in version 0.5.\n\n\n\n\n\nParameters:\ndirectory -- the directory where all the files are stored.\nfilename -- the filename relative to that directory to\ndownload.\noptions -- optional keyword arguments that are directly\nforwarded to send_file().\n\n\n\n\n\n"
    ),
    _(
        "session() \nThe session object works pretty much like an ordinary dict, with the\ndifference that it keeps track on modifications.\n\nThis is a proxy.  See Notes On Proxies for more information.\n\nThe following attributes are interesting:\n\n"
    ),
    _(
        "session() \nThe session object works pretty much like an ordinary dict, with the\ndifference that it keeps track on modifications.\n\nThis is a proxy.  See Notes On Proxies for more information.\n\nThe following attributes are interesting:\n\n"
    ),
    _(
        "session.modified() \nTrue if the session object detected a modification.  Be advised\nthat modifications on mutable structures are not picked up\nautomatically, in that situation you have to explicitly set the\nattribute to True yourself.  Here an example:\n# this change is not picked up because a mutable object (here\n# a list) is changed.\nsession['objects'].append(42)\n# so mark it as modified yourself\nsession.modified = True\n\n\n"
    ),
    _(
        "session.modified() \nTrue if the session object detected a modification.  Be advised\nthat modifications on mutable structures are not picked up\nautomatically, in that situation you have to explicitly set the\nattribute to True yourself.  Here an example:\n# this change is not picked up because a mutable object (here\n# a list) is changed.\nsession['objects'].append(42)\n# so mark it as modified yourself\nsession.modified = True\n\n\n"
    ),
    _("session.new() \nTrue if the session is new, False otherwise.\n"),
    _("session.new() \nTrue if the session is new, False otherwise.\n"),
    _(
        "session.permanent() \nIf set to True the session lives for\npermanent_session_lifetime seconds.  The\ndefault is 31 days.  If set to False (which is the default) the\nsession will be deleted when the user closes the browser.\n"
    ),
    _(
        "session.permanent() \nIf set to True the session lives for\npermanent_session_lifetime seconds.  The\ndefault is 31 days.  If set to False (which is the default) the\nsession will be deleted when the user closes the browser.\n"
    ),
    _(
        "stream_with_context(generator_or_function) \nRequest contexts disappear when the response is started on the server.\nThis is done for efficiency reasons and to make it less likely to encounter\nmemory leaks with badly written WSGI middlewares.  The downside is that if\nyou are using streamed responses, the generator cannot access request bound\ninformation any more.\nThis function however can help you keep the context around for longer:\nfrom flask import stream_with_context, request, Response\n\n@app.route('/stream')\ndef streamed_response():\n    @stream_with_context\n    def generate():\n        yield 'Hello '\n        yield request.args['name']\n        yield '!'\n    return Response(generate())\n\n\nAlternatively it can also be used around a specific generator:\nfrom flask import stream_with_context, request, Response\n\n@app.route('/stream')\ndef streamed_response():\n    def generate():\n        yield 'Hello '\n        yield request.args['name']\n        yield '!'\n    return Response(stream_with_context(generate()))\n\n\n\nChangelog\nNew in version 0.9.\n\n"
    ),
    _(
        "stream_with_context(generator_or_function) \nRequest contexts disappear when the response is started on the server.\nThis is done for efficiency reasons and to make it less likely to encounter\nmemory leaks with badly written WSGI middlewares.  The downside is that if\nyou are using streamed responses, the generator cannot access request bound\ninformation any more.\nThis function however can help you keep the context around for longer:\nfrom flask import stream_with_context, request, Response\n\n@app.route('/stream')\ndef streamed_response():\n    @stream_with_context\n    def generate():\n        yield 'Hello '\n        yield request.args['name']\n        yield '!'\n    return Response(generate())\n\n\nAlternatively it can also be used around a specific generator:\nfrom flask import stream_with_context, request, Response\n\n@app.route('/stream')\ndef streamed_response():\n    def generate():\n        yield 'Hello '\n        yield request.args['name']\n        yield '!'\n    return Response(stream_with_context(generate()))\n\n\n\nChangelog\nNew in version 0.9.\n\n"
    ),
    _(
        "url_for(endpoint, **values) \nGenerates a URL to the given endpoint with the method provided.\nVariable arguments that are unknown to the target endpoint are appended\nto the generated URL as query arguments.  If the value of a query argument\nis None, the whole pair is skipped.  In case blueprints are active\nyou can shortcut references to the same blueprint by prefixing the\nlocal endpoint with a dot (.).\nThis will reference the index function local to the current blueprint:\nurl_for('.index')\n\n\nFor more information, head over to the Quickstart.\nTo integrate applications, Flask has a hook to intercept URL build\nerrors through Flask.url_build_error_handlers.  The url_for\nfunction results in a BuildError when the current\napp does not have a URL for the given endpoint and values.  When it does, the\ncurrent_app calls its url_build_error_handlers if\nit is not None, which can return a string to use as the result of\nurl_for (instead of url_for’s default to raise the\nBuildError exception) or re-raise the exception.\nAn example:\ndef external_url_handler(error, endpoint, values):\n    \"Looks up an external URL when `url_for` cannot build a URL.\"\n    # This is an example of hooking the build_error_handler.\n    # Here, lookup_url is some utility function you've built\n    # which looks up the endpoint in some external URL registry.\n    url = lookup_url(endpoint, **values)\n    if url is None:\n        # External lookup did not have a URL.\n        # Re-raise the BuildError, in context of original traceback.\n        exc_type, exc_value, tb = sys.exc_info()\n        if exc_value is error:\n            raise exc_type, exc_value, tb\n        else:\n            raise error\n    # url_for will use this result, instead of raising BuildError.\n    return url\n\napp.url_build_error_handlers.append(external_url_handler)\n\n\nHere, error is the instance of BuildError, and\nendpoint and values are the arguments passed into url_for.  Note\nthat this is for building URLs outside the current application, and not for\nhandling 404 NotFound errors.\n\nChangelog\nNew in version 0.10: The _scheme parameter was added.\n\n\nNew in version 0.9: The _anchor and _method parameters were added.\n\n\nNew in version 0.9: Calls Flask.handle_build_error() on\nBuildError.\n\n\n\n\n\nParameters:\nendpoint -- the endpoint of the URL (name of the function)\nvalues -- the variable arguments of the URL rule\n_external -- if set to True, an absolute URL is generated. Server\naddress can be changed via SERVER_NAME configuration variable which\ndefaults to localhost.\n_scheme -- a string specifying the desired URL scheme. The _external\nparameter must be set to True or a ValueError is raised. The default\nbehavior uses the same scheme as the current request, or\nPREFERRED_URL_SCHEME from the app configuration if no\nrequest context is available. As of Werkzeug 0.10, this also can be set\nto an empty string to build protocol-relative URLs.\n_anchor -- if provided this is added as anchor to the URL.\n_method -- if provided this explicitly specifies an HTTP method.\n\n\n\n\n\n"
    ),
    _(
        "url_for(endpoint, **values) \nGenerates a URL to the given endpoint with the method provided.\nVariable arguments that are unknown to the target endpoint are appended\nto the generated URL as query arguments.  If the value of a query argument\nis None, the whole pair is skipped.  In case blueprints are active\nyou can shortcut references to the same blueprint by prefixing the\nlocal endpoint with a dot (.).\nThis will reference the index function local to the current blueprint:\nurl_for('.index')\n\n\nFor more information, head over to the Quickstart.\nTo integrate applications, Flask has a hook to intercept URL build\nerrors through Flask.url_build_error_handlers.  The url_for\nfunction results in a BuildError when the current\napp does not have a URL for the given endpoint and values.  When it does, the\ncurrent_app calls its url_build_error_handlers if\nit is not None, which can return a string to use as the result of\nurl_for (instead of url_for’s default to raise the\nBuildError exception) or re-raise the exception.\nAn example:\ndef external_url_handler(error, endpoint, values):\n    \"Looks up an external URL when `url_for` cannot build a URL.\"\n    # This is an example of hooking the build_error_handler.\n    # Here, lookup_url is some utility function you've built\n    # which looks up the endpoint in some external URL registry.\n    url = lookup_url(endpoint, **values)\n    if url is None:\n        # External lookup did not have a URL.\n        # Re-raise the BuildError, in context of original traceback.\n        exc_type, exc_value, tb = sys.exc_info()\n        if exc_value is error:\n            raise exc_type, exc_value, tb\n        else:\n            raise error\n    # url_for will use this result, instead of raising BuildError.\n    return url\n\napp.url_build_error_handlers.append(external_url_handler)\n\n\nHere, error is the instance of BuildError, and\nendpoint and values are the arguments passed into url_for.  Note\nthat this is for building URLs outside the current application, and not for\nhandling 404 NotFound errors.\n\nChangelog\nNew in version 0.10: The _scheme parameter was added.\n\n\nNew in version 0.9: The _anchor and _method parameters were added.\n\n\nNew in version 0.9: Calls Flask.handle_build_error() on\nBuildError.\n\n\n\n\n\nParameters:\nendpoint -- the endpoint of the URL (name of the function)\nvalues -- the variable arguments of the URL rule\n_external -- if set to True, an absolute URL is generated. Server\naddress can be changed via SERVER_NAME configuration variable which\ndefaults to localhost.\n_scheme -- a string specifying the desired URL scheme. The _external\nparameter must be set to True or a ValueError is raised. The default\nbehavior uses the same scheme as the current request, or\nPREFERRED_URL_SCHEME from the app configuration if no\nrequest context is available. As of Werkzeug 0.10, this also can be set\nto an empty string to build protocol-relative URLs.\n_anchor -- if provided this is added as anchor to the URL.\n_method -- if provided this explicitly specifies an HTTP method.\n\n\n\n\n\n"
    ),
    _(
        "with_appcontext(f) \nWraps a callback so that it’s guaranteed to be executed with the\nscript’s application context.  If callbacks are registered directly\nto the app.cli object then they are wrapped with this function\nby default unless it’s disabled.\n"
    ),
    _(
        "with_appcontext(f) \nWraps a callback so that it’s guaranteed to be executed with the\nscript’s application context.  If callbacks are registered directly\nto the app.cli object then they are wrapped with this function\nby default unless it’s disabled.\n"
    ),
]
