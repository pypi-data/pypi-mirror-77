## {{{ http://code.activestate.com/recipes/534109/ (r8)
import re
import xml.sax.handler
import dateutil.parser as duparser
import calendar

# used to clean text by removing multiple spaces
R1 = re.compile(r"^\s{2,}", re.MULTILINE)

def clean_text(field_name, raw_text):
    if field_name in ['description','instruction']:
        return R1.sub(" ", raw_text.strip()).replace('\n',' ')
    return raw_text

def convert_timestamp(t):
    #e.g., 2012-03-15T22:18:00-04:00
    dt = duparser.parse(t)
    return calendar.timegm(dt.utctimetuple())

def xml2obj(src):
    """
    A simple function to converts XML data into native Python object.
    """

    non_id_char = re.compile('[^_0-9a-zA-Z]')
    def _name_mangle(name):
        return non_id_char.sub('_', name)

    class DataNode(object):
        def __init__(self):
            self._attrs = {}    # XML attributes and child elements
            self.data = None    # child text data
        def __len__(self):
            # treat single element as a list of 1
            return 1
        def __getitem__(self, key):
            if isinstance(key, basestring):
                return self._attrs.get(key,None)
            else:
                return [self][key]
        def __contains__(self, name):
            return name in self._attrs
        def __nonzero__(self):
            return bool(self._attrs or self.data)
        def __getattr__(self, name):
            if name.startswith('__'):
                # need to do this for Python special methods???
                raise AttributeError(name)
            return self._attrs.get(name,None)
        def _add_xml_attr(self, name, value):
            if name in self._attrs:
                # multiple attribute of the same name are represented by a list
                children = self._attrs[name]
                if not isinstance(children, list):
                    children = [children]
                    self._attrs[name] = children
                children.append(value)
            else:
                self._attrs[name] = value
        def __str__(self):
            return self.data or ''
        def __repr__(self):
            items = sorted(self._attrs.items())
            if self.data:
                items.append(('data', self.data))
            return u'{%s}' % ', '.join([u"'%s':%s" % (k,repr(v)) for k,v in items])

    class TreeBuilder(xml.sax.handler.ContentHandler):
        def __init__(self):
            self.stack = []
            self.root = DataNode()
            self.current = self.root
            self.text_parts = []
        def startElement(self, name, attrs):
            self.stack.append((self.current, self.text_parts))
            self.current = DataNode()
            self.text_parts = []
            # xml attributes --> python attributes
            for k, v in attrs.items():
                self.current._add_xml_attr(_name_mangle(k), v)
        def endElement(self, name):
            text = ''.join(self.text_parts).strip()
            if text:
                self.current.data = clean_text(name,text)
            if self.current._attrs:
                obj = self.current
            else:
                # a text only node is simply represented by the string
                obj = clean_text(name,text) or ''
            self.current, self.text_parts = self.stack.pop()
            self.current._add_xml_attr(_name_mangle(name), obj)
            try:
                if str(obj).strip() != '':
                    obj_epoch = convert_timestamp(obj)
                    self.current._add_xml_attr(_name_mangle("%s_epoch"%name), obj_epoch)
            except:
                pass
        def characters(self, content):
            self.text_parts.append(content)


    builder = TreeBuilder()
    if isinstance(src,basestring):
        xml.sax.parseString(src, builder)
    else:
        xml.sax.parse(src, builder)
    return builder.root._attrs.values()[0]
## end of http://code.activestate.com/recipes/534109/ }}}
