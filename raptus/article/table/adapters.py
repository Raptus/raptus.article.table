from simplejson import dumps, loads

from zope import interface, component

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import normalizeString

from raptus.article.core.interfaces import IArticle
from raptus.article.table.interfaces import ITable, ITables, IRows, IDefinitions, IDefinition, IType
from raptus.article.table.utils import parseColumn

class Tables(object):
    """ Provider for tables contained in an article
    """
    interface.implements(ITables)
    component.adapts(IArticle)
    
    def __init__(self, context):
        self.context = context
        
    def getTables(self, **kwargs):
        """ Returns a list of tables (catalog brains)
        """
        catalog = getToolByName(self.context, 'portal_catalog')
        return catalog(portal_type='Table', path={'query': '/'.join(self.context.getPhysicalPath()),
                                                  'depth': 1}, sort_on='getObjPositionInParent', **kwargs)

class Rows(object):
    """ Provider for rows contained in a table
    """
    interface.implements(IRows)
    component.adapts(ITable)
    
    def __init__(self, context):
        self.context = context
        
    def getRows(self, **kwargs):
        """ Returns a list of rows (catalog brains)
        """
        catalog = getToolByName(self.context, 'portal_catalog')
        return catalog(portal_type='Row', path={'query': '/'.join(self.context.getPhysicalPath()),
                                                'depth': 1}, sort_on='getObjPositionInParent', **kwargs)
        
class Definitions(object):
    """Handles table definitions
    """
    interface.implements(IDefinitions)
    component.adapts(interface.Interface)
    
    def __init__(self, context):
        self.context = context
        props = getToolByName(self.context, 'portal_properties')
        if not 'raptus_article_table' in props:
            props.addPropertySheet('raptus_article_table')
        self.properties = props.raptus_article_table
        
    def getDefinition(self, name):
        """ Returns the definition
        """
        name = normalizeString(name, self.context)
        definition =  loads(self.properties.getProperty(name, dumps({'columns': [],
                                                                     'style': ''})))
        columns = []
        for col in definition['columns']:
            try:
                col['utility'] = component.getUtility(IType, col['type'])
                columns.append(col)
            except:
                pass
        definition['columns'] = columns
        return definition
    
    def getAvailableDefinitions(self):
        """ Returns a dict of definitions available for this article
        """
        definitions = {}
        for name in self.properties.propertyIds():
            try:
                definitions[name] = loads(self.properties.getProperty(name))
            except: # filter out malformed definitions
                pass
        return definitions
    
    def addDefinition(self, name, style, columns):
        """ Adds a new global definition
        """
        value = dumps({'columns': columns,
                       'style': style,
                       'name': name})
        name = normalizeString(name, self.context)
        if self.properties.hasProperty(name):
            self.properties._updateProperty(name, value)
        else:
            self.properties._setProperty(name, value)
    
    def removeDefinition(self, name):
        """ Removes a global definition
        """
        name = normalizeString(name, self.context)
        if self.properties.hasProperty(name):
            self.properties._delProperty(name)
        
class Definition(object):
    """ Definition provider for tables
    """
    interface.implements(IDefinition)
    component.adapts(ITable)
    
    def __init__(self, context):
        self.context = context
        
    def getCurrentDefinition(self):
        """ Returns the definition for this article
        """
        definition = {}
        if self.context.getDefinition():
            definition = IDefinitions(self.context).getDefinition(self.context.getDefinition())
        columns = self.context.getColumns()
        if columns:
            definition['columns'] = []
            for col in columns:
                try:
                    column = parseColumn(col)
                    utility = component.getUtility(IType, column['type'])
                    column['utility'] = utility
                    definition['columns'].append(column)
                except:
                    pass
        style = self.context.getStyle()
        if style:
            definition['style'] = style
        return definition