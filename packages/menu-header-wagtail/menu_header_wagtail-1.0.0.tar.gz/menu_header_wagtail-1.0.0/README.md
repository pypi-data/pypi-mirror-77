# Wagtail Header 

Full navigation header, menus, sub menus, internal and external links and documents, simple integrated design.

###### Version Python: `^3`
###### Version django: `^3`
###### Version wagtail: `^2.8`

## Installation
- `pip install menu_header_wagtail`
- Add `menu_header_wagtail` to your installed apps
- Run migrations `./ manage.py migrate`


## Usage
- Import in models of app

my_app/models.py
```python
from menu_header_wagtail.models import HeaderPage
```

- Add the model `HeaderPage` to the page model as `ForeignKey` in your HomePage or other pages
```python
class HomePage(Page):
    header = models.ForeignKey(
        HeaderPage,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    ...
```
and then in content
```python
    ...
    content_panels = Page.content_panels + [
        SnippetChooserPanel('header'),
        ...
    ]
```


## And to render:

- Load tag and pass param page
```djangotemplate
{% load menu_header_wagtail_tag %}

{% render_header_ui page %}
```

**NOTE:** If you have nested pages, then use the get_parent_page tag and the child page as a parameter. 

When you get it, you must indicate the type of page that the parent is: `page_parent.{type_page}`

```djangotemplate
{% get_parent_page page as page_parent %}

{% render_header page_parent.homepage %}

```


- And finally, stop and start server


Using this type of menu is important because it allows you to reuse as well as create different ones for different pages.


Made with ♥ by [Jose Florez](www.joseflorez.co)