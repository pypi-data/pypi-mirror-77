# -*- coding: UTF-8 -*-
# Copyright 2009-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""Views for `lino_openui5.openui5`.
"""

from __future__ import division
from past.utils import old_div

import logging ; logger = logging.getLogger(__name__)

import zlib
import codecs

from django import http
from django.db import models
from django.conf import settings
from django.views.generic import View
from django.core import exceptions
from django.utils.translation import ugettext as _
from django.utils.translation import get_language

# from django.contrib import auth
from lino.core import auth
from lino.utils import isiterable
from lino.utils.jsgen import py2js
from lino.core import fields

from lino.core.gfks import ContentType

# from lino.api import dd
from lino.core import constants
# from lino.core import auth
from lino.core.requests import BaseRequest
from lino.core.tablerequest import TableRequest
import json

from lino.core.views import requested_actor, action_request
from lino.core.views import json_response, json_response_kw

from lino.core.views import action_request
from lino.core.utils import navinfo
from etgen.html import E, tostring
from etgen import html as xghtml
from lino.core import kernel

from lino.api import rt
import re
import cgi

from lino.core.elems import ComboFieldElement

from jinja2.exceptions import TemplateNotFound


def find(itter, target, key=None):
    """Returns the index of an element in a callable which can be use a key function"""
    assert key == None or callable(key), "key shold be a function that takes the itter's item " \
                                         "and returns that wanted matched item"
    for i, x in enumerate(itter):
        if key:
            x = key(x)
        if x == target:
            return i
    else:
        return -1


# Taken from lino.modlib.extjs.views
NOT_FOUND = "%s has no row with primary key %r"


def elem2rec_empty(ar, ah, elem, **rec):
    """
    Returns a dict of this record, designed for usage by an EmptyTable.
    """
    # ~ rec.update(data=rh.store.row2dict(ar,elem))
    rec.update(data=elem._data)
    # ~ rec = elem2rec1(ar,ah,elem)
    # ~ rec.update(title=_("Insert into %s...") % ar.get_title())
    rec.update(title=ar.get_action_title())
    rec.update(id=-99998)
    # ~ rec.update(id=elem.pk) or -99999)
    if ar.actor.parameters:
        rec.update(
            param_values=ar.actor.params_layout.params_store.pv2dict(
                ar, ar.param_values))
    return rec


# class Callbacks(View):
#     def get(self, request, thread_id, button_id):
#         return settings.SITE.kernel.run_callback(request, thread_id, button_id)


class ApiElement(View):
    def get(self, request, app_label=None, actor=None, pk=None):
        ui = settings.SITE.kernel
        rpt = requested_actor(app_label, actor)

        action_name = request.GET.get(constants.URL_PARAM_ACTION_NAME,
                                      rpt.default_elem_action_name)
        ba = rpt.get_url_action(action_name)
        if ba is None:
            raise http.Http404("%s has no action %r" % (rpt, action_name))

        if pk and pk != '-99999' and pk != '-99998':
            # ~ ar = ba.request(request=request,selected_pks=[pk])
            # ~ print 20131004, ba.actor
            # Use url selected rows as selected PKs if defined, otherwise use the PK defined in the url path
            sr = request.GET.getlist(constants.URL_PARAM_SELECTED)
            if not sr:
                sr = [pk]
            ar = ba.request(request=request, selected_pks=sr)
            elem = ar.selected_rows[0]
        else:
            ar = ba.request(request=request)
            elem = None

        ar.renderer = ui.default_renderer
        ah = ar.ah

        fmt = request.GET.get(
            constants.URL_PARAM_FORMAT, ba.action.default_format)

        if ba.action.opens_a_window:

            if fmt == constants.URL_FORMAT_JSON:
                if pk == '-99999':
                    elem = ar.create_instance()
                    datarec = ar.elem2rec_insert(ah, elem)
                elif pk == '-99998':
                    elem = ar.create_instance()
                    datarec = elem2rec_empty(ar, ah, elem)
                elif elem is None:
                    datarec = dict(
                        success=False, message=NOT_FOUND % (rpt, pk))
                else:
                    datarec = ar.elem2rec_detailed(elem)
                return json_response(datarec)

            after_show = ar.get_status(record_id=pk)
            tab = request.GET.get(constants.URL_PARAM_TAB, None)
            if tab is not None:
                tab = int(tab)
                after_show.update(active_tab=tab)

            return http.HttpResponse(
                ui.extjs_renderer.html_page(
                    request, ba.action.label,
                    on_ready=ui.extjs_renderer.action_call(
                        request, ba, after_show)))

        # if isinstance(ba.action, actions.RedirectAction):
        #     target = ba.action.get_target_url(elem)
        #     if target is None:
        #         raise http.Http404("%s failed for %r" % (ba, elem))
        #     return http.HttpResponseRedirect(target)

        if pk == '-99998':
            assert elem is None
            elem = ar.create_instance()
            ar.selected_rows = [elem]
        elif elem is None:
            raise http.Http404(NOT_FOUND % (rpt, pk))
        return settings.SITE.kernel.run_action(ar)

    def post(self, request, app_label=None, actor=None, pk=None):
        ar = action_request(
            app_label, actor, request, request.POST, True,
            renderer=settings.SITE.kernel.extjs_renderer)
        if pk == '-99998':
            elem = ar.create_instance()
            ar.selected_rows = [elem]
        else:
            ar.set_selected_pks(pk)
        return settings.SITE.kernel.run_action(ar)

    def put(self, request, app_label=None, actor=None, pk=None):
        data = http.QueryDict(request.body)  # raw_post_data before Django 1.4
        # logger.info("20150130 %s", data)
        ar = action_request(
            app_label, actor, request, data, False,
            renderer=settings.SITE.kernel.extjs_renderer)
        ar.set_selected_pks(pk)
        return settings.SITE.kernel.run_action(ar)

    def delete(self, request, app_label=None, actor=None, pk=None):
        data = http.QueryDict(request.body)
        ar = action_request(
            app_label, actor, request, data, False,
            renderer=settings.SITE.kernel.extjs_renderer)
        ar.set_selected_pks(pk)
        return settings.SITE.kernel.run_action(ar)

    def old_delete(self, request, app_label=None, actor=None, pk=None):
        rpt = requested_actor(app_label, actor)
        ar = rpt.request(request=request)
        ar.set_selected_pks(pk)
        elem = ar.selected_rows[0]
        return delete_element(ar, elem)


class ApiList(View):
    def post(self, request, app_label=None, actor=None):
        ar = action_request(app_label, actor, request, request.POST, True)
        ar.renderer = settings.SITE.kernel.extjs_renderer
        return settings.SITE.kernel.run_action(ar)

    def get(self, request, app_label=None, actor=None):
        ar = action_request(app_label, actor, request, request.GET, True)
        # Add this hack to support the 'sort' param which is different in Extjs6.
        if ar.order_by and ar.order_by[0]:
            _sort = ast.literal_eval(ar.order_by[0])
            sort = _sort[0]['property']
            if _sort[0]['direction'] and _sort[0]['direction'] == 'DESC':
                sort = '-' + sort
            ar.order_by = [str(sort)]
        ar.renderer = settings.SITE.kernel.default_renderer
        rh = ar.ah

        fmt = request.GET.get(
            constants.URL_PARAM_FORMAT,
            ar.bound_action.action.default_format)

        if fmt == constants.URL_FORMAT_JSON:
            rows = [rh.store.row2list(ar, row)
                    for row in ar.sliced_data_iterator]
            total_count = ar.get_total_count()
            for row in ar.create_phantom_rows():
                if ar.limit is None or len(rows) + 1 < ar.limit or ar.limit == total_count + 1:
                    d = rh.store.row2list(ar, row)
                    rows.append(d)
                total_count += 1
            # assert len(rows) <= ar.limit
            kw = dict(count=total_count,
                      rows=rows,
                      success=True,
                      no_data_text=ar.no_data_text,
                      # title=str(ar.get_title()),
                      title=ar.get_title())
            if ar.actor.parameters:
                kw.update(
                    param_values=ar.actor.params_layout.params_store.pv2dict(
                        ar, ar.param_values))
            return json_response(kw)

        if fmt == constants.URL_FORMAT_HTML:
            after_show = ar.get_status()

            sp = request.GET.get(
                constants.URL_PARAM_SHOW_PARAMS_PANEL, None)
            if sp is not None:
                # ~ after_show.update(show_params_panel=sp)
                after_show.update(
                    show_params_panel=constants.parse_boolean(sp))

            # if isinstance(ar.bound_action.action, actions.ShowInsert):
            #     elem = ar.create_instance()
            #     rec = ar.elem2rec_insert(rh, elem)
            #     after_show.update(data_record=rec)

            kw = dict(on_ready=
            ar.renderer.action_call(
                ar.request,
                ar.bound_action, after_show))
            # ~ print '20110714 on_ready', params
            kw.update(title=ar.get_title())
            return http.HttpResponse(ar.renderer.html_page(request, **kw))

        if fmt == 'csv':
            # ~ response = HttpResponse(mimetype='text/csv')
            charset = settings.SITE.csv_params.get('encoding', 'utf-8')
            response = http.HttpResponse(
                content_type='text/csv;charset="%s"' % charset)
            if False:
                response['Content-Disposition'] = \
                    'attachment; filename="%s.csv"' % ar.actor
            else:
                # ~ response = HttpResponse(content_type='application/csv')
                response['Content-Disposition'] = \
                    'inline; filename="%s.csv"' % ar.actor

            # ~ response['Content-Disposition'] = 'attachment; filename=%s.csv' % ar.get_base_filename()
            w = ucsv.UnicodeWriter(response, **settings.SITE.csv_params)
            w.writerow(ar.ah.store.column_names())
            if True:  # 20130418 : also column headers, not only internal names
                column_names = None
                fields, headers, cellwidths = ar.get_field_info(column_names)
                w.writerow(headers)

            for row in ar.data_iterator:
                w.writerow([str(v) for v in rh.store.row2list(ar, row)])
            return response

        if fmt == constants.URL_FORMAT_PRINTER:
            if ar.get_total_count() > MAX_ROW_COUNT:
                raise Exception(_("List contains more than %d rows") %
                                MAX_ROW_COUNT)
            response = http.HttpResponse(
                content_type='text/html;charset="utf-8"')
            doc = xghtml.Document(force_text(ar.get_title()))
            doc.body.append(E.h1(doc.title))
            t = doc.add_table()
            # ~ settings.SITE.kernel.ar2html(ar,t,ar.data_iterator)
            ar.dump2html(t, ar.data_iterator, header_links=False)
            doc.write(response, encoding='utf-8')
            return response

        return settings.SITE.kernel.run_action(ar)


# Should we Refactor into lino.modlib.extjs.choicees_views.py and import?
#
# choices_for_field is copied line-for-line from lino.modlib.extjs.views.choices_for_field
def choices_for_field(ar, holder, field):
    """
    Return the choices for the given field and the given HTTP request
    whose `holder` is either a Model, an Actor or an Action.
    """
    if not holder.get_view_permission(ar.request.user.user_type):
        raise Exception(
            "{user} has no permission for {holder}".format(
                user=ar.request.user, holder=holder))
    # model = holder.get_chooser_model()
    chooser = holder.get_chooser_for_field(field.name)
    # logger.info('20140822 choices_for_field(%s.%s) --> %s',
    #             holder, field.name, chooser)
    if chooser:
        qs = chooser.get_request_choices(ar, holder)
        if not isiterable(qs):
            raise Exception("%s.%s_choices() returned non-iterable %r" % (
                holder.model, field.name, qs))
        if chooser.simple_values:
            def row2dict(obj, d):
                d[constants.CHOICES_TEXT_FIELD] = str(obj)
                d[constants.CHOICES_VALUE_FIELD] = obj
                return d
        elif chooser.instance_values:
            # same code as for ForeignKey
            def row2dict(obj, d):
                d[constants.CHOICES_TEXT_FIELD] = holder.get_choices_text(
                    obj, ar.request, field)
                d[constants.CHOICES_VALUE_FIELD] = obj.pk
                return d
        else:  # values are (value, text) tuples
            def row2dict(obj, d):
                d[constants.CHOICES_TEXT_FIELD] = str(obj[1])
                d[constants.CHOICES_VALUE_FIELD] = obj[0]
                return d
        return (qs, row2dict)

    if field.choices:
        qs = field.choices

        def row2dict(obj, d):
            if type(obj) is list or type(obj) is tuple:
                d[constants.CHOICES_TEXT_FIELD] = str(obj[1])
                d[constants.CHOICES_VALUE_FIELD] = obj[0]
            else:
                d[constants.CHOICES_TEXT_FIELD] = holder.get_choices_text(
                    obj, ar.request, field)
                d[constants.CHOICES_VALUE_FIELD] = str(obj)
            return d

        return (qs, row2dict)

    if isinstance(field, fields.VirtualField):
        field = field.return_type

    if isinstance(field, fields.RemoteField):
        field = field.field

    if isinstance(field, models.ForeignKey):
        m = field.remote_field.model
        t = m.get_default_table()
        qs = t.request(request=ar.request).data_iterator

        # logger.info('20120710 choices_view(FK) %s --> %s', t, qs.query)

        def row2dict(obj, d):
            d[constants.CHOICES_TEXT_FIELD] = holder.get_choices_text(
                obj, ar.request, field)
            d[constants.CHOICES_VALUE_FIELD] = obj.pk
            return d
    else:
        raise http.Http404("No choices for %s" % field)
    return (qs, row2dict)


# choices_response is copied line-for-line from lino.modlib.extjs.views.choices_response
def choices_response(actor, request, qs, row2dict, emptyValue):
    """
    :param actor: requesting Actor
    :param request: web request
    :param qs: list of django model QS,
    :param row2dict: function for converting data set into a dict for json
    :param emptyValue: The Text value to represent None in the choice-list
    :return: json web responce

    Filters data-set acording to quickseach
    Counts total rows in the set,
    Calculates offset and limit
    Adds None value
    returns
    """
    quick_search = request.GET.get(constants.URL_PARAM_FILTER, None)
    offset = request.GET.get(constants.URL_PARAM_START, None)
    limit = request.GET.get(constants.URL_PARAM_LIMIT, None)
    if isinstance(qs, models.QuerySet):
        qs = qs.filter(qs.model.quick_search_filter(quick_search)) if quick_search else qs
        count = qs.count()

        if offset:
            qs = qs[int(offset):]
            # ~ kw.update(offset=int(offset))

        if limit:
            # ~ kw.update(limit=int(limit))
            qs = qs[:int(limit)]

        rows = [row2dict(row, {}) for row in qs]

    else:
        rows = [row2dict(row, {}) for row in qs]
        if quick_search:
            txt = quick_search.lower()

            rows = [row for row in rows
                    if txt in row[constants.CHOICES_TEXT_FIELD].lower()]
        count = len(rows)
        rows = rows[int(offset):] if offset else rows
        rows = rows[:int(limit)] if limit else rows

    # Add None choice
    if emptyValue is not None and not quick_search:
        empty = dict()
        empty[constants.CHOICES_TEXT_FIELD] = emptyValue
        empty[constants.CHOICES_VALUE_FIELD] = None
        rows.insert(0, empty)

    return json_response_kw(count=count, rows=rows)
    # ~ return json_response_kw(count=len(rows),rows=rows)
    # ~ return json_response_kw(count=len(rows),rows=rows,title=_('Choices for %s') % fldname)


class ChoiceListModel(View):
    """
    Creates a large JSON model that contains all the choicelists + choices

    Note: This could be improved, or might cause issues due to changing language
    """

    def get(self, request):
        data = {str(cl): [{"key": py2js(c[0]).strip('"'), "text": py2js(c[1]).strip('"')} for c in cl.get_choices()] for
                cl in
                kernel.CHOICELISTS.values()}
        return json_response(data)


# Copied from lino.modlib.extjs.views.Choices line for line.
class Choices(View):
    def get(self, request, app_label=None, rptname=None, fldname=None, **kw):
        """If `fldname` is specified, return a JSON object with two
        attributes `count` and `rows`, where `rows` is a list of
        `(display_text, value)` tuples.  Used by ComboBoxes or similar
        widgets.

        If `fldname` is not specified, returns the choices for the
        `record_selector` widget.

        """
        rpt = requested_actor(app_label, rptname)
        emptyValue = None
        if fldname is None:
            ar = rpt.request(request=request)
            # ~ rh = rpt.get_handle(self)
            # ~ ar = ViewReportRequest(request,rh,rpt.default_action)
            # ~ ar = dbtables.TableRequest(self,rpt,request,rpt.default_action)
            # ~ rh = ar.ah
            # ~ qs = ar.get_data_iterator()
            qs = ar.data_iterator

            # ~ qs = rpt.request(self).get_queryset()

            def row2dict(obj, d):
                d[constants.CHOICES_TEXT_FIELD] = str(obj)
                # getattr(obj,'pk')
                d[constants.CHOICES_VALUE_FIELD] = obj.pk
                return d
        else:
            # NOTE: if you define a *parameter* with the same name as
            # some existing *data element* name, then the parameter
            # will override the data element here in choices view.
            field = rpt.get_param_elem(fldname)
            if field is None:
                field = rpt.get_data_elem(fldname)
            if field.blank:
                # logger.info("views.Choices: %r is blank",field)
                emptyValue = ''
            qs, row2dict = choices_for_field(rpt.request(request=request), rpt, field)

        return choices_response(rpt, request, qs, row2dict, emptyValue)


# Also coppied from extjs.views line for line
class ActionParamChoices(View):
    # Examples: `welfare.pcsw.CreateCoachingVisit`
    def get(self, request, app_label=None, actor=None, an=None, field=None, **kw):
        actor = requested_actor(app_label, actor)
        ba = actor.get_url_action(an)
        if ba is None:
            raise Exception("Unknown action %r for %s" % (an, actor))
        field = ba.action.get_param_elem(field)
        qs, row2dict = choices_for_field(ba.request(request=request), ba.action, field)
        if field.blank:
            emptyValue = '<br/>'
        else:
            emptyValue = None
        return choices_response(actor, request, qs, row2dict, emptyValue)


class Restful(View):
    """
    Used to collaborate with a restful Ext.data.Store.
    """

    def post(self, request, app_label=None, actor=None, pk=None):
        rpt = requested_actor(app_label, actor)
        ar = rpt.request(request=request)

        instance = ar.create_instance()
        # store uploaded files.
        # html forms cannot send files with PUT or GET, only with POST
        if ar.actor.handle_uploaded_files is not None:
            ar.actor.handle_uploaded_files(instance, request)

        data = request.POST.get('rows')
        data = json.loads(data)
        ar.form2obj_and_save(data, instance, True)

        # Ext.ensible needs list_fields, not detail_fields
        ar.set_response(
            rows=[ar.ah.store.row2dict(
                ar, instance, ar.ah.store.list_fields)])
        return json_response(ar.response)

    # def delete(self, request, app_label=None, actor=None, pk=None):
    #     rpt = requested_actor(app_label, actor)
    #     ar = rpt.request(request=request)
    #     ar.set_selected_pks(pk)
    #     return delete_element(ar, ar.selected_rows[0])

    def get(self, request, app_label=None, actor=None, pk=None):
        """
        Works, but is ugly to get list and detail
        """
        rpt = requested_actor(app_label, actor)

        action_name = request.GET.get(constants.URL_PARAM_ACTION_NAME,
                                      rpt.default_elem_action_name)
        fmt = request.GET.get(
            constants.URL_PARAM_FORMAT, constants.URL_FORMAT_JSON)
        sr = request.GET.getlist(constants.URL_PARAM_SELECTED)
        if not sr:
            sr = [pk]
        ar = rpt.request(request=request, selected_pks=sr)
        if pk is None:
            rh = ar.ah
            rows = [
                rh.store.row2dict(ar, row, rh.store.all_fields)
                for row in ar.sliced_data_iterator]
            kw = dict(count=ar.get_total_count(), rows=rows)
            kw.update(title=str(ar.get_title()))
            return json_response(kw)

        else:  # action_name=="detail": #ba.action.opens_a_window:

            ba = rpt.get_url_action(action_name)
            ah = ar.ah
            ar = ba.request(request=request, selected_pks=sr)
            elem = ar.selected_rows[0]
            if fmt == constants.URL_FORMAT_JSON:
                if pk == '-99999':
                    elem = ar.create_instance()
                    datarec = ar.elem2rec_insert(ah, elem)
                elif pk == '-99998':
                    elem = ar.create_instance()
                    datarec = elem2rec_empty(ar, ah, elem)
                elif elem is None:
                    datarec = dict(
                        success=False, message=NOT_FOUND % (rpt, pk))
                else:
                    datarec = ar.elem2rec_detailed(elem)
                return json_response(datarec)

    def put(self, request, app_label=None, actor=None, pk=None):
        rpt = requested_actor(app_label, actor)
        ar = rpt.request(request=request)
        ar.set_selected_pks(pk)
        elem = ar.selected_rows[0]
        rh = ar.ah

        data = http.QueryDict(request.body).get('rows')
        data = json.loads(data)
        a = rpt.get_url_action(rpt.default_list_action_name)
        ar = rpt.request(request=request, action=a)
        ar.renderer = settings.SITE.kernel.extjs_renderer
        ar.form2obj_and_save(data, elem, False)
        # Ext.ensible needs list_fields, not detail_fields
        ar.set_response(
            rows=[rh.store.row2dict(ar, elem, rh.store.list_fields)])
        return json_response(ar.response)


def http_response(ar, tplname, context):
    "Deserves a docstring"
    u = ar.get_user()
    lang = get_language()
    k = (u.user_type, lang)
    context = ar.get_printable_context(**context)
    context['ar'] = ar
    context['memo'] = ar.parse_memo  # MEMO_PARSER.parse
    env = settings.SITE.plugins.jinja.renderer.jinja_env
    template = env.get_template(tplname)

    response = http.HttpResponse(
        template.render(**context),
        content_type='text/html;charset="utf-8"')

    return response


# Give better name, does more then just XML, does all the connector responses.
def XML_response(ar, tplname, context):
    """
    Respone used for rendering XML views in openui5.
    Includes some helper functions for rendering.
    """
    # u = ar.get_user()
    # lang = get_language()
    # k = (u.user_type, lang)
    context = ar.get_printable_context(**context)
    context.update(constants=constants)
    # context['ar'] = ar
    # context['memo'] = ar.parse_memo  # MEMO_PARSER.parse
    env = settings.SITE.plugins.jinja.renderer.jinja_env
    try:
        template = env.get_template(tplname)
    except TemplateNotFound as e:
        return http.HttpResponseNotFound()

    def bind(*args):
        """Helper function to wrap a string in {}s"""
        args = [str(a) for a in args]
        return "{" + "".join(args) + "}"

    context.update(bind=bind)

    def p(*args):
        """Debugger helper; prints out all args put into the filter but doesn't include them in the template.
        usage: {{debug | p}}
        """
        print(args)
        return ""

    def zlib_compress(s):
        """
        Compress a complex value in order to get decompress by the controller afterwards
        :param s: value to get compressed.
        :return: Compressed value.
        """
        compressed = zlib.compress(str(s).encode('utf-8'))
        # return compressed
        return codecs.encode(compressed, 'base64')
        # return cgi.escape(s, quote=True)  # escapes "<", ">", "&" "'" and '"'

    def fields_search(searched_field, collections):
        """
        check if the fields is available in the set of collections
        :param searched_field: searched field
        :param collections: set of fields
        :return: True if the field is present in the collections,False otherwise.
        """
        if searched_field:
            for field in collections:
                if searched_field == field:
                    return True
        return False

    env.filters.update(dict(p=p, zlib_compress=zlib_compress, fields_search=fields_search))
    content_type = "text/xml" if tplname.endswith(".xml") else \
        "application/javascript" if tplname.endswith(".js") else \
            "application/json"
    response = http.HttpResponse(
        template.render(**context),
        content_type=content_type + ';charset="utf-8"')

    return response


def layout2html(ar, elem):
    wl = ar.bound_action.get_window_layout()
    # ~ print 20120901, wl.main
    lh = wl.get_layout_handle(settings.SITE.kernel.default_ui)

    items = list(lh.main.as_plain_html(ar, elem))
    # if navigator:
    #     items.insert(0, navigator)
    # ~ print tostring(E.div())
    # ~ if len(items) == 0: return ""
    return E.form(*items)


class MainHtml(View):
    def get(self, request, *args, **kw):
        """Returns a json struct for the main user dashboard."""
        # ~ logger.info("20130719 MainHtml")
        settings.SITE.startup()
        # ~ raise Exception("20131023")
        ar = BaseRequest(request)
        html = settings.SITE.get_main_html(
            request, extjs=settings.SITE.plugins.openui5)
        html = settings.SITE.plugins.openui5.renderer.html_text(html)
        ar.success(html=html)
        return json_response(ar.response, ar.content_type)


class Connector(View):
    """
    Static View for Tickets,
    Uses a template for generating the XML views  rather then layouts
    """

    def get(self, request, name=None):
        # ar = action_request(None, None, request, request.GET, True)
        ar = BaseRequest(
            # user=user,
            request=request,
            renderer=settings.SITE.plugins.openui5.renderer)
        u = ar.get_user()

        context = dict(
            menu=settings.SITE.get_site_menu(u.user_type)
        )

        device_type = request.device_type
        # print ("device_type", device_type)
        # print(u)
        # print(name)
        if name.startswith("dialog/SignInActionFormPanel"):
            tplname = "openui5/fragment/SignInActionFormPanel.fragment.xml"

        elif name.startswith("menu/user/user.fragment.xml"):
            tplname = "openui5/fragment/UserMenu.fragment.xml"

        elif name.startswith("menu/"):
            tplname = "openui5/fragment/Menu.fragment.xml"
            sel_menu = name.split("/", 1)[1].split('.', 1)[0]
            # [05/Feb/2018 09:32:25] "GET /ui/menu/mailbox.fragment.xml HTTP/1.1" 200 325
            for i in context['menu'].items:
                if i.name == sel_menu:
                    context.update(dict(
                        opened_menu=i
                    ))
                    break
            else:
                raise Exception("No Menu with name %s" % sel_menu)
        elif name.startswith("grid/") or name.startswith("slavetable/") or \
                name.startswith("view/grid/") or name.startswith("view/slavetable/"):  # Table/grid view
            # todo Get table data
            # "grid/tickets/AllTickets.view.xml"
            # or
            # "slavetable/tickets/AllTickets.view.xml
            app_label, actor = re.match(r"(?:(?:view\/)?grid|slavetable)\/(.+)\/(.+).view.xml$", name).groups()
            ar = action_request(app_label, actor, request, request.GET, True)
            actor = rt.models.resolve(app_label + "." + actor)
            store = ar.ah.store
            columns = actor.get_handle().get_columns()
            store.list_fields
            # todo match columns's field.name with store.list_fields storefield's index.
            index_mod = 0
            for c in columns:
                c.fields_index = find(store.list_fields, c.field.name,
                                      key=lambda f: f.name) + index_mod
                if isinstance(c, ComboFieldElement):
                    # Skip the data value for multi value columns, such as choices and FK fields.
                    # use c.fields_index -1 for data value
                    index_mod += 1
            # print(ar.ah.store.pk_index) # indexk of PK in detail row data

            if settings.SITE.is_installed('contenttypes'):
                # Used in slave tables of gfks relations
                m = getattr(store.pk, 'model', None)
                # e.g. pk may be the VALUE_FIELD of a choicelist which
                # has no model
                if m is not None:
                    ct = ContentType.objects.get_for_model(m).pk
                    context.update(content_type=ct)

            ba_actions = ar.actor.get_toolbar_actions(ar.bound_action.action)
            context.update({
                'ba_actions': ba_actions,
                "actor": actor,
                "columns": columns,
                "actions": actor.get_actions(),
                "title": actor.label,
                "pk_index": store.pk_index,
                "is_slave": name.startswith("slavetable/") or actor.master is not None,
            })
            if name.startswith("slavetable/"):
                tplname = "openui5/view/slaveTable.view.xml"
            else:
                # if device_type == 'desktop':
                if not actor.tablet_columns and not actor.mobile_columns:
                    tplname = "openui5/view/table.view.xml"  # Change to "grid" to match action?
                else:
                    tplname = "openui5/view/table.mview.xml"

                    # ar = action_request(app_label, actor, request, request.GET, True)
                    # add to context

        elif name.startswith("detail") or name.startswith("view/detail"):  # Detail view
            # "detail/tickets/AllTickets.view.xml"
            app_label, actor = re.match(r"(?:view\/)?detail\/(.+)\/(.+).view.xml$", name).groups()
            actor = rt.models.resolve(app_label + "." + actor)
            # detail_action = actor.actions['detail']
            detail_action = actor.detail_action
            window_layout = detail_action.get_window_layout()
            layout_handle = window_layout.get_layout_handle(settings.SITE.plugins.openui5)
            layout_handle.main.elements  # elems # Refactor into actor get method?
            ba_actions = actor.get_toolbar_actions(actor.detail_action.action)

            if settings.SITE.is_installed('contenttypes'):
                # Used to open slave tables from detail views
                m = getattr(actor, 'model', None)
                # e.g. pk may be the VALUE_FIELD of a choicelist which
                # has no model
                if m is not None:
                    ct = ContentType.objects.get_for_model(m).pk
                    context.update(content_type=ct)

            context.update({
                "actor": actor,
                # "columns": actor.get_handle().get_columns(),
                "actions": actor.get_actions(),
                'ba_actions': ba_actions,
                "title": actor.label,  #
                # "main_elems": layout_handle.main.elements,
                "main": layout_handle.main,
                "layout_handle": layout_handle,
                "save_fields": ' '.join([f.name for f in actor.model._meta.fields if f.editable]),

            })
            tplname = "openui5/view/detail.view.xml"  # Change to "grid" to match action?
            # ar = action_request(app_label, actor, request, request.GET, True)
            # add to context

        elif name.startswith("action/"):
            # Param actions
            actor_id, action_name = re.match(r"(?:action\/)?(.+)\/(.+).fragment.xml$", name).groups()
            actor = rt.models.resolve(actor_id.replace("/", "."))
            action = actor.actions[action_name]
            window_layout = action.get_window_layout()
            layout_handle = window_layout.get_layout_handle(settings.SITE.plugins.openui5)
            context.update({
                "actor": actor,
                "action": action,
                "title": actor.label,
                "main": layout_handle.main,
                "layout_handle": layout_handle,
                "save_fields": " ".join([f.name for f in layout_handle._store_fields]),
                "e": layout_handle.main,  # set e for the initial main element
                "is_insert_action": True if action.action.params_layout is None else False
            })
            tplname = "openui5/fragment/ActionFormPanel.fragment.xml"


        elif (name.startswith("view/") or
              name.startswith("controller/") or
              name.startswith("core/") or
              name.startswith("fragment/")):
            tplname = "openui5/" + name

            if "manifest.json" in name:
                ## List all master tables for routing
                actors_list = [
                    rpt for rpt in kernel.master_tables
                                   + kernel.slave_tables
                                   + list(kernel.generic_slaves.values())
                                   + kernel.virtual_tables
                                   + kernel.frames_list
                ]
                detail_list = set()

                def add(res, collector, fl, formpanel_name):
                    if fl is None or fl._datasource is None:
                        return  # 20130804
                    if fl._datasource != res:
                        fl._other_datasources.add(res)
                    if fl not in collector:
                        collector.add(res)

                for res in actors_list:
                    add(res, detail_list, res.detail_layout, "detail.%s" % res)

                    # self.actors_list.extend(
                #     [a for a in list(kernel.CHOICELISTS.values())
                #      if settings.SITE.is_installed(a.app_label)])

                # don't include for abstract actors
                actors_list = [a for a in actors_list
                               if not a.is_abstract()]
                # Choicelists
                choicelists_list = kernel.CHOICELISTS.values()

                context.update(actors_list=actors_list,
                               detail_list=detail_list,
                               choicelists_list=choicelists_list
                               )



        else:
            raise Exception("Can't find a view for path: {}".format(name))

        return XML_response(ar, tplname, context)


class Authenticate(View):
    def get(self, request, *args, **kw):
        action_name = request.GET.get(constants.URL_PARAM_ACTION_NAME)
        if action_name == 'logout':
            username = request.session.pop('username', None)
            auth.logout(request)
            # request.user = settings.SITE.user_model.get_anonymous_user()
            # request.session.pop('password', None)
            # ~ username = request.session['username']
            # ~ del request.session['password']
            target = '/'
            return http.HttpResponseRedirect(target)

            # ar = BaseRequest(request)
            # ar.success("User %r logged out." % username)
            # return ar.renderer.render_action_response(ar)
        raise http.Http404()

    def post(self, request, *args, **kw):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(
            request, username=username, password=password)
        auth.login(request, user, backend=u'lino.core.auth.backends.ModelBackend')
        target = '/'
        return http.HttpResponseRedirect(target)
        # ar = BaseRequest(request)
        # mw = auth.get_auth_middleware()
        # msg = mw.authenticate(username, password, request)
        # if msg:
        #     request.session.pop('username', None)
        #     ar.error(msg)
        # else:
        #     request.session['username'] = username
        #     # request.session['password'] = password
        #     # ar.user = request....
        #     ar.success(("Now logged in as %r" % username))
        #     # print "20150428 Now logged in as %r (%s)" % (username, user)
        # return ar.renderer.render_action_response(ar)


class App(View):
    """
    Main app entry point,
    """

    def get(self, request):
        ui = settings.SITE.plugins.openui5
        ar = BaseRequest(
            # user=user,
            request=request,
            renderer=ui.renderer)
        context = dict(
            # title=ar.get_title(),
            # heading=ar.get_title(),
            # main=main,
        )
        context.update(ar=ar)

        context = ar.get_printable_context(**context)
        env = settings.SITE.plugins.jinja.renderer.jinja_env
        template = env.get_template("openui5/main.html")
        return http.HttpResponse(
            template.render(**context),
            content_type='text/html;charset="utf-8"')

# class Index(View):
#     """
#     Render the main dashboard.
#     """

#     def get(self, request, *args, **kw):
#         # raise Exception("20171122 {} {}".format(
#         #     get_language(), settings.MIDDLEWARE_CLASSES))
#         ui = settings.SITE.plugins.openui5
#         # print("20170607", request.user)
#         # assert ui.renderer is not None
#         ar = BaseRequest(
#             # user=user,
#             request=request,
#             renderer=ui.renderer)
#         return index_response(ar)


# def index_response(ar):
#     ui = settings.SITE.plugins.openui5

#     main = settings.SITE.get_main_html(ar.request, extjs=ui)
#     main = ui.renderer.html_text(main)
#     context = dict(
#         title=settings.SITE.title,
#         main=main,
#     )
#     # if settings.SITE.user_model is None:
#     #     user = auth.AnonymousUser.instance()
#     # else:
#     #     user = request.subst_user or request.user
#     # context.update(ar=ar)
#     return http_response(ar, 'bootstrap3/index.html', context)
