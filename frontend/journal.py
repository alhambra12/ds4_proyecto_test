class Journal:
    ''' Constructor de la clase Journal '''
    def __init__(self, id, title, areas, catalogs, website, h_index, area_categoria, publisher, issn, widget, publication_type):
        self.id = id
        self.title = title
        self.areas = areas
        self.catalogs = catalogs
        self.website = website
        self.h_index = h_index
        self.area_category = area_categoria
        self.publisher = publisher
        self.issn = issn
        self.widget = widget
        self.publication_type = publication_type
        
        
    def to_dict(self):
        ''' Retorna un diccionario con los atributos del objeto '''
        return {
            'id': self.id,
            'title': self.title,
            'areas': self.areas,
            'catalogs': self.catalogs,
            'website': self.website,
            'h_index': self.h_index,
            'area_category': self.area_category,
            'publisher': self.publisher,
            'issn': self.issn,
            'widget': self.widget,
            'publication_type': self.publication_type
        }

    def __str__(self):
        ''' Método para imprimir el objeto Journal '''
        return self.title
