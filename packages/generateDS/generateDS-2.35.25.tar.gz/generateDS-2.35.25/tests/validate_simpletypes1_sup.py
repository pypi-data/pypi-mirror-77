#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Generated  by generateDS.py.
# Python 3.7.7 (default, Mar 26 2020, 15:48:22)  [GCC 7.3.0]
#
# Command line options:
#   ('--no-dates', '')
#   ('--no-versions', '')
#   ('--member-specs', 'list')
#   ('-f', '')
#   ('-o', 'tests/validate_simpletypes2_sup.py')
#   ('-s', 'tests/validate_simpletypes2_sub.py')
#   ('--super', 'validate_simpletypes2_sup')
#   ('--external-encoding', 'utf-8')
#   ('--export', 'write validate')
#
# Command line arguments:
#   tests/validate_simpletypes.xsd
#
# Command line:
#   generateDS.py --no-dates --no-versions --member-specs="list" -f -o "tests/validate_simpletypes2_sup.py" -s "tests/validate_simpletypes2_sub.py" --super="validate_simpletypes2_sup" --external-encoding="utf-8" --export="write validate" tests/validate_simpletypes.xsd
#
# Current working directory (os.getcwd()):
#   generateds
#

from six.moves import zip_longest
import os
import sys
import re as re_
import base64
import datetime as datetime_
import decimal as decimal_
try:
    from lxml import etree as etree_
except ImportError:
    from xml.etree import ElementTree as etree_


Validate_simpletypes_ = True
SaveElementTreeNode = True
if sys.version_info.major == 2:
    BaseStrType_ = basestring
else:
    BaseStrType_ = str


def parsexml_(infile, parser=None, **kwargs):
    if parser is None:
        # Use the lxml ElementTree compatible parser so that, e.g.,
        #   we ignore comments.
        try:
            parser = etree_.ETCompatXMLParser()
        except AttributeError:
            # fallback to xml.etree
            parser = etree_.XMLParser()
    try:
        if isinstance(infile, os.PathLike):
            infile = os.path.join(infile)
    except AttributeError:
        pass
    doc = etree_.parse(infile, parser=parser, **kwargs)
    return doc

def parsexmlstring_(instring, parser=None, **kwargs):
    if parser is None:
        # Use the lxml ElementTree compatible parser so that, e.g.,
        #   we ignore comments.
        try:
            parser = etree_.ETCompatXMLParser()
        except AttributeError:
            # fallback to xml.etree
            parser = etree_.XMLParser()
    element = etree_.fromstring(instring, parser=parser, **kwargs)
    return element

#
# Namespace prefix definition table (and other attributes, too)
#
# The module generatedsnamespaces, if it is importable, must contain
# a dictionary named GeneratedsNamespaceDefs.  This Python dictionary
# should map element type names (strings) to XML schema namespace prefix
# definitions.  The export method for any class for which there is
# a namespace prefix definition, will export that definition in the
# XML representation of that element.  See the export method of
# any generated element type class for an example of the use of this
# table.
# A sample table is:
#
#     # File: generatedsnamespaces.py
#
#     GenerateDSNamespaceDefs = {
#         "ElementtypeA": "http://www.xxx.com/namespaceA",
#         "ElementtypeB": "http://www.xxx.com/namespaceB",
#     }
#
# Additionally, the generatedsnamespaces module can contain a python
# dictionary named GenerateDSNamespaceTypePrefixes that associates element
# types with the namespace prefixes that are to be added to the
# "xsi:type" attribute value.  See the exportAttributes method of
# any generated element type and the generation of "xsi:type" for an
# example of the use of this table.
# An example table:
#
#     # File: generatedsnamespaces.py
#
#     GenerateDSNamespaceTypePrefixes = {
#         "ElementtypeC": "aaa:",
#         "ElementtypeD": "bbb:",
#     }
#

try:
    from generatedsnamespaces import GenerateDSNamespaceDefs as GenerateDSNamespaceDefs_
except ImportError:
    GenerateDSNamespaceDefs_ = {}
try:
    from generatedsnamespaces import GenerateDSNamespaceTypePrefixes as GenerateDSNamespaceTypePrefixes_
except ImportError:
    GenerateDSNamespaceTypePrefixes_ = {}

#
# You can replace the following class definition by defining an
# importable module named "generatedscollector" containing a class
# named "GdsCollector".  See the default class definition below for
# clues about the possible content of that class.
#
try:
    from generatedscollector import GdsCollector as GdsCollector_
except ImportError:

    class GdsCollector_(object):

        def __init__(self, messages=None):
            if messages is None:
                self.messages = []
            else:
                self.messages = messages

        def add_message(self, msg):
            self.messages.append(msg)

        def get_messages(self):
            return self.messages

        def clear_messages(self):
            self.messages = []

        def print_messages(self):
            for msg in self.messages:
                print("Warning: {}".format(msg))

        def write_messages(self, outstream):
            for msg in self.messages:
                outstream.write("Warning: {}\n".format(msg))


#
# The super-class for enum types
#

try:
    from enum import Enum
except ImportError:
    Enum = object

#
# The root super-class for element type classes
#
# Calls to the methods in these classes are generated by generateDS.py.
# You can replace these methods by re-implementing the following class
#   in a module named generatedssuper.py.

try:
    from generatedssuper import GeneratedsSuper
except ImportError as exp:
    
    class GeneratedsSuper(object):
        __hash__ = object.__hash__
        tzoff_pattern = re_.compile(r'(\+|-)((0\d|1[0-3]):[0-5]\d|14:00)$')
        class _FixedOffsetTZ(datetime_.tzinfo):
            def __init__(self, offset, name):
                self.__offset = datetime_.timedelta(minutes=offset)
                self.__name = name
            def utcoffset(self, dt):
                return self.__offset
            def tzname(self, dt):
                return self.__name
            def dst(self, dt):
                return None
        def gds_format_string(self, input_data, input_name=''):
            return input_data
        def gds_parse_string(self, input_data, node=None, input_name=''):
            return input_data
        def gds_validate_string(self, input_data, node=None, input_name=''):
            if not input_data:
                return ''
            else:
                return input_data
        def gds_format_base64(self, input_data, input_name=''):
            return base64.b64encode(input_data)
        def gds_validate_base64(self, input_data, node=None, input_name=''):
            return input_data
        def gds_format_integer(self, input_data, input_name=''):
            return '%d' % input_data
        def gds_parse_integer(self, input_data, node=None, input_name=''):
            try:
                ival = int(input_data)
            except (TypeError, ValueError) as exp:
                raise_parse_error(node, 'Requires integer value: %s' % exp)
            return ival
        def gds_validate_integer(self, input_data, node=None, input_name=''):
            try:
                value = int(input_data)
            except (TypeError, ValueError):
                raise_parse_error(node, 'Requires integer value')
            return value
        def gds_format_integer_list(self, input_data, input_name=''):
            return '%s' % ' '.join(input_data)
        def gds_validate_integer_list(
                self, input_data, node=None, input_name=''):
            values = input_data.split()
            for value in values:
                try:
                    int(value)
                except (TypeError, ValueError):
                    raise_parse_error(node, 'Requires sequence of integer valuess')
            return values
        def gds_format_float(self, input_data, input_name=''):
            return ('%.15f' % input_data).rstrip('0')
        def gds_parse_float(self, input_data, node=None, input_name=''):
            try:
                fval_ = float(input_data)
            except (TypeError, ValueError) as exp:
                raise_parse_error(node, 'Requires float or double value: %s' % exp)
            return fval_
        def gds_validate_float(self, input_data, node=None, input_name=''):
            try:
                value = float(input_data)
            except (TypeError, ValueError):
                raise_parse_error(node, 'Requires float value')
            return value
        def gds_format_float_list(self, input_data, input_name=''):
            return '%s' % ' '.join(input_data)
        def gds_validate_float_list(
                self, input_data, node=None, input_name=''):
            values = input_data.split()
            for value in values:
                try:
                    float(value)
                except (TypeError, ValueError):
                    raise_parse_error(node, 'Requires sequence of float values')
            return values
        def gds_format_decimal(self, input_data, input_name=''):
            return_value = '%s' % input_data
            if '.' in return_value:
                return_value = return_value.rstrip('0')
                if return_value.endswith('.'):
                    return_value = return_value.rstrip('.')
            return return_value
        def gds_parse_decimal(self, input_data, node=None, input_name=''):
            try:
                decimal_value = decimal_.Decimal(input_data)
            except (TypeError, ValueError):
                raise_parse_error(node, 'Requires decimal value')
            return decimal_value
        def gds_validate_decimal(self, input_data, node=None, input_name=''):
            try:
                value = decimal_.Decimal(input_data)
            except (TypeError, ValueError):
                raise_parse_error(node, 'Requires decimal value')
            return value
        def gds_format_decimal_list(self, input_data, input_name=''):
            return ' '.join([self.gds_format_decimal(item) for item in input_data])
        def gds_validate_decimal_list(
                self, input_data, node=None, input_name=''):
            values = input_data.split()
            for value in values:
                try:
                    decimal_.Decimal(value)
                except (TypeError, ValueError):
                    raise_parse_error(node, 'Requires sequence of decimal values')
            return values
        def gds_format_double(self, input_data, input_name=''):
            return '%e' % input_data
        def gds_parse_double(self, input_data, node=None, input_name=''):
            try:
                fval_ = float(input_data)
            except (TypeError, ValueError) as exp:
                raise_parse_error(node, 'Requires double or float value: %s' % exp)
            return fval_
        def gds_validate_double(self, input_data, node=None, input_name=''):
            try:
                value = float(input_data)
            except (TypeError, ValueError):
                raise_parse_error(node, 'Requires double or float value')
            return value
        def gds_format_double_list(self, input_data, input_name=''):
            return '%s' % ' '.join(input_data)
        def gds_validate_double_list(
                self, input_data, node=None, input_name=''):
            values = input_data.split()
            for value in values:
                try:
                    float(value)
                except (TypeError, ValueError):
                    raise_parse_error(
                        node, 'Requires sequence of double or float values')
            return values
        def gds_format_boolean(self, input_data, input_name=''):
            return ('%s' % input_data).lower()
        def gds_parse_boolean(self, input_data, node=None, input_name=''):
            if input_data in ('true', '1'):
                bval = True
            elif input_data in ('false', '0'):
                bval = False
            else:
                raise_parse_error(node, 'Requires boolean value')
            return bval
        def gds_validate_boolean(self, input_data, node=None, input_name=''):
            if input_data not in (True, 1, False, 0, ):
                raise_parse_error(
                    node,
                    'Requires boolean value '
                    '(one of True, 1, False, 0)')
            return input_data
        def gds_format_boolean_list(self, input_data, input_name=''):
            return '%s' % ' '.join(input_data)
        def gds_validate_boolean_list(
                self, input_data, node=None, input_name=''):
            values = input_data.split()
            for value in values:
                if value not in (True, 1, False, 0, ):
                    raise_parse_error(
                        node,
                        'Requires sequence of boolean values '
                        '(one of True, 1, False, 0)')
            return values
        def gds_validate_datetime(self, input_data, node=None, input_name=''):
            return input_data
        def gds_format_datetime(self, input_data, input_name=''):
            if input_data.microsecond == 0:
                _svalue = '%04d-%02d-%02dT%02d:%02d:%02d' % (
                    input_data.year,
                    input_data.month,
                    input_data.day,
                    input_data.hour,
                    input_data.minute,
                    input_data.second,
                )
            else:
                _svalue = '%04d-%02d-%02dT%02d:%02d:%02d.%s' % (
                    input_data.year,
                    input_data.month,
                    input_data.day,
                    input_data.hour,
                    input_data.minute,
                    input_data.second,
                    ('%f' % (float(input_data.microsecond) / 1000000))[2:],
                )
            if input_data.tzinfo is not None:
                tzoff = input_data.tzinfo.utcoffset(input_data)
                if tzoff is not None:
                    total_seconds = tzoff.seconds + (86400 * tzoff.days)
                    if total_seconds == 0:
                        _svalue += 'Z'
                    else:
                        if total_seconds < 0:
                            _svalue += '-'
                            total_seconds *= -1
                        else:
                            _svalue += '+'
                        hours = total_seconds // 3600
                        minutes = (total_seconds - (hours * 3600)) // 60
                        _svalue += '{0:02d}:{1:02d}'.format(hours, minutes)
            return _svalue
        @classmethod
        def gds_parse_datetime(cls, input_data):
            tz = None
            if input_data[-1] == 'Z':
                tz = GeneratedsSuper._FixedOffsetTZ(0, 'UTC')
                input_data = input_data[:-1]
            else:
                results = GeneratedsSuper.tzoff_pattern.search(input_data)
                if results is not None:
                    tzoff_parts = results.group(2).split(':')
                    tzoff = int(tzoff_parts[0]) * 60 + int(tzoff_parts[1])
                    if results.group(1) == '-':
                        tzoff *= -1
                    tz = GeneratedsSuper._FixedOffsetTZ(
                        tzoff, results.group(0))
                    input_data = input_data[:-6]
            time_parts = input_data.split('.')
            if len(time_parts) > 1:
                micro_seconds = int(float('0.' + time_parts[1]) * 1000000)
                input_data = '%s.%s' % (
                    time_parts[0], "{}".format(micro_seconds).rjust(6, "0"), )
                dt = datetime_.datetime.strptime(
                    input_data, '%Y-%m-%dT%H:%M:%S.%f')
            else:
                dt = datetime_.datetime.strptime(
                    input_data, '%Y-%m-%dT%H:%M:%S')
            dt = dt.replace(tzinfo=tz)
            return dt
        def gds_validate_date(self, input_data, node=None, input_name=''):
            return input_data
        def gds_format_date(self, input_data, input_name=''):
            _svalue = '%04d-%02d-%02d' % (
                input_data.year,
                input_data.month,
                input_data.day,
            )
            try:
                if input_data.tzinfo is not None:
                    tzoff = input_data.tzinfo.utcoffset(input_data)
                    if tzoff is not None:
                        total_seconds = tzoff.seconds + (86400 * tzoff.days)
                        if total_seconds == 0:
                            _svalue += 'Z'
                        else:
                            if total_seconds < 0:
                                _svalue += '-'
                                total_seconds *= -1
                            else:
                                _svalue += '+'
                            hours = total_seconds // 3600
                            minutes = (total_seconds - (hours * 3600)) // 60
                            _svalue += '{0:02d}:{1:02d}'.format(
                                hours, minutes)
            except AttributeError:
                pass
            return _svalue
        @classmethod
        def gds_parse_date(cls, input_data):
            tz = None
            if input_data[-1] == 'Z':
                tz = GeneratedsSuper._FixedOffsetTZ(0, 'UTC')
                input_data = input_data[:-1]
            else:
                results = GeneratedsSuper.tzoff_pattern.search(input_data)
                if results is not None:
                    tzoff_parts = results.group(2).split(':')
                    tzoff = int(tzoff_parts[0]) * 60 + int(tzoff_parts[1])
                    if results.group(1) == '-':
                        tzoff *= -1
                    tz = GeneratedsSuper._FixedOffsetTZ(
                        tzoff, results.group(0))
                    input_data = input_data[:-6]
            dt = datetime_.datetime.strptime(input_data, '%Y-%m-%d')
            dt = dt.replace(tzinfo=tz)
            return dt.date()
        def gds_validate_time(self, input_data, node=None, input_name=''):
            return input_data
        def gds_format_time(self, input_data, input_name=''):
            if input_data.microsecond == 0:
                _svalue = '%02d:%02d:%02d' % (
                    input_data.hour,
                    input_data.minute,
                    input_data.second,
                )
            else:
                _svalue = '%02d:%02d:%02d.%s' % (
                    input_data.hour,
                    input_data.minute,
                    input_data.second,
                    ('%f' % (float(input_data.microsecond) / 1000000))[2:],
                )
            if input_data.tzinfo is not None:
                tzoff = input_data.tzinfo.utcoffset(input_data)
                if tzoff is not None:
                    total_seconds = tzoff.seconds + (86400 * tzoff.days)
                    if total_seconds == 0:
                        _svalue += 'Z'
                    else:
                        if total_seconds < 0:
                            _svalue += '-'
                            total_seconds *= -1
                        else:
                            _svalue += '+'
                        hours = total_seconds // 3600
                        minutes = (total_seconds - (hours * 3600)) // 60
                        _svalue += '{0:02d}:{1:02d}'.format(hours, minutes)
            return _svalue
        def gds_validate_simple_patterns(self, patterns, target):
            # pat is a list of lists of strings/patterns.
            # The target value must match at least one of the patterns
            # in order for the test to succeed.
            found1 = True
            for patterns1 in patterns:
                found2 = False
                for patterns2 in patterns1:
                    mo = re_.search(patterns2, target)
                    if mo is not None and len(mo.group(0)) == len(target):
                        found2 = True
                        break
                if not found2:
                    found1 = False
                    break
            return found1
        @classmethod
        def gds_parse_time(cls, input_data):
            tz = None
            if input_data[-1] == 'Z':
                tz = GeneratedsSuper._FixedOffsetTZ(0, 'UTC')
                input_data = input_data[:-1]
            else:
                results = GeneratedsSuper.tzoff_pattern.search(input_data)
                if results is not None:
                    tzoff_parts = results.group(2).split(':')
                    tzoff = int(tzoff_parts[0]) * 60 + int(tzoff_parts[1])
                    if results.group(1) == '-':
                        tzoff *= -1
                    tz = GeneratedsSuper._FixedOffsetTZ(
                        tzoff, results.group(0))
                    input_data = input_data[:-6]
            if len(input_data.split('.')) > 1:
                dt = datetime_.datetime.strptime(input_data, '%H:%M:%S.%f')
            else:
                dt = datetime_.datetime.strptime(input_data, '%H:%M:%S')
            dt = dt.replace(tzinfo=tz)
            return dt.time()
        def gds_check_cardinality_(
                self, value, input_name,
                min_occurs=0, max_occurs=1, required=None):
            if value is None:
                length = 0
            elif isinstance(value, list):
                length = len(value)
            else:
                length = 1
            if required is not None :
                if required and length < 1:
                    self.gds_collector_.add_message(
                        "Required value {}{} is missing".format(
                            input_name, self.gds_get_node_lineno_()))
            if length < min_occurs:
                self.gds_collector_.add_message(
                    "Number of values for {}{} is below "
                    "the minimum allowed, "
                    "expected at least {}, found {}".format(
                        input_name, self.gds_get_node_lineno_(),
                        min_occurs, length))
            elif length > max_occurs:
                self.gds_collector_.add_message(
                    "Number of values for {}{} is above "
                    "the maximum allowed, "
                    "expected at most {}, found {}".format(
                        input_name, self.gds_get_node_lineno_(),
                        max_occurs, length))
        def gds_validate_builtin_ST_(
                self, validator, value, input_name,
                min_occurs=None, max_occurs=None, required=None):
            if value is not None:
                try:
                    validator(value, input_name=input_name)
                except GDSParseError as parse_error:
                    self.gds_collector_.add_message(str(parse_error))
        def gds_validate_defined_ST_(
                self, validator, value, input_name,
                min_occurs=None, max_occurs=None, required=None):
            if value is not None:
                try:
                    validator(value)
                except GDSParseError as parse_error:
                    self.gds_collector_.add_message(str(parse_error))
        def gds_str_lower(self, instring):
            return instring.lower()
        def get_path_(self, node):
            path_list = []
            self.get_path_list_(node, path_list)
            path_list.reverse()
            path = '/'.join(path_list)
            return path
        Tag_strip_pattern_ = re_.compile(r'\{.*\}')
        def get_path_list_(self, node, path_list):
            if node is None:
                return
            tag = GeneratedsSuper.Tag_strip_pattern_.sub('', node.tag)
            if tag:
                path_list.append(tag)
            self.get_path_list_(node.getparent(), path_list)
        def get_class_obj_(self, node, default_class=None):
            class_obj1 = default_class
            if 'xsi' in node.nsmap:
                classname = node.get('{%s}type' % node.nsmap['xsi'])
                if classname is not None:
                    names = classname.split(':')
                    if len(names) == 2:
                        classname = names[1]
                    class_obj2 = globals().get(classname)
                    if class_obj2 is not None:
                        class_obj1 = class_obj2
            return class_obj1
        def gds_build_any(self, node, type_name=None):
            # provide default value in case option --disable-xml is used.
            content = ""
            content = etree_.tostring(node, encoding="unicode")
            return content
        @classmethod
        def gds_reverse_node_mapping(cls, mapping):
            return dict(((v, k) for k, v in mapping.items()))
        @staticmethod
        def gds_encode(instring):
            if sys.version_info.major == 2:
                if ExternalEncoding:
                    encoding = ExternalEncoding
                else:
                    encoding = 'utf-8'
                return instring.encode(encoding)
            else:
                return instring
        @staticmethod
        def convert_unicode(instring):
            if isinstance(instring, str):
                result = quote_xml(instring)
            elif sys.version_info.major == 2 and isinstance(instring, unicode):
                result = quote_xml(instring).encode('utf8')
            else:
                result = GeneratedsSuper.gds_encode(str(instring))
            return result
        def __eq__(self, other):
            def excl_select_objs_(obj):
                return (obj[0] != 'parent_object_' and
                        obj[0] != 'gds_collector_')
            if type(self) != type(other):
                return False
            return all(x == y for x, y in zip_longest(
                filter(excl_select_objs_, self.__dict__.items()),
                filter(excl_select_objs_, other.__dict__.items())))
        def __ne__(self, other):
            return not self.__eq__(other)
        # Django ETL transform hooks.
        def gds_djo_etl_transform(self):
            pass
        def gds_djo_etl_transform_db_obj(self, dbobj):
            pass
        # SQLAlchemy ETL transform hooks.
        def gds_sqa_etl_transform(self):
            return 0, None
        def gds_sqa_etl_transform_db_obj(self, dbobj):
            pass
        def gds_get_node_lineno_(self):
            if (hasattr(self, "gds_elementtree_node_") and
                    self.gds_elementtree_node_ is not None):
                return ' near line {}'.format(
                    self.gds_elementtree_node_.sourceline)
            else:
                return ""
    
    
    def getSubclassFromModule_(module, class_):
        '''Get the subclass of a class from a specific module.'''
        name = class_.__name__ + 'Sub'
        if hasattr(module, name):
            return getattr(module, name)
        else:
            return None


#
# If you have installed IPython you can uncomment and use the following.
# IPython is available from http://ipython.scipy.org/.
#

## from IPython.Shell import IPShellEmbed
## args = ''
## ipshell = IPShellEmbed(args,
##     banner = 'Dropping into IPython',
##     exit_msg = 'Leaving Interpreter, back to program.')

# Then use the following line where and when you want to drop into the
# IPython shell:
#    ipshell('<some message> -- Entering ipshell.\nHit Ctrl-D to exit')

#
# Globals
#

ExternalEncoding = 'utf-8'
# Set this to false in order to deactivate during export, the use of
# name space prefixes captured from the input document.
UseCapturedNS_ = True
CapturedNsmap_ = {}
Tag_pattern_ = re_.compile(r'({.*})?(.*)')
String_cleanup_pat_ = re_.compile(r"[\n\r\s]+")
Namespace_extract_pat_ = re_.compile(r'{(.*)}(.*)')
CDATA_pattern_ = re_.compile(r"<!\[CDATA\[.*?\]\]>", re_.DOTALL)

# Change this to redirect the generated superclass module to use a
# specific subclass module.
CurrentSubclassModule_ = None

#
# Support/utility functions.
#


def showIndent(outfile, level, pretty_print=True):
    if pretty_print:
        for idx in range(level):
            outfile.write('    ')


def quote_xml(inStr):
    "Escape markup chars, but do not modify CDATA sections."
    if not inStr:
        return ''
    s1 = (isinstance(inStr, BaseStrType_) and inStr or '%s' % inStr)
    s2 = ''
    pos = 0
    matchobjects = CDATA_pattern_.finditer(s1)
    for mo in matchobjects:
        s3 = s1[pos:mo.start()]
        s2 += quote_xml_aux(s3)
        s2 += s1[mo.start():mo.end()]
        pos = mo.end()
    s3 = s1[pos:]
    s2 += quote_xml_aux(s3)
    return s2


def quote_xml_aux(inStr):
    s1 = inStr.replace('&', '&amp;')
    s1 = s1.replace('<', '&lt;')
    s1 = s1.replace('>', '&gt;')
    return s1


def quote_attrib(inStr):
    s1 = (isinstance(inStr, BaseStrType_) and inStr or '%s' % inStr)
    s1 = s1.replace('&', '&amp;')
    s1 = s1.replace('<', '&lt;')
    s1 = s1.replace('>', '&gt;')
    if '"' in s1:
        if "'" in s1:
            s1 = '"%s"' % s1.replace('"', "&quot;")
        else:
            s1 = "'%s'" % s1
    else:
        s1 = '"%s"' % s1
    return s1


def quote_python(inStr):
    s1 = inStr
    if s1.find("'") == -1:
        if s1.find('\n') == -1:
            return "'%s'" % s1
        else:
            return "'''%s'''" % s1
    else:
        if s1.find('"') != -1:
            s1 = s1.replace('"', '\\"')
        if s1.find('\n') == -1:
            return '"%s"' % s1
        else:
            return '"""%s"""' % s1


def get_all_text_(node):
    if node.text is not None:
        text = node.text
    else:
        text = ''
    for child in node:
        if child.tail is not None:
            text += child.tail
    return text


def find_attr_value_(attr_name, node):
    attrs = node.attrib
    attr_parts = attr_name.split(':')
    value = None
    if len(attr_parts) == 1:
        value = attrs.get(attr_name)
    elif len(attr_parts) == 2:
        prefix, name = attr_parts
        namespace = node.nsmap.get(prefix)
        if namespace is not None:
            value = attrs.get('{%s}%s' % (namespace, name, ))
    return value


def encode_str_2_3(instr):
    return instr


class GDSParseError(Exception):
    pass


def raise_parse_error(node, msg):
    if node is not None:
        msg = '%s (element %s/line %d)' % (msg, node.tag, node.sourceline, )
    raise GDSParseError(msg)


class MixedContainer:
    # Constants for category:
    CategoryNone = 0
    CategoryText = 1
    CategorySimple = 2
    CategoryComplex = 3
    # Constants for content_type:
    TypeNone = 0
    TypeText = 1
    TypeString = 2
    TypeInteger = 3
    TypeFloat = 4
    TypeDecimal = 5
    TypeDouble = 6
    TypeBoolean = 7
    TypeBase64 = 8
    def __init__(self, category, content_type, name, value):
        self.category = category
        self.content_type = content_type
        self.name = name
        self.value = value
    def getCategory(self):
        return self.category
    def getContenttype(self, content_type):
        return self.content_type
    def getValue(self):
        return self.value
    def getName(self):
        return self.name
    def export(self, outfile, level, name, namespace,
               pretty_print=True):
        if self.category == MixedContainer.CategoryText:
            # Prevent exporting empty content as empty lines.
            if self.value.strip():
                outfile.write(self.value)
        elif self.category == MixedContainer.CategorySimple:
            self.exportSimple(outfile, level, name)
        else:    # category == MixedContainer.CategoryComplex
            self.value.export(
                outfile, level, namespace, name_=name,
                pretty_print=pretty_print)
    def exportSimple(self, outfile, level, name):
        if self.content_type == MixedContainer.TypeString:
            outfile.write('<%s>%s</%s>' % (
                self.name, self.value, self.name))
        elif self.content_type == MixedContainer.TypeInteger or \
                self.content_type == MixedContainer.TypeBoolean:
            outfile.write('<%s>%d</%s>' % (
                self.name, self.value, self.name))
        elif self.content_type == MixedContainer.TypeFloat or \
                self.content_type == MixedContainer.TypeDecimal:
            outfile.write('<%s>%f</%s>' % (
                self.name, self.value, self.name))
        elif self.content_type == MixedContainer.TypeDouble:
            outfile.write('<%s>%g</%s>' % (
                self.name, self.value, self.name))
        elif self.content_type == MixedContainer.TypeBase64:
            outfile.write('<%s>%s</%s>' % (
                self.name,
                base64.b64encode(self.value),
                self.name))
    def to_etree(self, element, mapping_=None, nsmap_=None):
        if self.category == MixedContainer.CategoryText:
            # Prevent exporting empty content as empty lines.
            if self.value.strip():
                if len(element) > 0:
                    if element[-1].tail is None:
                        element[-1].tail = self.value
                    else:
                        element[-1].tail += self.value
                else:
                    if element.text is None:
                        element.text = self.value
                    else:
                        element.text += self.value
        elif self.category == MixedContainer.CategorySimple:
            subelement = etree_.SubElement(
                element, '%s' % self.name)
            subelement.text = self.to_etree_simple()
        else:    # category == MixedContainer.CategoryComplex
            self.value.to_etree(element)
    def to_etree_simple(self, mapping_=None, nsmap_=None):
        if self.content_type == MixedContainer.TypeString:
            text = self.value
        elif (self.content_type == MixedContainer.TypeInteger or
                self.content_type == MixedContainer.TypeBoolean):
            text = '%d' % self.value
        elif (self.content_type == MixedContainer.TypeFloat or
                self.content_type == MixedContainer.TypeDecimal):
            text = '%f' % self.value
        elif self.content_type == MixedContainer.TypeDouble:
            text = '%g' % self.value
        elif self.content_type == MixedContainer.TypeBase64:
            text = '%s' % base64.b64encode(self.value)
        return text
    def exportLiteral(self, outfile, level, name):
        if self.category == MixedContainer.CategoryText:
            showIndent(outfile, level)
            outfile.write(
                'model_.MixedContainer(%d, %d, "%s", "%s"),\n' % (
                    self.category, self.content_type,
                    self.name, self.value))
        elif self.category == MixedContainer.CategorySimple:
            showIndent(outfile, level)
            outfile.write(
                'model_.MixedContainer(%d, %d, "%s", "%s"),\n' % (
                    self.category, self.content_type,
                    self.name, self.value))
        else:    # category == MixedContainer.CategoryComplex
            showIndent(outfile, level)
            outfile.write(
                'model_.MixedContainer(%d, %d, "%s",\n' % (
                    self.category, self.content_type, self.name,))
            self.value.exportLiteral(outfile, level + 1)
            showIndent(outfile, level)
            outfile.write(')\n')


class MemberSpec_(object):
    def __init__(self, name='', data_type='', container=0,
            optional=0, child_attrs=None, choice=None):
        self.name = name
        self.data_type = data_type
        self.container = container
        self.child_attrs = child_attrs
        self.choice = choice
        self.optional = optional
    def set_name(self, name): self.name = name
    def get_name(self): return self.name
    def set_data_type(self, data_type): self.data_type = data_type
    def get_data_type_chain(self): return self.data_type
    def get_data_type(self):
        if isinstance(self.data_type, list):
            if len(self.data_type) > 0:
                return self.data_type[-1]
            else:
                return 'xs:string'
        else:
            return self.data_type
    def set_container(self, container): self.container = container
    def get_container(self): return self.container
    def set_child_attrs(self, child_attrs): self.child_attrs = child_attrs
    def get_child_attrs(self): return self.child_attrs
    def set_choice(self, choice): self.choice = choice
    def get_choice(self): return self.choice
    def set_optional(self, optional): self.optional = optional
    def get_optional(self): return self.optional


def _cast(typ, value):
    if typ is None or value is None:
        return value
    return typ(value)

#
# Data representation classes.
#


class token_enum_st(str, Enum):
    FLOAT='float'
    INT='int'
    NAME='Name'
    TOKEN='token'


class containerType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    member_data_items_ = [
        MemberSpec_('sample1', 'simpleOneType', 1, 0, {'maxOccurs': 'unbounded', 'name': 'sample1', 'type': 'simpleOneType'}, None),
        MemberSpec_('sample2_bad', 'simpleOneType', 1, 0, {'maxOccurs': 'unbounded', 'name': 'sample2_bad', 'type': 'simpleOneType'}, None),
        MemberSpec_('sample3_bad', 'simpleOneType', 1, 0, {'maxOccurs': 'unbounded', 'name': 'sample3_bad', 'type': 'simpleOneType'}, None),
        MemberSpec_('sample4_bad', 'simpleOneType', 1, 0, {'maxOccurs': 'unbounded', 'name': 'sample4_bad', 'type': 'simpleOneType'}, None),
        MemberSpec_('sample2', 'simpleTwoType', 1, 0, {'maxOccurs': 'unbounded', 'name': 'sample2', 'type': 'simpleTwoType'}, None),
    ]
    subclass = None
    superclass = None
    def __init__(self, sample1=None, sample2_bad=None, sample3_bad=None, sample4_bad=None, sample2=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if sample1 is None:
            self.sample1 = []
        else:
            self.sample1 = sample1
        self.sample1_nsprefix_ = None
        if sample2_bad is None:
            self.sample2_bad = []
        else:
            self.sample2_bad = sample2_bad
        self.sample2_bad_nsprefix_ = None
        if sample3_bad is None:
            self.sample3_bad = []
        else:
            self.sample3_bad = sample3_bad
        self.sample3_bad_nsprefix_ = None
        if sample4_bad is None:
            self.sample4_bad = []
        else:
            self.sample4_bad = sample4_bad
        self.sample4_bad_nsprefix_ = None
        if sample2 is None:
            self.sample2 = []
        else:
            self.sample2 = sample2
        self.sample2_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, containerType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if containerType.subclass:
            return containerType.subclass(*args_, **kwargs_)
        else:
            return containerType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_sample1(self):
        return self.sample1
    def set_sample1(self, sample1):
        self.sample1 = sample1
    def add_sample1(self, value):
        self.sample1.append(value)
    def insert_sample1_at(self, index, value):
        self.sample1.insert(index, value)
    def replace_sample1_at(self, index, value):
        self.sample1[index] = value
    def get_sample2_bad(self):
        return self.sample2_bad
    def set_sample2_bad(self, sample2_bad):
        self.sample2_bad = sample2_bad
    def add_sample2_bad(self, value):
        self.sample2_bad.append(value)
    def insert_sample2_bad_at(self, index, value):
        self.sample2_bad.insert(index, value)
    def replace_sample2_bad_at(self, index, value):
        self.sample2_bad[index] = value
    def get_sample3_bad(self):
        return self.sample3_bad
    def set_sample3_bad(self, sample3_bad):
        self.sample3_bad = sample3_bad
    def add_sample3_bad(self, value):
        self.sample3_bad.append(value)
    def insert_sample3_bad_at(self, index, value):
        self.sample3_bad.insert(index, value)
    def replace_sample3_bad_at(self, index, value):
        self.sample3_bad[index] = value
    def get_sample4_bad(self):
        return self.sample4_bad
    def set_sample4_bad(self, sample4_bad):
        self.sample4_bad = sample4_bad
    def add_sample4_bad(self, value):
        self.sample4_bad.append(value)
    def insert_sample4_bad_at(self, index, value):
        self.sample4_bad.insert(index, value)
    def replace_sample4_bad_at(self, index, value):
        self.sample4_bad[index] = value
    def get_sample2(self):
        return self.sample2
    def set_sample2(self, sample2):
        self.sample2 = sample2
    def add_sample2(self, value):
        self.sample2.append(value)
    def insert_sample2_at(self, index, value):
        self.sample2.insert(index, value)
    def replace_sample2_at(self, index, value):
        self.sample2[index] = value
    def hasContent_(self):
        if (
            self.sample1 or
            self.sample2_bad or
            self.sample3_bad or
            self.sample4_bad or
            self.sample2
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='containerType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('containerType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'containerType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='containerType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='containerType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='containerType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='containerType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for sample1_ in self.sample1:
            namespaceprefix_ = self.sample1_nsprefix_ + ':' if (UseCapturedNS_ and self.sample1_nsprefix_) else ''
            sample1_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='sample1', pretty_print=pretty_print)
        for sample2_bad_ in self.sample2_bad:
            namespaceprefix_ = self.sample2_bad_nsprefix_ + ':' if (UseCapturedNS_ and self.sample2_bad_nsprefix_) else ''
            sample2_bad_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='sample2_bad', pretty_print=pretty_print)
        for sample3_bad_ in self.sample3_bad:
            namespaceprefix_ = self.sample3_bad_nsprefix_ + ':' if (UseCapturedNS_ and self.sample3_bad_nsprefix_) else ''
            sample3_bad_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='sample3_bad', pretty_print=pretty_print)
        for sample4_bad_ in self.sample4_bad:
            namespaceprefix_ = self.sample4_bad_nsprefix_ + ':' if (UseCapturedNS_ and self.sample4_bad_nsprefix_) else ''
            sample4_bad_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='sample4_bad', pretty_print=pretty_print)
        for sample2_ in self.sample2:
            namespaceprefix_ = self.sample2_nsprefix_ + ':' if (UseCapturedNS_ and self.sample2_nsprefix_) else ''
            sample2_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='sample2', pretty_print=pretty_print)
    def validate_(self, gds_collector, recursive=False):
        self.gds_collector_ = gds_collector
        message_count = len(self.gds_collector_.get_messages())
        # validate simple type attributes
        # validate simple type children
        # validate complex type children
        self.gds_check_cardinality_(self.sample1, 'sample1', min_occurs=1, max_occurs=9999999)
        self.gds_check_cardinality_(self.sample2_bad, 'sample2_bad', min_occurs=1, max_occurs=9999999)
        self.gds_check_cardinality_(self.sample3_bad, 'sample3_bad', min_occurs=1, max_occurs=9999999)
        self.gds_check_cardinality_(self.sample4_bad, 'sample4_bad', min_occurs=1, max_occurs=9999999)
        self.gds_check_cardinality_(self.sample2, 'sample2', min_occurs=1, max_occurs=9999999)
        if recursive:
            for item in self.sample1:
                item.validate_(gds_collector, recursive=True)
            for item in self.sample2_bad:
                item.validate_(gds_collector, recursive=True)
            for item in self.sample3_bad:
                item.validate_(gds_collector, recursive=True)
            for item in self.sample4_bad:
                item.validate_(gds_collector, recursive=True)
            for item in self.sample2:
                item.validate_(gds_collector, recursive=True)
        return message_count == len(self.gds_collector_.get_messages())
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'sample1':
            obj_ = simpleOneType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.sample1.append(obj_)
            obj_.original_tagname_ = 'sample1'
        elif nodeName_ == 'sample2_bad':
            obj_ = simpleOneType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.sample2_bad.append(obj_)
            obj_.original_tagname_ = 'sample2_bad'
        elif nodeName_ == 'sample3_bad':
            obj_ = simpleOneType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.sample3_bad.append(obj_)
            obj_.original_tagname_ = 'sample3_bad'
        elif nodeName_ == 'sample4_bad':
            obj_ = simpleOneType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.sample4_bad.append(obj_)
            obj_.original_tagname_ = 'sample4_bad'
        elif nodeName_ == 'sample2':
            obj_ = simpleTwoType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.sample2.append(obj_)
            obj_.original_tagname_ = 'sample2'
# end class containerType


class simpleOneType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    member_data_items_ = [
        MemberSpec_('integer_range_1_value_with_default', 'integer_range_1_st', 0, 1, {'use': 'optional'}),
        MemberSpec_('integer_range_1_value', ['integer_range_1_st', 'integer_range_2_st', 'xs:integer'], 0, 0, {'default': '5', 'name': 'integer_range_1_value', 'type': 'xs:integer'}, None),
        MemberSpec_('pattern_value', ['pattern_st', 'pattern_1_st', 'min_length_st', 'xs:string'], 0, 0, {'name': 'pattern_value', 'type': 'xs:string'}, None),
        MemberSpec_('token_enum_value', ['token_enum_st', 'xs:NMTOKEN'], 0, 0, {'name': 'token_enum_value', 'type': 'xs:NMTOKEN'}, None),
        MemberSpec_('integer_range_incl_value', ['integer_range_incl_st', 'xs:integer'], 0, 0, {'name': 'integer_range_incl_value', 'type': 'xs:integer'}, None),
        MemberSpec_('integer_range_excl_value', ['integer_range_excl_st', 'xs:integer'], 0, 0, {'name': 'integer_range_excl_value', 'type': 'xs:integer'}, None),
        MemberSpec_('min_max_length_value', ['min_max_length_st', 'xs:string'], 0, 0, {'name': 'min_max_length_value', 'type': 'xs:string'}, None),
        MemberSpec_('length_value', ['length_st', 'xs:string'], 0, 0, {'name': 'length_value', 'type': 'xs:string'}, None),
        MemberSpec_('totalDigits_value', ['totalDigits_st', 'xs:decimal'], 0, 0, {'name': 'totalDigits_value', 'type': 'xs:decimal'}, None),
        MemberSpec_('date_minincl_value', ['date_minincl_st', 'xs:date'], 0, 0, {'name': 'date_minincl_value', 'type': 'xs:date'}, None),
        MemberSpec_('date_maxincl_value', ['date_maxincl_st', 'xs:date'], 0, 0, {'name': 'date_maxincl_value', 'type': 'xs:date'}, None),
        MemberSpec_('date_minexcl_value', ['date_minexcl_st', 'xs:date'], 0, 0, {'name': 'date_minexcl_value', 'type': 'xs:date'}, None),
        MemberSpec_('date_maxexcl_value', ['date_maxexcl_st', 'xs:date'], 0, 0, {'name': 'date_maxexcl_value', 'type': 'xs:date'}, None),
        MemberSpec_('time_minincl_value', ['time_minincl_st', 'xs:time'], 0, 0, {'name': 'time_minincl_value', 'type': 'xs:time'}, None),
        MemberSpec_('time_maxincl_value', ['time_maxincl_st', 'xs:time'], 0, 0, {'name': 'time_maxincl_value', 'type': 'xs:time'}, None),
        MemberSpec_('time_minexcl_value', ['time_minexcl_st', 'xs:time'], 0, 0, {'name': 'time_minexcl_value', 'type': 'xs:time'}, None),
        MemberSpec_('time_maxexcl_value', ['time_maxexcl_st', 'xs:time'], 0, 0, {'name': 'time_maxexcl_value', 'type': 'xs:time'}, None),
        MemberSpec_('datetime_minincl_value', ['datetime_minincl_st', 'xs:dateTime'], 0, 0, {'name': 'datetime_minincl_value', 'type': 'xs:dateTime'}, None),
        MemberSpec_('datetime_maxincl_value', ['datetime_maxincl_st', 'xs:dateTime'], 0, 0, {'name': 'datetime_maxincl_value', 'type': 'xs:dateTime'}, None),
        MemberSpec_('datetime_minexcl_value', ['datetime_minexcl_st', 'xs:dateTime'], 0, 0, {'name': 'datetime_minexcl_value', 'type': 'xs:dateTime'}, None),
        MemberSpec_('datetime_maxexcl_value', ['datetime_maxexcl_st', 'xs:dateTime'], 0, 0, {'name': 'datetime_maxexcl_value', 'type': 'xs:dateTime'}, None),
        MemberSpec_('vbar_pattern_value', ['vbar_pattern_st', 'xs:string'], 0, 0, {'name': 'vbar_pattern_value', 'type': 'xs:string'}, None),
        MemberSpec_('unicode_pattern_value', ['unicode_pattern_st', 'xs:string'], 0, 0, {'name': 'unicode_pattern_value', 'type': 'xs:string'}, None),
        MemberSpec_('gyear_minincl_value', ['gyear_minincl_st', 'xs:gYear'], 0, 0, {'name': 'gyear_minincl_value', 'type': 'xs:gYear'}, None),
        MemberSpec_('gyearmonth_minincl_value', ['gyearmonth_minincl_st', 'xs:gYearMonth'], 0, 0, {'name': 'gyearmonth_minincl_value', 'type': 'xs:gYearMonth'}, None),
        MemberSpec_('simpletype0', ['integer_range_A_0_st', 'namespaceA:integer_range_A_1_st'], 0, 0, {'name': 'simpletype0', 'type': 'xs:integer'}, None),
        MemberSpec_('simpletype1', ['integer_range_A_1_st', 'namespaceA:integer_range_A_2_st'], 0, 0, {'name': 'simpletype1', 'type': 'xs:integer'}, None),
        MemberSpec_('simpletype2', ['integer_range_A_2_st', 'xs:integer'], 0, 0, {'name': 'simpletype2', 'type': 'xs:integer'}, None),
        MemberSpec_('simpletype0a', ['integer_range_A_0_st', 'namespaceA:integer_range_A_1_st'], 0, 0, {'name': 'simpletype0a', 'type': 'xs:integer'}, None),
        MemberSpec_('simpletype1a', ['integer_range_A_1_st', 'namespaceA:integer_range_A_2_st'], 0, 0, {'name': 'simpletype1a', 'type': 'xs:integer'}, None),
        MemberSpec_('simpletype2a', ['integer_range_A_2_st', 'xs:integer'], 0, 0, {'name': 'simpletype2a', 'type': 'xs:integer'}, None),
        MemberSpec_('anonymous_float_value', ['anonymous_float_valueType', 'xs:float'], 0, 0, {'name': 'anonymous_float_value', 'type': 'xs:float'}, None),
        MemberSpec_('primative_integer', 'xs:integer', 0, 0, {'name': 'primative_integer', 'type': 'xs:integer'}, None),
        MemberSpec_('primative_float', 'xs:float', 0, 0, {'name': 'primative_float', 'type': 'xs:float'}, None),
    ]
    subclass = None
    superclass = None
    def __init__(self, integer_range_1_value_with_default='6', integer_range_1_value=5, pattern_value=None, token_enum_value=None, integer_range_incl_value=None, integer_range_excl_value=None, min_max_length_value=None, length_value=None, totalDigits_value=None, date_minincl_value=None, date_maxincl_value=None, date_minexcl_value=None, date_maxexcl_value=None, time_minincl_value=None, time_maxincl_value=None, time_minexcl_value=None, time_maxexcl_value=None, datetime_minincl_value=None, datetime_maxincl_value=None, datetime_minexcl_value=None, datetime_maxexcl_value=None, vbar_pattern_value=None, unicode_pattern_value=None, gyear_minincl_value=None, gyearmonth_minincl_value=None, simpletype0=None, simpletype1=None, simpletype2=None, simpletype0a=None, simpletype1a=None, simpletype2a=None, anonymous_float_value=None, primative_integer=None, primative_float=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.integer_range_1_value_with_default = _cast(int, integer_range_1_value_with_default)
        self.integer_range_1_value_with_default_nsprefix_ = None
        self.integer_range_1_value = integer_range_1_value
        self.validate_integer_range_1_st(self.integer_range_1_value)
        self.integer_range_1_value_nsprefix_ = None
        self.pattern_value = pattern_value
        self.validate_pattern_st(self.pattern_value)
        self.pattern_value_nsprefix_ = None
        self.token_enum_value = token_enum_value
        self.validate_token_enum_st(self.token_enum_value)
        self.token_enum_value_nsprefix_ = None
        self.integer_range_incl_value = integer_range_incl_value
        self.validate_integer_range_incl_st(self.integer_range_incl_value)
        self.integer_range_incl_value_nsprefix_ = None
        self.integer_range_excl_value = integer_range_excl_value
        self.validate_integer_range_excl_st(self.integer_range_excl_value)
        self.integer_range_excl_value_nsprefix_ = None
        self.min_max_length_value = min_max_length_value
        self.validate_min_max_length_st(self.min_max_length_value)
        self.min_max_length_value_nsprefix_ = None
        self.length_value = length_value
        self.validate_length_st(self.length_value)
        self.length_value_nsprefix_ = None
        self.totalDigits_value = totalDigits_value
        self.validate_totalDigits_st(self.totalDigits_value)
        self.totalDigits_value_nsprefix_ = None
        if isinstance(date_minincl_value, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(date_minincl_value, '%Y-%m-%d').date()
        else:
            initvalue_ = date_minincl_value
        self.date_minincl_value = initvalue_
        self.date_minincl_value_nsprefix_ = None
        if isinstance(date_maxincl_value, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(date_maxincl_value, '%Y-%m-%d').date()
        else:
            initvalue_ = date_maxincl_value
        self.date_maxincl_value = initvalue_
        self.date_maxincl_value_nsprefix_ = None
        if isinstance(date_minexcl_value, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(date_minexcl_value, '%Y-%m-%d').date()
        else:
            initvalue_ = date_minexcl_value
        self.date_minexcl_value = initvalue_
        self.date_minexcl_value_nsprefix_ = None
        if isinstance(date_maxexcl_value, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(date_maxexcl_value, '%Y-%m-%d').date()
        else:
            initvalue_ = date_maxexcl_value
        self.date_maxexcl_value = initvalue_
        self.date_maxexcl_value_nsprefix_ = None
        if isinstance(time_minincl_value, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(time_minincl_value, '%H:%M:%S').time()
        else:
            initvalue_ = time_minincl_value
        self.time_minincl_value = initvalue_
        self.time_minincl_value_nsprefix_ = None
        if isinstance(time_maxincl_value, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(time_maxincl_value, '%H:%M:%S').time()
        else:
            initvalue_ = time_maxincl_value
        self.time_maxincl_value = initvalue_
        self.time_maxincl_value_nsprefix_ = None
        if isinstance(time_minexcl_value, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(time_minexcl_value, '%H:%M:%S').time()
        else:
            initvalue_ = time_minexcl_value
        self.time_minexcl_value = initvalue_
        self.time_minexcl_value_nsprefix_ = None
        if isinstance(time_maxexcl_value, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(time_maxexcl_value, '%H:%M:%S').time()
        else:
            initvalue_ = time_maxexcl_value
        self.time_maxexcl_value = initvalue_
        self.time_maxexcl_value_nsprefix_ = None
        if isinstance(datetime_minincl_value, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(datetime_minincl_value, '%Y-%m-%dT%H:%M:%S')
        else:
            initvalue_ = datetime_minincl_value
        self.datetime_minincl_value = initvalue_
        self.datetime_minincl_value_nsprefix_ = None
        if isinstance(datetime_maxincl_value, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(datetime_maxincl_value, '%Y-%m-%dT%H:%M:%S')
        else:
            initvalue_ = datetime_maxincl_value
        self.datetime_maxincl_value = initvalue_
        self.datetime_maxincl_value_nsprefix_ = None
        if isinstance(datetime_minexcl_value, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(datetime_minexcl_value, '%Y-%m-%dT%H:%M:%S')
        else:
            initvalue_ = datetime_minexcl_value
        self.datetime_minexcl_value = initvalue_
        self.datetime_minexcl_value_nsprefix_ = None
        if isinstance(datetime_maxexcl_value, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(datetime_maxexcl_value, '%Y-%m-%dT%H:%M:%S')
        else:
            initvalue_ = datetime_maxexcl_value
        self.datetime_maxexcl_value = initvalue_
        self.datetime_maxexcl_value_nsprefix_ = None
        self.vbar_pattern_value = vbar_pattern_value
        self.validate_vbar_pattern_st(self.vbar_pattern_value)
        self.vbar_pattern_value_nsprefix_ = None
        self.unicode_pattern_value = unicode_pattern_value
        self.validate_unicode_pattern_st(self.unicode_pattern_value)
        self.unicode_pattern_value_nsprefix_ = None
        self.gyear_minincl_value = gyear_minincl_value
        self.validate_gyear_minincl_st(self.gyear_minincl_value)
        self.gyear_minincl_value_nsprefix_ = None
        self.gyearmonth_minincl_value = gyearmonth_minincl_value
        self.validate_gyearmonth_minincl_st(self.gyearmonth_minincl_value)
        self.gyearmonth_minincl_value_nsprefix_ = None
        self.simpletype0 = simpletype0
        self.validate_integer_range_A_0_st(self.simpletype0)
        self.simpletype0_nsprefix_ = None
        self.simpletype1 = simpletype1
        self.validate_integer_range_A_1_st(self.simpletype1)
        self.simpletype1_nsprefix_ = None
        self.simpletype2 = simpletype2
        self.validate_integer_range_A_2_st(self.simpletype2)
        self.simpletype2_nsprefix_ = None
        self.simpletype0a = simpletype0a
        self.validate_integer_range_A_0_st(self.simpletype0a)
        self.simpletype0a_nsprefix_ = None
        self.simpletype1a = simpletype1a
        self.validate_integer_range_A_1_st(self.simpletype1a)
        self.simpletype1a_nsprefix_ = None
        self.simpletype2a = simpletype2a
        self.validate_integer_range_A_2_st(self.simpletype2a)
        self.simpletype2a_nsprefix_ = None
        self.anonymous_float_value = anonymous_float_value
        self.validate_anonymous_float_valueType(self.anonymous_float_value)
        self.anonymous_float_value_nsprefix_ = None
        self.primative_integer = primative_integer
        self.primative_integer_nsprefix_ = None
        self.primative_float = primative_float
        self.primative_float_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, simpleOneType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if simpleOneType.subclass:
            return simpleOneType.subclass(*args_, **kwargs_)
        else:
            return simpleOneType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_integer_range_1_value(self):
        return self.integer_range_1_value
    def set_integer_range_1_value(self, integer_range_1_value):
        self.integer_range_1_value = integer_range_1_value
    def get_pattern_value(self):
        return self.pattern_value
    def set_pattern_value(self, pattern_value):
        self.pattern_value = pattern_value
    def get_token_enum_value(self):
        return self.token_enum_value
    def set_token_enum_value(self, token_enum_value):
        self.token_enum_value = token_enum_value
    def get_integer_range_incl_value(self):
        return self.integer_range_incl_value
    def set_integer_range_incl_value(self, integer_range_incl_value):
        self.integer_range_incl_value = integer_range_incl_value
    def get_integer_range_excl_value(self):
        return self.integer_range_excl_value
    def set_integer_range_excl_value(self, integer_range_excl_value):
        self.integer_range_excl_value = integer_range_excl_value
    def get_min_max_length_value(self):
        return self.min_max_length_value
    def set_min_max_length_value(self, min_max_length_value):
        self.min_max_length_value = min_max_length_value
    def get_length_value(self):
        return self.length_value
    def set_length_value(self, length_value):
        self.length_value = length_value
    def get_totalDigits_value(self):
        return self.totalDigits_value
    def set_totalDigits_value(self, totalDigits_value):
        self.totalDigits_value = totalDigits_value
    def get_date_minincl_value(self):
        return self.date_minincl_value
    def set_date_minincl_value(self, date_minincl_value):
        self.date_minincl_value = date_minincl_value
    def get_date_maxincl_value(self):
        return self.date_maxincl_value
    def set_date_maxincl_value(self, date_maxincl_value):
        self.date_maxincl_value = date_maxincl_value
    def get_date_minexcl_value(self):
        return self.date_minexcl_value
    def set_date_minexcl_value(self, date_minexcl_value):
        self.date_minexcl_value = date_minexcl_value
    def get_date_maxexcl_value(self):
        return self.date_maxexcl_value
    def set_date_maxexcl_value(self, date_maxexcl_value):
        self.date_maxexcl_value = date_maxexcl_value
    def get_time_minincl_value(self):
        return self.time_minincl_value
    def set_time_minincl_value(self, time_minincl_value):
        self.time_minincl_value = time_minincl_value
    def get_time_maxincl_value(self):
        return self.time_maxincl_value
    def set_time_maxincl_value(self, time_maxincl_value):
        self.time_maxincl_value = time_maxincl_value
    def get_time_minexcl_value(self):
        return self.time_minexcl_value
    def set_time_minexcl_value(self, time_minexcl_value):
        self.time_minexcl_value = time_minexcl_value
    def get_time_maxexcl_value(self):
        return self.time_maxexcl_value
    def set_time_maxexcl_value(self, time_maxexcl_value):
        self.time_maxexcl_value = time_maxexcl_value
    def get_datetime_minincl_value(self):
        return self.datetime_minincl_value
    def set_datetime_minincl_value(self, datetime_minincl_value):
        self.datetime_minincl_value = datetime_minincl_value
    def get_datetime_maxincl_value(self):
        return self.datetime_maxincl_value
    def set_datetime_maxincl_value(self, datetime_maxincl_value):
        self.datetime_maxincl_value = datetime_maxincl_value
    def get_datetime_minexcl_value(self):
        return self.datetime_minexcl_value
    def set_datetime_minexcl_value(self, datetime_minexcl_value):
        self.datetime_minexcl_value = datetime_minexcl_value
    def get_datetime_maxexcl_value(self):
        return self.datetime_maxexcl_value
    def set_datetime_maxexcl_value(self, datetime_maxexcl_value):
        self.datetime_maxexcl_value = datetime_maxexcl_value
    def get_vbar_pattern_value(self):
        return self.vbar_pattern_value
    def set_vbar_pattern_value(self, vbar_pattern_value):
        self.vbar_pattern_value = vbar_pattern_value
    def get_unicode_pattern_value(self):
        return self.unicode_pattern_value
    def set_unicode_pattern_value(self, unicode_pattern_value):
        self.unicode_pattern_value = unicode_pattern_value
    def get_gyear_minincl_value(self):
        return self.gyear_minincl_value
    def set_gyear_minincl_value(self, gyear_minincl_value):
        self.gyear_minincl_value = gyear_minincl_value
    def get_gyearmonth_minincl_value(self):
        return self.gyearmonth_minincl_value
    def set_gyearmonth_minincl_value(self, gyearmonth_minincl_value):
        self.gyearmonth_minincl_value = gyearmonth_minincl_value
    def get_simpletype0(self):
        return self.simpletype0
    def set_simpletype0(self, simpletype0):
        self.simpletype0 = simpletype0
    def get_simpletype1(self):
        return self.simpletype1
    def set_simpletype1(self, simpletype1):
        self.simpletype1 = simpletype1
    def get_simpletype2(self):
        return self.simpletype2
    def set_simpletype2(self, simpletype2):
        self.simpletype2 = simpletype2
    def get_simpletype0a(self):
        return self.simpletype0a
    def set_simpletype0a(self, simpletype0a):
        self.simpletype0a = simpletype0a
    def get_simpletype1a(self):
        return self.simpletype1a
    def set_simpletype1a(self, simpletype1a):
        self.simpletype1a = simpletype1a
    def get_simpletype2a(self):
        return self.simpletype2a
    def set_simpletype2a(self, simpletype2a):
        self.simpletype2a = simpletype2a
    def get_anonymous_float_value(self):
        return self.anonymous_float_value
    def set_anonymous_float_value(self, anonymous_float_value):
        self.anonymous_float_value = anonymous_float_value
    def get_primative_integer(self):
        return self.primative_integer
    def set_primative_integer(self, primative_integer):
        self.primative_integer = primative_integer
    def get_primative_float(self):
        return self.primative_float
    def set_primative_float(self, primative_float):
        self.primative_float = primative_float
    def get_integer_range_1_value_with_default(self):
        return self.integer_range_1_value_with_default
    def set_integer_range_1_value_with_default(self, integer_range_1_value_with_default):
        self.integer_range_1_value_with_default = integer_range_1_value_with_default
    def validate_integer_range_1_st(self, value):
        result = True
        # Validate type integer_range_1_st, a restriction on integer_range_2_st.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, int):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (int)' % {"value": value, "lineno": lineno, })
                return False
            if value <= 4:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minExclusive restriction on integer_range_1_st' % {"value": value, "lineno": lineno} )
                result = False
            if value >= 8:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxExclusive restriction on integer_range_1_st' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_pattern_st(self, value):
        result = True
        # Validate type pattern_st, a restriction on pattern_1_st.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) < 10:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on pattern_st' % {"value" : value, "lineno": lineno} )
                result = False
            if not self.gds_validate_simple_patterns(
                    self.validate_pattern_st_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_pattern_st_patterns_, ))
                result = False
        return result
    validate_pattern_st_patterns_ = [['^(aaa.*zzz)$', '^(bbb.*xxx)$'], ['^(.*123.*)$', '^(.*456.*)$']]
    def validate_token_enum_st(self, value):
        result = True
        # Validate type token_enum_st, a restriction on xs:NMTOKEN.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['float', 'int', 'Name', 'token']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on token_enum_st' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_integer_range_incl_st(self, value):
        result = True
        # Validate type integer_range_incl_st, a restriction on xs:integer.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, int):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (int)' % {"value": value, "lineno": lineno, })
                return False
            if value < -5:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minInclusive restriction on integer_range_incl_st' % {"value": value, "lineno": lineno} )
                result = False
            if value > 10:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxInclusive restriction on integer_range_incl_st' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_integer_range_excl_st(self, value):
        result = True
        # Validate type integer_range_excl_st, a restriction on xs:integer.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, int):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (int)' % {"value": value, "lineno": lineno, })
                return False
            if value <= -5:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minExclusive restriction on integer_range_excl_st' % {"value": value, "lineno": lineno} )
                result = False
            if value >= 10:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxExclusive restriction on integer_range_excl_st' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_min_max_length_st(self, value):
        result = True
        # Validate type min_max_length_st, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 20:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on min_max_length_st' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 10:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on min_max_length_st' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_length_st(self, value):
        result = True
        # Validate type length_st, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) != 10:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on length_st' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_totalDigits_st(self, value):
        result = True
        # Validate type totalDigits_st, a restriction on xs:decimal.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, decimal_.Decimal):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (decimal_.Decimal)' % {"value": value, "lineno": lineno, })
                return False
            if len(str(value)) >= 15:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd totalDigits restriction on totalDigits_st' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_date_minincl_st(self, value):
        result = True
        # Validate type date_minincl_st, a restriction on xs:date.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, datetime_.date):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (datetime_.date)' % {"value": value, "lineno": lineno, })
                return False
            if value < self.gds_parse_date('2015-06-01'):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minInclusive restriction on date_minincl_st' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_date_maxincl_st(self, value):
        result = True
        # Validate type date_maxincl_st, a restriction on xs:date.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, datetime_.date):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (datetime_.date)' % {"value": value, "lineno": lineno, })
                return False
            if value > self.gds_parse_date('2015-10-31'):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxInclusive restriction on date_maxincl_st' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_date_minexcl_st(self, value):
        result = True
        # Validate type date_minexcl_st, a restriction on xs:date.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, datetime_.date):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (datetime_.date)' % {"value": value, "lineno": lineno, })
                return False
            if value <= self.gds_parse_date('2015-06-01'):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minExclusive restriction on date_minexcl_st' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_date_maxexcl_st(self, value):
        result = True
        # Validate type date_maxexcl_st, a restriction on xs:date.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, datetime_.date):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (datetime_.date)' % {"value": value, "lineno": lineno, })
                return False
            if value >= self.gds_parse_date('2015-10-31'):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxExclusive restriction on date_maxexcl_st' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_time_minincl_st(self, value):
        result = True
        # Validate type time_minincl_st, a restriction on xs:time.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, datetime_.time):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (datetime_.time)' % {"value": value, "lineno": lineno, })
                return False
            if value < self.gds_parse_time('14:20:10'):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minInclusive restriction on time_minincl_st' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_time_maxincl_st(self, value):
        result = True
        # Validate type time_maxincl_st, a restriction on xs:time.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, datetime_.time):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (datetime_.time)' % {"value": value, "lineno": lineno, })
                return False
            if value > self.gds_parse_time('16:20:10'):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxInclusive restriction on time_maxincl_st' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_time_minexcl_st(self, value):
        result = True
        # Validate type time_minexcl_st, a restriction on xs:time.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, datetime_.time):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (datetime_.time)' % {"value": value, "lineno": lineno, })
                return False
            if value <= self.gds_parse_time('14:20:10'):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minExclusive restriction on time_minexcl_st' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_time_maxexcl_st(self, value):
        result = True
        # Validate type time_maxexcl_st, a restriction on xs:time.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, datetime_.time):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (datetime_.time)' % {"value": value, "lineno": lineno, })
                return False
            if value >= self.gds_parse_time('16:20:10'):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxExclusive restriction on time_maxexcl_st' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_datetime_minincl_st(self, value):
        result = True
        # Validate type datetime_minincl_st, a restriction on xs:dateTime.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, datetime_.datetime):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (datetime_.datetime)' % {"value": value, "lineno": lineno, })
                return False
            if value < self.gds_parse_datetime('2015-06-01T14:20:10'):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minInclusive restriction on datetime_minincl_st' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_datetime_maxincl_st(self, value):
        result = True
        # Validate type datetime_maxincl_st, a restriction on xs:dateTime.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, datetime_.datetime):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (datetime_.datetime)' % {"value": value, "lineno": lineno, })
                return False
            if value > self.gds_parse_datetime('2015-10-31T16:20:10'):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxInclusive restriction on datetime_maxincl_st' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_datetime_minexcl_st(self, value):
        result = True
        # Validate type datetime_minexcl_st, a restriction on xs:dateTime.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, datetime_.datetime):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (datetime_.datetime)' % {"value": value, "lineno": lineno, })
                return False
            if value <= self.gds_parse_datetime('2015-06-01T14:20:10'):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minExclusive restriction on datetime_minexcl_st' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_datetime_maxexcl_st(self, value):
        result = True
        # Validate type datetime_maxexcl_st, a restriction on xs:dateTime.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, datetime_.datetime):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (datetime_.datetime)' % {"value": value, "lineno": lineno, })
                return False
            if value >= self.gds_parse_datetime('2015-10-31T16:20:10'):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxExclusive restriction on datetime_maxexcl_st' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_vbar_pattern_st(self, value):
        result = True
        # Validate type vbar_pattern_st, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_vbar_pattern_st_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_vbar_pattern_st_patterns_, ))
                result = False
        return result
    validate_vbar_pattern_st_patterns_ = [['^(abcd|ef\\|gh)$']]
    def validate_unicode_pattern_st(self, value):
        result = True
        # Validate type unicode_pattern_st, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_unicode_pattern_st_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_unicode_pattern_st_patterns_, ))
                result = False
        return result
    validate_unicode_pattern_st_patterns_ = [['^(abçd|ef\\|gh)$']]
    def validate_gyear_minincl_st(self, value):
        result = True
        # Validate type gyear_minincl_st, a restriction on xs:gYear.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if value < '2015':
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minInclusive restriction on gyear_minincl_st' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_gyearmonth_minincl_st(self, value):
        result = True
        # Validate type gyearmonth_minincl_st, a restriction on xs:gYearMonth.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if value < '2015-06':
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minInclusive restriction on gyearmonth_minincl_st' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_integer_range_A_0_st(self, value):
        result = True
        # Validate type integer_range_A_0_st, a restriction on namespaceA:integer_range_A_1_st.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, int):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (int)' % {"value": value, "lineno": lineno, })
                return False
            if value < 4:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minInclusive restriction on integer_range_A_0_st' % {"value": value, "lineno": lineno} )
                result = False
            if value > 6:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxInclusive restriction on integer_range_A_0_st' % {"value": value, "lineno": lineno} )
                result = False
            if value < 2:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minInclusive restriction on integer_range_A_0_st' % {"value": value, "lineno": lineno} )
                result = False
            if value > 8:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxInclusive restriction on integer_range_A_0_st' % {"value": value, "lineno": lineno} )
                result = False
            if value < 0:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minInclusive restriction on integer_range_A_0_st' % {"value": value, "lineno": lineno} )
                result = False
            if value > 10:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxInclusive restriction on integer_range_A_0_st' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_integer_range_A_1_st(self, value):
        result = True
        # Validate type integer_range_A_1_st, a restriction on namespaceA:integer_range_A_2_st.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, int):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (int)' % {"value": value, "lineno": lineno, })
                return False
            if value < 2:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minInclusive restriction on integer_range_A_1_st' % {"value": value, "lineno": lineno} )
                result = False
            if value > 8:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxInclusive restriction on integer_range_A_1_st' % {"value": value, "lineno": lineno} )
                result = False
            if value < 0:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minInclusive restriction on integer_range_A_1_st' % {"value": value, "lineno": lineno} )
                result = False
            if value > 10:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxInclusive restriction on integer_range_A_1_st' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_integer_range_A_2_st(self, value):
        result = True
        # Validate type integer_range_A_2_st, a restriction on xs:integer.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, int):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (int)' % {"value": value, "lineno": lineno, })
                return False
            if value < 0:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minInclusive restriction on integer_range_A_2_st' % {"value": value, "lineno": lineno} )
                result = False
            if value > 10:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxInclusive restriction on integer_range_A_2_st' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_anonymous_float_valueType(self, value):
        result = True
        # Validate type anonymous_float_valueType, a restriction on xs:float.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, float):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (float)' % {"value": value, "lineno": lineno, })
                return False
            if value < 1.1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minInclusive restriction on anonymous_float_valueType' % {"value": value, "lineno": lineno} )
                result = False
            if value > 4.4:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxInclusive restriction on anonymous_float_valueType' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.integer_range_1_value != 5 or
            self.pattern_value is not None or
            self.token_enum_value is not None or
            self.integer_range_incl_value is not None or
            self.integer_range_excl_value is not None or
            self.min_max_length_value is not None or
            self.length_value is not None or
            self.totalDigits_value is not None or
            self.date_minincl_value is not None or
            self.date_maxincl_value is not None or
            self.date_minexcl_value is not None or
            self.date_maxexcl_value is not None or
            self.time_minincl_value is not None or
            self.time_maxincl_value is not None or
            self.time_minexcl_value is not None or
            self.time_maxexcl_value is not None or
            self.datetime_minincl_value is not None or
            self.datetime_maxincl_value is not None or
            self.datetime_minexcl_value is not None or
            self.datetime_maxexcl_value is not None or
            self.vbar_pattern_value is not None or
            self.unicode_pattern_value is not None or
            self.gyear_minincl_value is not None or
            self.gyearmonth_minincl_value is not None or
            self.simpletype0 is not None or
            self.simpletype1 is not None or
            self.simpletype2 is not None or
            self.simpletype0a is not None or
            self.simpletype1a is not None or
            self.simpletype2a is not None or
            self.anonymous_float_value is not None or
            self.primative_integer is not None or
            self.primative_float is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_=' xmlns:namespaceA="http://www.someplace.org/namespaceA" ', name_='simpleOneType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('simpleOneType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'simpleOneType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='simpleOneType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='simpleOneType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='simpleOneType'):
        if self.integer_range_1_value_with_default != "6" and 'integer_range_1_value_with_default' not in already_processed:
            already_processed.add('integer_range_1_value_with_default')
            outfile.write(' integer_range_1_value_with_default=%s' % (quote_attrib(self.integer_range_1_value_with_default), ))
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_=' xmlns:namespaceA="http://www.someplace.org/namespaceA" ', name_='simpleOneType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.integer_range_1_value is not None:
            namespaceprefix_ = self.integer_range_1_value_nsprefix_ + ':' if (UseCapturedNS_ and self.integer_range_1_value_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sinteger_range_1_value>%s</%sinteger_range_1_value>%s' % (namespaceprefix_ , self.gds_format_integer(self.integer_range_1_value, input_name='integer_range_1_value'), namespaceprefix_ , eol_))
        if self.pattern_value is not None:
            namespaceprefix_ = self.pattern_value_nsprefix_ + ':' if (UseCapturedNS_ and self.pattern_value_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%spattern_value>%s</%spattern_value>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.pattern_value), input_name='pattern_value')), namespaceprefix_ , eol_))
        if self.token_enum_value is not None:
            namespaceprefix_ = self.token_enum_value_nsprefix_ + ':' if (UseCapturedNS_ and self.token_enum_value_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%stoken_enum_value>%s</%stoken_enum_value>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.token_enum_value), input_name='token_enum_value')), namespaceprefix_ , eol_))
        if self.integer_range_incl_value is not None:
            namespaceprefix_ = self.integer_range_incl_value_nsprefix_ + ':' if (UseCapturedNS_ and self.integer_range_incl_value_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sinteger_range_incl_value>%s</%sinteger_range_incl_value>%s' % (namespaceprefix_ , self.gds_format_integer(self.integer_range_incl_value, input_name='integer_range_incl_value'), namespaceprefix_ , eol_))
        if self.integer_range_excl_value is not None:
            namespaceprefix_ = self.integer_range_excl_value_nsprefix_ + ':' if (UseCapturedNS_ and self.integer_range_excl_value_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sinteger_range_excl_value>%s</%sinteger_range_excl_value>%s' % (namespaceprefix_ , self.gds_format_integer(self.integer_range_excl_value, input_name='integer_range_excl_value'), namespaceprefix_ , eol_))
        if self.min_max_length_value is not None:
            namespaceprefix_ = self.min_max_length_value_nsprefix_ + ':' if (UseCapturedNS_ and self.min_max_length_value_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%smin_max_length_value>%s</%smin_max_length_value>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.min_max_length_value), input_name='min_max_length_value')), namespaceprefix_ , eol_))
        if self.length_value is not None:
            namespaceprefix_ = self.length_value_nsprefix_ + ':' if (UseCapturedNS_ and self.length_value_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%slength_value>%s</%slength_value>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.length_value), input_name='length_value')), namespaceprefix_ , eol_))
        if self.totalDigits_value is not None:
            namespaceprefix_ = self.totalDigits_value_nsprefix_ + ':' if (UseCapturedNS_ and self.totalDigits_value_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%stotalDigits_value>%s</%stotalDigits_value>%s' % (namespaceprefix_ , self.gds_format_decimal(self.totalDigits_value, input_name='totalDigits_value'), namespaceprefix_ , eol_))
        if self.date_minincl_value is not None:
            namespaceprefix_ = self.date_minincl_value_nsprefix_ + ':' if (UseCapturedNS_ and self.date_minincl_value_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sdate_minincl_value>%s</%sdate_minincl_value>%s' % (namespaceprefix_ , self.gds_format_date(self.date_minincl_value, input_name='date_minincl_value'), namespaceprefix_ , eol_))
        if self.date_maxincl_value is not None:
            namespaceprefix_ = self.date_maxincl_value_nsprefix_ + ':' if (UseCapturedNS_ and self.date_maxincl_value_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sdate_maxincl_value>%s</%sdate_maxincl_value>%s' % (namespaceprefix_ , self.gds_format_date(self.date_maxincl_value, input_name='date_maxincl_value'), namespaceprefix_ , eol_))
        if self.date_minexcl_value is not None:
            namespaceprefix_ = self.date_minexcl_value_nsprefix_ + ':' if (UseCapturedNS_ and self.date_minexcl_value_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sdate_minexcl_value>%s</%sdate_minexcl_value>%s' % (namespaceprefix_ , self.gds_format_date(self.date_minexcl_value, input_name='date_minexcl_value'), namespaceprefix_ , eol_))
        if self.date_maxexcl_value is not None:
            namespaceprefix_ = self.date_maxexcl_value_nsprefix_ + ':' if (UseCapturedNS_ and self.date_maxexcl_value_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sdate_maxexcl_value>%s</%sdate_maxexcl_value>%s' % (namespaceprefix_ , self.gds_format_date(self.date_maxexcl_value, input_name='date_maxexcl_value'), namespaceprefix_ , eol_))
        if self.time_minincl_value is not None:
            namespaceprefix_ = self.time_minincl_value_nsprefix_ + ':' if (UseCapturedNS_ and self.time_minincl_value_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%stime_minincl_value>%s</%stime_minincl_value>%s' % (namespaceprefix_ , self.gds_format_time(self.time_minincl_value, input_name='time_minincl_value'), namespaceprefix_ , eol_))
        if self.time_maxincl_value is not None:
            namespaceprefix_ = self.time_maxincl_value_nsprefix_ + ':' if (UseCapturedNS_ and self.time_maxincl_value_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%stime_maxincl_value>%s</%stime_maxincl_value>%s' % (namespaceprefix_ , self.gds_format_time(self.time_maxincl_value, input_name='time_maxincl_value'), namespaceprefix_ , eol_))
        if self.time_minexcl_value is not None:
            namespaceprefix_ = self.time_minexcl_value_nsprefix_ + ':' if (UseCapturedNS_ and self.time_minexcl_value_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%stime_minexcl_value>%s</%stime_minexcl_value>%s' % (namespaceprefix_ , self.gds_format_time(self.time_minexcl_value, input_name='time_minexcl_value'), namespaceprefix_ , eol_))
        if self.time_maxexcl_value is not None:
            namespaceprefix_ = self.time_maxexcl_value_nsprefix_ + ':' if (UseCapturedNS_ and self.time_maxexcl_value_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%stime_maxexcl_value>%s</%stime_maxexcl_value>%s' % (namespaceprefix_ , self.gds_format_time(self.time_maxexcl_value, input_name='time_maxexcl_value'), namespaceprefix_ , eol_))
        if self.datetime_minincl_value is not None:
            namespaceprefix_ = self.datetime_minincl_value_nsprefix_ + ':' if (UseCapturedNS_ and self.datetime_minincl_value_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sdatetime_minincl_value>%s</%sdatetime_minincl_value>%s' % (namespaceprefix_ , self.gds_format_datetime(self.datetime_minincl_value, input_name='datetime_minincl_value'), namespaceprefix_ , eol_))
        if self.datetime_maxincl_value is not None:
            namespaceprefix_ = self.datetime_maxincl_value_nsprefix_ + ':' if (UseCapturedNS_ and self.datetime_maxincl_value_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sdatetime_maxincl_value>%s</%sdatetime_maxincl_value>%s' % (namespaceprefix_ , self.gds_format_datetime(self.datetime_maxincl_value, input_name='datetime_maxincl_value'), namespaceprefix_ , eol_))
        if self.datetime_minexcl_value is not None:
            namespaceprefix_ = self.datetime_minexcl_value_nsprefix_ + ':' if (UseCapturedNS_ and self.datetime_minexcl_value_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sdatetime_minexcl_value>%s</%sdatetime_minexcl_value>%s' % (namespaceprefix_ , self.gds_format_datetime(self.datetime_minexcl_value, input_name='datetime_minexcl_value'), namespaceprefix_ , eol_))
        if self.datetime_maxexcl_value is not None:
            namespaceprefix_ = self.datetime_maxexcl_value_nsprefix_ + ':' if (UseCapturedNS_ and self.datetime_maxexcl_value_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sdatetime_maxexcl_value>%s</%sdatetime_maxexcl_value>%s' % (namespaceprefix_ , self.gds_format_datetime(self.datetime_maxexcl_value, input_name='datetime_maxexcl_value'), namespaceprefix_ , eol_))
        if self.vbar_pattern_value is not None:
            namespaceprefix_ = self.vbar_pattern_value_nsprefix_ + ':' if (UseCapturedNS_ and self.vbar_pattern_value_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%svbar_pattern_value>%s</%svbar_pattern_value>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.vbar_pattern_value), input_name='vbar_pattern_value')), namespaceprefix_ , eol_))
        if self.unicode_pattern_value is not None:
            namespaceprefix_ = self.unicode_pattern_value_nsprefix_ + ':' if (UseCapturedNS_ and self.unicode_pattern_value_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sunicode_pattern_value>%s</%sunicode_pattern_value>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.unicode_pattern_value), input_name='unicode_pattern_value')), namespaceprefix_ , eol_))
        if self.gyear_minincl_value is not None:
            namespaceprefix_ = self.gyear_minincl_value_nsprefix_ + ':' if (UseCapturedNS_ and self.gyear_minincl_value_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sgyear_minincl_value>%s</%sgyear_minincl_value>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.gyear_minincl_value), input_name='gyear_minincl_value')), namespaceprefix_ , eol_))
        if self.gyearmonth_minincl_value is not None:
            namespaceprefix_ = self.gyearmonth_minincl_value_nsprefix_ + ':' if (UseCapturedNS_ and self.gyearmonth_minincl_value_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sgyearmonth_minincl_value>%s</%sgyearmonth_minincl_value>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.gyearmonth_minincl_value), input_name='gyearmonth_minincl_value')), namespaceprefix_ , eol_))
        if self.simpletype0 is not None:
            namespaceprefix_ = self.simpletype0_nsprefix_ + ':' if (UseCapturedNS_ and self.simpletype0_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%ssimpletype0>%s</%ssimpletype0>%s' % (namespaceprefix_ , self.gds_format_integer(self.simpletype0, input_name='simpletype0'), namespaceprefix_ , eol_))
        if self.simpletype1 is not None:
            namespaceprefix_ = self.simpletype1_nsprefix_ + ':' if (UseCapturedNS_ and self.simpletype1_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%ssimpletype1>%s</%ssimpletype1>%s' % (namespaceprefix_ , self.gds_format_integer(self.simpletype1, input_name='simpletype1'), namespaceprefix_ , eol_))
        if self.simpletype2 is not None:
            namespaceprefix_ = self.simpletype2_nsprefix_ + ':' if (UseCapturedNS_ and self.simpletype2_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%ssimpletype2>%s</%ssimpletype2>%s' % (namespaceprefix_ , self.gds_format_integer(self.simpletype2, input_name='simpletype2'), namespaceprefix_ , eol_))
        if self.simpletype0a is not None:
            namespaceprefix_ = self.simpletype0a_nsprefix_ + ':' if (UseCapturedNS_ and self.simpletype0a_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%ssimpletype0a>%s</%ssimpletype0a>%s' % (namespaceprefix_ , self.gds_format_integer(self.simpletype0a, input_name='simpletype0a'), namespaceprefix_ , eol_))
        if self.simpletype1a is not None:
            namespaceprefix_ = self.simpletype1a_nsprefix_ + ':' if (UseCapturedNS_ and self.simpletype1a_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%ssimpletype1a>%s</%ssimpletype1a>%s' % (namespaceprefix_ , self.gds_format_integer(self.simpletype1a, input_name='simpletype1a'), namespaceprefix_ , eol_))
        if self.simpletype2a is not None:
            namespaceprefix_ = self.simpletype2a_nsprefix_ + ':' if (UseCapturedNS_ and self.simpletype2a_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%ssimpletype2a>%s</%ssimpletype2a>%s' % (namespaceprefix_ , self.gds_format_integer(self.simpletype2a, input_name='simpletype2a'), namespaceprefix_ , eol_))
        if self.anonymous_float_value is not None:
            namespaceprefix_ = self.anonymous_float_value_nsprefix_ + ':' if (UseCapturedNS_ and self.anonymous_float_value_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sanonymous_float_value>%s</%sanonymous_float_value>%s' % (namespaceprefix_ , self.gds_format_float(self.anonymous_float_value, input_name='anonymous_float_value'), namespaceprefix_ , eol_))
        if self.primative_integer is not None:
            namespaceprefix_ = self.primative_integer_nsprefix_ + ':' if (UseCapturedNS_ and self.primative_integer_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sprimative_integer>%s</%sprimative_integer>%s' % (namespaceprefix_ , self.gds_format_integer(self.primative_integer, input_name='primative_integer'), namespaceprefix_ , eol_))
        if self.primative_float is not None:
            namespaceprefix_ = self.primative_float_nsprefix_ + ':' if (UseCapturedNS_ and self.primative_float_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sprimative_float>%s</%sprimative_float>%s' % (namespaceprefix_ , self.gds_format_float(self.primative_float, input_name='primative_float'), namespaceprefix_ , eol_))
    def validate_(self, gds_collector, recursive=False):
        self.gds_collector_ = gds_collector
        message_count = len(self.gds_collector_.get_messages())
        # validate simple type attributes
        self.gds_validate_defined_ST_(self.validate_integer_range_1_st, self.integer_range_1_value_with_default, 'integer_range_1_value_with_default')
        self.gds_check_cardinality_(self.integer_range_1_value_with_default, 'integer_range_1_value_with_default', required=False)
        # validate simple type children
        self.gds_validate_defined_ST_(self.validate_integer_range_1_st, self.integer_range_1_value, 'integer_range_1_value')
        self.gds_check_cardinality_(self.integer_range_1_value, 'integer_range_1_value', min_occurs=1, max_occurs=1)
        self.gds_validate_defined_ST_(self.validate_pattern_st, self.pattern_value, 'pattern_value')
        self.gds_check_cardinality_(self.pattern_value, 'pattern_value', min_occurs=1, max_occurs=1)
        self.gds_validate_defined_ST_(self.validate_token_enum_st, self.token_enum_value, 'token_enum_value')
        self.gds_check_cardinality_(self.token_enum_value, 'token_enum_value', min_occurs=1, max_occurs=1)
        self.gds_validate_defined_ST_(self.validate_integer_range_incl_st, self.integer_range_incl_value, 'integer_range_incl_value')
        self.gds_check_cardinality_(self.integer_range_incl_value, 'integer_range_incl_value', min_occurs=1, max_occurs=1)
        self.gds_validate_defined_ST_(self.validate_integer_range_excl_st, self.integer_range_excl_value, 'integer_range_excl_value')
        self.gds_check_cardinality_(self.integer_range_excl_value, 'integer_range_excl_value', min_occurs=1, max_occurs=1)
        self.gds_validate_defined_ST_(self.validate_min_max_length_st, self.min_max_length_value, 'min_max_length_value')
        self.gds_check_cardinality_(self.min_max_length_value, 'min_max_length_value', min_occurs=1, max_occurs=1)
        self.gds_validate_defined_ST_(self.validate_length_st, self.length_value, 'length_value')
        self.gds_check_cardinality_(self.length_value, 'length_value', min_occurs=1, max_occurs=1)
        self.gds_validate_defined_ST_(self.validate_totalDigits_st, self.totalDigits_value, 'totalDigits_value')
        self.gds_check_cardinality_(self.totalDigits_value, 'totalDigits_value', min_occurs=1, max_occurs=1)
        self.gds_validate_defined_ST_(self.validate_date_minincl_st, self.date_minincl_value, 'date_minincl_value')
        self.gds_check_cardinality_(self.date_minincl_value, 'date_minincl_value', min_occurs=1, max_occurs=1)
        self.gds_validate_defined_ST_(self.validate_date_maxincl_st, self.date_maxincl_value, 'date_maxincl_value')
        self.gds_check_cardinality_(self.date_maxincl_value, 'date_maxincl_value', min_occurs=1, max_occurs=1)
        self.gds_validate_defined_ST_(self.validate_date_minexcl_st, self.date_minexcl_value, 'date_minexcl_value')
        self.gds_check_cardinality_(self.date_minexcl_value, 'date_minexcl_value', min_occurs=1, max_occurs=1)
        self.gds_validate_defined_ST_(self.validate_date_maxexcl_st, self.date_maxexcl_value, 'date_maxexcl_value')
        self.gds_check_cardinality_(self.date_maxexcl_value, 'date_maxexcl_value', min_occurs=1, max_occurs=1)
        self.gds_validate_defined_ST_(self.validate_time_minincl_st, self.time_minincl_value, 'time_minincl_value')
        self.gds_check_cardinality_(self.time_minincl_value, 'time_minincl_value', min_occurs=1, max_occurs=1)
        self.gds_validate_defined_ST_(self.validate_time_maxincl_st, self.time_maxincl_value, 'time_maxincl_value')
        self.gds_check_cardinality_(self.time_maxincl_value, 'time_maxincl_value', min_occurs=1, max_occurs=1)
        self.gds_validate_defined_ST_(self.validate_time_minexcl_st, self.time_minexcl_value, 'time_minexcl_value')
        self.gds_check_cardinality_(self.time_minexcl_value, 'time_minexcl_value', min_occurs=1, max_occurs=1)
        self.gds_validate_defined_ST_(self.validate_time_maxexcl_st, self.time_maxexcl_value, 'time_maxexcl_value')
        self.gds_check_cardinality_(self.time_maxexcl_value, 'time_maxexcl_value', min_occurs=1, max_occurs=1)
        self.gds_validate_defined_ST_(self.validate_datetime_minincl_st, self.datetime_minincl_value, 'datetime_minincl_value')
        self.gds_check_cardinality_(self.datetime_minincl_value, 'datetime_minincl_value', min_occurs=1, max_occurs=1)
        self.gds_validate_defined_ST_(self.validate_datetime_maxincl_st, self.datetime_maxincl_value, 'datetime_maxincl_value')
        self.gds_check_cardinality_(self.datetime_maxincl_value, 'datetime_maxincl_value', min_occurs=1, max_occurs=1)
        self.gds_validate_defined_ST_(self.validate_datetime_minexcl_st, self.datetime_minexcl_value, 'datetime_minexcl_value')
        self.gds_check_cardinality_(self.datetime_minexcl_value, 'datetime_minexcl_value', min_occurs=1, max_occurs=1)
        self.gds_validate_defined_ST_(self.validate_datetime_maxexcl_st, self.datetime_maxexcl_value, 'datetime_maxexcl_value')
        self.gds_check_cardinality_(self.datetime_maxexcl_value, 'datetime_maxexcl_value', min_occurs=1, max_occurs=1)
        self.gds_validate_defined_ST_(self.validate_vbar_pattern_st, self.vbar_pattern_value, 'vbar_pattern_value')
        self.gds_check_cardinality_(self.vbar_pattern_value, 'vbar_pattern_value', min_occurs=1, max_occurs=1)
        self.gds_validate_defined_ST_(self.validate_unicode_pattern_st, self.unicode_pattern_value, 'unicode_pattern_value')
        self.gds_check_cardinality_(self.unicode_pattern_value, 'unicode_pattern_value', min_occurs=1, max_occurs=1)
        self.gds_validate_defined_ST_(self.validate_gyear_minincl_st, self.gyear_minincl_value, 'gyear_minincl_value')
        self.gds_check_cardinality_(self.gyear_minincl_value, 'gyear_minincl_value', min_occurs=1, max_occurs=1)
        self.gds_validate_defined_ST_(self.validate_gyearmonth_minincl_st, self.gyearmonth_minincl_value, 'gyearmonth_minincl_value')
        self.gds_check_cardinality_(self.gyearmonth_minincl_value, 'gyearmonth_minincl_value', min_occurs=1, max_occurs=1)
        self.gds_validate_defined_ST_(self.validate_integer_range_A_0_st, self.simpletype0, 'simpletype0')
        self.gds_check_cardinality_(self.simpletype0, 'simpletype0', min_occurs=1, max_occurs=1)
        self.gds_validate_defined_ST_(self.validate_integer_range_A_1_st, self.simpletype1, 'simpletype1')
        self.gds_check_cardinality_(self.simpletype1, 'simpletype1', min_occurs=1, max_occurs=1)
        self.gds_validate_defined_ST_(self.validate_integer_range_A_2_st, self.simpletype2, 'simpletype2')
        self.gds_check_cardinality_(self.simpletype2, 'simpletype2', min_occurs=1, max_occurs=1)
        self.gds_validate_defined_ST_(self.validate_integer_range_A_0_st, self.simpletype0a, 'simpletype0a')
        self.gds_check_cardinality_(self.simpletype0a, 'simpletype0a', min_occurs=1, max_occurs=1)
        self.gds_validate_defined_ST_(self.validate_integer_range_A_1_st, self.simpletype1a, 'simpletype1a')
        self.gds_check_cardinality_(self.simpletype1a, 'simpletype1a', min_occurs=1, max_occurs=1)
        self.gds_validate_defined_ST_(self.validate_integer_range_A_2_st, self.simpletype2a, 'simpletype2a')
        self.gds_check_cardinality_(self.simpletype2a, 'simpletype2a', min_occurs=1, max_occurs=1)
        self.gds_validate_defined_ST_(self.validate_anonymous_float_valueType, self.anonymous_float_value, 'anonymous_float_value')
        self.gds_check_cardinality_(self.anonymous_float_value, 'anonymous_float_value', min_occurs=1, max_occurs=1)
        self.gds_validate_builtin_ST_(self.gds_validate_integer, self.primative_integer, 'primative_integer')
        self.gds_check_cardinality_(self.primative_integer, 'primative_integer', min_occurs=1, max_occurs=1)
        self.gds_validate_builtin_ST_(self.gds_validate_float, self.primative_float, 'primative_float')
        self.gds_check_cardinality_(self.primative_float, 'primative_float', min_occurs=1, max_occurs=1)
        # validate complex type children
        if recursive:
            pass
        return message_count == len(self.gds_collector_.get_messages())
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        value = find_attr_value_('integer_range_1_value_with_default', node)
        if value is not None and 'integer_range_1_value_with_default' not in already_processed:
            already_processed.add('integer_range_1_value_with_default')
            self.integer_range_1_value_with_default = value
            self.validate_integer_range_1_st(self.integer_range_1_value_with_default)    # validate type integer_range_1_st
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'integer_range_1_value' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'integer_range_1_value')
            ival_ = self.gds_validate_integer(ival_, node, 'integer_range_1_value')
            self.integer_range_1_value = ival_
            self.integer_range_1_value_nsprefix_ = child_.prefix
            # validate type integer_range_1_st
            self.validate_integer_range_1_st(self.integer_range_1_value)
        elif nodeName_ == 'pattern_value':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'pattern_value')
            value_ = self.gds_validate_string(value_, node, 'pattern_value')
            self.pattern_value = value_
            self.pattern_value_nsprefix_ = child_.prefix
            # validate type pattern_st
            self.validate_pattern_st(self.pattern_value)
        elif nodeName_ == 'token_enum_value':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'token_enum_value')
            value_ = self.gds_validate_string(value_, node, 'token_enum_value')
            self.token_enum_value = value_
            self.token_enum_value_nsprefix_ = child_.prefix
            # validate type token_enum_st
            self.validate_token_enum_st(self.token_enum_value)
        elif nodeName_ == 'integer_range_incl_value' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'integer_range_incl_value')
            ival_ = self.gds_validate_integer(ival_, node, 'integer_range_incl_value')
            self.integer_range_incl_value = ival_
            self.integer_range_incl_value_nsprefix_ = child_.prefix
            # validate type integer_range_incl_st
            self.validate_integer_range_incl_st(self.integer_range_incl_value)
        elif nodeName_ == 'integer_range_excl_value' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'integer_range_excl_value')
            ival_ = self.gds_validate_integer(ival_, node, 'integer_range_excl_value')
            self.integer_range_excl_value = ival_
            self.integer_range_excl_value_nsprefix_ = child_.prefix
            # validate type integer_range_excl_st
            self.validate_integer_range_excl_st(self.integer_range_excl_value)
        elif nodeName_ == 'min_max_length_value':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'min_max_length_value')
            value_ = self.gds_validate_string(value_, node, 'min_max_length_value')
            self.min_max_length_value = value_
            self.min_max_length_value_nsprefix_ = child_.prefix
            # validate type min_max_length_st
            self.validate_min_max_length_st(self.min_max_length_value)
        elif nodeName_ == 'length_value':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'length_value')
            value_ = self.gds_validate_string(value_, node, 'length_value')
            self.length_value = value_
            self.length_value_nsprefix_ = child_.prefix
            # validate type length_st
            self.validate_length_st(self.length_value)
        elif nodeName_ == 'totalDigits_value' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'totalDigits_value')
            fval_ = self.gds_validate_decimal(fval_, node, 'totalDigits_value')
            self.totalDigits_value = fval_
            self.totalDigits_value_nsprefix_ = child_.prefix
            # validate type totalDigits_st
            self.validate_totalDigits_st(self.totalDigits_value)
        elif nodeName_ == 'date_minincl_value':
            sval_ = child_.text
            dval_ = self.gds_parse_date(sval_)
            self.date_minincl_value = dval_
            self.date_minincl_value_nsprefix_ = child_.prefix
            # validate type date_minincl_st
            self.validate_date_minincl_st(self.date_minincl_value)
        elif nodeName_ == 'date_maxincl_value':
            sval_ = child_.text
            dval_ = self.gds_parse_date(sval_)
            self.date_maxincl_value = dval_
            self.date_maxincl_value_nsprefix_ = child_.prefix
            # validate type date_maxincl_st
            self.validate_date_maxincl_st(self.date_maxincl_value)
        elif nodeName_ == 'date_minexcl_value':
            sval_ = child_.text
            dval_ = self.gds_parse_date(sval_)
            self.date_minexcl_value = dval_
            self.date_minexcl_value_nsprefix_ = child_.prefix
            # validate type date_minexcl_st
            self.validate_date_minexcl_st(self.date_minexcl_value)
        elif nodeName_ == 'date_maxexcl_value':
            sval_ = child_.text
            dval_ = self.gds_parse_date(sval_)
            self.date_maxexcl_value = dval_
            self.date_maxexcl_value_nsprefix_ = child_.prefix
            # validate type date_maxexcl_st
            self.validate_date_maxexcl_st(self.date_maxexcl_value)
        elif nodeName_ == 'time_minincl_value':
            sval_ = child_.text
            dval_ = self.gds_parse_time(sval_)
            self.time_minincl_value = dval_
            self.time_minincl_value_nsprefix_ = child_.prefix
            # validate type time_minincl_st
            self.validate_time_minincl_st(self.time_minincl_value)
        elif nodeName_ == 'time_maxincl_value':
            sval_ = child_.text
            dval_ = self.gds_parse_time(sval_)
            self.time_maxincl_value = dval_
            self.time_maxincl_value_nsprefix_ = child_.prefix
            # validate type time_maxincl_st
            self.validate_time_maxincl_st(self.time_maxincl_value)
        elif nodeName_ == 'time_minexcl_value':
            sval_ = child_.text
            dval_ = self.gds_parse_time(sval_)
            self.time_minexcl_value = dval_
            self.time_minexcl_value_nsprefix_ = child_.prefix
            # validate type time_minexcl_st
            self.validate_time_minexcl_st(self.time_minexcl_value)
        elif nodeName_ == 'time_maxexcl_value':
            sval_ = child_.text
            dval_ = self.gds_parse_time(sval_)
            self.time_maxexcl_value = dval_
            self.time_maxexcl_value_nsprefix_ = child_.prefix
            # validate type time_maxexcl_st
            self.validate_time_maxexcl_st(self.time_maxexcl_value)
        elif nodeName_ == 'datetime_minincl_value':
            sval_ = child_.text
            dval_ = self.gds_parse_datetime(sval_)
            self.datetime_minincl_value = dval_
            self.datetime_minincl_value_nsprefix_ = child_.prefix
            # validate type datetime_minincl_st
            self.validate_datetime_minincl_st(self.datetime_minincl_value)
        elif nodeName_ == 'datetime_maxincl_value':
            sval_ = child_.text
            dval_ = self.gds_parse_datetime(sval_)
            self.datetime_maxincl_value = dval_
            self.datetime_maxincl_value_nsprefix_ = child_.prefix
            # validate type datetime_maxincl_st
            self.validate_datetime_maxincl_st(self.datetime_maxincl_value)
        elif nodeName_ == 'datetime_minexcl_value':
            sval_ = child_.text
            dval_ = self.gds_parse_datetime(sval_)
            self.datetime_minexcl_value = dval_
            self.datetime_minexcl_value_nsprefix_ = child_.prefix
            # validate type datetime_minexcl_st
            self.validate_datetime_minexcl_st(self.datetime_minexcl_value)
        elif nodeName_ == 'datetime_maxexcl_value':
            sval_ = child_.text
            dval_ = self.gds_parse_datetime(sval_)
            self.datetime_maxexcl_value = dval_
            self.datetime_maxexcl_value_nsprefix_ = child_.prefix
            # validate type datetime_maxexcl_st
            self.validate_datetime_maxexcl_st(self.datetime_maxexcl_value)
        elif nodeName_ == 'vbar_pattern_value':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'vbar_pattern_value')
            value_ = self.gds_validate_string(value_, node, 'vbar_pattern_value')
            self.vbar_pattern_value = value_
            self.vbar_pattern_value_nsprefix_ = child_.prefix
            # validate type vbar_pattern_st
            self.validate_vbar_pattern_st(self.vbar_pattern_value)
        elif nodeName_ == 'unicode_pattern_value':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'unicode_pattern_value')
            value_ = self.gds_validate_string(value_, node, 'unicode_pattern_value')
            self.unicode_pattern_value = value_
            self.unicode_pattern_value_nsprefix_ = child_.prefix
            # validate type unicode_pattern_st
            self.validate_unicode_pattern_st(self.unicode_pattern_value)
        elif nodeName_ == 'gyear_minincl_value':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'gyear_minincl_value')
            value_ = self.gds_validate_string(value_, node, 'gyear_minincl_value')
            self.gyear_minincl_value = value_
            self.gyear_minincl_value_nsprefix_ = child_.prefix
            # validate type gyear_minincl_st
            self.validate_gyear_minincl_st(self.gyear_minincl_value)
        elif nodeName_ == 'gyearmonth_minincl_value':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'gyearmonth_minincl_value')
            value_ = self.gds_validate_string(value_, node, 'gyearmonth_minincl_value')
            self.gyearmonth_minincl_value = value_
            self.gyearmonth_minincl_value_nsprefix_ = child_.prefix
            # validate type gyearmonth_minincl_st
            self.validate_gyearmonth_minincl_st(self.gyearmonth_minincl_value)
        elif nodeName_ == 'simpletype0' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'simpletype0')
            ival_ = self.gds_validate_integer(ival_, node, 'simpletype0')
            self.simpletype0 = ival_
            self.simpletype0_nsprefix_ = child_.prefix
            # validate type integer_range_A_0_st
            self.validate_integer_range_A_0_st(self.simpletype0)
        elif nodeName_ == 'simpletype1' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'simpletype1')
            ival_ = self.gds_validate_integer(ival_, node, 'simpletype1')
            self.simpletype1 = ival_
            self.simpletype1_nsprefix_ = child_.prefix
            # validate type integer_range_A_1_st
            self.validate_integer_range_A_1_st(self.simpletype1)
        elif nodeName_ == 'simpletype2' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'simpletype2')
            ival_ = self.gds_validate_integer(ival_, node, 'simpletype2')
            self.simpletype2 = ival_
            self.simpletype2_nsprefix_ = child_.prefix
            # validate type integer_range_A_2_st
            self.validate_integer_range_A_2_st(self.simpletype2)
        elif nodeName_ == 'simpletype0a' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'simpletype0a')
            ival_ = self.gds_validate_integer(ival_, node, 'simpletype0a')
            self.simpletype0a = ival_
            self.simpletype0a_nsprefix_ = child_.prefix
            # validate type integer_range_A_0_st
            self.validate_integer_range_A_0_st(self.simpletype0a)
        elif nodeName_ == 'simpletype1a' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'simpletype1a')
            ival_ = self.gds_validate_integer(ival_, node, 'simpletype1a')
            self.simpletype1a = ival_
            self.simpletype1a_nsprefix_ = child_.prefix
            # validate type integer_range_A_1_st
            self.validate_integer_range_A_1_st(self.simpletype1a)
        elif nodeName_ == 'simpletype2a' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'simpletype2a')
            ival_ = self.gds_validate_integer(ival_, node, 'simpletype2a')
            self.simpletype2a = ival_
            self.simpletype2a_nsprefix_ = child_.prefix
            # validate type integer_range_A_2_st
            self.validate_integer_range_A_2_st(self.simpletype2a)
        elif nodeName_ == 'anonymous_float_value' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_float(sval_, node, 'anonymous_float_value')
            fval_ = self.gds_validate_float(fval_, node, 'anonymous_float_value')
            self.anonymous_float_value = fval_
            self.anonymous_float_value_nsprefix_ = child_.prefix
            # validate type anonymous_float_valueType
            self.validate_anonymous_float_valueType(self.anonymous_float_value)
        elif nodeName_ == 'primative_integer' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'primative_integer')
            ival_ = self.gds_validate_integer(ival_, node, 'primative_integer')
            self.primative_integer = ival_
            self.primative_integer_nsprefix_ = child_.prefix
        elif nodeName_ == 'primative_float' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_float(sval_, node, 'primative_float')
            fval_ = self.gds_validate_float(fval_, node, 'primative_float')
            self.primative_float = fval_
            self.primative_float_nsprefix_ = child_.prefix
# end class simpleOneType


class simpleTwoType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    member_data_items_ = [
        MemberSpec_('simpleTwoElementOne', 'simpleTwoElementOneType', 0, 0, {'name': 'simpleTwoElementOne', 'type': 'simpleTwoElementOneType'}, None),
    ]
    subclass = None
    superclass = None
    def __init__(self, simpleTwoElementOne=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.simpleTwoElementOne = simpleTwoElementOne
        self.simpleTwoElementOne_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, simpleTwoType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if simpleTwoType.subclass:
            return simpleTwoType.subclass(*args_, **kwargs_)
        else:
            return simpleTwoType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_simpleTwoElementOne(self):
        return self.simpleTwoElementOne
    def set_simpleTwoElementOne(self, simpleTwoElementOne):
        self.simpleTwoElementOne = simpleTwoElementOne
    def hasContent_(self):
        if (
            self.simpleTwoElementOne is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='simpleTwoType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('simpleTwoType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'simpleTwoType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='simpleTwoType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='simpleTwoType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='simpleTwoType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='simpleTwoType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.simpleTwoElementOne is not None:
            namespaceprefix_ = self.simpleTwoElementOne_nsprefix_ + ':' if (UseCapturedNS_ and self.simpleTwoElementOne_nsprefix_) else ''
            self.simpleTwoElementOne.export(outfile, level, namespaceprefix_, namespacedef_='', name_='simpleTwoElementOne', pretty_print=pretty_print)
    def validate_(self, gds_collector, recursive=False):
        self.gds_collector_ = gds_collector
        message_count = len(self.gds_collector_.get_messages())
        # validate simple type attributes
        # validate simple type children
        # validate complex type children
        self.gds_check_cardinality_(self.simpleTwoElementOne, 'simpleTwoElementOne', min_occurs=1, max_occurs=1)
        if recursive:
            if self.simpleTwoElementOne is not None:
                self.simpleTwoElementOne.validate_(gds_collector, recursive=True)
        return message_count == len(self.gds_collector_.get_messages())
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'simpleTwoElementOne':
            obj_ = simpleTwoElementOneType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.simpleTwoElementOne = obj_
            obj_.original_tagname_ = 'simpleTwoElementOne'
# end class simpleTwoType


class simpleTwoElementOneType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    member_data_items_ = [
        MemberSpec_('simpleTwoElementTwo', ['simpleTwoElementTwoType', 'xs:string'], 0, 0, {'name': 'simpleTwoElementTwo', 'type': 'xs:string'}, None),
    ]
    subclass = None
    superclass = None
    def __init__(self, simpleTwoElementTwo=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.simpleTwoElementTwo = simpleTwoElementTwo
        self.validate_simpleTwoElementTwoType(self.simpleTwoElementTwo)
        self.simpleTwoElementTwo_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, simpleTwoElementOneType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if simpleTwoElementOneType.subclass:
            return simpleTwoElementOneType.subclass(*args_, **kwargs_)
        else:
            return simpleTwoElementOneType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_simpleTwoElementTwo(self):
        return self.simpleTwoElementTwo
    def set_simpleTwoElementTwo(self, simpleTwoElementTwo):
        self.simpleTwoElementTwo = simpleTwoElementTwo
    def validate_simpleTwoElementTwoType(self, value):
        result = True
        # Validate type simpleTwoElementTwoType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 24:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on simpleTwoElementTwoType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 12:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on simpleTwoElementTwoType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.simpleTwoElementTwo is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='simpleTwoElementOneType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('simpleTwoElementOneType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'simpleTwoElementOneType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='simpleTwoElementOneType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='simpleTwoElementOneType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='simpleTwoElementOneType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='simpleTwoElementOneType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.simpleTwoElementTwo is not None:
            namespaceprefix_ = self.simpleTwoElementTwo_nsprefix_ + ':' if (UseCapturedNS_ and self.simpleTwoElementTwo_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%ssimpleTwoElementTwo>%s</%ssimpleTwoElementTwo>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.simpleTwoElementTwo), input_name='simpleTwoElementTwo')), namespaceprefix_ , eol_))
    def validate_(self, gds_collector, recursive=False):
        self.gds_collector_ = gds_collector
        message_count = len(self.gds_collector_.get_messages())
        # validate simple type attributes
        # validate simple type children
        self.gds_validate_defined_ST_(self.validate_simpleTwoElementTwoType, self.simpleTwoElementTwo, 'simpleTwoElementTwo')
        self.gds_check_cardinality_(self.simpleTwoElementTwo, 'simpleTwoElementTwo', min_occurs=1, max_occurs=1)
        # validate complex type children
        if recursive:
            pass
        return message_count == len(self.gds_collector_.get_messages())
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'simpleTwoElementTwo':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'simpleTwoElementTwo')
            value_ = self.gds_validate_string(value_, node, 'simpleTwoElementTwo')
            self.simpleTwoElementTwo = value_
            self.simpleTwoElementTwo_nsprefix_ = child_.prefix
            # validate type simpleTwoElementTwoType
            self.validate_simpleTwoElementTwoType(self.simpleTwoElementTwo)
# end class simpleTwoElementOneType


GDSClassesMapping = {
    'container': containerType,
    'simpleTypeData': simpleTwoType,
}


USAGE_TEXT = """
Usage: python <Parser>.py [ -s ] <in_xml_file>
"""


def usage():
    print(USAGE_TEXT)
    sys.exit(1)


def get_root_tag(node):
    tag = Tag_pattern_.match(node.tag).groups()[-1]
    rootClass = GDSClassesMapping.get(tag)
    if rootClass is None:
        rootClass = globals().get(tag)
    return tag, rootClass


def get_required_ns_prefix_defs(rootNode):
    '''Get all name space prefix definitions required in this XML doc.
    Return a dictionary of definitions and a char string of definitions.
    '''
    nsmap = {
        prefix: uri
        for node in rootNode.iter()
        for (prefix, uri) in node.nsmap.items()
        if prefix is not None
    }
    namespacedefs = ' '.join([
        'xmlns:{}="{}"'.format(prefix, uri)
        for prefix, uri in nsmap.items()
    ])
    return nsmap, namespacedefs


def parse(inFileName, silence=False, print_warnings=True):
    global CapturedNsmap_
    gds_collector = GdsCollector_()
    parser = None
    doc = parsexml_(inFileName, parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'containerType'
        rootClass = containerType
    rootObj = rootClass.factory()
    rootObj.build(rootNode, gds_collector_=gds_collector)
    CapturedNsmap_, namespacedefs = get_required_ns_prefix_defs(rootNode)
    if not SaveElementTreeNode:
        doc = None
        rootNode = None
    if not silence:
        sys.stdout.write('<?xml version="1.0" ?>\n')
        rootObj.export(
            sys.stdout, 0, name_=rootTag,
            namespacedef_=namespacedefs,
            pretty_print=True)
    if print_warnings and len(gds_collector.get_messages()) > 0:
        separator = ('-' * 50) + '\n'
        sys.stderr.write(separator)
        sys.stderr.write('----- Warnings -- count: {} -----\n'.format(
            len(gds_collector.get_messages()), ))
        gds_collector.write_messages(sys.stderr)
        sys.stderr.write(separator)
    return rootObj


def parseEtree(inFileName, silence=False, print_warnings=True,
               mapping=None, nsmap=None):
    parser = None
    doc = parsexml_(inFileName, parser)
    gds_collector = GdsCollector_()
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'containerType'
        rootClass = containerType
    rootObj = rootClass.factory()
    rootObj.build(rootNode, gds_collector_=gds_collector)
    # Enable Python to collect the space used by the DOM.
    if mapping is None:
        mapping = {}
    rootElement = rootObj.to_etree(
        None, name_=rootTag, mapping_=mapping, nsmap_=nsmap)
    reverse_mapping = rootObj.gds_reverse_node_mapping(mapping)
    if not SaveElementTreeNode:
        doc = None
        rootNode = None
    if not silence:
        content = etree_.tostring(
            rootElement, pretty_print=True,
            xml_declaration=True, encoding="utf-8")
        sys.stdout.write(str(content))
        sys.stdout.write('\n')
    if print_warnings and len(gds_collector.get_messages()) > 0:
        separator = ('-' * 50) + '\n'
        sys.stderr.write(separator)
        sys.stderr.write('----- Warnings -- count: {} -----\n'.format(
            len(gds_collector.get_messages()), ))
        gds_collector.write_messages(sys.stderr)
        sys.stderr.write(separator)
    return rootObj, rootElement, mapping, reverse_mapping


def parseString(inString, silence=False, print_warnings=True):
    '''Parse a string, create the object tree, and export it.

    Arguments:
    - inString -- A string.  This XML fragment should not start
      with an XML declaration containing an encoding.
    - silence -- A boolean.  If False, export the object.
    Returns -- The root object in the tree.
    '''
    parser = None
    rootNode= parsexmlstring_(inString, parser)
    gds_collector = GdsCollector_()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'containerType'
        rootClass = containerType
    rootObj = rootClass.factory()
    rootObj.build(rootNode, gds_collector_=gds_collector)
    if not SaveElementTreeNode:
        rootNode = None
    if not silence:
        sys.stdout.write('<?xml version="1.0" ?>\n')
        rootObj.export(
            sys.stdout, 0, name_=rootTag,
            namespacedef_='')
    if print_warnings and len(gds_collector.get_messages()) > 0:
        separator = ('-' * 50) + '\n'
        sys.stderr.write(separator)
        sys.stderr.write('----- Warnings -- count: {} -----\n'.format(
            len(gds_collector.get_messages()), ))
        gds_collector.write_messages(sys.stderr)
        sys.stderr.write(separator)
    return rootObj


def parseLiteral(inFileName, silence=False, print_warnings=True):
    parser = None
    doc = parsexml_(inFileName, parser)
    gds_collector = GdsCollector_()
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'containerType'
        rootClass = containerType
    rootObj = rootClass.factory()
    rootObj.build(rootNode, gds_collector_=gds_collector)
    # Enable Python to collect the space used by the DOM.
    if not SaveElementTreeNode:
        doc = None
        rootNode = None
    if not silence:
        sys.stdout.write('#from validate_simpletypes2_sup import *\n\n')
        sys.stdout.write('import validate_simpletypes2_sup as model_\n\n')
        sys.stdout.write('rootObj = model_.rootClass(\n')
        rootObj.exportLiteral(sys.stdout, 0, name_=rootTag)
        sys.stdout.write(')\n')
    if print_warnings and len(gds_collector.get_messages()) > 0:
        separator = ('-' * 50) + '\n'
        sys.stderr.write(separator)
        sys.stderr.write('----- Warnings -- count: {} -----\n'.format(
            len(gds_collector.get_messages()), ))
        gds_collector.write_messages(sys.stderr)
        sys.stderr.write(separator)
    return rootObj


def main():
    args = sys.argv[1:]
    if len(args) == 1:
        parse(args[0])
    else:
        usage()


if __name__ == '__main__':
    #import pdb; pdb.set_trace()
    main()

RenameMappings_ = {
}

__all__ = [
    "containerType",
    "simpleOneType",
    "simpleTwoElementOneType",
    "simpleTwoType"
]
