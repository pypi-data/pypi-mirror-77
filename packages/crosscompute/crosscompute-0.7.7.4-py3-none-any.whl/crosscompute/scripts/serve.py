import datetime
import re
import simplejson as json
import webbrowser
from collections import OrderedDict
from invisibleroads_macros.disk import (
    compress_zip, copy_file, copy_text, get_file_extension, get_absolute_path,
    link_safely, load_text, make_unique_folder, move_path, remove_safely)
from invisibleroads_macros.exceptions import BadPath
from invisibleroads_macros.log import get_log
from invisibleroads_macros.text import cut_and_strip
from invisibleroads_posts import (
    InvisibleRoadsConfigurator, add_routes_for_fused_assets,
    add_website_dependency)
from invisibleroads_posts.views import expect_param
from invisibleroads_uploads.models import Upload
from markupsafe import Markup
from mistune import markdown
from os import environ
from os.path import exists, join, realpath
from pyramid.httpexceptions import (
    HTTPBadRequest, HTTPForbidden, HTTPNotFound, HTTPSeeOther)
from pyramid.renderers import get_renderer
from pyramid.request import Request
from pyramid.response import FileResponse, Response
from six import text_type
from traceback import format_exc
from wsgiref.simple_server import make_server

from . import ToolScript, corral_arguments, run_script
from ..configurations import (
    ResultConfiguration, get_default_key, get_default_value,
    parse_data_dictionary_from, ARGUMENT_PATTERN)
from ..exceptions import DataParseError, DataTypeError
from ..models import Result, Tool
from ..settings import S
from ..symmetries import suppress
from ..types import (
    DataItem, DataType, get_data_type, DATA_TYPE_BY_NAME,
    RESERVED_ARGUMENT_NAMES)


HELP = {
    'return_code': 'There was an error while running the script.',
    'raw_output': 'The script generated raw output.',
}
L = get_log(__name__)
MARKDOWN_TITLE_PATTERN = re.compile(r'^#[^#]\s*(.+)')
TOOL_PATH_PATTERN = re.compile(r'tools/(\w+)/(.+)$')
RESULT_PATH_PATTERN = re.compile(r'results/(\w+)/([xy])/(.+)$')
BRAND_URL = 'https://crosscompute.com'
WEBSITE_VERSION = '0.7.3.1'
WEBSITE_NAME = 'CrossCompute'
WEBSITE_OWNER = 'CrossCompute Inc'


class ServeScript(ToolScript):

    def configure(self, argument_subparser):
        super(ServeScript, self).configure(argument_subparser)
        argument_subparser.add_argument(
            '--host', default='127.0.0.1')
        argument_subparser.add_argument(
            '--port', default=4444, type=int)
        argument_subparser.add_argument(
            '--base_url', default='/')
        argument_subparser.add_argument(
            '--brand_url', default=BRAND_URL)
        argument_subparser.add_argument(
            '--website_version', default=WEBSITE_VERSION)
        argument_subparser.add_argument(
            '--website_name', default=WEBSITE_NAME)
        argument_subparser.add_argument(
            '--website_owner', default=WEBSITE_OWNER)
        argument_subparser.add_argument(
            '--without_browser', action='store_true')
        argument_subparser.add_argument(
            '--without_logging', action='store_true')

    def run(self, args):
        tool_definition, data_folder = super(ServeScript, self).run(args)
        app = get_app(
            tool_definition, data_folder, args.website_version,
            args.website_name, args.website_owner, args.brand_url,
            args.base_url, args.without_logging)
        app_url = 'http://%s:%s/t/1' % (args.host, args.port)
        if not args.without_browser:
            webbrowser.open_new_tab(app_url)
        server = make_server(args.host, args.port, app)
        print('Running on http://%s:%s' % (args.host, args.port))
        with suppress(KeyboardInterrupt):
            server.serve_forever()


class ResultRequest(Request):

    reserved_argument_names = RESERVED_ARGUMENT_NAMES
    ResultClass = Result

    def __init__(self, request):
        self.__dict__.update(request.__dict__)
        self.data_folder = request.data_folder

    def prepare_arguments(self, tool_definition, raw_arguments):
        draft_folder = make_unique_folder(join(
            self.data_folder, 'drafts', Result._plural), length=16)
        try:
            result_arguments = self.collect_arguments(
                tool_definition, raw_arguments, draft_folder)
        except DataParseError as e:
            raise HTTPBadRequest(e.message_by_name)
        result = self.spawn_result()
        try:
            result.arguments = corral_arguments(result.get_source_folder(
                self.data_folder), result_arguments, move_path)
        except IOError as e:
            raise HTTPBadRequest({
                e.args[0]: 'file not found (%s)' % e.args[1]})
        remove_safely(draft_folder)
        return result

    def collect_arguments(self, tool_definition, raw_arguments, draft_folder):
        arguments, errors = OrderedDict(), OrderedDict()
        configuration_folder = tool_definition['configuration_folder']
        for argument_name in tool_definition['argument_names']:
            if argument_name in self.reserved_argument_names:
                continue
            if argument_name.endswith('_path'):
                argument_noun = argument_name[:-5]
                default_path = get_default_value(
                    argument_name, tool_definition)
                try:
                    v = self.prepare_argument_path(
                        argument_noun, raw_arguments, draft_folder,
                        default_path)
                except (IOError, ValueError) as e:
                    L.debug(e)
                    errors[argument_noun] = 'invalid'
                    continue
                except KeyError:
                    errors[argument_noun] = 'required'
                    continue
            elif argument_name in raw_arguments:
                v = raw_arguments[argument_name]
            else:
                data_type = get_data_type(argument_name)
                for file_format in data_type.formats:
                    raw_argument_name = '%s_%s' % (argument_name, file_format)
                    if raw_argument_name in raw_arguments:
                        v = raw_arguments[raw_argument_name]
                        break
                else:
                    errors[argument_name] = 'required'
                    continue
            arguments[argument_name] = v
        if errors:
            raise DataParseError(errors, arguments)
        return parse_data_dictionary_from(arguments, configuration_folder, [
            Result.get_parent_folder(self.data_folder),
            draft_folder], tool_definition)

    def spawn_result(self):
        return Result.spawn(self.data_folder)

    def prepare_argument_path(
            self, argument_noun, raw_arguments, draft_folder, default_path):
        data_type = get_data_type(argument_noun)
        # If client sent direct content (x_table_csv), save it
        for file_format in data_type.formats:
            raw_argument_name = '%s_%s' % (argument_noun, file_format)
            if raw_argument_name not in raw_arguments:
                continue
            source_text = raw_arguments[raw_argument_name]
            target_name = '%s.%s' % (argument_noun, file_format)
            return copy_text(join(draft_folder, target_name), source_text)
        # Raise KeyError if client did not specify noun (x_table)
        v = raw_arguments[argument_noun]
        # If client sent multipart content, save it
        if hasattr(v, 'file'):
            target_name = argument_noun + get_file_extension(v.filename)
            return copy_file(join(draft_folder, target_name), v.file)
        # If client sent empty content, use default
        if v == '':
            if not default_path:
                raise KeyError
            target_name = argument_noun + get_file_extension(default_path)
            return link_safely(join(draft_folder, target_name), default_path)
        # If client sent a relative path (x_table=11/x/y.csv), find it
        if '/' in v:
            source_path = self.get_file_path(*parse_result_relative_path(v))
            target_name = argument_noun + get_file_extension(source_path)
            return link_safely(join(draft_folder, target_name), source_path)
        # If client sent an upload id (x_table=x), find it
        try:
            upload = Upload.get_from(self, record_id=v)
        except HTTPNotFound as e:
            raise ValueError(e)
        source_path = realpath(join(upload.folder, data_type.get_file_name()))
        target_name = argument_noun + get_file_extension(source_path)
        target_path = move_path(join(draft_folder, target_name), source_path)
        remove_safely(upload.folder)
        return target_path

    def get_file_path(self, result_id, folder_name, path):
        try:
            result = self.ResultClass.get_from(self, record_id=result_id)
        except HTTPNotFound:
            raise IOError
        result_folder = result.get_folder(self.data_folder)
        parent_folder = join(result_folder, folder_name)
        tool = result.tool
        return get_absolute_path(path, parent_folder, external_folders=[
            tool.get_folder(self.data_folder)])


def get_app(
        tool_definition, data_folder, website_version=WEBSITE_VERSION,
        website_name=WEBSITE_NAME, website_owner=WEBSITE_OWNER,
        brand_url=BRAND_URL, base_url='/', without_logging=False):
    S.update({
        'data.folder': data_folder,
        'website.version': website_version,
        'website.name': website_name,
        'website.owner': website_owner,
        'website.year': datetime.datetime.now().year,
        'website.brand_url': brand_url,
        'website.base_url': base_url,
        'website.base_template':
            'invisibleroads_posts:templates/base.jinja2',
        'website.page_not_found_template':
            'invisibleroads_posts:templates/404.jinja2',
        'website.root_assets': [
            'invisibleroads_posts:assets/favicon.ico',
            'invisibleroads_posts:assets/robots.txt'],
        'upload.id.length': 32,
        'client_cache.http.expiration_time_in_seconds': 3600,
        'jinja2.directories': 'crosscompute:templates',
        'jinja2.lstrip_blocks': True,
        'jinja2.trim_blocks': True,
        'without_logging': without_logging,
    })
    S['tool_definition'] = tool_definition
    config = InvisibleRoadsConfigurator(settings=S)
    config.include('invisibleroads_posts')
    includeme(config)
    add_routes(config)
    add_routes_for_fused_assets(config)
    return config.make_wsgi_app()


def includeme(config):
    config.include('invisibleroads_uploads')
    configure_jinja2_environment(config)
    add_website_dependency(config)
    add_routes_for_data_types(config)


def configure_jinja2_environment(config):
    settings = config.registry.settings
    jinja2_environment = config.get_jinja2_environment()
    jinja2_environment.filters.update({
        'markdown': lambda x: Markup(markdown(x, escape=True, hard_wrap=True)),
    })
    jinja2_environment.globals.update({
        'item_template': settings.get(
            'crosscompute.item_template',
            'crosscompute:templates/item.jinja2'),
        'get_environment_variable': lambda key, default: settings.get(
            key.lower(), environ.get(key.upper(), default)),
    })


def add_routes_for_data_types(config):
    for data_type_name, data_type in DATA_TYPE_BY_NAME.items():
        module_name = data_type.__module__
        for relative_view_url in data_type.views:
            # Get route_url
            route_name = '%s/%s' % (data_type_name, relative_view_url)
            route_url = '/c/' + route_name.replace('_', '-')
            # Get view
            view = config.maybe_dotted(module_name + '.' + relative_view_url)
            # Add view
            config.add_route(route_name, route_url)
            config.add_view(
                view, permission='tool-run', require_csrf=False,
                route_name=route_name)
        add_website_dependency(config, module_name)


def parse_template_from(tool_definition, template_type, data_items):
    template_text = get_template_text(tool_definition, template_type)
    if not template_text or not data_items:
        title, parts = '', data_items
    else:
        title = parse_template_title(template_text)
        parts = parse_template_parts(template_text, data_items)
    if not title:
        title = tool_definition['tool_name']
    return title, parts


def parse_template_title(template_text):
    try:
        title = MARKDOWN_TITLE_PATTERN.search(template_text).group(1)
    except AttributeError:
        title = ''
    return title


def parse_template_parts(template_text, data_items):
    content = MARKDOWN_TITLE_PATTERN.sub('', template_text).strip()
    parts = []
    data_item_by_key = {x.key: x for x in data_items}
    for index, x in enumerate(ARGUMENT_PATTERN.split(content)):
        x = x.strip()
        if not x:
            continue
        if x.startswith('{') and x.endswith('}'):
            x = x.strip('{ }')
            text, help_ = cut_and_strip(x, ' ? ')
            key, name = cut_and_strip(text, ':')
            x = data_item_by_key.get(key, '{ %s }' % x)
            if isinstance(x, DataItem):
                if name:
                    x.name = name
                if help_:
                    x.help = help_
        parts.append(x)
    for data_item in data_items:
        if data_item not in parts:
            parts.append(data_item)
    return parts


def get_template_text(tool_definition, template_type):
    path = tool_definition.get(template_type + '_template_path')
    if not path:
        return ''
    path = join(tool_definition['configuration_folder'], path)
    if not exists(path):
        return ''
    return load_text(path)


def add_routes(config):
    config.add_route('tool.json', '/t/{tool_id}.json')
    config.add_route('tool_file', '/t/{tool_id}/-/{path:.+}')
    config.add_route('tool', '/t/{tool_id}')
    config.add_route('result.json', '/r/{result_id}.json')
    config.add_route('result.zip', '/r/{result_id}/{result_name}.zip')
    config.add_route('result_file', '/r/{result_id}/{folder_name}/{path:.+}')
    config.add_route('result', '/r/{result_id}')

    config.add_view(
        index,
        route_name='index')
    config.add_view(
        run_tool_json, renderer='json', request_method='POST',
        route_name='tool.json')
    config.add_view(
        see_tool_file, request_method='GET',
        route_name='tool_file')
    config.add_view(
        see_tool, renderer='tool.jinja2', request_method='GET',
        route_name='tool')
    """
    config.add_view(
        see_result_json, renderer='json', request_method='GET',
        route_name='result.json')
    """
    config.add_view(
        see_result_zip, request_method='GET',
        route_name='result.zip')
    config.add_view(
        see_result_file, request_method='GET',
        route_name='result_file')
    config.add_view(
        see_result, renderer='result.jinja2', request_method='GET',
        route_name='result')


def index(request):
    return HTTPSeeOther(request.route_path('tool', tool_id=Tool.id))


def run_tool_json(request):
    settings = request.registry.settings
    data_folder = request.data_folder
    tool_definition = settings['tool_definition']
    result_request = ResultRequest(request)
    result = result_request.prepare_arguments(
        tool_definition, get_result_arguments_from(request))
    target_folder = result.get_target_folder(data_folder)
    run_script(
        tool_definition, result.arguments, result.folder, target_folder,
        without_logging=settings['without_logging'])
    compress_zip(target_folder)
    return {
        'result_id': result.id,
        'result_url': request.route_path('result', result_id=result.id),
    }


def see_tool_file(request):
    settings = request.registry.settings
    data_folder = request.data_folder
    tool_folder = Tool().get_folder(data_folder)
    tool_definition = settings['tool_definition']
    return get_tool_file_response(request, tool_folder, tool_definition)


def see_tool(request):
    tool = Tool.get_from(request)
    settings = request.registry.settings
    tool_definition = settings['tool_definition']
    return get_tool_template_variables(tool, tool_definition)


# def see_result_json(request): pass


def see_result_zip(request):
    result = Result.get_from(request)
    return get_result_zip_response(request, result)


def see_result_file(request):
    result = Result.get_from(request)
    return get_result_file_response(request, result)


def see_result(request):
    data_folder = request.data_folder
    result = Result.get_from(request)
    result_folder = result.get_folder(data_folder)
    return get_result_template_variables(result, result_folder)


def get_result_arguments_from(request):
    params = request.params
    x = params.get('x')
    if x is None:
        return {}
    return json.loads(x)


def import_upload_from(request, DataType, render_property_kw):
    params = request.params
    upload = Upload.get_from(request)
    name = expect_param(request, 'argument_name')
    help_ = params.get('help', '')
    try:
        value = import_upload(upload, DataType)
    except Exception as e:
        if isinstance(e, DataTypeError):
            message = text_type(e)
        else:
            message = 'Import failed'
        raise HTTPBadRequest({name: message})
    template = get_renderer(DataType.template).template_loader()
    data_item = DataItem(name, value, DataType, help_)
    html = template.make_module().render_property(
        request, data_item, **render_property_kw)
    return Response(html)


def import_upload(upload, DataType):
    try:
        value = DataType.load(upload.path)
    except Exception as e:
        traceback_text = format_exc()
        L.error(traceback_text)
        copy_text(join(upload.folder, 'error.log'), traceback_text)
        raise
    DataType.save(join(upload.folder, DataType.get_file_name()), value)
    return DataType.load_for_view_safely(upload.path)


def get_tool_template_variables(tool, tool_definition):
    tool_arguments = get_tool_arguments(tool_definition)
    tool_items = get_data_items(tool_arguments, tool_definition)
    tool.title, tool.template_parts = parse_template_from(
        tool_definition, 'tool', tool_items)
    return {
        'data_types': set(x.data_type for x in tool_items),
        'tool': tool,
    }


def get_tool_arguments(tool_definition):
    value_by_key = OrderedDict()
    for key in tool_definition['argument_names']:
        try:
            value = get_default_value(key, tool_definition)
        except DataTypeError:
            L.warning('could not parse value for %s' % key)
            value = None
        value_by_key[key] = value
    return value_by_key


def get_tool_file_response(request, tool_folder, tool_definition):
    matchdict = request.matchdict
    # Check that the file is in an accessible folder
    try:
        file_path = get_absolute_path(matchdict['path'], tool_folder)
    except BadPath:
        raise HTTPNotFound
    # Check that the file exists
    if not exists(file_path):
        raise HTTPNotFound
    # Check that the file is specified as an argument in the tool definition
    for key in tool_definition['argument_names']:
        default_key = get_default_key(key, tool_definition)
        if default_key and default_key.endswith('_path'):
            if tool_definition[default_key] == file_path:
                break
    else:
        raise HTTPNotFound
    # Return file response
    return FileResponse(file_path, request=request)


def get_data_items(value_by_key, tool_definition):
    data_items = []
    for key, value in value_by_key.items():
        if isinstance(value, DataType):
            continue
        if key.startswith('_') or key in RESERVED_ARGUMENT_NAMES:
            continue
        if value is None:
            value = ''
        if key.endswith('_path'):
            key = key[:-5]
            data_type = get_data_type(key)
            file_location = get_result_file_location(value)
            default_key = get_default_key(key, tool_definition)
            if default_key and tool_definition[default_key] != value:
                default_value = get_default_value(key, tool_definition)
            else:
                default_value = None
            value = data_type.load_for_view_safely(value, default_value)
        else:
            data_type = get_data_type(key)
            file_location = ''
        help_ = tool_definition.get(key + '.help', HELP.get(key, ''))
        data_items.append(DataItem(
            key, value, data_type, file_location, help_))
    return data_items


def get_result_zip_response(request, result):
    data_folder = request.data_folder
    file_path = result.get_target_folder(data_folder) + '.zip'
    if not exists(file_path):
        raise HTTPNotFound
    return FileResponse(file_path, request=request)


def get_result_file_response(request, result):
    matchdict = request.matchdict
    # Check that the file is in an accessible folder
    folder_name = matchdict['folder_name']
    if folder_name not in ('x', 'y'):
        raise HTTPForbidden
    data_folder = request.data_folder
    result_folder = result.get_folder(data_folder)
    file_folder = join(result_folder, folder_name)
    tool = result.tool
    try:
        file_path = get_absolute_path(
            matchdict['path'], file_folder, external_folders=[
                tool.get_folder(data_folder),
            ])
    except BadPath:
        raise HTTPNotFound
    # Check that the file exists
    if not exists(file_path):
        raise HTTPNotFound
    # Return file response
    return FileResponse(file_path, request=request)


def get_result_template_variables(result, result_folder):
    result_configuration = ResultConfiguration(result_folder)
    tool_definition = result_configuration.tool_definition
    result_arguments = result_configuration.result_arguments
    result_properties = result_configuration.result_properties

    tool_items = get_data_items(result_arguments, tool_definition)
    result_items = get_data_items(
        result_properties.pop('raw_outputs', {}), tool_definition)
    result_errors = get_data_items(
        result_properties.pop('type_errors', {}), tool_definition)
    result_properties = get_data_items(result_properties, tool_definition)

    tool = result.tool
    tool.title, tool.template_parts = parse_template_from(
        tool_definition, 'tool', tool_items)
    result.title, result.template_parts = parse_template_from(
        tool_definition, 'result', result_items)
    return {
        'data_types': set(x.data_type for x in tool_items + result_items),
        'tool': tool,
        'result': result,
        'result_errors': result_errors,
        'result_properties': result_properties,
    }


def get_file_url(file_path):
    return get_tool_file_url(file_path) or get_result_file_url(file_path)


def get_tool_file_url(tool_file_path):
    try:
        tool_id, path = TOOL_PATH_PATTERN.search(tool_file_path).groups()
    except AttributeError:
        return
    return '/t/%s/-/%s' % (tool_id, path)


def get_result_file_url(result_file_path):
    try:
        result_id, folder_name, path = RESULT_PATH_PATTERN.search(
            result_file_path).groups()
    except AttributeError:
        return ''
    return '/r/%s/%s/%s' % (result_id, folder_name, path)


def get_result_file_location(result_path):
    try:
        result_id, folder_name, path = RESULT_PATH_PATTERN.search(
            result_path).groups()
    except AttributeError:
        return ''
    return '%s/%s/%s' % (result_id, folder_name, path)


def parse_result_relative_path(result_relative_path):
    result_id, folder_name, path = result_relative_path.split('/', 2)
    if folder_name not in ('x', 'y'):
        raise ValueError
    return result_id, folder_name, path
