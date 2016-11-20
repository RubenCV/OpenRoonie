/*globals Anywhere, SockJS, hterm, lib, jQuery, */

(function ($) {

    hterm.defaultStorage = new lib.Storage.Local();

    var _startSockJS = function (consoleServer, sessionKey, consoleID, guid) {
        var whitelist = ['websocket', 'xdr-streaming', 'xhr-streaming', 'iframe-eventsource', 'iframe-htmlfile', 'xdr-polling', 'xhr-polling', 'iframe-xhr-polling', 'jsonp-polling'];
        $('#id_connecting_to_server_indicator_text').text(
            "Starting encrypted connection to " + consoleServer + " on port 443"
        );
        $('#id_connecting_to_server_indicator').show();
        if (Anywhere.sockjs) {
            Anywhere.sockjs.onclose = function () {};
            Anywhere.sockjs.close();
        }
        Anywhere.sockjs = new SockJS('https://' + consoleServer + '/sj', null, {protocols_whitelist: whitelist});
        Anywhere.sockjs.onopen = function () {
            Anywhere.reconnect_wait = 1000;
            Anywhere.terminal.reset();
            Anywhere.sockjs.send('\x1b[' + sessionKey + ';' + consoleID + ';' + guid + ';a');
            $('#id_connecting_to_server_indicator').hide();
            Anywhere.sockjs.send('\x1b[8;' + Anywhere.terminal.screenSize.height + ";" + Anywhere.terminal.screenSize.width + 't');
        };
        Anywhere.sockjs.onmessage = _incomingMessageHandler;
        Anywhere.sockjs.onerror = Anywhere.reconnect;
        Anywhere.sockjs.onclose = Anywhere.reconnect;

        Anywhere.incoming = [];
    };

    var _incomingMessageHandler = function (data) {
        Anywhere.incoming.push(data.data);
        setTimeout(
            function () {
                var nextData = Anywhere.incoming.shift();
                Anywhere.terminal.io.print(nextData);
            },
            0
        );
    };

    var _keyPressHandler = function (chars) {
        Anywhere.sockjs.send(chars);
    };

    var lastWidth;
    var lastHeight;
    var _resizeHandler = function (width, height) {
        if (Anywhere.sockjs.readyState !== SockJS.OPEN) {
            return;
        }
        if (width !== lastWidth || height !== lastHeight) {
            Anywhere.sockjs.send('\x1b[8;' + height + ";" + width + 't');
            lastWidth = width;
            lastHeight = height;
        }
    };

    var _startShell = function (isMobile) {
        var terminal = new hterm.Terminal();
        Anywhere.terminal = terminal;
        terminal.prefs_.set("send-encoding", "raw");
        terminal.prefs_.set("receive-encoding", "utf-8");
        terminal.prefs_.set("ctrl-c-copy", true);
        terminal.prefs_.set("ctrl-v-paste", true);
        terminal.prefs_.set('use-default-window-copy', true);
        terminal.prefs_.set(
            'font-family',
            '"DejaVu Sans Mono for Powerline", "DejaVu Sans Mono", "Everson Mono", "FreeMono", "Menlo", "Lucida Console", "Terminal", "Source Code Pro", "monospace"'
        );
        terminal.onTerminalReady = function () {
            var io = terminal.io.push();
            io.onVTKeystroke = _keyPressHandler;
            io.sendString = _keyPressHandler;
            io.onTerminalResize = _resizeHandler;
        };

        terminal.decorate(document.querySelector("#terminal"), isMobile);
        terminal.installKeyboard();
    };

    var LoadConsole = function (consoleServer, sessionKey, consoleId, guid, isMobile) {
        var startSockJS = function () {Anywhere._startSockJS(consoleServer, sessionKey, consoleId, guid);};
        Anywhere._startShell(isMobile);
        Anywhere.reconnect = function () {
            setTimeout(startSockJS, Anywhere.reconnect_wait);
            Anywhere.reconnect_wait *= 2;
            if (Anywhere.reconnect_wait > 16000) {
                Anywhere.reconnect_wait = 16000;
            }
        };
        startSockJS();
    };


    $.extend(true, window, {
        'Anywhere': {
            'connected': false,
            'LoadConsole': LoadConsole,
            'reconnect': null,
            'reconnect_wait': 1000,
            'terminal': null,
            'sockjs': null,
            '_incomingMessageHandler': _incomingMessageHandler,
            '_resizeHandler': _resizeHandler,
            '_keyPressHandler': _keyPressHandler,
            '_startShell': _startShell,
            '_startSockJS': _startSockJS
        }
    });

})(jQuery);
