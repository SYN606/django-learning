# jazzmin.py

JAZZMIN_SETTINGS = {

    # Branding
    "site_title": "Zoro Admin",
    "site_header": "Zoro Blog",
    "site_brand": "Zoro",
    "welcome_sign": "Manage your content",
    "copyright": "Zoro Blog",

    # Sidebar
    "show_sidebar": True,
    "navigation_expanded": False,

    # App & Model Order
    "order_with_respect_to": [
        "blogs",
        "home",
        "auth",
    ],

    # Icons
    "icons": {
        "blogs.Blog": "fas fa-newspaper",
        "blogs.Category": "fas fa-folder",
        "blogs.Comment": "fas fa-comments",
        "auth.User": "fas fa-user",
    },

    # Top Menu
    "topmenu_links": [
        {
            "name": "View Site",
            "url": "/",
            "new_window": True
        },
    ],

    # Hide things you don’t want clutter
    "hide_apps": [],
    "hide_models": [],
}

JAZZMIN_UI_TWEAKS = {
    "theme": "darkly",
    "dark_mode_theme": "darkly",
    "navbar": "navbar-dark",
    "sidebar": "sidebar-dark-primary",
    "brand_colour": "navbar-primary",
    "accent": "accent-primary",
    "sidebar_nav_small_text": False,
}
