        
/* Soon v1.9.0 - Soon, Animated Responsive Countdowns, jQuery
 * Copyright (c) 2016 Rik Schennink - http://rikschennink.nl/products/soon
 */
!function(a, b, c) {
    function d() {
        H !== window.innerWidth && (H = window.innerWidth,
        g())
    }
    function e(a, b, c, d) {
        var e = parseInt(getComputedStyle(document.documentElement).fontSize, 10) / 16
          , f = parseInt(getComputedStyle(b).fontSize, 10) / 16 / e
          , g = d / b.scrollWidth
          , h = g * f;
        return 4 > h ? (a.style.fontSize = "",
        c.redraw(),
        !1) : (a.style.fontSize = h + "rem",
        a.setAttribute("data-scale-rounded", Math.round(h).toString()),
        c.redraw(),
        !0)
    }
    function f(a, b) {
        if (!B.isSlow()) {
            for (var c, d, f = window.getComputedStyle(a.parentNode), g = parseInt(f.getPropertyValue("padding-left"), 10), h = parseInt(f.getPropertyValue("padding-right"), 10), i = a.parentNode.clientWidth - g - h, j = a.getAttribute("data-scale-max"), k = a.getAttribute("data-scale-hide"), l = j ? I.indexOf(j) : J, m = a.querySelectorAll(".soon-group-sub"), n = 0, o = m.length, p = a.querySelector(".soon-group"); o > n; n++)
                m[n].style.display = "";
            if ("fit" === j || "fill" === j) {
                if (e(a, p, b, i))
                    return;
                l = 0
            }
            c = l;
            do
                a.setAttribute("data-scale", I[c]),
                c++;
            while (p.scrollWidth > i && I[c]);if (c !== l && b.redraw(),
            !(p.scrollWidth <= i || "none" === k)) {
                n = 0,
                d = !1;
                do {
                    if ("0" !== m[n].getAttribute("data-value"))
                        break;
                    m[n].style.display = "none",
                    d = !0,
                    n++
                } while (p.scrollWidth > i && o > n);if (d && b.redraw(),
                "empty" !== k) {
                    n = o - 1,
                    d = !1;
                    do
                        m[n].style.display = "none",
                        d = !0,
                        n--;
                    while (p.scrollWidth > i && n > 0);d && b.redraw()
                }
            }
        }
    }
    function g() {
        for (var a = K.length - 1; a >= 0; a--)
            f(K[a].node, K[a].presenter)
    }
    function h(a) {
        for (var b = 0, c = K.length; c > b; b++)
            if (K[b].node === a)
                return b;
        return null
    }
    function i(a) {
        for (var b = 0, c = L.length; c > b; b++)
            if (L[b].node === a)
                return b;
        return null
    }
    function j(a) {
        var b = h(a);
        return null === b ? null : K[b]
    }
    function k(a) {
        -1 === a.className.indexOf("soon") && (a.className += " soon"),
        B.supportsAnimation() || (a.className += " soon-no-animation");
        var b = a.getAttribute("data-layout");
        (!b || -1 === b.indexOf("group") && -1 === b.indexOf("line")) && (b || (b = ""),
        a.setAttribute("data-layout", b + " group")),
        B.isSlow() && (a.removeAttribute("data-visual"),
        a.setAttribute("data-view", "text"),
        a.className += " soon-slow-browser")
    }
    function l(a, b, c) {
        b[c] && !a.getAttribute("data-" + c) && a.setAttribute("data-" + c, b[c])
    }
    function m(a, b) {
        return a.getAttribute("data-" + b)
    }
    function n(a, b) {
        var c = null !== a.due || null !== a.since
          , d = null;
        if (c)
            if (a.since) {
                var e = a.now ? a.now.valueOf() : (new Date).valueOf();
                d = D.chain(function(b) {
                    return a.now ? -b : b
                }, D.offset(e), D.diff(a.since.valueOf()), function(a) {
                    return Math.abs(a)
                }, function(a) {
                    return Math.max(0, a)
                }, function(b) {
                    return a.callback.onTick(b, a.since),
                    b
                }, D.event(function(a) {
                    return 0 === a
                }, b), D.duration(new Date(e), a.since, a.format, a.cascade))
            } else
                d = D.chain(D.offset(a.now.valueOf()), D.diff(a.due.valueOf()), function(a) {
                    return Math.max(0, a)
                }, function(b) {
                    return a.callback.onTick(b, a.due),
                    b
                }, D.event(function(a) {
                    return 0 >= a
                }, b), D.duration(a.now, a.due, a.format, a.cascade));
        else
            d = function() {
                var a = new Date;
                return [a.getHours(), a.getMinutes(), a.getSeconds()]
            }
            ,
            a.format = ["h", "m", "s"],
            a.separator = ":";
        return d
    }
    function o(a, b) {
        for (var c, d, e, f, g, h, i, j = null !== a.due || null !== a.since, k = n(a, b), l = {
            type: "group",
            options: {
                transform: k,
                presenters: []
            }
        }, m = [], o = a.format.length, r = 0; o > r; r++)
            h = a.format[r],
            i = r,
            c = {
                type: "group",
                options: {
                    className: "soon-group-sub",
                    presenters: []
                }
            },
            a.visual && (c.options.presenters.push(p(a, h)),
            a.reflect && c.options.presenters.push(p(a, h, "soon-reflection"))),
            d = {
                type: "text",
                options: {
                    className: "soon-label"
                }
            },
            d.options.transform = a.singular ? D.plural(a.label[h], a.label[h + "_s"]) : function(b) {
                return function() {
                    return a.label[b + "_s"]
                }
            }(h),
            e = q(a, h),
            f = null,
            a.reflect && !a.visual && (f = q(a, h, "soon-reflection")),
            c.options.presenters.push(e),
            f && c.options.presenters.push(f),
            j && c.options.presenters.push(d),
            a.separator && (g = {
                type: "group",
                options: {
                    className: "soon-group-separator",
                    presenters: [c]
                }
            },
            0 !== i && (a.reflect && g.options.presenters.unshift({
                type: "text",
                options: {
                    className: "soon-separator soon-reflection",
                    transform: function() {
                        return a.separator
                    }
                }
            }),
            g.options.presenters.unshift({
                type: "text",
                options: {
                    className: "soon-separator",
                    transform: function() {
                        return a.separator
                    }
                }
            })),
            c = g),
            m.push(c);
        return l.options.presenters = m,
        l
    }
    function p(a, b, c) {
        var d = a.visual.split(" ")
          , e = d[0];
        return d.shift(),
        {
            type: e,
            options: {
                className: "soon-visual " + (c || ""),
                transform: D.chain(D.progress(B.MAX[b]), D.cap()),
                modifiers: d,
                animate: "ms" !== b
            }
        }
    }
    function q(a, b, c) {
        var d = [];
        return a.face && (d = a.face.split(" "),
        d.shift()),
        a.chars ? {
            type: "repeater",
            options: {
                delay: "text" === a.view ? 0 : 50,
                className: "soon-value " + (c || ""),
                transform: D.chain(D.pad(a.padding[b]), D.chars()),
                presenter: {
                    type: a.view,
                    options: {
                        modifiers: d
                    }
                }
            }
        } : {
            type: "group",
            options: {
                className: "soon-group-sub-sub soon-value " + (c || ""),
                transform: D.pad(a.padding[b]),
                presenters: [{
                    type: a.view,
                    options: {
                        modifiers: d
                    }
                }]
            }
        }
    }
    function r(a, b, c, d) {
        K.push({
            node: a,
            ticker: b,
            presenter: c,
            options: d
        })
    }
    function s(a) {
        return new (t(a.type))(a.options || {})
    }
    function t(a) {
        return C[a.charAt(0).toUpperCase() + a.slice(1)]
    }
    function u(a, b) {
        var c = a.getElementsByClassName ? a.getElementsByClassName("soon-placeholder") : a.querySelectorAll("soon-placeholder");
        c.length && (c[0].innerHTML = "",
        a = c[0]);
        var d = s(b);
        return a.appendChild(d.getElement()),
        d
    }
    function v(a, b, c, d) {
        var e = new F(function(a) {
            b.setValue(a)
        }
        ,{
            rate: c
        });
        return r(a, e, b, d),
        e.start(),
        f(a, b),
        e
    }
    function w(a) {
        var b, c, d = ["labels", "padding"], e = 2, f = {
            since: m(a, "since"),
            due: m(a, "due"),
            now: m(a, "now"),
            face: m(a, "face"),
            visual: m(a, "visual"),
            format: m(a, "format"),
            singular: "true" === m(a, "singular"),
            reflect: "true" === m(a, "reflect"),
            scaleMax: m(a, "scale-max"),
            scaleHide: m(a, "scale-hide"),
            separateChars: !("false" === m(a, "separate-chars")),
            cascade: !("false" === m(a, "cascade")),
            separator: m(a, "separator"),
            padding: !("false" === m(a, "padding")),
            eventComplete: m(a, "event-complete"),
            eventTick: m(a, "event-tick")
        };
        for (var g in M)
            if (M.hasOwnProperty(g))
                for (b = M[g],
                c = 0; e > c; c++)
                    f[d[c] + b.option] = m(a, d[c] + "-" + b.option.toLowerCase());
        return A.create(a, f)
    }
    function x(a) {
        var b;
        if (0 === a.indexOf("in ")) {
            var c = a.match(N)
              , d = parseInt(c[1], 10)
              , e = c[2];
            return b = new Date,
            -1 !== e.indexOf("hour") ? b.setHours(b.getHours() + d) : -1 !== e.indexOf("minute") ? b.setMinutes(b.getMinutes() + d) : -1 !== e.indexOf("second") && b.setSeconds(b.getSeconds() + d),
            b
        }
        if (-1 !== a.indexOf("at ")) {
            b = new Date;
            var f = b.getTime()
              , g = -1 !== a.indexOf("reset");
            a = a.replace("reset ", "");
            var h = a.split("at ")
              , i = h[1].match(O)
              , j = parseInt(i[1], 10)
              , k = i[2] ? parseInt(i[2], 10) : 0
              , l = i[3] ? parseInt(i[3], 10) : 0
              , m = h[1].split(" zone ");
            if (m && (m = m[1]),
            h[0].length) {
                var n = B.getDayIndex(h[0])
                  , o = (n + 7 - b.getDay()) % 7;
                b.setDate(b.getDate() + o)
            }
            b.setHours(j),
            b.setMinutes(k),
            b.setSeconds(l),
            b.setMilliseconds(0),
            g && f >= b.getTime() && b.setHours(j + (h[0].length ? 168 : 24));
            var p = B.pad
              , q = b.getFullYear() + "-" + p(b.getMonth() + 1) + "-" + p(b.getDate())
              , r = p(b.getHours()) + ":" + p(b.getMinutes()) + ":" + p(b.getSeconds());
            a = q + "T" + r + (m || "")
        }
        return B.isoToDate(a)
    }
    function y(a, b) {
        if (0 === b.indexOf(a))
            return "";
        if ("w" === a && -1 !== b.indexOf("M"))
            return "";
        if ("d" === a) {
            if (-1 !== b.indexOf("w"))
                return "";
            if (-1 !== b.indexOf("M"))
                return "00"
        }
        return null
    }
    function z(a, b, c) {
        if (c && -1 !== G.indexOf(a))
            return c;
        var d = function(c) {
            return function() {
                c(),
                A.destroy(a),
                A.create(a, b)
            }
        }(c);
        return G.push(a),
        d
    }
    if (document.querySelectorAll && !a.Soon) {
        var A = {}
          , B = {}
          , C = {}
          , D = {}
          , E = {
            timer: 0,
            cbs: [],
            register: function(a) {
                E.cbs.push(a)
            },
            deregister: function(a) {
                for (var b = E.cbs.length - 1; b >= 0; b--)
                    E.cbs[b] === a && E.cbs.splice(b, 1)
            },
            onresize: function() {
                clearTimeout(E.timer),
                E.timer = setTimeout(function() {
                    E.resize()
                }, 100)
            },
            resize: function() {
                for (var a = 0, b = E.cbs.length; b > a; a++)
                    E.cbs[a]()
            },
            init: function() {
                a.addEventListener && a.addEventListener("resize", E.onresize, !1)
            }
        };
        E.init(),
        Function.prototype.bind || (Function.prototype.bind = function(a) {
            if ("function" != typeof this)
                throw new TypeError("Function.prototype.bind - what is trying to be bound is not callable");
            var b = Array.prototype.slice.call(arguments, 1)
              , c = this
              , d = function() {}
              , e = function() {
                return c.apply(this instanceof d && a ? this : a, b.concat(Array.prototype.slice.call(arguments)))
            };
            return d.prototype = this.prototype,
            e.prototype = new d,
            e
        }
        ),
        Array.prototype.indexOf || (Array.prototype.indexOf = function(a, b) {
            var c;
            if (null == this)
                throw new TypeError('"this" is null or not defined');
            var d = Object(this)
              , e = d.length >>> 0;
            if (0 === e)
                return -1;
            var f = +b || 0;
            if (1 / 0 === Math.abs(f) && (f = 0),
            f >= e)
                return -1;
            for (c = Math.max(f >= 0 ? f : e - Math.abs(f), 0); e > c; ) {
                if (c in d && d[c] === a)
                    return c;
                c++
            }
            return -1
        }
        ),
        function() {
            function a(a) {
                this.el = a;
                for (var b = a.className.replace(/^\s+|\s+$/g, "").split(/\s+/), c = 0; c < b.length; c++)
                    d.call(this, b[c])
            }
            function b(a, b, c) {
                Object.defineProperty ? Object.defineProperty(a, b, {
                    get: c
                }) : a.__defineGetter__(b, c)
            }
            if (!("undefined" == typeof window.Element || "classList"in document.documentElement)) {
                var c = Array.prototype
                  , d = c.push
                  , e = c.splice
                  , f = c.join;
                a.prototype = {
                    add: function(a) {
                        this.contains(a) || (d.call(this, a),
                        this.el.className = this.toString())
                    },
                    contains: function(a) {
                        return -1 != this.el.className.indexOf(a)
                    },
                    item: function(a) {
                        return this[a] || null
                    },
                    remove: function(a) {
                        if (this.contains(a)) {
                            for (var b = 0; b < this.length && this[b] != a; b++)
                                ;
                            e.call(this, b, 1),
                            this.el.className = this.toString()
                        }
                    },
                    toString: function() {
                        return f.call(this, " ")
                    },
                    toggle: function(a) {
                        return this.contains(a) ? this.remove(a) : this.add(a),
                        this.contains(a)
                    }
                },
                window.DOMTokenList = a,
                b(Element.prototype, "classList", function() {
                    return new a(this)
                })
            }
        }(),
        function() {
            for (var a = 0, b = ["webkit", "moz"], c = 0; c < b.length && !window.requestAnimationFrame; ++c)
                window.requestAnimationFrame = window[b[c] + "RequestAnimationFrame"],
                window.cancelAnimationFrame = window[b[c] + "CancelAnimationFrame"] || window[b[c] + "CancelRequestAnimationFrame"];
            window.requestAnimationFrame || (window.requestAnimationFrame = function(b) {
                var c = (new Date).getTime()
                  , d = Math.max(0, 16 - (c - a))
                  , e = window.setTimeout(function() {
                    b(c + d)
                }, d);
                return a = c + d,
                e
            }
            ),
            window.cancelAnimationFrame || (window.cancelAnimationFrame = function(a) {
                clearTimeout(a)
            }
            )
        }(),
        B = function() {
            function a() {
                if (!window.getComputedStyle)
                    return !1;
                var a, b = document.createElement("div"), d = {
                    webkitTransform: "-webkit-transform",
                    OTransform: "-o-transform",
                    msTransform: "-ms-transform",
                    MozTransform: "-moz-transform",
                    transform: "transform"
                };
                document.body.insertBefore(b, null);
                for (var e in d)
                    b.style[e] !== c && (b.style[e] = "translate3d(1px,1px,1px)",
                    a = window.getComputedStyle(b).getPropertyValue(d[e]));
                return document.body.removeChild(b),
                a !== c && a.length > 0 && "none" !== a
            }
            function b() {
                var a = !1
                  , b = "animation"
                  , d = ""
                  , e = "Webkit Moz O ms Khtml".split(" ")
                  , f = ""
                  , g = 0
                  , h = document.body
                  , i = e.length;
                if (h.style.animationName !== c && (a = !0),
                a === !1)
                    for (; i > g; g++)
                        if (h.style[e[g] + "AnimationName"] !== c) {
                            f = e[g],
                            b = f + "Animation",
                            d = "-" + f.toLowerCase() + "-",
                            a = !0;
                            break
                        }
                return a
            }
            var d, e, f = "textContent"in document.documentElement, g = function(a) {
                var b, c, d = /^(\d{4}\-\d\d\-\d\d([tT ][\d:\.]*)?)([zZ]|([+\-])(\d\d):(\d\d))?$/, e = d.exec(a) || [];
                if (e[1]) {
                    b = e[1].split(/\D/);
                    for (var f = 0, g = b.length; g > f; f++)
                        b[f] = parseInt(b[f], 10) || 0;
                    return b[1] -= 1,
                    b = new Date(Date.UTC.apply(Date, b)),
                    b.getDate() ? (e[5] && (c = 60 * parseInt(e[5], 10),
                    e[6] && (c += parseInt(e[6], 10)),
                    "+" == e[4] && (c *= -1),
                    c && b.setUTCMinutes(b.getUTCMinutes() + c)),
                    b) : Number.NaN
                }
                return Number.NaN
            }, h = new Date("2015-01-01T12:00:00.123+01:00"), i = isNaN(h) ? function(a) {
                return g(a)
            }
            : function(a) {
                return new Date(a)
            }
            ;
            "undefined" != typeof document.hidden ? (e = "hidden",
            d = "visibilitychange") : "undefined" != typeof document.mozHidden ? (e = "mozHidden",
            d = "mozvisibilitychange") : "undefined" != typeof document.msHidden ? (e = "msHidden",
            d = "msvisibilitychange") : "undefined" != typeof document.webkitHidden && (e = "webkitHidden",
            d = "webkitvisibilitychange");
            var j = !1
              , k = 1
              , l = 1e3 * k
              , m = 60 * l
              , n = 60 * m
              , o = 24 * n
              , p = 7 * o
              , q = {
                MAX: {
                    y: 100,
                    M: 12,
                    w: 52,
                    d: 365,
                    h: 24,
                    m: 60,
                    s: 60,
                    ms: 1e3
                },
                AMOUNT: {
                    w: p,
                    d: o,
                    h: n,
                    m: m,
                    s: l,
                    ms: k
                },
                NAMES: {
                    y: "years",
                    M: "months",
                    w: "weeks",
                    d: "days",
                    h: "hours",
                    m: "minutes",
                    s: "seconds",
                    ms: "milliseconds"
                },
                FORMATS: ["y", "M", "w", "d", "h", "m", "s", "ms"],
                CIRC: 2 * Math.PI,
                QUART: .5 * Math.PI,
                DAYS: ["su", "mo", "tu", "we", "th", "fr", "sa"],
                setText: null,
                documentVisibilityEvent: d,
                pad: function(a) {
                    return ("00" + a).slice(-2)
                },
                getDayIndex: function(a) {
                    return this.DAYS.indexOf(a.substr(0, 2))
                },
                isSlow: function() {
                    return !f
                },
                supportsAnimation: function() {
                    return j = b() && a(),
                    q.supportsAnimation = function() {
                        return j
                    }
                    ,
                    j
                },
                toArray: function(a) {
                    return Array.prototype.slice.call(a)
                },
                toBoolean: function(a) {
                    return "string" == typeof a ? "true" === a : a
                },
                isoToDate: function(a) {
                    if (a.match(/(Z)|([+\-][0-9]{2}:?[0-9]*$)/g))
                        return i(a);
                    a += -1 !== a.indexOf("T") ? "Z" : "";
                    var b = i(a);
                    return this.dateToLocal(b)
                },
                dateToLocal: function(a) {
                    return new Date(a.getTime() + 6e4 * a.getTimezoneOffset())
                },
                prefix: function() {
                    for (var a, b = ["webkit", "Moz", "ms", "O"], c = 0, d = b.length, e = document.createElement("div").style; d > c; c++)
                        if (a = b[c] + "Transform",
                        a in e)
                            return b[c];
                    return null
                }(),
                setTransform: function(a, b) {
                    a.style[this.prefix + "Transform"] = b,
                    a.style.transform = b
                },
                setTransitionDelay: function(a, b) {
                    a.style[this.prefix + "TransitionDelay"] = b + "," + b + "," + b,
                    a.style.TransitionDelay = b + "," + b + "," + b
                },
                getShadowProperties: function(a) {
                    if (a = a ? a.match(/(-?\d+px)|(rgba\(.+\))|(rgb\(.+\))|(#[abcdef\d]+)/g) : null,
                    !a)
                        return null;
                    for (var b, c = 0, d = a.length, e = []; d > c; c++)
                        -1 !== a[c].indexOf("px") ? e.push(parseInt(a[c], 10)) : b = a[c];
                    return e.push(b),
                    5 === e.length && e.splice(3, 1),
                    e
                },
                getDevicePixelRatio: function() {
                    return window.devicePixelRatio || 1
                },
                isDocumentHidden: function() {
                    return e ? document[e] : !1
                },
                triggerAnimation: function(a, b) {
                    a.classList.remove(b),
                    window.requestAnimationFrame(function() {
                        a.offsetLeft,
                        a.classList.add(b)
                    })
                },
                getBackingStoreRatio: function(a) {
                    return a.webkitBackingStorePixelRatio || a.mozBackingStorePixelRatio || a.msBackingStorePixelRatio || a.oBackingStorePixelRatio || a.backingStorePixelRatio || 1
                },
                setShadow: function(a, b, c, d, e) {
                    a.shadowOffsetX = b,
                    a.shadowOffsetY = c,
                    a.shadowBlur = d,
                    a.shadowColor = e
                },
                getColorBetween: function(a, b, c) {
                    function d(a, b) {
                        return a + Math.round((b - a) * c)
                    }
                    function e(a) {
                        a = Math.min(a, 255),
                        a = Math.max(a, 0);
                        var b = a.toString(16);
                        return b.length < 2 && (b = "0" + b),
                        b
                    }
                    return "#" + e(d(a.r, b.r)) + e(d(a.g, b.g)) + e(d(a.b, b.b))
                },
                getGradientColors: function(a, b, c) {
                    for (var d = [], e = 0, f = c, g = 1 / (f - 1), h = 0; f > e; e++)
                        d[e] = this.getColorBetween(a, b, h),
                        h += g;
                    return d
                },
                hexToRgb: function(a) {
                    var b = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(a);
                    return b ? {
                        r: parseInt(b[1], 16),
                        g: parseInt(b[2], 16),
                        b: parseInt(b[3], 16)
                    } : null
                },
                drawGradientArc: function(a, b, c, d, e, f, g, h, i, j, k, l, m) {
                    if (!(g > h)) {
                        l && this.drawArc(a, b, c, d, e, f, g, h, i, "transparent", l, m);
                        for (var n, o, p, q, r, s, t, u = this.hexToRgb(j), v = this.hexToRgb(k), w = this.hexToRgb(this.getColorBetween(u, v, (g - e) / f)), x = this.hexToRgb(this.getColorBetween(u, v, (h - e) / f)), y = h - g, z = Math.ceil(30 * y), A = this.getGradientColors(w, x, z), B = -this.QUART + this.CIRC * g, C = A.length, D = 0, E = this.CIRC * y / C; C > D; D++)
                            o = A[D],
                            p = A[D + 1] || o,
                            q = b + Math.cos(B) * d,
                            s = b + Math.cos(B + E) * d,
                            r = c + Math.sin(B) * d,
                            t = c + Math.sin(B + E) * d,
                            a.beginPath(),
                            n = a.createLinearGradient(q, r, s, t),
                            n.addColorStop(0, o),
                            n.addColorStop(1, p),
                            a.lineCap = m,
                            a.strokeStyle = n,
                            a.arc(b, c, d, B - .005, B + E + .005),
                            a.lineWidth = i,
                            a.stroke(),
                            a.closePath(),
                            B += E
                    }
                },
                drawArc: function(a, b, c, d, e, f, g, h, i, j, k, l) {
                    if (!(g > h)) {
                        if (null !== j.gradient.colors && "follow" === j.gradient.type)
                            return void this.drawGradientArc(a, b, c, d, e, f, g, h, i, j.gradient.colors[0], j.gradient.colors[1], k, l);
                        if (k) {
                            var m = "transparent" === j.fill ? 9999 : 0;
                            a.save(),
                            a.translate(m, 0),
                            this.setShadow(a, k[0] - m, k[1], k[2], k[3])
                        }
                        if (a.beginPath(),
                        a.lineWidth = i,
                        a.arc(b, c, d, -this.QUART + this.CIRC * g, -this.QUART + this.CIRC * h, !1),
                        j.gradient.colors) {
                            var n = "horizontal" === j.gradient.type ? a.createLinearGradient(0, d, 2 * d, d) : a.createLinearGradient(d, 0, d, 2 * d);
                            n.addColorStop(0, j.gradient.colors[0]),
                            n.addColorStop(1, j.gradient.colors[1]),
                            a.strokeStyle = n
                        } else
                            a.strokeStyle = "transparent" === j.fill ? "#000" : j.fill;
                        a.lineCap = l,
                        a.stroke(),
                        k && a.restore()
                    }
                },
                drawRing: function(a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p) {
                    d + e > 1 && (d -= -1 + d + e,
                    c += .5 * e);
                    var q = c
                      , r = c + d
                      , s = b * d
                      , t = .5 - Math.abs(-.5 + b)
                      , u = c + (s - t * e)
                      , v = c + (s + (1 - t) * e);
                    (g || k) && (p ? (this.drawArc(a, f, f, g, c, d, v, r, h, i, j, o),
                    this.drawArc(a, f, f, k, c, d, q, u, l, m, n, o)) : (this.drawArc(a, f, f, g, c, d, q, u, h, i, j, o),
                    this.drawArc(a, f, f, k, c, d, v, r, l, m, n, o)))
                },
                setTextContent: function() {
                    return f ? function(a, b) {
                        a.textContent = b
                    }
                    : function(a, b) {
                        a.innerText = b
                    }
                }()
            };
            return q
        }(),
        D.cap = function(a, b) {
            return a = a || 0,
            b = b || 1,
            function(c) {
                return Math.min(Math.max(c, a), b)
            }
        }
        ,
        D.chain = function(a) {
            return function() {
                var b, c = a.toArray(arguments), d = c.length;
                return function(a) {
                    for (b = 0; d > b; b++)
                        a = c[b](a);
                    return a
                }
            }
        }(B),
        D.chars = function() {
            return function(a) {
                return (a + "").split("")
            }
        }
        ,
        D.diff = function(a) {
            return function(b) {
                return a - b
            }
        }
        ,
        D.duplicate = function(a) {
            var b, c = new Array(a);
            return function(d) {
                for (b = a; b--; )
                    c[b] = d;
                return c
            }
        }
        ,
        D.duration = function(a) {
            function b(a, b) {
                return a.setMonth(a.getMonth() + b),
                a
            }
            function c(a) {
                return new Date(a.valueOf())
            }
            function d(a, b) {
                return -1 !== b.indexOf(a)
            }
            function e(a, d) {
                var e, f, g = 12 * (d.getFullYear() - a.getFullYear()) + (d.getMonth() - a.getMonth()), h = b(c(a), g);
                return 0 > d - h ? (e = b(c(a), g - 1),
                f = (d - h) / (h - e)) : (e = b(c(a), g + 1),
                f = (d - h) / (e - h)),
                -(g + f)
            }
            var f = a.FORMATS
              , g = f.length
              , h = {
                M: 1,
                y: 12
            };
            return function(i, j, k, l) {
                var m = d("M", k)
                  , n = d("y", k);
                return function(j) {
                    var o, p, q, r, s, t, u = 0, v = [];
                    for ((m || n || !l) && (o = new Date(i.valueOf() + j),
                    p = e(o, i),
                    t = m ? Math.floor(p) : 12 * Math.floor(p / 12),
                    j = o.valueOf() - b(c(i), t).valueOf()); g > u; u++)
                        r = f[u],
                        2 > u ? (q = Math.floor(p / h[r]),
                        d(r, k) ? (p -= q * h[r],
                        v.push(Math.max(0, q))) : l || (p -= q * h[r])) : (s = a.AMOUNT[r],
                        q = Math.floor(j / s),
                        d(r, k) ? (j %= s,
                        v.push(Math.max(0, q))) : l || (j %= s));
                    return v
                }
            }
        }(B),
        D.event = function(a, b) {
            return function(c) {
                return a(c) && b(),
                c
            }
        }
        ,
        D.modulate = function(a) {
            return function(b) {
                return parseInt(b, 10) % 2 === 0 ? a : ""
            }
        }
        ,
        D.now = function() {
            return function() {
                return (new Date).getTime()
            }
        }
        ,
        D.offset = function(a) {
            return function(b) {
                return a + b
            }
        }
        ,
        D.pad = function(a) {
            return a = a || "",
            function(b) {
                return (a + b).slice(-a.length)
            }
        }
        ,
        D.plural = function(a, b) {
            return function(c) {
                return 1 === parseInt(c, 10) ? a : b
            }
        }
        ,
        D.progress = function(a, b) {
            return function(c) {
                return c = parseInt(c, 10),
                b > a ? c / b : (a - c) / a
            }
        }
        ,
        C.Console = function() {
            var a = function(a) {
                this._transform = a.transform || function(a) {
                    return a
                }
            };
            return a.prototype = {
                redraw: function() {},
                destroy: function() {
                    return null
                },
                getElement: function() {
                    return null
                },
                setValue: function(a) {
                    console.log(this._transform(a))
                }
            },
            a
        }(),
        C.Fill = function(a) {
            var b = function(a) {
                this._wrapper = document.createElement("span"),
                this._wrapper.className = "soon-fill " + (a.className || ""),
                this._transform = a.transform || function(a) {
                    return a
                }
                ,
                this._direction = "to-top";
                for (var b = 0, c = a.modifiers.length; c > b; b++)
                    if (0 === a.modifiers[b].indexOf("to-")) {
                        this._direction = a.modifiers[b];
                        break
                    }
                this._fill = document.createElement("span"),
                this._fill.className = "soon-fill-inner",
                this._progress = document.createElement("span"),
                this._progress.className = "soon-fill-progress",
                this._fill.appendChild(this._progress),
                this._wrapper.appendChild(this._fill)
            };
            return b.prototype = {
                redraw: function() {},
                destroy: function() {
                    return this._wrapper
                },
                getElement: function() {
                    return this._wrapper
                },
                setValue: function(b) {
                    var c, d = this._transform(b);
                    switch (this._direction) {
                    case "to-top":
                        c = "translateY(" + (100 - 100 * d) + "%)";
                        break;
                    case "to-top-right":
                        c = "scale(1.45) rotateZ(-45deg) translateX(" + (-100 + 100 * d) + "%)";
                        break;
                    case "to-top-left":
                        c = "scale(1.45) rotateZ(45deg) translateX(" + (100 - 100 * d) + "%)";
                        break;
                    case "to-left":
                        c = "translateX(" + (100 - 100 * d) + "%)";
                        break;
                    case "to-right":
                        c = "translateX(" + (-100 + 100 * d) + "%)";
                        break;
                    case "to-bottom-right":
                        c = "scale(1.45) rotateZ(45deg) translateX(" + (-100 + 100 * d) + "%)";
                        break;
                    case "to-bottom-left":
                        c = "scale(1.45) rotateZ(-45deg) translateX(" + (100 - 100 * d) + "%)";
                        break;
                    case "to-bottom":
                        c = "translateY(" + (-100 + 100 * d) + "%)"
                    }
                    a.setTransform(this._progress, c)
                }
            },
            b
        }(B),
        C.Flip = function(a) {
            var b = function(b) {
                this._wrapper = document.createElement("span"),
                this._wrapper.className = "soon-flip " + (b.className || ""),
                this._transform = b.transform || function(a) {
                    return a
                }
                ,
                this._inner = document.createElement("span"),
                this._inner.className = "soon-flip-inner",
                this._card = document.createElement("span"),
                this._card.className = "soon-flip-card",
                a.supportsAnimation() ? (this._front = document.createElement("span"),
                this._front.className = "soon-flip-front soon-flip-face",
                this._back = document.createElement("span"),
                this._back.className = "soon-flip-back soon-flip-face",
                this._card.appendChild(this._front),
                this._card.appendChild(this._back),
                this._top = document.createElement("span"),
                this._top.className = "soon-flip-top soon-flip-face",
                this._card.appendChild(this._top),
                this._bottom = document.createElement("span"),
                this._bottom.className = "soon-flip-bottom soon-flip-face",
                this._card.appendChild(this._bottom)) : (this._fallback = document.createElement("span"),
                this._fallback.className = "soon-flip-fallback",
                this._card.appendChild(this._fallback)),
                this._bounding = document.createElement("span"),
                this._bounding.className = "soon-flip-bounding",
                this._card.appendChild(this._bounding),
                this._inner.appendChild(this._card),
                this._wrapper.appendChild(this._inner),
                this._frontValue = null,
                this._backValue = null,
                this._boundingLength = 0
            };
            return b.prototype = {
                redraw: function() {},
                _setBoundingForValue: function(a) {
                    var b = (a + "").length;
                    if (b !== this._boundingLength) {
                        this._boundingLength = b;
                        for (var c = "", d = 0; b > d; d++)
                            c += "8";
                        this._bounding.textContent = c;
                        var e = parseInt(getComputedStyle(this._card).fontSize, 10)
                          , f = this._bounding.offsetWidth / e;
                        this._inner.style.width = f + .1 * (b - 1) + "em"
                    }
                },
                destroy: function() {
                    return this._wrapper
                },
                getElement: function() {
                    return this._wrapper
                },
                setValue: function(b) {
                    return b = this._transform(b),
                    a.supportsAnimation() ? this._frontValue ? void (this._backValue && this._backValue === b || this._frontValue === b || (this._backValue && (this._bottom.textContent = this._backValue,
                    this._front.textContent = this._backValue,
                    this._frontValue = this._backValue),
                    this._setBoundingForValue(b),
                    this._top.textContent = b,
                    this._back.textContent = b,
                    this._backValue = b,
                    a.triggerAnimation(this._inner, "soon-flip-animate"))) : (this._bottom.textContent = b,
                    this._front.textContent = b,
                    this._frontValue = b,
                    void this._setBoundingForValue(b)) : (this._fallback.textContent = b,
                    void this._setBoundingForValue(b))
                }
            },
            b
        }(B),
        C.Group = function(a) {
            var b = function(a) {
                this._wrapper = document.createElement("span"),
                this._wrapper.className = "soon-group " + (a.className || ""),
                this._inner = document.createElement("span"),
                this._inner.className = "soon-group-inner",
                this._wrapper.appendChild(this._inner),
                this._transform = a.transform || function(a) {
                    return a
                }
                ,
                this._presenters = a.presenters,
                this._presenterStorage = []
            };
            return b.prototype = {
                redraw: function() {
                    for (var a = this._presenterStorage.length - 1; a >= 0; a--)
                        this._presenterStorage[a].redraw()
                },
                destroy: function() {
                    for (var a = this._presenterStorage.length - 1; a >= 0; a--)
                        this._presenterStorage[a].destroy();
                    return this._wrapper
                },
                getElement: function() {
                    return this._wrapper
                },
                setValue: function(b) {
                    this._wrapper.setAttribute("data-value", b),
                    b = this._transform(b);
                    for (var c, d = 0, e = b instanceof Array, f = e ? b.length : this._presenters.length; f > d; d++)
                        c = this._presenterStorage[d],
                        c || (c = a(this._presenters[d]),
                        this._inner.appendChild(c.getElement()),
                        this._presenterStorage[d] = c),
                        c.setValue(e ? b[d] : b)
                }
            },
            b
        }(s),
        C.Matrix = function() {
            var a = {
                "3x5": {
                    " ": [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
                    0: [[1, 1, 1], [1, 0, 1], [1, 0, 1], [1, 0, 1], [1, 1, 1]],
                    1: [[1, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0]],
                    2: [[1, 1, 1], [0, 0, 1], [1, 1, 1], [1, 0, 0], [1, 1, 1]],
                    3: [[1, 1, 1], [0, 0, 1], [1, 1, 1], [0, 0, 1], [1, 1, 1]],
                    4: [[1, 0, 1], [1, 0, 1], [1, 1, 1], [0, 0, 1], [0, 0, 1]],
                    5: [[1, 1, 1], [1, 0, 0], [1, 1, 1], [0, 0, 1], [1, 1, 1]],
                    6: [[1, 1, 1], [1, 0, 0], [1, 1, 1], [1, 0, 1], [1, 1, 1]],
                    7: [[1, 1, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1]],
                    8: [[1, 1, 1], [1, 0, 1], [1, 1, 1], [1, 0, 1], [1, 1, 1]],
                    9: [[1, 1, 1], [1, 0, 1], [1, 1, 1], [0, 0, 1], [1, 1, 1]]
                },
                "5x7": {
                    " ": [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
                    0: [[0, 1, 1, 1, 0], [1, 1, 0, 1, 1], [1, 1, 0, 1, 1], [1, 1, 0, 1, 1], [1, 1, 0, 1, 1], [1, 1, 0, 1, 1], [0, 1, 1, 1, 0]],
                    1: [[0, 0, 1, 1, 0], [0, 1, 1, 1, 0], [0, 0, 1, 1, 0], [0, 0, 1, 1, 0], [0, 0, 1, 1, 0], [0, 0, 1, 1, 0], [0, 1, 1, 1, 1]],
                    2: [[0, 1, 1, 1, 0], [1, 1, 0, 1, 1], [0, 0, 0, 1, 1], [0, 0, 1, 1, 0], [0, 1, 1, 0, 0], [1, 1, 0, 0, 0], [1, 1, 1, 1, 1]],
                    3: [[0, 1, 1, 1, 0], [1, 1, 0, 1, 1], [0, 0, 0, 1, 1], [0, 0, 1, 1, 0], [0, 0, 0, 1, 1], [1, 1, 0, 1, 1], [0, 1, 1, 1, 0]],
                    4: [[0, 0, 1, 1, 1], [0, 1, 0, 1, 1], [1, 1, 0, 1, 1], [1, 1, 1, 1, 1], [0, 0, 0, 1, 1], [0, 0, 0, 1, 1], [0, 0, 0, 1, 1]],
                    5: [[1, 1, 1, 1, 1], [1, 1, 0, 0, 0], [1, 1, 0, 0, 0], [1, 1, 1, 1, 0], [0, 0, 0, 1, 1], [1, 1, 0, 1, 1], [0, 1, 1, 1, 0]],
                    6: [[0, 1, 1, 1, 0], [1, 1, 0, 0, 0], [1, 1, 1, 1, 0], [1, 1, 0, 1, 1], [1, 1, 0, 1, 1], [1, 1, 0, 1, 1], [0, 1, 1, 1, 0]],
                    7: [[1, 1, 1, 1, 1], [0, 0, 0, 1, 1], [0, 0, 0, 1, 1], [0, 0, 1, 1, 0], [0, 1, 1, 0, 0], [1, 1, 0, 0, 0], [1, 1, 0, 0, 0]],
                    8: [[0, 1, 1, 1, 0], [1, 1, 0, 1, 1], [1, 1, 0, 1, 1], [0, 1, 1, 1, 0], [1, 1, 0, 1, 1], [1, 1, 0, 1, 1], [0, 1, 1, 1, 0]],
                    9: [[0, 1, 1, 1, 0], [1, 1, 0, 1, 1], [1, 1, 0, 1, 1], [1, 1, 0, 1, 1], [0, 1, 1, 1, 1], [0, 0, 0, 1, 1], [0, 1, 1, 1, 0]]
                }
            }
              , b = function() {
                var b, c, d, e, f, g, h = [];
                for (d in a)
                    if (a.hasOwnProperty(d)) {
                        for (b = a[d][0].length,
                        c = a[d][0][0].length,
                        g = "",
                        e = 0; b > e; e++) {
                            for (g += '<span class="soon-matrix-row">',
                            f = 0; c > f; f++)
                                g += '<span class="soon-matrix-dot"></span>';
                            g += "</span>"
                        }
                        h[d] = g
                    }
                return h
            }()
              , c = function(a) {
                this._wrapper = document.createElement("span"),
                this._wrapper.className = "soon-matrix " + (a.className || ""),
                this._inner = document.createElement("span"),
                this._inner.className = "soon-matrix-inner",
                this._wrapper.appendChild(this._inner),
                this._transform = a.transform || function(a) {
                    return a
                }
                ,
                this._value = [],
                this._type = -1 !== a.modifiers.indexOf("3x5") ? "3x5" : "5x7"
            };
            return c.prototype = {
                redraw: function() {},
                destroy: function() {
                    return this._wrapper
                },
                getElement: function() {
                    return this._wrapper
                },
                _addChar: function() {
                    var a = document.createElement("span");
                    return a.className = "soon-matrix-char",
                    a.innerHTML = b[this._type],
                    {
                        node: a,
                        ref: []
                    }
                },
                _updateChar: function(b, c) {
                    var d, e = a[this._type][c], f = e.length, g = e[0].length, h = 0, i = b.ref;
                    if (!i.length)
                        for (var j = b.node.getElementsByClassName("soon-matrix-dot"); f > h; h++)
                            for (i[h] = [],
                            d = 0; g > d; d++)
                                i[h][d] = j[h * g + d];
                    for (; f > h; h++)
                        for (d = 0; g > d; d++)
                            i[h][d].setAttribute("data-state", 1 === e[h][d] ? "1" : "0")
                },
                setValue: function(a) {
                    a = this._transform(a),
                    a += "",
                    a = a.split("");
                    for (var b = 0, c = a.length; c > b; b++) {
                        var d = this._value[b];
                        d || (d = this._addChar(),
                        this._inner.appendChild(d.node),
                        this._value[b] = d),
                        this._updateChar(d, a[b])
                    }
                }
            },
            c
        }(),
        C.Repeater = function(a) {
            var b = function(b) {
                this._wrapper = document.createElement("span"),
                this._wrapper.className = "soon-repeater " + (b.className || ""),
                this._delay = b.delay || 0,
                this._transform = b.transform || function(a) {
                    return a
                }
                ,
                this._destroyed = !1,
                this._presenter = b.presenter,
                this._Presenter = a(this._presenter.type),
                this._prepend = "undefined" == typeof b.prepend ? !0 : b.prepend,
                this._presenterStorage = []
            };
            return b.prototype = {
                redraw: function() {
                    for (var a = this._presenterStorage.length - 1; a >= 0; a--)
                        this._presenterStorage[a].redraw()
                },
                destroy: function() {
                    this._destroyed = !0;
                    for (var a = this._presenterStorage.length - 1; a >= 0; a--)
                        this._presenterStorage[a].destroy();
                    return this._wrapper
                },
                getElement: function() {
                    return this._wrapper
                },
                setValue: function(a) {
                    a = this._transform(a),
                    a = a instanceof Array ? a : [a],
                    this._prepend && a.reverse();
                    for (var b, c, d, e = 0, f = a.length, g = 0, h = a.length !== this._wrapper.children.length; f > e; e++)
                        b = this._presenterStorage[e],
                        b || (b = new this._Presenter(this._presenter.options || {}),
                        0 !== this._wrapper.children.length && this._prepend ? this._wrapper.insertBefore(b.getElement(), this._wrapper.firstChild) : this._wrapper.appendChild(b.getElement()),
                        this._presenterStorage[e] = b,
                        this._delay && (g -= this._delay)),
                        this._delay && !h ? (this._setValueDelayed(b, a[e], g),
                        g += this._delay) : this._setValue(b, a[e], h);
                    for (f = this._wrapper.children.length,
                    d = e; f > e; e++)
                        b = this._presenterStorage[e],
                        c = b.destroy(),
                        c.parentNode.removeChild(c),
                        this._presenterStorage[e] = null;
                    this._presenterStorage.length = d
                },
                _setValueDelayed: function(a, b, c, d) {
                    var e = this;
                    setTimeout(function() {
                        e._setValue(a, b, d)
                    }, c)
                },
                _setValue: function(a, b, c) {
                    c && a.setValue(" "),
                    a.setValue(b)
                }
            },
            b
        }(t),
        C.Ring = function(a, b) {
            var c = function(b) {
                this._wrapper = document.createElement("span"),
                this._wrapper.className = "soon-ring " + (b.className || ""),
                this._transform = b.transform || function(a) {
                    return a
                }
                ,
                this._modifiers = b.modifiers,
                this._animate = b.animate,
                this._drawn = !1,
                this._canvas = document.createElement("canvas"),
                this._wrapper.appendChild(this._canvas),
                this._style = document.createElement("span"),
                this._style.className = "soon-ring-progress",
                this._style.style.visibility = "hidden",
                this._style.style.position = "absolute",
                this._wrapper.appendChild(this._style),
                this._current = 0,
                this._target = null,
                this._destroyed = !1,
                this._lastTick = 0,
                this._styles = null;
                var c = this;
                a.supportsAnimation() ? window.requestAnimationFrame(function(a) {
                    c._tick(a)
                }) : this._animate = !1
            };
            return c.prototype = {
                destroy: function() {
                    return this._destroyed = !0,
                    b.deregister(this._resizeBind),
                    this._wrapper
                },
                getElement: function() {
                    return this._wrapper
                },
                _getModifier: function(a) {
                    for (var b = 0, c = this._modifiers.length, d = null; c > b; b++)
                        if (-1 !== this._modifiers[b].indexOf(a)) {
                            d = this._modifiers[b];
                            break
                        }
                    if (!d)
                        return null;
                    if (-1 === d.indexOf("-"))
                        return !0;
                    var e = d.split("-");
                    if (-1 !== e[1].indexOf("_")) {
                        var f = e[1].split("_");
                        return f[0] = "#" + f[0],
                        f[1] = "#" + f[1],
                        f
                    }
                    var g = parseFloat(e[1]);
                    return isNaN(g) ? e[1] : g / 100
                },
                redraw: function() {
                    var b = window.getComputedStyle(this._style);
                    this._styles = {
                        offset: this._getModifier("offset") || 0,
                        gap: this._getModifier("gap") || 0,
                        length: this._getModifier("length") || 1,
                        flip: this._getModifier("flip") || !1,
                        invert: this._getModifier("invert") || null,
                        align: "center",
                        size: 0,
                        radius: 0,
                        padding: parseInt(b.getPropertyValue("padding-bottom"), 10) || 0,
                        cap: 0 === parseInt(b.getPropertyValue("border-top-right-radius"), 10) ? "butt" : "round",
                        progressColor: {
                            fill: b.getPropertyValue("color") || "#000",
                            gradient: {
                                colors: this._getModifier("progressgradient") || null,
                                type: this._getModifier("progressgradienttype") || "follow"
                            }
                        },
                        progressWidth: parseInt(b.getPropertyValue("border-top-width"), 10) || 2,
                        progressShadow: a.getShadowProperties(b.getPropertyValue("text-shadow")),
                        ringColor: {
                            fill: b.getPropertyValue("background-color") || "#fff",
                            gradient: {
                                colors: this._getModifier("ringgradient") || null,
                                type: this._getModifier("ringgradienttype") || "follow"
                            }
                        },
                        ringWidth: parseInt(b.getPropertyValue("border-bottom-width"), 10) || 2,
                        ringShadow: a.getShadowProperties(b.getPropertyValue("box-shadow"))
                    };
                    var c = this._canvas.getContext("2d")
                      , d = this._canvas.parentNode.clientWidth
                      , e = a.getDevicePixelRatio()
                      , f = a.getBackingStoreRatio(c)
                      , g = e / f
                      , h = 125 > d ? Math.min(1, .005 * d) : 1;
                    if (this._styles.ringWidth = Math.ceil(this._styles.ringWidth * h),
                    this._styles.progressWidth = Math.ceil(this._styles.progressWidth * h),
                    "transparent" === this._styles.ringColor.fill && (this._styles.ringColor.fill = "rgba(0,0,0,0)"),
                    "transparent" === this._styles.progressColor.fill && (this._styles.progressColor.fill = "rgba(0,0,0,0)"),
                    "round" === this._styles.cap && -1 === this._modifiers.join("").indexOf("gap-") && (this._styles.gap = .5 * (this._styles.ringWidth + this._styles.progressWidth) * .005),
                    d) {
                        e !== f ? (this._canvas.width = d * g,
                        this._canvas.height = d * g,
                        this._canvas.style.width = d + "px",
                        this._canvas.style.height = d + "px",
                        c.scale(g, g)) : (this._canvas.width = d,
                        this._canvas.height = d),
                        this._styles.size = .5 * d;
                        var i = this._styles.size - this._styles.padding;
                        this._styles.ringRadius = i - .5 * this._styles.ringWidth,
                        this._styles.progressRadius = i - .5 * this._styles.progressWidth,
                        this._styles.progressWidth === this._styles.ringWidth ? this._styles.progressRadius = this._styles.ringRadius : this._styles.progressWidth < this._styles.ringWidth ? -1 !== this._modifiers.indexOf("align-center") ? this._styles.progressRadius = this._styles.ringRadius : -1 !== this._modifiers.indexOf("align-bottom") ? this._styles.progressRadius = i - (this._styles.ringWidth - .5 * this._styles.progressWidth) : -1 !== this._modifiers.indexOf("align-inside") && (this._styles.progressRadius = i - (this._styles.ringWidth + .5 * this._styles.progressWidth)) : -1 !== this._modifiers.indexOf("align-center") ? this._styles.ringRadius = this._styles.progressRadius : -1 !== this._modifiers.indexOf("align-bottom") ? this._styles.ringRadius = i - (this._styles.progressWidth - .5 * this._styles.ringWidth) : -1 !== this._modifiers.indexOf("align-inside") && (this._styles.ringRadius = i - (this._styles.progressWidth + .5 * this._styles.ringWidth)),
                        -1 !== this._modifiers.indexOf("glow-progress") && this._styles.progressShadow && (this._styles.progressShadow[this._styles.progressShadow.length - 1] = null !== this._styles.progressColor.gradient.colors ? this._styles.progressColor.gradient.colors[0] : this._styles.progressColor.fill),
                        -1 !== this._modifiers.indexOf("glow-background") && this._styles.ringShadow && (this._styles.ringShadow[this._styles.ringShadow.length - 1] = null !== this._styles.ringColor.gradient.colors ? this._styles.ringColor.gradient.colors[0] : this._styles.ringColor.fill),
                        this._drawn = !1
                    }
                },
                _tick: function(a) {
                    if (!this._destroyed) {
                        null !== this._target && this._draw(a);
                        var b = this;
                        window.requestAnimationFrame(function(a) {
                            b._tick(a)
                        })
                    }
                },
                _draw: function(b) {
                    if (this._animate) {
                        var c = b - this._lastTick
                          , d = 250 > c ? 1e3 / c : 30;
                        if (this._lastTick = b,
                        this._current === this._target && this._drawn)
                            return;
                        this._current += (this._target - this._current) / (d / 3),
                        Math.abs(this._current - this._target) <= .001 && (this._current = this._target)
                    } else
                        this._current = this._target;
                    var e = this._canvas.getContext("2d");
                    e.clearRect(0, 0, this._canvas.width, this._canvas.height);
                    var f = this._styles.flip ? 1 - this._current : this._current;
                    a.drawRing(e, f, this._styles.offset, this._styles.length, this._styles.gap, this._styles.size, this._styles.ringRadius, this._styles.ringWidth, this._styles.ringColor, this._styles.ringShadow, this._styles.progressRadius, this._styles.progressWidth, this._styles.progressColor, this._styles.progressShadow, this._styles.cap, this._styles.invert),
                    this._drawn = !0
                },
                setValue: function(b) {
                    this._styles || this.redraw(),
                    b = this._transform(b),
                    this._target !== b && (null == this._target && (this._current = b),
                    this._target = b),
                    a.supportsAnimation() || (this._current = this._target,
                    this._draw())
                }
            },
            c
        }(B, E),
        C.Slot = function(a) {
            var b = function(a) {
                this._forceReplace = "undefined" == typeof a.forceReplace ? !1 : a.forceReplace,
                this._wrapper = document.createElement("span"),
                this._wrapper.className = "soon-slot " + (a.className || ""),
                this._transform = a.transform || function(a) {
                    return a
                }
                ,
                this._new = document.createElement("span"),
                this._new.className = "soon-slot-new",
                this._old = document.createElement("span"),
                this._old.className = "soon-slot-old",
                this._bounding = document.createElement("span"),
                this._bounding.className = "soon-slot-bounding",
                this._inner = document.createElement("span"),
                this._inner.className = "soon-slot-inner soon-slot-animate",
                this._inner.appendChild(this._old),
                this._inner.appendChild(this._new),
                this._inner.appendChild(this._bounding),
                this._wrapper.appendChild(this._inner),
                this._newValue = "",
                this._oldValue = "",
                this._boundingLength = 0
            };
            return b.prototype = {
                redraw: function() {},
                destroy: function() {
                    return this._wrapper
                },
                getElement: function() {
                    return this._wrapper
                },
                _isEmpty: function() {
                    return !this._newValue
                },
                _isSame: function(a) {
                    return this._newValue === a
                },
                _setBoundingForValue: function(a) {
                    var b = (a + "").length;
                    if (b !== this._boundingLength) {
                        this._boundingLength = b;
                        for (var c = "", d = 0; b > d; d++)
                            c += "8";
                        this._bounding.textContent = c;
                        var e = parseInt(getComputedStyle(this._wrapper).fontSize, 10)
                          , f = this._bounding.offsetWidth / e;
                        this._inner.style.width = f + .1 * (b - 1) + "em"
                    }
                },
                _setNewValue: function(a) {
                    this._newValue = a,
                    " " !== a && (this._new.textContent = a)
                },
                _setOldValue: function(a) {
                    this._oldValue = a,
                    this._old.textContent = a
                },
                setValue: function(b) {
                    b = this._transform(b),
                    this._isEmpty() ? (this._setNewValue(b),
                    this._setBoundingForValue(b),
                    a.triggerAnimation(this._inner, "soon-slot-animate")) : this._isSame(b) && !this._forceReplace || (this._newValue.length && this._setOldValue(this._newValue),
                    this._setNewValue(b),
                    this._setBoundingForValue(b),
                    a.triggerAnimation(this._inner, "soon-slot-animate"))
                }
            },
            b
        }(B),
        C.Text = function(a) {
            var b = function(a) {
                this._wrapper = document.createElement("span"),
                this._wrapper.className = "soon-text " + (a.className || ""),
                this._transform = a.transform || function(a) {
                    return a
                }
            };
            return b.prototype = {
                redraw: function() {},
                destroy: function() {
                    return this._wrapper
                },
                getElement: function() {
                    return this._wrapper
                },
                setValue: function(b) {
                    a.setTextContent(this._wrapper, this._transform(b))
                }
            },
            b
        }(B);
        var F = function(a, b) {
            var c = function(a, c) {
                c = c || {},
                this._rate = c.rate || 1e3,
                this._offset = null,
                this._time = 0,
                this._paused = !1,
                this._nextTickReference = null,
                this._tickBind = this._tick.bind(this),
                this._onTick = a || function() {}
                ,
                "addEventListener"in document && document.addEventListener(b.documentVisibilityEvent, this)
            };
            return c.prototype = {
                handleEvent: function() {
                    b.isDocumentHidden() ? this._lock() : this._unlock()
                },
                isRunning: function() {
                    return null !== this._offset
                },
                isPaused: function() {
                    return this.isRunning() && this._paused
                },
                start: function() {
                    this.isRunning() || this.reset()
                },
                getTime: function() {
                    return this._time
                },
                reset: function() {
                    this.pause(),
                    this._offset = (new Date).getTime(),
                    this._time = 0,
                    this.resume()
                },
                stop: function() {
                    var a = this;
                    setTimeout(function() {
                        a._clearTimer(),
                        a._offset = null
                    }, 0)
                },
                pause: function() {
                    this._paused = !0,
                    this._clearTimer()
                },
                resume: function() {
                    if (this.isPaused()) {
                        this._paused = !1;
                        var a = (new Date).getTime();
                        this._time += a - this._offset,
                        this._offset = a,
                        this._tick()
                    }
                },
                _clearTimer: function() {
                    clearTimeout(this._nextTickReference),
                    this._nextTickReference = null
                },
                _lock: function() {
                    this._clearTimer()
                },
                _unlock: function() {
                    this.isPaused() || (this.pause(),
                    this.resume())
                },
                _tick: function() {
                    this._onTick(this._time),
                    this._offset += this._rate,
                    this._time += this._rate,
                    this._nextTickReference = setTimeout(this._tickBind, this._offset - (new Date).getTime())
                }
            },
            c
        }(this, B)
          , G = []
          , H = 0
          , I = ["xxl", "xl", "l", "m", "s", "xs", "xxs"]
          , J = 3
          , K = (I.length,
        [])
          , L = []
          , M = {
            y: {
                labels: "Year,Years",
                option: "Years",
                padding: ""
            },
            M: {
                labels: "Month,Months",
                option: "Months",
                padding: "00"
            },
            w: {
                labels: "Week,Weeks",
                option: "Weeks",
                padding: "00"
            },
            d: {
                labels: "Day,Days",
                option: "Days",
                padding: "000"
            },
            h: {
                labels: "Hour,Hours",
                option: "Hours",
                padding: "00"
            },
            m: {
                labels: "Minute,Minutes",
                option: "Minutes",
                padding: "00"
            },
            s: {
                labels: "Second,Seconds",
                option: "Seconds",
                padding: "00"
            },
            ms: {
                labels: "Millisecond,Milliseconds",
                option: "Milliseconds",
                padding: "000"
            }
        };
        E.register(d);
        var N = /([\d]+)[\s]+([a-z]+)/i
          , O = /([\d]+)[:]*([\d]{2})*[:]*([\d]{2})*/;
        A.parse = function(a) {
            w(a)
        }
        ,
        A.redraw = function(a) {
            if (a) {
                var b = j(a);
                f(b.node, b.presenter)
            } else
                g()
        }
        ,
        A.reset = function(a) {
            var b = j(a);
            b && b.ticker.reset()
        }
        ,
        A.freeze = function(a) {
            var b = j(a);
            b && b.ticker.pause()
        }
        ,
        A.unfreeze = function(a) {
            var b = j(a);
            b && b.ticker.resume()
        }
        ,
        A.setOption = function(a, b, c) {
            var d = j(a);
            if (d) {
                var e = d.options;
                e[b] = c,
                this.destroy(a),
                this.create(a, e)
            }
        }
        ,
        A.setOptions = function(a, b) {
            var c = j(a);
            if (c) {
                var d, e = c.options;
                for (d in b)
                    b.hasOwnProperty(d) && (e[d] = b[d]);
                this.destroy(a),
                this.create(a, b)
            }
        }
        ,
        A.destroy = function(a) {
            var b = h(a);
            if (null !== b) {
                var c = i(a);
                null !== c && L.splice(c, 1);
                var d = K[b];
                d.ticker && d.ticker.stop(),
                d.presenter.destroy();
                var e = d.node.querySelector(".soon-placeholder");
                d.node.removeChild(e ? e : d.node.querySelector(".soon-group")),
                a.removeAttribute("data-initialized"),
                K.splice(b, 1)
            }
        }
        ,
        A.create = function(a, b) {
            if (!b)
                return w(a);
            if ("true" === a.getAttribute("data-initialized"))
                return null;
            a.setAttribute("data-initialized", "true");
            var c = null
              , d = null;
            b.eventComplete && (c = "string" == typeof b.eventComplete ? window[b.eventComplete] : b.eventComplete),
            b.eventTick && (d = "string" == typeof b.eventTick ? window[b.eventTick] : b.eventTick),
            b.due && -1 !== b.due.indexOf("reset") && (c = z(a, b, c),
            b.eventComplete = c),
            l(a, b, "layout"),
            l(a, b, "face"),
            l(a, b, "visual"),
            l(a, b, "format"),
            b.scaleMax && a.setAttribute("data-scale-max", b.scaleMax),
            b.scaleHide && a.setAttribute("data-scale-hide", b.scaleHide);
            var e, f, g, h = (b.format || "d,h,m,s").split(","), i = -1 === h.indexOf("ms") ? 1e3 : 24, j = {};
            for (e in M)
                M.hasOwnProperty(e) && (f = M[e],
                g = (b["labels" + f.option] || f.labels).split(","),
                j[e] = g[0],
                j[e + "_s"] = g[1] || g[0]);
            var m = "undefined" == typeof b.padding ? !0 : b.padding
              , n = {};
            for (e in M)
                M.hasOwnProperty(e) && (f = M[e],
                m ? (n[e] = y(e, h),
                null === n[e] && (n[e] = f.padding),
                b["padding" + f.option] && (n[e] = b["padding" + f.option])) : n[e] = "");
            var p = (b.face || "text ").split(" ")[0]
              , q = b.due ? x(b.due) : null
              , r = b.since ? B.isoToDate(b.since) : null
              , s = b.now ? B.isoToDate(b.now) : r ? null : new Date
              , t = {
                due: q,
                since: r,
                now: s,
                view: p,
                face: b.face,
                visual: b.visual || null,
                format: h,
                separator: b.separator || null,
                cascade: "undefined" == typeof b.cascade ? !0 : B.toBoolean(b.cascade),
                singular: b.singular,
                reflect: b.reflect || !1,
                chars: "undefined" == typeof b.separateChars ? !0 : B.toBoolean(b.separateChars),
                label: j,
                padding: n,
                callback: {
                    onComplete: c || function() {}
                    ,
                    onTick: d || function() {}
                }
            };
            B.isSlow() && (t.view = "text",
            t.reflect = !1,
            t.visual = null);
            var A = null
              , C = o(t, function() {
                A && A.stop(),
                t.callback.onComplete()
            });
            k(a);
            var D = u(a, C);
            return A = v(a, D, i, b)
        }
        ;
        var P;
        !function(a) {
            P = a()
        }(function(a) {
            function b(a) {
                for (n = 1; a = d.shift(); )
                    a()
            }
            var c, d = [], e = !1, f = document, g = f.documentElement, h = g.doScroll, i = "DOMContentLoaded", j = "addEventListener", k = "onreadystatechange", l = "readyState", m = h ? /^loaded|^c/ : /^loaded|c/, n = m.test(f[l]);
            return f[j] && f[j](i, c = function() {
                f.removeEventListener(i, c, e),
                b()
            }
            , e),
            h && f.attachEvent(k, c = function() {
                /^c/.test(f[l]) && (f.detachEvent(k, c),
                b())
            }
            ),
            a = h ? function(b) {
                self != top ? n ? b() : d.push(b) : function() {
                    try {
                        g.doScroll("left")
                    } catch (c) {
                        return setTimeout(function() {
                            a(b)
                        }, 50)
                    }
                    b()
                }()
            }
            : function(a) {
                n ? a() : d.push(a)
            }
        }),
        P(function() {
            var a = document.querySelector("script[src*=soon]");
            if (!a || "false" !== a.getAttribute("data-auto"))
                for (var b = document.getElementsByClassName ? document.getElementsByClassName("soon") : document.querySelectorAll(".soon"), c = 0, d = b.length; d > c; c++)
                    w(b[c])
        }),
        function(a, b) {
            "use strict";
            if (b) {
                var c = ["destroy", "reset", "resize", "freeze", "unfreeze", "redraw"]
                  , d = c.length;
                b.fn.soon = function() {
                    var b = this;
                    b.create = function(b) {
                        return this.each(function() {
                            a.create(this, b)
                        })
                    }
                    ,
                    b.setOption = function(b, c) {
                        return this.each(function() {
                            a.setOption(this, b, c)
                        })
                    }
                    ,
                    b.setOptions = function(b) {
                        return this.each(function() {
                            a.setOptions(this, b)
                        })
                    }
                    ;
                    for (var e = 0; d > e; e++)
                        !function(c) {
                            b[c] = function() {
                                return this.each(function() {
                                    a[c](this)
                                })
                            }
                        }(c[e]);
                    return this
                }
            }
        }(A, b),
        "undefined" != typeof module && module.exports ? module.exports = A : "function" == typeof define && define.amd ? define(function() {
            return A
        }) : a.Soon = A
    }
}(window, window.jQuery);