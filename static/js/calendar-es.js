/* Copyright Notice for Dynarch Date Time Picker */
/*  Copyright Mihai Bazon, 2002-2005  |  www.bazon.net/mishoo
 * -----------------------------------------------------------
 *
 * The DHTML Calendar, version 1.0 "It is happening again"
 *
 * Details and latest version at:
 * www.dynarch.com/projects/calendar
 *
 * This script is developed by Dynarch.com.  Visit us at www.dynarch.com. (THIS SITE IS DOWN)
 *
 * This script is distributed under the GNU Lesser General Public License.
 * Read the entire license text here: http://www.gnu.org/licenses/lgpl.html
 */
// Calendar ES language traduction by Leandro E. Colombo Vi�a <colomboleandro AT gmail DOT com>
// Author: Mihai Bazon, <mihai_bazon@yahoo.com>
// Encoding: any
// Distributed under the same terms as the calendar itself.
/* End Copyright Notice for Dynarch Date Time Picker */
Calendar = function (J, K, H, G) {
    this.activeDiv = null;
    this.currentDateEl = null;
    this.getDateStatus = null;
    this.getDateToolTip = null;
    this.getDateText = null;
    this.timeout = null;
    this.onSelected = H || null;
    this.onClose = G || null;
    this.dragging = false;
    this.hidden = false;
    this.minYear = 1970;
    this.maxYear = 2050;
    this.dateFormat = Calendar._TT.DEF_DATE_FORMAT;
    this.ttDateFormat = Calendar._TT.TT_DATE_FORMAT;
    this.isPopup = true;
    this.weekNumbers = true;
    this.firstDayOfWeek = typeof J == "number" ? J : Calendar._FD;
    this.showsOtherMonths = false;
    this.dateStr = K;
    this.ar_days = null;
    this.showsTime = false;
    this.time24 = true;
    this.yearStep = 2;
    this.hiliteToday = true;
    this.multiple = null;
    this.table = null;
    this.element = null;
    this.tbody = null;
    this.firstdayname = null;
    this.monthsCombo = null;
    this.yearsCombo = null;
    this.hilitedMonth = null;
    this.activeMonth = null;
    this.hilitedYear = null;
    this.activeYear = null;
    this.dateClicked = false;
    if (typeof Calendar._SDN == "undefined") {
        if (typeof Calendar._SDN_len == "undefined") {
            Calendar._SDN_len = 3
        }
        var L = new Array();
        for (var I = 8; I > 0;) {
            L[--I] = Calendar._DN[I].substr(0, Calendar._SDN_len)
        }
        Calendar._SDN = L;
        if (typeof Calendar._SMN_len == "undefined") {
            Calendar._SMN_len = 3
        }
        L = new Array();
        for (var I = 12; I > 0;) {
            L[--I] = Calendar._MN[I].substr(0, Calendar._SMN_len)
        }
        Calendar._SMN = L
    }
};
Calendar._C = null;
Calendar.is_ie = (/msie/i.test(navigator.userAgent) && !/opera/i.test(navigator.userAgent));
Calendar.is_ie5 = (Calendar.is_ie && /msie 5\.0/i.test(navigator.userAgent));
Calendar.is_opera = /opera/i.test(navigator.userAgent);
Calendar.is_khtml = /Konqueror|Safari|KHTML/i.test(navigator.userAgent);
Calendar.getAbsolutePos = function (I) {
    var G = 0,
        J = 0;
    var K = /^div$/i.test(I.tagName);
    if (K && I.scrollLeft) {
        G = I.scrollLeft
    }
    if (K && I.scrollTop) {
        J = I.scrollTop
    }
    var H = {
        x: I.offsetLeft - G,
        y: I.offsetTop - J
    };
    if (I.offsetParent) {
        var L = this.getAbsolutePos(I.offsetParent);
        H.x += L.x;
        H.y += L.y
    }
    return H
};
Calendar.isRelated = function (G, E) {
    var F = E.relatedTarget;
    if (!F) {
        var H = E.type;
        if (H == "mouseover") {
            F = E.fromElement
        } else {
            if (H == "mouseout") {
                F = E.toElement
            }
        }
    }
    while (F) {
        if (F == G) {
            return true
        }
        F = F.parentNode
    }
    return false
};
Calendar.removeClass = function (G, H) {
    if (!(G && G.className)) {
        return
    }
    var F = G.className.split(" ");
    var J = new Array();
    for (var I = F.length; I > 0;) {
        if (F[--I] != H) {
            J[J.length] = F[I]
        }
    }
    G.className = J.join(" ")
};
Calendar.addClass = function (D, C) {
    Calendar.removeClass(D, C);
    D.className += " " + C
};
Calendar.getElement = function (C) {
    var D = Calendar.is_ie ? window.event.srcElement : C.currentTarget;
    while (D.nodeType != 1 || /^div$/i.test(D.tagName)) {
        D = D.parentNode
    }
    return D
};
Calendar.getTargetElement = function (C) {
    var D = Calendar.is_ie ? window.event.srcElement : C.target;
    while (D.nodeType != 1) {
        D = D.parentNode
    }
    return D
};
Calendar.stopEvent = function (B) {
    B || (B = window.event);
    if (Calendar.is_ie) {
        B.cancelBubble = true;
        B.returnValue = false
    } else {
        B.preventDefault();
        B.stopPropagation()
    }
    return false
};
Calendar.addEvent = function (D, E, F) {
    if (D.attachEvent) {
        D.attachEvent("on" + E, F)
    } else {
        if (D.addEventListener) {
            D.addEventListener(E, F, true)
        } else {
            D["on" + E] = F
        }
    }
};
Calendar.removeEvent = function (D, E, F) {
    if (D.detachEvent) {
        D.detachEvent("on" + E, F)
    } else {
        if (D.removeEventListener) {
            D.removeEventListener(E, F, true)
        } else {
            D["on" + E] = null
        }
    }
};
Calendar.createElement = function (E, F) {
    var D = null;
    if (document.createElementNS) {
        D = document.createElementNS("http://www.w3.org/1999/xhtml", E)
    } else {
        D = document.createElement(E)
    } if (typeof F != "undefined") {
        F.appendChild(D)
    }
    return D
};
Calendar._add_evs = function (el) {
    with(Calendar) {
        addEvent(el, "mouseover", dayMouseOver);
        addEvent(el, "mousedown", dayMouseDown);
        addEvent(el, "mouseout", dayMouseOut);
        if (is_ie) {
            addEvent(el, "dblclick", dayMouseDblClick);
            el.setAttribute("unselectable", true)
        }
    }
};
Calendar.findMonth = function (B) {
    if (typeof B.month != "undefined") {
        return B
    } else {
        if (typeof B.parentNode.month != "undefined") {
            return B.parentNode
        }
    }
    return null
};
Calendar.findYear = function (B) {
    if (typeof B.year != "undefined") {
        return B
    } else {
        if (typeof B.parentNode.year != "undefined") {
            return B.parentNode
        }
    }
    return null
};
Calendar.showMonthsCombo = function () {
    var I = Calendar._C;
    if (!I) {
        return false
    }
    var I = I;
    var H = I.activeDiv;
    var J = I.monthsCombo;
    if (I.hilitedMonth) {
        Calendar.removeClass(I.hilitedMonth, "hilite")
    }
    if (I.activeMonth) {
        Calendar.removeClass(I.activeMonth, "active")
    }
    var K = I.monthsCombo.getElementsByTagName("div")[I.date.getMonth()];
    Calendar.addClass(K, "active");
    I.activeMonth = K;
    var L = J.style;
    L.display = "block";
    if (H.navtype < 0) {
        L.left = H.offsetLeft + "px"
    } else {
        var G = J.offsetWidth;
        if (typeof G == "undefined") {
            G = 50
        }
        L.left = (H.offsetLeft + H.offsetWidth - G) + "px"
    }
    L.top = (H.offsetTop + H.offsetHeight) + "px"
};
Calendar.showYearsCombo = function (K) {
    var N = Calendar._C;
    if (!N) {
        return false
    }
    var N = N;
    var L = N.activeDiv;
    var S = N.yearsCombo;
    if (N.hilitedYear) {
        Calendar.removeClass(N.hilitedYear, "hilite")
    }
    if (N.activeYear) {
        Calendar.removeClass(N.activeYear, "active")
    }
    N.activeYear = null;
    var M = N.date.getFullYear() + (K ? 1 : -1);
    var P = S.firstChild;
    var Q = false;
    for (var T = 12; T > 0; --T) {
        if (M >= N.minYear && M <= N.maxYear) {
            P.innerHTML = M;
            P.year = M;
            P.style.display = "block";
            Q = true
        } else {
            P.style.display = "none"
        }
        P = P.nextSibling;
        M += K ? N.yearStep : -N.yearStep
    }
    if (Q) {
        var O = S.style;
        O.display = "block";
        if (L.navtype < 0) {
            O.left = L.offsetLeft + "px"
        } else {
            var R = S.offsetWidth;
            if (typeof R == "undefined") {
                R = 50
            }
            O.left = (L.offsetLeft + L.offsetWidth - R) + "px"
        }
        O.top = (L.offsetTop + L.offsetHeight) + "px"
    }
};
Calendar.tableMouseUp = function (ev) {
    var cal = Calendar._C;
    if (!cal) {
        return false
    }
    if (cal.timeout) {
        clearTimeout(cal.timeout)
    }
    var el = cal.activeDiv;
    if (!el) {
        return false
    }
    var target = Calendar.getTargetElement(ev);
    ev || (ev = window.event);
    Calendar.removeClass(el, "active");
    if (target == el || target.parentNode == el) {
        Calendar.cellClick(el, ev)
    }
    var mon = Calendar.findMonth(target);
    var date = null;
    if (mon) {
        date = new Date(cal.date);
        if (mon.month != date.getMonth()) {
            date.setMonth(mon.month);
            cal.setDate(date);
            cal.dateClicked = false;
            cal.callHandler()
        }
    } else {
        var year = Calendar.findYear(target);
        if (year) {
            date = new Date(cal.date);
            if (year.year != date.getFullYear()) {
                date.c_setFullYear(year.year);
                cal.setDate(date);
                cal.dateClicked = false;
                cal.callHandler()
            }
        }
    }
    with(Calendar) {
        removeEvent(document, "mouseup", tableMouseUp);
        removeEvent(document, "mouseover", tableMouseOver);
        removeEvent(document, "mousemove", tableMouseOver);
        cal._hideCombos();
        _C = null;
        return stopEvent(ev)
    }
};
Calendar.tableMouseOver = function (X) {
    var T = Calendar._C;
    if (!T) {
        return
    }
    var R = T.activeDiv;
    var b = Calendar.getTargetElement(X);
    if (b == R || b.parentNode == R) {
        Calendar.addClass(R, "hilite active");
        Calendar.addClass(R.parentNode, "rowhilite")
    } else {
        if (typeof R.navtype == "undefined" || (R.navtype != 50 && (R.navtype == 0 || Math.abs(R.navtype) > 2))) {
            Calendar.removeClass(R, "active")
        }
        Calendar.removeClass(R, "hilite");
        Calendar.removeClass(R.parentNode, "rowhilite")
    }
    X || (X = window.event);
    if (R.navtype == 50 && b != R) {
        var Y = Calendar.getAbsolutePos(R);
        var V = R.offsetWidth;
        var W = X.clientX;
        var U;
        var Z = true;
        if (W > Y.x + V) {
            U = W - Y.x - V;
            Z = false
        } else {
            U = Y.x - W
        } if (U < 0) {
            U = 0
        }
        var e = R._range;
        var c = R._current;
        var d = Math.floor(U / 10) % e.length;
        for (var f = e.length; --f >= 0;) {
            if (e[f] == c) {
                break
            }
        }
        while (d-- > 0) {
            if (Z) {
                if (--f < 0) {
                    f = e.length - 1
                }
            } else {
                if (++f >= e.length) {
                    f = 0
                }
            }
        }
        var S = e[f];
        R.innerHTML = S;
        T.onUpdateTime()
    }
    var Q = Calendar.findMonth(b);
    if (Q) {
        if (Q.month != T.date.getMonth()) {
            if (T.hilitedMonth) {
                Calendar.removeClass(T.hilitedMonth, "hilite")
            }
            Calendar.addClass(Q, "hilite");
            T.hilitedMonth = Q
        } else {
            if (T.hilitedMonth) {
                Calendar.removeClass(T.hilitedMonth, "hilite")
            }
        }
    } else {
        if (T.hilitedMonth) {
            Calendar.removeClass(T.hilitedMonth, "hilite")
        }
        var a = Calendar.findYear(b);
        if (a) {
            if (a.year != T.date.getFullYear()) {
                if (T.hilitedYear) {
                    Calendar.removeClass(T.hilitedYear, "hilite")
                }
                Calendar.addClass(a, "hilite");
                T.hilitedYear = a
            } else {
                if (T.hilitedYear) {
                    Calendar.removeClass(T.hilitedYear, "hilite")
                }
            }
        } else {
            if (T.hilitedYear) {
                Calendar.removeClass(T.hilitedYear, "hilite")
            }
        }
    }
    return Calendar.stopEvent(X)
};
Calendar.tableMouseDown = function (B) {
    if (Calendar.getTargetElement(B) == Calendar.getElement(B)) {
        return Calendar.stopEvent(B)
    }
};
Calendar.calDragIt = function (J) {
    var I = Calendar._C;
    if (!(I && I.dragging)) {
        return false
    }
    var G;
    var H;
    if (Calendar.is_ie) {
        H = window.event.clientY + document.body.scrollTop;
        G = window.event.clientX + document.body.scrollLeft
    } else {
        G = J.pageX;
        H = J.pageY
    }
    I.hideShowCovered();
    var F = I.element.style;
    F.left = (G - I.xOffs) + "px";
    F.top = (H - I.yOffs) + "px";
    return Calendar.stopEvent(J)
};
Calendar.calDragEnd = function (ev) {
    var cal = Calendar._C;
    if (!cal) {
        return false
    }
    cal.dragging = false;
    with(Calendar) {
        removeEvent(document, "mousemove", calDragIt);
        removeEvent(document, "mouseup", calDragEnd);
        tableMouseUp(ev)
    }
    cal.hideShowCovered()
};
Calendar.dayMouseDown = function (ev) {
    var el = Calendar.getElement(ev);
    if (el.disabled) {
        return false
    }
    var cal = el.calendar;
    cal.activeDiv = el;
    Calendar._C = cal;
    if (el.navtype != 300) {
        with(Calendar) {
            if (el.navtype == 50) {
                el._current = el.innerHTML;
                addEvent(document, "mousemove", tableMouseOver)
            } else {
                addEvent(document, Calendar.is_ie5 ? "mousemove" : "mouseover", tableMouseOver)
            }
            addClass(el, "hilite active");
            addEvent(document, "mouseup", tableMouseUp)
        }
    } else {
        if (cal.isPopup) {
            cal._dragStart(ev)
        }
    } if (el.navtype == -1 || el.navtype == 1) {
        if (cal.timeout) {
            clearTimeout(cal.timeout)
        }
        cal.timeout = setTimeout("Calendar.showMonthsCombo()", 250)
    } else {
        if (el.navtype == -2 || el.navtype == 2) {
            if (cal.timeout) {
                clearTimeout(cal.timeout)
            }
            cal.timeout = setTimeout((el.navtype > 0) ? "Calendar.showYearsCombo(true)" : "Calendar.showYearsCombo(false)", 250)
        } else {
            cal.timeout = null
        }
    }
    return Calendar.stopEvent(ev)
};
Calendar.dayMouseDblClick = function (B) {
    Calendar.cellClick(Calendar.getElement(B), B || window.event);
    if (Calendar.is_ie) {
        document.selection.empty()
    }
};
Calendar.dayMouseOver = function (D) {
    var C = Calendar.getElement(D);
    if (Calendar.isRelated(C, D) || Calendar._C || C.disabled) {
        return false
    }
    if (C.ttip) {
        if (C.ttip.substr(0, 1) == "_") {
            C.ttip = C.caldate.c_print(C.calendar.ttDateFormat) + C.ttip.substr(1)
        }
        C.calendar.tooltips.innerHTML = C.ttip
    }
    if (C.navtype != 300) {
        Calendar.addClass(C, "hilite");
        if (C.caldate) {
            Calendar.addClass(C.parentNode, "rowhilite")
        }
    }
    return Calendar.stopEvent(D)
};
Calendar.dayMouseOut = function (ev) {
    with(Calendar) {
        var el = getElement(ev);
        if (isRelated(el, ev) || _C || el.disabled) {
            return false
        }
        removeClass(el, "hilite");
        if (el.caldate) {
            removeClass(el.parentNode, "rowhilite")
        }
        if (el.calendar) {
            el.calendar.tooltips.innerHTML = _TT.SEL_DATE
        }
        return stopEvent(ev)
    }
};
Calendar.cellClick = function (d, U) {
    var Q = d.calendar;
    var a = false;
    var X = false;
    var c = null;
    if (typeof d.navtype == "undefined") {
        if (Q.currentDateEl) {
            Calendar.removeClass(Q.currentDateEl, "selected");
            Calendar.addClass(d, "selected");
            a = (Q.currentDateEl == d);
            if (!a) {
                Q.currentDateEl = d
            }
        }
        Q.date.c_setDateOnly(d.caldate);
        c = Q.date;
        var R = !(Q.dateClicked = !d.otherMonth);
        if (!R && !Q.currentDateEl) {
            Q._toggleMultipleDate(new Date(c))
        } else {
            X = !d.disabled
        } if (R) {
            Q._init(Q.firstDayOfWeek, c)
        }
    } else {
        if (d.navtype == 200) {
            Calendar.removeClass(d, "hilite");
            Q.callCloseHandler();
            return
        }
        c = new Date(Q.date);
        if (d.navtype == 0) {
            c.c_setDateOnly(new Date())
        }
        Q.dateClicked = false;
        var V = c.getFullYear();
        var b = c.getMonth();

        function S(B) {
            var A = c.getDate();
            var C = c.c_getMonthDays(B);
            if (A > C) {
                c.setDate(C)
            }
            c.setMonth(B)
        }
        switch (d.navtype) {
        case 400:
            Calendar.removeClass(d, "hilite");
            var T = Calendar._TT.ABOUT;
            if (typeof T != "undefined") {
                T += Q.showsTime ? Calendar._TT.ABOUT_TIME : ""
            } else {
                T = 'Help and about box text is not translated into this language.\nIf you know this language and you feel generous please update\nthe corresponding file in "lang" subdir to match calendar-en.js\nand send it back to <mihai_bazon@yahoo.com> to get it into the distribution  ;-)\n\nThank you!\nhttp://dynarch.com/mishoo/calendar.epl\n'
            }
            alert(T);
            return;
        case -2:
            if (V > Q.minYear) {
                c.c_setFullYear(V - 1)
            }
            break;
        case -1:
            if (b > 0) {
                S(b - 1)
            } else {
                if (V-- > Q.minYear) {
                    c.c_setFullYear(V);
                    S(11)
                }
            }
            break;
        case 1:
            if (b < 11) {
                S(b + 1)
            } else {
                if (V < Q.maxYear) {
                    c.c_setFullYear(V + 1);
                    S(0)
                }
            }
            break;
        case 2:
            if (V < Q.maxYear) {
                c.c_setFullYear(V + 1)
            }
            break;
        case 100:
            Q.setFirstDayOfWeek(d.fdow);
            return;
        case 50:
            var Y = d._range;
            var W = d.innerHTML;
            for (var Z = Y.length; --Z >= 0;) {
                if (Y[Z] == W) {
                    break
                }
            }
            if (U && U.shiftKey) {
                if (--Z < 0) {
                    Z = Y.length - 1
                }
            } else {
                if (++Z >= Y.length) {
                    Z = 0
                }
            }
            var P = Y[Z];
            d.innerHTML = P;
            Q.onUpdateTime();
            return;
        case 0:
            if ((typeof Q.getDateStatus == "function") && Q.getDateStatus(c, c.getFullYear(), c.getMonth(), c.getDate())) {
                return false
            }
            break
        }
        if (!c.c_equalsTo(Q.date)) {
            Q.setDate(c);
            X = true
        } else {
            if (d.navtype == 0) {
                X = a = true
            }
        }
    } if (X) {
        U && Q.callHandler()
    }
    if (a) {
        Calendar.removeClass(d, "hilite");
        U && Q.callCloseHandler()
    }
};
Calendar.prototype.create = function (Y) {
    var Z = null;
    if (!Y) {
        Z = document.getElementsByTagName("body")[0];
        this.isPopup = true
    } else {
        Z = Y;
        this.isPopup = false
    }
    this.date = this.dateStr ? new Date(this.dateStr) : new Date();
    var V = Calendar.createElement("table");
    this.table = V;
    V.cellSpacing = 0;
    V.cellPadding = 0;
    V.calendar = this;
    Calendar.addEvent(V, "mousedown", Calendar.tableMouseDown);
    var T = Calendar.createElement("div");
    this.element = T;
    T.className = "calendar";
    if (this.isPopup) {
        T.style.position = "absolute";
        T.style.display = "none"
    }
    T.appendChild(V);
    var b = Calendar.createElement("thead", V);
    var X = null;
    var U = null;
    var S = this;
    var f = function (A, B, C) {
        X = Calendar.createElement("td", U);
        X.colSpan = B;
        X.className = "button";
        if (C != 0 && Math.abs(C) <= 2) {
            X.className += " nav"
        }
        Calendar._add_evs(X);
        X.calendar = S;
        X.navtype = C;
        X.innerHTML = "<div unselectable='on'>" + A + "</div>";
        return X
    };
    U = Calendar.createElement("tr", b);
    var R = 6;
    (this.isPopup) && --R;
    (this.weekNumbers) && ++R;
    f("?", 1, 400).ttip = Calendar._TT.INFO;
    this.title = f("", R, 300);
    this.title.className = "title";
    if (this.isPopup) {
        this.title.ttip = Calendar._TT.DRAG_TO_MOVE;
        this.title.style.cursor = "move";
        f("&#x00d7;", 1, 200).ttip = Calendar._TT.CLOSE
    }
    U = Calendar.createElement("tr", b);
    U.className = "headrow";
    this._nav_py = f("&#x00ab;", 1, -2);
    this._nav_py.ttip = Calendar._TT.PREV_YEAR;
    this._nav_pm = f("&#x2039;", 1, -1);
    this._nav_pm.ttip = Calendar._TT.PREV_MONTH;
    this._nav_now = f(Calendar._TT.TODAY, this.weekNumbers ? 4 : 3, 0);
    this._nav_now.ttip = Calendar._TT.GO_TODAY;
    this._nav_nm = f("&#x203a;", 1, 1);
    this._nav_nm.ttip = Calendar._TT.NEXT_MONTH;
    this._nav_ny = f("&#x00bb;", 1, 2);
    this._nav_ny.ttip = Calendar._TT.NEXT_YEAR;
    U = Calendar.createElement("tr", b);
    U.className = "daynames";
    if (this.weekNumbers) {
        X = Calendar.createElement("td", U);
        X.className = "name wn";
        X.innerHTML = Calendar._TT.WK
    }
    for (var c = 7; c > 0; --c) {
        X = Calendar.createElement("td", U);
        if (!c) {
            X.navtype = 100;
            X.calendar = this;
            Calendar._add_evs(X)
        }
    }
    this.firstdayname = (this.weekNumbers) ? U.firstChild.nextSibling : U.firstChild;
    this._displayWeekdays();
    var d = Calendar.createElement("tbody", V);
    this.tbody = d;
    for (c = 6; c > 0; --c) {
        U = Calendar.createElement("tr", d);
        if (this.weekNumbers) {
            X = Calendar.createElement("td", U)
        }
        for (var e = 7; e > 0; --e) {
            X = Calendar.createElement("td", U);
            X.calendar = this;
            Calendar._add_evs(X)
        }
    }
    if (this.showsTime) {
        U = Calendar.createElement("tr", d);
        U.className = "time";
        X = Calendar.createElement("td", U);
        X.className = "time";
        X.colSpan = 2;
        X.innerHTML = Calendar._TT.TIME || "&nbsp;";
        X = Calendar.createElement("td", U);
        X.className = "time";
        X.colSpan = this.weekNumbers ? 4 : 3;
        (function () {
            function F(P, N, O, L) {
                var K = Calendar.createElement("span", X);
                K.className = P;
                K.innerHTML = N;
                K.calendar = S;
                K.ttip = Calendar._TT.TIME_PART;
                K.navtype = 50;
                K._range = [];
                if (typeof O != "number") {
                    K._range = O
                } else {
                    for (var J = O; J <= L; ++J) {
                        var M;
                        if (J < 10 && L >= 10) {
                            M = "0" + J
                        } else {
                            M = "" + J
                        }
                        K._range[K._range.length] = M
                    }
                }
                Calendar._add_evs(K);
                return K
            }
            var B = S.date.getHours();
            var I = S.date.getMinutes();
            var A = !S.time24;
            var H = (B > 12);
            if (A && H) {
                B -= 12
            }
            var D = F("hour", B, A ? 1 : 0, A ? 12 : 23);
            var E = Calendar.createElement("span", X);
            E.innerHTML = ":";
            E.className = "colon";
            var G = F("minute", I, 0, 59);
            var C = null;
            X = Calendar.createElement("td", U);
            X.className = "time";
            X.colSpan = 2;
            if (A) {
                C = F("ampm", H ? "pm" : "am", ["am", "pm"])
            } else {
                X.innerHTML = "&nbsp;"
            }
            S.onSetTime = function () {
                var K, L = this.date.getHours(),
                    J = this.date.getMinutes();
                if (A) {
                    K = (L >= 12);
                    if (K) {
                        L -= 12
                    }
                    if (L == 0) {
                        L = 12
                    }
                    C.innerHTML = K ? "pm" : "am"
                }
                D.innerHTML = (L < 10) ? ("0" + L) : L;
                G.innerHTML = (J < 10) ? ("0" + J) : J
            };
            S.onUpdateTime = function () {
                var K = this.date;
                var J = parseInt(D.innerHTML, 10);
                if (A) {
                    if (/pm/i.test(C.innerHTML) && J < 12) {
                        J += 12
                    } else {
                        if (/am/i.test(C.innerHTML) && J == 12) {
                            J = 0
                        }
                    }
                }
                var N = K.getDate();
                var M = K.getMonth();
                var L = K.getFullYear();
                K.setHours(J);
                K.setMinutes(parseInt(G.innerHTML, 10));
                K.c_setFullYear(L);
                K.setMonth(M);
                K.setDate(N);
                this.dateClicked = false;
                this.callHandler()
            }
        })()
    } else {
        this.onSetTime = this.onUpdateTime = function () {}
    }
    var a = Calendar.createElement("tfoot", V);
    U = Calendar.createElement("tr", a);
    U.className = "footrow";
    X = f(Calendar._TT.SEL_DATE, this.weekNumbers ? 8 : 7, 300);
    X.className = "ttip";
    if (this.isPopup) {
        X.ttip = Calendar._TT.DRAG_TO_MOVE;
        X.style.cursor = "move"
    }
    this.tooltips = X;
    T = Calendar.createElement("div", this.element);
    this.monthsCombo = T;
    T.className = "combo";
    for (c = 0; c < Calendar._MN.length; ++c) {
        var Q = Calendar.createElement("div");
        Q.className = Calendar.is_ie ? "label-IEfix" : "label";
        Q.month = c;
        Q.innerHTML = Calendar._SMN[c];
        T.appendChild(Q)
    }
    T = Calendar.createElement("div", this.element);
    this.yearsCombo = T;
    T.className = "combo";
    for (c = 12; c > 0; --c) {
        var W = Calendar.createElement("div");
        W.className = Calendar.is_ie ? "label-IEfix" : "label";
        T.appendChild(W)
    }
    this._init(this.firstDayOfWeek, this.date);
    Z.appendChild(this.element)
};
Calendar._keyEvent = function (T) {
    var Q = window._dynarch_popupCalendar;
    if (!Q || Q.multiple) {
        return false
    }(Calendar.is_ie) && (T = window.event);
    var V = (Calendar.is_ie || T.type == "keypress"),
        S = T.keyCode;
    if (T.ctrlKey) {
        switch (S) {
        case 37:
            V && Calendar.cellClick(Q._nav_pm);
            break;
        case 38:
            V && Calendar.cellClick(Q._nav_py);
            break;
        case 39:
            V && Calendar.cellClick(Q._nav_nm);
            break;
        case 40:
            V && Calendar.cellClick(Q._nav_ny);
            break;
        default:
            return false
        }
    } else {
        switch (S) {
        case 32:
            Calendar.cellClick(Q._nav_now);
            break;
        case 27:
            V && Q.callCloseHandler();
            break;
        case 37:
        case 38:
        case 39:
        case 40:
            if (V) {
                var Z, R, U, X, O, K;
                Z = S == 37 || S == 38;
                K = (S == 37 || S == 39) ? 1 : 7;

                function P() {
                    O = Q.currentDateEl;
                    var A = O.pos;
                    R = A & 15;
                    U = A >> 4;
                    X = Q.ar_days[U][R]
                }
                P();

                function Y() {
                    var A = new Date(Q.date);
                    A.setDate(A.getDate() - K);
                    Q.setDate(A)
                }

                function W() {
                    var A = new Date(Q.date);
                    A.setDate(A.getDate() + K);
                    Q.setDate(A)
                }
                while (1) {
                    switch (S) {
                    case 37:
                        if (--R >= 0) {
                            X = Q.ar_days[U][R]
                        } else {
                            R = 6;
                            S = 38;
                            continue
                        }
                        break;
                    case 38:
                        if (--U >= 0) {
                            X = Q.ar_days[U][R]
                        } else {
                            Y();
                            P()
                        }
                        break;
                    case 39:
                        if (++R < 7) {
                            X = Q.ar_days[U][R]
                        } else {
                            R = 0;
                            S = 40;
                            continue
                        }
                        break;
                    case 40:
                        if (++U < Q.ar_days.length) {
                            X = Q.ar_days[U][R]
                        } else {
                            W();
                            P()
                        }
                        break
                    }
                    break
                }
                if (X) {
                    if (!X.disabled) {
                        Calendar.cellClick(X)
                    } else {
                        if (Z) {
                            Y()
                        } else {
                            W()
                        }
                    }
                }
            }
            break;
        case 13:
            if (V) {
                Calendar.cellClick(Q.currentDateEl, T)
            }
            break;
        default:
            return false
        }
    }
    return Calendar.stopEvent(T)
};
Calendar.prototype._init = function (q, e) {
    var f = new Date(),
        l = f.getFullYear(),
        c = f.getMonth(),
        AB = f.getDate();
    this.table.style.visibility = "hidden";
    var v = e.getFullYear();
    if (v < this.minYear) {
        v = this.minYear;
        e.c_setFullYear(v)
    } else {
        if (v > this.maxYear) {
            v = this.maxYear;
            e.c_setFullYear(v)
        }
    }
    this.firstDayOfWeek = q;
    this.date = new Date(e);
    var d = e.getMonth();
    var a = e.getDate();
    var b = e.c_getMonthDays();
    e.setDate(1);
    var k = (e.getDay() - this.firstDayOfWeek) % 7;
    if (k < 0) {
        k += 7
    }
    e.setDate(0 - k);
    e.setDate(e.getDate() + 1);
    var y = this.tbody.firstChild;
    var s = Calendar._SMN[d];
    var o = this.ar_days = new Array();
    var p = Calendar._TT.WEEKEND;
    var z = this.multiple ? (this.datesCells = {}) : null;
    for (var i = 0; i < 6; ++i, y = y.nextSibling) {
        var AC = y.firstChild;
        if (this.weekNumbers) {
            AC.className = "day wn";
            AC.innerHTML = e.c_getWeekNumber();
            AC = AC.nextSibling
        }
        y.className = "daysrow";
        var g = false,
            x, AA = o[i] = [];
        for (var j = 0; j < 7; ++j, AC = AC.nextSibling, e.setDate(x + 1)) {
            x = e.getDate();
            var w = e.getDay();
            AC.className = "day";
            AC.pos = i << 4 | j;
            AA[j] = AC;
            var r = (e.getMonth() == d);
            if (!r) {
                if (this.showsOtherMonths) {
                    AC.className += " othermonth";
                    AC.otherMonth = true
                } else {
                    AC.className = "emptycell";
                    AC.innerHTML = "&nbsp;";
                    AC.disabled = true;
                    continue
                }
            } else {
                AC.otherMonth = false;
                g = true
            }
            AC.disabled = false;
            AC.innerHTML = this.getDateText ? this.getDateText(e, x) : x;
            if (z) {
                z[e.c_print("%Y%m%d")] = AC
            }
            if (this.getDateStatus) {
                var n = this.getDateStatus(e, v, d, x);
                if (this.getDateToolTip) {
                    var u = this.getDateToolTip(e, v, d, x);
                    if (u) {
                        AC.title = u
                    }
                }
                if (n === true) {
                    AC.className += " disabled";
                    AC.disabled = true
                } else {
                    if (/disabled/i.test(n)) {
                        AC.disabled = true
                    }
                    AC.className += " " + n
                }
            }
            if (!AC.disabled) {
                AC.caldate = new Date(e);
                AC.ttip = "_";
                if (!this.multiple && r && x == a && this.hiliteToday) {
                    AC.className += " selected";
                    this.currentDateEl = AC
                }
                if (e.getFullYear() == l && e.getMonth() == c && x == AB) {
                    AC.className += " today";
                    AC.ttip += Calendar._TT.PART_TODAY
                }
                if (p.indexOf(w.toString()) != -1) {
                    AC.className += AC.otherMonth ? " oweekend" : " weekend"
                }
            }
        }
        if (!(g || this.showsOtherMonths)) {
            y.className = "emptyrow"
        }
    }
    this.title.innerHTML = Calendar._MN[d] + " " + v;
    this.onSetTime();
    this.table.style.visibility = "visible";
    this._initMultipleDates()
};
Calendar.prototype._initMultipleDates = function () {
    if (this.multiple) {
        for (var F in this.multiple) {
            var D = this.datesCells[F];
            var E = this.multiple[F];
            if (!E) {
                continue
            }
            if (D) {
                D.className += " selected"
            }
        }
    }
};
Calendar.prototype._toggleMultipleDate = function (H) {
    if (this.multiple) {
        var G = H.c_print("%Y%m%d");
        var E = this.datesCells[G];
        if (E) {
            var F = this.multiple[G];
            if (!F) {
                Calendar.addClass(E, "selected");
                this.multiple[G] = H
            } else {
                Calendar.removeClass(E, "selected");
                delete this.multiple[G]
            }
        }
    }
};
Calendar.prototype.setDateToolTipHandler = function (B) {
    this.getDateToolTip = B
};
Calendar.prototype.setDate = function (B) {
    if (!B.c_equalsTo(this.date)) {
        this._init(this.firstDayOfWeek, B)
    }
};
Calendar.prototype.refresh = function () {
    this._init(this.firstDayOfWeek, this.date)
};
Calendar.prototype.setFirstDayOfWeek = function (B) {
    this._init(B, this.date);
    this._displayWeekdays()
};
Calendar.prototype.setDateStatusHandler = Calendar.prototype.setDisabledHandler = function (B) {
    this.getDateStatus = B
};
Calendar.prototype.setRange = function (C, D) {
    this.minYear = C;
    this.maxYear = D
};
Calendar.prototype.callHandler = function () {
    if (this.onSelected) {
        this.onSelected(this, this.date.c_print(this.dateFormat))
    }
};
Calendar.prototype.callCloseHandler = function () {
    if (this.onClose) {
        this.onClose(this)
    }
    this.hideShowCovered()
};
Calendar.prototype.destroy = function () {
    var B = this.element.parentNode;
    B.removeChild(this.element);
    Calendar._C = null;
    window._dynarch_popupCalendar = null
};
Calendar.prototype.reparent = function (D) {
    var C = this.element;
    C.parentNode.removeChild(C);
    D.appendChild(C)
};
Calendar._checkCalendar = function (F) {
    var E = window._dynarch_popupCalendar;
    if (!E) {
        return false
    }
    var D = Calendar.is_ie ? Calendar.getElement(F) : Calendar.getTargetElement(F);
    for (; D != null && D != E.element; D = D.parentNode) {}
    if (D == null) {
        window._dynarch_popupCalendar.callCloseHandler();
        return Calendar.stopEvent(F)
    }
};
Calendar.prototype.show = function () {
    var I = this.table.getElementsByTagName("tr");
    for (var J = I.length; J > 0;) {
        var H = I[--J];
        Calendar.removeClass(H, "rowhilite");
        var K = H.getElementsByTagName("td");
        for (var L = K.length; L > 0;) {
            var G = K[--L];
            Calendar.removeClass(G, "hilite");
            Calendar.removeClass(G, "active")
        }
    }
    this.element.style.display = "block";
    this.hidden = false;
    if (this.isPopup) {
        window._dynarch_popupCalendar = this;
        Calendar.addEvent(document, "keydown", Calendar._keyEvent);
        Calendar.addEvent(document, "keypress", Calendar._keyEvent);
        Calendar.addEvent(document, "mousedown", Calendar._checkCalendar)
    }
    this.hideShowCovered()
};
Calendar.prototype.hide = function () {
    if (this.isPopup) {
        Calendar.removeEvent(document, "keydown", Calendar._keyEvent);
        Calendar.removeEvent(document, "keypress", Calendar._keyEvent);
        Calendar.removeEvent(document, "mousedown", Calendar._checkCalendar)
    }
    this.element.style.display = "none";
    this.hidden = true;
    this.hideShowCovered()
};
Calendar.prototype.showAt = function (D, E) {
    var F = this.element.style;
    F.left = D + "px";
    F.top = E + "px";
    this.show()
};
Calendar.prototype.showAtElement = function (I, H) {
    var F = this;
    var G = Calendar.getAbsolutePos(I);
    if (!H || typeof H != "string") {
        this.showAt(G.x, G.y + I.offsetHeight);
        return true
    }

    function J(B) {
        if (B.x < 0) {
            B.x = 0
        }
        if (B.y < 0) {
            B.y = 0
        }
        var A = document.createElement("div");
        var C = A.style;
        C.position = "absolute";
        C.right = C.bottom = C.width = C.height = "0px";
        document.body.appendChild(A);
        var D = Calendar.getAbsolutePos(A);
        document.body.removeChild(A);
        if (Calendar.is_ie) {
            D.y += document.body.scrollTop;
            D.x += document.body.scrollLeft
        } else {
            D.y += window.scrollY;
            D.x += window.scrollX
        }
        var E = B.x + B.width - D.x;
        if (E > 0) {
            B.x -= E
        }
        E = B.y + B.height - D.y;
        if (E > 0) {
            B.y -= E
        }
    }
    this.element.style.display = "block";
    Calendar.continuation_for_the_fucking_khtml_browser = function () {
        var D = F.element.offsetWidth;
        var B = F.element.offsetHeight;
        F.element.style.display = "none";
        var C = H.substr(0, 1);
        var A = "l";
        if (H.length > 1) {
            A = H.substr(1, 1)
        }
        switch (C) {
        case "T":
            G.y -= B;
            break;
        case "B":
            G.y += I.offsetHeight;
            break;
        case "C":
            G.y += (I.offsetHeight - B) / 2;
            break;
        case "t":
            G.y += I.offsetHeight - B;
            break;
        case "b":
            break
        }
        switch (A) {
        case "L":
            G.x -= D;
            break;
        case "R":
            G.x += I.offsetWidth;
            break;
        case "C":
            G.x += (I.offsetWidth - D) / 2;
            break;
        case "l":
            G.x += I.offsetWidth - D;
            break;
        case "r":
            break
        }
        G.width = D;
        G.height = B + 40;
        F.monthsCombo.style.display = "none";
        J(G);
        F.showAt(G.x, G.y)
    };
    if (Calendar.is_khtml) {
        setTimeout("Calendar.continuation_for_the_fucking_khtml_browser()", 10)
    } else {
        Calendar.continuation_for_the_fucking_khtml_browser()
    }
};
Calendar.prototype.setDateFormat = function (B) {
    this.dateFormat = B
};
Calendar.prototype.setTtDateFormat = function (B) {
    this.ttDateFormat = B
};
Calendar.prototype.parseDate = function (D, C) {
    if (!C) {
        C = this.dateFormat
    }
    this.setDate(Date.parseDate(D, C))
};
Calendar.prototype.hideShowCovered = function () {
    if (!Calendar.is_ie && !Calendar.is_opera) {
        return
    }

    function S(A) {
        var B = A.style.visibility;
        if (!B) {
            if (document.defaultView && typeof (document.defaultView.getComputedStyle) == "function") {
                if (!Calendar.is_khtml) {
                    B = document.defaultView.getComputedStyle(A, "").getPropertyValue("visibility")
                } else {
                    B = ""
                }
            } else {
                if (A.currentStyle) {
                    B = A.currentStyle.visibility
                } else {
                    B = ""
                }
            }
        }
        return B
    }
    var U = new Array("applet", "iframe", "select");
    var R = this.element;
    var T = Calendar.getAbsolutePos(R);
    var e = T.x;
    var Q = R.offsetWidth + e;
    var V = T.y;
    var W = R.offsetHeight + V;
    for (var c = U.length; c > 0;) {
        var d = document.getElementsByTagName(U[--c]);
        var f = null;
        for (var a = d.length; a > 0;) {
            f = d[--a];
            T = Calendar.getAbsolutePos(f);
            var X = T.x;
            var Y = f.offsetWidth + X;
            var Z = T.y;
            var b = f.offsetHeight + Z;
            if (this.hidden || (X > Q) || (Y < e) || (Z > W) || (b < V)) {
                if (!f.__msh_save_visibility) {
                    f.__msh_save_visibility = S(f)
                }
                f.style.visibility = f.__msh_save_visibility
            } else {
                if (!f.__msh_save_visibility) {
                    f.__msh_save_visibility = S(f)
                }
                f.style.visibility = "hidden"
            }
        }
    }
};
Calendar.prototype._displayWeekdays = function () {
    var J = this.firstDayOfWeek;
    var F = this.firstdayname;
    var H = Calendar._TT.WEEKEND;
    for (var I = 0; I < 7; ++I) {
        F.className = "day name";
        var G = (I + J) % 7;
        if (I) {
            F.ttip = Calendar._TT.DAY_FIRST.replace("%s", Calendar._DN[G]);
            F.navtype = 100;
            F.calendar = this;
            F.fdow = G;
            Calendar._add_evs(F)
        }
        if (H.indexOf(G.toString()) != -1) {
            Calendar.addClass(F, "weekend")
        }
        F.innerHTML = Calendar._SDN[(I + J) % 7];
        F = F.nextSibling
    }
};
Calendar.prototype._hideCombos = function () {
    this.monthsCombo.style.display = "none";
    this.yearsCombo.style.display = "none"
};
Calendar.prototype._dragStart = function (ev) {
    if (this.dragging) {
        return
    }
    this.dragging = true;
    var posX;
    var posY;
    if (Calendar.is_ie) {
        posY = window.event.clientY + document.body.scrollTop;
        posX = window.event.clientX + document.body.scrollLeft
    } else {
        posY = ev.clientY + window.scrollY;
        posX = ev.clientX + window.scrollX
    }
    var st = this.element.style;
    this.xOffs = posX - parseInt(st.left);
    this.yOffs = posY - parseInt(st.top);
    with(Calendar) {
        addEvent(document, "mousemove", calDragIt);
        addEvent(document, "mouseup", calDragEnd)
    }
};
Date._MD = new Array(31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31);
Date.SECOND = 1000;
Date.MINUTE = 60 * Date.SECOND;
Date.HOUR = 60 * Date.MINUTE;
Date.DAY = 24 * Date.HOUR;
Date.WEEK = 7 * Date.DAY;
Date.parseDate = function (X, Q) {
    var W = new Date();
    var V = 0;
    var P = -1;
    var Y = 0;
    var T = X.split(/\W+/);
    var U = Q.match(/%./g);
    var Z = 0,
        N = 0;
    var S = 0;
    var O = 0;
    for (Z = 0; Z < T.length; ++Z) {
        if (!T[Z]) {
            continue
        }
        switch (U[Z]) {
        case "%d":
        case "%e":
            Y = parseInt(T[Z], 10);
            break;
        case "%m":
            P = parseInt(T[Z], 10) - 1;
            break;
        case "%Y":
        case "%y":
            V = parseInt(T[Z], 10);
            (V < 100) && (V += (V > 29) ? 1900 : 2000);
            break;
        case "%b":
        case "%B":
            for (N = 0; N < 12; ++N) {
                if (Calendar._MN[N].substr(0, T[Z].length).toLowerCase() == T[Z].toLowerCase()) {
                    P = N;
                    break
                }
            }
            break;
        case "%H":
        case "%I":
        case "%k":
        case "%l":
            S = parseInt(T[Z], 10);
            break;
        case "%P":
        case "%p":
            if (/pm/i.test(T[Z]) && S < 12) {
                S += 12
            } else {
                if (/am/i.test(T[Z]) && S >= 12) {
                    S -= 12
                }
            }
            break;
        case "%M":
            O = parseInt(T[Z], 10);
            break
        }
    }
    if (isNaN(V)) {
        V = W.getFullYear()
    }
    if (isNaN(P)) {
        P = W.getMonth()
    }
    if (isNaN(Y)) {
        Y = W.getDate()
    }
    if (isNaN(S)) {
        S = W.getHours()
    }
    if (isNaN(O)) {
        O = W.getMinutes()
    }
    if (V != 0 && P != -1 && Y != 0) {
        return new Date(V, P, Y, S, O, 0)
    }
    V = 0;
    P = -1;
    Y = 0;
    for (Z = 0; Z < T.length; ++Z) {
        if (T[Z].search(/[a-zA-Z]+/) != -1) {
            var R = -1;
            for (N = 0; N < 12; ++N) {
                if (Calendar._MN[N].substr(0, T[Z].length).toLowerCase() == T[Z].toLowerCase()) {
                    R = N;
                    break
                }
            }
            if (R != -1) {
                if (P != -1) {
                    Y = P + 1
                }
                P = R
            }
        } else {
            if (parseInt(T[Z], 10) <= 12 && P == -1) {
                P = T[Z] - 1
            } else {
                if (parseInt(T[Z], 10) > 31 && V == 0) {
                    V = parseInt(T[Z], 10);
                    (V < 100) && (V += (V > 29) ? 1900 : 2000)
                } else {
                    if (Y == 0) {
                        Y = T[Z]
                    }
                }
            }
        }
    }
    if (V == 0) {
        V = W.getFullYear()
    }
    if (P != -1 && Y != 0) {
        return new Date(V, P, Y, S, O, 0)
    }
    return W
};
Date.prototype.c_getMonthDays = function (D) {
    var C = this.getFullYear();
    if (typeof D == "undefined") {
        D = this.getMonth()
    }
    if (((0 == (C % 4)) && ((0 != (C % 100)) || (0 == (C % 400)))) && D == 1) {
        return 29
    } else {
        return Date._MD[D]
    }
};
Date.prototype.c_getDayOfYear = function () {
    var D = new Date(this.getFullYear(), this.getMonth(), this.getDate(), 0, 0, 0);
    var E = new Date(this.getFullYear(), 0, 0, 0, 0, 0);
    var F = D - E;
    return Math.floor(F / Date.DAY)
};
Date.prototype.c_getWeekNumber = function () {
    var E = new Date(this.getFullYear(), this.getMonth(), this.getDate(), 0, 0, 0);
    var F = E.getDay();
    E.setDate(E.getDate() - (F + 6) % 7 + 3);
    var D = E.valueOf();
    E.setMonth(0);
    E.setDate(4);
    return Math.round((D - E.valueOf()) / (7 * 86400000)) + 1
};
Date.prototype.c_equalsTo = function (B) {
    return ((this.getFullYear() == B.getFullYear()) && (this.getMonth() == B.getMonth()) && (this.getDate() == B.getDate()) && (this.getHours() == B.getHours()) && (this.getMinutes() == B.getMinutes()))
};
Date.prototype.c_setDateOnly = function (C) {
    var D = new Date(C);
    this.setDate(1);
    this.c_setFullYear(D.getFullYear());
    this.setMonth(D.getMonth());
    this.setDate(D.getDate())
};
Date.prototype.c_print = function (d) {
    var U = this.getMonth();
    var e = this.getDate();
    var c = this.getFullYear();
    var a = this.c_getWeekNumber();
    var Z = this.getDay();
    var V = {};
    var Y = this.getHours();
    var T = (Y >= 12);
    var g = (T) ? (Y - 12) : Y;
    var W = this.c_getDayOfYear();
    if (g == 0) {
        g = 12
    }
    var S = this.getMinutes();
    var f = this.getSeconds();
    V["%a"] = Calendar._SDN[Z];
    V["%A"] = Calendar._DN[Z];
    V["%b"] = Calendar._SMN[U];
    V["%B"] = Calendar._MN[U];
    V["%C"] = 1 + Math.floor(c / 100);
    V["%d"] = (e < 10) ? ("0" + e) : e;
    V["%e"] = e;
    V["%H"] = (Y < 10) ? ("0" + Y) : Y;
    V["%I"] = (g < 10) ? ("0" + g) : g;
    V["%j"] = (W < 100) ? ((W < 10) ? ("00" + W) : ("0" + W)) : W;
    V["%k"] = Y;
    V["%l"] = g;
    V["%m"] = (U < 9) ? ("0" + (1 + U)) : (1 + U);
    V["%M"] = (S < 10) ? ("0" + S) : S;
    V["%n"] = "\n";
    V["%p"] = T ? "PM" : "AM";
    V["%P"] = T ? "pm" : "am";
    V["%s"] = Math.floor(this.getTime() / 1000);
    V["%S"] = (f < 10) ? ("0" + f) : f;
    V["%t"] = "\t";
    V["%U"] = V["%W"] = V["%V"] = (a < 10) ? ("0" + a) : a;
    V["%u"] = Z + 1;
    V["%w"] = Z;
    V["%y"] = ("" + c).substr(2, 2);
    V["%Y"] = c;
    V["%%"] = "%";
    var X = /%./g;
    if (!Calendar.is_ie5 && !Calendar.is_khtml) {
        return d.replace(X, function (A) {
            return V[A] || A
        })
    }
    var b = d.match(X);
    for (var i = 0; i < b.length; i++) {
        var R = V[b[i]];
        if (R) {
            X = new RegExp(b[i], "g");
            d = d.replace(X, R)
        }
    }
    return d
};
Date.prototype.__msh_oldSetFullYear = Date.prototype.setFullYear;
Date.prototype.c_setFullYear = function (D) {
    var C = new Date(this);
    C.__msh_oldSetFullYear(D);
    if (C.getMonth() != this.getMonth()) {
        this.setDate(28)
    }
    this.__msh_oldSetFullYear(D)
};
window._dynarch_popupCalendar = null;
Calendar._DN = new Array("Domingo", "Lunes", "Martes", "Mi&eacute;rcoles", "Jueves", "Viernes", "S&aacute;bado", "Domingo");
Calendar._SDN = new Array("Dom", "Lun", "Mar", "Mi&eacute;", "Jue", "Vie", "S&aacute;b", "Dom");
Calendar._FD = 0;
Calendar._MN = new Array("Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Deciembre");
Calendar._SMN = new Array("Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dec");
Calendar._TT = {};
Calendar._TT.INFO = "Sobre el calendario";
Calendar._TT.ABOUT = "DHTML Date/Time Selector\n(c) dynarch.com 2002-2005 / Autor: Mihai Bazon\n Traductor: Leandro E. Colombo Vi&ntilde;a\nPara la &uacute;ltima versi&oacute;n visite: http://www.dynarch.com/projects/calendar/\nDistribuido bajo licencia GNU LGPL.  See http://gnu.org/licenses/lgpl.html para m&aacute;s detalles.\n\nC&oacute;mo usar:\n- Use los botones \xab, \xbb para seleccionar el a&ntilde;o\n- Use los botones " + String.fromCharCode(8249) + ", " + String.fromCharCode(8250) + " para seleccionar el mes.\n- Mantenga presionado el bot&oacute;n del mouse en cualquiera de los botones anteriormente mencionados para acelerar la b&uacute;squeda.";
Calendar._TT.ABOUT_TIME = "\n\nSelecci&oacute;n de hora:\n- Presione en cualquiera de las partes para incrementarla\n- o Shift-click para decrementarla\n- o presione y arrastre para una selecci&oacute;n m&aacute;s r&aacute;pida.";
Calendar._TT.PREV_YEAR = "A&ntilde;o anterior (Mantenga para men&uacute;)";
Calendar._TT.PREV_MONTH = "Mes  anterior (Mantenga para men&uacute;)";
Calendar._TT.GO_TODAY = "Ir a Hoy";
Calendar._TT.NEXT_MONTH = "Mes siguiente (Mantenga para men&uacute;)";
Calendar._TT.NEXT_YEAR = "A&ntilde;o siguiente (Mantenga para men&uacute;)";
Calendar._TT.SEL_DATE = "Selecciones una fecha";
Calendar._TT.DRAG_TO_MOVE = "Arrastre para mover";
Calendar._TT.PART_TODAY = " (hoy)";
Calendar._TT.DAY_FIRST = "Mostrar %s primero";
Calendar._TT.WEEKEND = "0,6";
Calendar._TT.CLOSE = "Cerrar";
Calendar._TT.TODAY = "Hoy";
Calendar._TT.TIME_PART = "(Shift-)Click o arrastrar para cambiar el valor";
Calendar._TT.DEF_DATE_FORMAT = "%Y-%m-%d";
Calendar._TT.TT_DATE_FORMAT = "%a, %b %e";
Calendar._TT.WK = "sem";
Calendar._TT.TIME = "Hora:";
Calendar.setup = function (I) {
    function J(B, A) {
        if (typeof I[B] == "undefined") {
            I[B] = A
        }
    }
    J("inputField", null);
    J("displayArea", null);
    J("button", null);
    J("eventName", "click");
    J("ifFormat", "%Y/%m/%d");
    J("daFormat", "%Y/%m/%d");
    J("singleClick", true);
    J("disableFunc", null);
    J("dateStatusFunc", I.disableFunc);
    J("dateText", null);
    J("firstDay", null);
    J("align", "Br");
    J("range", [1900, 2999]);
    J("weekNumbers", true);
    J("flat", null);
    J("flatCallback", null);
    J("onSelect", null);
    J("onClose", null);
    J("onUpdate", null);
    J("date", null);
    J("showsTime", false);
    J("timeFormat", "24");
    J("electric", true);
    J("step", 2);
    J("position", null);
    J("cache", false);
    J("showOthers", false);
    J("multiple", null);
    var M = ["inputField", "displayArea", "button"];
    for (var N in M) {
        if (typeof I[M[N]] == "string") {
            I[M[N]] = document.getElementById(I[M[N]])
        }
    }
    if (!(I.flat || I.multiple || I.inputField || I.displayArea || I.button)) {
        alert("Calendar.setup:\n  Nothing to setup (no fields found).  Please check your code");
        return false
    }

    function H(B) {
        var C = B.params;
        var A = (B.dateClicked || C.electric);
        if (A && C.inputField) {
            C.inputField.value = B.date.c_print(C.ifFormat);
            if (typeof C.inputField.onchange == "function") {
                C.inputField.onchange()
            }
        }
        if (A && C.displayArea) {
            C.displayArea.innerHTML = B.date.c_print(C.daFormat)
        }
        if (A && typeof C.onUpdate == "function") {
            C.onUpdate(B)
        }
        if (A && C.flat) {
            if (typeof C.flatCallback == "function") {
                C.flatCallback(B)
            }
        }
        if (A && C.singleClick && B.dateClicked) {
            B.callCloseHandler()
        }
    }
    if (I.flat != null) {
        if (typeof I.flat == "string") {
            I.flat = document.getElementById(I.flat)
        }
        if (!I.flat) {
            alert("Calendar.setup:\n  Flat specified but can't find parent.");
            return false
        }
        var K = new Calendar(I.firstDay, I.date, I.onSelect || H);
        K.showsOtherMonths = I.showOthers;
        K.showsTime = I.showsTime;
        K.time24 = (I.timeFormat == "24");
        K.params = I;
        K.weekNumbers = I.weekNumbers;
        K.setRange(I.range[0], I.range[1]);
        K.setDateStatusHandler(I.dateStatusFunc);
        K.getDateText = I.dateText;
        if (I.ifFormat) {
            K.setDateFormat(I.ifFormat)
        }
        if (I.inputField && typeof I.inputField.value == "string") {
            K.parseDate(I.inputField.value)
        }
        K.create(I.flat);
        K.show();
        return false
    }
    var L = I.button || I.displayArea || I.inputField;
    L["on" + I.eventName] = function () {
        var E = I.inputField || I.displayArea;
        var C = I.inputField ? I.ifFormat : I.daFormat;
        var F = false;
        var A = window.calendar;
        if (E) {
            I.date = Date.parseDate(E.value || E.innerHTML, C)
        }
        if (!(A && I.cache)) {
            window.calendar = A = new Calendar(I.firstDay, I.date, I.onSelect || H, I.onClose || function (P) {
                P.hide()
            });
            A.showsTime = I.showsTime;
            A.time24 = (I.timeFormat == "24");
            A.weekNumbers = I.weekNumbers;
            F = true
        } else {
            if (I.date) {
                A.setDate(I.date)
            }
            A.hide()
        } if (I.multiple) {
            A.multiple = {};
            for (var D = I.multiple.length; --D >= 0;) {
                var G = I.multiple[D];
                var B = G.c_print("%Y%m%d");
                A.multiple[B] = G
            }
        }
        A.showsOtherMonths = I.showOthers;
        A.yearStep = I.step;
        A.setRange(I.range[0], I.range[1]);
        A.params = I;
        A.setDateStatusHandler(I.dateStatusFunc);
        A.getDateText = I.dateText;
        A.setDateFormat(C);
        if (F) {
            A.create()
        }
        A.refresh();
        if (!I.position) {
            A.showAtElement(I.button || I.displayArea || I.inputField, I.align)
        } else {
            A.showAt(I.position[0], I.position[1])
        }
        return false
    };
    return K
};

/* http://keith-wood.name/timeEntry.html
   Time entry for jQuery v1.5.1.
   Written by Keith Wood (kbwood{at}iinet.com.au) June 2007.
   Licensed under the MIT (https://github.com/jquery/jquery/blob/master/MIT-LICENSE.txt) license.
   Please attribute the author if you use it. */
(function ($) {
    function TimeEntry() {
        this._disabledInputs = [];
        this.regional = [];
        this.regional[''] = {
            show24Hours: true,
            separator: ':',
            ampmPrefix: '',
            ampmNames: ['AM', 'PM'],
            spinnerTexts: ['Ahora', 'Campo anterior', 'Campo siguiente', 'Incremento', 'Decremento']
        };
        this._defaults = {
            appendText: '',
            showSeconds: true,
            timeSteps: [1, 1, 1],
            initialField: 0,
            noSeparatorEntry: false,
            useMouseWheel: true,
            defaultTime: null,
            minTime: null,
            maxTime: null,
            spinnerImage: 'spinnerDefault.png',
            spinnerSize: [20, 20, 8],
            spinnerBigImage: '',
            spinnerBigSize: [40, 40, 16],
            spinnerIncDecOnly: false,
            spinnerRepeat: [500, 250],
            beforeShow: null,
            beforeSetTime: null
        };
        $.extend(this._defaults, this.regional[''])
    }
    $.extend(TimeEntry.prototype, {
        markerClassName: 'hasTimeEntry',
        propertyName: 'timeEntry',
        _appendClass: 'timeEntry_append',
        _controlClass: 'timeEntry_control',
        _expandClass: 'timeEntry_expand',
        setDefaults: function (a) {
            $.extend(this._defaults, a || {});
            return this
        },
        _attachPlugin: function (b, c) {
            var d = $(b);
            if (d.hasClass(this.markerClassName)) {
                return
            }
            var e = {
                options: $.extend({}, this._defaults, c),
                input: d,
                _field: 0,
                _selectedHour: 0,
                _selectedMinute: 0,
                _selectedSecond: 0
            };
            d.data(this.propertyName, e).addClass(this.markerClassName).bind('focus.' + this.propertyName, this._doFocus).bind('blur.' + this.propertyName, this._doBlur).bind('click.' + this.propertyName, this._doClick).bind('keydown.' + this.propertyName, this._doKeyDown).bind('keypress.' + this.propertyName, this._doKeyPress).bind('paste.' + this.propertyName, function (a) {
                setTimeout(function () {
                    n._parseTime(e)
                }, 1)
            });
            this._optionPlugin(b, c)
        },
        _optionPlugin: function (a, b, c) {
            a = $(a);
            var d = a.data(this.propertyName);
            if (!b || (typeof b == 'string' && c == null)) {
                var e = b;
                b = (d || {}).options;
                return (b && e ? b[e] : b)
            }
            if (!a.hasClass(this.markerClassName)) {
                return
            }
            b = b || {};
            if (typeof b == 'string') {
                var e = b;
                b = {};
                b[e] = c
            }
            var f = this._extractTime(d);
            $.extend(d.options, b);
            d._field = 0;
            if (f) {
                this._setTime(d, new Date(0, 0, 0, f[0], f[1], f[2]))
            }
            a.next('span.' + this._appendClass).remove();
            a.parent().find('span.' + this._controlClass).remove();
            if ($.fn.mousewheel) {
                a.unmousewheel()
            }
            var g = (!d.options.spinnerImage ? null : $('<span class="' + this._controlClass + '" style="display: inline-block; ' + 'background: url(\'' + d.options.spinnerImage + '\') 0 0 no-repeat; width: ' + d.options.spinnerSize[0] + 'px; height: ' + d.options.spinnerSize[1] + 'px;"></span>'));
            a.after(d.options.appendText ? '<span class="' + this._appendClass + '">' + d.options.appendText + '</span>' : '').after(g || '');
            if (d.options.useMouseWheel && $.fn.mousewheel) {
                a.mousewheel(this._doMouseWheel)
            }
            if (g) {
                g.mousedown(this._handleSpinner).mouseup(this._endSpinner).mouseover(this._expandSpinner).mouseout(this._endSpinner).mousemove(this._describeSpinner)
            }
        },
        _enablePlugin: function (a) {
            this._enableDisable(a, false)
        },
        _disablePlugin: function (a) {
            this._enableDisable(a, true)
        },
        _enableDisable: function (b, c) {
            var d = $.data(b, this.propertyName);
            if (!d) {
                return
            }
            b.disabled = c;
            if (b.nextSibling && b.nextSibling.nodeName.toLowerCase() == 'span') {
                n._changeSpinner(d, b.nextSibling, (c ? 5 : -1))
            }
            n._disabledInputs = $.map(n._disabledInputs, function (a) {
                return (a == b ? null : a)
            });
            if (c) {
                n._disabledInputs.push(b)
            }
        },
        _isDisabledPlugin: function (a) {
            return $.inArray(a, this._disabledInputs) > -1
        },
        _destroyPlugin: function (b) {
            b = $(b);
            if (!b.hasClass(this.markerClassName)) {
                return
            }
            b.removeClass(this.markerClassName).removeData(this.propertyName).unbind('.' + this.propertyName);
            if ($.fn.mousewheel) {
                b.unmousewheel()
            }
            this._disabledInputs = $.map(this._disabledInputs, function (a) {
                return (a == b[0] ? null : a)
            });
            b.siblings('.' + this._appendClass + ',.' + this._controlClass).remove()
        },
        _setTimePlugin: function (a, b) {
            var c = $.data(a, this.propertyName);
            if (c) {
                if (b === null || b === '') {
                    c.input.val('')
                } else {
                    this._setTime(c, b ? (typeof b == 'object' ? new Date(b.getTime()) : b) : null)
                }
            }
        },
        _getTimePlugin: function (a) {
            var b = $.data(a, this.propertyName);
            var c = (b ? this._extractTime(b) : null);
            return (!c ? null : new Date(0, 0, 0, c[0], c[1], c[2]))
        },
        _getOffsetPlugin: function (a) {
            var b = $.data(a, this.propertyName);
            var c = (b ? this._extractTime(b) : null);
            return (!c ? 0 : (c[0] * 3600 + c[1] * 60 + c[2]) * 1000)
        },
        _doFocus: function (a) {
            var b = (a.nodeName && a.nodeName.toLowerCase() == 'input' ? a : this);
            if (n._lastInput == b || n._isDisabledPlugin(b)) {
                n._focussed = false;
                return
            }
            var c = $.data(b, n.propertyName);
            n._focussed = true;
            n._lastInput = b;
            n._blurredInput = null;
            $.extend(c.options, ($.isFunction(c.options.beforeShow) ? c.options.beforeShow.apply(b, [b]) : {}));
            n._parseTime(c);
            setTimeout(function () {
                n._showField(c)
            }, 10)
        },
        _doBlur: function (a) {
            n._blurredInput = n._lastInput;
            n._lastInput = null
        },
        _doClick: function (b) {
            var c = b.target;
            var d = $.data(c, n.propertyName);
            if (!n._focussed) {
                var e = d.options.separator.length + 2;
                d._field = 0;
                if (c.selectionStart != null) {
                    for (var f = 0; f <= Math.max(1, d._secondField, d._ampmField); f++) {
                        var g = (f != d._ampmField ? (f * e) + 2 : (d._ampmField * e) + d.options.ampmPrefix.length + d.options.ampmNames[0].length);
                        d._field = f;
                        if (c.selectionStart < g) {
                            break
                        }
                    }
                } else if (c.createTextRange) {
                    var h = $(b.srcElement);
                    var i = c.createTextRange();
                    var j = function (a) {
                        return {
                            thin: 2,
                            medium: 4,
                            thick: 6
                        }[a] || a
                    };
                    var k = b.clientX + document.documentElement.scrollLeft - (h.offset().left + parseInt(j(h.css('border-left-width')), 10)) - i.offsetLeft;
                    for (var f = 0; f <= Math.max(1, d._secondField, d._ampmField); f++) {
                        var g = (f != d._ampmField ? (f * e) + 2 : (d._ampmField * e) + d.options.ampmPrefix.length + d.options.ampmNames[0].length);
                        i.collapse();
                        i.moveEnd('character', g);
                        d._field = f;
                        if (k < i.boundingWidth) {
                            break
                        }
                    }
                }
            }
            n._showField(d);
            n._focussed = false
        },
        _doKeyDown: function (a) {
            if (a.keyCode >= 48) {
                return true
            }
            var b = $.data(a.target, n.propertyName);
            switch (a.keyCode) {
            case 9:
                return (a.shiftKey ? n._changeField(b, -1, true) : n._changeField(b, +1, true));
            case 35:
                if (a.ctrlKey) {
                    n._setValue(b, '')
                } else {
                    b._field = Math.max(1, b._secondField, b._ampmField);
                    n._adjustField(b, 0)
                }
                break;
            case 36:
                if (a.ctrlKey) {
                    n._setTime(b)
                } else {
                    b._field = 0;
                    n._adjustField(b, 0)
                }
                break;
            case 37:
                n._changeField(b, -1, false);
                break;
            case 38:
                n._adjustField(b, +1);
                break;
            case 39:
                n._changeField(b, +1, false);
                break;
            case 40:
                n._adjustField(b, -1);
                break;
            case 46:
                n._setValue(b, '');
                break;
            default:
                return true
            }
            return false
        },
        _doKeyPress: function (a) {
            var b = String.fromCharCode(a.charCode == undefined ? a.keyCode : a.charCode);
            if (b < ' ') {
                return true
            }
            var c = $.data(a.target, n.propertyName);
            n._handleKeyPress(c, b);
            return false
        },
        _doMouseWheel: function (a, b) {
            if (n._isDisabledPlugin(a.target)) {
                return
            }
            var c = $.data(a.target, n.propertyName);
            c.input.focus();
            if (!c.input.val()) {
                n._parseTime(c)
            }
            n._adjustField(c, b);
            a.preventDefault()
        },
        _expandSpinner: function (b) {
            var c = n._getSpinnerTarget(b);
            var d = $.data(n._getInput(c), n.propertyName);
            if (n._isDisabledPlugin(d.input[0])) {
                return
            }
            if (d.options.spinnerBigImage) {
                d._expanded = true;
                var e = $(c).offset();
                var f = null;
                $(c).parents().each(function () {
                    var a = $(this);
                    if (a.css('position') == 'relative' || a.css('position') == 'absolute') {
                        f = a.offset()
                    }
                    return !f
                });
                $('<div class="' + n._expandClass + '" style="position: absolute; left: ' + (e.left - (d.options.spinnerBigSize[0] - d.options.spinnerSize[0]) / 2 - (f ? f.left : 0)) + 'px; top: ' + (e.top - (d.options.spinnerBigSize[1] - d.options.spinnerSize[1]) / 2 - (f ? f.top : 0)) + 'px; width: ' + d.options.spinnerBigSize[0] + 'px; height: ' + d.options.spinnerBigSize[1] + 'px; background: transparent url(' + d.options.spinnerBigImage + ') no-repeat 0px 0px; z-index: 10;"></div>').mousedown(n._handleSpinner).mouseup(n._endSpinner).mouseout(n._endExpand).mousemove(n._describeSpinner).insertAfter(c)
            }
        },
        _getInput: function (a) {
            return $(a).siblings('.' + n.markerClassName)[0]
        },
        _describeSpinner: function (a) {
            var b = n._getSpinnerTarget(a);
            var c = $.data(n._getInput(b), n.propertyName);
            b.title = c.options.spinnerTexts[n._getSpinnerRegion(c, a)]
        },
        _handleSpinner: function (a) {
            var b = n._getSpinnerTarget(a);
            var c = n._getInput(b);
            if (n._isDisabledPlugin(c)) {
                return
            }
            if (c == n._blurredInput) {
                n._lastInput = c;
                n._blurredInput = null
            }
            var d = $.data(c, n.propertyName);
            n._doFocus(c);
            var e = n._getSpinnerRegion(d, a);
            n._changeSpinner(d, b, e);
            n._actionSpinner(d, e);
            n._timer = null;
            n._handlingSpinner = true;
            if (e >= 3 && d.options.spinnerRepeat[0]) {
                n._timer = setTimeout(function () {
                    n._repeatSpinner(d, e)
                }, d.options.spinnerRepeat[0]);
                $(b).one('mouseout', n._releaseSpinner).one('mouseup', n._releaseSpinner)
            }
        },
        _actionSpinner: function (a, b) {
            if (!a.input.val()) {
                n._parseTime(a)
            }
            switch (b) {
            case 0:
                this._setTime(a);
                break;
            case 1:
                this._changeField(a, -1, false);
                break;
            case 2:
                this._changeField(a, +1, false);
                break;
            case 3:
                this._adjustField(a, +1);
                break;
            case 4:
                this._adjustField(a, -1);
                break
            }
        },
        _repeatSpinner: function (a, b) {
            if (!n._timer) {
                return
            }
            n._lastInput = n._blurredInput;
            this._actionSpinner(a, b);
            this._timer = setTimeout(function () {
                n._repeatSpinner(a, b)
            }, a.options.spinnerRepeat[1])
        },
        _releaseSpinner: function (a) {
            clearTimeout(n._timer);
            n._timer = null
        },
        _endExpand: function (a) {
            n._timer = null;
            var b = n._getSpinnerTarget(a);
            var c = n._getInput(b);
            var d = $.data(c, n.propertyName);
            $(b).remove();
            d._expanded = false
        },
        _endSpinner: function (a) {
            n._timer = null;
            var b = n._getSpinnerTarget(a);
            var c = n._getInput(b);
            var d = $.data(c, n.propertyName);
            if (!n._isDisabledPlugin(c)) {
                n._changeSpinner(d, b, -1)
            }
            if (n._handlingSpinner) {
                n._lastInput = n._blurredInput
            }
            if (n._lastInput && n._handlingSpinner) {
                n._showField(d)
            }
            n._handlingSpinner = false
        },
        _getSpinnerTarget: function (a) {
            return a.target || a.srcElement
        },
        _getSpinnerRegion: function (a, b) {
            var c = this._getSpinnerTarget(b);
            var d = $(c).offset();
            var e = [document.documentElement.scrollLeft || document.body.scrollLeft, document.documentElement.scrollTop || document.body.scrollTop];
            var f = (a.options.spinnerIncDecOnly ? 99 : b.clientX + e[0] - d.left);
            var g = b.clientY + e[1] - d.top;
            var h = a.options[a._expanded ? 'spinnerBigSize' : 'spinnerSize'];
            var i = (a.options.spinnerIncDecOnly ? 99 : h[0] - 1 - f);
            var j = h[1] - 1 - g;
            if (h[2] > 0 && Math.abs(f - i) <= h[2] && Math.abs(g - j) <= h[2]) {
                return 0
            }
            var k = Math.min(f, g, i, j);
            return (k == f ? 1 : (k == i ? 2 : (k == g ? 3 : 4)))
        },
        _changeSpinner: function (a, b, c) {
            $(b).css('background-position', '-' + ((c + 1) * a.options[a._expanded ? 'spinnerBigSize' : 'spinnerSize'][0]) + 'px 0px')
        },
        _parseTime: function (a) {
            var b = this._extractTime(a);
            if (b) {
                a._selectedHour = b[0];
                a._selectedMinute = b[1];
                a._selectedSecond = b[2]
            } else {
                var c = this._constrainTime(a);
                a._selectedHour = c[0];
                a._selectedMinute = c[1];
                a._selectedSecond = (a.options.showSeconds ? c[2] : 0)
            }
            a._secondField = (a.options.showSeconds ? 2 : -1);
            a._ampmField = (a.options.show24Hours ? -1 : (a.options.showSeconds ? 3 : 2));
            a._lastChr = '';
            a._field = Math.max(0, Math.min(Math.max(1, a._secondField, a._ampmField), a.options.initialField));
            if (a.input.val() != '') {
                this._showTime(a)
            }
        },
        _extractTime: function (a, b) {
            b = b || a.input.val();
            var c = b.split(a.options.separator);
            if (a.options.separator == '' && b != '') {
                c[0] = b.substring(0, 2);
                c[1] = b.substring(2, 4);
                c[2] = b.substring(4, 6)
            }
            if (c.length >= 2) {
                var d = !a.options.show24Hours && (b.indexOf(a.options.ampmNames[0]) > -1);
                var e = !a.options.show24Hours && (b.indexOf(a.options.ampmNames[1]) > -1);
                var f = parseInt(c[0], 10);
                f = (isNaN(f) ? 0 : f);
                f = ((d || e) && f == 12 ? 0 : f) + (e ? 12 : 0);
                var g = parseInt(c[1], 10);
                g = (isNaN(g) ? 0 : g);
                var h = (c.length >= 3 ? parseInt(c[2], 10) : 0);
                h = (isNaN(h) || !a.options.showSeconds ? 0 : h);
                return this._constrainTime(a, [f, g, h])
            }
            return null
        },
        _constrainTime: function (a, b) {
            var c = (b != null);
            if (!c) {
                var d = this._determineTime(a.options.defaultTime, a) || new Date();
                b = [d.getHours(), d.getMinutes(), d.getSeconds()]
            }
            var e = false;
            for (var i = 0; i < a.options.timeSteps.length; i++) {
                if (e) {
                    b[i] = 0
                } else if (a.options.timeSteps[i] > 1) {
                    b[i] = Math.round(b[i] / a.options.timeSteps[i]) * a.options.timeSteps[i];
                    e = true
                }
            }
            return b
        },
        _showTime: function (a) {
            var b = (this._formatNumber(a.options.show24Hours ? a._selectedHour : ((a._selectedHour + 11) % 12) + 1) + a.options.separator + this._formatNumber(a._selectedMinute) + (a.options.showSeconds ? a.options.separator + this._formatNumber(a._selectedSecond) : '') + (a.options.show24Hours ? '' : a.options.ampmPrefix + a.options.ampmNames[(a._selectedHour < 12 ? 0 : 1)]));
            this._setValue(a, b);
            this._showField(a)
        },
        _showField: function (a) {
            var b = a.input[0];
            if (a.input.is(':hidden') || n._lastInput != b) {
                return
            }
            var c = a.options.separator.length + 2;
            var d = (a._field != a._ampmField ? (a._field * c) : (a._ampmField * c) - a.options.separator.length + a.options.ampmPrefix.length);
            var e = d + (a._field != a._ampmField ? 2 : a.options.ampmNames[0].length);
            if (b.setSelectionRange) {
                b.setSelectionRange(d, e)
            } else if (b.createTextRange) {
                var f = b.createTextRange();
                f.moveStart('character', d);
                f.moveEnd('character', e - a.input.val().length);
                f.select()
            }
            if (!b.disabled) {
                b.focus()
            }
        },
        _formatNumber: function (a) {
            return (a < 10 ? '0' : '') + a
        },
        _setValue: function (a, b) {
            if (b != a.input.val()) {
                a.input.val(b).trigger('change')
            }
        },
        _changeField: function (a, b, c) {
            var d = (a.input.val() == '' || a._field == (b == -1 ? 0 : Math.max(1, a._secondField, a._ampmField)));
            if (!d) {
                a._field += b
            }
            this._showField(a);
            a._lastChr = '';
            return (d && c)
        },
        _adjustField: function (a, b) {
            if (a.input.val() == '') {
                b = 0
            }
            this._setTime(a, new Date(0, 0, 0, a._selectedHour + (a._field == 0 ? b * a.options.timeSteps[0] : 0) + (a._field == a._ampmField ? b * 12 : 0), a._selectedMinute + (a._field == 1 ? b * a.options.timeSteps[1] : 0), a._selectedSecond + (a._field == a._secondField ? b * a.options.timeSteps[2] : 0)))
        },
        _setTime: function (a, b) {
            b = this._determineTime(b, a);
            var c = this._constrainTime(a, b ? [b.getHours(), b.getMinutes(), b.getSeconds()] : null);
            b = new Date(0, 0, 0, c[0], c[1], c[2]);
            var b = this._normaliseTime(b);
            var d = this._normaliseTime(this._determineTime(a.options.minTime, a));
            var e = this._normaliseTime(this._determineTime(a.options.maxTime, a));
            b = (d && b < d ? d : (e && b > e ? e : b));
            if ($.isFunction(a.options.beforeSetTime)) {
                b = a.options.beforeSetTime.apply(a.input[0], [this._getTimePlugin(a.input[0]), b, d, e])
            }
            a._selectedHour = b.getHours();
            a._selectedMinute = b.getMinutes();
            a._selectedSecond = b.getSeconds();
            this._showTime(a)
        },
        _determineTime: function (i, j) {
            var k = function (a) {
                var b = new Date();
                b.setTime(b.getTime() + a * 1000);
                return b
            };
            var l = function (a) {
                var b = n._extractTime(j, a);
                var c = new Date();
                var d = (b ? b[0] : c.getHours());
                var e = (b ? b[1] : c.getMinutes());
                var f = (b ? b[2] : c.getSeconds());
                if (!b) {
                    var g = /([+-]?[0-9]+)\s*(s|S|m|M|h|H)?/g;
                    var h = g.exec(a);
                    while (h) {
                        switch (h[2] || 's') {
                        case 's':
                        case 'S':
                            f += parseInt(h[1], 10);
                            break;
                        case 'm':
                        case 'M':
                            e += parseInt(h[1], 10);
                            break;
                        case 'h':
                        case 'H':
                            d += parseInt(h[1], 10);
                            break
                        }
                        h = g.exec(a)
                    }
                }
                c = new Date(0, 0, 10, d, e, f, 0);
                if (/^!/.test(a)) {
                    if (c.getDate() > 10) {
                        c = new Date(0, 0, 10, 23, 59, 59)
                    } else if (c.getDate() < 10) {
                        c = new Date(0, 0, 10, 0, 0, 0)
                    }
                }
                return c
            };
            return (i ? (typeof i == 'string' ? l(i) : (typeof i == 'number' ? k(i) : i)) : null)
        },
        _normaliseTime: function (a) {
            if (!a) {
                return null
            }
            a.setFullYear(1900);
            a.setMonth(0);
            a.setDate(0);
            return a
        },
        _handleKeyPress: function (a, b) {
            if (b == a.options.separator) {
                this._changeField(a, +1, false)
            } else if (b >= '0' && b <= '9') {
                var c = parseInt(b, 10);
                var d = parseInt(a._lastChr + b, 10);
                var e = (a._field != 0 ? a._selectedHour : (a.options.show24Hours ? (d < 24 ? d : c) : (d >= 1 && d <= 12 ? d : (c > 0 ? c : a._selectedHour)) % 12 + (a._selectedHour >= 12 ? 12 : 0)));
                var f = (a._field != 1 ? a._selectedMinute : (d < 60 ? d : c));
                var g = (a._field != a._secondField ? a._selectedSecond : (d < 60 ? d : c));
                var h = this._constrainTime(a, [e, f, g]);
                this._setTime(a, new Date(0, 0, 0, h[0], h[1], h[2]));
                if (a.options.noSeparatorEntry && a._lastChr) {
                    this._changeField(a, +1, false)
                } else {
                    a._lastChr = b
                }
            } else if (!a.options.show24Hours) {
                b = b.toLowerCase();
                if ((b == a.options.ampmNames[0].substring(0, 1).toLowerCase() && a._selectedHour >= 12) || (b == a.options.ampmNames[1].substring(0, 1).toLowerCase() && a._selectedHour < 12)) {
                    var i = a._field;
                    a._field = a._ampmField;
                    this._adjustField(a, +1);
                    a._field = i;
                    this._showField(a)
                }
            }
        }
    });
    var m = ['getOffset', 'getTime', 'isDisabled'];

    function isNotChained(a, b) {
        if (a == 'option' && (b.length == 0 || (b.length == 1 && typeof b[0] == 'string'))) {
            return true
        }
        return $.inArray(a, m) > -1
    }
    $.fn.timeEntry = function (b) {
        var c = Array.prototype.slice.call(arguments, 1);
        if (isNotChained(b, c)) {
            return n['_' + b + 'Plugin'].apply(n, [this[0]].concat(c))
        }
        return this.each(function () {
            if (typeof b == 'string') {
                if (!n['_' + b + 'Plugin']) {
                    throw 'Unknown command: ' + b;
                }
                n['_' + b + 'Plugin'].apply(n, [this].concat(c))
            } else {
                var a = ($.fn.metadata ? $(this).metadata() : {});
                n._attachPlugin(this, $.extend({}, a, b || {}))
            }
        })
    };
    var n = $.timeEntry = new TimeEntry()
})(jQuery);