# mkdocs-encryptcontent-plugin

*This plugin allows you to have password protected articles and pages in MKdocs.* 

*The content is encrypted with AES-256 in Python using PyCryptodome, and decrypted in the browser with Crypto-JS.*

*It has been tested in Python Python 3.5+*

An mkdocs version of the plugin [Encrypt content](https://github.com/mindcruzer/pelican-encrypt-content) for Pelican.

**Usecase**

> I want to be able to protect my articles with password. And I would like this protection to be as granular as possible.
>
> It is possible to define a password to protect each article independently or a global password to encrypt all of them.
>
> If a global password exists, all articles and pages are encrypted with this password.
>
> If a password is defined in an article or a page, it is always used even if a global password exists.
>
> If a password is defined as an empty character string, the page is not encrypted.


## Installation

Install the package with pip:

```bash
pip install mkdocs-encryptcontent-plugin
```

Install the package from source with pip:

```bash
cd mkdocs-encryptcontent-plugin/
python3 setup.py sdist bdist_wheel
pip3 install dist/mkdocs_encryptcontent_plugin-0.0.10-py3-none-any.whl
```

Enable the plugin in your `mkdocs.yml`:

```yaml
plugins:
    - encryptcontent: {}
```

You are then able to use the meta tag `password: secret_password` in your markdown files to protect them.

> **Note:** If you have no `plugins` entry in your config file yet, you'll likely also want to add the `search` plugin. MkDocs enables it by default if there is no `plugins` entry set, but now you have to enable it explicitly.


### Using global password protection

Add `global_password: your_password` in plugin config variable, to protect by default your articles with this password

```yaml
plugins:
    - encryptcontent:
        global_password: 'your_password'
```

If a password is defined in an article, it will ALWAYS overwrite the global password. 

> **NOTE** Keep in mind that if the `password:` tag exists without value in an article, it will not be protected !

### Extra vars customization

Optionally you can use some extra variables in plugin config to customize default messages.

```yaml
plugins:
    - encryptcontent:
        title_prefix: '[LOCK]'
        summary: 'another informational message to encrypted content'
        placeholder: 'another password placeholder'
        decryption_failure_message: 'another informational message when decryption fail'
        encryption_info_message: 'another information message when you dont have acess !'
```

Default prefix title is `[Protected]`

Default summary message is `This content is protected with AES encryption.`

Default password palceholder is `Provide password and press ENTER`

Default decryption failure message is `Invalid password.`

Defaut encryption information message is `Contact your administrator for access to this page.`

> **NOTE** Adding a prefix to the title does not change the default navigation path !


## Features

### HighlightJS support

If your theme use HighlightJS module to improve color, set `highlightjs: true` in your `mkdocs.yml`, to enable color reloading after decryption process.
 
When enable the following part of the template is add to force reloading decrypted content.

```jinja
{% if hljs %}
document.getElementById("mkdocs-decrypted-content").querySelectorAll('pre code').forEach((block) => {
    hljs.highlightBlock(block);
});
{% endif %}
```

### Tag encrypted page

Related to [issue #7](https://github.com/CoinK0in/mkdocs-encryptcontent-plugin/issues/7)

You can add `tag_encrypted_page: True` in plugin config variable, to enable tagging of encrypted pages.

When this feature is enabled, an additional attribute `encrypted` with value `True,` is added to the mkdocs type `mkdocs.nav.page` object.

```yaml
plugins:
    - encryptcontent:
        tag_encrypted_page: True
```

It becomes possible to use this attribute in the jinja template of your theme, as a condition to perform custom modification.

```jinja
{%- for nav_item in nav %}
    {% if nav_item.encrypted %}
        <!-- Do something --> 
    {% endif %}
{%- endfor %}
```

For example, in your template, you can use conditional check to add custom class :

```jinja
<a {% if nav_item.encrypted %}class="mkdocs-encrypted-class"{% endif %}href="{{ nav_item.url|url }}">{{ nav_item.title }}</a>
```

### Rebember password

Related to [issue #6](https://github.com/CoinK0in/mkdocs-encryptcontent-plugin/issues/6)

> :warning: **This feature is not really secure !** Password are store in clear text inside local cookie without httpOnly flag.
>
> Instead of using this feature, I recommend to use a password manager with its web plugins.
> For example **KeepassXC** allows you, with a simple keyboard shortcut, to detect the password field `mkdocs-content-password` and to fill it automatically in a much more secure way.

If you do not have password manager, you can set `remember_password: True` in your `mkdocs.yml` to enable password remember feature.

When enabled, each time you fill password form and press `Enter` a cookie is create with your password as value. 
When you reload the page, if you already have an 'encryptcontent' cookie in your browser,
the page will be automatically decrypted using the value of the cookie.

By default, the cookie is created with a `path=` relative to the page on which it was generated.
This 'specific' cookie will always be used as first attempt to decrypt the current page when loading.

If your password is a global password, you can fill in the `mkdocs-content-password` field,
then use the keyboard shortcut `CTRL + ENTER` instead of the classic `ENTER`. 
The cookie that will be created with a `path=/` making it accessible, by default, on all the pages of your site.

The form of decryption remains visible as long as the content has not been successfully decrypted,
 which allows in case of error to modify the created cookie.

All cookies created with this feature have the default security options `Secure` and` SameSite=Strict`, just cause ...

However *(optionally)*, its possible to remove these two security options by adding `disable_cookie_protection: True` in your` mkdocs.yml`.

Your configuration should look like this when you enabled this feature :
```yaml
plugins:
    - encryptcontent:
        remember_password: True
        disable_cookie_protection: True   # <-- Really a bad idea
```

### Add button

Add `password_button: True` in plugin config variable, to add button to the right of the password field.

When enable, it allows to decrypt the content without creating a cookie *(if remember password feature is activated)*

Optionnally, you can add `password_button_text: 'custome_text_button'` to customize the button text.
 
```yaml
plugins:
    - encryptcontent:
        password_button: True
        password_button_text: 'custome_text_button'
```

## Contributing

From reporting a bug to submitting a pull request: every contribution is appreciated and welcome.
Report bugs, ask questions and request features using [Github issues][github-issues].
If you want to contribute to the code of this project, please read the [Contribution Guidelines][contributing].

[mkdocs-plugins]: http://www.mkdocs.org/user-guide/plugins/
[github-issues]: https://github.com/CoinK0in/mkdocs-encryptcontent-plugin/issues
[contributing]: CONTRIBUTING.md

### Contributors

- [anthonyeden](https://github.com/anthonyeden)
