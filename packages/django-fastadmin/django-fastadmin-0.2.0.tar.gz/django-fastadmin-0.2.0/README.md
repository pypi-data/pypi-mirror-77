# django-fastadmin

django admin extensions.

## Install

```shell
pip install django-fastadmin
```

## Installed Admin Extensions

### Admin extends

- UuidFieldSearchableAdmin
- InlineBooleanFieldsAllowOnlyOneCheckedMixin

### Widgets

### Forms

### Filters

### Jquery Generic Plugins

**Note:**
- `$.fn.xxx` is jQuery object related util.
- `$.xxx` is simple util in jQuery namespace.
- All jquery plugin files are prefixed with `django-jquery-plugins/`.
- Add `admin/js/vendor/jquery/jquery.js` at the first and add `admin/js/jquery.init.js` at the last in your js list. Use `django_fastadmin.admin.jquery_plugins`([...your jquery files...]) for easy.

| File | Plugin Name | Memo |
| :---- | :---- | :---- |
| jquery.utils.js | $.fn.classes | |
| jquery.cookie.js | $.cookie | |
| jquery.cookie.js | $.removeCookie | |


## InlineBooleanFieldsAllowOnlyOneCheckedMixin Usage

- Add this mixin to inline class, and put it before TabularInline.
- Add classes property
    - Add class InlineBooleanFieldsAllowOnlyOneCheckedMixin.special_class_name
    - Add class InlineBooleanFieldsAllowOnlyOneCheckedMixin.field_name_prefix + {field name},
- Example:
    ```
    from django.contrib import admin
    from django_fastadmin.admin import InlineBooleanFieldsAllowOnlyOneCheckedMixin

    from .models import Book
    from .models import Category

    class BookInline(InlineBooleanFieldsAllowOnlyOneCheckedMixin, admin.TabularInline):
        model = Book
        extra = 0
        classes = [
            InlineBooleanFieldsAllowOnlyOneCheckedMixin.special_class_name,
            InlineBooleanFieldsAllowOnlyOneCheckedMixin.field_name_prefix + "is_best_seller",
            ]


    class CategoryAdmin(admin.ModelAdmin):
        inlines = [
            BookInline,
        ]

    admin.site.register(Category, CategoryAdmin)
    ```

## Bug report

Please report any issues at https://github.com/zencore-cn/zencore-issues.

## Releases

### v0.2.0 2020/08/25

- Add widgets.AceWidget.

### v0.1.1 2020/08/13

- Fix jquery.js and jquery.init.js including orders, so that we don't need to change js plugin's source to use django.jQuery.

### v0.1.0 2020/08/12

- First release.
- Add UuidFieldSearchableAdmin.
- Add InlineBooleanFieldsAllowOnlyOneCheckedMixin.