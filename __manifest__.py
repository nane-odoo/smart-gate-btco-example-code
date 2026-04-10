{
    'name': "Eagle Estate",

    'summary': "This module will allow us to manage properties, tenants, contracts and much more!",

    'description': """
Long description of module's purpose
    """,
    'application': True,

    'author': "Smart Gate",
    'website': "https://www.yourcompany.com",
    'category': 'Uncategorized',
    'version': '19.0.0.0.0',
    'depends': ["mail"],
    'data': [
        "security/ir.model.access.csv",
        "views/eagle_property_views.xml",
        "views/eagle_property_room_views.xml",
        "views/menuitem.xml",
        "data/eagle_tag_data.xml",
        "data/eagle_property_data.xml",
        "views/eagle_property_room_area_wizard_views.xml",
        "reports/report_eagle_property.xml"
    ],
}
