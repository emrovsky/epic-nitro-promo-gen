import json
import random
import secrets

import random_strings
import requests

true = True
false = False
from datetime import datetime, timedelta



def generate_random_t_values(num_values, min_value, max_value, precision):
    t_values = []
    for _ in range(num_values):
        t = round(random.uniform(min_value, max_value), precision)
        t_values.append({"t": t})
    return t_values
def generate_random_data(num_values, t_range, x_range, y_range, t_precision):
    data = []
    for _ in range(num_values):
        t = round(random.uniform(t_range[0], t_range[1]), t_precision)
        x = random.randint(x_range[0], x_range[1])
        y = random.randint(y_range[0], y_range[1])
        data.append({"t": t, "x": x, "y": y})
    return data

def create_fingerprint():

    unmaskedRenderer, unmaskedVendor = random.choice(open("fingerprint.txt","r").readlines()).strip().split("|")

    fingerprint = {
        "fingerprint_version": 42,
        "timestamp": (datetime.utcnow() + timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z',
        "math_rand": str(secrets.token_hex(7))[:13],
        "webasm": true,
        "document": {
            "title": "Sign in to Your Epic Games account | Epic Games",
            "referrer": ""
        },
        "navigator": {
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "platform": "Win32",
            "language": "en-US",
            "languages": [
                "en-US"
            ],
            "hardware_concurrency": random.choice([8,16,32,64]),
            "device_memory": random.choice([8,16,32,64]),
            "product": "Gecko",
            "product_sub": "20030107",
            "vendor": "Google Inc.",
            "vendor_sub": "",
            "webdriver": false,
            "max_touch_points": 0,
            "cookie_enabled": true,
            "property_list": ["vendorSub","productSub","vendor","maxTouchPoints","scheduling","userActivation","doNotTrack","geolocation","connection","plugins","mimeTypes","pdfViewerEnabled","webkitTemporaryStorage","webkitPersistentStorage","windowControlsOverlay","hardwareConcurrency","cookieEnabled","appCodeName","appName","appVersion","platform","product","userAgent","language","languages","onLine","webdriver","getGamepads","javaEnabled","sendBeacon","vibrate","deprecatedRunAdAuctionEnforcesKAnonymity","bluetooth","storageBuckets","clipboard","credentials","keyboard","managed","mediaDevices","storage","serviceWorker","virtualKeyboard","wakeLock","deviceMemory","userAgentData","login","ink","mediaCapabilities","hid","locks","gpu","mediaSession","permissions","presentation","usb","xr","serial","adAuctionComponents","runAdAuction","canLoadAdAuctionFencedFrame","canShare","share","clearAppBadge","getBattery","getUserMedia","requestMIDIAccess","requestMediaKeySystemAccess","setAppBadge","webkitGetUserMedia","clearOriginJoinedAdInterestGroups","createAuctionNonce","deprecatedReplaceInURN","deprecatedURNToURL","getInstalledRelatedApps","joinAdInterestGroup","leaveAdInterestGroup","updateAdInterestGroups","registerProtocolHandler","unregisterProtocolHandler"
            ],
            "connection_rtt": random.choice([50,100,150,200,250,300,350,400,450,500]),
        },
        "web_gl": {
            "canvas_fingerprint": {
                "length": 32942,
                "num_colors": 4764,
                "md5": str(random_strings.random_hex(16)),
                "tlsh": random_strings.random_string(70).upper()
            },
            "parameters": {
                "renderer": unmaskedVendor,
                "vendor": unmaskedVendor
            }
        },
        "window": {
            "location": {
                "origin": "https://www.epicgames.com",
                "pathname": "/id/login",
                "href": "https://www.epicgames.com/id/login?redirect_uri=https%3A%2F%2Fwww.epicgames.com%2Fsite%2F&client_id=5a6fcd3b82e04f8fa0065253835c5221"
            },
            "history": {
                "length": 2
            },
            "screen": {
                "avail_height": 1050,
                "avail_width": 1920,
                "avail_top": 0,
                "height": 1080,
                "width": 1920,
                "color_depth": 24
            },
            "performance": {
                "memory": {
                    "js_heap_size_limit": random.randint(100000000, 200000000),
                    "total_js_heap_size": random.randint(10000000, 50000000),
                    "used_js_heap_size": random.randint(1000000, 5000000)
                },
                "resources": ["https://static-assets-prod.unrealengine.com/account-portal/static/static/js/main.1f766214.js","https://static-assets-prod.unrealengine.com/account-portal/static/static/css/main.c19873d8.css","https://tracking.epicgames.com/tracking.js","https://tracking.epicgames.com/track.png?referringUrl=none&location=https%3A%2F%2Fwww.epicgames.com%2Fid%2Fregister%2Fdate-of-birth%3Fredirect_uri%3Dhttps%253A%252F%252Fwww.epicgames.com%252Fsite%252F%26client_id%3D5a6fcd3b82e04f8fa0065253835c5221&now=1716066403392&eventType=pageView","https://static-assets-prod.unrealengine.com/account-portal/static/static/js/7947.50df8dbf.chunk.js","https://static-assets-prod.unrealengine.com/account-portal/static/static/css/polyfills.fdeb4d23.chunk.css","https://static-assets-prod.unrealengine.com/account-portal/static/static/js/polyfills.7de817c8.chunk.js","https://www.epicgames.com/id/api/reputation","https://www.epicgames.com/id/api/i18n?ns=messages","https://www.epicgames.com/id/api/i18n?ns=epic-consent-dialog","https://www.epicgames.com/id/api/analytics","https://sentry.io/api/1333512/envelope/?sentry_key=7a13b97c16f4455f92376d5c1e27f102&sentry_version=7&sentry_client=sentry.javascript.react%2F7.106.1","https://www.epicgames.com/id/api/location","https://www.epicgames.com/id/api/analytics","https://static-assets-prod.unrealengine.com/account-portal/static/epic-favicon-96x96.png","https://www.epicgames.com/id/api/analytics","https://www.epicgames.com/id/api/client/5a6fcd3b82e04f8fa0065253835c5221?redirectUrl=https%3A%2F%2Fwww.epicgames.com%2Fsite%2F","https://www.epicgames.com/id/api/authenticate","https://www.epicgames.com/id/api/analytics","https://www.epicgames.com/id/api/analytics","https://static-assets-prod.unrealengine.com/account-portal/static/static/js/8903.1a87d99d.chunk.js","https://static-assets-prod.unrealengine.com/account-portal/static/static/js/9896.6f646c07.chunk.js","https://www.epicgames.com/id/api/age-gate","https://tracking.epicgames.com/track.png?referringUrl=none&location=https%3A%2F%2Fwww.epicgames.com%2Fid%2Flogin%3Fredirect_uri%3Dhttps%253A%252F%252Fwww.epicgames.com%252Fsite%252F%26client_id%3D5a6fcd3b82e04f8fa0065253835c5221&now=1716066404511&eventType=pageView","https://www.epicgames.com/id/api/analytics","https://www.epicgames.com/id/api/client/5a6fcd3b82e04f8fa0065253835c5221?redirectUrl=https%3A%2F%2Fwww.epicgames.com%2Fsite%2F","https://static-assets-prod.unrealengine.com/account-portal/static/epic-favicon-96x96.png","https://www.epicgames.com/id/api/analytics","https://www.epicgames.com/id/api/analytics","https://static-assets-prod.unrealengine.com/account-portal/static/static/js/2893.1b7db46f.chunk.js","https://talon-website-prod.ecosec.on.epicgames.com/talon_sdk.js","https://talon-service-prod.ecosec.on.epicgames.com/v1/init","https://js.hcaptcha.com/1/api.js?onload=hCaptchaLoaded&render=explicit","https://newassets.hcaptcha.com/captcha/v1/7329d5a/static/hcaptcha.html#frame=challenge&id=0cz6i37otncr&host=www.epicgames.com&sentry=true&reportapi=https%3A%2F%2Faccounts.hcaptcha.com&recaptchacompat=true&custom=false&hl=en&tplinks=on&pstissuer=https%3A%2F%2Fpst-issuer.hcaptcha.com&sitekey=5928de2d-2800-4c58-be91-060e5a6aa117&theme=light&size=invisible&challenge-container=h_captcha_challenge_email_exists_prod&origin=https%3A%2F%2Fwww.epicgames.com","https://sentry.io/api/1333512/envelope/?sentry_key=7a13b97c16f4455f92376d5c1e27f102&sentry_version=7&sentry_client=sentry.javascript.react%2F7.106.1","https://talon-service-prod.ecosec.on.epicgames.com/v1/phaser/batch"
                ]
            },
            "device_pixel_ratio": 1,
            "dark_mode": false,
            "chrome": true,
            "property_list": ["0","1","2","window","self","document","name","location","customElements","history","navigation","locationbar","menubar","personalbar","scrollbars","statusbar","toolbar","status","closed","frames","length","top","opener","parent","frameElement","navigator","origin","external","screen","innerWidth","innerHeight","scrollX","pageXOffset","scrollY","pageYOffset","visualViewport","screenX","screenY","outerWidth","outerHeight","devicePixelRatio","clientInformation","screenLeft","screenTop","styleMedia","onsearch","isSecureContext","trustedTypes","performance","onappinstalled","onbeforeinstallprompt","crypto","indexedDB","sessionStorage","localStorage","onbeforexrselect","onabort","onbeforeinput","onbeforematch","onbeforetoggle","onblur","oncancel","oncanplay","oncanplaythrough","onchange","onclick","onclose","oncontentvisibilityautostatechange","oncontextlost","oncontextmenu","oncontextrestored","oncuechange","ondblclick","ondrag","ondragend","ondragenter","ondragleave","ondragover","ondragstart","ondrop","ondurationchange","onemptied","onended","onerror","onfocus","onformdata","oninput","oninvalid","onkeydown","onkeypress","onkeyup","onload","onloadeddata","onloadedmetadata","onloadstart","onmousedown","onmouseenter","onmouseleave","onmousemove","onmouseout","onmouseover","onmouseup","onmousewheel","onpause","onplay","onplaying","onprogress","onratechange","onreset","onresize","onscroll","onsecuritypolicyviolation","onseeked","onseeking","onselect","onslotchange","onstalled","onsubmit","onsuspend","ontimeupdate","ontoggle","onvolumechange","onwaiting","onwebkitanimationend","onwebkitanimationiteration","onwebkitanimationstart","onwebkittransitionend","onwheel","onauxclick","ongotpointercapture","onlostpointercapture","onpointerdown","onpointermove","onpointerrawupdate","onpointerup","onpointercancel","onpointerover","onpointerout","onpointerenter","onpointerleave","onselectstart","onselectionchange","onanimationend","onanimationiteration","onanimationstart","ontransitionrun","ontransitionstart","ontransitionend","ontransitioncancel","onafterprint","onbeforeprint","onbeforeunload","onhashchange","onlanguagechange","onmessage","onmessageerror","onoffline","ononline","onpagehide","onpageshow","onpopstate","onrejectionhandled","onstorage","onunhandledrejection","onunload","crossOriginIsolated","scheduler","alert","atob","blur","btoa","cancelAnimationFrame","cancelIdleCallback","captureEvents","clearInterval","clearTimeout","close","confirm","createImageBitmap","fetch","find","focus","getComputedStyle","getSelection","matchMedia","moveBy","moveTo","open","postMessage","print","prompt","queueMicrotask","releaseEvents","reportError","requestAnimationFrame","requestIdleCallback","resizeBy","resizeTo","scroll","scrollBy","scrollTo","setInterval","setTimeout","stop","structuredClone","webkitCancelAnimationFrame","webkitRequestAnimationFrame","chrome","fence","caches","cookieStore","ondevicemotion","ondeviceorientation","ondeviceorientationabsolute","launchQueue","sharedStorage","documentPictureInPicture","getScreenDetails","queryLocalFonts","showDirectoryPicker","showOpenFilePicker","showSaveFilePicker","originAgentCluster","onpageswap","onpagereveal","credentialless","speechSynthesis","onscrollend","webkitRequestFileSystem","webkitResolveLocalFileSystemURL","AppInit","_epicEnableCookieGuard","__tracking_base","_epicTrackingCookieDomainId","_epicTrackingCountryCode","regeneratorRuntime","_epicTracking","_sentryDebugIds","webpackChunkaccountportal_node_website","__axiosInstance","__core-js_shared__","core","__axiosInstanceCached","IMask","__store","__SENTRY__","clearImmediate","setImmediate","recaptchaOptions","a0_0x1ea3","a0_0x3a11","talon","hCaptchaLoaded","hCaptchaReady","Raven","hcaptcha","grecaptcha","k","i","TEMPORARY","PERSISTENT","addEventListener","dispatchEvent","removeEventListener"
            ]
        },
        "date": {
            "timezone_offset": -180,
            "format": {
                "calendar": "gregory",
                "day": "2-digit",
                "locale": "tr",
                "month": "2-digit",
                "numbering_system": "latn",
                "time_zone": "Europe/Istanbul",
                "year": "numeric"
            }
        },
        "runtime": {
            "sd_recurse": false
        },
        "fpjs": {
            "version": "3.4.2",
            "visitor_id": random_strings.random_hex(16),
            "confidence": 0.6,
            "hashes": {
                "fonts": random_strings.random_hex(16),
                "plugins": random_strings.random_hex(16),
                "audio": random_strings.random_hex(16),
                "canvas": random_strings.random_hex(16),
                "screen": random_strings.random_hex(16)
            }
        },
        "motion": {
            "mousemove": generate_random_data(14, [5000,150000], [400,600], [10,400], 9),
            "mousedown": generate_random_data(2, [5000,150000], [400,600], [10,400], 9),
            "mouseup": generate_random_data(14, [5000,150000], [400,600], [10,400], 9),
            "wheel": [],
            "touchstart": [],
            "touchend": [],
            "touchmove": [],
            "scroll": [],
            "keydown": generate_random_t_values(38,6900,9100,9),
            "keyup": generate_random_t_values(38,6900,9100,9),
            "resize": [],
            "paste": []
        },
        "sdk": {
            "caller_stack_trace": ""
        },
        "s": random.randint(11111111,99999999),
        "solve_token": false
    }

    response = requests.post('http://localhost:3000/process_fingerprint', json=fingerprint)
    return response.json()["result"]


