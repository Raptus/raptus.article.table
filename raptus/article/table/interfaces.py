from zope import interface

class ITables(interface.Interface):
    """ Provider for tables contained in an article
    """
    
    def getTables(**kwargs):
        """ Returns a list of tables (catalog brains)
        """

class IRows(interface.Interface):
    """ Provider for rows contained in a table
    """
    
    def getRows(**kwargs):
        """ Returns a list of rows (catalog brains)
        """

class IDefinitions(interface.Interface):
    """ Handles table definitions
    """
        
    def getDefinition(name):
        """ Returns the definition
        """
    
    def getAvailableDefinitions():
        """ Returns a dict of definitions available for this article
        """
    
    def addDefinition(name, style, columns):
        """ Adds a new global definition
        """
    
    def removeDefinition(name):
        """ Removes a global definition
        """

class IDefinition(interface.Interface):
    """ Definition provider for tables
    """
        
    def getCurrentDefinition():
        """ Returns the definition for this article
        """

class ITable(interface.Interface):
    """ Marker interface for the table content type
    """

class IRow(interface.Interface):
    """ Marker interface for the row content type
    """

class IType(interface.Interface):
    """ A column type
    """
    
    def structure():
        """ Whether the value has to be rendered as structure or not
        """
        
    def modifier(value):
        """ Returns the modified value
        """
        
    def field(name, label):
        """ Returns the ExtensionField to be used in the SchemaExtender
        """
        
    def widget(name):
        """ Renders a simple widget to add data in a table cell
        """
