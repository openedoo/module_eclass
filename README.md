## Openedoo module Eclass

Eclass module for openedoo, current status is WIP.


## What is eClass?

eClass will be acting like a regular classroom in school, like handling group discussions for eClass member.


This module is the backend side, it is based on REST API.


## Installing
```
$ python manage.py module install 'module_eclass'
```

See WIKI page for available endpoint, [wiki](https://github.com/openedoo/module_eclass/wiki)

### Testing

Testing for module is a litle bit tricky with the `openedoo core`. See this information for unittest setup, [Pull request 81](https://github.com/openedoo/openedoo/pull/81). Also be careful, you must ensure that `config.py` in `openedoo core` is set for testing (different DB setup).

From project root run:
```
python -m unittest discover modules/module_eclass
```

With coverage:
```
coverage run -m unittest discover modules/module_eclass
```


## Contributing
Every kind of contribution is welcomed here :heart:.


## Some word about the mantainer
One of the maintainer (@dwipr_) is a paid contributor to work on this project, if you make some contribution, maybe he will buy you a coffee.
