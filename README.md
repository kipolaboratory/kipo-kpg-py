# Python Kipo KPG Library: make payment easy with kipo

[![Latest Stable Version](https://poser.pugx.org/kipolaboratory/kipo-kpg/v/stable)](https://packagist.org/packages/kipolaboratory/kipo-kpg)
[![](https://img.shields.io/github/license/kipolaboratory/kipo-kpg.svg)](https://github.com/kipolaboratory/kipo-kpg/blob/master/LICENSE)
[![](https://img.shields.io/travis/kipolaboratory/kipo-kpg.svg)](https://travis-ci.org/kipolaboratory/kipo-kpg/)
[![](https://img.shields.io/packagist/dt/kipolaboratory/kipo-kpg.svg)](https://github.com/kipolaboratory/kipo-kpg/releases/)

Python Kipo KPG Library make it easy to stablish payment with kipo gateway.

![KipoPay Company logo](https://kipopay.com/img/fr.png)

---
- [Installation](#installation)
- [Quick Start and Examples](#quick-start-and-examples)
- [Properties](#properties)
- [HTML Form to transfer user to KPG](#html-form-to-transfer-user-to-kpg)
---
### Installation
Add KipoKPG files to Your project
or simply run 
```pip install kipo-kpg```

### Quick Start and Examples
Initial Kipo KPG and request shopping key from kipo server.
```python
from KipoKPG import KipoKPG

"""
    Initial Kipo Library and craete object from KipoKPG class
    Merchant key is merchant phone number
"""
kipo = KipoKPG("YOUR MERCHANT KEY")

"""
    Replace "YOUR CALLBACK URL" and "AMOUNT" with what you want
    kpg_initiate return a Dictionary 
    Successful - {"status": True, "shopping_key": SHOPING_KEY}
    Failed - {"status": false, "message": ERROR_CODE}
"""
kpg_initiate = kipo.kpg_initiate(AMOUNT, 'YOUR CALLBACK URL')

if kpg_initiate['status']:
    """
        Store kpg_initiate["shopping_key"] to session to verfiy
        payment after user came back from gateway
        
        Call render_form function to render a html form and send
        user to Kipo KPG Gateway (you can create this form manually
        where you want - form example is at the end of Quick Start
    """
    kipo.render_form(kpg_initiate['shopping_key'])
else:
    """
        Show error to user
        
        You can call getErrorMessage and send error code to that as input
        and get error message
        kipo.get_error_message(ERROR_CODE)
    """
  
```
Verify payment after user return back to *CALLBACK URL*
```python
"""
    Replace "SHOPPING_KEY" with your SHOPPING_KEY that you taken from
    Initiate function
    
    kpg_inquery return a dictionary for result
    Successful - {"status": True, "referent_code": REFERENT_CODE}
    Failed - {"status": False, "message": ERROR_CODE}
"""
kpg_inquery = kipo.kpg_inquery(SHOPPING_KEY)
```

```python
# Get shopping key after kpg_initiate called
kipo.get_shopping_key()
```

```python
# Get referent code after kpg_inquery called
kipo.get_referent_code()
```

### Properties
```python
""" 
    URL of Kipo server - https://kpg.kipopay.com:8091/V1.0/processors/json/
    This server create shopping key and 
"""
kipo.request_url

"""
    URL of Kipo KPG - http://webgate.kipopay.com/
    Shopping key must post to this url with SK name
"""
kipo.kipo_webgate_url
```

### HTML Form to transfer user to KPG
```html
<form id="kipopay-gateway" method="post" action="KIPO_WEBGATE_URL" style="display: none;">
    <input type="hidden" id="sk" name="sk" value="SHOPING_KEY"/>
</form>
<script language="javascript">document.forms['kipopay-gateway'].submit();</script>
```
