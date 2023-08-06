# Django-Cookiebanner

## Installation

`pip install django-cookiebanner`


## Usage

* Add `cookiebanner` to your `INSTALLED_APPS`

* in your settings (`settings.py`) specify the different Cookie Groups:
```python
COOKIEBANNER = {
    "title": "Cookie settings",
    "header_text": "We are using cookies on this website. A few are essential, others are not.",
    "footer_text": "Please accept our cookies",
    "footer_links": [
        { 
            "title": "Imprint", 
            "href": "/imprint" 
        },
        { 
            "title": "Privacy", 
            "href": "/privacy" 
        },
    ],
    "groups": [
        {
            "id": "essential",
            "name": "Essential",
            "description": "Essential cookies allow this page to work.",
            "cookies": [
                {
                    "pattern": "cookiebanner",
                    "description": "Meta cookie for the cookies that are set.",
                },
                {
                    "pattern": "csrftoken",
                    "description": "This cookie prevents Cross-Site-Request-Forgery attacks.",
                },
                {
                    "pattern": "sessionid",
                    "description": "This cookie is necessary to allow logging in, for example.",
                },
            ],
        },
        {
            "id": "analytics",
            "name": "Analytics",
            "optional": True,
            "cookies": [
                {
                    "pattern": "_pk_.*",
                    "description": "Matomo cookie for website analysis.",
                },
            ],
        },
    ],
}
```

* In your base template add the banner and the conditionals:
```djangotemplate
{% load cookiebanner %}
...
<body>
{% cookiebanner_modal %}
...


{% cookie_accepted 'analytics' as cookie_analytics %}
{% if cookie_analytics %}
<script>... javascript for matomo ...</script>
{% endif %}
</body>
```


