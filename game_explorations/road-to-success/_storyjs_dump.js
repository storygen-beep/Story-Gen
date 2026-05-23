/* twine-user-script #1: "StoryScript" */
Config.passages.nobr = true;
Config.saves.maxAutoSaves = 1;

var cryptoScript = document.createElement('script');
cryptoScript.src = "https://cdnjs.cloudflare.com/ajax/libs/crypto-js/4.1.1/crypto-js.min.js";
document.head.appendChild(cryptoScript);

window.gameVersion = "0.25";
window.patreon = false;
/* twine-user-script #2: "colors.js" */
Macro.add('pink', {
    tags: null,
    handler: function () {
      if (this.payload[0].contents === '') {
        return;
      }
  
      var texto = this.payload[0].contents.trim();
      var span = document.createElement('span');
      span.style.color = 'pink';
      span.textContent = texto;
      this.output.appendChild(span);
    }
});

Macro.add('red', {
    tags: null,
    handler: function () {
      if (this.payload[0].contents === '') {
        return;
      }
  
      var texto = this.payload[0].contents.trim();
      var span = document.createElement('span');
      span.style.color = 'red';
      span.textContent = texto;
      this.output.appendChild(span);
    }
});

Macro.add('blue', {
    tags: null,
    handler: function () {
      if (this.payload[0].contents === '') {
        return;
      }
  
      var texto = this.payload[0].contents.trim();
      var span = document.createElement('span');
      span.style.color = 'blue';
      span.textContent = texto;
      this.output.appendChild(span);
    }
});

Macro.add('green', {
    tags: null,
    handler: function () {
      if (this.payload[0].contents === '') {
        return;
      }
  
      var texto = this.payload[0].contents.trim();
      var span = document.createElement('span');
      span.style.color = 'green';
      span.textContent = texto;
      this.output.appendChild(span);
    }
});
/* twine-user-script #3: "cycles.js" */
(function () {
    'use strict';
    // cycles.js, by chapel; for SugarCube 2
    // v2.1.1

    // OPTIONS

    var options = {
        storyVar : '%%cycles',
        tryGlobal : true,
        pauseTag : 'cycles.pause',
        menuPauseTag : 'cycles.pause.menu',
        taskObject : 'cycles.postdisplay'
    };

    // stateful storage

    State.variables[options.storyVar] = {};

    // utilities

    function _get () {
        return State.variables[options.storyVar];
    }

    function _payloadMapper (pl) {
        if (pl.args.length < 1) {
            return null;
        }
        var phases = pl.args.flat(Infinity);
        if (!phases.every(function (ph) {
            return typeof ph === 'string';
        })) {
            return null;
        }
        return phases;
    }

    // CLASS

    /* 
        Cycle definition:
            {
                phases (array): the list of phases the cycle moves through
                period (number) (default 1): the number of turns that constitute a single cycle change
                increment (number) (default 1): the amount to increment a cycle per turn
                active (boolean) (default true): whether the cycle should start active or paused
            }
            stack (default 0)
    */

    function Cycle (def, stack) {
        if (!(this instanceof Cycle)) {
            return new Cycle(def, stack);
        }

        if (!def || typeof def !== 'object') {
            throw new Error('Cycle() -> invalid definition object');
        }

        if (!def.name || typeof def.name !== 'string' || !def.name.trim()) {
            throw new Error('Cycle() -> invalid name');
        }
        this.name = def.name;

        if (!def.phases || !Array.isArray(def.phases) || def.phases.length < 2) {
            throw new Error('Cycle() -> phases should be an array of at least two strings');
        }
        if (!def.phases.every( function (ph) {
            return ph && typeof ph === 'string' && ph.trim();
        })) {
            throw new Error('Cycle() -> each phase should be a valid, non-empty string');
        }
        this.phases = clone(def.phases);

        def.period = Number(def.period);
        if (Number.isNaN(def.period) || def.period < 1) {
            def.period = 1;
        }
        if (!Number.isInteger(def.period)) {
            def.period = Math.trunc(def.period);
        }
        this.period = def.period;

        def.increment = Number(def.increment);
        if (Number.isNaN(def.increment) || def.increment < 1) {
            def.increment = 1;
        }
        if (!Number.isInteger(def.increment)) {
            def.increment = Math.trunc(def.increment);
        }
        this.increment = def.increment;

        this.active = (def.active === undefined) ? true : !!def.active;

        stack = Number(stack);
        if (Number.isNaN(stack) || stack < 0) {
            stack = 0;
        }
        if (!Number.isInteger(stack)) {
            stack = Math.trunc(stack);
        }
        this.stack = stack;
    }

    Object.assign(Cycle, {
        is : function (thing) {
            return thing instanceof Cycle;
        },
        add : function (name, def) {
            if (!def || typeof def !== 'object') {
                throw new Error('Cycle.add() -> invalid definition object');
            }
            if (!name || typeof name !== 'string' || !name.trim()) {
                if (!def.name || typeof def.name !== 'string' || !def.name.trim()) {
                    throw new Error('Cycle.add() -> invalid name');
                }
            } else {
                def.name = name;
            }
            var c = new Cycle(def, 0);
            _get()[def.name] = c;
            return c;
        },
        has : function (name) {
            var got = _get();
            return got.hasOwnProperty(name) && Cycle.is(got[name]);
        },
        get : function (name) {
            if (Cycle.has(name)) {
                return _get()[name];
            }
            return null;
        },
        del : function (name) {
            if (Cycle.has(name)) {
                delete _get()[name];
                return true;
            }
            return false;
        },
        check : function (name) {
            if (Cycle.has(name)) {
                var phases = [].slice.call(arguments).flat(Infinity).slice(1);
                return Cycle.get(name).check(phases);
            }
        },
        clear : function (name) {
            var got = _get();
            got = {};
        },
        _emit : function (inst, type) {
            $(document).trigger({
                type : ':cycle-' + type,
                cycle : inst
            });
        },
        _retrieveCycles : _get
    });

    Object.assign(Cycle.prototype, {
        constructor : Cycle,
        revive : function () {
            var ownData = {};
            Object.keys(this).forEach(function (pn) {
                ownData[pn] = clone(this[pn]);
            }, this);
            return ownData;
        },
        clone : function () { // for SC
            return new Cycle(this.revive(), this.stack);
        },
        toJSON : function () { // for SC
            return Serial.createReviver('new setup.Cycle(' + JSON.stringify(this.revive()) + ', ' + this.stack + ')');
        },
        current : function () {
            // returns the current phase based on the stack
            return this.phases[Math.trunc(this.stack / this.period) % this.phases.length];
        },
        length : function () {
            // returns the length (in increments)
            return this.period * this.phases.length;
        },
        turns : function () {
            return this.period / this.increment;
        },
        turnsTotal : function () {
            return this.length() / this.increment;
        },
        update : function (by) {
            // add or subtract from the stack
            by = Number(by);
            if (Number.isNaN(by)) {
                by = this.increment; // 0 is valid, increment is default, negatives are possible
            }
            var cache = this.current();
            this.stack += by;
            if (this.stack < 0) {
                this.stack = 0;
            }
            if (!Number.isInteger(this.stack)) {
                this.stack = Math.trunc(this.stack);
            }
            if (cache !== this.current()) {
                // the phase changed
                Cycle._emit(this, 'change');
            }
            return this;
        },
        reset : function () {
            // reset stack to 0, and phase
            this.stack = 0;
            Cycle._emit(this, 'reset');
            return this.update(0);
        },
        suspend : function () {
            // suspend a cycle (pause it)
            var cache = this.active;
            this.active = false;
            if (cache !== this.active) {
                Cycle._emit(this, 'suspend');
            }
            return this;
        },
        resume : function () {
            // resume a suspended cycle
            var cache = this.active;
            this.active = true;
            if (cache !== this.active) {
                Cycle._emit(this, 'resume');
            }
            return this;
        },
        toggle : function () {
            // toggle a cycle's active state
            if (this.active) {
                this.suspend();
            } else {
                this.resume();
            }
            return this;
        },
        isSuspended : function () {
            // what it says on the tin
            return !this.active;
        },
        editIncrement : function (set) {
            // get or set the increment (how much the stack goes up per turn)
            set = Number(set);
            if (!Number.isNaN(set) || set > 0) {
                if (!Number.isInteger(set)) {
                    set = Math.trunc(set);
                }
                this.increment = set;
            }
            return this.increment;
        },
        check : function () {
            var phases = [].slice.call(arguments).flat(Infinity);
            return phases.includes(this.current());
        }
    });

    // main postdisplay

    postdisplay[options.taskObject] = function () {
        var skipNext;
        if (tags().includes(options.pauseTag) || skipNext) {
            // pause tag handling
            skipNext = false;
            return;
        }
        if (tags().includes(options.menuPauseTag)) {
            skipNext = true; // skip next passage too
            return;
        }
        Object.keys(_get()).forEach( function (name) {
            // look at each defined cycle
            var cycle = Cycle.get(name);
            if (!cycle.active) {
                // suspended cycles
                return;
            }
            // active cycles
            cycle.update();
        });
    };

    // APIs

    setup.Cycle = Cycle;
    if (options.tryGlobal) {
        window.Cycle = window.Cycle || Cycle;
    }

    // MACROS

    /*
        <<newcycle name period increment suspend>>
            <<phase name [name]>> (requires at least two phases, can be in one phase tag or several)
            <<phase name>>
        <</newcycle>>

    */
    Macro.add('newcycle', {
        tags : ['phase'],
        handler : function () {

            if (this.args.length < 1) {
                return this.error('A cycle must at least be given a name.');
            }

            if (this.payload.length < 2) {
                return this.error('A cycle must be given at least two phases.');
            }

            // render the payload tags' args as cycles
            var phases = this.payload.slice(1).map( function (pl) {
                return _payloadMapper(pl);
            }).flat(Infinity);

            if (phases.includes(null)) {
                // throw on junk phases
                return this.error('Each `<<phase>>` tag must be given a valid name.');
            }

            try {
                Cycle.add(this.args[0], {
                    // create the cycle
                    phases : phases,
                    period : this.args[1],
                    increment : this.args[2],
                    // `suspend`` keyword
                    active : (this.args[3] && typeof this.args[3] === 'string' && (this.args[3].trim() !== 'suspend'))
                });
            } catch (err) {
                // render errors
                var preferredMessage = err.message && err.message.split('->')[1];
                preferredMessage = preferredMessage ? preferredMessage.trim() : false;
                return this.error(preferredMessage || err.message);
            }
        }
    });

    // <<editcycle name actionList>>
    // actions: suspend/toggle/resume, increment n, period n, reset/clear, change n
    Macro.add('editcycle', {
        handler : function () {

            if (this.args.length < 1 || typeof this.args[0] !== 'string' || !this.args[0].trim()) {
                return this.error('You must name the cycle you wish to act on.');
            }
            if (this.args.length < 2) {
                return this.error('You must provide an action to perform.');
            }

            var cycle = Cycle.get(this.args[0]);

            if (cycle === null) {
                return this.error('Cannot find a cycle named "' + this.args[0] + '".');
            }

            // suspend, resume, toggle
            if (this.args.includes('suspend')) {
                cycle.suspend();
            } else if (this.args.includes('toggle')) {
                cycle.toggle();
            } else if (this.args.includes('resume')) {
                cycle.resume();
            }

            // change increment or period
            if (this.args.includes('increment')) {
                var value = this.args[this.args.indexOf('increment') + 1];
                if (typeof value === 'number') {
                    cycle.editIncrement(value);
                }
            }

            // reset cycle
            if (this.args.includesAny('reset', 'clear')) {
                cycle.reset();
            }

            // increase / decrease cycle
            if (this.args.includes('change')) {
                var add = this.args[this.args.indexOf('change') + 1];
                add = Number(add);
                if (!Number.isNaN(add) && Number.isInteger(add)) {
                    cycle.update(add);
                }
            }

        }
    });

    // <<showcycle name [options]>> (options: uppercase, lowercase, upperfirst)
    Macro.add('showcycle', {
        handler : function () {

            if (this.args.length < 1 || typeof this.args[0] !== 'string' || !this.args[0].trim()) {
                return this.error('You must name the cycle you wish to act on.');
            }

            var cycle = Cycle.get(this.args[0]);

            if (cycle === null) {
                return this.error('Cannot find a cycle named "' + this.args[0] + '".');
            }

            // formatting keywords
            var display = cycle.current();
            if (this.args.includes('uppercase')) {
                display = display.toUpperCase();
            } else if (this.args.includes('lowercase')) {
                display = display.toLowerCase();
            } else if (this.args.includes('upperfirst')) {
                display = display.toUpperFirst();
            }

            $(document.createElement('span'))
                .addClass('macro-' + this.name)
                .append(display)
                .appendTo(this.output);

        }
    });

}());
/* twine-user-script #4: "dialogs.js" */

(function () {
    function getDialog(id) {
        return document.getElementById(id);
    }

    window.openDialog = function (id) {
    const dlg = getDialog(id);
        if (!dlg || dlg.open) return;
        dlg.showModal();
    };

    window.closeDialog = function (id) {
    const dlg = getDialog(id);
    if (!dlg || !dlg.open) return;

    // Evita múltiplos disparos
    if (dlg.classList.contains('closing')) return;

    dlg.classList.add('closing');
    dlg.addEventListener('animationend', () => {
        dlg.classList.remove('closing');
    dlg.close();
    }, {once: true });
  };

  // Fazer ESC fechar suavemente também
  ['questbook','inventory','relations'].forEach(id => {
    const dlg = getDialog(id);
    if (!dlg) return;
    dlg.addEventListener('cancel', (ev) => {
        ev.preventDefault();
    window.closeDialog(id);
    });
  });

})();
/* twine-user-script #5: "flash.js" */
// FlashMessage macro by SjoerdHekking
setup.isFontAvailable = function (fontName, testChar) {
	const testSize = '72px';
	const span = document.createElement('span');
	span.style.fontSize = testSize;
	span.style.position = 'absolute';
	span.style.left = '-9999px';
	span.textContent = testChar || 'a';
	span.style.fontFamily = 'monospace';
	document.body.appendChild(span);
	const baselineWidth = span.offsetWidth;
	span.style.fontFamily = `${fontName}, monospace`;
	const testFontWidth = span.offsetWidth;
	document.body.removeChild(span);

	return testFontWidth !== baselineWidth;
};
$(document).one(':passageend', function (ev) {
	if (setup.isFontAvailable('Font Awesome', '\f071')) {
		document.documentElement.style.setProperty('--icon-font-family', 'Font Awesome');
		document.documentElement.style.setProperty('--success-icon-content', '"\\f00c"');  // Check icon
		document.documentElement.style.setProperty('--warning-icon-content', '"\\f071"');  // Warning icon
		document.documentElement.style.setProperty('--error-icon-content', '"\\f00d"');    // Error icon
		document.documentElement.style.setProperty('--info-icon-content', '"\\f05a"');     // Info icon
		document.documentElement.style.setProperty('--bug-icon-content', '"\\f188"');      // Bug icon
		document.documentElement.style.setProperty('--disabled-icon-content', '"\\e88e"'); // Disabled icon
		document.documentElement.style.setProperty('--corruption-icon-content', "'\\e391'");  // Corruption icon
		document.documentElement.style.setProperty('--arousal-icon-content', '"\\e390"');     // Arousal icon
		document.documentElement.style.setProperty('--int-icon-content', '"\\f5dc"');         // Intelligence icon
		document.documentElement.style.setProperty('--exb-icon-content', '"\\e367"');         // Exhibitionism icon
		document.documentElement.style.setProperty('--fitness-icon-content', '"\\f44b"');     // Fitness icon
		document.documentElement.style.setProperty('--social-icon-content', '"\\f075"');      // Social icon
		document.documentElement.style.setProperty('--beauty-icon-content', '"\\f600"');     // Beauty icon
		document.documentElement.style.setProperty('--money-icon-content', '"\\f0d6"');   // Money icon
		document.documentElement.style.setProperty('--love-icon-content', '"\\f004"');      // Love icon
	}
});

class FlashMessageManager {
	static DEFAULT_OPTIONS = {
		limit: 0,
		debug: false
	};

	static bag = [];
	static displayed = [];
	static displayedMessage = [];
	static _displayQueue = 0;

	constructor(message, flashOptions) {
		this.options = FlashMessageManager.DEFAULT_OPTIONS;
		this.singleMessage = this.formatMessage(message, flashOptions);
		this.checkLimit();
	}

	/**
	 * Sets a random ID
	 * @returns {String} UUID4 format.
	 */
	genNewID() {
		return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
			const r = Math.random() * 16 | 0;
			const v = c === 'x' ? r : (r & 0x3 | 0x8);
			return v.toString(16);
		});
	}
	/**
	 * Formats a message to a bag-able object with an unique ID.
	 * @param {string} message The text to format
	 * @param {Object} flashOptions The options to pass down
	 * @returns Formatted message
	 */
	formatMessage(message, flashOptions) {
		if (!message && !flashOptions) {
			return null;
		} else {
			const tempMessage = {
				message: message,
				flashOptions: flashOptions,
				id: this.genNewID()
			};
			return tempMessage;
		}
	}

	/**
	 * Check if a display limit has been set, if so, queue message, else pass them down.
	 * @returns Notification creation or queueing
	 */
	checkLimit() {
		if (this.singleMessage !== null) {
			FlashMessageManager.bag.push(this);
		}

		if (FlashMessageManager.bag.length === 0) {
			this.garbageCollection();
			return;
		}

		if ((FlashMessageManager._displayQueue >= this.options.limit) && (this.options.limit > 0)) {
			// FlashMessageManager.bag.length > this.options.limit
			if (this.options.debug) {
				console.log("Display limit (" + this.options.limit + ") reached, queueing message, bag is holding: " + (FlashMessageManager.bag.length - this.options.limit) + " messages.");
			}
			return;
		}

		const nextMessage = FlashMessageManager.bag.find(
			(instance) => !FlashMessageManager.displayed.includes(instance.singleMessage.id)
		);

		if (!nextMessage) {
			if (this.options.debug) {
				console.log("Can not find more messages, the bag is probably empty, waiting for confirmation.");
			}
			return;
		}

		if (this.options.debug) {
			console.log("Displaying message:", nextMessage.singleMessage);
		}

		const messageExists = FlashMessageManager.displayedMessage.includes(nextMessage.singleMessage.message);

		if (messageExists) {
			if (this.options.debug) {
				console.log("Message already displayed, waiting for confirmation.");
			}
			FlashMessageManager.bag = FlashMessageManager.bag.filter((item) => item.singleMessage.id !== nextMessage.singleMessage.id);
			return;
		}

		FlashMessageManager.create(nextMessage.singleMessage);
		FlashMessageManager.displayed.push(nextMessage.singleMessage.id);
		FlashMessageManager.displayedMessage.push(nextMessage.singleMessage.message);
	}

	/**
	 * If the bag has been emptied, be sure to clean the history even if it is cleaned.
	 */
	garbageCollection() {
		if (this.options.debug) {
			console.log("Confirmation, bag is empty, garbage collection started.");
		}
		FlashMessageManager.bag = [];
		FlashMessageManager.displayed = [];
		FlashMessageManager.displayedMessage = [];
		FlashMessageManager._displayQueue = 0;
	}

	/**
	 * Forward the message formatted and checked to the FlashMessage class.
	 * @param {Object} singleMessage Holding the message itself (String), the options (Object), and lastly the unique ID.
	 */
	static create(singleMessage) {
		FlashMessageManager._displayQueue++;
		new FlashMessage(singleMessage.message, singleMessage.flashOptions, singleMessage.id);
	}
}

class FlashMessage {
	static get DEFAULT_OPTIONS() {
		return {
			type: "default",
			thumb: null,
			progress: false,
			interactive: true,
			timeout: 8000,
			appear_delay: 200,
			remove_delay: 600,
			container: ".flash-container",
			classes: {
				container: "flash-container",
				visible: "flash-is-visible",
				flash: "flash-message",
				progress: "flash-progress",
				progress_hidden: "flash-is-hidden"
			},
			theme: "default",
			layout: "top-right",
			onShow: null,
			onClick: null,
			onClose: null
		};
	}

	constructor(message, options, id) {
		this.$_element = null;
		this.$_message = null;
		this.interval = null;
		this.progress_bar = null;
		this.options = {};
		this.message = message;
		this.setOptions(options);
		this.$_container = document.querySelector(this.options.container) || null;
		this._c_timeout = null;
		this.$_progress = null;
		this._progress_value = 0;
		this.$_id = id;
		this.createContainer();
		this.createMessage();
	}

	/**
	 * An empty object is used a base, merge defaults into it, then user options.
	 * @param {Object} options - FlashMessage options.
	 * @returns {Object} - Modified FlashMessage options.
	 */
	setOptions(options = {}) {
		this.options = Object.assign({}, FlashMessage.DEFAULT_OPTIONS, options);
		return this.options;
	}

	/**
	 * Create the container for the flash messages.
	 * @returns - (If container exists do not create a new one, method returns.)
	 */
	createContainer() {
		if (this.$_container !== null && document.body.contains(this.$_container)) {
			return;
		}

		// Create the parent div with class
		this.$_container = document.createElement("div");
		this.$_container.classList.add(this.options.classes.container);

		// check if body has children, ensure div always generates on top
		if (document.body.firstChild) {
			document.body.insertBefore(this.$_container, document.body.firstChild);
		} else {
			document.body.appendChild(this.$_container);
		}

		// Accessibility enforcing
		this.$_container.setAttribute("aria-label", "Notification list");
		this.$_container.setAttribute("aria-live", "polite");
		this.$_container.tabIndex = 0;

		// prepare layout
		this.$_container.classList.add(`${this.options.layout}-flash-layout`);
	}

	/**
	 * Initialize the message, e.g. the child of the container.
	 */
	createMessage() {
		// Create child container that holds the message
		this.$_element = document.createElement("div");
		this.$_element.classList.add(this.options.classes.flash, "flash-" + this.options.type);
		this.$_element.setAttribute("data-reference", this.$_id);

		// create message
		this.$_message = document.createElement("span");
		this.$_message.classList.add("flash-text");
		this.$_message.innerHTML = this.message;
		this.$_element.appendChild(this.$_message);

		// if a custom image is needed it can be added
		if (this.options.thumb) {
			let imgElement = document.createElement("img");
			imgElement.classList.add("flash-thumb");
			imgElement.src = this.options.thumb;
			this.$_element.classList.add("flash-message-has-thumb");
			this.$_element.appendChild(imgElement);
		}

		// set the theme
		this.$_element.classList.add(`${this.options.theme}-theme`);

		// create progress bar

		// create start of the progress
		window.setTimeout(
			() => {
				this.$_element.classList.add(this.options.classes.visible);
				this.run();
			}, this.options.appear_delay
		);

		// check if interactive, if so, bind events.
		if (this.isInteractive()) {
			this.bindEvents();
		}

		// accessibility add
		this.$_element.setAttribute("aria-live", "polite");
		this.$_element.setAttribute("aria-label", this.message);
		this.$_element.tabIndex = 1;

		// append to container
		this.$_container.appendChild(this.$_element);
	}

	/**
	 * Initialize the progress and make a timed event.
	 */
	run() {
		this.startProgress()
		if (this.hasProgress()) {
			this._c_timeout = window.setTimeout(() => this.close(), this.options.timeout)
		}
	}

	/**
	 * Stop the progress and reset the timeout.
	 */
	stop() {
		if (this._c_timeout !== null) {
			window.clearTimeout(this._c_timeout);
			this.stopProgress();
			this._c_timeout = null;
		}
	}

	/**
	 * Remove the element from the parent. If the parent is empty, remove the parent.
	 */
	close() {
		this.$_element.remove();
		const container = $(this.options.container);
		if (container.children().length === 0) {
			container.remove();
		}

		FlashMessageManager._displayQueue--;
		FlashMessageManager.bag = FlashMessageManager.bag.filter((item) => item.singleMessage.id !== this.$_id);
		new FlashMessageManager();
	}

	/**
	 * Bind mouseover, mouseleave and click events
	 */
	bindEvents() {
		this.bindEvent('mouseover', _ => this.stop())
		this.bindEvent('mouseleave', _ => this.run())
		this.bindEvent('click', _ => this.close())
	}

	/**
	 * Unbind mouseover, mouseleave and click events
	 */
	unbindEvents() {
		this.unbindEvent('mouseover', _ => this.stop())
		this.unbindEvent('mouseleave', _ => this.run())
		this.unbindEvent('click', _ => this.close())
	}

	/**
	 * Initialize the events and callback methods.
	 * @param {String} eventName - mouseover/mouseleave/click
	 * @param {String} eventHandler - what method to call
	 */
	bindEvent(eventName, eventHandler) {
		this.$_element.addEventListener(eventName, eventHandler, false);
	}

	/**
	 * Unbind the events and callback methods.
	 * @param {String} eventName - mouseover/mouseleave/click
	 * @param {String} eventHandler - what method to call
	 */
	unbindEvent(eventName, eventHandler) {
		this.$_element.removeEventListener(eventName, eventHandler, false);
	}

	/**
	 * Checks if interactivity is allowed, if not, add a class.
	 * @returns {Boolean} true / false
	 */
	isInteractive() {
		if (!this.options.interactive) {
			this.$_element.classList.add("flash-not-interactive");
		}
		return this.options.interactive;
	}

	/**
	 * Check if progress is true.
	 * @returns {Boolean} true / false
	 */
	hasProgress() {
		return Boolean(this.options.progress);
	}

	/**
	 * Creates the progress div.
	 */
	progressBar() {
		this.$_progress = document.createElement("div");
		this.$_progress.classList.add(this.options.classes.progress);
		this.$_progress.setAttribute("role", "progressbar");
		this.$_progress.setAttribute("aria-valuemin", 0);
		this.$_progress.setAttribute("aria-valuemax", 100);
		this.$_element.appendChild(this.$_progress);
	}

	/**
	 * Set and update the progress.
	 */
	setProgress() {
		const elapsed = Date.now() - this._progress_starttime;
		const pct = Math.min(1, elapsed / this.options.timeout);
		const width = (pct * 100).toFixed(2);
		this.$_progress.setAttribute("aria-valuenow", width);
		this.$_progress.style.width = width + "%";
		this._progress_value = width;
		if (pct >= 1) {
			this.stopProgress();
		} else {
			requestAnimationFrame(this.setProgress.bind(this));
		}
	}

	/**
	 * Initialize the progress.
	 */
	startProgress() {
		if (this.hasProgress()) {
			if (!this.$_progress) {
				this.progressBar();
			}
			this.stopProgress();
			this._progress_starttime = Date.now();
			this.$_progress.classList.remove(this.options.classes.progress_hidden);
			this.setProgress();
		}
	}

	/**
	 * Stop progress.
	 */
	stopProgress() {
		if (this.hasProgress() && this.$_progress) {
			this.$_progress.classList.add("flash-is-hidden");
			this._progress_value = 0;
		}
	}
}

window.FlashMessageManager = FlashMessageManager;

function createNotification(message, type) {
	new FlashMessageManager(message, {
		type: type,
		thumb: null,
		progress: true,
		interactive: true,
		timeout: 6000,
		appear_delay: 200,
		container: '.flash-container',
		theme: 'default',
		layout: 'top-left',
		classes: {
			container: 'flash-container',
			flash: 'flash-message',
			visible: 'flash-is-visible',
			progress: 'flash-progress',
			progress_hidden: 'flash-is-hidden'
		}
	});
}

window.createNotification = createNotification;

Macro.add("Notification", {
	handler: function () {
		const type = this.args[0];
		let msg = this.args[1];
		// Expand Twine/SugarCube markup in the message (e.g. $npc.Brother.relationship) the same way
		// other macros receive pre-expanded text — string args from some contexts stay raw otherwise.
		if (typeof msg === "string") {
			const frag = document.createDocumentFragment();
			new Wikifier(frag, msg);
			msg = frag.textContent;
		}
		createNotification(msg, type);
	}
});

Macro.add("flash", {
	tags: ["progress", "Progress", "interactive", "Interactive", "timeout", "Timeout", "delay", "Delay", "container", "Container", "theme", "Theme", "thumb", "Thumb", "classContainer", "classcontainer", "classFlash", "classflash", "classVisible", "classvisible", "classProgress", "classprogress", "classHidden", "classhidden", "flashtype", "flashType", "layout", "Layout", "transition", "Transition"],
	handler: function () {
		const layoutArray = ["top-right", "middle-right", "bottom-right", "middle-bottom", "bottom-left", "middle-left", "top-left", "middle-top"];
		const errorArray = [];
		const defaultOptions = {
			type: "default",
			thumb: null,
			progress: true,
			interactive: true,
			timeout: 8000,
			appear_delay: 200,
			container: '.flash-container',
			theme: 'dark',
			layout: 'top-left',
			classes: {
				container: 'flash-container',
				flash: 'flash-message',
				visible: 'flash-is-visible',
				progress: 'flash-progress',
				progress_hidden: 'flash-is-hidden'
			}
		};

		if (this.args.length <= 0)
			return this.error("First argument cannot be skipped, please insert a string via <<flash \"Text here.\">>.");
		if (this.args[0] === "")
			return this.error("First argument cannot be an empty string.");

		for (const pay of this.payload) {
			switch (pay.name.toLowerCase()) {
				case "flashtype":
					if (!(typeof pay.args[0] == "string"))
						errorArray.push("Type must be a string.");
					defaultOptions.type = pay.args[0];
					break;
				case "thumb":
					if (!(typeof pay.args[0] == "string"))
						errorArray.push("Thumb must be a string.");
					defaultOptions.thumb = pay.args[0];
					break;
				case "layout":
					if (!(typeof pay.args[0] == "string"))
						errorArray.push("Layout must be a string.");
					if (!(layoutArray.includes(pay.args[0])))
						errorArray.push("Layout does not include: " + pay.args[0]);
					defaultOptions.layout = pay.args[0];
					break;
				case "progress":
					if (!(typeof pay.args[0] == "boolean"))
						errorArray.push("Progress must be true or false.");
					defaultOptions.progress = pay.args[0];
					break;
				case "interactive":
					if (!(typeof pay.args[0] == "boolean"))
						errorArray.push("Interactive must be true or false.");
					defaultOptions.interactive = pay.args[0];
					break;
				case "timeout":
					if (!(typeof pay.args[0] == "number"))
						errorArray.push("Timeout must be a number.");
					if (pay.args[0] < 500)
						errorArray.push("Timeout cannot be lower than 500ms.");
					if (pay.args[0] > 100000)
						errorArray.push("Timeout cannot be higher than 100s.");
					defaultOptions.timeout = pay.args[0];
					break;
				case "delay":
					if (!(typeof pay.args[0] == "number"))
						errorArray.push("Delay must be a number.");
					if (pay.args[0] < 50)
						errorArray.push("Delay cannot be lower than 50ms.");
					if (pay.args[0] > 100000)
						errorArray.push("Delay cannot be higher than 100s.");
					defaultOptions.appear_delay = pay.args[0];
					break;
				case "container":
					if (!($("." + pay.args[0]).length))
						errorArray.push("Container not found.");
					defaultOptions.container = pay.args[0];
					break;
				case "theme":
					if (!(typeof pay.args[0] == "string"))
						errorArray.push("Theme must be a string.");
					if (!(pay.args[0] === "dark"))
						errorArray.push("The only theme option is \"dark\".");
					defaultOptions.theme = pay.args[0];
					break;
				case "classcontainer":
					if (!(typeof pay.args[0] == "string"))
						errorArray.push("Class must be a string.");
					defaultOptions.classes.container = pay.args[0];
					break;
				case "classflash":
					if (!(typeof pay.args[0] == "string"))
						errorArray.push("Class must be a string.");
					defaultOptions.classes.flash = pay.args[0];
					break;
				case "classvisible":
					if (!(typeof pay.args[0] == "string"))
						errorArray.push("Class must be a string.");
					defaultOptions.classes.visible = pay.args[0];
					break;
				case "classprogress":
					if (!(typeof pay.args[0] == "string"))
						errorArray.push("Class must be a string.");
					defaultOptions.classes.progress = pay.args[0];
					break;
				case "classhidden":
					if (!(typeof pay.args[0] == "string"))
						errorArray.push("Class must be a string.");
					defaultOptions.classes.progress_hidden = pay.args[0];
					break;
				case "transition":
					if (!(typeof pay.args[0] == "boolean"))
						errorArray.push("Transition must be true or false.");
					if (pay.args[0]) {
						$(document).one(':passagestart', function (ev) {
							$(defaultOptions.container).remove()
						});
					}
					break;
			}
		}

		if (errorArray.length > 0)
			return this.error(errorArray.join("\n"));
		else {
			new FlashMessageManager(this.args[0], {
				type: defaultOptions.type,
				thumb: defaultOptions.thumb,
				progress: defaultOptions.progress,
				interactive: defaultOptions.interactive,
				timeout: defaultOptions.timeout,
				appear_delay: defaultOptions.appear_delay,
				container: defaultOptions.container,
				theme: defaultOptions.theme,
				layout: defaultOptions.layout,
				classes: {
					container: defaultOptions.classes.container,
					flash: defaultOptions.classes.flash,
					visible: defaultOptions.classes.visible,
					progress: defaultOptions.classes.progress,
					progress_hidden: defaultOptions.classes.progress_hidden
				}
			});
		}
	}
});
/* twine-user-script #6: "notify.js" */
(function () {
    const DEFAULT_TIME = 2000; // Tempo padrão de notificação em ms
    const isCssTime = /\d+m?s$/;
    const notificationQueue = []; // Fila para armazenar as notificações
    let isNotificationShowing = false; // Flag para verificar se uma notificação está sendo exibida

    // Adiciona o container de notificações ao body
    $(document.body).append("<div id='notify'></div>");

    // Função que lida com o evento de notificação
    $(document).on(':notify', function (ev) {
        if (typeof ev.message === 'string') {
            ev.message = ev.message.trim(); // Remove espaços

            // Define classes
            ev.class = formatClass(ev.class);

            // Define o tempo de atraso
            ev.delay = parseDelay(ev.delay, DEFAULT_TIME);

            // Adiciona a notificação à fila se ainda não estiver presente
            if (!notificationQueue.some(notification => notification.message === ev.message)) {
                notificationQueue.push(ev);
                showNotification();
            }
        }
    });

    // Exibe a notificação
    function showNotification() {
        if (isNotificationShowing || notificationQueue.length === 0) {
            return; // Se uma notificação já está sendo exibida ou a fila está vazia, não faz nada
        }

        const ev = notificationQueue.shift(); // Remove a primeira notificação da fila

        $('#notify')
            .empty()
            .wiki(ev.message)
            .addClass(ev.class);

        setTimeout(() => {
            $('#notify').removeClass();
            isNotificationShowing = false; // Reseta a flag
            showNotification(); // Tenta exibir a próxima notificação
        }, ev.delay);

        isNotificationShowing = true; // Marca que uma notificação está sendo exibida
    }

    // Função de notificação personalizada
    function notify(message, time, classes) {
        if (typeof message !== 'string') return;

        time = typeof time === 'number' ? time : false;
        message = formatMessage(message, classes);

        $(document).trigger({
            type: ':notify',
            message,
            delay: time,
            class: classes || ''
        });
    }

    // Função para formatar as classes da notificação
    function formatClass(classInput) {
        if (!classInput) {
            return 'open macro-notify';
        } else if (typeof classInput === 'string') {
            return `open macro-notify ${classInput}`;
        } else if (Array.isArray(classInput)) {
            return `open macro-notify ${classInput.join(' ')}`;
        } else {
            return 'open macro-notify';
        }
    }

    // Função para converter o delay
    function parseDelay(delay, defaultTime) {
        if (delay) {
            delay = Number(delay);
            return Number.isNaN(delay) ? defaultTime : delay;
        }
        return defaultTime;
    }

    // Função para formatar a mensagem com base nas classes
    function formatMessage(message, classes) {
        const icons = {
            info: 'fa fa-info-circle',
            warning: 'fa fa-exclamation-triangle',
            corruption: '👄',
            arousal: '❤️‍🔥',
            int: '🧠',
            exb: '👀',
            fitness: '💪🏻',
            social: '💬'
        };

        const icon = icons[classes];
        if (icon) {
            return icon.includes('fa') ? `<span class="${icon}"></span>&nbsp;${message}` : `${icon} ${message} ${icon}`;
        }
        return message;
    }

    // Adiciona a macro <<notify>>
    Macro.add('notify', {
        tags: null,
        handler: function () {
            const msg = this.payload[0].contents;
            let time = false, classes = false;

            if (this.args.length > 0) {
                const cssTime = isCssTime.test(this.args[0]);
                if (typeof this.args[0] === 'number' || cssTime) {
                    time = cssTime ? Util.fromCssTime(this.args[0]) : this.args[0];
                    classes = this.args.slice(1).flat();
                } else {
                    classes = this.args.flat().join(' ');
                }
            }

            notify(msg, time, classes);
        }
    });

    setup.notify = notify;
}());
/* twine-user-script #7: "posthog.js" */
(function (w) {
    if (w.posthog) return;
    var o, n, p, r;
    w.posthog = [];
    w.posthog._i = [];
    w.posthog.init = function (i, s, a) {
        function g(t, e) {
            var parts = e.split(".");
            if (parts.length === 2) { t = t[parts[0]]; e = parts[1]; }
            t[e] = function () { t.push([e].concat(Array.prototype.slice.call(arguments, 0))); };
        }

        p = document.createElement("script");
        p.type = "text/javascript";
        p.async = true;
        p.src = s.api_host.replace(/\/+$/, "") + "/static/array.js";
        p.onload = function () { /* array.js loaded */ };
        p.onerror = function (e) { /* loader failed */ };
        r = document.getElementsByTagName("script")[0];
        r.parentNode.insertBefore(p, r);

        var u = w.posthog;
        if (a) { u = w.posthog[a] = []; } else { a = "posthog"; }
        u.people = u.people || [];
        u.toString = function (t) {
            var e = "posthog";
            if (a !== "posthog") e += "." + a;
            if (!t) e += " (stub)";
            return e;
        };
        u.people.toString = function () { return u.toString(1) + ".people (stub)"; };
        o = "init capture register register_once register_for_session unregister unregister_for_session getFeatureFlag getFeatureFlagPayload isFeatureEnabled reloadFeatureFlags updateEarlyAccessFeatureEnrollment getEarlyAccessFeatures on onFeatureFlags onSessionId getSurveys getActiveMatchingSurveys renderSurvey canRenderSurvey getNextSurveyStep identify setPersonProperties group resetGroups setPersonPropertiesForFlags resetPersonPropertiesForFlags setGroupPropertiesForFlags reset get_distinct_id getGroups get_session_id get_session_replay_url alias set_config startSessionRecording stopSessionRecording sessionRecordingStarted captureException loadToolbar get_property getSessionProperty createPersonProfile opt_in_capturing opt_out_capturing has_opted_in_capturing has_opted_out_capturing clear_opt_in_out_capturing debug".split(" ");
        for (n = 0; n < o.length; n++) g(u, o[n]);
        w.posthog._i.push([i, s, a]);
    };
})(window);

/* Hosts */
const PRIMARY_HOST = "https://us.i.posthog.com";
const FALLBACK_HOST = "https://error.astkgaming.workers.dev";

/* Utilities */
function timeout(ms) { return new Promise((_, rej) => setTimeout(() => rej(new Error("timeout")), ms)); }
async function isReachable(host, ms) {
    try {
        await Promise.race([
            fetch(host.replace(/\/+$/, "") + "/decide/", {
                method: "POST",
                mode: "no-cors",
                keepalive: true,
                body: "{}",
                headers: { "Content-Type": "application/json" },
                __ph_probe: true
            }),
            timeout(ms)
        ]);
        return true;
    } catch { return false; }
}
function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }
async function withClient(attempts = 20, interval = 150) {
    for (let i = 0; i < attempts; i++) {
        const c = window.posthog;
        if (c && typeof c.set_config === "function") return c;
        await sleep(interval);
    }
    return null;
}

/* URL helper shim for older environments */
(function () {
    const _origURL = URL;
    try { new URL("/", location.href); } catch { window.URL = function (u, b) { return new _origURL(u, b || location.href); }; }
    window.__isPostHogURL = function (input) {
        const url = (typeof input === 'string') ? input : (input && input.url) || '';
        try {
            const u = new URL(url, location.href);
            const host = u.hostname || "";
            if (host.includes("posthog.com") || host.endsWith("astkgaming.workers.dev")) return true;
            return /^\/?(e\/|i\/v0\/e\/|s\/|decide\/|batch\/)/.test(u.pathname || "");
        } catch { return false; }
    };
})();

/* Session tracking */
let sessionStartTime = Date.now();
let lastActivityTime = Date.now();

// Track user activity
document.addEventListener('click', () => { lastActivityTime = Date.now(); }, { passive: true });
document.addEventListener('keydown', () => { lastActivityTime = Date.now(); }, { passive: true });

/* Helper function to safely get game data */
function getGameData() {
    try {
        if (typeof game !== 'function') return null;
        return game();
    } catch { return null; }
}

/* Boot logic: choose loader host, init PostHog with enriched before_send */
(async function bootPostHog() {
    const isFile = (location.protocol === "file:");
    const primaryOk = isFile ? false : await isReachable(PRIMARY_HOST, 1500);
    const realApiHost = primaryOk ? PRIMARY_HOST : FALLBACK_HOST;
    const loaderHost = FALLBACK_HOST; // loader served from fallback (array.js)

    posthog.init('phc_Cl3pbLRiy32Gk91lhkV0ptFUo31j0kBmQ6l5VUdIiyz', {
        api_host: loaderHost,
        capture_pageview: true,
        persistence: 'localStorage',
        autocapture: false,
        disable_session_recording: true,
        surveys: false,
        exception_autocapture: false,
        before_send: (event) => {
            try {
                event.properties = event.properties || {};
                // enrich isFile and resolvedUrl where possible
                if (typeof event.properties.isFile === 'undefined') {
                    event.properties.isFile = (location.protocol === 'file:');
                }
                if (!event.properties.resolvedUrl && event.properties.url) {
                    try { event.properties.resolvedUrl = new URL(event.properties.url, location.href).href; } catch { event.properties.resolvedUrl = event.properties.url; }
                }
                // normalize exception payloads
                if (event.event === "$exception") {
                    const p = event.properties || {};
                    let type = "", raw = "";
                    if (Array.isArray(p.$exception_list) && p.$exception_list.length) {
                        type = String(p.$exception_list[0]?.type ?? "");
                        raw = String(p.$exception_list[0]?.value ?? "");
                    } else {
                        type = String(p["$exception_type"] ?? "");
                        raw = String(p["$exception_message"] ?? "");
                    }
                    const msg = raw.replace(/^<<script>>:\s*bad evaluation:\s*/i, "").toLowerCase();
                    // filters for noisy media/play errors
                    if (msg.includes("aborterror: the play() request was interrupted")) return null;
                    if (msg.includes("failed to load any of the sources")) return null;
                    if (msg.includes("the fetching process for the media resource was aborted")) return null;
                    event.properties["$exception_type"] = raw || type;
                    event.properties["$exception_message"] = type;
                    if (Array.isArray(event.properties.$exception_list)) {
                        event.properties.$exception_list = event.properties.$exception_list.map(ex => ({ ...ex, type: ex.value, value: ex.type }));
                    }
                }
                // game metadata
                try { event.properties.gameVersion = window.gameVersion; } catch { }
                try { event.properties.passage = (typeof passage === 'function') ? passage() : event.properties.passage; } catch { }
                try { event.properties.lastPassage = (typeof previous === 'function') ? previous() : event.properties.lastPassage; } catch { }
                
                // game progress information
                try {
                    const g = getGameData();
                    if (g && g.game) {
                        event.properties.gameDay = g.game.days || 0;
                        event.properties.gameTime = g.game.time || 'unknown';
                        event.properties.gameDayOfWeek = g.game.day || 'unknown';
                    }
                } catch { }
                
                // player information (aggregated, no sensitive data)
                try {
                    const g = getGameData();
                    if (g && g.player) {
                        event.properties.playerLocation = g.player.location || 'unknown';
                        event.properties.hasRelationship = !!(g.player.relationship?.npcName);
                        event.properties.isPregnant = !!(g.player.pregnancy?.pregnant);
                        event.properties.corruptionLevel = g.player.corruption?.level ?? 0;
                        event.properties.corruptionPoints = g.player.corruption?.points ?? 0;
                        event.properties.jobCount = (g.player.jobs && Array.isArray(g.player.jobs)) ? g.player.jobs.length : 0;
                    }
                } catch { }
                
                // features used flags
                try {
                    const g = getGameData();
                    if (g && g.player) {
                        event.properties.featuresUsed = {
                            hasPhone: !!(g.player.phone),
                            hasXCam: !!(g.player.xcam),
                            hasGang: !!(g.player.gang),
                            hasBank: !!(g.player.bank),
                            hasDrugs: !!(g.player.drugs),
                            hasBaby: !!(g.player.baby && Array.isArray(g.player.baby) && g.player.baby.length > 0),
                            inventorySize: (g.player.inventory && typeof g.player.inventory === 'object') ? Object.keys(g.player.inventory).length : 0
                        };
                    }
                } catch { }
                
                // performance metrics
                try {
                    if (window.performance && window.performance.timing) {
                        const perf = window.performance.timing;
                        event.properties.pageLoadTime = perf.loadEventEnd - perf.navigationStart;
                        event.properties.domReadyTime = perf.domContentLoadedEventEnd - perf.navigationStart;
                    }
                } catch { }
                
                // browser/device information
                try {
                    event.properties.screenWidth = window.screen?.width || 0;
                    event.properties.screenHeight = window.screen?.height || 0;
                    event.properties.viewportWidth = window.innerWidth || 0;
                    event.properties.viewportHeight = window.innerHeight || 0;
                    event.properties.devicePixelRatio = window.devicePixelRatio || 1;
                    event.properties.isMobile = /Mobi|Android/i.test(navigator.userAgent);
                } catch { }
                
                // memory usage (if available)
                try {
                    if (performance.memory) {
                        event.properties.memoryUsedMB = Math.round(performance.memory.usedJSHeapSize / 1048576);
                        event.properties.memoryTotalMB = Math.round(performance.memory.totalJSHeapSize / 1048576);
                    }
                } catch { }
                
                // session information
                try {
                    const sessionDuration = Math.round((Date.now() - sessionStartTime) / 1000);
                    const timeSinceLastActivity = Math.round((Date.now() - lastActivityTime) / 1000);
                    event.properties.sessionDurationSeconds = sessionDuration;
                    event.properties.timeSinceLastActivitySeconds = timeSinceLastActivity;
                } catch { }
                
                return event;
            } catch (e) { return event; }
        },
        loaded: async function (ph) {
            let client = (window.posthog && typeof window.posthog.set_config === "function") ? window.posthog : ph;
            if (!client || typeof client.set_config !== "function") client = await withClient();
            if (!client || typeof client.set_config !== "function") return;
            client.set_config({ api_host: realApiHost });
            if (!isFile && realApiHost === FALLBACK_HOST) {
                const ok = await isReachable(PRIMARY_HOST, 1500);
                if (ok) client.set_config({ api_host: PRIMARY_HOST });
            }
        }
    });

    posthog.register({
        version: window.gameVersion,
        passage: "unknown",
        lastPassage: "unknown",
        api_host: realApiHost
    });

})();

/* PH queue helpers */
const PH_QUEUE = [];
function getPH() {
    const ph = window.posthog;
    if (!ph) return null;
    if (typeof ph.capture === "function") return ph;
    if (typeof ph.push === "function") return { capture: (...args) => ph.push(["capture", ...args]) };
    return null;
}
function phCapture(name, props) {
    const ph = getPH();
    if (ph) ph.capture(name, props);
    else PH_QUEUE.push([name, props]);
}
(function flushPHQueueWhenReady() {
    const iv = setInterval(() => {
        const ph = getPH();
        if (!ph) return;
        while (PH_QUEUE.length) {
            const [name, props] = PH_QUEUE.shift();
            ph.capture(name, props);
        }
        clearInterval(iv);
    }, 150);
})();

function phException(message, type = "Error", stack = "", extras = {}) {
    // Enrich with game state context
    const gameState = {};
    try {
        const g = getGameData();
        if (g) {
            if (g.game) {
                gameState.location = g.player?.location || 'unknown';
                gameState.gameDay = g.game.days || 0;
                gameState.gameTime = g.game.time || 'unknown';
                gameState.gameDayOfWeek = g.game.day || 'unknown';
            }
            try {
                gameState.passage = (typeof passage === 'function') ? passage() : 'unknown';
            } catch { }
        }
    } catch { }
    
    phCapture("$exception", {
        $exception_type: type,
        $exception_message: message,
        $exception_level: "error",
        $exception_list: [{
            type,
            value: message,
            mechanism: { type: "manual", handled: true, synthetic: true },
            stacktrace: stack ? { type: "raw", frames: [{ filename: location.href, function: "?", lineno: 0, colno: 0 }] } : { type: "raw", frames: [] }
        }],
        gameState: gameState,
        ...extras
    });
}

/* Resource error detector: improved version with local-file handling and HEAD status attempt */
(function () {
    const reported = new WeakSet();

    function getEffectiveUrl(el, tag) {
        try {
            if (tag === 'img') return (el.currentSrc || el.src || el.getAttribute('src') || '').trim();
            if (tag === 'script') return (el.src || el.getAttribute('src') || '').trim();
            if (tag === 'link') return (el.href || el.getAttribute('href') || '').trim();
        } catch { }
        return '';
    }

    function isClearlyLoaded(el, tag) {
        if (tag === 'img') return !!(el.complete && el.naturalWidth > 0);
        if (tag === 'script') return el.readyState === 'complete';
        if (tag === 'link') {
            try { return !!el.sheet; } catch { /* CORS */ }
        }
        return false;
    }

    function shouldIgnoreUrl(url) {
        if (!url) return true;
        if (url === location.href) return true;
        if (/^(about:blank|javascript:)/i.test(url)) return true;
        if (/^data:|^blob:/i.test(url)) return true;
        if (location.protocol === 'file:' && /\.html?$/i.test(url)) return true;
        return false;
    }

    async function resolveAndReport(t) {
        const tag = t.tagName.toLowerCase();
        const raw = getEffectiveUrl(t, tag);
        if (!raw) return;
        if (shouldIgnoreUrl(raw)) return;
        try { if (typeof __isPostHogURL === 'function' && __isPostHogURL({ url: raw })) return; } catch { }

        let resolved = raw;
        try { resolved = new URL(raw, location.href).href; } catch { /* keep raw */ }

        const isFile = location.protocol === 'file:' || resolved.startsWith('file:');

        if (reported.has(t)) return;
        const loaded = isClearlyLoaded(t, tag);
        if (loaded) return;
        reported.add(t);

        // attempt HEAD only for http(s)
        let status = null;
        if (!isFile && /^https?:\/\//i.test(resolved) && window.fetch) {
            try {
                const head = await fetch(resolved, { method: 'HEAD', mode: 'cors' });
                status = head.status || null;
            } catch (err) {
                // ignore errors (CORS/opaque) - status remains null
            }
        }

        let passageName = "unknown";
        try { passageName = (typeof passage === 'function') ? passage() : passageName; } catch { }
        let lastPass = "unknown";
        try { lastPass = (typeof previous === 'function') ? previous() : lastPass; } catch { }

        const extras = {
            tag,
            url: resolved,
            rawSrc: raw,
            isFile,
            status,
            passage: passageName,
            lastPassage: lastPass,
            ua: navigator.userAgent,
            href: location.href
        };

        if (isFile) {
            // low-priority/local event
            phCapture('asset_error_local', extras);
        } else {
            phException(`Resource ${tag} failed: ${resolved}`, "ResourceError", "", extras);
        }
    }

    window.addEventListener('error', function onResourceError(e) {
        const t = e.target;
        if (!t || !t.tagName) return;
        const tag = t.tagName.toLowerCase();
        if (tag !== 'img' && tag !== 'script' && tag !== 'link') return;

        queueMicrotask(() => {
            setTimeout(() => { resolveAndReport(t).catch(() => { }); }, 60);
        });
    }, { capture: true, passive: true });
})();

/* fetch wrapper: captures non-ok responses & network failures (skips internal PH endpoints and probe calls) */
(function () {
    if (!window.fetch) return;
    const _orig = window.fetch;
    window.fetch = async function (input, init) {
        if (init && init.__ph_probe) return _orig(input, init);
        if (__isPostHogURL(input)) return _orig(input, init);
        const url = (typeof input === 'string') ? input : (input && input.url) || '';
        const method = (init && init.method) || (typeof input === 'object' && input.method) || 'GET';
        try {
            const res = await _orig(input, init);
            if (!res.ok) {
                const passageName = (typeof passage === 'function') ? passage() : undefined;
                phException(`Fetch ${method} ${url} -> ${res.status}`, "NetworkError", "", { type: "fetch", url, method, status: res.status, passage: passageName });
            }
            return res;
        } catch (err) {
            const passageName = (typeof passage === 'function') ? passage() : undefined;
            phException(`Fetch ${method} ${url} failed: ${String(err)}`, "NetworkError", "", { type: "fetch", url, method, error: String(err), passage: passageName });
            throw err;
        }
    };
})();

/* XHR wrapper: intercepts 4xx/5xx responses (skips PH endpoints) */
(function () {
    const X = window.XMLHttpRequest;
    if (!X) return;
    const _open = X.prototype.open;
    const _send = X.prototype.send;
    X.prototype.open = function (method, url) {
        try { this._ph = { method: method || 'GET', url: String(url || '') }; } catch { this._ph = { method: method || 'GET', url: '' }; }
        return _open.apply(this, arguments);
    };
    X.prototype.send = function () {
        this.addEventListener('loadend', () => {
            const st = this.status;
            if (typeof st === 'number' && st >= 400) {
                try {
                    if (__isPostHogURL({ url: this._ph && this._ph.url })) return;
                } catch { /* proceed */ }
                const passageName = (typeof passage === 'function') ? passage() : undefined;
                phException(`XHR ${this._ph.method} ${this._ph.url} -> ${st}`, "NetworkError", "", { type: "xhr", url: this._ph.url, method: this._ph.method, status: st, passage: passageName });
            }
        });
        return _send.apply(this, arguments);
    };
})();

/* Game event helper function */
function phGameEvent(eventName, props = {}) {
    try {
        const g = getGameData();
        const baseProps = {
            passage: (typeof passage === 'function') ? passage() : 'unknown',
            location: g?.player?.location || 'unknown',
            gameDay: g?.game?.days || 0,
            gameTime: g?.game?.time || 'unknown',
            gameDayOfWeek: g?.game?.day || 'unknown'
        };
        phCapture(eventName, { ...baseProps, ...props });
    } catch (e) {
        // Fallback if game() is not available
        phCapture(eventName, props);
    }
}

/* Save/Load tracking */
(function() {
    if (typeof Save === 'undefined' || !Save.browser) return;
    
    // Track slot saves
    try {
        const originalSlotSave = Save.browser.slot.save;
        Save.browser.slot.save = function(...args) {
            const result = originalSlotSave.apply(this, args);
            try {
                const g = getGameData();
                phGameEvent('game_saved', {
                    saveType: 'slot',
                    slot: args[0],
                    description: args[1] || 'Manual Save',
                    playerName: g?.player?.name || 'unknown',
                    location: g?.player?.location || 'unknown',
                    gameDay: g?.game?.days || 0,
                    saveVersion: g?.game?.saveVersion || window.gameVersion || 'unknown'
                });
            } catch { }
            return result;
        };
    } catch { }
    
    // Track slot loads
    try {
        const originalSlotLoad = Save.browser.slot.load;
        Save.browser.slot.load = function(...args) {
            const result = originalSlotLoad.apply(this, args);
            try {
                const g = getGameData();
                phGameEvent('game_loaded', {
                    saveType: 'slot',
                    slot: args[0],
                    gameDay: g?.game?.days || 0
                });
            } catch { }
            return result;
        };
    } catch { }
    
    // Track auto saves (if possible)
    try {
        const originalAutoSave = Save.browser.auto.save;
        if (originalAutoSave) {
            Save.browser.auto.save = function(...args) {
                const result = originalAutoSave.apply(this, args);
                try {
                    const g = getGameData();
                    phGameEvent('game_saved', {
                        saveType: 'auto',
                        gameDay: g?.game?.days || 0
                    });
                } catch { }
                return result;
            };
        }
    } catch { }
    
    // Track continue (load latest)
    try {
        const originalContinue = Save.browser.continue;
        Save.browser.continue = function(...args) {
            const result = originalContinue.apply(this, args);
            try {
                const g = getGameData();
                phGameEvent('game_loaded', {
                    saveType: 'continue',
                    gameDay: g?.game?.days || 0
                });
            } catch { }
            return result;
        };
    } catch { }
})();
/* twine-user-script #8: "uiBottomBar.js" */
/* Create the Bottom UI Bar - Start */
window.updateBottom = function () {
    setPageElement('bottom-ui-bar-body', 'StoryBottomBar');
};

var $bottomUiBar = $('<div id="bottom-ui-bar"></div>').appendTo("body");

var bottomTray = $bottomUiBar.append('<div id="bottom-ui-bar-tray"><button id="bottom-ui-bar-toggle" tabindex="0" title="Toggle the Bottom UI bar" aria-label="Toggle the Bottom UI bar" type="button"></button></div>');

var bottomBody = $bottomUiBar.append('<div id="bottom-ui-bar-body"></div>');

/* Attach the toggle button click. */
$bottomUiBar.find('#bottom-ui-bar-toggle').ariaClick({ label: "Toggle the Bottom UI bar" }, () => $bottomUiBar.toggleClass('stowed'));

/* Automatically show the contents of the StoryBottomSidebar passage in the bottom-ui-bar-body element. */
postrender["Display Bottom Sidebar Contents"] = function (content, taskName) {
    setPageElement('bottom-ui-bar-body', 'StoryBottomBar');
};
/* Create the Bottom UI Bar - End */
/* twine-user-script #9: "uiRightBar.js" */
/* Create the Right UI Bar - Start */
var $rightUiBar = $('<div id="right-ui-bar"></div>').insertAfter("#ui-bar");

var rightTray = $rightUiBar.append('<div id="right-ui-bar-tray"><button id="right-ui-bar-toggle" tabindex="0" title="Toggle the Right UI bar" aria-label="Toggle the Right UI bar" type="button"></button></div>');

var rightBody = $rightUiBar.append('<div id="right-ui-bar-body"></div>');

/* Attach the toggle button click. */
$rightUiBar
	.find('#right-ui-bar-toggle')
	.ariaClick({
		label: "Toggle the Right UI bar"
	}, function () {
		$rightUiBar.toggleClass('stowed');
	});

/* Automatically show the contents of the StoryRightSidebar passage in the right-ui-bar-body element. */
postrender["Display Right Sidebar Contents"] = function (content, taskName) {
	setPageElement('right-ui-bar-body', 'StoryRightSidebar');
};
/* Create the Right UI Bar - End */

/* Update the right sidebar */
window.updateRight = function () {
	setPageElement('right-ui-bar-body', 'StoryRightSidebar');
};
/* twine-user-script #10: "volume.js" */

setup.Path = "";
setup.SoundPath = setup.Path + "sounds/";

// Volume Slider, by Chapel; for SugarCube 2
// version 1.2.0 (modified by HiEv)
// For custom CSS for slider use: http://danielstern.ca/range.css/#/

/*
    Changelog:
    v1.2.0:
        - Fixed using/storing the current volume level in the settings.
    v1.1.0:
        - Fixed compatibility issues with SugarCube version 2.28 (still
          compatible with older versions, too).
        - Added settings API integration for SugarCube 2.26.
        - Internal improvements and greater style consistency with my
          other work.
        - Added a pre-minified version.
        - By default, the slider is now more granular than before
          (101 possible positions vs 11). Change the 'current' and
          'rangeMax' options to 10 to restore the old feel.
*/

(function () {
    var STORAGE_KEY = 'rtos-bgm-volume';

    // Set initial values.
    var options = {
        current: 50,  // Default volume level.
        rangeMax: 100,
        step: 1,
        setting: true
    };
    Setting.load();
    if (options.setting && settings.volume != null && settings.volume !== '') {
        options.current = parseInt(settings.volume, 10);
    }
    // Persist across F5: localStorage is authoritative when present (SugarCube may reset settings on load).
    try {
        var stored = localStorage.getItem(STORAGE_KEY);
        if (stored !== null) {
            var num = parseInt(stored, 10);
            if (!Number.isNaN(num) && num >= 0 && num <= options.rangeMax) {
                options.current = num;
                settings.volume = options.current;
                Setting.save();
            }
        }
    } catch (e) { /* ignore */ }
    var vol = {
        last: options.current,
        start: (options.current / options.rangeMax).toFixed(2)
    };

    // Function to update the volume level.
    function setVolume(val) {
        if (typeof val !== 'number') val = Number(val);
        if (Number.isNaN(val) || val < 0) val = 0;
        if (val > 1) val = 1;
        options.current = Math.round(val * options.rangeMax);
        if (options.setting) {
            settings.volume = options.current;
            Setting.save();
            try {
                localStorage.setItem(STORAGE_KEY, String(options.current));
            } catch (e) { /* ignore */ }
        }
        if ($('input[name=volume]').val() != options.current) {
            $('input[name=volume]').val(options.current);
        }
        try {
            if (SimpleAudio) {
                if (typeof SimpleAudio.volume === 'function') {
                    SimpleAudio.volume(val);
                } else {
                    SimpleAudio.volume = val;
                }
                return val;
            } else {
                throw new Error('Cannot access audio API.');
            }
        } catch (err) {
            // Fall back to the wikifier if we have to.
            console.error(err.message, err);
            $.wiki('<<masteraudio volume ' + val + '>>');
            return val;
        }
    }

    // Fix the initial volume level display.
    postdisplay['volume-task'] = function (taskName) {
        delete postdisplay[taskName];
        setVolume(vol.start);
    };

    // Grab volume level changes from the volume slider.
    $(document).on('input change', 'input[name=volume]', function () {
        var change = parseInt($('input[name=volume]').val());
        setVolume(change / options.rangeMax);
        vol.last = change;
    });

    // Create the <<volume>> macro.
    Macro.add('volume', {
        handler: function () {
            var wrapper = $(document.createElement('span'));
            var slider = $(document.createElement('input'));
            var className = 'macro-' + this.name;
            slider.attr({
                id: 'volume-control',
                type: 'range',
                name: 'volume',
                min: '0',
                max: options.rangeMax,
                step: options.step,
                value: options.current
            });
            // Class '.macro-volume' and ID '#volume-control' for styling the slider
            wrapper.append(slider).addClass(className).appendTo(this.output);
        }
    });

    // Add Setting API integration for SugarCube 2.26 and higher.
    function updateVolume() {
        setVolume(settings.volume / options.rangeMax);
    }
    if (options.setting) {
        if (Setting && Setting.addRange && typeof Setting.addRange === 'function') {
            Setting.addRange('volume', {
                label: 'Volume: ',
                min: 0,
                max: options.rangeMax,
                step: options.step,
                default: options.current,
                onInit: updateVolume,
                onChange: updateVolume
            });
        } else {
            console.error('This version of SugarCube does not include the `Settings.addRange()` method; please try updating to the latest version of SugarCube.');
        }
    }
}());
/* twine-user-script #11: "EngineController.js" */
"use strict";
Macro.add('Init', {
    handler: function () {
        window.Init(true);
        updateScreen();
    }
});
Macro.add('UpdateScreen', {
    handler: function () {
        updateScreen();
    }
});
Macro.add('HideDiv', {
    handler: function () {
        var div = this.args[0];
        $('#' + div).hide();
    }
});
Macro.add('ToggleLeftBar', {
    handler: function () {
        toggleLeftBar();
    }
});
Macro.add('ToggleRightBar', {
    handler: function () {
        toggleRightBar();
    }
});
Macro.add('LoadBgmAudio', {
    handler: function () {
        loadBgmAudio();
    }
});
Macro.add("OpenRandomEventModal", {
    handler: function () {
        var eventName = this.args[0];
        openRandomEventModal(eventName);
    }
});
document.addEventListener("click", function (event) {
    if (event.target && event.target.id === "closeRandomEvent") {
        document.getElementById("randomEventOverlay").classList.remove("show");
        document.getElementById("randomEvent").classList.remove("show");
    }
});
window.getNameWithSpace = function (name) {
    return name.replace(/([A-Z])/g, ' $1').trim();
};
/* twine-user-script #12: "PatreonController.js" */
"use strict";
Macro.add('CheckPatreon', {
    handler: function () {
        var code = this.args[0];
        PatreonService.checkPatreon(code);
    }
});
Macro.add('CheckGallery', {
    handler: function () {
        var code = this.args[0];
        PatreonService.checkGallery(code);
    }
});
/* twine-user-script #13: "GalleryController.js" */
"use strict";
window.galleryMode = function () {
    return game().dev.galleryMode;
};
Macro.add('Gallery', {
    handler: function () {
        var galleryObject = this.args[0];
        if (!galleryObject.scenes) {
            throw new Error("No scenes found on galleryObject: ".concat(JSON.stringify(galleryObject)));
        }
        var output = "<div class=\"gallery-grid\">";
        Object.keys(galleryObject.scenes).forEach(function (key) {
            var scene = galleryObject.scenes[key];
            if (scene.gallery) {
                if (scene.unlocked || game().dev.uAs) {
                    output += "<<button ".concat(JSON.stringify(scene.title), ">>") +
                        "<<set $dev.galleryMode = true>>" +
                        "<<goto \"".concat(key, "\">>") +
                        "<</button>>";
                }
                else {
                    output += "<<button ".concat(JSON.stringify("🔒 " + scene.title), ">>") +
                        "<<Notification \"info\" \"You have not unlocked this scene yet!\">>" +
                        "<</button>>";
                }
            }
            else {
                output += "<<button ".concat(JSON.stringify("❌ " + scene.title), ">>") +
                    "<<Notification \"warning\" \"This scene is not available in the gallery yet!\">>" +
                    "<</button>>";
            }
        });
        output += "</div>";
        new Wikifier(this.output, output);
    }
});
Macro.add('ReturnGallery', {
    handler: function () {
        Engine.play("GalleryPatreon");
        game().dev.galleryMode = false;
        ClothService.getDressed();
    }
});
/* twine-user-script #14: "GameController.js" */
"use strict";
Macro.add('CheckGameVersion', {
    handler: function () {
        checkGameVersion();
    }
});
Macro.add('GoToBedroom', {
    handler: function () {
        ClothService.changeClothAutomatic(ClothType.Casual);
        if (ApartmentService.isLivingInApartment()) {
            LocationService.enterLocation('ApartmentBedroom');
            LocationService.setPlayerLocation('Apartment');
        }
        else {
            LocationService.enterLocation('Bedroom');
            LocationService.setPlayerLocation('House');
        }
    }
});
window.checkPreferences = function () {
    var pregnancyDays = game().game.preferences.pregnancyDays;
    var pregnancyChance = game().game.preferences.pregnancyChance;
    if (isNaN(pregnancyDays)) {
        createNotification("Pregnancy days is not a number", NotificationType.WARNING);
        return false;
    }
    if (pregnancyDays < 7) {
        createNotification("Pregnancy days must be at least 7", NotificationType.WARNING);
        return false;
    }
    if (isNaN(pregnancyChance)) {
        createNotification("Pregnancy chance is not a number", NotificationType.WARNING);
        return false;
    }
    if (pregnancyChance < 0 || pregnancyChance > 100) {
        createNotification("Pregnancy chance must be between 0 and 100", NotificationType.WARNING);
        return false;
    }
    return true;
};
/* twine-user-script #15: "LeftBarController.js" */
"use strict";
Macro.add('ArousalDisplay', {
    handler: function () {
        var currentArousal = game().player.arousal;
        var maxArousal = game().game.maxArousal;
        var percentage = Math.floor((currentArousal / maxArousal) * 100);
        var arousalClass = percentage > 70 ? 'high' : percentage > 40 ? 'medium' : 'low';
        // Get arousal level and corresponding text
        var arousalLevel = currentArousal === 0 ? 0 : Math.min(Math.ceil((currentArousal / maxArousal) * 4), 4); // 0-4 scale
        var arousalData = LeftBarService.getArousalText(arousalLevel);
        var arousalIcon = arousalData.icon;
        var arousalText = arousalData.text;
        // Principal container
        var container = document.createElement('div');
        container.className = 'arousal-progress-container';
        // Tooltip
        var tooltip = document.createElement('div');
        tooltip.className = 'arousal-tooltip';
        tooltip.textContent = 'Arousal';
        // Progress bar
        var progressBar = document.createElement('div');
        progressBar.className = 'arousal-progress-bar';
        // Progress fill
        var progressFill = document.createElement('div');
        progressFill.className = "arousal-progress-fill ".concat(arousalClass);
        progressFill.style.width = "".concat(percentage, "%");
        // Progress text
        var progressText = document.createElement('span');
        progressText.className = 'arousal-progress-text';
        progressText.textContent = "".concat(arousalIcon, " ").concat(arousalText);
        progressBar.appendChild(progressFill);
        progressBar.appendChild(progressText);
        container.appendChild(progressBar);
        container.appendChild(tooltip);
        // Wrapper for the tooltip
        var wrapper = document.createElement('div');
        wrapper.className = 'arousal-wrapper';
        wrapper.appendChild(container);
        wrapper.appendChild(tooltip);
        $(this.output).append(wrapper);
    }
});
Macro.add('EnergyDisplay', {
    handler: function () {
        var currentEnergy = game().player.energy;
        var maxEnergy = game().game.maxEnergy;
        var percentage = Math.floor((currentEnergy / maxEnergy) * 100);
        var energyClass = percentage > 60 ? 'high' : percentage > 30 ? 'medium' : 'low';
        var energyIcon = percentage > 30 ? '🔋' : '🪫';
        // Principal container
        var container = document.createElement('div');
        container.className = 'energy-progress-container';
        // Tooltip
        var tooltip = document.createElement('div');
        tooltip.className = 'energy-tooltip';
        tooltip.textContent = 'Energy';
        // Progress bar
        var progressBar = document.createElement('div');
        progressBar.className = 'energy-progress-bar';
        // Progress fill
        var progressFill = document.createElement('div');
        progressFill.className = "energy-progress-fill ".concat(energyClass);
        progressFill.style.width = "".concat(percentage, "%");
        // Progress text
        var progressText = document.createElement('span');
        progressText.className = 'energy-progress-text';
        progressText.textContent = "".concat(energyIcon, " ").concat(percentage, "%");
        progressBar.appendChild(progressFill);
        progressBar.appendChild(progressText);
        container.appendChild(progressBar);
        // Wrapper for the tooltip
        var wrapper = document.createElement('div');
        wrapper.className = 'energy-wrapper';
        wrapper.appendChild(container);
        wrapper.appendChild(tooltip);
        $(this.output).append(wrapper);
    }
});
/* twine-user-script #16: "ObjectsController.js" */
"use strict";
function game() {
    return State.variables;
}
function player() {
    return game().player;
}
function clothes() {
    return game().clothes;
}
function instafame() {
    return player().phone.instafame;
}
function fastJobs() {
    return player().phone.fastJobs;
}
/* twine-user-script #17: "ItemController.js" */
"use strict";
Macro.add('BuyGymMembership', {
    handler: function () {
        var gym = this.args[0];
        var gymItem = game().items[gym];
        var gymImg = gymItem.image;
        var gymPrice = gymItem.price;
        var container = document.createElement('div');
        container.className = 'image-wrapper';
        var priceSpan = document.createElement('span');
        priceSpan.textContent = "".concat(gymPrice, " $");
        container.appendChild(priceSpan);
        var link = document.createElement('a');
        link.href = '#';
        link.addEventListener('click', function (e) {
            e.preventDefault();
            ItemService.buyGymMembership(gym);
        });
        var img = document.createElement('img');
        img.src = "".concat(setup.ImagePath, "/gym/").concat(gymImg);
        link.appendChild(img);
        container.appendChild(link);
        jQuery(this.output).append(container);
    }
});
Macro.add('Buy', {
    handler: function () {
        var itemId = this.args[0];
        ItemService.buyItem(itemId);
    }
});
/* twine-user-script #18: "LocationController.js" */
"use strict";
window.GameLocation = {};
Macro.add('EnterLocation', {
    handler: function () {
        var location = this.args[0];
        LocationService.enterLocation(location);
    }
});
Macro.add('SetPlayerLocation', {
    handler: function () {
        var location = this.args[0];
        LocationService.setPlayerLocation(location);
    }
});
Macro.add('UnlockLocation', {
    handler: function () {
        var location = this.args[0];
        LocationService.unlockLocation(location);
    }
});
Macro.add('createSubLocationButton', {
    handler: function () {
        var actionFragment = document.createDocumentFragment();
        new Wikifier(actionFragment, this.args[0]);
        var action = actionFragment.textContent;
        var location = this.args[1];
        var imagePath = this.args[2];
        var buttonHtml = "\n            <div class=\"image-wrapper\" style=\"display: inline-block;\">\n                <span>".concat(action, "</span>\n                <a href=\"javascript:void(0);\" onclick=\"handleSubLocation('").concat(location, "')\">\n                    <img src=\"").concat(setup.ImagePath + imagePath, "\" alt=\"").concat(action, "\">\n                </a>\n            </div>\n        ");
        $(this.output).append($(document.createElement('div')).html(buttonHtml));
    }
});
Macro.add('Bus', {
    handler: function () {
        var _location = this.args[0];
        if (_location.unlocked) {
            // Create the wrapper div & span for the title
            var busWrapper = document.createElement('div');
            busWrapper.className = 'image-wrapper';
            var titleSpan = document.createElement('span');
            titleSpan.textContent = _location.title;
            busWrapper.appendChild(titleSpan);
            if (_location.open === false) {
                var closedSpan = document.createElement('span');
                closedSpan.className = 'closed';
                closedSpan.innerHTML = '<span class="closed-label">CLOSED</span>' +
                    (_location.opensAt ? '<span class="closed-opens-at">Opens at ' + _location.opensAt + '</span>' : '');
                busWrapper.appendChild(closedSpan);
            }
            // Create the link element
            var linkEl = document.createElement('a');
            linkEl.href = 'javascript:void(0);';
            // Create the image element
            var imgEl = document.createElement('img');
            imgEl.src = setup.ImagePath + _location.imgPath;
            imgEl.alt = _location.title;
            linkEl.appendChild(imgEl);
            // Add click handler for link
            linkEl.addEventListener('click', function () {
                // Generate a random integer between 1 and 3
                if (Math.floor(Math.random() * 3) + 1 === 1) {
                    game().location.bus.busDestination = _location;
                    Engine.play("BusRandomEvent");
                }
                else {
                    LocationService.enterLocation(_location.name);
                }
            });
            busWrapper.appendChild(linkEl);
            $(this.output).append(busWrapper);
        }
    }
});
Macro.add('MoveNPC', {
    handler: function () {
        var npcName = this.args[0];
        var npcLocation = this.args[1];
        game().npc[npcName].location = npcLocation;
    }
});
Macro.add('CityMap', {
    handler: function () {
        var _location = this.args[0];
        if (_location.unlocked) {
            var mapWrapper = document.createElement('div');
            mapWrapper.className = 'image-wrapper';
            var titleSpan = document.createElement('span');
            titleSpan.textContent = _location.title;
            mapWrapper.appendChild(titleSpan);
            if (_location.open === false) {
                var closedSpan = document.createElement('span');
                closedSpan.className = 'closed';
                closedSpan.innerHTML = '<span class="closed-label">CLOSED</span>' +
                    (_location.opensAt ? '<span class="closed-opens-at">Opens at ' + _location.opensAt + '</span>' : '');
                mapWrapper.appendChild(closedSpan);
            }
            var linkEl = document.createElement('a');
            linkEl.href = 'javascript:void(0);';
            var imgEl = document.createElement('img');
            imgEl.src = setup.ImagePath + _location.imgPath;
            imgEl.alt = _location.title;
            linkEl.appendChild(imgEl);
            linkEl.addEventListener('click', function () {
                LocationService.enterLocation(_location.name);
            });
            mapWrapper.appendChild(linkEl);
            $(this.output).append(mapWrapper);
        }
    }
});
Macro.add('UpdatePreviousPassage', {
    handler: function () {
        LocationService.updatePreviousPassage();
    }
});
Macro.add('UpdateLocationsImg', {
    handler: function () {
        LocationService.updateLocationsImg();
    }
});
window.handleSubLocation = function (location) {
    LocationService.handleSubLocation(location);
};
window.isPlayerAtHouse = function () {
    return game().player.location == "House";
};
/**
 * Returns the correct passage name based on player location.
 * If player is at house, returns the house passage.
 * If player is at apartment, returns the apartment passage.
 *
 * @param housePassage - The passage name for the house (e.g., "Bedroom", "Kitchen")
 * @returns The correct passage name based on current location
 */
window.getLocationPassage = function (housePassage) {
    var passageMap = {
        "Bedroom": "ApartmentBedroom",
        "Kitchen": "ApartmentKitchen",
        "Bathroom": "ApartmentBathroom",
        "LivingRoom": "ApartmentLivingRoom",
        "Hallway": "ApartmentHallway"
    };
    if (window.isPlayerAtHouse()) {
        return housePassage;
    }
    else {
        return passageMap[housePassage] || housePassage;
    }
};
/**
 * Macro to create a return button that automatically navigates to the correct location
 * based on whether the player is at house or apartment.
 *
 * Usage:
 *   <<ReturnButton "Bedroom">>
 *   <<ReturnButton "Kitchen" "Voltar">>
 *   <<ReturnButton "Bathroom">>
 *     <<AddTime 1>>
 *     <<Energy -10>>
 *   <</ReturnButton>>
 */
Macro.add('ReturnButton', {
    tags: null,
    handler: function () {
        var housePassage = this.args[0];
        var buttonText = this.args[1] || 'Return ↩️';
        if (!housePassage) {
            throw new Error('ReturnButton: House passage name is required');
        }
        var targetPassage = window.getLocationPassage(housePassage);
        var content = this.payload && this.payload[0] ? this.payload[0].contents : '';
        // Create button with goto macro
        var buttonHtml = "<<button \"".concat(buttonText, "\">>").concat(content, "<<goto \"").concat(targetPassage, "\">><</button>>");
        new Wikifier(this.output, buttonHtml);
    }
});
/* twine-user-script #19: "CasinoController.js" */
"use strict";
Macro.add('ClearRoulette', {
    handler: function () {
        CasinoService.clearRoulette();
    }
});
Macro.add('ClearRouletteResult', {
    handler: function () {
        CasinoService.clearRouletteResult();
    }
});
Macro.add('SpinRoulette', {
    handler: function () {
        CasinoService.spinRoulette();
    }
});
Macro.add('ClearSlots', {
    handler: function () {
        CasinoService.clearSlots();
    }
});
Macro.add('SpinSlots', {
    handler: function () {
        CasinoService.spinSlots();
    }
});
/* twine-user-script #20: "DrivingSchoolController.js" */
"use strict";
Macro.add('TakeDrivingLesson', {
    handler: function () {
        var result = DrivingSchoolService.takeLesson();
        if (!result.success) {
            createNotification(result.message, NotificationType.WARNING);
        }
    }
});
window.getDrivingSchoolStats = function () {
    return DrivingSchoolService.getDrivingSchoolStats();
};
window.canTakePracticalExam = function () {
    return DrivingSchoolService.canTakePracticalExam();
};
Macro.add('PassPracticalExam', {
    handler: function () {
        var result = DrivingSchoolService.passPracticalExam();
        if (!result.success) {
            createNotification(result.message, NotificationType.WARNING);
        }
    }
});
Macro.add('FailPracticalExam', {
    handler: function () {
        DrivingSchoolService.failPracticalExam();
    }
});
/* twine-user-script #21: "SchoolController.js" */
"use strict";
Macro.add('createClassButton', {
    handler: function () {
        var className = this.args[0];
        var classData = game().location.school[className];
        var buttonHtml = "\n            <div class=\"image-wrapper inline-block\">\n                <span>".concat(classData.title, "</span>\n                <a href=\"javascript:void(0);\" onclick=\"SugarCube.Engine.play('").concat(classData.location, "')\">\n                    <img src=\"").concat(setup.ImagePath + classData.imagePath, "\" alt=\"").concat(classData.title, "\">\n                </a>\n            </div>\n        ");
        $(this.output).append($(document.createElement('div')).html(buttonHtml));
    }
});
Macro.add('class', {
    handler: function () {
        var className = this.args[0];
        var location = this.args[1];
        var imagePath = this.args[2];
        var classHtml = "\n            <div class=\"image-wrapper\">\n                <span>".concat(className, "</span>\n                <<link [img[").concat(setup.ImagePath + imagePath, "]]>>\n                    <<goto ").concat(location, ">>\n                <</link>>\n            </div>\n        ");
        new Wikifier(this.output, classHtml);
    }
});
window.checkGraduationRequirements = function () {
    return SchoolService.checkGraduationRequirements();
};
window.getSchoolStats = function () {
    return SchoolService.getSchoolStats();
};
window.calculateGrade = function () {
    SchoolService.calculateGrade();
};
window.recordTestResult = function (grade) {
    SchoolService.recordTestResult(grade);
};
window.processFinalExam = function (grade) {
    return SchoolService.processFinalExam(grade);
};
window.graduate = function () {
    return SchoolService.graduate();
};
window.getGraduationReasonText = function (reason) {
    var reasonMap = {
        "alreadyGraduated": "You have already graduated from school.",
        "needMoreTests": "You need to complete more tests before you can graduate.",
        "canTakeFinalExamOrContinue": "You can take the final exam or continue with more tests to improve your average."
    };
    return reasonMap[reason] || reason;
};
window.forceGraduate = function () {
    SchoolService.forceGraduate();
};
window.resetSchoolProgress = function () {
    SchoolService.resetSchoolProgress();
};
window.maximizeSchoolAverage = function () {
    SchoolService.maximizeSchoolAverage();
};
window.getSchoolAverageGrade = function () {
    var school = game().location.school;
    var testsCompleted = school.testsCompleted || 0;
    if (testsCompleted > 0) {
        var average = school.averageGrade || 0;
        return (Math.round(average * 10) / 10).toString();
    }
    return "-";
};
window.isPlayerGraduated = function () {
    var _a;
    return (_a = game().location.school.graduated) !== null && _a !== void 0 ? _a : false;
};
Macro.add('ForceGraduate', {
    handler: function () {
        if (galleryMode())
            return;
        SchoolService.forceGraduate();
        createNotification("You have graduated from school!", NotificationType.SUCCESS);
    }
});
Macro.add('ResetSchoolProgress', {
    handler: function () {
        if (galleryMode())
            return;
        SchoolService.resetSchoolProgress();
        createNotification("School progress has been reset!", NotificationType.SUCCESS);
    }
});
Macro.add('MaximizeSchoolAverage', {
    handler: function () {
        if (galleryMode())
            return;
        SchoolService.maximizeSchoolAverage();
        createNotification("School average set to maximum (10.0)!", NotificationType.SUCCESS);
    }
});
/* twine-user-script #22: "NpcController.js" */
"use strict";
Macro.add("Talk", {
    handler: function () {
        var npc = this.args[0];
        NpcService.npcTalk(npc);
    }
});
Macro.add('Speech', {
    handler: function () {
        var id = this.args[0];
        var name = id;
        var message = '';
        // Handle different argument patterns
        if (this.args.length === 1) {
            // Only ID provided, require at least a message
            throw new Error('Speech macro requires at least 2 arguments: ID and message');
        }
        else if (this.args.length === 2) {
            // ID and message provided
            message = this.args[1];
        }
        else if (this.args.length === 3) {
            // ID, name, and message provided
            name = this.args[1];
            message = this.args[2];
        }
        var npcName = name;
        var speakerId = id;
        var g = game();
        // If it's a known NPC, use the proper name only when no custom name is provided
        var hasCustomName = this.args.length === 3 && typeof this.args[1] === 'string' && this.args[1].trim() !== '';
        if (!hasCustomName) {
            if (id !== 'Player' && g.npc && g.npc[id] && g.npc[id].name) {
                npcName = g.npc[id].name;
            }
            else if (id === 'Player' && g.player && g.player.name) {
                npcName = g.player.name;
            }
            else {
                npcName = name; // fallback
            }
        }
        // Create speech bubble with enhanced structure
        var output = '<div class="speech ' + speakerId + '">';
        output += '<span class="avatar"></span>';
        output += '<div class="speech-content">';
        output += '<b>' + npcName + '</b>';
        output += '<hr>';
        output += '<div class="speech-text">' + message + '</div>';
        output += '</div>';
        output += '</div>';
        // Add animation effect
        $(this.output).wiki(output);
        // Add entrance animation
        var $speech = $(this.output).find('.speech').last();
        $speech.css({
            'opacity': '0',
            'transform': 'translateY(20px) scale(0.95)'
        });
        $speech.animate({
            'opacity': '1'
        }, 300).css({
            'transform': 'translateY(0) scale(1)'
        });
    }
});
Macro.add('SpeechPhone', {
    handler: function () {
        var id = this.args[0];
        var name = id;
        var message = '';
        if (this.args.length === 1) {
            throw new Error('SpeechPhone macro requires at least 2 arguments: ID and message');
        }
        else if (this.args.length === 2) {
            message = this.args[1];
        }
        else if (this.args.length === 3) {
            name = this.args[1];
            message = this.args[2];
        }
        var npcName = name;
        var speakerId = id;
        var g = game();
        var hasCustomName = this.args.length === 3 && typeof this.args[1] === 'string' && this.args[1].trim() !== '';
        if (!hasCustomName) {
            if (id !== 'Player' && g.npc && g.npc[id] && g.npc[id].name) {
                npcName = g.npc[id].name;
            }
            else if (id === 'Player' && g.player && g.player.name) {
                npcName = g.player.name;
            }
            else {
                npcName = name;
            }
        }
        var output = '<div class="speech speech-phone ' + speakerId + '">';
        output += '<span class="avatar"></span>';
        output += '<div class="speech-content">';
        output += '<div class="speech-phone-name">' + npcName + '</div>';
        output += '<div class="speech-text">' + message + '</div>';
        output += '</div>';
        output += '</div>';
        $(this.output).wiki(output);
        var $speech = $(this.output).find('.speech-phone').last();
        $speech.css({
            'opacity': '0',
            'transform': 'translateY(12px)'
        });
        $speech.animate({
            'opacity': '1'
        }, 220).css({
            'transform': 'translateY(0)'
        });
    }
});
// Thought Macro - simulates internal thoughts
Macro.add('Think', {
    handler: function () {
        var id = this.args[0];
        var message = this.args[1];
        // Handle NPC/Player logic using game() like Speech macro
        var npcName = id;
        var speakerId = id;
        var g = game();
        // If it's a known NPC, get the proper name
        if (id !== 'Player' && g.npc && g.npc[id]) {
            npcName = g.npc[id].name;
        }
        else if (id === 'Player' && g.player) {
            npcName = g.player.name;
        }
        // Create thought bubble with different styling
        var output = '<div class="speech thought ' + speakerId + '">';
        output += '<span class="avatar thought-avatar"></span>';
        output += '<div class="speech-content">';
        output += '<b>💭 ' + npcName + ' is thinking...</b>';
        output += '<hr>';
        output += '<div class="speech-text thought-text">' + message + '</div>';
        output += '</div>';
        output += '</div>';
        // Add animation effect
        $(this.output).wiki(output);
        // Add entrance animation
        var $speech = $(this.output).find('.speech').last();
        $speech.css({
            'opacity': '0',
            'transform': 'translateY(20px) scale(0.95)'
        });
        $speech.animate({
            'opacity': '1'
        }, 300).css({
            'transform': 'translateY(0) scale(1)'
        });
    }
});
window.GetNpcArousal = function (npc) {
    var _a;
    return (_a = game().npc[npc].arousal) !== null && _a !== void 0 ? _a : 0;
};
window.GetNpcLocation = function (npc) {
    return game().npc[npc].location;
};
window.IsNpcAtHome = function (npc) {
    if (game().npc[npc].location == "Bedroom"
        || game().npc[npc].location == "Bathroom"
        || game().npc[npc].location == "Kitchen"
        || game().npc[npc].location == "Living Room"
        || game().npc[npc].location == "Garage")
        return true;
    else
        return false;
};
/* twine-user-script #23: "PlayerController.js" */
"use strict";
Macro.add('MakeBoyfriend', {
    handler: function () {
        var npc = this.args[0];
        PlayerService.makeBoyfriend(npc);
        createNotification("You are now in a relationship with " + npc + "!", NotificationType.LOVE);
    }
});
window.isOnRelationship = function () {
    return player().relationship.npcName !== null && player().relationship.npcName !== undefined;
};
window.isBoyfriend = function (npcName) {
    return PlayerService.isBoyfriend(npcName);
};
/* twine-user-script #24: "BabyController.js" */
"use strict";
Macro.add("AddBabyAge", {
    handler: function () {
        BabyService.addBabyAge();
    }
});
Macro.add("GiveAdoption", {
    handler: function () {
        var baby = this.args[0];
        BabyService.removeBaby(baby);
        createNotification("You gave " + baby.name + " for adoption, you feel bad with your choice", NotificationType.SUCCESS);
        updateScreen();
    }
});
/* twine-user-script #25: "BankController.js" */
"use strict";
Macro.add('CreateBankAccount', {
    handler: function () {
        BankService.openBankAccount();
    }
});
Macro.add('OpenBankMenu', {
    handler: function () {
        BankService.openBankMenu();
    }
});
Macro.add('CloseBankMenu', {
    handler: function () {
        BankService.closeBankMenu();
    }
});
Macro.add('BankDeposit', {
    handler: function () {
        var amount = this.args[0];
        BankService.bankDeposit(amount);
    }
});
Macro.add('BankWithdraw', {
    handler: function () {
        var amount = this.args[0];
        BankService.bankWithdraw(amount);
    }
});
/* twine-user-script #26: "ClothController.js" */
"use strict";
Macro.add('BuyCloth', {
    handler: function () {
        var cloth = this.args[0];
        ClothService.buyCloth(cloth);
    }
});
Macro.add('ChangeClothes', {
    handler: function () {
        var cloth = this.args[0];
        ClothService.changeClothes(cloth);
    }
});
Macro.add('GetNaked', {
    handler: function () {
        ClothService.getNaked();
    }
});
Macro.add('GetDressed', {
    handler: function () {
        ClothService.getDressed();
    }
});
Macro.add('UpdateClothesPregnant', {
    handler: function () {
        var isPregnant = this.args[0];
        ClothService.updateClothes(isPregnant);
    }
});
Macro.add('ClothShop', {
    handler: function () {
        var cloth = this.args[0];
        if (cloth.purchased) {
            return;
        }
        var shopDiv = document.createElement('div');
        shopDiv.className = 'gridStore-item store-item';
        var headerDiv = document.createElement('div');
        headerDiv.className = 'store-item-header';
        shopDiv.appendChild(headerDiv);
        var titleDiv = document.createElement('h3');
        titleDiv.className = 'store-item-title';
        titleDiv.textContent = cloth.title;
        headerDiv.appendChild(titleDiv);
        var imageDiv = document.createElement('div');
        imageDiv.className = 'store-item-image';
        shopDiv.appendChild(imageDiv);
        var img = document.createElement('img');
        img.src = "".concat(setup.ImagePath, "/player/clothes/").concat(cloth.type, "/").concat(cloth.image);
        img.alt = cloth.name;
        imageDiv.appendChild(img);
        var priceDiv = document.createElement('div');
        priceDiv.className = 'store-item-price';
        priceDiv.textContent = "$".concat(cloth.price);
        shopDiv.appendChild(priceDiv);
        var actionsDiv = document.createElement('div');
        actionsDiv.className = 'store-item-actions';
        shopDiv.appendChild(actionsDiv);
        var button = document.createElement('button');
        button.className = 'store-buy-btn';
        button.textContent = '🛒 Buy Now';
        button.addEventListener('click', function () {
            ClothService.buyCloth(cloth);
        });
        actionsDiv.appendChild(button);
        var beautyDiv = document.createElement('div');
        beautyDiv.className = 'gridStore-text';
        beautyDiv.textContent = "+".concat(cloth.beauty, " beauty");
        beautyDiv.style.color = '#4ecdc4';
        beautyDiv.style.fontSize = '0.9em';
        beautyDiv.style.marginTop = '10px';
        actionsDiv.appendChild(beautyDiv);
        var corruptionDiv = document.createElement('div');
        corruptionDiv.className = 'gridStore-text';
        if (cloth.corruption > 0) {
            corruptionDiv.textContent = "Requires ".concat(cloth.corruption, "+ corruption");
        }
        else {
            corruptionDiv.textContent = 'No corruption required';
        }
        corruptionDiv.style.color = '#ff6b6b';
        corruptionDiv.style.fontSize = '0.9em';
        corruptionDiv.style.marginTop = '5px';
        actionsDiv.appendChild(corruptionDiv);
        $(this.output).append(shopDiv);
    }
});
Macro.add('Wardrobe', {
    handler: function () {
        var cloth = this.args[0];
        if (!cloth.purchased) {
            return;
        }
        var wardrobeDiv = document.createElement('div');
        wardrobeDiv.className = 'gridWardrobe-item';
        var nameDiv = document.createElement('div');
        nameDiv.className = 'gridwardrobe-text';
        nameDiv.textContent = cloth.title;
        wardrobeDiv.appendChild(nameDiv);
        var beautyDiv = document.createElement('div');
        beautyDiv.className = 'gridwardrobe-beauty';
        beautyDiv.textContent = "+".concat(cloth.beauty, " beauty \uD83D\uDC84");
        wardrobeDiv.appendChild(beautyDiv);
        var link = document.createElement('a');
        link.href = 'javascript:void(0)';
        link.addEventListener('click', function () {
            ClothService.changeClothes(cloth);
        });
        var img = document.createElement('img');
        img.src = "".concat(setup.ImagePath, "/player/clothes/").concat(cloth.type, "/").concat(cloth.image);
        img.alt = cloth.name;
        link.appendChild(img);
        wardrobeDiv.appendChild(link);
        var buttonContainer = document.createElement('div');
        buttonContainer.className = 'wardrobe-button-container';
        // --- Button Logic ---
        var defaultButton = document.createElement('button');
        defaultButton.className = 'button';
        if (cloth.isDefault) {
            // If it's the default outfit
            defaultButton.textContent = 'Default Outfit';
            defaultButton.disabled = true; // Make the button non-interactive
        }
        else {
            // If it's not the default outfit
            defaultButton.textContent = 'Set as Default';
            defaultButton.addEventListener('click', function () {
                ClothService.setDefaultCloth(cloth);
            });
        }
        buttonContainer.appendChild(defaultButton);
        wardrobeDiv.appendChild(buttonContainer);
        $(this.output).append(wardrobeDiv);
    }
});
/* twine-user-script #27: "CorruptionController.js" */
"use strict";
window.StageOneCorruption = function (npc) {
    return game().dev.galleryMode || (npc.corruption >= 5 && npc.arousal >= 1);
};
window.StageTwoCorruption = function (npc) {
    return game().dev.galleryMode || (npc.corruption >= 10 && npc.arousal >= 2);
};
window.StageThreeCorruption = function (npc) {
    return game().dev.galleryMode || (npc.corruption >= 15 && npc.arousal >= 3);
};
window.getCorruptionLevel = function () {
    return CorruptionService.getCorruptionLevel();
};
window.getArousal = function () {
    return game().dev.galleryMode ? 10 : game().player.arousal;
};
window.getExb = function () {
    return game().dev.galleryMode ? 99 : game().player.exhibitionism;
};
window.getNpcCorruption = function (npc) {
    return game().npc[npc].corruption;
};
window.getPlayerCorruptionPoints = function () {
    return CorruptionService.getCorruptionPoints();
};
window.getPlayerCorruptionLevel = function () {
    return window.getCorruptionLevel();
};
window.getCorruptionTitle = function () {
    var level = window.getCorruptionLevel();
    switch (true) {
        case (level == 0):
            return "Pure 😇";
        case (level == 1):
            return "Innocent 😊";
        case (level == 2):
            return "Naughty 😏";
        case (level == 3):
            return "Slut 😈";
        case (level >= 4):
            return "Whore 🔥";
        default:
            throw new Error("Invalid corruption level");
    }
};
Macro.add("CorruptionDisplay", {
    handler: function () {
        var _a;
        var level = Math.min(Math.max(0, Math.floor(CorruptionService.getCorruptionLevel())), 4);
        var title = window.getCorruptionTitle();
        var classes = ["pure", "innocent", "naughty", "slut", "whore"];
        var cls = (_a = classes[level]) !== null && _a !== void 0 ? _a : "pure";
        $(this.output).append($("<div></div>").addClass(cls).text(title));
    }
});
Macro.add("CorruptionController", {
    handler: function () {
        CorruptionService.updateCorruptionTitle();
    }
});
Macro.add("NotifyExhibitionism", {
    handler: function () {
        var exbNeeded = this.args[0];
        var notification = "You are not exhibitionist enough to do this. (".concat(exbNeeded, "+ exhibitionism required!)");
        createNotification(notification, NotificationType.EXB);
    }
});
Macro.add("NotifyCorruption", {
    handler: function () {
        var levelNeeded = this.args[0];
        var pointsMap = [0, 5, 15, 30, 45];
        var pointsNeeded = pointsMap[levelNeeded] || levelNeeded;
        var corruptionMessage = "You are not corrupted enough to do this. (".concat(pointsNeeded, "+ corruption required!)");
        createNotification(corruptionMessage, NotificationType.CORRUPTION);
    }
});
Macro.add("StageNotification", {
    handler: function () {
        var npc = this.args[0];
        var requirement = this.args[1];
        switch (requirement) {
            case 1:
                var notification = "You need to corrupt your ".concat(npc.relationship, " more! They need at least 5 corruption and to be a little aroused \uD83D\uDD25!");
                createNotification(notification, NotificationType.CORRUPTION);
                break;
            case 2:
                var notification2 = "Your ".concat(npc.relationship, " is starting to enjoy this! Push them further - at least 10 corruption and aroused \uD83D\uDD25\uD83D\uDD25!");
                createNotification(notification2, NotificationType.CORRUPTION);
                break;
            case 3:
                var notification3 = "Things are getting intense! Your ".concat(npc.relationship, " needs at least 15 corruption and to be very aroused \uD83D\uDD25\uD83D\uDD25\uD83D\uDD25!");
                createNotification(notification3, NotificationType.CORRUPTION);
                break;
        }
    }
});
Macro.add("UpdateFamilyArousal", {
    handler: function () {
        CorruptionService.updateFamilyArousal();
    }
});
/* twine-user-script #28: "DrugController.js" */
"use strict";
Macro.add("UseDrug", {
    handler: function () {
        var drug = this.args[0];
        DrugService.useDrugs(drug);
    }
});
Macro.add("UseDrugs", {
    handler: function () {
        var items = game().items;
        var inventory = game().player.inventory;
        var output = '';
        Object.keys(items).forEach(function (itemName) {
            var item = items[itemName];
            // Filter for drugs and check if player has the item
            if (item.type === "drugs" && inventory[itemName] > 0) {
                output += "<<button ".concat(JSON.stringify("Use " + item.title), ">>") +
                    "<<UseDrug ".concat(JSON.stringify(itemName), ">>") +
                    "<</button>>";
            }
        });
        if (output) {
            new Wikifier(this.output, output);
        }
    }
});
/* twine-user-script #29: "EnergyController.js" */
"use strict";
Macro.add('EnergyController', {
    handler: function () {
        EnergyService.checkEnergy();
    }
});
Macro.add('NotifyEnergy', {
    handler: function () {
        EnergyService.notifyLowEnergy();
    }
});
/* twine-user-script #30: "GangController.js" */
"use strict";
Macro.add('SetDaysToWork', {
    handler: function () {
        GangService.setDaysToWork(Number(this.args[0]));
    }
});
Macro.add('AddVipersRespect', {
    handler: function () {
        GangService.addVipersRespect();
    }
});
Macro.add('PromoteViper', {
    handler: function () {
        GangService.promoteViper(this.args[0], this.args[1]);
    }
});
/* twine-user-script #31: "InventoryController.js" */
"use strict";
window.isPurchased = function (item) {
    return InventoryService.isPurchased(item);
};
Macro.add('AddToInventory', {
    handler: function () {
        var itemName = this.args[0];
        InventoryService.addToInventory(itemName);
    }
});
Macro.add('RemoveFromInventory', {
    handler: function () {
        var itemName = this.args[0];
        InventoryService.removeFromInventory(itemName);
    }
});
/* twine-user-script #32: "JobsController.js" */
"use strict";
Macro.add("AddJob", {
    handler: function () {
        var jobName = this.args[0];
        JobsService.addJob(jobName);
    }
});
Macro.add("AddJobXp", {
    handler: function () {
        var jobName = this.args[0];
        var xp = this.args[1];
        JobsService.addJobXp(jobName, xp);
    }
});
Macro.add("AddJobRank", {
    handler: function () {
        var jobName = this.args[0];
        var rank = this.args[1];
        JobsService.addJobRank(jobName, rank);
    }
});
window.isJobActive = function (jobName) {
    return JobsService.isJobActive(jobName);
};
window.getJobXp = function (jobName) {
    return JobsService.getJobXp(jobName);
};
window.getJobRank = function (jobName) {
    return JobsService.getJobRank(jobName);
};
/* twine-user-script #33: "PregnancyController.js" */
"use strict";
Macro.add('MakePregnant', {
    handler: function () {
        PregnancyService.makePregnant();
        createNotification("You are now pregnant", NotificationType.INFO);
    }
});
Macro.add('FinishPregnancy', {
    handler: function () {
        var _a;
        var babyName = this.args[0];
        PregnancyService.finishPregnancy(babyName, (_a = this.args[1]) !== null && _a !== void 0 ? _a : false);
    }
});
Macro.add('RemovePregnancy', {
    handler: function () {
        PregnancyService.removePregnancy();
        createNotification("You are not pregnant anymore", NotificationType.WARNING);
    }
});
Macro.add('AbortPregnancy', {
    handler: function () {
        PregnancyService.removePregnancy();
        game().player.statistics.abortions++;
        createNotification("You aborted your pregnancy", NotificationType.WARNING);
    }
});
Macro.add("DnaTest", {
    handler: function () {
        PregnancyService.dnaTest();
    }
});
window.isPregnant = function () {
    return PregnancyService.isPregnant();
};
window.hasPregnancySymptoms = function () {
    return PregnancyService.hasEarlySymptoms();
};
window.changeMediaPregnant = function () {
    return PregnancyService.changeMediaPregnant();
};
window.getPregnancyProgress = function () {
    return PregnancyService.getPregnancyProgress();
};
window.getPregnancyStage = function () {
    return PregnancyService.getPregnancyStage();
};
window.hasVisibleBelly = function () {
    return PregnancyService.hasVisibleBelly();
};
window.getPregnancyStatusText = function () {
    return PregnancyService.getPregnancyStatusText();
};
window.haveBaby = function () {
    var player = game().player;
    return player && player.baby ? player.baby.length > 0 : false;
};
/* twine-user-script #34: "SexController.js" */
"use strict";
Macro.add('FinishSex', {
    handler: function () {
        var npc = this.args[0];
        var inside = this.args[1];
        if (galleryMode())
            return;
        SexService.finishSex(npc, inside);
    }
});
Macro.add('FinishMasturbation', {
    handler: function () {
        if (galleryMode())
            return;
        SexService.finishMasturbation();
    }
});
/* twine-user-script #35: "StatsController.js" */
"use strict";
Macro.add('AddCorruption', {
    handler: function () {
        StatsService.addCorruption();
    }
});
Macro.add('ReduceCorruption', {
    handler: function () {
        if (!galleryMode() && game().player.corruption.points > 0) {
            game().player.corruption.points -= 1;
            CorruptionService.updateCorruptionTitle();
            createNotification("Corruption reduced", NotificationType.CORRUPTION);
            updateBar();
        }
    }
});
Macro.add('AddExb', {
    handler: function () {
        if (galleryMode())
            return;
        game().player.exhibitionism += 1;
        createNotification("Exhibitionism increased", "exb");
        updateBar();
    }
});
Macro.add('AddBrotherCorruption', {
    handler: function () {
        if (galleryMode())
            return;
        NpcService.addCorruption('Brother');
    }
});
Macro.add('AddBrotherArousal', {
    handler: function () {
        if (galleryMode())
            return;
        StatsService.increaseArousal(game().npc.Brother, 3);
    }
});
Macro.add('ResetBrotherArousal', {
    handler: function () {
        if (galleryMode())
            return;
        game().npc.Brother.arousal = 0;
        updateBar();
    }
});
Macro.add('ResetGrandpaArousal', {
    handler: function () {
        if (galleryMode())
            return;
        game().npc.Grandpa.arousal = 0;
        updateBar();
    }
});
Macro.add('ResetDadArousal', {
    handler: function () {
        if (galleryMode())
            return;
        game().npc.Dad.arousal = 0;
        updateBar();
    }
});
Macro.add('AddDadCorruption', {
    handler: function () {
        if (galleryMode())
            return;
        NpcService.addCorruption('Dad');
    }
});
Macro.add('AddDadArousal', {
    handler: function () {
        if (galleryMode())
            return;
        StatsService.increaseArousal(game().npc.Dad, 3);
    }
});
Macro.add('AddInt', {
    handler: function () {
        if (galleryMode())
            return;
        game().player.intelligence += 1;
        createNotification("Intelligence increased", NotificationType.INT);
        updateBar();
    }
});
Macro.add('AddFit', {
    handler: function () {
        if (galleryMode())
            return;
        game().player.fitness += 1;
        createNotification("Fitness increased", NotificationType.FITNESS);
        StatsService.improveMcMaximumStats();
        updateBar();
    }
});
Macro.add('AddSocial', {
    handler: function () {
        StatsService.addSocial();
    }
});
Macro.add('AddArousal', {
    handler: function () {
        StatsService.addArousal();
    }
});
Macro.add('ResetArousal', {
    handler: function () {
        StatsService.resetArousal();
    }
});
Macro.add('AddMoney', {
    handler: function () {
        if (galleryMode())
            return;
        var moneyValue = this.args[0];
        StatsService.addMoney(moneyValue);
    }
});
Macro.add('AddDirtyMoney', {
    handler: function () {
        if (galleryMode())
            return;
        var dirtyMoneyValue = this.args[0];
        if (game().player.dirtyMoney + dirtyMoneyValue >= 0) {
            game().player.dirtyMoney += dirtyMoneyValue;
            if (dirtyMoneyValue > 0) {
                createNotification("You earn $" + dirtyMoneyValue + " dirty money", NotificationType.MONEY);
            }
            else if (dirtyMoneyValue < 0) {
                createNotification("You pay $" + Math.abs(dirtyMoneyValue) + " dirty money", NotificationType.MONEY);
            }
            ;
            updateBar();
        }
    }
});
Macro.add('LaunderMoney', {
    handler: function () {
        var dirtyMoneyToLaunder = this.args[0];
        StatsService.launderMoney(dirtyMoneyToLaunder);
    }
});
Macro.add('AddRelation', {
    handler: function () {
        if (galleryMode())
            return;
        var npc = this.args[0];
        NpcService.addRelation(npc);
    }
});
Macro.add('Energy', {
    handler: function () {
        if (galleryMode())
            return;
        var energyValue = this.args[0];
        StatsService.addEnergy(energyValue);
    }
});
Macro.add('AddBeauty', {
    handler: function () {
        if (galleryMode())
            return;
        game().player.beauty += 1;
        createNotification("Beauty increased", NotificationType.BEAUTY);
        updateBar();
    }
});
Macro.add('AddDrunkness', {
    handler: function () {
        StatsService.addDrunkness();
    }
});
Macro.add('AddIntimacy', {
    handler: function () {
        if (galleryMode())
            return;
        game().player.relationship.intimacy += 1;
        createNotification("Intimacy increased", NotificationType.LOVE);
    }
});
Macro.add('AddNpcCorruption', {
    handler: function () {
        if (galleryMode())
            return;
        var npc = this.args[0];
        var qtd = this.args[1];
        game().npc[npc].corruption += qtd !== null && qtd !== void 0 ? qtd : 1;
        createNotification("".concat(game().npc[npc].name, " corruption increased"), NotificationType.CORRUPTION);
        updateBar();
    }
});
Macro.add('NotifyNpcCorruption', {
    handler: function () {
        var npc = this.args[0];
        var corruptionNeeded = this.args[1];
        createNotification("".concat(game().npc[npc].name, " is not corrupted enough. ").concat(corruptionNeeded, "+ corruption required."), NotificationType.WARNING);
    }
});
Macro.add('NotifyNpcRelation', {
    handler: function () {
        var npc = this.args[0];
        var relationNeeded = this.args[1];
        createNotification("".concat(game().npc[npc].name, " relation is not high enough. ").concat(relationNeeded, "+ relation required."), NotificationType.WARNING);
    }
});
Macro.add('AddInstafameFollowers', {
    handler: function () {
        if (galleryMode())
            return;
        StatsService.addInstafameFollowers(this.args[0]);
    }
});
Macro.add('ResetDrunkness', {
    handler: function () {
        if (galleryMode())
            return;
        game().player.drunkness = 0;
        updateBar();
    }
});
window.getBeauty = function () {
    return StatsService.getBeauty();
};
window.getRelation = function (npc) {
    var _a;
    return galleryMode() ? 99 : (_a = game().npc[npc].relation) !== null && _a !== void 0 ? _a : 0;
};
window.getDrunkness = function () {
    var _a;
    return (_a = game().player.drunkness) !== null && _a !== void 0 ? _a : 0;
};
/* twine-user-script #36: "PropertyController.js" */
"use strict";
// Expose PropertyService methods as global functions for Twine passages
window.PropertyService = {
    getRentAmount: function (propertyId) {
        return PropertyService.getRentAmount(propertyId);
    },
    getTotalRentDue: function (propertyId) {
        return PropertyService.getTotalRentDue(propertyId);
    },
    getAccumulatedDebt: function (propertyId) {
        return PropertyService.getAccumulatedDebt(propertyId);
    },
    getLateFeeAmount: function (propertyId) {
        return PropertyService.getLateFeeAmount(propertyId);
    },
    hasAccumulatedDebt: function (propertyId) {
        return PropertyService.hasAccumulatedDebt(propertyId);
    },
    hasLateFee: function (propertyId) {
        return PropertyService.hasLateFee(propertyId);
    },
    getSkippedRentCount: function (propertyId) {
        return PropertyService.getSkippedRentCount(propertyId);
    },
    canAcquireProperty: function (propertyId) {
        return PropertyService.canAcquireProperty(propertyId);
    },
    getLandlordName: function (propertyId) {
        return PropertyService.getLandlordName(propertyId);
    },
    hasProperty: function (propertyId) {
        return PropertyService.hasProperty(propertyId);
    },
    isRentDue: function (propertyId) {
        return PropertyService.isRentDue(propertyId);
    },
    canAffordRent: function (propertyId) {
        return PropertyService.canAffordRent(propertyId);
    },
    payRent: function (propertyId) {
        return PropertyService.payRent(propertyId);
    },
    skipRent: function (propertyId) {
        return PropertyService.skipRent(propertyId);
    },
    alternativePayment: function (propertyId) {
        PropertyService.alternativePayment(propertyId);
    },
    getDaysUntilRent: function (propertyId) {
        return PropertyService.getDaysUntilRent(propertyId);
    },
    getCurrentResidence: function () {
        return PropertyService.getCurrentResidence();
    },
    hasAnyProperty: function () {
        return PropertyService.hasAnyProperty();
    },
    decrementRentDays: function () {
        PropertyService.decrementRentDays();
    },
    unrentProperty: function (propertyId) {
        return PropertyService.unrentProperty(propertyId);
    }
};
// Helper functions for apartment grid display
window.getApartmentInfo = function () {
    var hasApartment = PropertyService.hasProperty("apartment");
    if (!hasApartment) {
        return {
            hasApartment: false,
            rent: "-",
            daysUntilRent: "-",
            landlord: "-",
            debt: "-",
            hasLateFee: false
        };
    }
    var days = PropertyService.getDaysUntilRent("apartment");
    var daysUntilRent = PropertyService.isRentDue("apartment")
        ? "Due now!"
        : days + " day" + (days !== 1 ? "s" : "");
    var totalDue = PropertyService.getTotalRentDue("apartment");
    var debt = PropertyService.getAccumulatedDebt("apartment");
    var hasLateFee = PropertyService.hasLateFee("apartment");
    // Show total due if there's debt or late fee, otherwise show base rent
    var rentDisplay = debt > 0 || hasLateFee
        ? "$".concat(totalDue, " (Base: $").concat(PropertyService.getRentAmount("apartment")).concat(debt > 0 ? " + Debt: $".concat(debt) : '').concat(hasLateFee ? " + Late Fee: $".concat(PropertyService.getLateFeeAmount("apartment")) : '', ")")
        : "$".concat(PropertyService.getRentAmount("apartment"));
    return {
        hasApartment: true,
        rent: rentDisplay,
        daysUntilRent: daysUntilRent,
        landlord: PropertyService.getLandlordName("apartment"),
        debt: debt > 0 ? "$".concat(debt) : "-",
        hasLateFee: hasLateFee
    };
};
// Expose ApartmentService methods as global functions for Twine passages
var apartmentServiceExports = {
    rentApartment: function () {
        return ApartmentService.rentApartment();
    },
    payRent: function () {
        return ApartmentService.payRent();
    },
    skipRent: function () {
        return ApartmentService.skipRent();
    },
    alternativePayment: function () {
        ApartmentService.alternativePayment();
    },
    canAffordRent: function () {
        return ApartmentService.canAffordRent();
    },
    isRentDue: function () {
        return ApartmentService.isRentDue();
    },
    isLivingInApartment: function () {
        return ApartmentService.isLivingInApartment();
    },
    getDaysUntilRent: function () {
        return ApartmentService.getDaysUntilRent();
    },
    getRentAmount: function () {
        return ApartmentService.getRentAmount();
    },
    getLandlordName: function () {
        return ApartmentService.getLandlordName();
    },
    unrentApartment: function () {
        return ApartmentService.unrentApartment();
    }
};
window.ApartmentService = apartmentServiceExports;
// Create SugarCube macros for apartment actions
Macro.add("RentApartment", {
    handler: function () {
        ApartmentService.rentApartment();
    }
});
Macro.add("PayRent", {
    handler: function () {
        ApartmentService.payRent();
    }
});
Macro.add("SkipRent", {
    handler: function () {
        ApartmentService.skipRent();
    }
});
Macro.add("AlternativePayment", {
    handler: function () {
        ApartmentService.alternativePayment();
    }
});
Macro.add("UnrentApartment", {
    handler: function () {
        ApartmentService.unrentApartment();
    }
});
/* twine-user-script #37: "QuestController.js" */
"use strict";
window.isQuestActive = function (questKey) {
    return QuestService.isQuestActive(questKey);
};
window.isQuestCompleted = function (questKey) {
    return QuestService.isQuestCompleted(questKey);
};
window.isQuestAvailable = function (questKey) {
    return QuestService.isQuestAvailable(questKey);
};
window.getQuestProgress = function (questKey) {
    return galleryMode() ? 99 : QuestService.getQuestProgress(questKey);
};
window.getQuestDisplayTitle = function (questKey) {
    return QuestService.getQuestTitle(questKey);
};
window.getPinnedQuestKey = function () {
    return QuestService.getPinnedQuestKey();
};
window.getSidebarQuest = function () {
    return QuestService.getSidebarQuest();
};
window.togglePinnedQuest = function (questKey) {
    QuestService.togglePinnedQuest(questKey);
};
window.clearPinnedQuest = function () {
    QuestService.clearPinnedQuest();
};
window.isPinnedQuest = function (questKey) {
    return QuestService.isPinnedQuest(questKey);
};
// Helper functions for quest display
function getQuestIcon(quest) {
    if (quest.title.includes('School'))
        return '🎓';
    if (quest.title.includes('Game'))
        return '📱';
    if (quest.title.includes('Jim') || quest.title.includes('Richard') || quest.title.includes('Edward'))
        return '💕';
    if (quest.title.includes('Model'))
        return '📸';
    if (quest.title.includes('Father'))
        return '🧬';
    if (quest.title.includes('Math'))
        return '📐';
    if (quest.title.includes('Cheerleader'))
        return '🏆';
    return '📋';
}
function getQuestStatusIcon(quest) {
    if (quest.progress >= 100)
        return '✅';
    if (quest.progress >= 75)
        return '🔄';
    if (quest.progress >= 50)
        return '⏳';
    if (quest.progress >= 25)
        return '📝';
    return '🆕';
}
function updateQuestStats() {
    var questList = game().questList;
    var activeCount = questList.filter(function (quest) { return quest.active; }).length;
    var completedCount = questList.filter(function (quest) { return quest.completed; }).length;
    $('#active-count').text(activeCount);
    $('#completed-count').text(completedCount);
}
// Make functions globally accessible
window.updateQuestStats = updateQuestStats;
Macro.add('FinishQuest', {
    handler: function () {
        var questKey = this.args[0];
        QuestService.finishQuest(questKey);
    }
});
Macro.add('StartQuest', {
    handler: function () {
        var quest = this.args[0];
        QuestService.startQuest(quest);
    }
});
Macro.add('UpdateQuest', {
    handler: function () {
        var quest = this.args[0];
        var progress = this.args[1];
        var questDescription = this.args[2];
        QuestService.updateQuest(quest, progress, questDescription);
    }
});
Macro.add('CancelQuest', {
    handler: function () {
        var quest = this.args[0];
        var message = this.args[1];
        QuestService.cancelQuest(quest, message);
    }
});
Macro.add("ShowActiveQuests", {
    handler: function () {
        var activeQuests = game().questList.filter(function (quest) { return quest.active; });
        if (activeQuests.length === 0) {
            var emptyHtml = "\n                <div class=\"empty-state\">\n                    <div class=\"empty-state-icon\">\uD83C\uDFAF</div>\n                    <div class=\"empty-state-text\">No active quests</div>\n                </div>\n            ";
            $(this.output).append(emptyHtml);
            return;
        }
        for (var _i = 0, activeQuests_1 = activeQuests; _i < activeQuests_1.length; _i++) {
            var quest = activeQuests_1[_i];
            var titleWithSpaces = QuestService.getQuestTitle(quest.title);
            var icon = getQuestIcon(quest);
            var isPinned = QuestService.isPinnedQuest(quest.title);
            var questHtml = "\n                <div class=\"quest-card\" data-quest-id=\"".concat(quest.id, "\">\n                    <div class=\"quest-card-header\">\n                        <h3 class=\"quest-title-text\">").concat(icon, " ").concat(titleWithSpaces, "</h3>\n                        <span class=\"quest-icon-badge\">").concat(getQuestStatusIcon(quest), "</span>\n                    </div>\n                    <p class=\"quest-description\">").concat(quest.description, "</p>\n                    <div class=\"quest-meta\">\n                        ").concat(quest.repeatable ? '<span class="quest-tag repeatable">Repeatable</span>' : '', "\n                    </div>\n                    <div class=\"quest-actions\">\n                        <button\n                            type=\"button\"\n                            class=\"quest-pin-button ").concat(isPinned ? 'is-pinned' : '', "\"\n                            data-quest-key=\"").concat(quest.title, "\"\n                            onclick=\"event.stopPropagation(); QuestUIController.toggleQuestPin('").concat(quest.title, "')\"\n                        >\n                            ").concat(isPinned ? '📌 Pinned in Sidebar' : '📍 Pin to Sidebar', "\n                        </button>\n                    </div>\n                </div>\n            ");
            $(this.output).append(questHtml);
        }
        // Update stats and initialize UI
        updateQuestStats();
        // Initialize UI controller after quests are rendered
        setTimeout(function () {
            if (window.QuestUIController) {
                window.QuestUIController.initialize();
            }
        }, 50);
    }
});
Macro.add("ShowCompletedQuests", {
    handler: function () {
        var completedQuests = game().questList.filter(function (quest) { return quest.completed; });
        if (completedQuests.length === 0) {
            var emptyHtml = "\n                <div class=\"empty-state\">\n                    <div class=\"empty-state-icon\">\uD83C\uDFC6</div>\n                    <div class=\"empty-state-text\">No completed quests yet</div>\n                </div>\n            ";
            $(this.output).append(emptyHtml);
            return;
        }
        for (var _i = 0, completedQuests_1 = completedQuests; _i < completedQuests_1.length; _i++) {
            var quest = completedQuests_1[_i];
            var titleWithSpaces = QuestService.getQuestTitle(quest.title);
            var icon = getQuestIcon(quest);
            var questHtml = "\n                <div class=\"quest-card completed\" data-quest-id=\"".concat(quest.id, "\">\n                    <div class=\"quest-card-header\">\n                        <h3 class=\"quest-title-text\">").concat(icon, " ").concat(titleWithSpaces, "</h3>\n                        <span class=\"quest-icon-badge\">\u2705</span>\n                    </div>\n                    <p class=\"quest-description\">").concat(quest.description, "</p>\n                    <div class=\"quest-meta\">\n                        ").concat(quest.repeatable ? '<span class="quest-tag repeatable">Repeatable</span>' : '', "\n                        <span class=\"quest-tag completed\">Completed</span>\n                    </div>\n                </div>\n            ");
            $(this.output).append(questHtml);
        }
    }
});
Macro.add("ScheduleQuest", {
    handler: function () {
        if (galleryMode()) {
            return;
        }
        var questKey = this.args[0];
        var delayDays = parseInt(this.args[1], 10) || 0;
        QuestService.scheduleQuest(questKey, delayDays);
    }
});
/* twine-user-script #38: "QuestUIController.js" */
"use strict";
var QuestUIController = /** @class */ (function () {
    function QuestUIController() {
    }
    /**
     * Initialize the quest UI controller
     */
    QuestUIController.initialize = function () {
        var _this = this;
        this.setupKeyboardNavigation();
        this.updateQuestStats();
        this.syncPinButtons();
        // Add click animations to quest cards
        setTimeout(function () {
            _this.addQuestCardAnimations();
        }, 100);
    };
    /**
     * Switch between active and completed quest tabs
     */
    QuestUIController.switchTab = function (tabName) {
        if (tabName === this.currentTab)
            return;
        // Remove active class from all buttons and contents
        var tabButtons = document.querySelectorAll('.tab-button');
        var tabContents = document.querySelectorAll('.tab-content');
        tabButtons.forEach(function (btn) { return btn.classList.remove('active'); });
        tabContents.forEach(function (content) { return content.classList.remove('active'); });
        // Add active class to clicked button and corresponding content
        var activeButton = document.querySelector("[data-tab=\"".concat(tabName, "\"]"));
        var activeContent = document.getElementById("".concat(tabName, "-tab"));
        if (activeButton && activeContent) {
            activeButton.classList.add('active');
            activeContent.classList.add('active');
            this.currentTab = tabName;
            // Update stats when switching tabs
            this.updateQuestStats();
        }
    };
    /**
     * Update quest statistics display (delegates to QuestController)
     */
    QuestUIController.updateQuestStats = function () {
        // Delegate to QuestController which has the reliable data source
        if (window.updateQuestStats) {
            window.updateQuestStats();
        }
    };
    QuestUIController.toggleQuestPin = function (questKey) {
        QuestService.togglePinnedQuest(questKey);
        this.syncPinButtons();
        if (typeof updateRight === 'function') {
            updateRight();
        }
    };
    /**
     * Animate number changes
     */
    QuestUIController.animateNumber = function (element, start, end, duration) {
        var startTime = performance.now();
        var animate = function (currentTime) {
            var elapsed = currentTime - startTime;
            var progress = Math.min(elapsed / duration, 1);
            var current = Math.floor(progress * (end - start) + start);
            element.textContent = current.toString();
            if (progress < 1) {
                requestAnimationFrame(animate);
            }
        };
        requestAnimationFrame(animate);
    };
    /**
     * Setup keyboard navigation
     */
    QuestUIController.setupKeyboardNavigation = function () {
        var _this = this;
        // Remove existing listener if any
        if (this.keyboardListener) {
            document.removeEventListener('keydown', this.keyboardListener);
        }
        this.keyboardListener = function (e) {
            if (e.key === 'Escape') {
                _this.closeModal();
            }
            else if (e.key === 'Tab') {
                e.preventDefault();
                // Cycle through tabs with Tab key
                var nextTab = _this.currentTab === 'active' ? 'completed' : 'active';
                _this.switchTab(nextTab);
            }
        };
        document.addEventListener('keydown', this.keyboardListener);
    };
    /**
     * Add click animations to quest cards
     */
    QuestUIController.addQuestCardAnimations = function () {
        var questCards = document.querySelectorAll('.quest-card');
        questCards.forEach(function (card) {
            card.addEventListener('click', function () {
                var _this = this;
                this.style.transform = 'scale(0.98)';
                setTimeout(function () {
                    _this.style.transform = '';
                }, 150);
            });
        });
    };
    QuestUIController.syncPinButtons = function () {
        var pinnedQuestKey = QuestService.getPinnedQuestKey();
        var pinButtons = document.querySelectorAll('.quest-pin-button');
        pinButtons.forEach(function (button) {
            var questKey = button.dataset.questKey || "";
            var isPinned = questKey !== "" && questKey === pinnedQuestKey;
            button.classList.toggle('is-pinned', isPinned);
            button.textContent = isPinned ? '📌 Pinned in Sidebar' : '📍 Pin to Sidebar';
        });
    };
    /**
     * Close the quest modal
     */
    QuestUIController.closeModal = function () {
        // Cleanup UI
        this.cleanup();
        // Cleanup quest service
        QuestService.cleanupQuestUI();
        window.closeDialog('questbook');
    };
    /**
     * Cleanup when modal is closed
     */
    QuestUIController.cleanup = function () {
        if (this.keyboardListener) {
            document.removeEventListener('keydown', this.keyboardListener);
            this.keyboardListener = null;
        }
    };
    QuestUIController.currentTab = 'active';
    QuestUIController.keyboardListener = null;
    return QuestUIController;
}());
// Make QuestUIController available globally
window.QuestUIController = QuestUIController;
/* twine-user-script #39: "SceneController.js" */
"use strict";
Macro.add('UnlockNPCScene', {
    handler: function () {
        var npc = this.args[0];
        var scene = this.args[1];
        if (!galleryMode()) {
            SceneService.unlockNpcScene(npc, scene);
        }
    }
});
Macro.add('UnlockLocationScene', {
    handler: function () {
        var location = this.args[0];
        var scene = this.args[1];
        if (!galleryMode()) {
            if (!location || !scene) {
                var msg = "UnlockLocationScene: Location or scene argument is missing. Location: ".concat(location, ", Scene: ").concat(scene);
                throw new Error(msg);
            }
            SceneService.unlockLocationScene(location, scene);
        }
    }
});
Macro.add('UnlockMCScene', {
    handler: function () {
        var scene = this.args[0];
        if (!galleryMode()) {
            if (!scene) {
                var msg = "UnlockMCScene: Scene argument is missing. Scene: ".concat(scene);
                throw new Error(msg);
            }
            SceneService.unlockMCScene(scene);
        }
    }
});
window.checkSceneReq = function (sceneKey) {
    // Try to find the scene in location scenes first
    var locations = game().location;
    for (var locationKey in locations) {
        var location_1 = locations[locationKey];
        if (location_1.scenes && location_1.scenes[sceneKey]) {
            return SceneService.CheckSceneReq(location_1.scenes[sceneKey]);
        }
    }
    // Try to find in NPC scenes
    var npcs = game().npc;
    for (var npcKey in npcs) {
        var npc = npcs[npcKey];
        if (npc.scenes && npc.scenes[sceneKey]) {
            return SceneService.CheckSceneReq(npc.scenes[sceneKey]);
        }
    }
    // Try to find in player scenes
    if (game().player.scenes && game().player.scenes[sceneKey]) {
        return SceneService.CheckSceneReq(game().player.scenes[sceneKey]);
    }
    // Scene not found
    createNotification("Scene '".concat(sceneKey, "' not found!"), NotificationType.WARNING);
    return false;
};
window.isNpcSceneUnlocked = function (npc, scene) {
    return SceneService.isNpcSceneUnlocked(npc, scene);
};
window.isLocationSceneUnlocked = function (location, scene) {
    var _a, _b, _c;
    if (!((_c = (_b = (_a = game().location) === null || _a === void 0 ? void 0 : _a[location]) === null || _b === void 0 ? void 0 : _b.scenes) === null || _c === void 0 ? void 0 : _c[scene])) {
        var msg = "isLocationSceneUnlocked: Scene ".concat(scene, " does not exist in location ").concat(location, ".");
        throw new Error(msg);
    }
    var locationScene = game().location[location].scenes[scene];
    return locationScene.unlocked;
};
window.isSceneExecutedToday = function (scene) {
    return SceneService.isSceneExecutedToday(scene);
};
/* twine-user-script #40: "PhoneController.js" */
"use strict";
Macro.add('NotifyPhone', {
    handler: function () {
        PhoneService.showNotification(this.args[0]);
    }
});
Macro.add('NewMessage', {
    handler: function () {
        PhoneService.newMessage(this.args[0]);
    }
});
Macro.add('RenderPhoneMessage', {
    handler: function () {
        var messageId = this.args[0];
        var templateId = PhoneService.getMessageTemplateId(messageId);
        var widgetName = templateId + "Message";
        $(this.output).wiki('<<' + widgetName + ' "' + messageId + '">>');
    }
});
Macro.add('RefreshMessages', {
    handler: function () {
        $('#phone-screen').empty().wiki(Story.get('Messages').processText());
    }
});
window.findPhoneThread = function (threadId) {
    return threadId ? PhoneService.findThread(threadId) : undefined;
};
window.getUnreadPhoneThreadCount = function () {
    return PhoneService.getUnreadThreadCount();
};
window.selectPhoneThread = function (threadId) {
    PhoneService.selectThread(threadId);
};
window.clearSelectedPhoneThread = function () {
    PhoneService.clearSelectedThread();
};
window.resetPhoneUi = function () {
    PhoneService.clearSelectedThread();
    $("#phone-screen").empty().wiki(Story.get("PhoneHome").processText());
    $("#phone-top").empty().wiki(Story.get("PhoneTop").processText());
};
window.getPhoneThreadButtonLabel = function (threadId) {
    return threadId ? PhoneService.getThreadButtonLabel(threadId) : "";
};
window.getPhoneThreadActionLabel = function (actionId) {
    return actionId ? PhoneService.getThreadActionLabel(actionId) : "";
};
window.getPhoneThreadActions = function (threadId) {
    return threadId ? PhoneService.getThreadActions(threadId) : [];
};
window.getPhoneThreadTimeline = function (threadId) {
    return threadId ? PhoneService.getThreadTimeline(threadId) : [];
};
window.sendPhoneThreadAction = function (threadId, actionId) {
    PhoneService.sendThreadAction(threadId, actionId);
};
/* twine-user-script #41: "FastJobsController.js" */
"use strict";
Macro.add("StartFastJob", {
    handler: function () {
        var jobId = this.args[0];
        FastJobsService.startFastJob(jobId);
    }
});
Macro.add("FinishFastJob", {
    handler: function () {
        var jobName = this.args[0];
        if (!galleryMode()) {
            FastJobsService.finishFastJob(jobName);
        }
    }
});
/* twine-user-script #42: "NakedLifeController.js" */
"use strict";
Macro.add("AcceptNakedLifeChallenge", {
    handler: function () {
        var nakedLifeId = this.args[0];
        NakedLifeService.startNakedLifeChallenge(nakedLifeId);
    }
});
Macro.add("CompleteNakedLifeChallenge", {
    handler: function () {
        var nakedLifeScene = this.args[0];
        if (galleryMode())
            return;
        NakedLifeService.completeNakedLifeChallenge(nakedLifeScene);
    }
});
Macro.add("AddNakedLifeXp", {
    handler: function () {
        var xp = parseInt(this.args[0]);
        NakedLifeService.addExp(xp);
    }
});
window.getProgressToNextRank = function () {
    return NakedLifeService.getProgressToNextRank();
};
window.isChallengeActive = function (scene) {
    var _a;
    try {
        return ((_a = NakedLifeService.getNakedLifeChallengeByScene(scene)) === null || _a === void 0 ? void 0 : _a.active) || false;
    }
    catch (error) {
        console.error("Error checking challenge activity:", error);
        return false;
    }
};
/* twine-user-script #43: "TimeController.js" */
"use strict";
Macro.add('TimeController', {
    handler: function () {
        TimeService.updateGameTime();
    }
});
Macro.add('NewDay', {
    handler: function () {
        TimeService.newDay();
    }
});
Macro.add('AddTime', {
    handler: function () {
        if (galleryMode())
            return;
        var timeCount = this.args[0];
        TimeService.addTime(timeCount);
    }
});
Macro.add('GetDayPeriodName', {
    handler: function () {
        var timeEnum = this.args[0];
        return TimeService.getDayPeriodByEnum(timeEnum);
    }
});
window.getDayPeriodName = function (timeEnum) {
    return TimeService.getDayPeriodByEnum(timeEnum);
};
window.getTime = function () {
    return TimeService.getTime();
};
window.getDay = function () {
    return TimeService.getDay();
};
/* twine-user-script #44: "WeatherController.js" */
"use strict";
Macro.add('WeatherController', {
    handler: function () {
        WeatherService.updateWeatherUI();
    }
});
/* twine-user-script #45: "game.model.js" */
"use strict";
var NotificationType;
(function (NotificationType) {
    NotificationType["WARNING"] = "warning";
    NotificationType["INFO"] = "info";
    NotificationType["MONEY"] = "money";
    NotificationType["SUCCESS"] = "success";
    NotificationType["ALERT"] = "alert";
    NotificationType["EXB"] = "exb";
    NotificationType["CORRUPTION"] = "corruption";
    NotificationType["INT"] = "int";
    NotificationType["FITNESS"] = "fitness";
    NotificationType["SOCIAL"] = "social";
    NotificationType["ERROR"] = "error";
    NotificationType["BEAUTY"] = "beauty";
    NotificationType["LOVE"] = "love";
})(NotificationType || (NotificationType = {}));
/* twine-user-script #46: "item.model.js" */
"use strict";
var ItemType;
(function (ItemType) {
    ItemType["Electronics"] = "electronics";
    ItemType["Drugs"] = "drugs";
    ItemType["Gym"] = "gym";
    ItemType["Health"] = "health";
    ItemType["Object"] = "object";
})(ItemType || (ItemType = {}));
/* twine-user-script #47: "location.model.js" */
"use strict";
var masterLocationConfig = [
    {
        name: "center", passage: "Center", title: "City Center", area: "Zone", unlocked: true, imgPath: "/citymap/center/citybanner.webp",
        check: function () {
            var result = {
                success: true
            };
            var clothingType = player().clothing.type;
            if (clothingType === ClothType.Underwear ||
                clothingType === ClothType.Swim ||
                clothingType === ClothType.Uniform) {
                result = {
                    success: false,
                    clothingType: ClothType.Casual,
                };
            }
            return result;
        },
        action: function () {
            LocationService.setPlayerLocation('Center');
            Engine.play('Center');
        }
    },
    {
        name: "residential", passage: "Residential", title: "Residential", area: "Zone", unlocked: true, imgPath: "/citymap/residential/residentialbanner.webp",
        action: function () {
            if (player().clothing.type === ClothType.Underwear) {
                return 'clothing';
            }
            LocationService.setPlayerLocation('Residential');
            Engine.play('Residential');
        }
    },
    {
        name: "elite", passage: "Elite", title: "Elite District", area: "Zone", unlocked: true, imgPath: "/citymap/elite/elitebanner.webp",
        action: function () {
            if (player().clothing.type === ClothType.Underwear) {
                return 'clothing';
            }
            LocationService.setPlayerLocation('Elite');
            Engine.play('Elite');
        }
    },
    {
        name: "ghetto", passage: "Ghetto", title: "Ghetto", area: "Zone", unlocked: true, imgPath: "/citymap/ghetto/ghettobanner.webp",
        action: function () {
            if (player().clothing.type === ClothType.Underwear) {
                return 'clothing';
            }
            LocationService.setPlayerLocation('Ghetto');
            Engine.play('Ghetto');
        }
    },
    {
        name: "house", passage: "Hallway", title: "House", area: "Residential", unlocked: true, imgPath: "/house/housebanner.webp",
        action: function () {
            LocationService.setPlayerLocation('House');
            Engine.play('Hallway');
        }
    },
    {
        name: "busStop", passage: "BusStop", title: "Bus Stop", area: "*", unlocked: true, imgPath: "/bus/busStopbanner.webp",
        action: function () {
            LocationService.setPlayerLocation('BusStop');
            Engine.play('BusStop');
        }
    },
    {
        name: "bus", passage: "Bus", title: "Bus", area: "Bus", unlocked: true, imgPath: "",
        action: function () {
            LocationService.setPlayerLocation('Bus');
            Engine.play('Bus');
        }
    },
    {
        name: "photoStudio", passage: "PhotoStudio", title: "Photo Studio", area: "Center", unlocked: false, imgPath: "/photoStudio/banner.webp",
        openPeriods: ["EM", "M", "A", "E"],
        action: function () {
            LocationService.setPlayerLocation('PhotoStudio');
            Engine.play('PhotoStudio');
        }
    },
    {
        name: "school", passage: "School", title: "School", area: "Residential", unlocked: true, imgPath: "/school/schoolbanner.webp",
        openPeriods: ["EM", "M", "A", "E"],
        check: function () {
            var school = game().location.school;
            var clothingType = game().player.clothing.type;
            var result = {
                success: false
            };
            if (school === null || school === void 0 ? void 0 : school.graduated) {
                result.success = false;
                result.message = "You have already graduated! You no longer need to attend school.";
                return result;
            }
            if (clothingType === ClothType.School || clothingType === ClothType.SchoolCheerleader) {
                result.success = true;
            }
            else {
                result.success = false;
                result.clothingType = ClothType.School;
            }
            return result;
        },
        action: function () {
            LocationService.setPlayerLocation('School');
            Engine.play('School');
        }
    },
    {
        name: "park", passage: "Park", title: "Park", area: "Residential", unlocked: true, imgPath: "/park/parkbanner.webp",
        openPeriods: ["EM", "M", "A", "E", "N"],
        action: function () {
            var scene = LocationService.checkLocationOpen('park') ? 'Park' : 'ParkLateNight';
            LocationService.setPlayerLocation(scene);
            Engine.play(scene);
        }
    },
    {
        name: "marcusHouse", passage: "MarcusHallway", title: "Marcus's House", area: "Residential", unlocked: false, imgPath: "/marcus/house/house.webp",
        openPeriods: ["A", "E"],
        action: function () {
            LocationService.setPlayerLocation('MarcusHouse');
            Engine.play('MarcusHallway');
        }
    },
    {
        name: "emmaHouse", passage: "EmmaHallway", title: "Emma's House", area: "Residential", unlocked: false, imgPath: "/emma/house/housebanner.webp",
        openPeriods: ["E"],
        action: function () {
            LocationService.setPlayerLocation('EmmaHouse');
            Engine.play('EmmaHallway');
        }
    },
    {
        name: "gym", passage: "Gym", title: "Gym", area: "Center", unlocked: true, imgPath: "/gym/gymbanner.webp",
        openPeriods: ["EM", "M", "A", "E", "N"],
        action: function () {
            LocationService.setPlayerLocation('Gym');
            Engine.play('Gym');
        }
    },
    {
        name: "mall", passage: "Mall", title: "Mall", area: "Center", unlocked: true, imgPath: "/shopping/shoppingbanner.webp",
        openPeriods: ["EM", "M", "A", "E", "N"],
        action: function () {
            LocationService.setPlayerLocation('Mall');
            Engine.play('Mall');
        }
    },
    {
        name: "club", passage: "Club", title: "Night Club", area: "Center", unlocked: true, imgPath: "/club/clubbanner.webp",
        openPeriods: ["N", "LN"],
        action: function () {
            LocationService.setPlayerLocation('Club');
            Engine.play('Club');
        }
    },
    {
        name: "beach", passage: "Beach", title: "Beach", area: "Center", unlocked: true, imgPath: "/beach/beachbanner.webp",
        openPeriods: ["EM", "M", "A", "E", "N"],
        action: function () {
            var scene = LocationService.checkLocationOpen('beach') ? 'Beach' : 'BeachNight';
            LocationService.setPlayerLocation(scene);
            Engine.play(scene);
        }
    },
    {
        name: "bar", passage: "Bar", title: "Bar", area: "Center", unlocked: true, imgPath: "/bar/barbanner.webp",
        openPeriods: ["E", "N", "LN"],
        action: function () {
            LocationService.setPlayerLocation('Bar');
            Engine.play('Bar');
        }
    },
    {
        name: "pool", passage: "Pool", title: "Public Pool ", area: "Center", unlocked: true, imgPath: "/pool/poolbanner.webp",
        openPeriods: ["EM", "M", "A", "E"],
        action: function () {
            LocationService.setPlayerLocation('Pool');
            Engine.play('Pool');
        }
    },
    {
        name: "office", passage: "Office", title: "Office", area: "Center", unlocked: true, imgPath: "/office/officebanner.webp",
        openPeriods: ["EM", "M", "A"],
        action: function () {
            LocationService.setPlayerLocation('Office');
            Engine.play('Office');
        }
    },
    {
        name: "bank", passage: "Bank", title: "Bank", area: "Center", unlocked: true, imgPath: "/bank/bankbanner.webp",
        openPeriods: ["EM", "M", "A"],
        action: function () {
            LocationService.setPlayerLocation('Bank');
            Engine.play('Bank');
        }
    },
    {
        name: "drivingSchool", passage: "DrivingSchool", title: "Driving School", area: "Center", unlocked: true, imgPath: "/drivingSchool/drivingschoolbanner.webp",
        openPeriods: ["EM", "M", "A"],
        action: function () {
            LocationService.setPlayerLocation('DrivingSchool');
            Engine.play('DrivingSchool');
        }
    },
    {
        name: "jamalHouse", passage: "JamalHallway", title: "Jamal's House", area: "Elite", unlocked: false, imgPath: "/jamal/house/house.webp",
        openPeriods: ["EM", "M", "A", "E", "N"],
        action: function () {
            LocationService.setPlayerLocation('JamalHouse');
            Engine.play('JamalHallway');
        }
    },
    {
        name: "veronicaHouse", passage: "VeronicaHallway", title: "Veronica's House", area: "Elite", unlocked: false, imgPath: "/veronica/house/house.webp",
        openPeriods: ["E", "N"],
        action: function () {
            LocationService.setPlayerLocation('VeronicaHouse');
            Engine.play('VeronicaHallway');
        }
    },
    {
        name: "thomasHouse", passage: "ThomasHallway", title: "Thomas's House", area: "Elite", unlocked: false, imgPath: "/thomas/house/house.webp",
        openPeriods: ["EM", "M", "A", "E", "N", "LN"],
        action: function () {
            LocationService.setPlayerLocation('ThomasHouse');
            Engine.play('ThomasHallway');
        }
    },
    {
        name: "church", passage: "Church", title: "Church", area: "Ghetto", unlocked: true, imgPath: "/church/churchbanner.webp",
        openPeriods: ["M", "A", "E", "N"],
        action: function () {
            LocationService.setPlayerLocation('Church');
            Engine.play('Church');
        }
    },
    {
        name: "stripclub", passage: "Stripclub", title: "Strip Club", area: "Ghetto", unlocked: true, imgPath: "/stripclub/stripclubbanner.webp",
        openPeriods: ["E", "N", "LN"],
        action: function () {
            LocationService.setPlayerLocation('StripClub');
            Engine.play('StripClub');
        }
    },
    {
        name: "clandestineClinic", passage: "ClandestineClinic", title: "Clandestine Clinic", area: "Ghetto", unlocked: false, imgPath: "/clandestineClinic/clandestinebanner.webp",
        openPeriods: ["E", "N"],
        action: function () {
            LocationService.setPlayerLocation('ClandestineClinic');
            Engine.play('ClandestineClinic');
        }
    },
    {
        name: "restaurant", passage: "Restaurant", title: "Restaurant", area: "Center", unlocked: true, imgPath: "/restaurant/restaurantbanner.webp",
        openPeriods: ["EM", "M", "A", "E"],
        action: function () {
            LocationService.setPlayerLocation('Restaurant');
            Engine.play('Restaurant');
        },
    },
    {
        name: "darkAlley", passage: "DarkAlley", title: "Dark Alley", area: "Ghetto", unlocked: true, imgPath: "/darkalley/darkAlleybanner.webp",
        action: function () {
            LocationService.setPlayerLocation('DarkAlley');
            Engine.play('DarkAlley');
        },
    },
    {
        name: "vipers", passage: "Vipers", title: "The Vipers", area: "Ghetto", unlocked: false, imgPath: "/vipers/vipersbanner.webp",
        action: function () {
            LocationService.setPlayerLocation('Vipers');
            Engine.play('Vipers');
        },
    },
    {
        name: "policeDep", passage: "PoliceStation", title: "Police Station", area: "Center", unlocked: true, imgPath: "/policedep/policebanner.webp",
        action: function () {
            LocationService.setPlayerLocation('PoliceStation');
            Engine.play('PoliceStation');
        },
    },
    {
        name: "hospital", passage: "Hospital", title: "Hospital", area: "Center", unlocked: true, imgPath: "/hospital/hospitalbanner.webp",
        action: function () {
            LocationService.setPlayerLocation('Hospital');
            Engine.play('Hospital');
        },
    },
    {
        name: "abandonedBuilding", passage: "AbandonedBuilding", title: "Abandoned Building", area: "Ghetto", unlocked: true, imgPath: "/abandonedBuilding/abandonedbuildingbanner.webp",
        action: function () {
            LocationService.setPlayerLocation('AbandonedBuilding');
            Engine.play('AbandonedBuilding');
        },
    },
    {
        name: "hotel", passage: "Hotel", title: "Hotel", area: "Center", unlocked: false, imgPath: "/hotel/hotelbanner.webp",
        action: function () {
            LocationService.setPlayerLocation('Hotel');
            Engine.play('Hotel');
        },
    },
    {
        name: "laundry", passage: "Laundry", title: "Laundry", area: "Ghetto", unlocked: true, imgPath: "/laundry/laundrybanner.webp",
        openPeriods: ["EM", "M", "A", "E", "N"],
        action: function () {
            LocationService.setPlayerLocation('Laundry');
            Engine.play('Laundry');
        }
    },
    {
        name: "gasStation", passage: "GasStation", title: "Gas Station", area: "Center", unlocked: true, imgPath: "/gasStation/gasstationbanner.webp",
        action: function () {
            LocationService.setPlayerLocation('GasStation');
            Engine.play('GasStation');
        }
    },
    {
        name: "streetChallenge1", passage: "StreetChallenge1", title: "Street Challenge 1", area: "Center", unlocked: false, imgPath: "/events/streetChallenge1/streetChallenge1.webp",
        action: function () {
            LocationService.setPlayerLocation('StreetChallenge1');
            Engine.play('StreetChallenge1');
        }
    },
    {
        name: "Casino", passage: "Casino", title: "Casino", area: "Elite", unlocked: true, imgPath: "/casino/casinobanner.webp",
        openPeriods: ["E", "N", "LN"],
        action: function () {
            LocationService.setPlayerLocation('Casino');
            Engine.play('Casino');
        }
    },
    {
        name: "movieTheater", passage: "MovieTheater", title: "Movie Theater", area: "Center", unlocked: true, imgPath: "/movieTheater/movieTheaterbanner.webp",
        openPeriods: ["M", "A", "E", "N"],
        action: function () {
            LocationService.setPlayerLocation('MovieTheater');
            Engine.play('MovieTheater');
        }
    },
    {
        name: "apartment", passage: "ApartmentRent", title: "Apartment", area: "Residential", unlocked: true, imgPath: "/apartment/apartmentbanner.webp",
        action: function () {
            if (PropertyService.hasProperty("apartment")) {
                LocationService.setPlayerLocation('Apartment');
                Engine.play('ApartmentHall');
            }
            else {
                Engine.play('ApartmentRent');
            }
        }
    }
];
/* twine-user-script #48: "npc.model.js" */
"use strict";
var Gender;
(function (Gender) {
    Gender["Male"] = "Male";
    Gender["Female"] = "Female";
    Gender["Transgender"] = "Transgender";
    Gender["Other"] = "Other";
})(Gender || (Gender = {}));
/* twine-user-script #49: "baby.model.js" */
"use strict";
/* twine-user-script #50: "bank.model.js" */
"use strict";
/* twine-user-script #51: "cloth.model.js" */
"use strict";
var ClothType;
(function (ClothType) {
    ClothType["Underwear"] = "underwear";
    ClothType["Casual"] = "casual";
    ClothType["School"] = "school";
    ClothType["SchoolCheerleader"] = "schoolCheerleader";
    ClothType["Fitness"] = "fitness";
    ClothType["Swim"] = "swim";
    ClothType["Uniform"] = "uniform";
    ClothType["Costume"] = "costume";
})(ClothType || (ClothType = {}));
/* twine-user-script #52: "corruption.model.js" */
"use strict";
/* twine-user-script #53: "drug.model.js" */
"use strict";
var DrugType;
(function (DrugType) {
    DrugType["Weed"] = "weed";
    DrugType["Cocaine"] = "cocaine";
    DrugType["Heroin"] = "heroin";
})(DrugType || (DrugType = {}));
/* twine-user-script #54: "gang.model.js" */
"use strict";
/* twine-user-script #55: "inventory.model.js" */
"use strict";
/* twine-user-script #56: "jobs.model.js" */
"use strict";
var Jobs;
(function (Jobs) {
    Jobs["Waiter"] = "Waiter";
    Jobs["Secretary"] = "Secretary";
    Jobs["Bartender"] = "Bartender";
    Jobs["Stripper"] = "Stripper";
})(Jobs || (Jobs = {}));
/* twine-user-script #57: "player.model.js" */
"use strict";
/* twine-user-script #58: "pregnancy.model.js" */
"use strict";
/* twine-user-script #59: "property.model.js" */
"use strict";
/**
 * Property ownership type
 */
var PropertyType;
(function (PropertyType) {
    PropertyType["Rent"] = "rent";
    PropertyType["Buy"] = "buy";
})(PropertyType || (PropertyType = {}));
/**
 * Property status
 */
var PropertyStatus;
(function (PropertyStatus) {
    PropertyStatus["Available"] = "available";
    PropertyStatus["Rented"] = "rented";
    PropertyStatus["Owned"] = "owned";
})(PropertyStatus || (PropertyStatus = {}));
/* twine-user-script #60: "quest.model.js" */
"use strict";
/* twine-user-script #61: "scene.model.js" */
"use strict";
/* twine-user-script #62: "xcam.model.js" */
"use strict";
/* twine-user-script #63: "fastJobs.model.js" */
"use strict";
var FastJobType;
(function (FastJobType) {
    FastJobType["Cleaning"] = "cleaning";
    FastJobType["BabySitting"] = "babySitting";
    FastJobType["PetCare"] = "petCare";
    FastJobType["ElderlyCare"] = "elderlyCare";
})(FastJobType || (FastJobType = {}));
/* twine-user-script #64: "instafame.model.js" */
"use strict";
var SelfieType;
(function (SelfieType) {
    SelfieType["Normal"] = "normal";
    SelfieType["Lewd"] = "lewd";
    SelfieType["Nude"] = "nude";
})(SelfieType || (SelfieType = {}));
/* twine-user-script #65: "nakedlife.model.js" */
"use strict";
var NakedLifeRank;
(function (NakedLifeRank) {
    NakedLifeRank["Newbie"] = "Newbie";
    NakedLifeRank["Exhibitionist"] = "Exhibitionist";
    NakedLifeRank["Shameless"] = "Shameless";
    NakedLifeRank["Legend"] = "Legend";
})(NakedLifeRank || (NakedLifeRank = {}));
/* twine-user-script #66: "phone.model.js" */
"use strict";
/* twine-user-script #67: "pornCenter.model.js" */
"use strict";
/* twine-user-script #68: "time.model.js" */
"use strict";
var DayPeriod;
(function (DayPeriod) {
    DayPeriod["EarlyMorning"] = "EM";
    DayPeriod["Morning"] = "M";
    DayPeriod["Afternoon"] = "A";
    DayPeriod["Evening"] = "E";
    DayPeriod["Night"] = "N";
    DayPeriod["LateNight"] = "LN";
})(DayPeriod || (DayPeriod = {}));
/* twine-user-script #69: "EngineService.js" */
"use strict";
window.Init = function (importSave) {
    DevService.initDev();
    GameService.initGame();
    WeatherService.initWeather();
    TimeService.initTime();
    ItemService.initItems();
    PropertyService.initProperties();
    LocationService.initLocations();
    PlayerService.initPlayer();
    NpcService.initNpc();
    QuestService.initQuests();
    SchoolService.initSchool();
    DrivingSchoolService.initDrivingSchool();
    SceneService.initScenes();
    ClothService.initClothes();
    TimeService.updateGameTime();
    WeatherService.updateWeatherUI();
    createRandomEventModal();
    SaveModalService.init();
    checkVersion();
    PassageHeaderEnhancer.init();
    if (importSave) {
        game().game.saveVersion = window.gameVersion;
        createNotification("Save imported successfully", NotificationType.SUCCESS);
    }
    var mobileVersion = /Mobi|Android/i.test(navigator.userAgent);
    if (mobileVersion) {
        toggleRightBar();
        UIBar.stow();
        UIBar.hide();
    }
};
/* twine-user-script #70: "SaveModalService.js" */
"use strict";
/**
 * SaveModalService - Complete modal for managing saves
 * Includes save, load, delete, export and import functionality
 */
var SaveModalService = /** @class */ (function () {
    function SaveModalService() {
    }
    SaveModalService.isValidImportFile = function (fileName) {
        return this.validImportFileExtensions.some(function (extension) { return fileName.endsWith(extension); });
    };
    SaveModalService.isBundleImportFile = function (fileName) {
        return fileName.endsWith('.savesbundle') || fileName.endsWith('.savesbundle.txt');
    };
    SaveModalService.getImportFileType = function (fileName) {
        return this.isBundleImportFile(fileName) ? 'bundle' : 'save';
    };
    /**
     * Initialize the save modal
     */
    SaveModalService.init = function () {
        this.createModal();
        this.attachEventListeners();
    };
    /**
     * Create the modal HTML
     */
    SaveModalService.createModal = function () {
        var modalHtml = "\n            <div id=\"saveModalOverlay\" class=\"save-modal-overlay\">\n                <div id=\"saveModal\" class=\"save-modal\">\n                    <div class=\"save-modal-header\">\n                        <h2>\uD83D\uDCBE Save Manager</h2>\n                        <button id=\"closeSaveModal\" class=\"close-button\">\u2715</button>\n                    </div>\n                    \n                    <div class=\"save-modal-content\">\n                        <!-- Save/Load Section -->\n                        <div class=\"save-section\">\n                            <h3>\uD83D\uDCBE Save & Load Game</h3>\n                            \n                            <!-- Save Controls -->\n                            <div class=\"save-controls\">\n                                <div class=\"save-inputs\">\n                                    <div class=\"save-input-group\">\n                                        <label for=\"save-description\">Description:</label>\n                                        <input type=\"text\" id=\"save-description\" placeholder=\"Enter save description...\" maxlength=\"50\">\n                                    </div>\n                                    <div class=\"save-input-group\">\n                                        <label for=\"save-slot\">Slot:</label>\n                                        <select id=\"save-slot\">\n                                            <option value=\"0\">Slot 1</option>\n                                            <option value=\"1\">Slot 2</option>\n                                            <option value=\"2\">Slot 3</option>\n                                            <option value=\"3\">Slot 4</option>\n                                            <option value=\"4\">Slot 5</option>\n                                            <option value=\"5\">Slot 6</option>\n                                            <option value=\"6\">Slot 7</option>\n                                            <option value=\"7\">Slot 8</option>\n                                        </select>\n                                    </div>\n                                </div>\n                                <div class=\"save-actions\">\n                                    <button id=\"save-game-button\" class=\"action-button primary\">\n                                        \uD83D\uDCBE Save Game\n                                    </button>\n                                    <button id=\"continue-button\" class=\"action-button secondary\" disabled>\n                                        \u25B6\uFE0F Continue Latest\n                                    </button>\n                                </div>\n                            </div>\n\n                            <!-- Saves List -->\n                            <div class=\"saves-grid\">\n                                <div class=\"saves-column\">\n                                    <h4>Auto Saves</h4>\n                                    <div id=\"auto-saves-list\" class=\"saves-list\"></div>\n                                </div>\n                                <div class=\"saves-column\">\n                                    <h4>Manual Saves</h4>\n                                    <div id=\"slot-saves-list\" class=\"saves-list\"></div>\n                                </div>\n                            </div>\n                        </div>\n\n                        <!-- Export/Import Section -->\n                        <div class=\"save-section\">\n                            <h3>\uD83D\uDCE4 Export / \uD83D\uDCE5 Import</h3>\n                            <div class=\"export-import-grid\">\n                                <div class=\"export-column\">\n                                    <h4>Export</h4>\n                                    <div class=\"export-input-group\">\n                                        <label for=\"export-filename\">Filename:</label>\n                                        <input type=\"text\" id=\"export-filename\" placeholder=\"My Game Saves\" value=\"RoadToSuccess-Saves\">\n                                    </div>\n                                    <div class=\"export-actions\">\n                                        <button id=\"export-all-button\" class=\"action-button primary\">\n                                            \uD83D\uDCE6 Export All Saves\n                                        </button>\n                                        <button id=\"export-disk-button\" class=\"action-button secondary\">\n                                            \uD83D\uDCBE Export Single Save\n                                        </button>\n                                    </div>\n                                </div>\n                                <div class=\"import-column\">\n                                    <h4>Import</h4>\n                                    <div class=\"file-input-group\">\n                                        <input type=\"file\" id=\"import-file-input\" accept=\".save,.savesbundle,.txt\" style=\"display: none;\">\n                                        <button id=\"import-file-button\" class=\"action-button primary\">\n                                            \uD83D\uDCC1 Choose File\n                                        </button>\n                                        <span id=\"import-file-name\" class=\"file-name\"></span>\n                                    </div>\n                                    <button id=\"import-button\" class=\"action-button primary\" disabled>\n                                        \uD83D\uDCE5 Import Saves\n                                    </button>\n                                </div>\n                            </div>\n                        </div>\n                    </div>\n\n                        <div class=\"save-modal-footer\">\n                            <button id=\"legacy-saves-button\" class=\"action-button secondary\">\n                                \uD83D\uDD04 Open Legacy Menu\n                            </button>\n                            <button id=\"close-save-modal\" class=\"action-button\">Close</button>\n                        </div>\n</div>\n</div>\n        ";
        // Remove existing modal if any
        var existingModal = document.getElementById('saveModalOverlay');
        if (existingModal) {
            existingModal.remove();
        }
        // Add modal to DOM
        var container = document.createElement('div');
        container.innerHTML = modalHtml;
        document.body.appendChild(container.firstElementChild);
        this.modalElement = document.getElementById('saveModalOverlay');
    };
    /**
     * Attach event listeners to the modal
     */
    SaveModalService.attachEventListeners = function () {
        var _this = this;
        var _a, _b, _c, _d, _e, _f, _g, _h, _j, _k, _l;
        // Close modal
        (_a = document.getElementById('closeSaveModal')) === null || _a === void 0 ? void 0 : _a.addEventListener('click', function () { return _this.closeModal(); });
        (_b = document.getElementById('close-save-modal')) === null || _b === void 0 ? void 0 : _b.addEventListener('click', function () { return _this.closeModal(); });
        (_c = document.getElementById('saveModalOverlay')) === null || _c === void 0 ? void 0 : _c.addEventListener('click', function (e) {
            if (e.target === document.getElementById('saveModalOverlay')) {
                _this.closeModal();
            }
        });
        // No tabs needed - single view
        // Load functionality
        (_d = document.getElementById('continue-button')) === null || _d === void 0 ? void 0 : _d.addEventListener('click', function () { return _this.continueLatestSave(); });
        // Save functionality
        (_e = document.getElementById('save-game-button')) === null || _e === void 0 ? void 0 : _e.addEventListener('click', function () { return _this.saveGame(); });
        // Export functionality
        (_f = document.getElementById('export-all-button')) === null || _f === void 0 ? void 0 : _f.addEventListener('click', function () { return _this.exportAllSaves(); });
        (_g = document.getElementById('export-disk-button')) === null || _g === void 0 ? void 0 : _g.addEventListener('click', function () { return _this.exportToDisk(); });
        // Import functionality
        (_h = document.getElementById('import-file-button')) === null || _h === void 0 ? void 0 : _h.addEventListener('click', function () {
            var _a;
            (_a = document.getElementById('import-file-input')) === null || _a === void 0 ? void 0 : _a.click();
        });
        (_j = document.getElementById('import-file-input')) === null || _j === void 0 ? void 0 : _j.addEventListener('change', function (e) { return _this.handleFileSelect(e); });
        (_k = document.getElementById('import-button')) === null || _k === void 0 ? void 0 : _k.addEventListener('click', function () { return _this.importSaves(); });
        // Legacy saves functionality
        (_l = document.getElementById('legacy-saves-button')) === null || _l === void 0 ? void 0 : _l.addEventListener('click', function () { return _this.openLegacySaves(); });
    };
    /**
     * Open the modal
     */
    SaveModalService.openModal = function () {
        var _a;
        if (!this.modalElement) {
            this.init();
        }
        (_a = this.modalElement) === null || _a === void 0 ? void 0 : _a.classList.add('show');
        this.isOpen = true;
        this.refreshSaveLists();
        this.updateContinueButton();
    };
    /**
     * Close the modal
     */
    SaveModalService.closeModal = function () {
        var _a;
        (_a = this.modalElement) === null || _a === void 0 ? void 0 : _a.classList.remove('show');
        this.isOpen = false;
    };
    /**
     * Update the save lists
     */
    SaveModalService.refreshSaveLists = function () {
        this.loadAutoSaves();
        this.loadSlotSaves();
    };
    /**
     * Load auto saves list
     */
    SaveModalService.loadAutoSaves = function () {
        var _this = this;
        var container = document.getElementById('auto-saves-list');
        if (!container)
            return;
        container.innerHTML = '';
        try {
            var entries = Save.browser.auto.entries();
            if (entries.length === 0) {
                container.innerHTML = '<p class="no-saves">No auto saves found</p>';
                return;
            }
            entries.forEach(function (_a) {
                var index = _a.index, info = _a.info;
                var saveElement = _this.createSaveElement(index, info, 'auto');
                container.appendChild(saveElement);
            });
        }
        catch (error) {
            container.innerHTML = '<p class="error">Error loading auto saves</p>';
            console.error('Error loading auto saves:', error);
        }
    };
    /**
     * Load slot saves list
     */
    SaveModalService.loadSlotSaves = function () {
        var _this = this;
        var container = document.getElementById('slot-saves-list');
        if (!container)
            return;
        container.innerHTML = '';
        try {
            var entries = Save.browser.slot.entries();
            if (entries.length === 0) {
                container.innerHTML = '<p class="no-saves">No manual saves found</p>';
                return;
            }
            entries.forEach(function (_a) {
                var index = _a.index, info = _a.info;
                var saveElement = _this.createSaveElement(index, info, 'slot');
                container.appendChild(saveElement);
            });
        }
        catch (error) {
            container.innerHTML = '<p class="error">Error loading slot saves</p>';
            console.error('Error loading slot saves:', error);
        }
    };
    /**
     * Create HTML element for a save
     */
    SaveModalService.createSaveElement = function (index, info, type) {
        var _this = this;
        var _a, _b, _c;
        var saveElement = document.createElement('div');
        saveElement.className = 'save-item';
        var date = new Date(info.date);
        var dateStr = date.toLocaleString();
        saveElement.innerHTML = "\n            <div class=\"save-info\">\n                <div class=\"save-title\">".concat(info.desc || 'Untitled Save', "</div>\n                <div class=\"save-date\">").concat(dateStr, "</div>\n                <div class=\"save-version\">v").concat(info.version || ((_a = game().game) === null || _a === void 0 ? void 0 : _a.version) || window.gameVersion || 'Unknown', "</div>\n            </div>\n            <div class=\"save-actions\">\n                <button class=\"load-button\" data-index=\"").concat(index, "\" data-type=\"").concat(type, "\">Load</button>\n                <button class=\"delete-button\" data-index=\"").concat(index, "\" data-type=\"").concat(type, "\">Delete</button>\n            </div>\n        ");
        // Event listeners for buttons
        (_b = saveElement.querySelector('.load-button')) === null || _b === void 0 ? void 0 : _b.addEventListener('click', function (e) {
            var target = e.target;
            var saveIndex = parseInt(target.dataset.index);
            var saveType = target.dataset.type;
            _this.loadSave(saveIndex, saveType);
        });
        (_c = saveElement.querySelector('.delete-button')) === null || _c === void 0 ? void 0 : _c.addEventListener('click', function (e) {
            var target = e.target;
            var saveIndex = parseInt(target.dataset.index);
            var saveType = target.dataset.type;
            _this.deleteSave(saveIndex, saveType);
        });
        return saveElement;
    };
    /**
     * Update the Continue button
     */
    SaveModalService.updateContinueButton = function () {
        var button = document.getElementById('continue-button');
        if (!button)
            return;
        try {
            var hasSaves = Save.browser.size > 0;
            button.disabled = !hasSaves;
            if (hasSaves) {
                button.textContent = 'Continue Latest Save';
            }
            else {
                button.textContent = 'No Saves Available';
            }
        }
        catch (error) {
            button.disabled = true;
            button.textContent = 'Error Checking Saves';
            console.error('Error checking saves:', error);
        }
    };
    /**
     * Load the latest save
     */
    SaveModalService.continueLatestSave = function () {
        var _this = this;
        try {
            Save.browser.continue()
                .then(function () {
                _this.showNotification('Game loaded successfully!', 'success');
                _this.closeModal();
                Engine.show();
            })
                .catch(function (error) {
                _this.showNotification('Error loading save: ' + error.message, 'error');
                console.error('Error loading save:', error);
            });
        }
        catch (error) {
            this.showNotification('Error loading save: ' + error, 'error');
            console.error('Error loading save:', error);
        }
    };
    /**
     * Load a specific save
     */
    SaveModalService.loadSave = function (index, type) {
        var _this = this;
        try {
            var saveAPI = type === 'auto' ? Save.browser.auto : Save.browser.slot;
            saveAPI.load(index)
                .then(function () {
                _this.showNotification('Save loaded successfully!', 'success');
                _this.closeModal();
                Engine.show();
            })
                .catch(function (error) {
                _this.showNotification('Error loading save: ' + error.message, 'error');
                console.error('Error loading save:', error);
            });
        }
        catch (error) {
            this.showNotification('Error loading save: ' + error, 'error');
            console.error('Error loading save:', error);
        }
    };
    /**
     * Delete a save
     */
    SaveModalService.deleteSave = function (index, type) {
        if (!confirm('Are you sure you want to delete this save?')) {
            return;
        }
        try {
            var saveAPI = type === 'auto' ? Save.browser.auto : Save.browser.slot;
            saveAPI.delete(index);
            this.showNotification('Save deleted successfully!', 'success');
            this.refreshSaveLists();
            this.updateContinueButton();
        }
        catch (error) {
            this.showNotification('Error deleting save: ' + error, 'error');
            console.error('Error deleting save:', error);
        }
    };
    /**
     * Save the game
     */
    SaveModalService.saveGame = function () {
        var _a, _b, _c, _d, _e, _f;
        var description = ((_a = document.getElementById('save-description')) === null || _a === void 0 ? void 0 : _a.value) || 'Manual Save';
        var slot = parseInt(((_b = document.getElementById('save-slot')) === null || _b === void 0 ? void 0 : _b.value) || '0');
        slot = Math.max(0, Math.min(7, slot));
        try {
            var metadata = {
                playerName: ((_c = game().player) === null || _c === void 0 ? void 0 : _c.name) || 'Unknown',
                currentLocation: ((_d = game().player) === null || _d === void 0 ? void 0 : _d.location) || 'Unknown',
                gameDay: ((_e = game().game) === null || _e === void 0 ? void 0 : _e.days) || 1,
                gameVersion: ((_f = game().game) === null || _f === void 0 ? void 0 : _f.version) || window.gameVersion || 'Unknown',
                timestamp: Date.now()
            };
            Save.browser.slot.save(slot, description, metadata);
            this.showNotification('Game saved successfully!', 'success');
            this.refreshSaveLists();
        }
        catch (error) {
            this.showNotification('Error saving game: ' + error, 'error');
            console.error('Error saving game:', error);
        }
    };
    /**
     * Export all saves as bundle
     */
    SaveModalService.exportAllSaves = function () {
        var _a;
        var filename = ((_a = document.getElementById('export-filename')) === null || _a === void 0 ? void 0 : _a.value) || 'RoadToSuccess-Saves';
        try {
            Save.disk.export(filename);
            this.showNotification('All saves exported successfully!', 'success');
        }
        catch (error) {
            this.showNotification('Error exporting saves: ' + error, 'error');
            console.error('Error exporting saves:', error);
        }
    };
    /**
     * Export current save to disk
     */
    SaveModalService.exportToDisk = function () {
        var _a, _b, _c, _d;
        try {
            var filename = "RoadToSuccess-Save-".concat(new Date().toISOString().slice(0, 10));
            Save.disk.save(filename, {
                playerName: ((_a = game().player) === null || _a === void 0 ? void 0 : _a.name) || 'Unknown',
                currentLocation: ((_b = game().player) === null || _b === void 0 ? void 0 : _b.location) || 'Unknown',
                gameDay: ((_c = game().game) === null || _c === void 0 ? void 0 : _c.days) || 1,
                gameVersion: ((_d = game().game) === null || _d === void 0 ? void 0 : _d.version) || window.gameVersion || 'Unknown',
                timestamp: Date.now()
            });
            this.showNotification('Current save exported to disk!', 'success');
        }
        catch (error) {
            this.showNotification('Error exporting to disk: ' + error, 'error');
            console.error('Error exporting to disk:', error);
        }
    };
    /**
     * Handle file selection
     */
    SaveModalService.handleFileSelect = function (event) {
        var _a;
        var input = event.target;
        var file = (_a = input.files) === null || _a === void 0 ? void 0 : _a[0];
        // Store the event for later use
        this.lastFileEvent = event;
        if (file) {
            var fileNameSpan = document.getElementById('import-file-name');
            var importButton = document.getElementById('import-button');
            // Validate file extension
            var fileName = file.name.toLowerCase();
            var isValidFile = this.isValidImportFile(fileName);
            if (fileNameSpan) {
                if (isValidFile) {
                    fileNameSpan.textContent = file.name;
                    fileNameSpan.className = 'file-name valid';
                }
                else {
                    fileNameSpan.textContent = "".concat(file.name, " (Invalid file type)");
                    fileNameSpan.className = 'file-name invalid';
                }
            }
            if (importButton) {
                importButton.disabled = !isValidFile;
                if (isValidFile) {
                    importButton.textContent = '📥 Import Saves';
                }
                else {
                    importButton.textContent = '❌ Invalid File Type';
                }
            }
        }
    };
    /**
     * Import saves
     */
    SaveModalService.importSaves = function () {
        var _this = this;
        var _a;
        var fileInput = document.getElementById('import-file-input');
        var file = (_a = fileInput.files) === null || _a === void 0 ? void 0 : _a[0];
        if (!file) {
            this.showNotification('Please select a file first!', 'error');
            return;
        }
        // Validate file type again
        var fileName = file.name.toLowerCase();
        var isValidFile = this.isValidImportFile(fileName);
        if (!isValidFile) {
            this.showNotification('Invalid file type. Please select a .save, .savesbundle, or .txt file.', 'error');
            return;
        }
        try {
            // Show different messages based on file type
            var importFileType = this.getImportFileType(fileName);
            var isBundleFile = importFileType === 'bundle';
            var fileType = isBundleFile ? 'save bundle' : 'save file';
            var action = isBundleFile ? 'Importing' : 'Loading';
            this.showNotification("".concat(action, " ").concat(fileType, "..."), 'info');
            // Use different methods based on file type
            if (isBundleFile) {
                // Import bundle (multiple saves) - use the stored event
                if (this.lastFileEvent) {
                    Save.disk.import(this.lastFileEvent)
                        .then(function () {
                        _this.showNotification('Save bundle imported successfully!', 'success');
                        _this.refreshSaveLists();
                        _this.updateContinueButton();
                    })
                        .catch(function (error) {
                        _this.showNotification("Error importing save bundle: ".concat(error.message), 'error');
                        console.error('Error importing save bundle:', error);
                    });
                }
                else {
                    this.showNotification('No file event available. Please select the file again.', 'error');
                }
            }
            else {
                // Import single save using the original file input event, matching SugarCube's native flow
                if (this.lastFileEvent) {
                    Save.disk.load(this.lastFileEvent)
                        .then(function () {
                        _this.showNotification('Save file loaded and game started!', 'success');
                        _this.closeModal();
                        Engine.show();
                    })
                        .catch(function (error) {
                        _this.showNotification("Error loading save file: ".concat(error.message), 'error');
                        console.error('Error loading save file:', error);
                    });
                }
                else {
                    this.showNotification('No file event available. Please select the file again.', 'error');
                }
            }
        }
        catch (error) {
            this.showNotification('Error importing saves: ' + error, 'error');
            console.error('Error importing saves:', error);
        }
    };
    /**
     * Show notification using the same system as PhoneService
     */
    SaveModalService.showNotification = function (message, type) {
        this.ensureNotificationElement();
        var notification = document.getElementById('notification');
        if (notification) {
            notification.textContent = message;
            notification.className = "notification ".concat(type); // Add type class for styling
            notification.classList.add('show');
            setTimeout(function () {
                notification.classList.remove('show');
            }, 3000);
        }
    };
    /**
     * Ensure notification element exists (similar to PhoneService)
     */
    SaveModalService.ensureNotificationElement = function () {
        var notificationElement = document.getElementById('notification');
        if (!notificationElement) {
            notificationElement = document.createElement('div');
            notificationElement.id = 'notification';
            notificationElement.className = 'notification';
            document.body.appendChild(notificationElement);
        }
    };
    /**
     * Open legacy saves interface
     */
    SaveModalService.openLegacySaves = function () {
        try {
            this.closeModal();
            UI.saves();
        }
        catch (error) {
            var message = 'Error opening legacy saves: ' + error;
            throw new Error(message);
        }
    };
    Object.defineProperty(SaveModalService, "isModalOpen", {
        /**
         * Check if modal is open
         */
        get: function () {
            return this.isOpen;
        },
        enumerable: false,
        configurable: true
    });
    SaveModalService.modalElement = null;
    SaveModalService.isOpen = false;
    SaveModalService.lastFileEvent = null;
    SaveModalService.validImportFileExtensions = ['.save', '.savesbundle', '.txt'];
    return SaveModalService;
}());
// Make class available globally
window.SaveModalService = SaveModalService;
/* twine-user-script #71: "DevService.js" */
"use strict";
var DevService = /** @class */ (function () {
    function DevService() {
    }
    DevService.initDev = function () {
        try {
            setup.Path = "";
            setup.ImagePath = "".concat(setup.Path, "images/");
            setup.SoundPath = "".concat(setup.Path, "sounds/");
            game().dev = {
                devMode: false,
                ptPw: "03b62516184fb6ef591f45bd4974b753",
                gPW: "08b1d443ef0ab3677d2af8ef1afb1b28",
                gUn: false,
                uAs: false,
                galleryMode: false,
                galleryCode: ""
            };
            loadAudioTracks();
        }
        catch (error) {
            throw new Error("InitDev failed: ".concat(error));
        }
    };
    return DevService;
}());
/* twine-user-script #72: "PatreonService.js" */
"use strict";
var PatreonService = /** @class */ (function () {
    function PatreonService() {
    }
    PatreonService.checkGallery = function (code) {
        if (!code) {
            Engine.play("GalleryPatreonCode");
            game().dev.gUn = false;
            return;
        }
        var pw = this.crypto(code);
        if (pw === game().dev.gPW) {
            game().dev.gUn = true;
            Engine.play('GalleryPatreon');
        }
        else {
            createNotification("Invalid Gallery Code", NotificationType.WARNING);
            game().dev.gUn = false;
            Engine.play("GalleryPatreonCode");
        }
    };
    PatreonService.checkPatreon = function (code) {
        var pw = this.crypto(code);
        if (pw === game().dev.ptPw) {
            Engine.play('Menu');
            var mobileVersion = /Mobi|Android/i.test(navigator.userAgent);
            if (mobileVersion) {
                hideRightBar();
                UIBar.stow();
                UIBar.hide();
            }
        }
        else {
            createNotification("Invalid Patreon Code", NotificationType.WARNING);
        }
        return false;
    };
    PatreonService.crypto = function (value) {
        return CryptoJS.MD5(value).toString(CryptoJS.enc.Hex);
    };
    return PatreonService;
}());
/* twine-user-script #73: "GameService.js" */
"use strict";
var GameService = /** @class */ (function () {
    function GameService() {
    }
    GameService.initGame = function () {
        var _a, _b, _c, _d, _e, _f, _g, _h, _j, _k, _l, _m, _o, _p, _q, _r, _s, _t, _u, _v, _w, _x, _y, _z, _0, _1, _2, _3, _4;
        try {
            var currentGame = game().game || {};
            var gameVersion = window.gameVersion;
            game().game = {
                days: (_a = currentGame.days) !== null && _a !== void 0 ? _a : 1,
                dice: 0,
                randomMedia: "",
                randomMoney: 0,
                maxEnergy: (_b = currentGame.maxEnergy) !== null && _b !== void 0 ? _b : 100,
                maxArousal: (_c = currentGame.maxArousal) !== null && _c !== void 0 ? _c : 10,
                time: (_d = currentGame.time) !== null && _d !== void 0 ? _d : "EM",
                day: (_e = currentGame.day) !== null && _e !== void 0 ? _e : "Sunday",
                timeIcon: (_f = currentGame.timeIcon) !== null && _f !== void 0 ? _f : '☀️',
                weather: (_g = currentGame.weather) !== null && _g !== void 0 ? _g : "clear",
                weatherIcon: (_h = currentGame.weatherIcon) !== null && _h !== void 0 ? _h : "☀️",
                lastPassage: (_j = currentGame.lastPassage) !== null && _j !== void 0 ? _j : "",
                intro: (_k = currentGame.intro) !== null && _k !== void 0 ? _k : true,
                saveVersion: (_l = currentGame.version) !== null && _l !== void 0 ? _l : gameVersion,
                version: gameVersion,
                activeWardrobeTab: "Casual",
                pinnedQuestKey: (_m = currentGame.pinnedQuestKey) !== null && _m !== void 0 ? _m : "",
                questStartCounter: (_o = currentGame.questStartCounter) !== null && _o !== void 0 ? _o : 0,
                preferences: {
                    pregnancyDays: (_q = (_p = currentGame.preferences) === null || _p === void 0 ? void 0 : _p.pregnancyDays) !== null && _q !== void 0 ? _q : 21,
                    pregnancyChance: (_s = (_r = currentGame.preferences) === null || _r === void 0 ? void 0 : _r.pregnancyChance) !== null && _s !== void 0 ? _s : 33,
                    changeClothesAuto: (_u = (_t = currentGame.preferences) === null || _t === void 0 ? void 0 : _t.changeClothesAuto) !== null && _u !== void 0 ? _u : false,
                    autoplayVideos: (_w = (_v = currentGame.preferences) === null || _v === void 0 ? void 0 : _v.autoplayVideos) !== null && _w !== void 0 ? _w : false,
                    muteVideos: (_y = (_x = currentGame.preferences) === null || _x === void 0 ? void 0 : _x.muteVideos) !== null && _y !== void 0 ? _y : false,
                    loopVideos: (_0 = (_z = currentGame.preferences) === null || _z === void 0 ? void 0 : _z.loopVideos) !== null && _0 !== void 0 ? _0 : true,
                    autoSave: (_2 = (_1 = currentGame.preferences) === null || _1 === void 0 ? void 0 : _1.autoSave) !== null && _2 !== void 0 ? _2 : false,
                    autoSaveSlot: Math.max(0, Math.min(7, (_4 = (_3 = currentGame.preferences) === null || _3 === void 0 ? void 0 : _3.autoSaveSlot) !== null && _4 !== void 0 ? _4 : 0)),
                },
            };
        }
        catch (error) {
            throw new Error("InitGame failed: " + error);
        }
    };
    return GameService;
}());
function checkGameVersion() {
    if (passage() !== "OldSaveImport" &&
        passage() !== "PatreonBlock" &&
        passage() !== "Menu" &&
        window.gameVersion !== game().game.saveVersion) {
        createNotification("You are playing an old version of the game, please import your save to the latest version", NotificationType.WARNING);
        Engine.play("OldSaveImport");
    }
}
/* twine-user-script #74: "LeftBarService.js" */
"use strict";
var LeftBarService = /** @class */ (function () {
    function LeftBarService() {
    }
    LeftBarService.getArousalText = function (level) {
        switch (level) {
            case 0:
                return { icon: '❄️', text: 'Calm' };
            case 1:
                return { icon: '🔥', text: 'Warm' };
            case 2:
                return { icon: '🔥', text: 'Aroused' };
            case 3:
                return { icon: '🔥', text: 'Hot' };
            case 4:
                return { icon: '🔥', text: 'Burning' };
            default:
                return { icon: '❄️', text: 'Calm' };
        }
    };
    return LeftBarService;
}());
/* twine-user-script #75: "ItemService.js" */
"use strict";
var ItemService = /** @class */ (function () {
    function ItemService() {
    }
    ItemService.initItems = function () {
        var items = [
            { name: "laptop", title: "Laptop", price: 800, image: "laptop.webp", type: ItemType.Electronics, icon: "💻" },
            { name: "phone", title: "Phone", price: 400, image: "phone.webp", type: ItemType.Electronics, icon: "📱" },
            { name: "webcam", title: "Webcam", price: 200, image: "webcam.webp", type: ItemType.Electronics, icon: "📷" },
            { name: "oneDayGym", title: "1 Day Membership", price: 40, image: "1daybanner.webp", type: ItemType.Gym, icon: "🏋️" },
            { name: "sevenDayGym", title: "7 Days Membership", price: 120, image: "7daybanner.webp", type: ItemType.Gym, icon: "🧘" },
            { name: "thirtyDayGym", title: "30 Days Membership", price: 250, image: "30daybanner.webp", type: ItemType.Gym, icon: "💪" },
            { name: "lifetimegym", title: "Lifetime Membership", price: 1100, image: "lifetimebanner.webp", type: ItemType.Gym, icon: "🏅" },
            { name: "pregnancyTest", title: "Pregnancy Test", price: 12, image: "pregnancyTest.webp", type: ItemType.Health, icon: "🧪" },
            { name: "contraceptivePill", title: "Contraceptive Pill", price: 8, image: "contraceptive.webp", type: ItemType.Health, icon: "💊" },
            { name: "weed", title: "Weed", price: 18, image: "weed.webp", type: ItemType.Drugs, icon: "🌿" },
            { name: "cocaine", title: "Cocaine", price: 90, image: "cocaine.webp", type: ItemType.Drugs, icon: "🧂" },
            { name: "heroin", title: "Heroin", price: 170, image: "heroin.webp", type: ItemType.Drugs, icon: "💉" },
            { name: "fakeID", title: "Fake ID", price: 150, image: "fakeID.webp", type: ItemType.Object, icon: "🪪" }
        ];
        for (var _i = 0, items_1 = items; _i < items_1.length; _i++) {
            var item = items_1[_i];
            try {
                ItemService.createItem(item);
            }
            catch (e) {
                throw new Error("Cannot create item ".concat(item.name, ": ").concat(e.message));
            }
        }
    };
    ItemService.createItem = function (item) {
        var gameData = game();
        if (!gameData.items || typeof gameData.items !== "object" || Array.isArray(gameData.items)) {
            gameData.items = {};
        }
        gameData.items[item.name] = item;
    };
    ItemService.buyItem = function (itemId) {
        var player = game().player;
        var items = game().items;
        var item = items[itemId];
        if (!item) {
            throw new Error("Item \"".concat(itemId, "\" not found."));
        }
        if (player.money >= item.price) {
            player.money -= item.price;
            player.inventory[itemId] = (player.inventory[itemId] || 0) + 1;
            createNotification("You have successfully purchased ".concat(item.title), NotificationType.SUCCESS);
            updateScreen();
            if (itemId === "fakeID") {
                QuestService.updateQuest("FakeId", 1, "I have a fake ID. I should go to the club and show it to the bouncer");
            }
        }
        else {
            createNotification("You don't have enough money to buy this!", NotificationType.WARNING);
        }
    };
    ItemService.buyGymMembership = function (membershipId) {
        var player = game().player;
        var location = game().location;
        var items = game().items;
        var item = items[membershipId];
        if (!item) {
            throw new Error("Gym membership \"".concat(membershipId, "\" not found."));
        }
        if (player.money < item.price) {
            createNotification("You don't have enough money to buy this!", NotificationType.WARNING);
            return;
        }
        var durations = {
            "oneDayGym": 1,
            "sevenDayGym": 7,
            "thirtyDayGym": 30,
            "lifetimegym": 9999
        };
        if (!(membershipId in durations)) {
            throw new Error("Invalid gym membership ID: \"".concat(membershipId, "\""));
        }
        player.money -= item.price;
        location.gym.days = durations[membershipId];
        createNotification("You have successfully purchased a ".concat(item.title), NotificationType.SUCCESS);
        Engine.play("Gym");
    };
    return ItemService;
}());
/* twine-user-script #76: "LocationService.js" */
"use strict";
var __assign = (this && this.__assign) || function () {
    __assign = Object.assign || function(t) {
        for (var s, i = 1, n = arguments.length; i < n; i++) {
            s = arguments[i];
            for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p))
                t[p] = s[p];
        }
        return t;
    };
    return __assign.apply(this, arguments);
};
var LocationService = /** @class */ (function () {
    function LocationService() {
    }
    LocationService.initLocations = function () {
        var _this = this;
        var _a, _b, _c, _d, _e, _f, _g, _h, _j, _k, _l, _m, _o, _p, _q, _r, _s, _t, _u, _v, _w, _x;
        try {
            game().location = (_a = game().location) !== null && _a !== void 0 ? _a : {};
            // Get list of valid location names from master config
            var validLocationNames_1 = new Set(masterLocationConfig.map(function (config) { return config.name; }));
            // Create or update all locations from master config
            masterLocationConfig.forEach(function (config) {
                _this.createLocation(config);
                _this.locationActions[config.name] = {
                    check: config.check,
                    action: config.action
                };
            });
            // Remove locations that no longer exist in master config
            var existingLocations = Object.keys(game().location);
            existingLocations.forEach(function (locationName) {
                if (!validLocationNames_1.has(locationName)) {
                    delete game().location[locationName];
                    delete _this.locationActions[locationName];
                }
            });
            // CITY CENTER - SUBLOCATIONS
            var centerSubLocations = [
                { location: "mall", name: "techStore", title: "Tech Store 💻", unlocked: true, imgPath: "", open: true },
                { location: "mall", name: "clothingStore", title: "Clothing Store 👚", unlocked: true, imgPath: "", open: true },
                { location: "mall", name: "pharmacy", title: "Pharmacy 💊", unlocked: true, imgPath: "", open: true },
                { location: "beach", name: "marina", title: "Marina 🛥️", unlocked: true, imgPath: "", open: true },
            ];
            centerSubLocations.forEach(function (loc) { return _this.createSubLocation(loc); });
        }
        catch (error) {
            error = "InitLocations failed: " + error;
            throw error;
        }
        try {
            var location_1 = game().location;
            // Gym
            location_1.gym.days = (_b = location_1.gym.days) !== null && _b !== void 0 ? _b : 0;
            // Restaurant
            location_1.restaurant.xp = (_c = location_1.restaurant.xp) !== null && _c !== void 0 ? _c : 0;
            location_1.restaurant.promoted = (_d = location_1.restaurant.promoted) !== null && _d !== void 0 ? _d : false;
            // Office
            location_1.office.xp = (_e = location_1.office.xp) !== null && _e !== void 0 ? _e : 0;
            location_1.office.rank = (_f = location_1.office.rank) !== null && _f !== void 0 ? _f : 1;
            // Stripclub
            location_1.stripclub.experience = (_g = location_1.stripclub.experience) !== null && _g !== void 0 ? _g : 0;
            // Club
            location_1.club.gloryholeExp = (_h = location_1.club.gloryholeExp) !== null && _h !== void 0 ? _h : 0;
            // Mall - TechStore
            location_1.mall.subLocations.techStore.discount = (_k = (_j = location_1.mall.subLocations) === null || _j === void 0 ? void 0 : _j.techStore.discount) !== null && _k !== void 0 ? _k : false;
            // Hospital
            location_1.hospital.prenatal = (_l = location_1.hospital.prenatal) !== null && _l !== void 0 ? _l : 0;
            location_1.hospital.gynecologist = (_m = location_1.hospital.gynecologist) !== null && _m !== void 0 ? _m : 0;
            location_1.hospital.sperm = (_o = location_1.hospital.sperm) !== null && _o !== void 0 ? _o : [];
            // Bus
            location_1.bus.busDestination = (_p = location_1.bus.busDestination) !== null && _p !== void 0 ? _p : "";
            // Clandestine Clinic
            location_1.clandestineClinic.inseminationDays = (_q = location_1.clandestineClinic.inseminationDays) !== null && _q !== void 0 ? _q : 0;
            location_1.clandestineClinic.inseminationStage = (_r = location_1.clandestineClinic.inseminationStage) !== null && _r !== void 0 ? _r : 0;
            // Laundry
            location_1.laundry.cut = (_s = location_1.laundry.cut) !== null && _s !== void 0 ? _s : 20;
            // Driving School
            if (location_1.drivingSchool) {
                location_1.drivingSchool.lessonsCompleted = (_t = location_1.drivingSchool.lessonsCompleted) !== null && _t !== void 0 ? _t : 0;
                location_1.drivingSchool.licenseObtained = (_u = location_1.drivingSchool.licenseObtained) !== null && _u !== void 0 ? _u : false;
                location_1.drivingSchool.practicalExamPassed = (_v = location_1.drivingSchool.practicalExamPassed) !== null && _v !== void 0 ? _v : false;
                location_1.drivingSchool.practicalExamAttempts = (_w = location_1.drivingSchool.practicalExamAttempts) !== null && _w !== void 0 ? _w : 0;
            }
            // Casino
            location_1.casino = (_x = location_1.casino) !== null && _x !== void 0 ? _x : {
                betAmount: 0,
                playerBetColor: "",
                winningNumber: 0,
                winningColor: "",
                slotsReel1: "",
                slotsReel2: "",
                slotsReel3: "",
                slotsResult: "",
                slotsWinAmount: 0,
            };
        }
        catch (error) {
            error = "InitLocations (after creating locations) failed: " + error;
            throw error;
        }
    };
    LocationService.createLocation = function (location) {
        var _a, _b, _c, _d;
        try {
            var loc = (_a = game().location[location.name]) !== null && _a !== void 0 ? _a : {};
            loc.name = location.name;
            (_b = loc.open) !== null && _b !== void 0 ? _b : (loc.open = true);
            loc.title = location.title;
            (_c = loc.unlocked) !== null && _c !== void 0 ? _c : (loc.unlocked = location.unlocked);
            loc.area = location.area;
            loc.imgPath = location.imgPath;
            loc.passage = location.passage;
            loc.openPeriods = location.openPeriods;
            (_d = loc.subLocations) !== null && _d !== void 0 ? _d : (loc.subLocations = {});
            game().location[location.name] = loc;
        }
        catch (error) {
            error = "CreateLocation failed: " + error;
            throw error;
        }
    };
    LocationService.createSubLocation = function (sublocation) {
        var _a, _b;
        var parentKey = sublocation.location;
        var subKey = sublocation.name;
        var locations = game().location;
        var mainLocation = locations[parentKey];
        if (!mainLocation) {
            throw new Error("CreateSubLocation Failed: Location '".concat(parentKey, "' does not exist."));
        }
        (_a = mainLocation.subLocations) !== null && _a !== void 0 ? _a : (mainLocation.subLocations = {});
        var existing = mainLocation.subLocations[subKey];
        var created = __assign(__assign({}, sublocation), { open: true, unlocked: (_b = existing === null || existing === void 0 ? void 0 : existing.unlocked) !== null && _b !== void 0 ? _b : sublocation.unlocked, scenes: sublocation.scenes, discount: sublocation.discount });
        mainLocation.subLocations[subKey] = created;
        return created;
    };
    LocationService.unlockLocation = function (location) {
        if (!game().location[location]) {
            return createNotification("Location " + location + " not found!", NotificationType.WARNING);
        }
        game().location[location].unlocked = true;
        var msg = game().location[location].title + ' unlocked!';
        createNotification(msg, NotificationType.INFO);
    };
    LocationService.setPlayerLocation = function (location) {
        game().player.location = location;
    };
    LocationService.checkLocationOpen = function (locationName) {
        var location = game().location;
        var isOpen = location[locationName] && location[locationName].open;
        return isOpen !== null && isOpen !== void 0 ? isOpen : false;
    };
    LocationService.isPlayerInSubLocation = function (parentLocationKey) {
        if (!parentLocationKey) {
            return false;
        }
        var playerLocation = game().player.location.toLowerCase();
        var currentPassage = passage().toLowerCase();
        var parentLocation = game().location[parentLocationKey];
        if (parentLocation && parentLocation.subLocations) {
            for (var subLocationKey in parentLocation.subLocations) {
                var subLocation = parentLocation.subLocations[subLocationKey];
                if (subLocation && subLocation.name.toLowerCase() === playerLocation) {
                    return true;
                }
            }
        }
        var relatedPassages = this.locationRelatedPassages[parentLocationKey];
        if (relatedPassages) {
            if (relatedPassages.some(function (p) { return currentPassage.includes(p) || playerLocation.includes(p); })) {
                return true;
            }
        }
        return false;
    };
    LocationService.getParentLocationByPassage = function (passageName) {
        var normalizedPassage = passageName.toLowerCase();
        for (var _i = 0, _a = Object.entries(this.locationRelatedPassages); _i < _a.length; _i++) {
            var _b = _a[_i], locationKey = _b[0], relatedPassages = _b[1];
            if (relatedPassages.some(function (p) { return normalizedPassage.includes(p); })) {
                return locationKey;
            }
        }
        return null;
    };
    /**
     * Keys in locationActions / game().location match masterLocationConfig.name (usually camelCase).
     * The only PascalCase name is "Casino"; a naive lower-first-char key would hit game().location.casino (betting state) instead.
     */
    LocationService.resolveLocationConfigKey = function (locationName) {
        if (this.locationActions[locationName]) {
            return locationName;
        }
        var camelCase = locationName.charAt(0).toLowerCase() + locationName.slice(1);
        if (this.locationActions[camelCase]) {
            return camelCase;
        }
        return Object.keys(this.locationActions).find(function (k) { return k.toLowerCase() === locationName.toLowerCase(); });
    };
    LocationService.enterLocation = function (locationName) {
        var _a;
        var player = game().player;
        if (player.clothing.type == ClothType.Underwear) {
            return createNotification("You need to wear clothes to go there!", NotificationType.WARNING);
        }
        var locationKey = this.resolveLocationConfigKey(locationName);
        var locationData = locationKey ? this.locationActions[locationKey] : undefined;
        if (!locationData) {
            var parentLocationKey = this.getParentLocationByPassage(locationName);
            if (parentLocationKey) {
                var parentLocation = game().location[parentLocationKey];
                if ((parentLocation === null || parentLocation === void 0 ? void 0 : parentLocation.open) === false) {
                    createNotification("".concat(parentLocation.title, " is closed!"), NotificationType.WARNING);
                    var parentAreaAction = this.locationActions[parentLocation.area.toLowerCase()];
                    parentAreaAction === null || parentAreaAction === void 0 ? void 0 : parentAreaAction.action();
                    return;
                }
            }
            if (Story.has(locationName)) {
                Engine.play(locationName);
                return;
            }
            throw new Error("Location '".concat(locationName, "' not found in locationActions."));
        }
        var gameLocation = game().location[locationKey];
        if (gameLocation && gameLocation.open === false) {
            var isPlayerInLocation = gameLocation.name.toLowerCase() == player.location.toLowerCase();
            var isPlayerInSubLocation = this.isPlayerInSubLocation(locationKey);
            if (isPlayerInLocation || isPlayerInSubLocation) {
                locationData = this.locationActions[gameLocation.area.toLowerCase()];
                createNotification("".concat(gameLocation.title, " is closed!"), NotificationType.WARNING);
            }
            else {
                return createNotification("".concat(gameLocation.title, " is closed!"), NotificationType.WARNING);
            }
        }
        var result = (_a = locationData.check) === null || _a === void 0 ? void 0 : _a.call(locationData);
        if (result && !result.success) {
            if (result.message) {
                createNotification(result.message, NotificationType.INFO);
                return;
            }
            if (result.clothingType) {
                if (game().game.preferences.changeClothesAuto) {
                    ClothService.changeClothAutomatic(result.clothingType);
                }
                else {
                    createNotification("You need to wear " + result.clothingType + " clothes to go there!", NotificationType.WARNING);
                    return;
                }
            }
        }
        locationData.action();
    };
    LocationService.handleSubLocation = function (location) {
        switch (location) {
            case "ParkJog":
            case "ParkLateNightJog":
                this.handleParkJog(location);
                break;
            case "BarDrink":
                this.handleBarDrink(location);
                break;
            case "BarSocialize":
                this.handleBarSocialize();
                break;
            case "BarQuit":
                this.handleJobQuit(Jobs.Bartender);
                break;
            case "Wardrobe":
                this.handleWardrobe(location);
                break;
            case "RestaurantEat":
                this.handleRestaurantEat();
                break;
            case "RestaurantQuit":
                this.handleJobQuit(Jobs.Waiter);
                break;
            case "OfficeQuit":
                this.handleJobQuit(Jobs.Secretary);
                break;
            case "RestaurantVIP":
                this.handleRestaurantVIP(location);
                break;
            case "MallFlash":
                this.handleMallFlash(location);
                break;
            case "Workout":
                this.handleWorkout(location);
                break;
            case "SchoolTest":
                this.handleSchoolTest(location);
                break;
            case "OfficeWork":
                this.handleOfficeWork(location);
                break;
            case "BeachSwim":
                this.handleBeachSwimsuit(location);
                break;
            case "BeachSunbathe":
                this.handleBeachSwimsuit(location);
                break;
            case "JetSkiRide":
                this.handleBeachSwimsuit(location);
                break;
            case "PoolSwim":
                this.handleBeachSwimsuit(location);
                break;
            case "ArtificialInsemination":
                this.handleArtificialInsemination(location);
                break;
            case "MovieTheaterMovie":
                this.handleMovieTheaterMovie(location);
                break;
            default:
                Engine.play(location);
        }
    };
    ;
    LocationService.handleLocationAction = function (location, _a) {
        var _b = _a.checkEnergy, checkEnergy = _b === void 0 ? false : _b, checkClothes = _a.checkClothes, clothesToChange = _a.clothesToChange, autoSuccessMsg = _a.autoSuccessMsg, autoFailMsg = _a.autoFailMsg, warningMsg = _a.warningMsg;
        if (checkEnergy && game().player.energy <= 10) {
            return EnergyService.notifyLowEnergy();
        }
        if (!checkClothes()) {
            if (game().game.preferences.changeClothesAuto) {
                if (ClothService.changeClothAutomatic(clothesToChange)) {
                    return Engine.play(location);
                }
                else {
                    return createNotification(autoFailMsg, NotificationType.WARNING);
                }
            }
            return createNotification(warningMsg, NotificationType.WARNING);
        }
        Engine.play(location);
    };
    LocationService.handleMovieTheaterMovie = function (location) {
        if (player().money >= 10) {
            player().money -= 10;
            StatsService.addMoney(-10);
            Engine.play(location);
        }
        else {
            createNotification("You don't have enough money!", NotificationType.WARNING);
        }
    };
    LocationService.handleArtificialInsemination = function (location) {
        var clandestineClinic = game().location.clandestineClinic;
        var days = clandestineClinic.inseminationDays;
        var stage = clandestineClinic.inseminationStage;
        if (PregnancyService.isPregnant() && player().pregnancy.discovered) {
            return createNotification("You are already pregnant!", NotificationType.WARNING);
        }
        if (stage == 1) {
            if (days > 0) {
                return createNotification("You need to wait ".concat(days, " day").concat(days > 1 ? 's' : '', " to visit the doctor again!"), NotificationType.WARNING);
            }
            return Engine.play('SexualInsemination');
        }
        Engine.play(location);
    };
    LocationService.handleBeachSwimsuit = function (location) {
        this.handleLocationAction(location, {
            checkEnergy: true,
            checkClothes: function () { return player().clothing.type === "swim"; },
            clothesToChange: ClothType.Swim,
            autoSuccessMsg: "Your clothes have been changed to a swimsuit!",
            autoFailMsg: "You don't have a swimsuit to wear!",
            warningMsg: "You need to wear a swimsuit to do this!"
        });
    };
    LocationService.handleParkJog = function (location) {
        this.handleLocationAction(location, {
            checkEnergy: true,
            checkClothes: function () { return player().clothing.type === "fitness"; },
            clothesToChange: ClothType.Fitness,
            autoSuccessMsg: "Your clothes have been changed to fitness clothes!",
            autoFailMsg: "You don't have fitness clothes to wear!",
            warningMsg: "You are not wearing fitness clothes to jog!"
        });
    };
    LocationService.handleRestaurantVIP = function (location) {
        this.handleLocationAction(location, {
            checkEnergy: false,
            checkClothes: function () { return player().clothing.name === "sexymaid"; },
            clothesToChange: game().clothes.sexymaid,
            autoSuccessMsg: "Your clothes have been changed to a sexy maid outfit!",
            autoFailMsg: "You don't have a sexy maid outfit to wear!",
            warningMsg: "You need to wear the uniform of the VIP section!"
        });
    };
    LocationService.handleOfficeWork = function (location) {
        this.handleLocationAction(location, {
            checkEnergy: true,
            checkClothes: function () { return player().clothing.name === "secretary"; },
            clothesToChange: game().clothes.secretary,
            autoSuccessMsg: "Your clothes have been changed to a secretary outfit!",
            autoFailMsg: "You don't have a secretary outfit to wear!",
            warningMsg: "You need to wear your secretary outfit to work!"
        });
    };
    LocationService.handleWorkout = function (location) {
        this.handleLocationAction(location, {
            checkEnergy: true,
            checkClothes: function () { return player().clothing.type === "fitness"; },
            clothesToChange: ClothType.Fitness,
            autoSuccessMsg: "Your clothes have been changed to fitness clothes!",
            autoFailMsg: "You don't have fitness clothes to wear!",
            warningMsg: "You need to wear fitness clothes to workout!"
        });
    };
    LocationService.handleWardrobe = function (location) {
        var playerLocation = player().location;
        if (playerLocation == "Park" || playerLocation == "Gym") {
            game().game.activeWardrobeTab = ClothType.Fitness;
        }
        else if (playerLocation == "Restaurant" || playerLocation == "Office") {
            game().game.activeWardrobeTab = ClothType.Uniform;
        }
        else if (playerLocation == "Beach" || playerLocation == "Pool") {
            game().game.activeWardrobeTab = ClothType.Swim;
        }
        Engine.play(location);
    };
    LocationService.handleRestaurantEat = function () {
        if (player().money >= 10) {
            player().money -= 10;
            StatsService.addEnergy(10);
            TimeService.addTime(1);
            createNotification("You ate a delicious meal!", NotificationType.INFO);
            createNotification("You pay 10$", NotificationType.MONEY);
            Engine.show();
        }
        else {
            createNotification("You don't have enough money!", NotificationType.WARNING);
        }
    };
    LocationService.handleBarDrink = function (location) {
        if (player().money - 15 >= 0) {
            StatsService.addMoney(-15);
            StatsService.addDrunkness();
            updateBar();
            Engine.play(location);
        }
        else {
            createNotification("You don't have enough money!", NotificationType.WARNING);
        }
    };
    LocationService.handleBarSocialize = function () {
        StatsService.addMoney(-15);
        StatsService.addSocial();
        StatsService.addEnergy(-20);
        TimeService.addTime(2);
        updateBar();
    };
    LocationService.handleJobQuit = function (job) {
        JobsService.removeJob(job);
        createNotification("You quit your job!", NotificationType.INFO);
        Engine.show();
    };
    LocationService.handleMallFlash = function (location) {
        if (SceneService.CheckSceneReq(game().location.mall.scenes.MallFlash)) {
            Engine.play(location);
        }
    };
    LocationService.handleSchoolTest = function (location) {
        SchoolService.calculateGrade();
        SchoolService.recordTestResult(game().location.school.grade);
        game().location.school.daysToNextTest = 7;
        Engine.play(location);
    };
    LocationService.setLocation = function (location, open, title, opensAt) {
        game().location[location].open = open;
        if (title) {
            game().location[location].title = title;
        }
        game().location[location].opensAt = open ? undefined : opensAt;
    };
    LocationService.updatePreviousPassage = function () {
        var excludedPassages = [
            "Cheats", "PatreonActivation", "WalkthroughV2", "Phone", "Quests",
            "Instafame", "InstafameDM", "Selfie", "Preferences", "OldSaveImport",
            "Messages", "Wardrobe", "GalleryPatreon", "GalleryPatreonCode", "LightningKidnapping"
        ];
        var previousPassage = previous();
        if (!excludedPassages.includes(previousPassage) && !galleryMode()) {
            game().game.lastPassage = previousPassage;
        }
    };
    LocationService.updateLocationsImg = function () {
        var location = game().location;
        if (game().game.time == 'E') {
            location.center.imgPath = '/citymap/center/citybannernight.webp';
            location.residential.imgPath = '/citymap/residential/residentialbannernight.webp';
            location.elite.imgPath = '/citymap/elite/elitebannernight.webp';
            location.ghetto.imgPath = '/citymap/ghetto/ghettobannernight.webp';
            location.busStop.imgPath = '/bus/busStopbannernight.webp';
            location.park.imgPath = '/park/parkbannernight.webp';
            location.house.imgPath = '/house/housebannernight.webp';
            location.school.imgPath = '/school/schoolbannernight.webp';
            location.church.imgPath = '/church/churchbannernight.webp';
        }
        else if (game().game.time == 'EM') {
            location.center.imgPath = '/citymap/center/citybanner.webp';
            location.residential.imgPath = '/citymap/residential/residentialbanner.webp';
            location.elite.imgPath = '/citymap/elite/elitebanner.webp';
            location.ghetto.imgPath = '/citymap/ghetto/ghettobanner.webp';
            location.busStop.imgPath = '/bus/busStopbanner.webp';
            location.park.imgPath = '/park/parkbanner.webp';
            location.house.imgPath = '/house/housebanner.webp';
            location.school.imgPath = '/school/schoolbanner.webp';
            location.church.imgPath = '/church/churchbanner.webp';
        }
    };
    LocationService.locationActions = {};
    LocationService.locationRelatedPassages = {
        school: [
            'library', 'librarystudy', 'libraryexhibitionism', 'school', 'schooltest',
            'schoolmalebathroom', 'schoolwomenbathroom', 'cafeteria', 'mathclass', 'historyclass',
            'computerclass', 'peclass', 'emptyclass', 'teachertutoring'
        ],
        restaurant: [
            'restaurant', 'restauranteat', 'restaurantwork', 'restaurantvip', 'restaurantinterview',
            'restaurantquit', 'restaurantpromotion', 'restaurantgangbang', 'restaurantspecialvisit'
        ],
        pool: [
            'pool', 'poolswim', 'poolswimsex'
        ],
        mall: [
            'mall', 'mallflash', 'clothingstore', 'techstore', 'pharmacy', 'swimclothes',
            'schoolclothes', 'fitnessclothes', 'costumeclothes', 'casualclothes', 'discountsex'
        ],
        gym: [
            'gym', 'workout', 'gymshower', 'workouthelp', 'gymshowerthreesome'
        ],
        office: [
            'office', 'officework', 'officehr', 'officeinterview', 'officequit', 'secretarysex'
        ],
        beach: [
            'beach', 'beachswim', 'beachsunbathe', 'beachexplore', 'marina', 'jetskiride',
            'beachchallenge', 'beachnight', 'beachrandomevent', 'beachstrange'
        ]
    };
    return LocationService;
}());
/* twine-user-script #77: "ApartmentService.js" */
"use strict";
/**
 * ApartmentService - Thin wrapper around PropertyService for apartment-specific operations
 * This provides backward compatibility and apartment-specific convenience methods
 */
var ApartmentService = /** @class */ (function () {
    function ApartmentService() {
    }
    /**
     * Initialize apartment (delegates to PropertyService)
     */
    ApartmentService.initApartment = function () {
        // PropertyService handles initialization
    };
    /**
     * Rent the apartment
     */
    ApartmentService.rentApartment = function () {
        var success = PropertyService.rentProperty(this.PROPERTY_ID);
        if (success) {
            PropertyService.setCurrentResidence(this.PROPERTY_ID);
        }
        return success;
    };
    /**
     * Check if rent is due
     */
    ApartmentService.isRentDue = function () {
        return PropertyService.isRentDue(this.PROPERTY_ID);
    };
    /**
     * Decrement rent days (delegates to PropertyService for all properties)
     */
    ApartmentService.decrementRentDays = function () {
        PropertyService.decrementRentDays();
    };
    /**
     * Pay the rent
     */
    ApartmentService.payRent = function () {
        return PropertyService.payRent(this.PROPERTY_ID);
    };
    /**
     * Skip rent payment (can only be used once)
     */
    ApartmentService.skipRent = function () {
        return PropertyService.skipRent(this.PROPERTY_ID);
    };
    /**
     * Alternative payment
     */
    ApartmentService.alternativePayment = function () {
        PropertyService.alternativePayment(this.PROPERTY_ID);
    };
    /**
     * Check if player can afford rent
     */
    ApartmentService.canAffordRent = function () {
        return PropertyService.canAffordRent(this.PROPERTY_ID);
    };
    /**
     * Check if player is living in the apartment
     */
    ApartmentService.isLivingInApartment = function () {
        return PropertyService.hasProperty(this.PROPERTY_ID);
    };
    /**
     * Get days until next rent payment
     */
    ApartmentService.getDaysUntilRent = function () {
        return PropertyService.getDaysUntilRent(this.PROPERTY_ID);
    };
    /**
     * Get rent amount
     */
    ApartmentService.getRentAmount = function () {
        return PropertyService.getRentAmount(this.PROPERTY_ID);
    };
    /**
     * Get landlord name
     */
    ApartmentService.getLandlordName = function () {
        return PropertyService.getLandlordName(this.PROPERTY_ID);
    };
    /**
     * Unrent the apartment (terminate the lease)
     */
    ApartmentService.unrentApartment = function () {
        return PropertyService.unrentProperty(this.PROPERTY_ID);
    };
    ApartmentService.PROPERTY_ID = "apartment";
    return ApartmentService;
}());
// Expose ApartmentService to window for Twine access
window.ApartmentService = ApartmentService;
/* twine-user-script #78: "CasinoService.js" */
"use strict";
var CasinoService = /** @class */ (function () {
    function CasinoService() {
    }
    CasinoService.validateBetAmount = function (betAmount) {
        if (!betAmount || betAmount === 0) {
            createNotification("You need to bet something!", NotificationType.WARNING);
            return false;
        }
        if (typeof betAmount !== "number" || isNaN(betAmount)) {
            createNotification("Invalid bet amount!", NotificationType.WARNING);
            return false;
        }
        if (betAmount < 0) {
            createNotification("You cannot bet a negative amount!", NotificationType.WARNING);
            return false;
        }
        if (player().money < betAmount) {
            createNotification("You don't have that much money to bet!", NotificationType.WARNING);
            return false;
        }
        return true;
    };
    CasinoService.clearRoulette = function () {
        var casino = game().location.casino;
        if (casino.winningColor !== "") {
            casino.playerBetColor = "";
            casino.winningNumber = 0;
            casino.winningColor = "";
        }
    };
    CasinoService.clearRouletteResult = function () {
        var casino = game().location.casino;
        casino.winningNumber = 0;
        casino.winningColor = "";
    };
    CasinoService.spinRoulette = function () {
        var casino = game().location.casino;
        var betAmount = casino.betAmount;
        var isValid = this.validateBetAmount(betAmount);
        if (!isValid) {
            return;
        }
        casino.winningNumber = Math.floor(Math.random() * 38);
        if (casino.winningNumber === 37) {
            casino.winningNumber = 0;
            casino.winningColor = "green";
        }
        else if (casino.winningNumber === 0) {
            casino.winningColor = "green";
        }
        else if (casino.winningNumber % 2 === 0) {
            casino.winningColor = "red";
        }
        else {
            casino.winningColor = "black";
        }
        if (casino.winningColor === game().location.casino.playerBetColor) {
            player().statistics.moneyEarnedCasino += betAmount;
        }
        else {
            player().statistics.moneyLostCasino += betAmount;
        }
        updateScreen();
    };
    CasinoService.clearSlots = function () {
        var casino = game().location.casino;
        if (casino.slotsResult !== "") {
            casino.slotsReel1 = "";
            casino.slotsReel2 = "";
            casino.slotsReel3 = "";
            casino.slotsResult = "";
            casino.slotsWinAmount = 0;
        }
    };
    CasinoService.spinSlots = function () {
        var casino = game().location.casino;
        var isValid = this.validateBetAmount(casino.betAmount);
        if (!isValid) {
            return;
        }
        // Slot symbols: 🍒 🍋 🍊 🍇 🍓 🍎 💎 💰 🔔 ⭐
        var symbols = ["🍒", "🍋", "🍊", "🍇", "🍓", "🍎", "💎", "💰", "🔔", "⭐"];
        // Generate random symbols for each reel
        casino.slotsReel1 = symbols[Math.floor(Math.random() * symbols.length)];
        casino.slotsReel2 = symbols[Math.floor(Math.random() * symbols.length)];
        casino.slotsReel3 = symbols[Math.floor(Math.random() * symbols.length)];
        // Check for winning combinations
        var winAmount = 0;
        var result = "";
        if (casino.slotsReel1 === casino.slotsReel2 && casino.slotsReel2 === casino.slotsReel3) {
            // Three of a kind - different payouts based on symbol
            if (casino.slotsReel1 === "💎") {
                winAmount = casino.betAmount * 100; // 100x for diamonds
                result = "DIAMOND JACKPOT!";
            }
            else if (casino.slotsReel1 === "💰") {
                winAmount = casino.betAmount * 50; // 50x for money
                result = "MONEY JACKPOT!";
            }
            else if (casino.slotsReel1 === "🔔") {
                winAmount = casino.betAmount * 25; // 25x for bell
                result = "BELL JACKPOT!";
            }
            else if (casino.slotsReel1 === "⭐") {
                winAmount = casino.betAmount * 20; // 20x for star
                result = "STAR JACKPOT!";
            }
            else {
                winAmount = casino.betAmount * 10; // 10x for fruits
                result = "TRIPLE FRUIT!";
            }
        }
        else if (casino.slotsReel1 === casino.slotsReel2 || casino.slotsReel2 === casino.slotsReel3 || casino.slotsReel1 === casino.slotsReel3) {
            // Two of a kind - smaller payout
            winAmount = casino.betAmount * 2; // 2x for pair
            result = "PAIR WIN!";
        }
        else {
            // No win
            winAmount = 0;
            result = "NO WIN";
        }
        if (winAmount > 0) {
            player().statistics.moneyEarnedCasino += winAmount;
        }
        else {
            player().statistics.moneyLostCasino += casino.betAmount;
        }
        casino.slotsResult = result;
        casino.slotsWinAmount = winAmount;
        updateScreen();
    };
    return CasinoService;
}());
/* twine-user-script #79: "DrivingSchoolService.js" */
"use strict";
var DrivingSchoolService = /** @class */ (function () {
    function DrivingSchoolService() {
    }
    DrivingSchoolService.initDrivingSchool = function () {
        var _a, _b, _c, _d, _e, _f, _g, _h;
        try {
            game().location.drivingSchool = Object.assign({
                lessonsCompleted: (_b = (_a = game().location.drivingSchool) === null || _a === void 0 ? void 0 : _a.lessonsCompleted) !== null && _b !== void 0 ? _b : 0,
                licenseObtained: (_d = (_c = game().location.drivingSchool) === null || _c === void 0 ? void 0 : _c.licenseObtained) !== null && _d !== void 0 ? _d : false,
                practicalExamPassed: (_f = (_e = game().location.drivingSchool) === null || _e === void 0 ? void 0 : _e.practicalExamPassed) !== null && _f !== void 0 ? _f : false,
                practicalExamAttempts: (_h = (_g = game().location.drivingSchool) === null || _g === void 0 ? void 0 : _g.practicalExamAttempts) !== null && _h !== void 0 ? _h : 0
            }, game().location.drivingSchool || {});
        }
        catch (error) {
            error = "InitDrivingSchool failed: " + error;
            throw error;
        }
    };
    DrivingSchoolService.takeLesson = function () {
        try {
            var drivingSchool = game().location.drivingSchool;
            var player_1 = game().player;
            if (drivingSchool.licenseObtained) {
                return { success: false, message: "You already have your driver's license!" };
            }
            if (player_1.money < this.LESSON_PRICE) {
                return { success: false, message: "You don't have enough money! You need $" + this.LESSON_PRICE };
            }
            // Deduct money
            StatsService.addMoney(-this.LESSON_PRICE);
            // Increment lessons
            drivingSchool.lessonsCompleted = (drivingSchool.lessonsCompleted || 0) + 1;
            var lessonsLeft = this.LESSONS_REQUIRED - drivingSchool.lessonsCompleted;
            var message = "You completed a practical lesson! (".concat(drivingSchool.lessonsCompleted, "/").concat(this.LESSONS_REQUIRED, ")");
            if (lessonsLeft > 0) {
                message += "\nYou need ".concat(lessonsLeft, " more lesson").concat(lessonsLeft > 1 ? 's' : '', " to take the practical exam.");
            }
            else {
                message += "\nYou can now take the practical exam!";
            }
            createNotification(message, NotificationType.SUCCESS);
            updateBar();
            return { success: true, message: message };
        }
        catch (error) {
            var errorMessage = "takeLesson failed: " + error;
            throw new Error(errorMessage);
        }
    };
    DrivingSchoolService.canTakePracticalExam = function () {
        try {
            var drivingSchool = game().location.drivingSchool;
            return (drivingSchool.lessonsCompleted || 0) >= this.LESSONS_REQUIRED && !drivingSchool.licenseObtained;
        }
        catch (error) {
            error = "canTakePracticalExam failed: " + error;
            throw error;
        }
    };
    DrivingSchoolService.passPracticalExam = function () {
        try {
            var drivingSchool = game().location.drivingSchool;
            // Mark exam as passed and obtain license
            drivingSchool.practicalExamPassed = true;
            drivingSchool.licenseObtained = true;
            drivingSchool.practicalExamAttempts = (drivingSchool.practicalExamAttempts || 0) + 1;
            var message = "Congratulations! You passed the practical exam and obtained your driver's license! 🎉";
            createNotification(message, NotificationType.SUCCESS);
            updateBar();
            return { success: true, message: message };
        }
        catch (error) {
            var errorMessage = "passPracticalExam failed: " + error;
            throw new Error(errorMessage);
        }
    };
    DrivingSchoolService.failPracticalExam = function () {
        try {
            var drivingSchool = game().location.drivingSchool;
            drivingSchool.practicalExamAttempts = (drivingSchool.practicalExamAttempts || 0) + 1;
        }
        catch (error) {
            var errorMessage = "failPracticalExam failed: " + error;
            throw new Error(errorMessage);
        }
    };
    DrivingSchoolService.getDrivingSchoolStats = function () {
        try {
            var drivingSchool = game().location.drivingSchool;
            if (!drivingSchool) {
                return {
                    lessonsCompleted: 0,
                    lessonsRequired: this.LESSONS_REQUIRED,
                    licenseObtained: false,
                    practicalExamPassed: false,
                    practicalExamAttempts: 0,
                    canTakeExam: false,
                    lessonPrice: this.LESSON_PRICE,
                    examPrice: this.PRACTICAL_EXAM_PRICE
                };
            }
            return {
                lessonsCompleted: drivingSchool.lessonsCompleted || 0,
                lessonsRequired: this.LESSONS_REQUIRED,
                licenseObtained: drivingSchool.licenseObtained || false,
                practicalExamPassed: drivingSchool.practicalExamPassed || false,
                practicalExamAttempts: drivingSchool.practicalExamAttempts || 0,
                canTakeExam: this.canTakePracticalExam(),
                lessonPrice: this.LESSON_PRICE,
                examPrice: this.PRACTICAL_EXAM_PRICE
            };
        }
        catch (error) {
            var errorMessage = "getDrivingSchoolStats failed: " + error;
            throw new Error(errorMessage);
        }
    };
    DrivingSchoolService.LESSON_PRICE = 100;
    DrivingSchoolService.LESSONS_REQUIRED = 5;
    DrivingSchoolService.PRACTICAL_EXAM_PRICE = 200;
    return DrivingSchoolService;
}());
/* twine-user-script #80: "SchoolService.js" */
"use strict";
var SchoolService = /** @class */ (function () {
    function SchoolService() {
    }
    SchoolService.initSchool = function () {
        var _a, _b, _c, _d, _e, _f, _g, _h, _j, _k, _l, _m, _o, _p, _q, _r, _s, _t, _u, _v, _w, _x, _y, _z, _0, _1, _2, _3;
        try {
            game().location.school = Object.assign({
                daysToNextTest: (_b = (_a = game().location.school) === null || _a === void 0 ? void 0 : _a.daysToNextTest) !== null && _b !== void 0 ? _b : 7,
                classroom: (_d = (_c = game().location.school) === null || _c === void 0 ? void 0 : _c.classroom) !== null && _d !== void 0 ? _d : "",
                grade: (_f = (_e = game().location.school) === null || _e === void 0 ? void 0 : _e.grade) !== null && _f !== void 0 ? _f : 0,
                lastInt: (_h = (_g = game().location.school) === null || _g === void 0 ? void 0 : _g.lastInt) !== null && _h !== void 0 ? _h : 0,
                homework: (_k = (_j = game().location.school) === null || _j === void 0 ? void 0 : _j.homework) !== null && _k !== void 0 ? _k : false,
                testsCompleted: (_m = (_l = game().location.school) === null || _l === void 0 ? void 0 : _l.testsCompleted) !== null && _m !== void 0 ? _m : 0,
                totalGradePoints: (_p = (_o = game().location.school) === null || _o === void 0 ? void 0 : _o.totalGradePoints) !== null && _p !== void 0 ? _p : 0,
                averageGrade: (_r = (_q = game().location.school) === null || _q === void 0 ? void 0 : _q.averageGrade) !== null && _r !== void 0 ? _r : 0,
                testsHistory: (_t = (_s = game().location.school) === null || _s === void 0 ? void 0 : _s.testsHistory) !== null && _t !== void 0 ? _t : [],
                graduated: (_v = (_u = game().location.school) === null || _u === void 0 ? void 0 : _u.graduated) !== null && _v !== void 0 ? _v : false,
                finalExamAvailable: (_x = (_w = game().location.school) === null || _w === void 0 ? void 0 : _w.finalExamAvailable) !== null && _x !== void 0 ? _x : false,
                finalExamAttempted: (_z = (_y = game().location.school) === null || _y === void 0 ? void 0 : _y.finalExamAttempted) !== null && _z !== void 0 ? _z : false,
                finalExamPassed: (_1 = (_0 = game().location.school) === null || _0 === void 0 ? void 0 : _0.finalExamPassed) !== null && _1 !== void 0 ? _1 : false,
                finalExamAttempts: (_3 = (_2 = game().location.school) === null || _2 === void 0 ? void 0 : _2.finalExamAttempts) !== null && _3 !== void 0 ? _3 : 0,
                MathClass: this.createClass("Math Class 📐", "EM", "MathClass", "/school/classroom/mathClass/mathclassbanner.webp"),
                HistoryClass: this.createClass("History Class ⚔️", "M", "HistoryClass", "/school/classroom/historyClass/historyclassbanner.webp"),
                ComputerClass: this.createClass("Computer Class 🖥️", "M", "ComputerClass", "/school/classroom/computerClass/computerclassbanner.webp"),
                PEClass: this.createClass("PE Class 🏋🏼‍♀️", "A", "SchoolGym", "/school/classroom/peClass/peclassbanner.webp"),
                EmptyClass: this.createClass("Empty Classroom 👩🏻‍🏫", "E", "EmptyClass", "/school/classroom/emptyClass/emptyclassbanner.webp")
            }, game().location.school || {});
        }
        catch (error) {
            error = "InitSchool failed: " + error;
            throw error;
        }
    };
    SchoolService.createClass = function (title, time, location, imagePath) {
        try {
            var classroom = void 0;
            return classroom = {
                title: title,
                time: time,
                location: location,
                imagePath: imagePath
            };
        }
        catch (error) {
            error = "createClass failed: " + error;
            throw error;
        }
    };
    SchoolService.calculateGrade = function () {
        var requiredIntelligence = 7;
        var intelligenceGained = game().player.intelligence - game().location.school.lastInt;
        if (intelligenceGained === requiredIntelligence) {
            game().location.school.grade = 6;
        }
        else {
            game().location.school.grade = Math.floor((intelligenceGained / requiredIntelligence) * 6);
            if (game().location.school.grade > 10) {
                game().location.school.grade = 10;
            }
        }
        game().location.school.lastInt = game().player.intelligence;
    };
    SchoolService.recordTestResult = function (grade) {
        try {
            var school = game().location.school;
            school.testsCompleted = (school.testsCompleted || 0) + 1;
            if (!school.testsHistory) {
                school.testsHistory = [];
            }
            school.testsHistory.push(grade);
            school.totalGradePoints = (school.totalGradePoints || 0) + grade;
            this.calculateAverageGrade();
            if (school.testsCompleted >= 12 && !school.graduated) {
                this.checkFinalExamAvailability();
            }
        }
        catch (error) {
            error = "recordTestResult failed: " + error;
            throw error;
        }
    };
    SchoolService.calculateAverageGrade = function () {
        try {
            var school = game().location.school;
            if (school.testsCompleted && school.testsCompleted > 0) {
                school.averageGrade = school.totalGradePoints / school.testsCompleted;
            }
            else {
                school.averageGrade = 0;
            }
        }
        catch (error) {
            error = "calculateAverageGrade failed: " + error;
            throw error;
        }
    };
    SchoolService.checkFinalExamAvailability = function () {
        try {
            var school = game().location.school;
            if (school.graduated) {
                school.finalExamAvailable = false;
                return;
            }
            if (school.finalExamPassed) {
                school.finalExamAvailable = false;
                return;
            }
            if (school.testsCompleted >= 12 && school.averageGrade < 6.0) {
                school.finalExamAvailable = true;
            }
            else {
                school.finalExamAvailable = false;
            }
        }
        catch (error) {
            error = "checkFinalExamAvailability failed: " + error;
            throw error;
        }
    };
    SchoolService.checkGraduationRequirements = function () {
        try {
            var school = game().location.school;
            if (school.graduated) {
                return { canGraduate: false, reason: "alreadyGraduated" };
            }
            if (!school.testsCompleted || school.testsCompleted < 12) {
                return { canGraduate: false, reason: "needMoreTests", type: "tests" };
            }
            this.calculateAverageGrade();
            var passedTests = (school.testsHistory || []).filter(function (g) { return g >= 6; }).length;
            if (school.averageGrade >= 6.0 || passedTests >= 9) {
                return { canGraduate: true, type: "normal" };
            }
            this.checkFinalExamAvailability();
            if (school.finalExamAvailable && !school.finalExamPassed) {
                return {
                    canGraduate: false,
                    reason: "canTakeFinalExamOrContinue",
                    type: "options",
                    options: ["finalExam", "continueTests"]
                };
            }
            if (school.finalExamPassed) {
                return { canGraduate: true, type: "finalExam" };
            }
            return { canGraduate: false, reason: "needMoreTests", type: "continue" };
        }
        catch (error) {
            error = "checkGraduationRequirements failed: " + error;
            throw error;
        }
    };
    SchoolService.processFinalExam = function (grade) {
        try {
            var school = game().location.school;
            school.finalExamAttempted = true;
            school.finalExamAttempts = (school.finalExamAttempts || 0) + 1;
            if (grade >= 6) {
                school.finalExamPassed = true;
                school.finalExamAvailable = false;
                if (school.averageGrade < 6.0) {
                    var pointsNeeded = (6.0 * school.testsCompleted) - school.totalGradePoints;
                    school.totalGradePoints = school.totalGradePoints + pointsNeeded;
                    school.averageGrade = 6.0;
                }
                return { passed: true, message: "Congratulations! You passed the final exam!" };
            }
            else {
                return { passed: false, message: "You failed the final exam. You can try again after more tests." };
            }
        }
        catch (error) {
            error = "processFinalExam failed: " + error;
            throw error;
        }
    };
    SchoolService.graduate = function () {
        try {
            var school = game().location.school;
            var check = this.checkGraduationRequirements();
            if (!check.canGraduate) {
                throw new Error("Graduation requirements not met: " + check.reason);
            }
            school.graduated = true;
            school.finalExamAvailable = false;
            return {
                success: true,
                type: check.type,
                averageGrade: school.averageGrade,
                testsCompleted: school.testsCompleted
            };
        }
        catch (error) {
            error = "graduate failed: " + error;
            throw error;
        }
    };
    SchoolService.getSchoolStats = function () {
        try {
            var school = game().location.school;
            var passedTests = (school.testsHistory || []).filter(function (g) { return g >= 6; }).length;
            var perfectTests = (school.testsHistory || []).filter(function (g) { return g === 10; }).length;
            return {
                testsCompleted: school.testsCompleted || 0,
                averageGrade: school.averageGrade || 0,
                passedTests: passedTests,
                perfectTests: perfectTests,
                graduated: school.graduated || false,
                finalExamAvailable: school.finalExamAvailable || false,
                finalExamPassed: school.finalExamPassed || false
            };
        }
        catch (error) {
            error = "getSchoolStats failed: " + error;
            throw error;
        }
    };
    /**
     * Force graduation - cheat/dev function
     * Forces graduation even if requirements are not met
     */
    SchoolService.forceGraduate = function () {
        try {
            var school = game().location.school;
            // Force graduation by setting required values
            if ((school.testsCompleted || 0) < 12) {
                school.testsCompleted = 12;
            }
            if (!school.averageGrade || school.averageGrade < 6.0) {
                school.totalGradePoints = 72; // 12 tests * 6.0 average
                school.averageGrade = 6.0;
            }
            school.graduated = true;
            school.finalExamAvailable = false;
        }
        catch (error) {
            throw new Error("forceGraduate failed: " + error);
        }
    };
    /**
     * Reset school progress - cheat/dev function
     * Resets all school progress back to initial state
     */
    SchoolService.resetSchoolProgress = function () {
        try {
            var school = game().location.school;
            school.testsCompleted = 0;
            school.totalGradePoints = 0;
            school.averageGrade = 0;
            school.testsHistory = [];
            school.graduated = false;
            school.finalExamAvailable = false;
            school.finalExamAttempted = false;
            school.finalExamPassed = false;
            school.finalExamAttempts = 0;
            school.daysToNextTest = 7;
            school.grade = 0;
            // Keep current intelligence - don't reset lastInt
            school.lastInt = game().player.intelligence;
        }
        catch (error) {
            throw new Error("resetSchoolProgress failed: " + error);
        }
    };
    /**
     * Maximize school average - cheat/dev function
     * Sets all tests to perfect grade (10) to achieve maximum average
     */
    SchoolService.maximizeSchoolAverage = function () {
        try {
            var school = game().location.school;
            var currentTests = school.testsCompleted || 0;
            // If no tests completed, create 12 perfect tests
            if (currentTests === 0) {
                school.testsCompleted = 12;
                school.testsHistory = Array(12).fill(10);
                school.totalGradePoints = 120; // 12 tests * 10 points
                school.averageGrade = 10.0;
                school.grade = 10; // Set current grade to 10
            }
            else {
                // If tests already exist, adjust them to perfect scores
                var perfectPoints = currentTests * 10;
                var currentPoints = school.totalGradePoints || 0;
                var pointsToAdd = perfectPoints - currentPoints;
                // Update history to all 10s
                school.testsHistory = Array(currentTests).fill(10);
                school.totalGradePoints = perfectPoints;
                school.averageGrade = 10.0;
                school.grade = 10; // Set current grade to 10
            }
        }
        catch (error) {
            throw new Error("maximizeSchoolAverage failed: " + error);
        }
    };
    return SchoolService;
}());
/* twine-user-script #81: "NpcService.js" */
"use strict";
var __assign = (this && this.__assign) || function () {
    __assign = Object.assign || function(t) {
        for (var s, i = 1, n = arguments.length; i < n; i++) {
            s = arguments[i];
            for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p))
                t[p] = s[p];
        }
        return t;
    };
    return __assign.apply(this, arguments);
};
var NpcService = /** @class */ (function () {
    function NpcService() {
    }
    /**
     * Initialize all NPCs in the game by populating game().npc
     */
    NpcService.initNpc = function () {
        var _this = this;
        try {
            var g = game();
            g.npc = g.npc || {};
            // All NPCs consolidated into a single list
            var initNpc = [
                // FAMILY NPCs
                { id: 1, key: 'Dad', name: 'Alfred', location: 'House', gender: Gender.Male, relationship: 'Stepfather', player: 'Stepdaughter' },
                { id: 2, key: 'Brother', name: 'Robert', location: 'House', gender: Gender.Male, relationship: 'Stepbrother', player: 'Stepsister' },
                { id: 3, key: 'Grandpa', name: 'William', location: 'House', gender: Gender.Male, relationship: 'Stepgrandfather', player: 'Stepgranddaughter' },
                // MARCUS FAMILY NPCs
                { id: 4, key: 'Marcus', name: 'Marcus', location: 'School', gender: Gender.Male },
                { id: 5, key: 'Sam', name: 'Sam', location: 'Marcus House', gender: Gender.Male },
                { id: 6, key: 'Oliver', name: 'Oliver', location: 'Marcus House', gender: Gender.Male },
                // SCHOOL NPCs
                { id: 7, key: 'Janitor', name: 'Mr. Wilson', location: 'School', gender: Gender.Male },
                { id: 8, key: 'MathTeacher', name: 'Mr. Thompson', location: 'School', gender: Gender.Male },
                { id: 9, key: 'Coach', name: 'Mr. Williams', location: 'School', gender: Gender.Male },
                { id: 10, key: 'Natasha', name: 'Natasha', location: 'School Library', gender: Gender.Female },
                { id: 11, key: 'Emma', name: 'Emma', location: 'School', gender: Gender.Female },
                { id: 12, key: 'ComputerTeacher', name: 'Mr. Henry', location: 'School', gender: Gender.Male },
                { id: 13, key: 'Thomas', name: 'Thomas', location: 'School', gender: Gender.Male },
                { id: 14, key: 'Strange', name: 'Strange', location: 'Park', gender: Gender.Male },
                { id: 15, key: 'StrangeBBC', name: 'Strange', location: 'Center', gender: Gender.Male },
                { id: 16, key: "Maya", name: "Maya", location: "School", gender: Gender.Transgender },
                // FILM STUDIO NPCs
                { id: 16, key: 'Jim', name: 'Jim', location: 'Film Studio', gender: Gender.Male },
                // PHOTO STUDIO NPCs
                { id: 17, key: 'Richard', name: 'Richard', location: 'Photo Studio', gender: Gender.Male },
                // RESTAURANT NPCs
                { id: 18, key: 'Boss', name: 'Boss', location: 'Restaurant', gender: Gender.Male },
                { id: 19, key: 'Michael', name: 'Michael', location: 'Restaurant', gender: Gender.Male },
                { id: 20, key: 'Susan', name: 'Susan', location: 'Restaurant', gender: Gender.Female },
                // OFFICE NPCs
                { id: 21, key: 'OfficeBoss', name: 'Mr. Davis', location: 'Office', gender: Gender.Male },
                // CLUB NPCs
                { id: 22, key: 'Jamal', name: 'Jamal', location: 'Club', gender: Gender.Male },
                { id: 23, key: 'ClubBouncer', name: 'Club Bouncer', location: 'Club', gender: Gender.Male },
                // BAR NPCs
                { id: 23, key: 'Veronica', name: 'Veronica', location: 'Bar', gender: Gender.Transgender },
                // GYM NPCs
                { id: 24, key: 'PersonalTrainer', name: 'Personal Trainer', location: 'Gym', gender: Gender.Male },
                // CHURCH NPCs
                { id: 25, key: 'Priest', name: 'Priest', location: 'Church', gender: Gender.Male },
                // DARK ALLEY NPCs
                { id: 26, key: 'Gangster', name: 'Gangster', location: 'DarkAlley', gender: Gender.Male },
                { id: 27, key: 'DrugDealer', name: 'Drug Dealer', location: 'DarkAlley', gender: Gender.Male },
                // VIPERS NPCs
                { id: 28, key: 'KingCobra', name: 'King Cobra', location: 'Vipers', gender: Gender.Male },
                { id: 29, key: 'Mamba', name: 'Mamba', location: 'Vipers', gender: Gender.Male },
                { id: 30, key: 'Krait', name: 'Krait', location: 'Vipers', gender: Gender.Female },
                // STRIP CLUB NPCs
                { id: 31, key: 'StripClubManager', name: 'Strip Club Manager', location: 'StripClub', gender: Gender.Male },
                { id: 32, key: 'Stripper', name: 'Stripper', location: 'StripClub', gender: Gender.Female },
                { id: 33, key: 'Bartender', name: 'Bartender', location: 'StripClub', gender: Gender.Male },
                { id: 34, key: 'Matthew', name: 'Mr. Matthew', location: 'StripClub', gender: Gender.Male },
                // POLICE NPCs
                { id: 35, key: 'PoliceMan', name: 'Captain William Carter', location: 'PoliceStation', gender: Gender.Male },
                { id: 36, key: 'PoliceWoman', name: 'Sergeant Emily Lewis', location: 'PoliceStation', gender: Gender.Female },
                // HOSPITAL NPCs
                { id: 37, key: 'Doctor', name: 'Dr. Johnson', location: 'Hospital', gender: Gender.Male },
                { id: 38, key: 'Nurse', name: 'Nurse Sarah', location: 'Hospital', gender: Gender.Female },
                // ABANDONED BUILDING NPCs
                { id: 39, key: 'Homeless', name: 'Homeless', location: 'AbandonedBuilding', gender: Gender.Male },
                // INSTAFAME NPCs
                { id: 40, key: 'Edward', name: 'Edward', location: 'Instafame', gender: Gender.Male },
                // GENERIC NPCs
                { id: 41, key: 'TowTruckDriver', name: 'Tow Truck Driver', location: 'Nowhere', gender: Gender.Male },
                { id: 42, key: 'DeliveryGuy', name: 'Delivery Guy', location: 'Pizza Planet', gender: Gender.Male },
                { id: 43, key: 'YachtCaptain', name: 'Yacht Captain', location: 'Yacht', gender: Gender.Male },
                { id: 44, key: 'Thief', name: 'Thief', location: 'Nowhere', gender: Gender.Male },
                { id: 45, key: 'JetSkiInstructor', name: 'Jet Ski Instructor', location: 'Beach', gender: Gender.Male },
                { id: 46, key: 'Josh', name: 'Josh', location: 'Nowhere', gender: Gender.Male },
                // CLANDESTINE CLINIC
                { id: 47, key: 'ClandestineDoctor', name: 'Dr. Andrew', location: 'ClandestineClinic', gender: Gender.Male },
                // BAR NPC
                { id: 48, key: 'BarBoss', name: 'Bar Boss', location: 'Bar', gender: Gender.Male },
                // DRIVING SCHOOL NPCs
                { id: 49, key: 'DrivingSchoolInstructor', name: 'Driving School Instructor', location: 'DrivingSchool', gender: Gender.Male },
                { id: 50, key: 'DrivingExaminer', name: 'Driving Examiner', location: 'DrivingSchool', gender: Gender.Male },
                // APARTMENT NPCs
                { id: 51, key: 'Landlord', name: 'Mr. Henderson', location: 'Apartment', gender: Gender.Male, relationship: 'Landlord' },
            ];
            initNpc.forEach(function (npc) { return _this.createNpc(npc); });
        }
        catch (e) {
            throw new Error("NpcManager.init failed: ".concat(e));
        }
    };
    /** Create or update a generic NPC */
    NpcService.createNpc = function (data) {
        var _a, _b, _c, _d, _e, _f, _g, _h;
        try {
            var g = game();
            var existing = g.npc[data.key] || {};
            var isGrandpa = data.key == 'Grandpa';
            var npc = __assign(__assign({}, data), { avatar: (_a = data.avatar) !== null && _a !== void 0 ? _a : data.key, relation: (_b = existing.relation) !== null && _b !== void 0 ? _b : 0, talkedToday: false, corruption: (_c = existing.corruption) !== null && _c !== void 0 ? _c : 0, scenes: (_d = existing.scenes) !== null && _d !== void 0 ? _d : {}, arousal: (_e = existing.arousal) !== null && _e !== void 0 ? _e : 0, sideBarText: (_f = existing.sideBarText) !== null && _f !== void 0 ? _f : data.sideBarText, relationship: (_g = existing.relationship) !== null && _g !== void 0 ? _g : data.relationship, player: (_h = existing.player) !== null && _h !== void 0 ? _h : data.player });
            if (isGrandpa) {
                npc.corruption = 99;
            }
            g.npc[data.key] = npc;
        }
        catch (e) {
            throw new Error("Cannot create NPC ".concat(data.key, ": ").concat(e));
        }
    };
    /** Routine to update family NPC locations based on day/time */
    NpcService.npcRoutine = function () {
        var isWeekend = game().game.day === 'Saturday' || game().game.day === 'Sunday';
        var dad = game().npc['Dad'];
        var brother = game().npc['Brother'];
        var grandpa = game().npc['Grandpa'];
        var time = game().game.time;
        var weekend = {
            EM: { dad: 'Kitchen', brother: 'Bathroom', grandpa: 'Bedroom' },
            M: { dad: 'Living Room', brother: 'Bedroom', grandpa: 'Bathroom' },
            A: { dad: 'Kitchen', brother: 'Living Room', grandpa: 'Bedroom' },
            E: { dad: 'Bathroom', brother: 'Living Room', grandpa: 'Living Room' },
            N: { dad: 'Bedroom', brother: 'Bedroom', grandpa: 'Living Room' },
            LN: { dad: 'Bedroom', brother: 'Bedroom', grandpa: 'Bedroom' }
        };
        var weekday = {
            EM: { dad: 'Kitchen', brother: 'Bathroom', grandpa: 'Bedroom' },
            M: { dad: 'Work', brother: 'School', grandpa: 'Living Room' },
            A: { dad: 'Work', brother: 'School', grandpa: 'Kitchen' },
            E: { dad: 'Bedroom', brother: 'Bedroom', grandpa: 'Bathroom' },
            N: { dad: 'Bathroom', brother: 'Living Room', grandpa: 'Bedroom' },
            LN: { dad: 'Bedroom', brother: 'Bedroom', grandpa: 'Bedroom' }
        };
        var locs = isWeekend ? weekend : weekday;
        var schedule = locs[time];
        if (schedule) {
            dad.location = schedule.dad;
            brother.location = schedule.brother;
            grandpa.location = schedule.grandpa;
        }
        else {
            throw new Error("Invalid time \"".concat(time, "\" for NPC routine"));
        }
    };
    NpcService.addRelation = function (npc, shouldUpdateBar) {
        if (shouldUpdateBar === void 0) { shouldUpdateBar = true; }
        game().npc[npc].relation += 1;
        createNotification(game().npc[npc].name + " relation increased 🤝🏻", NotificationType.INFO);
        if (shouldUpdateBar) {
            updateBar();
        }
    };
    NpcService.addCorruption = function (npc, amount) {
        if (amount === void 0) { amount = 1; }
        game().npc[npc].corruption += amount;
        createNotification("".concat(game().npc[npc].relationship, " corruption increased"), NotificationType.CORRUPTION);
        updateBar();
    };
    NpcService.npcTalk = function (npc) {
        if (galleryMode())
            return;
        if (npc == "Strange" || npc == "StrangeBBC")
            return;
        if (game().npc[npc].talkedToday) {
            createNotification("I already talked with ".concat(game().npc[npc].name, " today"), NotificationType.WARNING);
        }
        else {
            game().npc[npc].talkedToday = true;
            NpcService.addRelation(npc);
        }
    };
    return NpcService;
}());
/* twine-user-script #82: "PlayerService.js" */
"use strict";
var PlayerService = /** @class */ (function () {
    function PlayerService() {
    }
    PlayerService.initPlayer = function () {
        var _a, _b, _c, _d, _e, _f, _g, _h, _j, _k, _l, _m, _o, _p, _q, _r;
        try {
            var oldPlayer = (_a = game().player) !== null && _a !== void 0 ? _a : {};
            game().player = {
                name: (_b = oldPlayer.name) !== null && _b !== void 0 ? _b : "Victoria",
                avatar: "Player",
                energy: 100,
                money: (_c = oldPlayer.money) !== null && _c !== void 0 ? _c : 50,
                dirtyMoney: (_d = oldPlayer.dirtyMoney) !== null && _d !== void 0 ? _d : 0,
                exhibitionism: (_e = oldPlayer.exhibitionism) !== null && _e !== void 0 ? _e : 0,
                intelligence: (_f = oldPlayer.intelligence) !== null && _f !== void 0 ? _f : 0,
                social: (_g = oldPlayer.social) !== null && _g !== void 0 ? _g : 0,
                fitness: (_h = oldPlayer.fitness) !== null && _h !== void 0 ? _h : 0,
                beauty: (_j = oldPlayer.beauty) !== null && _j !== void 0 ? _j : 0,
                arousal: (_k = oldPlayer.arousal) !== null && _k !== void 0 ? _k : 0,
                makeup: (_l = oldPlayer.makeup) !== null && _l !== void 0 ? _l : 0,
                drunkness: (_m = oldPlayer.drunkness) !== null && _m !== void 0 ? _m : 0,
                location: (_o = oldPlayer.location) !== null && _o !== void 0 ? _o : "House",
                trans: (_p = oldPlayer.trans) !== null && _p !== void 0 ? _p : true,
                lesbian: (_q = oldPlayer.lesbian) !== null && _q !== void 0 ? _q : true,
                busDestination: "",
                clothing: oldPlayer.clothing,
                lastClothing: oldPlayer.lastClothing,
                naked: (_r = oldPlayer.naked) !== null && _r !== void 0 ? _r : false,
                scenes: {},
                inventory: InventoryService.createInventory(oldPlayer),
                pregnancy: PregnancyService.createPregnancy(oldPlayer),
                corruption: CorruptionService.createCorruption(oldPlayer),
                phone: PhoneService.createPhone(oldPlayer),
                xcam: XCamService.createXCam(oldPlayer),
                gang: GangService.createGang(oldPlayer),
                baby: BabyService.createBaby(oldPlayer),
                bank: BankService.createBankAccount(oldPlayer),
                drugs: DrugService.createDrugs(oldPlayer),
                statistics: PlayerService.createPlayerStatistics(oldPlayer),
                relationship: PlayerService.createPlayerRelationship(oldPlayer),
                jobs: JobsService.createJobs((oldPlayer === null || oldPlayer === void 0 ? void 0 : oldPlayer.jobs) || []),
                residence: PlayerService.createPlayerResidence(oldPlayer)
            };
        }
        catch (error) {
            throw new Error("InitPlayer failed: " + error);
        }
    };
    PlayerService.createPlayerStatistics = function (oldPlayer) {
        var oldPlayerStatistics = (oldPlayer === null || oldPlayer === void 0 ? void 0 : oldPlayer.statistics) || {};
        oldPlayerStatistics = {
            vaginal: oldPlayerStatistics.vaginal || 0,
            anal: oldPlayerStatistics.anal || 0,
            threesomes: oldPlayerStatistics.threesomes || 0,
            blowjobs: oldPlayerStatistics.blowjobs || 0,
            gangbangs: oldPlayerStatistics.gangbangs || 0,
            creampies: oldPlayerStatistics.creampies || 0,
            abortions: oldPlayerStatistics.abortions || 0,
            miscarriages: oldPlayerStatistics.miscarriages || 0,
            pregnancies: oldPlayerStatistics.pregnancies || 0,
            masturbations: oldPlayerStatistics.masturbations || 0,
            moneyEarnedCasino: oldPlayerStatistics.moneyEarnedCasino || 0,
            moneyLostCasino: oldPlayerStatistics.moneyLostCasino || 0,
        };
        return oldPlayerStatistics;
    };
    PlayerService.updatePlayerStatistics = function (blowjob, vaginal, anal, threesome, gangbang) {
        var statistics = game().player.statistics;
        statistics.vaginal += vaginal ? 1 : 0;
        statistics.anal += anal ? 1 : 0;
        statistics.gangbangs += gangbang ? 1 : 0;
        statistics.blowjobs += blowjob ? 1 : 0;
        statistics.threesomes += threesome ? 1 : 0;
    };
    PlayerService.createPlayerRelationship = function (oldPlayer) {
        var oldPlayerRelationship = (oldPlayer === null || oldPlayer === void 0 ? void 0 : oldPlayer.relationship) || {};
        oldPlayerRelationship = {
            npcName: oldPlayerRelationship.npcName,
            loyalty: oldPlayerRelationship.loyalty || 0,
            intimacy: oldPlayerRelationship.intimacy || 0
        };
        return oldPlayerRelationship;
    };
    PlayerService.makeBoyfriend = function (npcName) {
        var relationship = game().player.relationship;
        relationship.npcName = npcName;
        relationship.loyalty = 100;
        relationship.intimacy = 0;
    };
    PlayerService.removeBoyfriend = function () {
        var relationship = game().player.relationship;
        relationship.npcName = null;
        relationship.loyalty = 0;
        relationship.intimacy = 0;
    };
    PlayerService.isBoyfriend = function (npcName) {
        return game().player.relationship.npcName === npcName && game().player.relationship.npcName !== null;
    };
    PlayerService.createPlayerResidence = function (oldPlayer) {
        var oldResidence = (oldPlayer === null || oldPlayer === void 0 ? void 0 : oldPlayer.residence) || {};
        return {
            currentResidence: oldResidence.currentResidence || "house",
            ownedProperties: oldResidence.ownedProperties || [],
            rentedProperties: oldResidence.rentedProperties || []
        };
    };
    return PlayerService;
}());
/* twine-user-script #83: "BabyService.js" */
"use strict";
var BabyService = /** @class */ (function () {
    function BabyService() {
    }
    BabyService.createBaby = function (oldPlayer) {
        var _a, _b;
        try {
            if (!(oldPlayer === null || oldPlayer === void 0 ? void 0 : oldPlayer.baby) || oldPlayer.baby.length == 0) {
                return Array();
            }
            var babies = Array();
            for (var _i = 0, _c = oldPlayer.baby; _i < _c.length; _i++) {
                var oldBaby = _c[_i];
                var baby = {
                    name: oldBaby.name,
                    father: {
                        name: ((_a = oldBaby.father) === null || _a === void 0 ? void 0 : _a.name) || "",
                        discovered: ((_b = oldBaby.father) === null || _b === void 0 ? void 0 : _b.discovered) || false
                    },
                    sex: oldBaby.sex,
                    days: oldBaby.days || 0
                };
                babies.push(baby);
            }
            return babies;
        }
        catch (error) {
            error = "createBaby failed: " + error;
            throw error;
        }
    };
    BabyService.addBaby = function (name, father, sex, days, fatherDiscovered) {
        if (fatherDiscovered === void 0) { fatherDiscovered = false; }
        var baby = {
            name: name,
            father: {
                name: (father === null || father === void 0 ? void 0 : father.name) || "",
                discovered: fatherDiscovered
            },
            sex: sex,
            days: days || 0
        };
        game().player.baby.push(baby);
    };
    BabyService.addBabyAge = function () {
        if (!game().player.baby || game().player.baby.length == 0) {
            return;
        }
        for (var _i = 0, _a = game().player.baby; _i < _a.length; _i++) {
            var baby = _a[_i];
            baby.days += 5;
        }
    };
    BabyService.chargeWeeklyExpenses = function () {
        var _a, _b;
        if (!game().player.baby || game().player.baby.length === 0) {
            return;
        }
        var player = game().player;
        for (var _i = 0, _c = player.baby; _i < _c.length; _i++) {
            var baby = _c[_i];
            if (baby.days >= BabyService.INDEPENDENT_AGE_DAYS) {
                continue;
            }
            if (baby.days % 7 === 0) {
                var totalWealth = player.money + ((_b = (_a = player.bank) === null || _a === void 0 ? void 0 : _a.balance) !== null && _b !== void 0 ? _b : 0);
                var amount = Math.floor(totalWealth * 0.1);
                if (amount <= 0) {
                    continue;
                }
                var fromCash = Math.min(player.money, amount);
                player.money -= fromCash;
                var remainder = amount - fromCash;
                if (remainder > 0) {
                    player.bank.balance -= remainder;
                }
                createNotification("You have to pay $".concat(amount, " for ").concat(baby.name, " expenses"), NotificationType.MONEY);
                updateBar();
            }
        }
    };
    BabyService.removeBaby = function (baby) {
        game().player.baby = game().player.baby.filter(function (b) { return b.name != baby.name; });
    };
    /** Age in days after which the player no longer pays weekly child expenses (18 years). */
    BabyService.INDEPENDENT_AGE_DAYS = 18 * 365;
    return BabyService;
}());
/* twine-user-script #84: "BankService.js" */
"use strict";
var BankService = /** @class */ (function () {
    function BankService() {
    }
    BankService.createBankAccount = function (oldPlayer) {
        try {
            var bank = (oldPlayer === null || oldPlayer === void 0 ? void 0 : oldPlayer.bank) || {};
            return {
                open: bank.open || false,
                balance: bank.balance || 0
            };
        }
        catch (error) {
            throw new Error("createBankAccount failed: " + error);
        }
    };
    BankService.bankDeposit = function (amount) {
        var player = game().player;
        var bank = player.bank;
        var parsedAmount = parseInt(amount, 10);
        if (isNaN(parsedAmount)) {
            createNotification("Invalid amount", NotificationType.WARNING);
            return;
        }
        if (player.money >= parsedAmount) {
            player.money -= parsedAmount;
            bank.balance += parsedAmount;
            updateBar();
            createNotification("You deposited " + parsedAmount + "$ in your bank account", NotificationType.SUCCESS);
        }
        else {
            createNotification("You don't have enough money to deposit", NotificationType.WARNING);
        }
    };
    BankService.bankWithdraw = function (amount) {
        var player = game().player;
        var bank = player.bank;
        var parsedAmount = parseInt(amount, 10);
        if (isNaN(parsedAmount)) {
            createNotification("Invalid amount", NotificationType.WARNING);
            return;
        }
        if (bank.balance >= parsedAmount) {
            player.money += parsedAmount;
            bank.balance -= parsedAmount;
            updateBar();
            createNotification("You withdrew " + parsedAmount + "$ from your bank account", NotificationType.SUCCESS);
        }
        else {
            createNotification("You don't have enough money to withdraw", NotificationType.WARNING);
        }
    };
    BankService.generateBankIncome = function () {
        var player = game().player;
        var bank = player.bank;
        if (bank.balance > 0) {
            var percentage = 0.01;
            var income = Math.floor(bank.balance * percentage);
            if (income > 0) {
                bank.balance += income;
                createNotification("Your bank account earned " + income + "$ in interest", NotificationType.INFO);
            }
        }
    };
    BankService.openBankAccount = function () {
        player().bank.open = true;
        updateScreen();
        createNotification("You have created a bank account", NotificationType.SUCCESS);
    };
    BankService.openBankMenu = function () {
        var bankMenu = document.getElementById("bankMenu");
        if (bankMenu) {
            bankMenu.classList.add("show");
        }
        else {
            throw new Error("Bank menu element not found");
        }
        var bankMenuOverlay = document.getElementById("bankMenuOverlay");
        if (bankMenuOverlay) {
            bankMenuOverlay.classList.add("show");
        }
        else {
            throw new Error("Bank menu overlay element not found");
        }
    };
    BankService.closeBankMenu = function () {
        var bankMenu = document.getElementById("bankMenu");
        if (bankMenu) {
            bankMenu.classList.remove("show");
        }
        else {
            throw new Error("Bank menu element not found");
        }
        var bankMenuOverlay = document.getElementById("bankMenuOverlay");
        if (bankMenuOverlay) {
            bankMenuOverlay.classList.remove("show");
        }
        else {
            throw new Error("Bank menu overlay element not found");
        }
    };
    return BankService;
}());
/* twine-user-script #85: "ClothService.js" */
"use strict";
/// <reference types="twine-sugarcube" />
var ClothService = /** @class */ (function () {
    function ClothService() {
    }
    ClothService.initClothes = function () {
        var _a;
        if (!game().clothes) {
            game().clothes = {};
        }
        var clothList = [
            { name: "naked", title: "Naked", type: ClothType.Underwear, price: 0, beauty: 0, corruption: 0, image: "naked.webp", purchased: false },
            { name: "underwear", title: "Underwear", type: ClothType.Underwear, price: 0, beauty: 0, corruption: 0, image: "underwear.webp", purchased: false },
            { name: "default", title: "Default", type: ClothType.Casual, price: 0, beauty: 0, corruption: 0, image: "default.webp", purchased: false },
            { name: "casual1", title: "Casual 1", type: ClothType.Casual, price: 1, beauty: 1, corruption: 0, image: "casual1.webp", purchased: false },
            { name: "casual2", title: "Casual 2", type: ClothType.Casual, price: 2, beauty: 2, corruption: 5, image: "casual2.webp", purchased: false },
            { name: "casual3", title: "Casual 3", type: ClothType.Casual, price: 3, beauty: 3, corruption: 15, image: "casual3.webp", purchased: false },
            { name: "casual4", title: "Casual 4", type: ClothType.Casual, price: 4, beauty: 4, corruption: 30, image: "casual4.webp", purchased: false },
            { name: "school1", title: "School 1", type: ClothType.School, price: 0, beauty: 0, corruption: 0, image: "school1.webp", purchased: false },
            { name: "school2", title: "School 2", type: ClothType.School, price: 1, beauty: 1, corruption: 5, image: "school2.webp", purchased: false },
            { name: "school3", title: "School 3", type: ClothType.School, price: 2, beauty: 2, corruption: 15, image: "school3.webp", purchased: false },
            { name: "school4", title: "School 4", type: ClothType.School, price: 3, beauty: 3, corruption: 30, image: "school4.webp", purchased: false },
            { name: "school5", title: "School 5", type: ClothType.School, price: 4, beauty: 4, corruption: 45, image: "school5.webp", purchased: false },
            { name: "cheerleader1", title: "Cheerleader 1", type: ClothType.SchoolCheerleader, price: 3, beauty: 3, corruption: 30, image: "cheerleader1.webp", purchased: false },
            { name: "cheerleader2", title: "Cheerleader 2", type: ClothType.SchoolCheerleader, price: 4, beauty: 4, corruption: 45, image: "cheerleader2.webp", purchased: false },
            { name: "fitness1", title: "Fitness 1", type: ClothType.Fitness, price: 1, beauty: 1, corruption: 0, image: "fitness1.webp", purchased: false },
            { name: "fitness2", title: "Fitness 2", type: ClothType.Fitness, price: 2, beauty: 2, corruption: 5, image: "fitness2.webp", purchased: false },
            { name: "fitness3", title: "Fitness 3", type: ClothType.Fitness, price: 3, beauty: 3, corruption: 5, image: "fitness3.webp", purchased: false },
            { name: "fitness4", title: "Fitness 4", type: ClothType.Fitness, price: 4, beauty: 4, corruption: 15, image: "fitness4.webp", purchased: false },
            { name: "fitness5", title: "Fitness 5", type: ClothType.Fitness, price: 5, beauty: 5, corruption: 30, image: "fitness5.webp", purchased: false },
            { name: "fitness6", title: "Fitness 6", type: ClothType.Fitness, price: 6, beauty: 6, corruption: 45, image: "fitness6.webp", purchased: false },
            { name: "swim1", title: "Swim 1", type: ClothType.Swim, price: 1, beauty: 1, corruption: 0, image: "swim1.webp", purchased: false },
            { name: "swim2", title: "Swim 2", type: ClothType.Swim, price: 2, beauty: 2, corruption: 5, image: "swim2.webp", purchased: false },
            { name: "swim3", title: "Swim 3", type: ClothType.Swim, price: 3, beauty: 3, corruption: 15, image: "swim3.webp", purchased: false },
            { name: "swim4", title: "Swim 4", type: ClothType.Swim, price: 4, beauty: 4, corruption: 15, image: "swim4.webp", purchased: false },
            { name: "swim5", title: "Swim 5", type: ClothType.Swim, price: 5, beauty: 5, corruption: 30, image: "swim5.webp", purchased: false },
            { name: "swim6", title: "Swim 6", type: ClothType.Swim, price: 6, beauty: 6, corruption: 45, image: "swim6.webp", purchased: false },
            { name: "sexymaid", title: "Sexy Maid", type: ClothType.Uniform, price: 5, beauty: 5, corruption: 0, image: "sexyuniform.webp", purchased: false },
            { name: "secretary", title: "Secretary", type: ClothType.Uniform, price: 1, beauty: 1, corruption: 0, image: "secretary.webp", purchased: false },
            { name: "photoshootDress", title: "Photoshoot Dress", type: ClothType.Casual, price: 3, beauty: 3, corruption: 30, image: "photoshootDress.webp", purchased: false },
            { name: "cute", title: "Cute", type: ClothType.Casual, price: 2, beauty: 2, corruption: 15, image: "cute.webp", purchased: false },
            { name: "costume1", title: "Costume 1", type: ClothType.Costume, price: 5, beauty: 5, corruption: 30, image: "costume1.webp", purchased: false }
        ];
        for (var _i = 0, clothList_1 = clothList; _i < clothList_1.length; _i++) {
            var cloth = clothList_1[_i];
            this.createCloth(cloth);
        }
        if (!player().clothing) {
            player().clothing = clothes().default;
            player().lastClothing = clothes().default;
        }
        // Reconcile beauty with current outfit (fixes loaded saves where beauty was stored without outfit bonus)
        if (((_a = player().clothing) === null || _a === void 0 ? void 0 : _a.beauty) > 0 && player().beauty < player().clothing.beauty) {
            player().beauty = player().clothing.beauty;
        }
        if (this.getDefaultCloth(ClothType.Casual) === undefined) {
            clothes().default.isDefault = true;
        }
    };
    ClothService.createCloth = function (cloth) {
        var _a, _b;
        var store = game().clothes;
        var existing = store[cloth.name];
        var price = cloth.beauty * 100;
        var setAsDefault = (_a = existing === null || existing === void 0 ? void 0 : existing.isDefault) !== null && _a !== void 0 ? _a : false;
        store[cloth.name] = {
            name: cloth.name,
            title: cloth.title,
            type: cloth.type,
            price: price,
            beauty: cloth.beauty,
            corruption: cloth.corruption,
            image: cloth.image,
            purchased: (_b = existing === null || existing === void 0 ? void 0 : existing.purchased) !== null && _b !== void 0 ? _b : cloth.beauty === 0,
            isDefault: setAsDefault
        };
    };
    ClothService.changeClothes = function (cloth) {
        var currentCloth = player().clothing;
        if (currentCloth.beauty > 0) {
            player().beauty = Math.max(0, player().beauty - currentCloth.beauty);
        }
        player().lastClothing = currentCloth;
        player().clothing = cloth;
        player().beauty += cloth.beauty;
        updateBar();
    };
    ClothService.changeClothAutomatic = function (clothesToChange) {
        var clothingItem = null;
        if (typeof clothesToChange === "string") {
            clothingItem = this.getDefaultCloth(clothesToChange);
            if (!clothingItem) {
                clothingItem = this.getMostCorruptAvailableCloth(clothesToChange);
            }
        }
        else if (clothesToChange.purchased) {
            clothingItem = clothesToChange;
        }
        if (!clothingItem) {
            return false;
        }
        if (clothingItem.name !== player().clothing.name) {
            createNotification('Your clothes have been changed to ' + clothingItem.title + '!', NotificationType.INFO);
            this.changeClothes(clothingItem);
        }
        return true;
    };
    ClothService.getDefaultCloth = function (type) {
        var allClothes = Object.values(clothes());
        if (type === ClothType.School || type === ClothType.SchoolCheerleader) {
            return allClothes.find(function (item) {
                return item.isDefault &&
                    item.purchased &&
                    (item.type === ClothType.School || item.type === ClothType.SchoolCheerleader);
            });
        }
        return allClothes.find(function (item) { return item.isDefault && item.type === type; });
    };
    ClothService.getMostCorruptAvailableCloth = function (type) {
        var allClothes = Object.values(clothes());
        var filterFn;
        if (type === ClothType.School || type === ClothType.SchoolCheerleader) {
            filterFn = function (item) {
                return item.purchased &&
                    (item.type === ClothType.School || item.type === ClothType.SchoolCheerleader);
            };
        }
        else {
            filterFn = function (item) { return item.purchased && item.type === type; };
        }
        return allClothes
            .filter(filterFn)
            .reduce(function (best, item) { return !best || item.corruption > best.corruption ? item : best; }, undefined);
    };
    ClothService.hasSchoolClothWithCorruption = function (minCorruption) {
        var allClothes = Object.values(clothes());
        return allClothes.some(function (item) {
            return item.purchased &&
                item.type === ClothType.School &&
                item.corruption >= minCorruption;
        });
    };
    ClothService.buyCloth = function (cloth) {
        if (CorruptionService.getCorruptionPoints() < cloth.corruption) {
            createNotification("You aren't corrupted enough to buy this!", NotificationType.WARNING);
            return;
        }
        if (player().money < cloth.price) {
            createNotification("You don't have enough money!", NotificationType.WARNING);
            return;
        }
        cloth.purchased = true;
        player().money -= cloth.price;
        createNotification("You bought ".concat(cloth.title, "!"), NotificationType.INFO);
        if (QuestService.isQuestActive("TeacherSecretFetish") && cloth.type === ClothType.School && cloth.corruption >= 30) {
            QuestService.updateQuest("TeacherSecretFetish", 1, "I need to wear a school outfit with at least 30 corruption. Then I need to study in Computer Class and accept the teacher's help.");
        }
        if (QuestService.isQuestActive("CostumeParty") && cloth.name == "costume1") {
            QuestService.updateQuest("CostumeParty", 1, "I should go to Veronica's house on Saturday in my fairy costume");
        }
        updateScreen();
    };
    ClothService.getNaked = function () {
        if (player().clothing.name !== "naked") {
            player().lastClothing = player().clothing;
            if (player().clothing.beauty > 0) {
                player().beauty = Math.max(0, player().beauty - player().clothing.beauty);
            }
        }
        player().clothing = clothes().naked;
        player().naked = true;
        updateBar();
    };
    ClothService.getDressed = function () {
        //TODO Improve this
        if (player().lastClothing.name == "naked") {
            player().lastClothing = this.getDefaultCloth(ClothType.Casual) || clothes().default;
        }
        if (player().naked) {
            player().clothing = player().lastClothing;
            if (player().clothing.beauty > 0) {
                player().beauty += player().clothing.beauty;
            }
            player().naked = false;
            updateBar();
        }
    };
    ClothService.updateClothes = function (isPregnant) {
        var suffix = "Preg";
        var allClothes = Object.values(clothes());
        allClothes.forEach(function (item) {
            var baseImage = item.image.split('.')[0];
            if (isPregnant) {
                if (!baseImage.endsWith(suffix)) {
                    item.image = "".concat(baseImage).concat(suffix, ".webp");
                }
            }
            else {
                if (baseImage.endsWith(suffix)) {
                    item.image = "".concat(baseImage.slice(0, -suffix.length), ".webp");
                }
            }
        });
        var currentName = player().clothing.name;
        var match = allClothes.find(function (i) { return i.name === currentName; });
        if (match) {
            player().clothing.image = match.image;
            updateBar();
        }
    };
    ClothService.setDefaultCloth = function (cloth) {
        var clothKey = Object.keys(game().clothes).find(function (key) { return game().clothes[key] === cloth; });
        if (clothKey) {
            game().clothes[clothKey].isDefault = true;
            Object.values(game().clothes).forEach(function (c) {
                var isSchoolType = (cloth.type === ClothType.School || cloth.type === ClothType.SchoolCheerleader)
                    && (c.type === ClothType.School || c.type === ClothType.SchoolCheerleader);
                if ((isSchoolType || c.type === cloth.type) && c !== cloth) {
                    c.isDefault = false;
                }
            });
            createNotification("".concat(cloth.title, " is now set as default clothing."), NotificationType.INFO);
            Engine.show();
        }
        else {
            throw new Error("Cloth ".concat(cloth.name, " not found in the game clothes map."));
        }
    };
    return ClothService;
}());
/* twine-user-script #86: "CorruptionService.js" */
"use strict";
var CorruptionService = /** @class */ (function () {
    function CorruptionService() {
    }
    CorruptionService.createCorruption = function (oldPlayer) {
        var corruption = (oldPlayer === null || oldPlayer === void 0 ? void 0 : oldPlayer.corruption) || {};
        corruption = {
            level: (corruption === null || corruption === void 0 ? void 0 : corruption.level) || 0,
            points: (corruption === null || corruption === void 0 ? void 0 : corruption.points) || 0
        };
        return corruption;
    };
    CorruptionService.getCorruptionPoints = function () {
        return game().player.corruption.points;
    };
    CorruptionService.getCorruptionLevel = function () {
        var _a, _b, _c, _d;
        if (galleryMode())
            return 4;
        var corruption = game().player.corruption;
        var drugModifier = (_c = (_b = (_a = game().player.drugs) === null || _a === void 0 ? void 0 : _a.modifiers) === null || _b === void 0 ? void 0 : _b.corruptionLevel) !== null && _c !== void 0 ? _c : 0;
        var baseLevel = Math.min(corruption.level + drugModifier, 4);
        var drunkness = (_d = game().player.drunkness) !== null && _d !== void 0 ? _d : 0;
        var drunknessFloor = Math.min(Math.max(0, drunkness), 4);
        return Math.max(baseLevel, drunknessFloor);
    };
    CorruptionService.updateArousalText = function (npc, arousal) {
        switch (arousal) {
            case 0:
                npc.sideBarText = "❄️";
                break;
            case 1:
                npc.sideBarText = "🔥";
                break;
            case 2:
                npc.sideBarText = "🔥🔥";
                break;
            case 3:
                npc.sideBarText = "🔥🔥🔥";
                break;
        }
    };
    CorruptionService.updateCorruptionTitle = function () {
        var corruptionPoints = this.getCorruptionPoints();
        switch (true) {
            case (corruptionPoints < 5):
                player().corruption.level = 0;
                break;
            case (corruptionPoints >= 5 && corruptionPoints < 15):
                player().corruption.level = 1;
                break;
            case (corruptionPoints >= 15 && corruptionPoints < 30):
                player().corruption.level = 2;
                break;
            case (corruptionPoints >= 30 && corruptionPoints < 45):
                player().corruption.level = 3;
                break;
            case (corruptionPoints >= 45):
                player().corruption.level = 4;
                break;
        }
    };
    CorruptionService.updateFamilyArousal = function () {
        var dadArousal = game().npc.Dad.arousal;
        var brotherArousal = game().npc.Brother.arousal;
        var grandpaArousal = game().npc.Grandpa.arousal;
        this.updateArousalText(game().npc.Dad, dadArousal !== null && dadArousal !== void 0 ? dadArousal : 0);
        this.updateArousalText(game().npc.Brother, brotherArousal !== null && brotherArousal !== void 0 ? brotherArousal : 0);
        this.updateArousalText(game().npc.Grandpa, grandpaArousal !== null && grandpaArousal !== void 0 ? grandpaArousal : 0);
    };
    return CorruptionService;
}());
/* twine-user-script #87: "DrugService.js" */
"use strict";
var __assign = (this && this.__assign) || function () {
    __assign = Object.assign || function(t) {
        for (var s, i = 1, n = arguments.length; i < n; i++) {
            s = arguments[i];
            for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p))
                t[p] = s[p];
        }
        return t;
    };
    return __assign.apply(this, arguments);
};
var DrugService = /** @class */ (function () {
    function DrugService() {
    }
    DrugService.createDrugs = function (oldPlayer) {
        var _a, _b, _c, _d, _e, _f;
        var defaults = {
            drugAddiction: 0,
            abstinence: 0,
            duration: 0,
            drug: "",
            withdrawn: false,
            onDrugs: false,
            modifiers: {
                energy: 0,
                arousal: 0,
                social: 0,
                intelligence: 0,
                fitness: 0,
                beauty: 0,
                corruptionLevel: 0
            }
        };
        var drugs = JSON.parse(JSON.stringify(defaults));
        if (oldPlayer === null || oldPlayer === void 0 ? void 0 : oldPlayer.drugs) {
            drugs.drugAddiction = (_a = oldPlayer.drugs.drugAddiction) !== null && _a !== void 0 ? _a : defaults.drugAddiction;
            drugs.abstinence = (_b = oldPlayer.drugs.abstinence) !== null && _b !== void 0 ? _b : defaults.abstinence;
            drugs.duration = (_c = oldPlayer.drugs.duration) !== null && _c !== void 0 ? _c : defaults.duration;
            drugs.drug = (_d = oldPlayer.drugs.drug) !== null && _d !== void 0 ? _d : defaults.drug;
            drugs.withdrawn = (_e = oldPlayer.drugs.withdrawn) !== null && _e !== void 0 ? _e : defaults.withdrawn;
            drugs.onDrugs = (_f = oldPlayer.drugs.onDrugs) !== null && _f !== void 0 ? _f : defaults.onDrugs;
            drugs.modifiers = __assign(__assign({}, defaults.modifiers), oldPlayer.drugs.modifiers);
        }
        return drugs;
    };
    DrugService.useDrugs = function (drug) {
        var _a, _b;
        var _c;
        var player = game().player;
        var inv = (_c = player.inventory) !== null && _c !== void 0 ? _c : {};
        if (!inv[drug] || inv[drug] <= 0) {
            createNotification("You don't have any ".concat(drug), NotificationType.WARNING);
            return;
        }
        var drugData = (_a = {},
            _a[DrugType.Weed] = { addiction: 5, duration: 2 },
            _a[DrugType.Cocaine] = { addiction: 10, duration: 4 },
            _a[DrugType.Heroin] = { addiction: 20, duration: 6 },
            _a);
        var selected = drugData[drug];
        if (!selected)
            throw new Error("Invalid drug: ".concat(drug));
        if (player.drugs.onDrugs) {
            DrugService.removeDrugEffects();
        }
        player.drugs.drugAddiction = Math.min(100, player.drugs.drugAddiction + selected.addiction);
        player.drugs.abstinence = 0;
        player.drugs.onDrugs = true;
        player.drugs.duration = selected.duration;
        player.drugs.drug = drug;
        player.inventory[drug]--;
        DrugService.notifyAddictionLevel(player.drugs.drugAddiction);
        DrugService.applyDrugEffects();
        DrugService.applyPregnancyDrugEffects(drug);
        var corruptionGains = (_b = {},
            _b[DrugType.Weed] = 0,
            _b[DrugType.Cocaine] = 1,
            _b[DrugType.Heroin] = 2,
            _b);
        var gain = corruptionGains[drug];
        if (gain > 0) {
            createNotification("Your corruption deepens...", NotificationType.CORRUPTION);
        }
        createNotification("You used ".concat(drug), NotificationType.INFO);
        updateScreen();
    };
    DrugService.notifyAddictionLevel = function (level) {
        if (level >= 90) {
            createNotification("You are heavily addicted to drugs", NotificationType.WARNING);
        }
        else if (level >= 75) {
            createNotification("You are very addicted to drugs", NotificationType.WARNING);
        }
        else if (level >= 50) {
            createNotification("You are addicted to drugs", NotificationType.WARNING);
        }
        else if (level >= 20) {
            createNotification("You are getting addicted to drugs", NotificationType.WARNING);
        }
    };
    DrugService.applyDrugEffects = function () {
        var player = game().player;
        var mods = player.drugs.modifiers;
        if (!player.drugs.onDrugs || player.drugs.duration <= 0)
            return;
        for (var key in mods) {
            mods[key] = 0;
        }
        switch (player.drugs.drug) {
            case DrugType.Weed:
                mods.energy = -5;
                mods.arousal = 5;
                mods.social = 3;
                mods.intelligence = -2;
                break;
            case DrugType.Cocaine:
                mods.energy = 10;
                mods.social = 5;
                mods.intelligence = 5;
                mods.arousal = -5;
                mods.corruptionLevel = 1;
                mods.beauty = -2;
                break;
            case DrugType.Heroin:
                mods.arousal = 8;
                mods.energy = -10;
                mods.intelligence = -5;
                mods.fitness = -5;
                mods.corruptionLevel = 2;
                mods.beauty = -3;
                break;
        }
        player.drugs.withdrawn = false;
        player.energy = Math.max(0, player.energy + mods.energy);
        player.arousal = Math.max(0, player.arousal + mods.arousal);
        player.social = Math.max(0, player.social + mods.social);
        player.intelligence = Math.max(0, player.intelligence + mods.intelligence);
        player.fitness = Math.max(0, player.fitness + mods.fitness);
    };
    DrugService.removeDrugEffects = function () {
        var player = game().player;
        var mods = player.drugs.modifiers;
        player.social = Math.max(0, player.social - mods.social);
        player.intelligence = Math.max(0, player.intelligence - mods.intelligence);
        player.fitness = Math.max(0, player.fitness - mods.fitness);
        for (var key in mods) {
            mods[key] = 0;
        }
        player.drugs.onDrugs = false;
        player.drugs.drug = "";
        player.drugs.duration = 0;
    };
    DrugService.applyPregnancyDrugEffects = function (drug) {
        var _a;
        var _b, _c;
        var player = game().player;
        if (!((_b = player.pregnancy) === null || _b === void 0 ? void 0 : _b.isPregnant))
            return;
        var chanceMap = (_a = {},
            _a[DrugType.Weed] = 0.05,
            _a[DrugType.Cocaine] = 0.25,
            _a[DrugType.Heroin] = 0.5,
            _a);
        var chance = (_c = chanceMap[drug]) !== null && _c !== void 0 ? _c : 0;
        if (Math.random() < chance) {
            PregnancyService.removePregnancy();
            createNotification("Due to drug use, you had a miscarriage", NotificationType.WARNING);
        }
        else {
            createNotification("Using drugs while pregnant is very dangerous!", NotificationType.WARNING);
        }
    };
    DrugService.updateDrugStatus = function (time) {
        var player = game().player;
        if (player.drugs.onDrugs && player.drugs.duration > 0) {
            player.drugs.duration -= time;
            if (player.drugs.duration <= 0) {
                DrugService.removeDrugEffects();
                createNotification("The effects of the drug have worn off", NotificationType.INFO);
            }
        }
        if (!player.drugs.onDrugs && player.drugs.drugAddiction > 0) {
            player.drugs.abstinence = Math.min(100, player.drugs.abstinence + time);
            if (player.drugs.drugAddiction >= 50 &&
                player.drugs.abstinence >= 3 &&
                !player.drugs.withdrawn) {
                var messages = [
                    "You feel shaky and uneasy...",
                    "Your body craves the drug...",
                    "You're having cold sweats...",
                    "You can't stop thinking about getting high..."
                ];
                createNotification(randomFrom(messages), NotificationType.WARNING);
                player.energy = Math.max(0, player.energy - 5);
                player.social = Math.max(0, player.social - 5);
                player.drugs.withdrawn = true;
            }
            if (player.drugs.abstinence >= 100) {
                player.drugs.drugAddiction = Math.max(0, player.drugs.drugAddiction - 3);
                createNotification("You feel a bit better, but the drug addiction is still there.", NotificationType.INFO);
            }
            if (player.drugs.drugAddiction === 0 && player.drugs.abstinence > 0) {
                player.drugs.abstinence = Math.max(0, player.drugs.abstinence - time);
            }
        }
    };
    return DrugService;
}());
/* twine-user-script #88: "EnergyService.js" */
"use strict";
var EnergyService = /** @class */ (function () {
    function EnergyService() {
    }
    EnergyService.checkEnergy = function () {
        if (game().player.energy >= game().game.maxEnergy) {
            game().player.energy = game().game.maxEnergy;
        }
        if (game().player.energy <= 0) {
            game().player.energy = 0;
        }
        if (game().player.energy == 0 && passage() != 'Bedroom' && passage() != 'NoEnergy' && passage() != 'BedroomSleep') {
            Engine.play('NoEnergy');
        }
    };
    EnergyService.notifyLowEnergy = function () {
        createNotification("I'm very tired, I should rest!", NotificationType.WARNING);
    };
    return EnergyService;
}());
/* twine-user-script #89: "GangService.js" */
"use strict";
var GangService = /** @class */ (function () {
    function GangService() {
    }
    GangService.createGang = function (oldPlayer) {
        var gang = oldPlayer.gang || {};
        gang = {
            respect: (gang === null || gang === void 0 ? void 0 : gang.respect) || 0,
            title: (gang === null || gang === void 0 ? void 0 : gang.title) || "Recruit",
            daysToWork: (gang === null || gang === void 0 ? void 0 : gang.worked) || 0,
        };
        return gang;
    };
    GangService.setDaysToWork = function (days) {
        if (isNaN(days)) {
            console.warn("setDaysToWork called without a valid number");
            return;
        }
        game().player.gang.daysToWork = days;
        updateBar();
    };
    GangService.addVipersRespect = function () {
        var gang = game().player.gang;
        if (gang.respect === 10 && gang.title === "Recruit") {
            createNotification("You should talk with the boss", NotificationType.INFO);
            return;
        }
        if (gang.respect === 20 && gang.title === "Dealer") {
            createNotification("You should talk with the boss", NotificationType.INFO);
            return;
        }
        gang.respect += 1;
        createNotification("Vipers respect increased", NotificationType.INFO);
        updateBar();
    };
    GangService.promoteViper = function (newTitle, resetDays) {
        if (resetDays === void 0) { resetDays = 0; }
        if (!newTitle) {
            console.warn("promoteViper called without a title");
            return;
        }
        var gang = game().player.gang;
        var parsedDays = Number(resetDays);
        gang.title = newTitle;
        gang.daysToWork = isNaN(parsedDays) ? 0 : parsedDays;
        createNotification("You are now a ".concat(newTitle), NotificationType.SUCCESS);
        updateBar();
    };
    return GangService;
}());
/* twine-user-script #90: "InventoryService.js" */
"use strict";
var InventoryService = /** @class */ (function () {
    function InventoryService() {
    }
    InventoryService.createInventory = function (oldPlayer) {
        var _a, _b, _c, _d, _e, _f, _g, _h, _j, _k, _l, _m, _o;
        var oldInventory = oldPlayer === null || oldPlayer === void 0 ? void 0 : oldPlayer.inventory;
        return {
            laptop: (_a = oldInventory === null || oldInventory === void 0 ? void 0 : oldInventory.laptop) !== null && _a !== void 0 ? _a : 0,
            phone: (_b = oldInventory === null || oldInventory === void 0 ? void 0 : oldInventory.phone) !== null && _b !== void 0 ? _b : 0,
            webcam: (_c = oldInventory === null || oldInventory === void 0 ? void 0 : oldInventory.webcam) !== null && _c !== void 0 ? _c : 0,
            oneDayGym: (_d = oldInventory === null || oldInventory === void 0 ? void 0 : oldInventory.oneDayGym) !== null && _d !== void 0 ? _d : 0,
            sevenDayGym: (_e = oldInventory === null || oldInventory === void 0 ? void 0 : oldInventory.sevenDayGym) !== null && _e !== void 0 ? _e : 0,
            thirtyDayGym: (_f = oldInventory === null || oldInventory === void 0 ? void 0 : oldInventory.thirtyDayGym) !== null && _f !== void 0 ? _f : 0,
            lifetimegym: (_g = oldInventory === null || oldInventory === void 0 ? void 0 : oldInventory.lifetimegym) !== null && _g !== void 0 ? _g : 0,
            pregnancyTest: (_h = oldInventory === null || oldInventory === void 0 ? void 0 : oldInventory.pregnancyTest) !== null && _h !== void 0 ? _h : 0,
            contraceptivePill: (_j = oldInventory === null || oldInventory === void 0 ? void 0 : oldInventory.contraceptivePill) !== null && _j !== void 0 ? _j : 0,
            weed: (_k = oldInventory === null || oldInventory === void 0 ? void 0 : oldInventory.weed) !== null && _k !== void 0 ? _k : 0,
            cocaine: (_l = oldInventory === null || oldInventory === void 0 ? void 0 : oldInventory.cocaine) !== null && _l !== void 0 ? _l : 0,
            heroin: (_m = oldInventory === null || oldInventory === void 0 ? void 0 : oldInventory.heroin) !== null && _m !== void 0 ? _m : 0,
            fakeID: (_o = oldInventory === null || oldInventory === void 0 ? void 0 : oldInventory.fakeID) !== null && _o !== void 0 ? _o : 0,
        };
    };
    InventoryService.isPurchased = function (itemName) {
        var player = game().player;
        var inventory = player.inventory;
        return inventory && (inventory[itemName] || 0) > 0;
    };
    InventoryService.addToInventory = function (itemName) {
        var _a;
        var player = game().player;
        player.inventory[itemName] = ((_a = player.inventory[itemName]) !== null && _a !== void 0 ? _a : 0) + 1;
    };
    InventoryService.removeFromInventory = function (itemName) {
        var _a;
        var player = game().player;
        var inventory = player.inventory;
        if (!inventory || !(itemName in inventory)) {
            throw new Error("Item \"".concat(itemName, "\" not found in inventory"));
        }
        if (inventory[itemName] > 0) {
            inventory[itemName] -= 1;
        }
        else {
            var title = ((_a = game().items[itemName]) === null || _a === void 0 ? void 0 : _a.title) || itemName;
            throw new Error("You don't have any \"".concat(title, "\" to remove"));
        }
    };
    return InventoryService;
}());
/* twine-user-script #91: "JobsService.js" */
"use strict";
var jobsDefinitions = [
    { id: 1, name: "Waiter", location: "Restaurant", xp: 0, active: false, rank: 1 },
    { id: 2, name: "Secretary", location: "Office", xp: 0, active: false, rank: 1 },
    { id: 3, name: "Bartender", location: "Bar", xp: 0, active: false, rank: 1 },
    { id: 4, name: "Stripper", location: "StripClub", xp: 0, active: false, rank: 1 },
];
var JobsService = /** @class */ (function () {
    function JobsService() {
    }
    JobsService.createJobs = function (oldJobs) {
        var jobs = [];
        try {
            jobs = jobsDefinitions.map(function (job) {
                var oldJob = oldJobs.find(function (j) { return j.name === job.name; });
                return {
                    id: job.id,
                    name: job.name,
                    xp: (oldJob === null || oldJob === void 0 ? void 0 : oldJob.xp) || 0,
                    location: job.location,
                    active: (oldJob === null || oldJob === void 0 ? void 0 : oldJob.active) || job.active,
                    rank: (oldJob === null || oldJob === void 0 ? void 0 : oldJob.rank) || 1
                };
            });
            return jobs;
        }
        catch (error) {
            throw new Error("CreateJobs failed: " + error);
        }
    };
    JobsService.addJob = function (jobName) {
        try {
            var job = this.getJobByName(jobName);
            job.active = true;
            createNotification("You have been hired as a ".concat(job.name), "info");
        }
        catch (error) {
            throw new Error("AddJob failed: " + error);
        }
    };
    JobsService.removeJob = function (jobName) {
        try {
            var job = this.getJobByName(jobName);
            job.active = false;
        }
        catch (error) {
            throw new Error("RemoveJob failed: " + error);
        }
    };
    JobsService.getJobByName = function (jobName) {
        try {
            var job = player().jobs.find(function (job) { return job.name === jobName; });
            if (!job) {
                throw new Error("Job not found: " + jobName);
            }
            return job;
        }
        catch (error) {
            throw new Error("GetJobByName failed: " + error);
        }
    };
    JobsService.isJobActive = function (jobName) {
        try {
            var job = this.getJobByName(jobName);
            return job.active;
        }
        catch (error) {
            throw new Error("IsJobActive failed: " + error);
        }
    };
    JobsService.addJobXp = function (jobName, xp) {
        try {
            var job = this.getJobByName(jobName);
            if (xp) {
                job.xp += xp;
            }
            else {
                job.xp += 1;
            }
            createNotification("You have gained ".concat(xp || 1, " XP in the ").concat(jobName, " job"), "info");
        }
        catch (error) {
            throw new Error("AddJobXP failed: " + error);
        }
    };
    JobsService.getJobXp = function (jobName) {
        try {
            var job = this.getJobByName(jobName);
            return job.xp;
        }
        catch (error) {
            throw new Error("GetJobXp failed: " + error);
        }
    };
    JobsService.getJobRank = function (jobName) {
        try {
            var job = this.getJobByName(jobName);
            return job.rank;
        }
        catch (error) {
            throw new Error("GetJobRank failed: " + error);
        }
    };
    JobsService.addJobRank = function (jobName, rank) {
        try {
            var job = this.getJobByName(jobName);
            if (rank) {
                job.rank = rank;
            }
            else {
                job.rank += 1;
            }
        }
        catch (error) {
            throw new Error("AddJobRank failed: " + error);
        }
    };
    return JobsService;
}());
/* twine-user-script #92: "PregnancyService.js" */
"use strict";
var PregnancyService = /** @class */ (function () {
    function PregnancyService() {
    }
    PregnancyService.createPregnancy = function (oldPlayer) {
        var _a, _b;
        var playerPregnancy = (oldPlayer === null || oldPlayer === void 0 ? void 0 : oldPlayer.pregnancy) || {};
        var pregnancy = {
            isPregnant: playerPregnancy.isPregnant || false,
            days: playerPregnancy.days || 0,
            father: {
                name: ((_a = playerPregnancy.father) === null || _a === void 0 ? void 0 : _a.name) || "",
                discovered: ((_b = playerPregnancy.father) === null || _b === void 0 ? void 0 : _b.discovered) || false,
            },
            discovered: playerPregnancy.discovered || false,
            enabled: playerPregnancy.enabled || false,
            pillDays: playerPregnancy.pillDays || 0,
        };
        return pregnancy;
    };
    PregnancyService.isPregnant = function () {
        var player = game().player;
        return player.pregnancy.isPregnant;
    };
    /** Progress from 0 (just pregnant) to 1 (birth). Uses configurable pregnancyDays. */
    PregnancyService.getPregnancyProgress = function () {
        var _a;
        var player = game().player;
        if (!((_a = player === null || player === void 0 ? void 0 : player.pregnancy) === null || _a === void 0 ? void 0 : _a.isPregnant) || player.pregnancy.days <= 0)
            return 0;
        var total = game().game.preferences.pregnancyDays;
        if (total <= 0)
            return 0;
        return Math.min(1, (total - player.pregnancy.days) / total);
    };
    /** Game stage by progress: early (symptoms), showing (visible belly), late (close to birth). */
    PregnancyService.getPregnancyStage = function () {
        var progress = PregnancyService.getPregnancyProgress();
        if (progress < 1 / 3)
            return "early";
        if (progress < 2 / 3)
            return "showing";
        return "late";
    };
    /** True when pregnancy is visibly noticeable (second half of pregnancy by current media logic). */
    PregnancyService.hasVisibleBelly = function () {
        return PregnancyService.getPregnancyProgress() >= 0.5;
    };
    /** True when in early stage (first third) - nausea, fatigue, etc. */
    PregnancyService.hasEarlySymptoms = function () {
        return PregnancyService.getPregnancyStage() === "early";
    };
    /** Short label for UI, e.g. "Early", "Showing", "Late". */
    PregnancyService.getPregnancyStatusText = function () {
        if (!PregnancyService.isPregnant())
            return "";
        var stage = PregnancyService.getPregnancyStage();
        return stage.charAt(0).toUpperCase() + stage.slice(1);
    };
    PregnancyService.changeMediaPregnant = function () {
        return PregnancyService.hasVisibleBelly();
    };
    PregnancyService.makePregnant = function () {
        var pregnancy = game().player.pregnancy;
        pregnancy.isPregnant = true;
        pregnancy.days = game().game.preferences.pregnancyDays;
        pregnancy.discovered = true;
        pregnancy.father = {
            name: "Unknown",
            discovered: true,
        };
    };
    PregnancyService.finishPregnancy = function (babyName, isMale) {
        if (isMale === void 0) { isMale = false; }
        if (babyName) {
            var sex = isMale ? Gender.Male : Gender.Female;
            BabyService.addBaby(babyName, game().player.pregnancy.father, sex, 0, game().player.pregnancy.father.discovered);
            createNotification("You now have a baby!", NotificationType.INFO);
        }
        else {
            createNotification("You lost your baby!", NotificationType.WARNING);
            game().player.statistics.miscarriages++;
        }
        var pregnancy = game().player.pregnancy;
        pregnancy.isPregnant = false;
        pregnancy.discovered = false;
        pregnancy.days = 0;
        pregnancy.father = {
            name: "Unknown",
            discovered: false,
        };
    };
    PregnancyService.dnaTest = function () {
        var fatherName = game().player.pregnancy.father.name;
        var samples = game().location.hospital.sperm;
        if (samples.some(function (sample) { return sample == fatherName; })) {
            game().player.pregnancy.father.discovered = true;
            createNotification("The DNA test was positive, the father is " + fatherName, NotificationType.INFO);
            QuestService.finishQuest("WhoIsTheFather");
        }
        else {
            createNotification("The DNA test was negative, the father is still unknown", NotificationType.INFO);
        }
        game().location.hospital.sperm = [];
    };
    PregnancyService.removePregnancy = function () {
        var pregnancy = game().player.pregnancy;
        pregnancy.isPregnant = false;
        pregnancy.discovered = false;
        pregnancy.days = 0;
        pregnancy.father = {
            name: "Unknown",
            discovered: false,
        };
    };
    return PregnancyService;
}());
/* twine-user-script #93: "SexService.js" */
"use strict";
var SexService = /** @class */ (function () {
    function SexService() {
    }
    SexService.finishSex = function (npc, inside) {
        var pregnancy = game().player.pregnancy;
        var gameNpc = game().npc[npc];
        if (!gameNpc) {
            throw new Error("NPC ".concat(npc, " not found"));
        }
        if (QuestService.isQuestActive("WhoIsTheFather") && (gameNpc.gender == Gender.Male || gameNpc.gender == Gender.Transgender)) {
            openRandomEventModal("SpermCollect");
            game().location.hospital.sperm.push(gameNpc.name);
        }
        var boyfriendName = game().player.relationship.npcName;
        if (gameNpc.name === boyfriendName) {
            player().relationship.intimacy++;
        }
        else if (boyfriendName) {
            player().relationship.loyalty--;
        }
        NpcService.addRelation(npc);
        StatsService.addCorruption();
        StatsService.resetArousal();
        // Automatically reset NPC arousal and add corruption for family members (Dad, Brother, Grandpa)
        if (npc === "Dad" || npc === "Brother" || npc === "Grandpa") {
            game().npc[npc].arousal = 0;
            NpcService.addCorruption(npc);
        }
        if (inside) {
            player().statistics.creampies++;
        }
        if (!pregnancy.enabled || pregnancy.pillDays > 0 || pregnancy.isPregnant || !inside) {
            return;
        }
        if (rollTheDice(game().game.preferences.pregnancyChance)) {
            pregnancy.isPregnant = true;
            pregnancy.father = {
                name: gameNpc.name,
                discovered: false,
            };
            pregnancy.days = game().game.preferences.pregnancyDays;
            pregnancy.discovered = false;
            player().statistics.pregnancies++;
        }
    };
    SexService.finishMasturbation = function () {
        StatsService.addCorruption();
        StatsService.resetArousal();
        player().statistics.masturbations++;
    };
    return SexService;
}());
/* twine-user-script #94: "StatsService.js" */
"use strict";
var StatsService = /** @class */ (function () {
    function StatsService() {
    }
    StatsService.increaseArousal = function (npc, maxArousal) {
        npc.arousal = Math.min(npc.arousal + 1, maxArousal);
        CorruptionService.updateFamilyArousal();
        updateBar();
    };
    StatsService.addArousal = function () {
        if (galleryMode())
            return;
        var maxArousal = game().game.maxArousal;
        this.increaseArousal(game().player, maxArousal);
        createNotification("Arousal increased", "arousal");
    };
    StatsService.addInstafameFollowers = function (followers) {
        instafame().followers += followers;
        createNotification("You gained " + followers + " followers", NotificationType.SUCCESS);
    };
    StatsService.addEnergy = function (energyValue) {
        if (energyValue == 0) {
            game().player.energy = 0;
        }
        else {
            game().player.energy += energyValue;
        }
        EnergyService.checkEnergy();
        updateBar();
    };
    StatsService.improveMcMaximumStats = function () {
        try {
            var bonus = Math.floor(game().player.fitness / 10) * 10;
            var newMaxEnergy = 100 + bonus;
            var oldMaxEnergy = game().game.maxEnergy;
            if (newMaxEnergy > oldMaxEnergy) {
                var energyIncrease = newMaxEnergy - oldMaxEnergy;
                game().game.maxEnergy = newMaxEnergy;
                game().player.energy += energyIncrease;
                EnergyService.checkEnergy();
                createNotification("Maximum energy increased to " + newMaxEnergy, NotificationType.INFO);
                updateBar();
            }
        }
        catch (error) {
            var errorMessage = "Error in static improveMcMaximumStats: " + error;
            throw new Error(errorMessage);
        }
    };
    StatsService.resetPlayerStats = function () {
        try {
            game().player.energy = game().game.maxEnergy;
            game().player.drunkness = 0;
            if (game().player.arousal < game().game.maxArousal) {
                this.addArousal();
            }
            else {
                game().player.arousal = 10;
            }
            if (game().player.makeup) {
                game().player.makeup = false;
                if (game().player.beauty > 0) {
                    game().player.beauty--;
                }
            }
        }
        catch (error) {
            var errorMessage = "Error in static resetPlayerStats: " + error;
            throw new Error(errorMessage);
        }
    };
    StatsService.addMoney = function (value) {
        if (!Number.isInteger(value)) {
            var errorMessage = "Error in addMoney: Value is not an integer: " + value;
            throw new Error(errorMessage);
        }
        if (game().player.money + value >= 0) {
            game().player.money += value;
            if (value > 0) {
                createNotification("You earned $" + value, NotificationType.MONEY);
            }
            else if (value < 0) {
                createNotification("You paid $" + Math.abs(value), NotificationType.WARNING);
            }
            updateBar();
        }
    };
    StatsService.addCorruption = function () {
        if (!galleryMode() && game().player.corruption.points < 45) {
            game().player.corruption.points += 1;
            CorruptionService.updateCorruptionTitle();
            createNotification("Corruption increased", NotificationType.CORRUPTION);
            updateBar();
        }
    };
    StatsService.resetArousal = function () {
        if (galleryMode())
            return;
        game().player.arousal = 0;
        updateBar();
    };
    StatsService.getBeauty = function () {
        var _a, _b, _c;
        if (galleryMode())
            return 99;
        var drugModifier = (_c = (_b = (_a = game().player.drugs) === null || _a === void 0 ? void 0 : _a.modifiers) === null || _b === void 0 ? void 0 : _b.beauty) !== null && _c !== void 0 ? _c : 0;
        return Math.max(0, game().player.beauty + drugModifier);
    };
    StatsService.addDrunkness = function () {
        if (galleryMode())
            return;
        if (game().player.drunkness < 3) {
            game().player.drunkness += 1;
            createNotification("Drunkness increased", NotificationType.WARNING);
        }
        else {
            createNotification("You are very drunk!", NotificationType.WARNING);
        }
        CorruptionService.updateCorruptionTitle();
        updateBar();
    };
    StatsService.addSocial = function () {
        if (galleryMode())
            return;
        game().player.social += 1;
        createNotification("Social increased", NotificationType.INFO);
        updateBar();
    };
    StatsService.launderMoney = function (dirtyMoneyToLaunder) {
        var _a, _b;
        if (galleryMode())
            return;
        if (!dirtyMoneyToLaunder || isNaN(dirtyMoneyToLaunder) || dirtyMoneyToLaunder <= 0) {
            createNotification("Invalid amount to launder", NotificationType.WARNING);
            return;
        }
        dirtyMoneyToLaunder = Math.floor(dirtyMoneyToLaunder);
        if (game().player.dirtyMoney < dirtyMoneyToLaunder) {
            createNotification("Not enough dirty money to launder", NotificationType.WARNING);
            return;
        }
        // Get the cut percentage from laundry location (default 20% if not set)
        var cutPercentage = (_b = (_a = game().location.laundry) === null || _a === void 0 ? void 0 : _a.cut) !== null && _b !== void 0 ? _b : 20;
        var cut = cutPercentage / 100;
        // Calculate clean money after applying the cut
        var cleanMoney = Math.floor(dirtyMoneyToLaunder * (1 - cut));
        // Remove dirty money and add clean money
        game().player.dirtyMoney = Math.max(0, game().player.dirtyMoney - dirtyMoneyToLaunder);
        game().player.money += cleanMoney;
        var cutAmount = dirtyMoneyToLaunder - cleanMoney;
        createNotification("You laundered $" + dirtyMoneyToLaunder + " dirty money. Cut: $" + cutAmount + " (" + cutPercentage + "%). You received $" + cleanMoney + " clean money.", NotificationType.MONEY);
        updateBar();
    };
    return StatsService;
}());
/* twine-user-script #95: "PropertyService.js" */
"use strict";
var __assign = (this && this.__assign) || function () {
    __assign = Object.assign || function(t) {
        for (var s, i = 1, n = arguments.length; i < n; i++) {
            s = arguments[i];
            for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p))
                t[p] = s[p];
        }
        return t;
    };
    return __assign.apply(this, arguments);
};
/**
 * PropertyService - Manages all rentable and purchasable properties in the game
 * This service provides a generic way to handle different types of residences
 */
var PropertyService = /** @class */ (function () {
    function PropertyService() {
    }
    /**
     * Initialize all properties
     */
    PropertyService.initProperties = function () {
        try {
            var g_1 = game();
            g_1.properties = g_1.properties || {};
            this.propertyConfig.forEach(function (config) {
                var _a, _b, _c, _d;
                var existing = g_1.properties[config.id] || {};
                g_1.properties[config.id] = __assign(__assign({}, config), { status: existing.status || PropertyStatus.Available, daysUntilRent: (_a = existing.daysUntilRent) !== null && _a !== void 0 ? _a : config.rentCycleDays, accumulatedDebt: (_b = existing.accumulatedDebt) !== null && _b !== void 0 ? _b : 0, skippedRentCount: (_c = existing.skippedRentCount) !== null && _c !== void 0 ? _c : 0, hasLateFee: (_d = existing.hasLateFee) !== null && _d !== void 0 ? _d : false });
            });
        }
        catch (error) {
            throw new Error("initProperties failed: " + error);
        }
    };
    /**
     * Get a property by ID
     */
    PropertyService.getProperty = function (propertyId) {
        var _a;
        return (_a = game().properties) === null || _a === void 0 ? void 0 : _a[propertyId];
    };
    /**
     * Check if the player meets unlock requirements for a property (validation is per propertyId inside the service)
     */
    PropertyService.meetsUnlockRequirements = function (propertyId) {
        var _a, _b, _c;
        switch (propertyId) {
            case "apartment":
                return ((_c = (_b = (_a = game()) === null || _a === void 0 ? void 0 : _a.location) === null || _b === void 0 ? void 0 : _b.school) === null || _c === void 0 ? void 0 : _c.graduated) === true;
            default:
                return true;
        }
    };
    /**
     * Get all available properties that meet unlock requirements
     */
    PropertyService.getAvailableProperties = function () {
        var _this = this;
        var properties = game().properties || {};
        return Object.values(properties).filter(function (prop) {
            if (prop.status !== PropertyStatus.Available)
                return false;
            if (!_this.meetsUnlockRequirements(prop.id))
                return false;
            return true;
        });
    };
    /**
     * Get all properties the player is renting
     */
    PropertyService.getRentedProperties = function () {
        var properties = game().properties || {};
        return Object.values(properties).filter(function (prop) { return prop.status === PropertyStatus.Rented; });
    };
    /**
     * Get all properties the player owns
     */
    PropertyService.getOwnedProperties = function () {
        var properties = game().properties || {};
        return Object.values(properties).filter(function (prop) { return prop.status === PropertyStatus.Owned; });
    };
    /**
     * Check if a property can be rented/purchased
     */
    PropertyService.canAcquireProperty = function (propertyId) {
        try {
            var property = this.getProperty(propertyId);
            if (!property) {
                return { success: false, message: "Property not found!" };
            }
            if (property.status !== PropertyStatus.Available) {
                return { success: false, message: "This property is not available!" };
            }
            // Check unlock requirements (validated per propertyId inside the service)
            if (!this.meetsUnlockRequirements(propertyId)) {
                if (propertyId === "apartment") {
                    return { success: false, message: "I should finish school first before thinking about this..." };
                }
                return { success: false, message: "You don't meet the requirements for this property!" };
            }
            var p = player();
            if (p.money < property.price) {
                return { success: false, message: "You don't have enough money! ($".concat(property.price, " required)") };
            }
            return { success: true };
        }
        catch (error) {
            throw new Error("canAcquireProperty failed: " + error);
        }
    };
    /**
     * Rent a property
     */
    PropertyService.rentProperty = function (propertyId) {
        try {
            var check = this.canAcquireProperty(propertyId);
            if (!check.success) {
                createNotification(check.message, NotificationType.WARNING);
                return false;
            }
            var property = this.getProperty(propertyId);
            // Deduct the first payment
            player().money -= property.price;
            StatsService.addMoney(-property.price);
            // Update property status
            property.status = PropertyStatus.Rented;
            property.daysUntilRent = property.rentCycleDays;
            // Add to player's rented properties
            if (!player().residence.rentedProperties.includes(propertyId)) {
                player().residence.rentedProperties.push(propertyId);
            }
            // Unlock the location
            if (property.locationKey) {
                LocationService.unlockLocation(property.locationKey);
            }
            createNotification("You have rented the ".concat(property.name, "! Rent is $").concat(property.price, " per week."), NotificationType.SUCCESS);
            return true;
        }
        catch (error) {
            throw new Error("rentProperty failed: " + error);
        }
    };
    /**
     * Buy a property
     */
    PropertyService.buyProperty = function (propertyId) {
        try {
            var check = this.canAcquireProperty(propertyId);
            if (!check.success) {
                createNotification(check.message, NotificationType.WARNING);
                return false;
            }
            var property = this.getProperty(propertyId);
            // Deduct the purchase price
            player().money -= property.price;
            StatsService.addMoney(-property.price);
            // Update property status
            property.status = PropertyStatus.Owned;
            property.daysUntilRent = undefined; // No rent for owned properties
            // Add to player's owned properties
            if (!player().residence.ownedProperties.includes(propertyId)) {
                player().residence.ownedProperties.push(propertyId);
            }
            // Unlock the location
            if (property.locationKey) {
                LocationService.unlockLocation(property.locationKey);
            }
            createNotification("You have purchased the ".concat(property.name, "!"), NotificationType.SUCCESS);
            return true;
        }
        catch (error) {
            throw new Error("buyProperty failed: " + error);
        }
    };
    /**
     * Set the player's current residence
     */
    PropertyService.setCurrentResidence = function (propertyId) {
        player().residence.currentResidence = propertyId;
    };
    /**
     * Get the player's current residence
     */
    PropertyService.getCurrentResidence = function () {
        var _a;
        try {
            var p = player();
            return ((_a = p === null || p === void 0 ? void 0 : p.residence) === null || _a === void 0 ? void 0 : _a.currentResidence) || "house";
        }
        catch (_b) {
            return "house";
        }
    };
    /**
     * Check if player is living in a specific property
     */
    PropertyService.isLivingIn = function (propertyId) {
        return this.getCurrentResidence() === propertyId;
    };
    /**
     * Check if rent is due for a property
     */
    PropertyService.isRentDue = function (propertyId) {
        var property = this.getProperty(propertyId);
        if (!property)
            return false;
        if (property.type !== PropertyType.Rent)
            return false;
        if (property.status !== PropertyStatus.Rented)
            return false;
        return property.daysUntilRent === 0;
    };
    /**
     * Check if any rented property has rent due
     */
    PropertyService.hasAnyRentDue = function () {
        var rentedProperties = this.getRentedProperties();
        return rentedProperties.some(function (prop) { return prop.daysUntilRent === 0; });
    };
    /**
     * Get all properties with rent due
     */
    PropertyService.getPropertiesWithRentDue = function () {
        return this.getRentedProperties().filter(function (prop) { return prop.daysUntilRent === 0; });
    };
    /**
     * Decrement rent days for all rented properties (called in newDay)
     */
    PropertyService.decrementRentDays = function () {
        try {
            var rentedProperties = this.getRentedProperties();
            rentedProperties.forEach(function (prop) {
                if (prop.daysUntilRent !== undefined && prop.daysUntilRent > 0) {
                    prop.daysUntilRent--;
                }
            });
        }
        catch (error) {
            throw new Error("decrementRentDays failed: " + error);
        }
    };
    /**
     * Pay rent for a property (including accumulated debt and late fees)
     */
    PropertyService.payRent = function (propertyId) {
        try {
            var property = this.getProperty(propertyId);
            if (!property) {
                createNotification("Property not found!", NotificationType.WARNING);
                return false;
            }
            if (property.status !== PropertyStatus.Rented) {
                createNotification("You are not renting this property!", NotificationType.WARNING);
                return false;
            }
            var totalDue = this.getTotalRentDue(propertyId);
            var baseRent = property.price;
            var debt = property.accumulatedDebt || 0;
            var lateFee = this.getLateFeeAmount(propertyId);
            if (player().money < totalDue) {
                createNotification("You don't have enough money! You need $".concat(totalDue, " (Rent: $").concat(baseRent).concat(debt > 0 ? " + Debt: $".concat(debt) : '').concat(lateFee > 0 ? " + Late Fee: $".concat(lateFee) : '', ")"), NotificationType.WARNING);
                return false;
            }
            // Deduct total amount
            player().money -= totalDue;
            StatsService.addMoney(-totalDue);
            // Build payment message
            var paymentMessage = "You paid $".concat(totalDue);
            var parts = [];
            if (baseRent > 0)
                parts.push("Rent: $".concat(baseRent));
            if (debt > 0)
                parts.push("Debt: $".concat(debt));
            if (lateFee > 0)
                parts.push("Late Fee: $".concat(lateFee));
            if (parts.length > 1) {
                paymentMessage += " (".concat(parts.join(', '), ")");
            }
            else {
                paymentMessage += " for this week's rent.";
            }
            // Reset debt and penalties
            property.accumulatedDebt = 0;
            property.skippedRentCount = 0;
            property.hasLateFee = false;
            property.daysUntilRent = property.rentCycleDays;
            createNotification(paymentMessage, NotificationType.SUCCESS);
            return true;
        }
        catch (error) {
            throw new Error("payRent failed: " + error);
        }
    };
    /**
     * Skip rent payment (landlord agrees to wait, but accumulates debt and applies late fee)
     * Can only be used once - if already skipped, returns false
     */
    PropertyService.skipRent = function (propertyId) {
        var _a, _b;
        try {
            var property = this.getProperty(propertyId);
            if (!property || property.status !== PropertyStatus.Rented) {
                return false;
            }
            // Check if rent was already skipped (player can only skip once)
            if (property.skippedRentCount && property.skippedRentCount > 0) {
                var landlordName_1 = property.landlordKey
                    ? ((_a = game().npc[property.landlordKey]) === null || _a === void 0 ? void 0 : _a.name) || "The landlord"
                    : "The landlord";
                createNotification("".concat(landlordName_1, " already gave you an extension last time. You need to pay the rent now."), NotificationType.WARNING);
                return false;
            }
            var skippedAmount = property.price;
            // Accumulate debt
            property.accumulatedDebt = (property.accumulatedDebt || 0) + skippedAmount;
            // Increment skip counter
            property.skippedRentCount = (property.skippedRentCount || 0) + 1;
            // Apply late fee penalty (50% of rent added to next payment)
            property.hasLateFee = true;
            // Reset rent cycle
            property.daysUntilRent = property.rentCycleDays;
            var landlordName = property.landlordKey
                ? ((_b = game().npc[property.landlordKey]) === null || _b === void 0 ? void 0 : _b.name) || "The landlord"
                : "The landlord";
            var totalDebt = property.accumulatedDebt;
            var nextPayment = this.getTotalRentDue(propertyId);
            createNotification("".concat(landlordName, " agreed to wait, but you now owe $").concat(totalDebt, " in accumulated debt. Next payment will be $").concat(nextPayment, " (including 50% late fee)."), NotificationType.WARNING);
            return true;
        }
        catch (error) {
            throw new Error("skipRent failed: " + error);
        }
    };
    /**
     * Alternative payment (resets rent cycle without money)
     */
    PropertyService.alternativePayment = function (propertyId) {
        try {
            var property = this.getProperty(propertyId);
            if (property && property.status === PropertyStatus.Rented) {
                // Alternative payment settles the current rent obligation, including penalties
                property.accumulatedDebt = 0;
                property.hasLateFee = false;
                property.skippedRentCount = 0;
                property.daysUntilRent = property.rentCycleDays;
                createNotification("You have paid the rent for this week.", NotificationType.SUCCESS);
            }
        }
        catch (error) {
            throw new Error("alternativePayment failed: " + error);
        }
    };
    /**
     * Check if player can afford rent for a property (including debt and late fees)
     */
    PropertyService.canAffordRent = function (propertyId) {
        var totalDue = this.getTotalRentDue(propertyId);
        return player().money >= totalDue;
    };
    /**
     * Get base rent amount for a property (without debt or fees)
     */
    PropertyService.getRentAmount = function (propertyId) {
        var property = this.getProperty(propertyId);
        return (property === null || property === void 0 ? void 0 : property.price) || 0;
    };
    /**
     * Get accumulated debt for a property
     */
    PropertyService.getAccumulatedDebt = function (propertyId) {
        var property = this.getProperty(propertyId);
        return (property === null || property === void 0 ? void 0 : property.accumulatedDebt) || 0;
    };
    /**
     * Get late fee amount (50% of rent payment if hasLateFee is true)
     */
    PropertyService.getLateFeeAmount = function (propertyId) {
        var property = this.getProperty(propertyId);
        if (!property || !property.hasLateFee) {
            return 0;
        }
        return Math.floor(property.price * 0.5); // Late fee is 50% of rent payment
    };
    /**
     * Get total amount due (base rent + accumulated debt + late fee)
     */
    PropertyService.getTotalRentDue = function (propertyId) {
        var property = this.getProperty(propertyId);
        if (!property)
            return 0;
        var baseRent = property.price;
        var debt = property.accumulatedDebt || 0;
        var lateFee = this.getLateFeeAmount(propertyId);
        return baseRent + debt + lateFee;
    };
    /**
     * Check if property has accumulated debt
     */
    PropertyService.hasAccumulatedDebt = function (propertyId) {
        var property = this.getProperty(propertyId);
        return ((property === null || property === void 0 ? void 0 : property.accumulatedDebt) || 0) > 0;
    };
    /**
     * Check if property has late fee pending
     */
    PropertyService.hasLateFee = function (propertyId) {
        var property = this.getProperty(propertyId);
        return (property === null || property === void 0 ? void 0 : property.hasLateFee) || false;
    };
    /**
     * Get number of times rent was skipped
     */
    PropertyService.getSkippedRentCount = function (propertyId) {
        var property = this.getProperty(propertyId);
        return (property === null || property === void 0 ? void 0 : property.skippedRentCount) || 0;
    };
    /**
     * Get days until rent for a property
     */
    PropertyService.getDaysUntilRent = function (propertyId) {
        var _a;
        var property = this.getProperty(propertyId);
        return (_a = property === null || property === void 0 ? void 0 : property.daysUntilRent) !== null && _a !== void 0 ? _a : 7;
    };
    /**
     * Get landlord name for a property
     */
    PropertyService.getLandlordName = function (propertyId) {
        var _a;
        var property = this.getProperty(propertyId);
        if (!property || !property.landlordKey)
            return "The landlord";
        return ((_a = game().npc[property.landlordKey]) === null || _a === void 0 ? void 0 : _a.name) || "The landlord";
    };
    /**
     * Check if player has any property (rented or owned)
     */
    PropertyService.hasAnyProperty = function () {
        try {
            var p = player();
            if (!p || !p.residence)
                return false;
            return (p.residence.rentedProperties.length > 0 || p.residence.ownedProperties.length > 0);
        }
        catch (_a) {
            // Player not initialized yet, check properties directly
            var properties = game().properties || {};
            return Object.values(properties).some(function (prop) {
                return prop.status === PropertyStatus.Rented || prop.status === PropertyStatus.Owned;
            });
        }
    };
    /**
     * Check if player has a specific property (rented or owned)
     */
    PropertyService.hasProperty = function (propertyId) {
        try {
            var p = player();
            if (!p || !p.residence) {
                // Fallback: check property status directly
                var property = this.getProperty(propertyId);
                return property ? (property.status === PropertyStatus.Rented || property.status === PropertyStatus.Owned) : false;
            }
            return p.residence.rentedProperties.includes(propertyId) || p.residence.ownedProperties.includes(propertyId);
        }
        catch (_a) {
            // Player not initialized yet, check property status directly
            var property = this.getProperty(propertyId);
            return property ? (property.status === PropertyStatus.Rented || property.status === PropertyStatus.Owned) : false;
        }
    };
    /**
     * Unrent a property (terminate the lease)
     */
    PropertyService.unrentProperty = function (propertyId) {
        try {
            var property = this.getProperty(propertyId);
            if (!property) {
                createNotification("Property not found!", NotificationType.WARNING);
                return false;
            }
            if (property.status !== PropertyStatus.Rented) {
                createNotification("You are not renting this property!", NotificationType.WARNING);
                return false;
            }
            // Remove from player's rented properties
            var rentedIndex = player().residence.rentedProperties.indexOf(propertyId);
            if (rentedIndex > -1) {
                player().residence.rentedProperties.splice(rentedIndex, 1);
            }
            // Reset property status to Available
            property.status = PropertyStatus.Available;
            // Clear all debt and penalties
            property.accumulatedDebt = 0;
            property.hasLateFee = false;
            property.skippedRentCount = 0;
            property.daysUntilRent = property.rentCycleDays;
            // If this is the current residence, set it back to "house"
            if (this.getCurrentResidence() === propertyId) {
                this.setCurrentResidence("house");
            }
            createNotification("You have terminated the lease for the ".concat(property.name, "."), NotificationType.INFO);
            return true;
        }
        catch (error) {
            throw new Error("unrentProperty failed: " + error);
        }
    };
    /**
     * Master configuration for all properties in the game
     */
    PropertyService.propertyConfig = [
        {
            id: "apartment",
            name: "Apartment",
            type: PropertyType.Rent,
            price: 300,
            status: PropertyStatus.Available,
            rentCycleDays: 7,
            landlordKey: "Landlord",
            locationKey: "apartment",
            hallwayPassage: "ApartmentHallway"
        }
        // Future properties can be added here:
        // {
        //     id: "penthouse",
        //     name: "Luxury Penthouse",
        //     type: PropertyType.Buy,
        //     price: 50000,
        //     status: PropertyStatus.Available,
        //     rentCycleDays: 0,
        //     locationKey: "penthouse",
        //     hallwayPassage: "PenthouseHallway"
        // }
    ];
    return PropertyService;
}());
// Expose PropertyService to window for Twine access
window.PropertyService = PropertyService;
/* twine-user-script #96: "QuestService.js" */
"use strict";
var __assign = (this && this.__assign) || function () {
    __assign = Object.assign || function(t) {
        for (var s, i = 1, n = arguments.length; i < n; i++) {
            s = arguments[i];
            for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p))
                t[p] = s[p];
        }
        return t;
    };
    return __assign.apply(this, arguments);
};
var questDefinitions = [
    { id: 1, key: "Game", title: "Instafame", description: "I need to buy a phone and create an Instafame account", progress: 0, active: false, completed: false, repeatable: false, delayDays: null },
    { id: 2, key: "Jim", title: "Pornstar", description: "I should accept Jim's proposal", progress: 0, active: false, completed: false, repeatable: false, delayDays: null },
    { id: 3, key: "Richard", title: "BecomeAModel", description: "I should accept Richard's proposal", progress: 0, active: false, completed: false, repeatable: false, delayDays: null },
    { id: 4, key: "Edward", title: "SecretAdmirer", description: "I should accept Edward's proposal", progress: 0, active: false, completed: false, repeatable: false, delayDays: null },
    { id: 5, key: "Game", title: "WhoIsTheFather", description: "I need to collect sperm samples from the possible fathers", progress: 0, active: false, completed: false, repeatable: true, delayDays: null },
    { id: 6, key: "School", title: "FirstDayOfSchool", description: "It's my first day at school. I'm so nervous", progress: 0, active: false, completed: false, repeatable: false, delayDays: null },
    { id: 7, key: "School", title: "SchoolTest", description: "I need to take the school test on Monday", progress: 0, active: false, completed: false, repeatable: false, delayDays: null },
    { id: 8, key: "MathTeacher", title: "MathHomework", description: "I need to go to math class and turn in my homework", progress: 0, active: false, completed: false, repeatable: false, delayDays: null },
    { id: 9, key: "MathTeacher", title: "Tutoring", description: "I should get private tutoring from the math teacher", progress: 0, active: false, completed: false, repeatable: false, delayDays: null },
    { id: 10, key: "Coach", title: "Cheerleader", description: "Being a cheerleader must be amazing. I need to keep practicing until the coach notices me", progress: 0, active: false, completed: false, repeatable: false, delayDays: null },
    { id: 11, key: "Janitor", title: "Afterclass", description: "I should go to the classroom after class this evening", progress: 0, active: false, completed: false, repeatable: false, delayDays: null },
    { id: 12, key: "Marcus", title: "StudyWithMarcus", description: "I should go to Marcus's house and study with him", progress: 0, active: false, completed: false, repeatable: false, delayDays: null },
    { id: 13, key: "Natasha", title: "LibraryExhibitionism", description: "I should go to the library and talk to Natasha", progress: 0, active: false, completed: false, repeatable: false, delayDays: null },
    { id: 14, key: "Natasha", title: "PublicExhibitionism", description: "I should talk to Natasha. Maybe she has something new in mind", progress: 0, active: false, completed: false, repeatable: false, delayDays: null },
    { id: 15, key: "ComputerTeacher", title: "TeacherSecretFetish", description: "I need to buy and wear a school outfit with at least 30 corruption and use it for the teacher", progress: 0, active: false, completed: false, repeatable: false, delayDays: null },
    { id: 16, key: "Thomas", title: "ThomasParty", description: "I should ask Thomas if I can go to the party. I think I saw him in the hallway", progress: 0, active: false, completed: false, repeatable: true, delayDays: null },
    { id: 17, key: "Restaurant", title: "INeedMoney", description: "I should get a job, maybe at the restaurant?", progress: 0, active: false, completed: false, repeatable: false, delayDays: null },
    { id: 18, key: "Restaurant", title: "Promotion", description: "I need to work hard if I want a promotion. That would really help my finances", progress: 0, active: false, completed: false, repeatable: false, delayDays: null },
    { id: 19, key: "DrugDealer", title: "PackageDelivering", description: "I need to deliver this package. The address says 'Church.' That doesn't make much sense", progress: 0, active: false, completed: false, repeatable: false, delayDays: null },
    { id: 20, key: "Jamal", title: "PoolParty", description: "Jamal invited me to a pool party on Sunday. I should go", progress: 0, active: false, completed: false, repeatable: true, delayDays: null },
    { id: 21, key: "Matthew", title: "YachtTour", description: "Matthew invited me on a yacht tour. I should be at the beach early Saturday morning", progress: 0, active: false, completed: false, repeatable: true, delayDays: null },
    { id: 22, key: "Veronica", title: "CostumeParty", description: "Veronica sent me a message about a costume party. I should reply on my phone", progress: 0, active: false, completed: false, repeatable: false, delayDays: null },
    { id: 23, key: "Edward", title: "SecondDate", description: "I have a new message on Instafame. I should check it", progress: 0, active: false, completed: false, repeatable: false, delayDays: null },
    { id: 24, key: "Edward", title: "Threesome", description: "There's a new message on Instafame. I should check it", progress: 0, active: false, completed: false, repeatable: false, delayDays: null },
    { id: 25, key: "Richard", title: "SecondPhotoShoot", description: "Instafame pinged me with something new. I should open it", progress: 0, active: false, completed: false, repeatable: false, delayDays: null },
    { id: 26, key: "Marcus", title: "MarcusDate", description: "I have a new message on my phone. I should check it", progress: 0, active: false, completed: false, repeatable: false, delayDays: null },
    { id: 27, key: "Strange", title: "FakeId", description: "I should meet the guy from the alley and get a fake ID at the abandoned building in the Ghetto", progress: 0, active: false, completed: false, repeatable: false, delayDays: null }
];
var QuestService = /** @class */ (function () {
    function QuestService() {
    }
    QuestService.initQuests = function () {
        try {
            game().questList = game().questList || [];
            for (var _i = 0, questDefinitions_1 = questDefinitions; _i < questDefinitions_1.length; _i++) {
                var def = questDefinitions_1[_i];
                var quest = __assign({}, def);
                this.createQuest(quest);
            }
            this.initializeSidebarQuestState();
        }
        catch (error) {
            var msg = "InitQuests failed: " + error;
            throw new Error(msg);
        }
    };
    QuestService.createQuest = function (quest) {
        try {
            var existingQuest = this.getQuestById(quest.id);
            if (!existingQuest) {
                game().questList.push(quest);
                return;
            }
            var state = {
                active: existingQuest.active,
                completed: existingQuest.completed,
                progress: existingQuest.progress,
                delayDays: existingQuest.delayDays,
                startedOrder: existingQuest.startedOrder,
                description: existingQuest.description,
            };
            Object.assign(existingQuest, quest, state);
        }
        catch (error) {
            var msg = "createQuest failed: " + quest.title + ": " + error;
            throw new Error(msg);
        }
    };
    QuestService.initializeSidebarQuestState = function () {
        var _a, _b;
        game().game.pinnedQuestKey = (_a = game().game.pinnedQuestKey) !== null && _a !== void 0 ? _a : "";
        game().game.questStartCounter = (_b = game().game.questStartCounter) !== null && _b !== void 0 ? _b : 0;
        var nextStartOrder = game().game.questStartCounter;
        for (var _i = 0, _c = this.getActiveQuests(); _i < _c.length; _i++) {
            var quest = _c[_i];
            if (!quest.startedOrder || quest.startedOrder < 1) {
                nextStartOrder += 1;
                quest.startedOrder = nextStartOrder;
            }
        }
        game().game.questStartCounter = nextStartOrder;
        this.normalizePinnedQuest();
    };
    QuestService.getActiveQuests = function () {
        return game().questList.filter(function (quest) { return quest.active && (!quest.completed || quest.repeatable); });
    };
    QuestService.getNextQuestStartOrder = function () {
        var _a;
        game().game.questStartCounter = ((_a = game().game.questStartCounter) !== null && _a !== void 0 ? _a : 0) + 1;
        return game().game.questStartCounter;
    };
    QuestService.normalizePinnedQuest = function () {
        var pinnedQuestKey = game().game.pinnedQuestKey;
        if (!pinnedQuestKey) {
            return;
        }
        var pinnedQuest = game().questList.find(function (quest) { return quest.title === pinnedQuestKey; });
        if (!pinnedQuest || !this.isQuestActive(pinnedQuestKey)) {
            game().game.pinnedQuestKey = "";
        }
    };
    QuestService.getPinnedQuestKey = function () {
        this.normalizePinnedQuest();
        return game().game.pinnedQuestKey || "";
    };
    QuestService.pinQuest = function (questKey) {
        if (!this.isQuestActive(questKey)) {
            return;
        }
        game().game.pinnedQuestKey = questKey;
    };
    QuestService.clearPinnedQuest = function () {
        game().game.pinnedQuestKey = "";
    };
    QuestService.togglePinnedQuest = function (questKey) {
        if (this.getPinnedQuestKey() === questKey) {
            this.clearPinnedQuest();
            return;
        }
        this.pinQuest(questKey);
    };
    QuestService.isPinnedQuest = function (questKey) {
        return this.getPinnedQuestKey() === questKey && this.isQuestActive(questKey);
    };
    QuestService.getLatestActiveQuest = function () {
        var activeQuests = this.getActiveQuests();
        if (activeQuests.length === 0) {
            return null;
        }
        return activeQuests
            .slice()
            .sort(function (left, right) {
            var _a, _b;
            var leftOrder = (_a = left.startedOrder) !== null && _a !== void 0 ? _a : 0;
            var rightOrder = (_b = right.startedOrder) !== null && _b !== void 0 ? _b : 0;
            return rightOrder - leftOrder || right.id - left.id;
        })[0] || null;
    };
    QuestService.getSidebarQuest = function () {
        var pinnedQuestKey = this.getPinnedQuestKey();
        if (pinnedQuestKey) {
            return this.getQuestByKey(pinnedQuestKey);
        }
        return this.getLatestActiveQuest();
    };
    QuestService.scheduleQuest = function (questKey, delayDays) {
        try {
            var quest = this.getQuestByKey(questKey);
            if (this.isQuestAvailable(questKey)) {
                quest.delayDays = delayDays;
            }
        }
        catch (error) {
            var msg = "Cannot schedule quest " + questKey + ": " + error;
            throw new Error(msg);
        }
    };
    QuestService.checkScheduledQuests = function () {
        var quests = game().questList;
        for (var _i = 0, quests_1 = quests; _i < quests_1.length; _i++) {
            var quest = quests_1[_i];
            if (quest.delayDays && quest.delayDays > 0) {
                quest.delayDays -= 1;
                if (quest.delayDays === 0) {
                    quest.delayDays = null;
                    this.startQuest(quest.title);
                }
            }
        }
    };
    QuestService.getQuestById = function (id) {
        try {
            var quests = game().questList;
            if (quests) {
                return quests.find(function (q) { return q.id === id; });
            }
        }
        catch (error) {
            throw new Error("GetQuestById failed: " + error);
        }
    };
    QuestService.getQuestByKey = function (questKey) {
        try {
            var quest = game().questList.find(function (q) { return q.title === questKey; });
            if (!quest) {
                throw new Error("Quest not found with key: " + questKey);
            }
            return quest;
        }
        catch (error) {
            throw new Error("GetQuestByKey failed: " + error);
        }
    };
    QuestService.getQuestProgress = function (questKey) {
        var quest = this.getQuestByKey(questKey);
        return galleryMode() ? 99 : quest.progress;
    };
    QuestService.isQuestActive = function (questKey) {
        var quest = this.getQuestByKey(questKey);
        return quest.active && (!quest.completed || quest.repeatable);
    };
    QuestService.isQuestCompleted = function (questKey) {
        var quest = this.getQuestByKey(questKey);
        return !quest.active && quest.completed;
    };
    QuestService.isQuestAvailable = function (questKey) {
        var quest = this.getQuestByKey(questKey);
        return !quest.active && quest.delayDays == null && (!quest.completed || quest.repeatable);
    };
    QuestService.getQuestTitle = function (questKey) {
        var quest = this.getQuestByKey(questKey);
        return quest.title.replace(/([A-Z])/g, function (letter) { return " " + letter; }).trim();
    };
    QuestService.updateQuest = function (questKey, progress, description) {
        if (this.isQuestActive(questKey)) {
            var quest = this.getQuestByKey(questKey);
            quest.progress += progress;
            if (description != null && quest.description != description) {
                quest.description = description;
                createNotification("Quest ".concat(this.getQuestTitle(questKey), " has been updated!"), NotificationType.INFO);
            }
        }
    };
    QuestService.finishQuest = function (questKey) {
        if (this.isQuestActive(questKey)) {
            var quest = this.getQuestByKey(questKey);
            quest.completed = true;
            quest.active = false;
            this.normalizePinnedQuest();
            createNotification("Quest ".concat(this.getQuestTitle(questKey), " completed!"), NotificationType.INFO);
        }
    };
    QuestService.startQuest = function (questKey) {
        var _a;
        if (this.isQuestAvailable(questKey)) {
            var quest_1 = this.getQuestByKey(questKey);
            quest_1.active = true;
            quest_1.progress = 0;
            quest_1.startedOrder = this.getNextQuestStartOrder();
            quest_1.description = ((_a = questDefinitions.find(function (q) { return q.id === quest_1.id; })) === null || _a === void 0 ? void 0 : _a.description) || quest_1.description;
            var titleWithSpaces = this.getQuestTitle(questKey);
            createNotification("New quest available: " + titleWithSpaces, NotificationType.INFO);
            // Special handling for TeacherSecretFetish quest: check if player already owns required outfit
            if (questKey === "TeacherSecretFetish" && ClothService.hasSchoolClothWithCorruption(30)) {
                this.updateQuest("TeacherSecretFetish", 1, "I need to wear a school outfit with at least 30 corruption. Then I need to study in Computer Class and accept the teacher's help");
            }
        }
    };
    QuestService.cancelQuest = function (questKey, message) {
        var quest = this.getQuestByKey(questKey);
        if (this.isQuestActive(questKey)) {
            quest.active = false;
            quest.progress = 0;
            this.normalizePinnedQuest();
            createNotification(message, NotificationType.WARNING);
        }
    };
    /**
     * Cleanup quest UI when modal is closed
     */
    QuestService.cleanupQuestUI = function () {
        if (window.QuestUIController) {
            window.QuestUIController.cleanup();
        }
    };
    return QuestService;
}());
/* twine-user-script #97: "SceneService.js" */
"use strict";
var SceneService = /** @class */ (function () {
    function SceneService() {
    }
    SceneService.initScenes = function () {
        var _this = this;
        try {
            var locationScenes = [
                { id: 1, location: "house", key: "PizzaDelivery", title: "Pizza Delivery", chance: 33, guide: "Order pizza naked", requirementsMC: { exhibitionism: 0, corruption: 30 }, executedToday: false, unlocked: false, gallery: true, blowjob: true },
                { id: 2, location: "park", key: "JoggingFlash", title: "Jogging Flash", chance: 33, guide: "Jog at the park", requirementsMC: { exhibitionism: 15, corruption: 30 }, executedToday: false, unlocked: false, gallery: false },
                { id: 3, location: "park", key: "KidnapAtPark", title: "Kidnapped At Park", chance: 50, guide: "Jog at the park late at night", requirementsMC: { exhibitionism: 0, corruption: 0 }, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true },
                { id: 4, location: "park", key: "JoggingSex1", title: "Jogging Sex I", chance: 33, guide: "Jog with +30 corruption outfit and flash tits", requirementsMC: { exhibitionism: 15, corruption: 45 }, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true },
                { id: 5, location: "park", key: "JoggingSexPregnant", title: "Jogging Sex Pregnant", chance: 33, guide: "Jog with +30 corruption outfit and flash tits while being pregnant", requirementsMC: { exhibitionism: 15, corruption: 45 }, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true },
                { id: 6, location: "park", key: "JoggingSex2", title: "Jogging Sex II", chance: 33, guide: "Jog with +30 corruption outfit and flash tits", requirementsMC: { exhibitionism: 15, corruption: 45 }, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true },
                { id: 7, location: "beach", key: "SwimFlash", title: "Swim Flash", chance: 50, guide: "Swim at the beach", requirementsMC: { exhibitionism: 15, corruption: 30 }, executedToday: false, unlocked: false, gallery: false },
                { id: 8, location: "beach", key: "BikiniThief", title: "Bikini Thief", chance: 50, guide: "Wear a bikini at the beach", requirementsMC: { exhibitionism: 0, corruption: 0 }, executedToday: false, unlocked: false, gallery: false },
                { id: 9, location: "beach", key: "TouristsThreesome", title: "Tourists Threesome", chance: 50, guide: "Wear a bikini at the beach", requirementsMC: { exhibitionism: 0, corruption: 0 }, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true, threesome: true, anal: true },
                { id: 10, location: "beach", key: "SunbatheLotion", title: "Sunbathe Lotion", chance: 33, guide: "Wear a 30+ corruption bikini and sunbathe", requirementsMC: { exhibitionism: 0, corruption: 30 }, executedToday: false, unlocked: false, gallery: true },
                { id: 11, location: "beach", key: "JetSkiRide", title: "Jet Ski Ride", chance: 50, guide: "Go to the beach and pay for a jet ski ride", requirementsMC: { exhibitionism: 15, corruption: 30 }, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true, anal: true },
                { id: 12, location: "mall", key: "MallFlash", title: "Mall Flash", chance: 33, guide: "Visit the mall", requirementsMC: { exhibitionism: 10, corruption: 15 }, executedToday: false, unlocked: false, gallery: false },
                { id: 13, location: "mall", key: "DiscountSex", title: "Discount Sex", chance: 100, guide: "Ask for discount at the Tech Store", requirementsMC: { exhibitionism: 0, corruption: 30 }, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true },
                { id: 14, location: "mall", key: "MallCaughtFlashing", title: "Caught Flashing", chance: 33, guide: "Flash at the mall; get caught by security", requirementsMC: { exhibitionism: 10, corruption: 15 }, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true },
                { id: 15, location: "club", key: "ClubFlash", title: "Club Flash", chance: 50, guide: "Dance at the club", requirementsMC: { exhibitionism: 10, corruption: 15 }, executedToday: false, unlocked: false, gallery: false },
                { id: 16, location: "club", key: "ClubGloryHole", title: "Club Gloryhole", chance: 100, guide: "Go to the club bathroom cabin", requirementsMC: { exhibitionism: 0, corruption: 30 }, executedToday: false, unlocked: false, gallery: true, blowjob: true },
                { id: 17, location: "school", key: "ClassroomFlash", title: "Classroom Flash", chance: 50, guide: "Go to the classroom and socialize", requirementsMC: { exhibitionism: 10, corruption: 15 }, executedToday: false, unlocked: false, gallery: false },
                { id: 18, location: "school", key: "BathroomStudentSex", title: "Bathroom Student Sex", chance: 50, guide: "Flash the student in the male bathroom", requirementsMC: { exhibitionism: 0, corruption: 30 }, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true },
                { id: 19, location: "school", key: "BathroomFlash", title: "Bathroom Flash", chance: 50, guide: "Flash the student in the male bathroom", requirementsMC: { exhibitionism: 10, corruption: 15 }, executedToday: false, unlocked: false, gallery: false },
                { id: 20, location: "school", key: "MathHomework", title: "Math Homework", chance: 100, guide: "Deliver homework to teacher in classroom", requirementsMC: { exhibitionism: 0, corruption: 30 }, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true },
                { id: 21, location: "school", key: "TeacherTutoring", title: "Teacher Tutoring", chance: 100, guide: "Fail school test (score < 6)", requirementsMC: { exhibitionism: 0, corruption: 30 }, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true },
                { id: 22, location: "school", key: "Cheerleader", title: "Join the Cheerleaders", chance: 100, guide: "Get enough fitness in PE class", requirementsMC: { exhibitionism: 0, corruption: 30 }, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true },
                { id: 23, location: "school", key: "Afterclass", title: "Janitor Event", chance: 50, guide: "Finish tutoring quest; study in classroom after class", requirementsMC: { exhibitionism: 0, corruption: 0 }, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true },
                { id: 24, location: "school", key: "LibraryExhibitionism", title: "Library Exhibitionism", chance: 25, guide: "Go to the library and study, you must have at least 5 relation points with Natasha", requirementsMC: { exhibitionism: 10, corruption: 15 }, executedToday: false, unlocked: false, gallery: true },
                { id: 25, location: "school", key: "PublicExhibitionism", title: "Public Exhibitionism", chance: 100, guide: "Talk with Natasha in the library after 'Library Exhibitionism'", requirementsMC: { exhibitionism: 20, corruption: 30 }, executedToday: false, unlocked: false, gallery: true },
                { id: 26, location: "school", key: "TeacherSecretFetish", title: "Teacher Secret Fetish", chance: 100, guide: "Spy on the teacher's laptop in Computer Class", requirementsMC: { exhibitionism: 0, corruption: 30 }, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true },
                { id: 27, location: "school", key: "ClassLactation", title: "Class Lactation", chance: 100, guide: "Study at classroom while being pregnant", requirementsMC: { exhibitionism: 0, corruption: 0 }, executedToday: false, unlocked: false, gallery: false },
                { id: 28, location: "gym", key: "GymFlash", title: "Gym Flash", chance: 50, guide: "Visit the gym and workout", requirementsMC: { exhibitionism: 10, corruption: 15 }, executedToday: false, unlocked: false, gallery: false },
                { id: 29, location: "gym", key: "GymPersonalSex", title: "Gym Personal Sex", chance: 50, guide: "Visit the gym and workout", requirementsMC: { exhibitionism: 0, corruption: 30 }, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true },
                { id: 30, location: "gym", key: "GymShowerThreesome", title: "Gym Shower Threesome", chance: 33, guide: "Take a shower at the gym", requirementsMC: { exhibitionism: 0, corruption: 30 }, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true, threesome: true },
                { id: 31, location: "restaurant", key: "RestaurantInterviewSex", title: "Interview Scene", chance: 100, guide: "Seduce the boss at the restaurant interview", requirementsMC: { exhibitionism: 0, corruption: 30 }, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true },
                { id: 32, location: "restaurant", key: "RestaurantPromotionScene", title: "Promotion Scene", chance: 100, guide: "Work at restaurant and have at least 10 XP", requirementsMC: { exhibitionism: 0, corruption: 30 }, executedToday: false, unlocked: false, gallery: true, blowjob: true },
                { id: 33, location: "restaurant", key: "RestaurantFlash", title: "Work Flash", chance: 50, guide: "Work at the restaurant", requirementsMC: { exhibitionism: 10, corruption: 15 }, executedToday: false, unlocked: false, gallery: false },
                { id: 34, location: "restaurant", key: "RestaurantSpecialVisitSex", title: "Special Visit", chance: 100, guide: "Work in VIP section at restaurant with 25+ XP", requirementsMC: { exhibitionism: 0, corruption: 45 }, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true },
                { id: 35, location: "restaurant", key: "RestaurantGangbang", title: "Restaurant Gangbang", chance: 25, guide: "Work in VIP section at restaurant with 30+ XP", requirementsMC: { exhibitionism: 0, corruption: 45 }, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true, anal: true, gangbang: true, },
                { id: 36, location: "pool", key: "PoolFlash", title: "Pool Flash", chance: 33, guide: "Swim at the pool with a 30+ corruption bikini", requirementsMC: { exhibitionism: 15, corruption: 30 }, executedToday: false, unlocked: false, gallery: false },
                { id: 37, location: "pool", key: "PoolSwimSex", title: "Pool Swimming Sex", chance: 33, guide: "Swim at the pool with a 30+ corruption bikini and flash", requirementsMC: { exhibitionism: 15, corruption: 45 }, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true },
                { id: 38, location: "photoStudio", key: "ModelPhotoshoot", title: "Model Photoshoot", chance: 100, guide: "Have 500+ Instafame followers; read your DMs", requirementsMC: { exhibitionism: 0, corruption: 0 }, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true },
                { id: 39, location: "stripclub", key: "StripClubInterview", title: "Strip Club Interview", chance: 100, guide: "Apply for a job at the strip club", requirementsMC: { exhibitionism: 0, corruption: 45 }, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true },
                { id: 40, location: "stripclub", key: "StripClubPrivate1", title: "Private Session I", chance: 25, guide: "Work at the strip club; get a client", requirementsMC: { exhibitionism: 0, corruption: 45 }, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true },
                { id: 41, location: "stripclub", key: "StripClubStage1", title: "Stage Session I", chance: 25, guide: "Work at the strip club; get a client", requirementsMC: { exhibitionism: 0, corruption: 45 }, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true },
                { id: 42, location: "bus", key: "BusFlash", title: "Bus Flash", chance: 50, guide: "Ride the bus and flash", requirementsMC: { exhibitionism: 10, corruption: 0 }, executedToday: false, unlocked: false, gallery: false },
                { id: 43, location: "bus", key: "BusMasturbate", title: "Bus Masturbate", chance: 33, guide: "Ride the bus and masturbate the strange guy", requirementsMC: { exhibitionism: 0, corruption: 30 }, executedToday: false, unlocked: false, gallery: false },
                { id: 44, location: "bus", key: "BusGrope", title: "Bus Grope", chance: 33, guide: "Ride the bus", requirementsMC: { exhibitionism: 0, corruption: 0 }, executedToday: false, unlocked: false, gallery: false },
                { id: 45, location: "policeDep", key: "HouseRobPrison", title: "House Robbing", chance: 100, guide: "Rob a house with the Vipers", requirementsMC: { exhibitionism: 0, corruption: 30 }, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true },
                { id: 46, location: "thomasHouse", key: "ThomasPartyPongSex", title: "Beer Pong Sex", chance: 33, guide: "Go to Thomas's party; play beer pong", requirementsMC: { exhibitionism: 0, corruption: 30 }, executedToday: false, unlocked: false, gallery: true, vaginal: true },
                { id: 47, location: "thomasHouse", key: "ThomasPartySpinTheBottle", title: "Spin Bottle Group Sex", chance: 33, guide: "Go to Thomas's party; go to the second floor", requirementsMC: { exhibitionism: 0, corruption: 30 }, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true, anal: true, gangbang: true },
                { id: 48, location: "office", key: "OfficeInterview", title: "Office Interview", chance: 100, guide: "Apply for a job at the office", requirementsMC: { exhibitionism: 0, corruption: 30 }, executedToday: false, unlocked: false, gallery: true, anal: true, vaginal: true },
                { id: 49, location: "office", key: "SecretarySex", title: "Secretary Sex", chance: 25, guide: "Work at the office", requirementsMC: { exhibitionism: 0, corruption: 0 }, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true },
                { id: 50, location: "abandonedBuilding", key: "HomelessThreesome", title: "Homeless Threesome", chance: 33, guide: "Escape from class with Natasha", requirementsMC: { exhibitionism: 20, corruption: 30 }, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true, threesome: true },
                { id: 51, location: "hospital", key: "PrenatalCareBigBelly", title: "Prenatal Care Big Belly", chance: 100, guide: "Get pregnant and go to the hospital for prenatal care and have 3 relation points with the Doctor", requirementsMC: { exhibitionism: 0, corruption: 30 }, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true },
                { id: 52, location: "hospital", key: "GynecologicalExam", title: "Gynecological Exam", chance: 100, guide: "Go to the hospital and do the gynecological exam and have 3 relation points with the Doctor", requirementsMC: { exhibitionism: 0, corruption: 30 }, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true, anal: true },
                { id: 53, location: "clandestineClinic", key: "ArtificialInsemination", title: "Artificial Insemination", chance: 100, guide: "If you lose your baby during childbirth, your doctor will give you the address of a clinic that can help you with artificial insemination", requirementsMC: { exhibitionism: 0, corruption: 0 }, executedToday: false, unlocked: false, gallery: true },
                { id: 54, location: "clandestineClinic", key: "SexualInsemination", title: "Sexual Insemination", chance: 100, guide: "After attempting artificial insemination, return to the clinic to check the result", requirementsMC: { exhibitionism: 0, corruption: 30 }, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true },
                { id: 55, location: "bar", key: "BarRandomSex1", title: "Bar Random Sex 1", chance: 25, guide: "Go to the bar and drink until you get drunk", requirementsMC: { exhibitionism: 0, corruption: 30 }, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true },
                { id: 56, location: "photoStudio", key: "SecondPhotoShoot", title: "Second Photo Shoot", chance: 100, guide: "Wait 15 days after the first photoshoot", requirementsMC: { exhibitionism: 0, corruption: 30 }, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true, threesome: true },
                { id: 57, location: "park", key: "ParkGangbang", title: "Park Gangbang", chance: 33, guide: "Jog at the park late at night", requirementsMC: { exhibitionism: 0, corruption: 0 }, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true, anal: true, gangbang: true },
                { id: 58, location: "gasStation", key: "CarWashChallenge", title: "Car Wash Challenge", chance: 100, guide: "Get the car wash challenge at Naked Life App", requirementsMC: { exhibitionism: 20, corruption: 30 }, executedToday: false, unlocked: false, gallery: true, blowjob: false, vaginal: false, anal: false, gangbang: false },
                { id: 59, location: "park", key: "ParkChallenge", title: "Park Challenge", chance: 100, guide: "Get the park challenge at Naked Life App", requirementsMC: { exhibitionism: 20, corruption: 30 }, executedToday: false, unlocked: false, gallery: true, blowjob: false, vaginal: false, anal: false, gangbang: false },
                { id: 60, location: "center", key: "StreetChallenge1", title: "Street Challenge I", chance: 100, guide: "Get the Street Challenge I at Naked Life App", requirementsMC: { exhibitionism: 30, corruption: 45 }, executedToday: false, unlocked: false, gallery: true, blowjob: false, vaginal: false, anal: false, gangbang: false },
                { id: 61, location: "beach", key: "BeachChallenge1", title: "Beach Challenge I", chance: 100, guide: "Get the Beach Challenge I at Naked Life App", requirementsMC: { exhibitionism: 30, corruption: 30 }, executedToday: false, unlocked: false, gallery: true, blowjob: false, vaginal: false, anal: false, gangbang: false },
                { id: 62, location: "beach", key: "BeachStrangeSex1", title: "Beach Strange Sex I", chance: 33, guide: "Go to the beach and wear a bikini", requirementsMC: { exhibitionism: 0, corruption: 30 }, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true },
                { id: 63, location: "drivingSchool", key: "DrivingSchoolExamSex", title: "Driving School Exam Sex", chance: 50, guide: "Take a practical lesson at the driving school", requirementsMC: { exhibitionism: 0, corruption: 30 }, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true },
                { id: 64, location: "movieTheater", key: "MovieTheaterGrope1", title: "Movie Theater Grope I", chance: 25, guide: "Go to the movie theater and watch a movie", requirementsMC: { exhibitionism: 0, corruption: 30 }, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: false },
                { id: 65, location: "movieTheater", key: "MovieTheaterGrope2", title: "Movie Theater Grope II", chance: 25, guide: "Go to the movie theater and watch a movie", requirementsMC: { exhibitionism: 0, corruption: 30 }, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: false },
                { id: 66, location: "bar", key: "BarThreesome", title: "Bar Threesome", chance: 25, guide: "Go to the bar and work", requirementsMC: { exhibitionism: 0, corruption: 30 }, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true, threesome: true },
                { id: 67, location: "bar", key: "BarBathroomSex", title: "Bar Bathroom Sex", chance: 25, guide: "Go to the bar and drink until you get drunk", requirementsMC: { exhibitionism: 0, corruption: 30 }, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true },
                { id: 68, location: "school", key: "LibraryTransSex", title: "Library Trans Sex", chance: 25, guide: "Go to the library and study", requirementsMC: { exhibitionism: 0, corruption: 30 }, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true },
                { id: 69, location: "bar", key: "OldManBarSex", title: "Old Man Bar Sex", chance: 25, guide: "Go to the bar and work as a bartender at late night", requirementsMC: { exhibitionism: 0, corruption: 30 }, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true },
                { id: 70, location: "park", key: "PoliceParkGangbang", title: "Police Park Gangbang", chance: 25, guide: "Flash your breasts at park at least one time and go jog", requirementsMC: { exhibitionism: 0, corruption: 0 }, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true },
                { id: 71, location: "park", key: "ParkRestLiftSkirt", title: "Park Rest Lift Skirt", chance: 33, guide: "Rest at the park and a boy lifts your skirt", requirementsMC: { exhibitionism: 0, corruption: 0 }, executedToday: false, unlocked: false, gallery: false, blowjob: false, vaginal: false }
            ];
            locationScenes.forEach(function (scene) {
                _this.createLocationScene(scene);
            });
            var playerScenes = [
                { id: 1, key: "XCam", title: "Stream at XCam", chance: 100, guide: "Buy laptop/webcam; stream at xCam", requirementsMC: { exhibitionism: 0, corruption: 45 }, executedToday: false, unlocked: false, gallery: true },
                { id: 2, key: "BathroomLactation", title: "Bathroom Lactation", chance: 33, guide: "Go to the bathroom at the house while being pregnant", requirementsMC: {}, executedToday: false, unlocked: false, gallery: true },
                { id: 3, key: "XCamBlackmail", title: "XCam Blackmail", chance: 20, guide: "Stream at last 5 times at xCam and go to your house at night or late night", requirementsMC: {}, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true },
                { id: 4, key: "HouseCleaning1", title: "House Cleaning", chance: 33, guide: "Get the house cleaning job at FastJobs app", requirementsMC: { exhibitionism: 0, corruption: 30 }, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true },
                { id: 5, key: "DogWalking", title: "Dog Walking", chance: 33, guide: "Get the dog wallking job at FastJobs app", requirementsMC: { exhibitionism: 0, corruption: 30 }, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true },
                { id: 6, key: "BabySitting", title: "Baby Sitting", chance: 100, guide: "Get the baby sitting job at FastJobs app", requirementsMC: { exhibitionism: 0, corruption: 30 }, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true },
                { id: 7, key: "ElderlyCare", title: "Elderly Care", chance: 100, guide: "Get the elderly care job at FastJobs app", requirementsMC: { exhibitionism: 0, corruption: 30 }, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true },
                { id: 8, key: "BedroomMasturbate1", title: "Bedroom Masturbate I", chance: 100, guide: "Masturbate in your bedroom", requirementsMC: {}, executedToday: false, unlocked: false, gallery: true },
                { id: 9, key: "HouseCleaning2", title: "House Cleaning II", chance: 33, guide: "Get the house cleaning job at FastJobs app", requirementsMC: { exhibitionism: 0, corruption: 30 }, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true },
                { id: 10, key: "xCamPizzaDelivery", title: "xCam Pizza Delivery", chance: 33, guide: "Stream at xCam and accept the challenge of your viewer", requirementsMC: { exhibitionism: 0, corruption: 45 }, executedToday: false, unlocked: false, gallery: true, blowjob: true },
                { id: 11, key: "SchoolBathroomMasturbate", title: "School Bathroom Masturbate", chance: 100, guide: "Masturbate in the school bathroom", requirementsMC: {}, executedToday: false, unlocked: false, gallery: false, blowjob: false, vaginal: false }
            ];
            playerScenes.forEach(function (scene) {
                _this.createPlayerScene(scene);
            });
            var npcScenes = [
                { id: 1, npc: "Dad", key: "DadBedroomGrope", title: "$npc.Dad.relationship Bedroom Grope", chance: 20, guide: "Go to your bedroom", requirements: { arousal: "🔥", corruption: 0 }, requirementsMC: {}, executedToday: false, unlocked: false, gallery: false },
                { id: 2, npc: "Dad", key: "BedroomStudyDadGrope", title: "$npc.Dad.relationship Bedroom Study Grope", chance: 20, guide: "Study in your bedroom", requirements: { arousal: "🔥", corruption: 1 }, requirementsMC: {}, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true },
                { id: 3, npc: "Dad", key: "BedroomSleepDadScene", title: "$npc.Dad.relationship Bedroom Sleep", chance: 25, guide: "Sleep in your bedroom", requirements: { arousal: "🔥", corruption: 1 }, requirementsMC: {}, executedToday: false, unlocked: false, gallery: true, vaginal: true },
                { id: 4, npc: "Dad", key: "ShowerFlash", title: "Shower Exhibitionism", chance: 50, guide: "Take a shower in the house bathroom", requirements: { arousal: "🔥", corruption: 1 }, requirementsMC: { exhibitionism: 0, corruption: 5 }, executedToday: false, unlocked: false, gallery: false },
                { id: 5, npc: "Dad", key: "ProstituteSex", title: "$npc.Dad.relationship Prostitute Sex", chance: 25, guide: "Go to $npc.Dad.relationship's bedroom when he is at the bedroom", requirements: {}, requirementsMC: {}, executedToday: false, unlocked: false, gallery: false },
                { id: 6, npc: "Dad", key: "DadWashDishesSex", title: "$npc.Dad.relationship Washing Dishes Sex", chance: 20, guide: "Go to the kitchen and wash the dishes", requirements: { arousal: "🔥🔥", corruption: 10 }, requirementsMC: {}, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true },
                { id: 7, npc: "Dad", key: "DadWashDishesSexPregnant", title: "$npc.Dad.relationship Washing Dishes Pregnant Sex", chance: 20, guide: "Go to the kitchen and wash the dishes", requirements: { arousal: "🔥🔥", corruption: 10 }, requirementsMC: {}, executedToday: false, unlocked: false, gallery: true, vaginal: true },
                { id: 8, npc: "Dad", key: "DadShowerSex", title: "$npc.Dad.relationship's Shower Sex", chance: 33, guide: "Go to the bathroom at early morning", requirements: { arousal: "🔥🔥🔥", corruption: 15 }, requirementsMC: { exhibitionism: 0, corruption: 30 }, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true },
                { id: 9, npc: "Dad", key: "DadShowerSexPregnant", title: "$npc.Dad.relationship's Shower Sex Pregnant", chance: 33, guide: "Go to the bathroom at early morning while being pregnant", requirements: { arousal: "🔥🔥🔥", corruption: 15 }, requirementsMC: { exhibitionism: 0, corruption: 35 }, executedToday: false, unlocked: false, gallery: true, vaginal: true },
                { id: 10, npc: "Dad", key: "DadPeepSex", title: "Peeping $npc.Dad.relationship's Shower", chance: 25, guide: "Go to the bathroom while he is in the shower", requirements: {}, requirementsMC: { corruption: 15 }, executedToday: false, unlocked: false, gallery: true },
                { id: 11, npc: "Dad", key: "EatSex", title: "Eating Sex", chance: 33, guide: "Eat at the kitchen", requirements: { arousal: "🔥🔥", corruption: 10 }, requirementsMC: {}, executedToday: false, unlocked: false, gallery: true, vaginal: true },
                { id: 12, npc: "Dad", key: "DadPeepSexBedroom", title: "Peeping $npc.Dad.relationship with a prostitute", chance: 33, guide: "Go to $npc.Dad.relationship's bedroom when he is at the bedroom", requirements: { arousal: "🔥🔥", corruption: 10 }, requirementsMC: { corruption: 30 }, executedToday: false, unlocked: false, gallery: true },
                { id: 13, npc: "Brother", key: "BrotherBedroomGrope", title: "$npc.Brother.relationship Bedroom Grope", chance: 20, guide: "Go to your bedroom", requirements: { arousal: "🔥", corruption: 0 }, requirementsMC: {}, executedToday: false, unlocked: false, gallery: false },
                { id: 14, npc: "Brother", key: "BedroomStudyBrotherGrope", title: "$npc.Brother.relationship Bedroom Study Grope", chance: 20, guide: "Study at your room", requirements: { arousal: "🔥", corruption: 1 }, requirementsMC: {}, executedToday: false, unlocked: false, gallery: true },
                { id: 15, npc: "Brother", key: "BedroomStudyBrotherGropePregnant", title: "$npc.Brother.relationship Bedroom Study Grope Pregnant", chance: 20, guide: "Study at your room while being pregnant", requirements: { arousal: "🔥", corruption: 1 }, requirementsMC: { corruption: 30 }, executedToday: false, unlocked: false, gallery: true, vaginal: true },
                { id: 16, npc: "Brother", key: "SleepingBrother", title: "Sleep with $npc.Brother.relationship", chance: 100, guide: "Go to $npc.Brother.relationship bedroom late at night and ask to sleep with him", requirements: { arousal: "🔥", corruption: 10, relation: 10 }, requirementsMC: { corruption: 30 }, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true },
                { id: 17, npc: "Brother", key: "BrotherBedroomFlash", title: "$npc.Brother.relationship Bedroom Flash", chance: 100, guide: "Go to your $npc.Brother.relationship bedroom", requirements: {}, requirementsMC: { corruption: 5 }, executedToday: false, unlocked: false, gallery: true },
                { id: 18, npc: "Brother", key: "BrotherBedroomTease", title: "Bedroom Tease", chance: 100, guide: "Go to your $npc.Brother.relationship bedroom", requirements: {}, requirementsMC: { corruption: 5 }, executedToday: false, unlocked: false, gallery: true },
                { id: 19, npc: "Brother", key: "BrotherShowerSex", title: "$npc.Brother.relationship Shower Sex", chance: 33, guide: "Masturbate at shower at the house bathroom", requirements: { arousal: "🔥", corruption: 5 }, requirementsMC: { corruption: 30 }, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true },
                { id: 20, npc: "Brother", key: "PeepBrotherSex", title: "Peep $npc.Brother.relationship sex", chance: 25, guide: "Go to your $npc.Brother.relationship bedroom", requirements: {}, requirementsMC: { corruption: 15 }, executedToday: false, unlocked: false, gallery: true },
                { id: 21, npc: "Brother", key: "PlayingGamesSexPregnant", title: "Playing Videogame Pregnant with $npc.Brother.relationship", chance: 20, guide: "Play videogame at your living room while being pregnant", requirements: { arousal: "🔥🔥", corruption: 10 }, requirementsMC: { corruption: 30 }, executedToday: false, unlocked: false, gallery: true, vaginal: true },
                { id: 22, npc: "Brother", key: "PlayingGamesSex", title: "Playing Videogame", chance: 20, guide: "Play videogame at your living room", requirements: { arousal: "🔥🔥", corruption: 10 }, requirementsMC: { corruption: 30 }, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true },
                { id: 23, npc: "Brother", key: "BrotherHelpStudy", title: "Brother Help Study", chance: 20, guide: "Study at your room", requirements: { arousal: "🔥🔥🔥", corruption: 15 }, requirementsMC: {}, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true },
                { id: 24, npc: "Brother", key: "BrotherCaughtMasturbating", title: "Brother Caught Masturbating", chance: 25, guide: "Go to your $npc.Brother.relationship bedroom", requirements: { arousal: "🔥🔥", corruption: 10 }, requirementsMC: { corruption: 30 }, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true },
                { id: 25, npc: "Grandpa", key: "GarageDrunk", title: "Garage Drunk", chance: 50, guide: "Go to your house at late night and very drunk", requirements: {}, requirementsMC: {}, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true },
                { id: 26, npc: "Grandpa", key: "GrandpaMagazine", title: "$npc.Grandpa.relationship Magazines", chance: 100, guide: "Go to the living room at morning and talk with $npc.Grandpa.relationship", requirements: { arousal: "🔥🔥" }, requirementsMC: { corruption: 30 }, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true },
                { id: 27, npc: "Grandpa", key: "GrandpaShowerSex", title: "$npc.Grandpa.relationship Shower Sex", chance: 25, guide: "Go to the shower when your $npc.Grandpa.relationship is there", requirements: { arousal: "🔥🔥" }, requirementsMC: { corruption: 30 }, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true },
                { id: 28, npc: "Veronica", key: "VeronicaMeet", title: "Meet Veronica", chance: 33, guide: "Go to the bar and drink until you get drunk", requirements: {}, requirementsMC: { corruption: 30 }, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true },
                { id: 29, npc: "Veronica", key: "VeronicaFirstVisit", title: "Visit Veronica", chance: 100, guide: "Visit Veronica at her house in the evening", requirements: {}, requirementsMC: { corruption: 30 }, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true },
                { id: 30, npc: "Veronica", key: "VeronicaCostumeParty", title: "Costume Party", chance: 100, guide: "After visiting Veronica, wait two weeks", requirements: {}, requirementsMC: { corruption: 30 }, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true },
                { id: 31, npc: "Jamal", key: "JamalMeet", title: "Meeting Jamal", chance: 33, guide: "Go to the club and dance", requirements: {}, requirementsMC: { corruption: 30 }, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true },
                { id: 32, npc: "Jamal", key: "JamalBilliardsSex", title: "Playing Billiards", chance: 33, guide: "Go to the jamal house at saturday afternoon", requirements: {}, requirementsMC: { corruption: 30 }, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true },
                { id: 33, npc: "Jamal", key: "JamalPoolGangbang", title: "Pool Gangbang", chance: 100, guide: "Receive an message at friday from Jamal inviting you to his house after playing billiards with him", requirements: {}, requirementsMC: { corruption: 45 }, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true, gangbang: true },
                { id: 34, npc: "Emma", key: "SexPlaying", title: "Playing with Emma", chance: 33, guide: "Play with Emma until she invites you to her house", requirements: {}, requirementsMC: { corruption: 30 }, executedToday: false, unlocked: false, gallery: true },
                { id: 35, npc: "Marcus", key: "StudyWithMarcus", title: "Study With Marcus", chance: 100, guide: "Take the test and get at least an 8 grade", requirements: {}, requirementsMC: { corruption: 30 }, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true },
                { id: 36, npc: "Sam", key: "BathroomSurprise", title: "Bathroom Surprise", chance: 33, guide: "Go to the bathroom at Marcus's house", requirements: {}, requirementsMC: { corruption: 30 }, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true },
                { id: 37, npc: "Sam", key: "CaughtMasturbating", title: "Caught Masturbating", chance: 25, guide: "Go to the Sam's bedroom at Marcus's House", requirements: {}, requirementsMC: { corruption: 30 }, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true },
                { id: 38, npc: "Priest", key: "ConfessionSex", title: "Sex in the confessional", chance: 25, guide: "Go to church and confess your sins", requirements: {}, requirementsMC: { corruption: 45 }, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true },
                { id: 39, npc: "Priest", key: "PriestVisit", title: "Priest Visit", chance: 100, guide: "After confessing your sins, go to the church and visit the priest", requirements: {}, requirementsMC: { corruption: 45 }, executedToday: false, unlocked: false, gallery: true, blowjob: true, anal: true },
                { id: 40, npc: "Gangster", key: "DarkAlleyRape1", title: "Dark Alley Scene", chance: 33, guide: "Go to the dark alley late at night", requirements: {}, requirementsMC: { corruption: 0 }, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true },
                { id: 41, npc: "TowTruckDriver", key: "TyreFixSex", title: "Tyre Fix", chance: 50, guide: "Go to the Thomas's party with your $npc.Dad.relationship's car", requirements: {}, requirementsMC: { corruption: 0 }, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true },
                { id: 42, npc: "Edward", key: "SecretAdmirer", title: "Secret Admirer", chance: 100, guide: "Reach 1000 followers on Instafame and read your dm", requirements: {}, requirementsMC: { corruption: 30 }, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true },
                { id: 43, npc: "Edward", key: "SecretAdmirerPregnant", title: "Secret Admirer Pregnant", chance: 100, guide: "Reach 1000 followers on Instafame and read your dm. (Visit Edward on Hotel while being pregnant.)", requirements: {}, requirementsMC: { corruption: 30 }, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true },
                { id: 44, npc: "Matthew", key: "YachtTour", title: "Yacht Tour", chance: 33, guide: "Work at stripclub and meet Matthew", requirements: {}, requirementsMC: { corruption: 30 }, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true },
                { id: 45, npc: "YachtCaptain", key: "YachtCaptainSex", title: "Yacht Sex", chance: 33, guide: "Go to the beach at saturday after Matthew invite you to a yacht tour", requirements: {}, requirementsMC: { corruption: 30 }, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true },
                { id: 46, npc: "Thief", key: "ThiefFlashing", title: "Thief Flashing", chance: 10, guide: "Go to any zone (residential, city center, etc) late at night and have less than 100$", requirements: {}, requirementsMC: {}, executedToday: false, unlocked: false, gallery: false },
                { id: 47, npc: "Thief", key: "LightningKidnapping", title: "Lightning Kidnapping", chance: 5, guide: "Go to any zone (residential, city center, etc) at anytime", requirements: {}, requirementsMC: {}, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true },
                { id: 48, npc: "Josh", key: "SellingMyStepsister", title: "Selling my $npc.Brother.player", chance: 33, guide: "Make your $npc.Brother.relationship have at least 10 corruption and go to his room while he is home", requirements: {}, requirementsMC: { corruption: 30 }, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true },
                { id: 49, npc: "Edward", key: "SecondDate", title: "Second Date", chance: 100, guide: "After the first date with Edward, wait 10 days and read his message", requirements: {}, requirementsMC: { corruption: 30 }, executedToday: false, unlocked: false, gallery: true },
                { id: 50, npc: "Edward", key: "EdwardThreesome", title: "Edward Threesome", chance: 100, guide: "After the second date with Edward, wait 15 days and read his message", requirements: {}, requirementsMC: { corruption: 45 }, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true, threesome: true },
                { id: 51, npc: "Marcus", key: "MarcusParkSex", title: "Marcus Park Sex", chance: 100, guide: "Have at least 15 relationship points with Marcus, wait for his invite and go to the date with him", requirements: {}, requirementsMC: { corruption: 30 }, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true },
                { id: 52, npc: "Marcus", key: "MarcusBedroomSex1", title: "Marcus Bedroom Sex 1", chance: 100, guide: "After starting a relationship with Marcus, go to his bedroom and have sex with him", requirements: {}, requirementsMC: {}, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true },
                { id: 53, npc: "Marcus", key: "MarcusBedroomSexPregnant", title: "Marcus Bedroom Sex Pregnant", chance: 100, guide: "After starting a relationship with Marcus, go to his bedroom and have sex with him while being pregnant", requirements: {}, requirementsMC: {}, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true },
                { id: 54, npc: "Marcus", key: "MarcusClassSex", title: "Marcus Class Sex", chance: 30, guide: "After starting a relationship with Marcus, go to the classroom and study", requirements: {}, requirementsMC: {}, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true },
                { id: 55, npc: "Grandpa", key: "GrandpaBedroomSex", title: "$npc.Grandpa.relationship Bedroom Sex", chance: 100, guide: "Go to your $npc.Grandpa.relationship bedroom when he is at here", requirements: { arousal: "🔥" }, requirementsMC: { corruption: 45 }, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true },
                { id: 56, npc: "Grandpa", key: "GrandpaExerciseSex", title: "$npc.Grandpa.relationship Exercise Sex", chance: 33, guide: "Exercise at the living room when your $npc.Grandpa.relationship is here", requirements: { arousal: "🔥" }, requirementsMC: { corruption: 45 }, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true },
                { id: 57, npc: "Grandpa", key: "GrandpaKitchenSex", title: "$npc.Grandpa.relationship Kitchen Sex", chance: 33, guide: "Go to the kitchen when your $npc.Grandpa.relationship is there", requirements: { arousal: "🔥" }, requirementsMC: { corruption: 45 }, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true },
                { id: 58, npc: "Brother", key: "BrotherBedroomPregnantSex1", title: "Brother Bedroom Pregnant Sex I", chance: 100, guide: "Go to your $npc.Brother.relationship bedroom while being pregnant and have sex with him", requirements: {}, requirementsMC: {}, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true },
                { id: 59, npc: "Brother", key: "BrotherBedroomSex1", title: "Brother Bedroom Sex I", chance: 100, guide: "Go to your $npc.Brother.relationship bedroom and have sex with him", requirements: {}, requirementsMC: {}, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true },
                { id: 60, npc: "Brother", key: "BrotherWashDishesSex", title: "$npc.Brother.relationship Washing Dishes Sex", chance: 20, guide: "Go to the kitchen and wash the dishes", requirements: { arousal: "🔥🔥", corruption: 10 }, requirementsMC: { corruption: 30 }, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true },
                { id: 61, npc: "Landlord", key: "PayingRent1", title: "$npc.Landlord.name Rent Payment I", chance: 100, guide: "Choose alternative payment when unable to pay rent at your apartment", requirements: {}, requirementsMC: { corruption: 30 }, executedToday: false, unlocked: false, gallery: true, blowjob: true, vaginal: true },
            ];
            npcScenes.forEach(function (scene) {
                _this.createNpcScene(scene);
            });
        }
        catch (error) {
            var errorMessage = "InitScenes failed. Error: ".concat(error);
            throw new Error(errorMessage);
        }
    };
    SceneService.createLocationScene = function (scene) {
        var _a, _b, _c;
        try {
            if (!game().location[scene.location].scenes) {
                game().location[scene.location].scenes = {};
            }
            var existing = null;
            var oldKey = null;
            for (var _i = 0, _d = Object.keys(game().location[scene.location].scenes); _i < _d.length; _i++) {
                var key = _d[_i];
                var currentScene = game().location[scene.location].scenes[key];
                if (currentScene.id == scene.id) {
                    existing = currentScene;
                    oldKey = key;
                    break;
                }
            }
            if (oldKey && oldKey !== scene.key) {
                delete game().location[scene.location].scenes[oldKey];
            }
            game().location[scene.location].scenes[(_a = scene.key) !== null && _a !== void 0 ? _a : ""] = {
                id: scene.id,
                requirementsMC: {
                    corruption: ((_b = scene.requirementsMC) === null || _b === void 0 ? void 0 : _b.corruption) || 0,
                    exhibitionism: ((_c = scene.requirementsMC) === null || _c === void 0 ? void 0 : _c.exhibitionism) || 0
                },
                title: scene.title,
                chance: scene.chance,
                guide: scene.guide,
                unlocked: existing ? existing.unlocked : false,
                executedToday: false,
                gallery: scene.gallery,
                inside: scene.inside || false,
                blowjob: scene.blowjob || false,
                vaginal: scene.vaginal || false,
                anal: scene.anal || false,
                threesome: scene.threesome || false,
                gangbang: scene.gangbang || false
            };
        }
        catch (error) {
            var errorMessage = "createLocationScene failed. Scene: ".concat(scene.key, ". Error: ").concat(error);
            throw new Error(errorMessage);
        }
    };
    SceneService.createNpcScene = function (scene) {
        var _a, _b, _c, _d, _e, _f;
        try {
            if (!game().npc[scene.npc].scenes) {
                game().npc[scene.npc].scenes = {};
            }
            var existing = null;
            var oldKey = null;
            for (var _i = 0, _g = Object.keys(game().npc[scene.npc].scenes); _i < _g.length; _i++) {
                var key = _g[_i];
                var currentScene = game().npc[scene.npc].scenes[key];
                if (currentScene.id == scene.id) {
                    existing = currentScene;
                    oldKey = key;
                    break;
                }
            }
            if (oldKey && oldKey !== scene.key) {
                delete game().npc[scene.npc].scenes[oldKey];
            }
            game().npc[scene.npc].scenes[(_a = scene.key) !== null && _a !== void 0 ? _a : ""] = {
                id: scene.id,
                requirements: {
                    arousal: ((_b = scene.requirements) === null || _b === void 0 ? void 0 : _b.arousal) || "",
                    corruption: ((_c = scene.requirements) === null || _c === void 0 ? void 0 : _c.corruption) || 0,
                    relation: ((_d = scene.requirements) === null || _d === void 0 ? void 0 : _d.relation) || 0
                },
                requirementsMC: {
                    corruption: ((_e = scene.requirementsMC) === null || _e === void 0 ? void 0 : _e.corruption) || 0,
                    exhibitionism: ((_f = scene.requirementsMC) === null || _f === void 0 ? void 0 : _f.exhibitionism) || 0
                },
                title: scene.title,
                chance: scene.chance,
                guide: scene.guide,
                unlocked: existing ? existing.unlocked : false,
                executedToday: false,
                gallery: scene.gallery,
                inside: scene.inside || false,
                blowjob: scene.blowjob || false,
                vaginal: scene.vaginal || false,
                anal: scene.anal || false,
                threesome: scene.threesome || false,
                gangbang: scene.gangbang || false
            };
        }
        catch (error) {
            var errorMessage = "createNpcScene failed. Scene: ".concat(scene.key, ". Error: ").concat(error);
            throw new Error(errorMessage);
        }
    };
    SceneService.createPlayerScene = function (scene) {
        var _a, _b, _c;
        try {
            if (!player().scenes) {
                player().scenes = {};
            }
            var existing = null;
            var oldKey = null;
            for (var _i = 0, _d = Object.keys(player().scenes); _i < _d.length; _i++) {
                var key = _d[_i];
                if (player().scenes[key].id == scene.id) {
                    existing = player().scenes[key];
                    oldKey = key;
                    break;
                }
            }
            if (oldKey && oldKey !== scene.key) {
                delete player().scenes[oldKey];
            }
            player().scenes[(_a = scene.key) !== null && _a !== void 0 ? _a : ""] = {
                id: scene.id,
                requirementsMC: {
                    corruption: ((_b = scene.requirementsMC) === null || _b === void 0 ? void 0 : _b.corruption) || 0,
                    exhibitionism: ((_c = scene.requirementsMC) === null || _c === void 0 ? void 0 : _c.exhibitionism) || 0
                },
                title: scene.title,
                chance: scene.chance,
                guide: scene.guide,
                unlocked: existing ? existing.unlocked : false,
                executedToday: false,
                gallery: scene.gallery,
                inside: scene.inside || false,
                blowjob: scene.blowjob || false,
                vaginal: scene.vaginal || false,
                anal: scene.anal || false,
                threesome: scene.threesome || false,
                gangbang: scene.gangbang || false
            };
        }
        catch (error) {
            var errorMessage = "createPlayerScene failed. Scene: ".concat(scene.key, ". Error: ").concat(error);
            throw new Error(errorMessage);
        }
    };
    SceneService.getNpcKey = function (npc) {
        if (typeof npc === "string") {
            return npc;
        }
        if (npc === null || npc === void 0 ? void 0 : npc.key) {
            return npc.key;
        }
        throw new Error("Invalid NPC reference: ".concat(npc));
    };
    SceneService.unlockNpcScene = function (npc, scene) {
        var _a, _b;
        try {
            var npcKey = this.getNpcKey(npc);
            var npcScene = (_b = (_a = game().npc[npcKey]) === null || _a === void 0 ? void 0 : _a.scenes) === null || _b === void 0 ? void 0 : _b[scene];
            if (!npcScene) {
                throw new Error("Scene: ".concat(scene, " not found for npc ").concat(npcKey));
            }
            npcScene.executedToday = true;
            PlayerService.updatePlayerStatistics(npcScene.blowjob || false, npcScene.vaginal || false, npcScene.anal || false, npcScene.threesome || false, npcScene.gangbang || false);
            NakedLifeService.checkNakedLifeChallenge(scene);
            if (!npcScene.unlocked) {
                npcScene.unlocked = true;
                createNotification("New NPC scene unlocked!", NotificationType.INFO);
            }
        }
        catch (error) {
            var errorMessage = "unlockNpcScene npc: ".concat(npc, " scene: ").concat(scene, " failed. ").concat(error);
            throw new Error(errorMessage);
        }
    };
    SceneService.unlockLocationScene = function (location, scene) {
        try {
            var locationScene = game().location[location].scenes[scene];
            if (!locationScene) {
                var errorMessage = "Scene: ".concat(scene, " not found");
                throw new Error(errorMessage);
            }
            locationScene.executedToday = true;
            PlayerService.updatePlayerStatistics(locationScene.blowjob || false, locationScene.vaginal || false, locationScene.anal || false, locationScene.threesome || false, locationScene.gangbang || false);
            NakedLifeService.checkNakedLifeChallenge(scene);
            if (!locationScene.unlocked) {
                locationScene.unlocked = true;
                createNotification("New location scene unlocked!", NotificationType.INFO);
            }
        }
        catch (error) {
            var errorMessage = "unlockLocationScene location: ".concat(location, " scene: ").concat(scene, " failed. ").concat(error);
            throw new Error(errorMessage);
        }
    };
    SceneService.unlockMCScene = function (scene) {
        try {
            var mcScene = player().scenes[scene];
            if (!mcScene) {
                var errorMessage = "Scene: ".concat(scene, " not found");
                throw new Error(errorMessage);
            }
            mcScene.executedToday = true;
            PlayerService.updatePlayerStatistics(mcScene.blowjob || false, mcScene.vaginal || false, mcScene.anal || false, mcScene.threesome || false, mcScene.gangbang || false);
            NakedLifeService.checkNakedLifeChallenge(scene);
            if (!mcScene.unlocked) {
                mcScene.unlocked = true;
                createNotification("New MC scene unlocked!", NotificationType.INFO);
            }
        }
        catch (error) {
            var errorMessage = "unlockMCScene scene: ".concat(scene, " failed. ").concat(error);
            throw new Error(errorMessage);
        }
    };
    SceneService.CheckSceneReq = function (scene) {
        var _a, _b;
        if (((_a = scene.requirementsMC) === null || _a === void 0 ? void 0 : _a.corruption) > player().corruption.points) {
            var corruptionNeeded = scene.requirementsMC.corruption;
            createNotification("You are not corrupted enough to do this. (" + corruptionNeeded + "+ corruption required!)", NotificationType.WARNING);
            return false;
        }
        if (((_b = scene.requirementsMC) === null || _b === void 0 ? void 0 : _b.exhibitionism) > player().exhibitionism) {
            var exhibitionismNeeded = scene.requirementsMC.exhibitionism;
            createNotification("You are not exhibitionist enough to do this. (" + exhibitionismNeeded + "+ exhibitionism required!)", NotificationType.WARNING);
            return false;
        }
        if (scene.executedToday) {
            createNotification("You already did this today!", NotificationType.WARNING);
            return false;
        }
        scene.executedToday = true;
        return true;
    };
    SceneService.isSceneExecutedToday = function (scene) {
        try {
            return scene.executedToday;
        }
        catch (error) {
            error = "isSceneExecutedToday scene: ".concat(scene.title, " failed. ").concat(error);
            throw error;
        }
    };
    SceneService.isNpcSceneUnlocked = function (npc, scene) {
        var _a, _b;
        try {
            var npcKey = this.getNpcKey(npc);
            var npcScene = (_b = (_a = game().npc[npcKey]) === null || _a === void 0 ? void 0 : _a.scenes) === null || _b === void 0 ? void 0 : _b[scene];
            if (!npcScene) {
                throw new Error("Scene: ".concat(scene, " not found for npc ").concat(npcKey));
            }
            return npcScene.unlocked;
        }
        catch (error) {
            error = "isNpcSceneUnlocked npc: ".concat(npc, " scene: ").concat(scene, " failed. ").concat(error);
            throw error;
        }
    };
    return SceneService;
}());
/* twine-user-script #98: "xCamService.js" */
"use strict";
var XCamService = /** @class */ (function () {
    function XCamService() {
    }
    XCamService.createXCam = function (oldPlayer) {
        var oldXcam = (oldPlayer === null || oldPlayer === void 0 ? void 0 : oldPlayer.xcam) || {};
        var xcam = {
            account: (oldXcam === null || oldXcam === void 0 ? void 0 : oldXcam.account) || false,
            name: (oldXcam === null || oldXcam === void 0 ? void 0 : oldXcam.name) || oldPlayer.name,
            exp: (oldXcam === null || oldXcam === void 0 ? void 0 : oldXcam.exp) || 0,
            streamed: (oldXcam === null || oldXcam === void 0 ? void 0 : oldXcam.streamed) || false
        };
        return xcam;
    };
    return XCamService;
}());
/* twine-user-script #99: "PhoneService.js" */
"use strict";
var __assign = (this && this.__assign) || function () {
    __assign = Object.assign || function(t) {
        for (var s, i = 1, n = arguments.length; i < n; i++) {
            s = arguments[i];
            for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p))
                t[p] = s[p];
        }
        return t;
    };
    return __assign.apply(this, arguments);
};
var __spreadArray = (this && this.__spreadArray) || function (to, from, pack) {
    if (pack || arguments.length === 2) for (var i = 0, l = from.length, ar; i < l; i++) {
        if (ar || !(i in from)) {
            if (!ar) ar = Array.prototype.slice.call(from, 0, i);
            ar[i] = from[i];
        }
    }
    return to.concat(ar || Array.prototype.slice.call(from));
};
var PhoneService = /** @class */ (function () {
    function PhoneService() {
    }
    PhoneService.getThreadConfig = function (messageId) {
        return this.MESSAGE_THREADS[messageId] || { id: messageId, name: messageId };
    };
    PhoneService.createMessageEntryId = function (messageId) {
        return "".concat(messageId).concat(this.MESSAGE_INSTANCE_SEPARATOR).concat(Date.now()).concat(this.MESSAGE_INSTANCE_SEPARATOR).concat(Math.floor(Math.random() * 100000));
    };
    PhoneService.getMessageTemplateId = function (messageEntryId) {
        if (!messageEntryId) {
            return "";
        }
        return messageEntryId.split(this.MESSAGE_INSTANCE_SEPARATOR)[0] || messageEntryId;
    };
    PhoneService.getMessageTimestamp = function (messageEntryId) {
        if (!messageEntryId) {
            return 0;
        }
        var messageTimestamp = Number(messageEntryId.split(this.MESSAGE_INSTANCE_SEPARATOR)[1]);
        return Number.isFinite(messageTimestamp) ? messageTimestamp : 0;
    };
    PhoneService.createThread = function (threadConfig, messageId) {
        return {
            id: threadConfig.id,
            name: threadConfig.name,
            messages: messageId ? [messageId] : [],
            sentActions: [],
            actionUsageDays: {},
            hasUnread: !!messageId
        };
    };
    PhoneService.migrateThreads = function (oldPhone) {
        var savedThreads = Array.isArray(oldPhone === null || oldPhone === void 0 ? void 0 : oldPhone.threads) ? oldPhone.threads : [];
        var threads = savedThreads
            .map(function (thread) {
            var messages = Array.isArray(thread === null || thread === void 0 ? void 0 : thread.messages) ? thread.messages.filter(Boolean) : [];
            var sentActions = Array.isArray(thread === null || thread === void 0 ? void 0 : thread.sentActions)
                ? thread.sentActions.filter(Boolean).map(function (action) { return ({
                    id: action.id,
                    speakerId: action.speakerId || "Player",
                    text: action.text,
                    dayUsed: action.dayUsed,
                    imagePath: action.imagePath,
                    timestamp: typeof action.timestamp === "number" ? action.timestamp : undefined
                }); })
                : [];
            if (!(thread === null || thread === void 0 ? void 0 : thread.id)) {
                return null;
            }
            return {
                id: thread.id,
                name: thread.name || thread.id,
                messages: messages,
                sentActions: sentActions,
                actionUsageDays: thread.actionUsageDays || {},
                hasUnread: !!thread.hasUnread
            };
        })
            .filter(function (thread) { return thread !== null; });
        if (!threads.length && (oldPhone === null || oldPhone === void 0 ? void 0 : oldPhone.message)) {
            var threadConfig = this.getThreadConfig(oldPhone.message);
            threads.push(this.createThread(threadConfig, oldPhone.message));
        }
        return threads;
    };
    PhoneService.createPhone = function (oldPlayer) {
        try {
            var oldPhone = (oldPlayer === null || oldPlayer === void 0 ? void 0 : oldPlayer.phone) || {};
            var phone = {
                selfies: (oldPhone === null || oldPhone === void 0 ? void 0 : oldPhone.selfies) || 0,
                lewdSelfies: (oldPhone === null || oldPhone === void 0 ? void 0 : oldPhone.lewdSelfies) || 0,
                nudeSelfies: (oldPhone === null || oldPhone === void 0 ? void 0 : oldPhone.nudeSelfies) || 0,
                message: "",
                threads: this.migrateThreads(oldPhone),
                selectedThread: (oldPhone === null || oldPhone === void 0 ? void 0 : oldPhone.selectedThread) || "",
                messageStates: (oldPhone === null || oldPhone === void 0 ? void 0 : oldPhone.messageStates) || {},
                instafame: InstafameService.createInstafame(oldPhone === null || oldPhone === void 0 ? void 0 : oldPhone.instafame),
                fastJobs: FastJobsService.createFastJobs(oldPhone === null || oldPhone === void 0 ? void 0 : oldPhone.fastJobs),
                nakedLife: NakedLifeService.createNakedLife(oldPhone === null || oldPhone === void 0 ? void 0 : oldPhone.nakedLife),
                pornCenter: PornCenterService.createPornCenter(oldPhone === null || oldPhone === void 0 ? void 0 : oldPhone.pornCenter)
            };
            return phone;
        }
        catch (error) {
            throw new Error("CreatePhone failed: " + error);
        }
    };
    PhoneService.ensureNotificationElement = function () {
        var notificationElement = document.getElementById('notification');
        if (!notificationElement) {
            notificationElement = document.createElement('div');
            notificationElement.id = 'notification';
            notificationElement.className = 'notification';
            var phoneElement = document.getElementById('phone');
            if (phoneElement) {
                phoneElement.appendChild(notificationElement);
            }
            else {
                document.body.appendChild(notificationElement);
            }
        }
    };
    PhoneService.showNotification = function (message) {
        this.ensureNotificationElement();
        var notification = document.getElementById('notification');
        notification.textContent = message;
        notification.classList.add('show');
        setTimeout(function () {
            notification.classList.remove('show');
        }, 2500);
    };
    PhoneService.findThread = function (threadId) {
        var _a;
        var threads = ((_a = player().phone) === null || _a === void 0 ? void 0 : _a.threads) || [];
        return threads.find(function (thread) { return thread.id === threadId; });
    };
    PhoneService.getUnreadThreadCount = function () {
        var _a;
        var threads = ((_a = player().phone) === null || _a === void 0 ? void 0 : _a.threads) || [];
        return threads.filter(function (thread) { return !!thread.hasUnread; }).length;
    };
    PhoneService.selectThread = function (threadId) {
        var thread = this.findThread(threadId);
        if (thread) {
            thread.hasUnread = false;
            player().phone.selectedThread = threadId;
        }
    };
    PhoneService.clearSelectedThread = function () {
        player().phone.selectedThread = "";
    };
    PhoneService.getThreadActions = function (threadId) {
        var _this = this;
        var thread = this.findThread(threadId);
        if (!thread) {
            return [];
        }
        var currentDay = game().game.days;
        var corruptionLevel = window.getCorruptionLevel();
        return Object.values(this.THREAD_ACTIONS).map(function (action) {
            var _a;
            var photoAction = _this.PHOTO_ACTIONS[action.id];
            var isLocked = !!((photoAction === null || photoAction === void 0 ? void 0 : photoAction.minCorruption) && corruptionLevel < photoAction.minCorruption);
            return __assign(__assign({}, action), { disabled: ((_a = thread.actionUsageDays) === null || _a === void 0 ? void 0 : _a[action.id]) === currentDay, locked: isLocked, lockedNote: isLocked ? ((photoAction === null || photoAction === void 0 ? void 0 : photoAction.lockedMessage) || "You aren't corrupted enough.") : undefined });
        });
    };
    PhoneService.getThreadButtonLabel = function (threadId) {
        var thread = this.findThread(threadId);
        if (!thread) {
            return "";
        }
        var messageCount = Array.isArray(thread.messages) ? thread.messages.length : 0;
        var threadMeta = thread.hasUnread
            ? "".concat(messageCount, " unread message").concat(messageCount !== 1 ? "s" : "")
            : "Read";
        return "".concat(thread.name, " - ").concat(threadMeta);
    };
    PhoneService.getThreadActionLabel = function (actionId) {
        var _a;
        return ((_a = this.THREAD_ACTIONS[actionId]) === null || _a === void 0 ? void 0 : _a.label) || "";
    };
    PhoneService.getThreadTimeline = function (threadId) {
        var _this = this;
        var thread = this.findThread(threadId);
        if (!thread) {
            return [];
        }
        var messageEntries = Array.isArray(thread.messages) ? thread.messages.filter(Boolean) : [];
        var sentActions = Array.isArray(thread.sentActions) ? thread.sentActions.filter(Boolean) : [];
        var knownTimestamps = __spreadArray(__spreadArray([], messageEntries.map(function (messageId) { return _this.getMessageTimestamp(messageId); }).filter(function (timestamp) { return timestamp > 0; }), true), sentActions
            .map(function (action) { return action.timestamp; })
            .filter(function (timestamp) { return typeof timestamp === "number" && timestamp > 0; }), true);
        var legacyActionBaseTimestamp = knownTimestamps.length ? Math.max.apply(Math, knownTimestamps) : 0;
        var timeline = [];
        messageEntries.forEach(function (messageId, index) {
            timeline.push({
                id: "message:".concat(messageId, ":").concat(index),
                kind: "message",
                timestamp: _this.getMessageTimestamp(messageId) || index + 1,
                messageId: messageId
            });
        });
        sentActions.forEach(function (action, index) {
            timeline.push({
                id: "action:".concat(action.id, ":").concat(index),
                kind: "action",
                timestamp: action.timestamp || legacyActionBaseTimestamp + index + 1,
                action: action
            });
        });
        return timeline.sort(function (leftEntry, rightEntry) { return leftEntry.timestamp - rightEntry.timestamp; });
    };
    PhoneService.getThreadReply = function (threadId, actionId) {
        var _a, _b;
        return ((_a = this.THREAD_ACTION_REPLIES[threadId]) === null || _a === void 0 ? void 0 : _a[actionId])
            || ((_b = this.THREAD_ACTION_REPLIES._default) === null || _b === void 0 ? void 0 : _b[actionId])
            || "Message received.";
    };
    PhoneService.sendThreadAction = function (threadId, actionId) {
        var thread = this.findThread(threadId);
        var action = this.THREAD_ACTIONS[actionId];
        var currentDay = game().game.days;
        if (!thread) {
            throw new Error("Phone thread \"".concat(threadId, "\" not found."));
        }
        if (!action) {
            throw new Error("Phone action \"".concat(actionId, "\" is invalid."));
        }
        if (!Array.isArray(thread.sentActions)) {
            thread.sentActions = [];
        }
        if (!thread.actionUsageDays) {
            thread.actionUsageDays = {};
        }
        if (thread.actionUsageDays[action.id] === currentDay) {
            this.showNotification("You already used this action today.");
            return;
        }
        var photoAction = this.PHOTO_ACTIONS[action.id];
        if ((photoAction === null || photoAction === void 0 ? void 0 : photoAction.minCorruption) && window.getCorruptionLevel() < photoAction.minCorruption) {
            this.showNotification(photoAction.lockedMessage || "You aren't corrupted enough.");
            return;
        }
        var sentTimestamp = Date.now();
        var replyTimestamp = sentTimestamp + 1;
        if (photoAction) {
            var randomImage = photoAction.files[Math.floor(Math.random() * photoAction.files.length)];
            var imagePath = "".concat(setup.ImagePath, "/tech/phone/instafame/selfies/").concat(randomImage);
            thread.sentActions.push({
                id: action.id,
                speakerId: "Player",
                text: action.text,
                imagePath: imagePath,
                timestamp: sentTimestamp
            });
            player().phone[photoAction.counterKey] += 1;
            this.showNotification("".concat(photoAction.notification, " to ").concat(thread.name, "."));
        }
        else {
            var sentTimestamp_1 = Date.now();
            thread.sentActions.push({
                id: action.id,
                speakerId: "Player",
                text: action.text,
                timestamp: sentTimestamp_1
            });
            this.showNotification("Message sent to ".concat(thread.name, "."));
        }
        thread.actionUsageDays[action.id] = currentDay;
        thread.sentActions.push({
            id: "".concat(action.id, "Reply"),
            speakerId: thread.id,
            text: this.getThreadReply(thread.id, action.id),
            dayUsed: currentDay,
            timestamp: replyTimestamp
        });
    };
    PhoneService.newMessage = function (message) {
        var threadConfig = this.getThreadConfig(message);
        var messageEntryId = this.createMessageEntryId(message);
        if (!player().phone.threads) {
            player().phone.threads = [];
        }
        var thread = this.findThread(threadConfig.id);
        if (!thread) {
            thread = this.createThread(threadConfig);
            player().phone.threads.push(thread);
        }
        thread.name = threadConfig.name;
        if (!Array.isArray(thread.messages)) {
            thread.messages = [];
        }
        thread.messages.push(messageEntryId);
        thread.hasUnread = true;
        player().phone.message = "";
        createNotification("You have a new message, check your phone!", NotificationType.INFO);
    };
    PhoneService.MESSAGE_INSTANCE_SEPARATOR = "::";
    PhoneService.MESSAGE_THREADS = {
        JamalPoolParty: { id: "Jamal", name: "Jamal" },
        VeronicaCostumeParty: { id: "Veronica", name: "Veronica" },
        MarcusDate: { id: "Marcus", name: "Marcus" }
    };
    PhoneService.THREAD_ACTIONS = {
        sendSelfie: {
            id: "sendSelfie",
            label: "Send a selfie",
            text: "Thought I'd send you a cute selfie."
        },
        sendLewd: {
            id: "sendLewd",
            label: "Send a lewd photo",
            text: "Thought you might like this one."
        },
        sendNude: {
            id: "sendNude",
            label: "Send a nude",
            text: "Here's something a little more daring."
        }
    };
    PhoneService.THREAD_ACTION_REPLIES = {
        _default: {
            sendSelfie: "You look really good in that selfie.",
            sendLewd: "Damn... that's a really tempting picture.",
            sendNude: "Wow... I wasn't expecting that, but I like it."
        },
        Jamal: {
            sendSelfie: "Damn, you look cute as hell in that pic.",
            sendLewd: "Shit... now that's a tease. You're driving me crazy.",
            sendNude: "Shit... that's hot. You know exactly how to tease me."
        },
        Veronica: {
            sendSelfie: "You're so pretty. I love this picture.",
            sendLewd: "Damn, babe. That's bold, and I love it.",
            sendNude: "Damn, you look incredible. You're really tempting me now."
        },
        Marcus: {
            sendSelfie: "You look amazing. Thanks for sending me that.",
            sendLewd: "Wow... that's really sexy. I wasn't ready for that.",
            sendNude: "Wow... you look amazing. I wasn't ready for that."
        }
    };
    PhoneService.PHOTO_ACTIONS = {
        sendSelfie: {
            files: ["selfie1.webp", "selfie2.webp", "selfie3.webp", "selfie4.webp", "selfie5.webp"],
            notification: "Selfie sent",
            counterKey: "selfies"
        },
        sendLewd: {
            files: ["lewd1.webp", "lewd2.webp", "lewd3.webp", "lewd4.webp", "lewd5.webp"],
            notification: "Lewd photo sent",
            counterKey: "lewdSelfies",
            minCorruption: 3,
            lockedMessage: "You aren't corrupted enough to send a lewd photo."
        },
        sendNude: {
            files: ["naked1.webp", "naked2.webp", "naked3.webp", "naked4.webp", "naked5.webp"],
            notification: "Nude sent",
            counterKey: "nudeSelfies",
            minCorruption: 4,
            lockedMessage: "You aren't corrupted enough to send a nude."
        }
    };
    return PhoneService;
}());
/* twine-user-script #100: "FastJobsService.js" */
"use strict";
var FastJobsService = /** @class */ (function () {
    function FastJobsService() {
    }
    FastJobsService.createFastJobs = function (fastJobs) {
        try {
            fastJobs = {
                xp: (fastJobs === null || fastJobs === void 0 ? void 0 : fastJobs.xp) || 0,
                jobs: this.createJobs((fastJobs === null || fastJobs === void 0 ? void 0 : fastJobs.jobs) || {})
            };
            return fastJobs;
        }
        catch (error) {
            throw new Error("CreateFastJobs failed: " + error);
        }
    };
    FastJobsService.createJobs = function (oldJobs) {
        var jobs = [
            { id: 1, name: "DogWalking", description: "Walk dogs in the neighborhood.", income: 45, type: FastJobType.PetCare, finished: false, repeatable: true, active: false, time: DayPeriod.Afternoon, xp: 0 },
            { id: 2, name: "HouseCleaning", description: "Clean houses for extra cash.", income: 75, type: FastJobType.Cleaning, finished: false, repeatable: true, active: false, time: DayPeriod.Morning, xp: 5 },
            { id: 3, name: "BabySitting", description: "Take care of children while their parents are away.", income: 110, type: FastJobType.BabySitting, finished: false, repeatable: true, active: false, time: DayPeriod.Afternoon, xp: 10 },
            { id: 4, name: "ElderlyCare", description: "Take care of the elderly.", income: 110, type: FastJobType.ElderlyCare, finished: false, repeatable: true, active: false, time: DayPeriod.Morning, xp: 10 },
        ];
        var jobsMap = {};
        try {
            var _loop_1 = function (job) {
                var oldJob = Object.values(oldJobs).find(function (j) { return j.id === job.id; });
                jobsMap[job.name] = {
                    id: job.id,
                    name: job.name,
                    description: job.description,
                    active: (oldJob === null || oldJob === void 0 ? void 0 : oldJob.active) || job.active,
                    income: job.income,
                    type: job.type,
                    finished: (oldJob === null || oldJob === void 0 ? void 0 : oldJob.finished) || job.finished,
                    repeatable: job.repeatable,
                    delayDays: (oldJob === null || oldJob === void 0 ? void 0 : oldJob.delayDays) || job.delayDays,
                    time: job.time,
                    xp: job.xp
                };
            };
            for (var _i = 0, jobs_1 = jobs; _i < jobs_1.length; _i++) {
                var job = jobs_1[_i];
                _loop_1(job);
            }
            return jobsMap;
        }
        catch (error) {
            throw new Error("CreateJobs failed: " + error);
        }
    };
    FastJobsService.getJobById = function (jobId) {
        try {
            var job = Object.values(fastJobs().jobs).find(function (job) { return job.id === jobId; });
            if (!job) {
                throw new Error("Job with ID ".concat(jobId, " not found."));
            }
            return job;
        }
        catch (error) {
            throw new Error("GetJobById failed: " + error);
        }
    };
    FastJobsService.startFastJob = function (jobId) {
        try {
            var job = this.getJobById(jobId);
            if (job.time == game().game.time) {
                job.active = true;
                LocationService.enterLocation(job.name);
            }
            else {
                var timeName = TimeService.getDayPeriodByEnum(job.time);
                PhoneService.showNotification("You can only start this job during " + timeName + ".");
            }
        }
        catch (error) {
            throw new Error("startFastJob failed: " + error);
        }
    };
    FastJobsService.getJobByName = function (jobName) {
        try {
            var job = Object.values(fastJobs().jobs).find(function (job) { return job.name === jobName; });
            if (!job) {
                throw new Error("Job with name ".concat(jobName, " not found."));
            }
            return job;
        }
        catch (error) {
            throw new Error("GetJobByName failed: " + error);
        }
    };
    FastJobsService.finishFastJob = function (jobName) {
        var defaultDelayDays = 2;
        try {
            var job = this.getJobByName(jobName);
            job.finished = true;
            job.active = false;
            job.delayDays = defaultDelayDays;
            fastJobs().xp += 1;
            StatsService.addMoney(job.income);
        }
        catch (error) {
            throw new Error("FinishFastJob failed: " + error);
        }
    };
    return FastJobsService;
}());
/* twine-user-script #101: "InstafameService.js" */
"use strict";
var InstafameService = /** @class */ (function () {
    function InstafameService() {
    }
    InstafameService.createInstafame = function (instafame) {
        try {
            instafame = {
                account: (instafame === null || instafame === void 0 ? void 0 : instafame.account) || false,
                name: (instafame === null || instafame === void 0 ? void 0 : instafame.name) || "",
                followers: (instafame === null || instafame === void 0 ? void 0 : instafame.followers) || 0,
                likes: (instafame === null || instafame === void 0 ? void 0 : instafame.likes) || 0,
                selfieType: (instafame === null || instafame === void 0 ? void 0 : instafame.selfieType) || SelfieType.Normal,
                dm: (instafame === null || instafame === void 0 ? void 0 : instafame.dm) || 0,
                posted: (instafame === null || instafame === void 0 ? void 0 : instafame.posted) || false
            };
            return instafame;
        }
        catch (error) {
            throw new Error("CreateInstafame failed: " + error);
        }
    };
    return InstafameService;
}());
/* twine-user-script #102: "NakedLifeService.js" */
"use strict";
var XP_NEWBIE = 0;
var XP_EXHIBITIONIST = 20;
var XP_SHAMELESS = 40;
var XP_LEGEND = 60;
var GAIN_NEWBIE = 1;
var GAIN_EXHIBITIONIST = 2;
var GAIN_SHAMELESS = 3;
var GAIN_LEGEND = 4;
var NakedLifeService = /** @class */ (function () {
    function NakedLifeService() {
    }
    NakedLifeService.createNakedLife = function (nakedLife) {
        var _a;
        try {
            return {
                account: (nakedLife === null || nakedLife === void 0 ? void 0 : nakedLife.account) || false,
                challenges: this.createNakedLifeChallenges(nakedLife === null || nakedLife === void 0 ? void 0 : nakedLife.challenges),
                rank: (nakedLife === null || nakedLife === void 0 ? void 0 : nakedLife.rank) || NakedLifeRank.Newbie,
                exp: (_a = nakedLife === null || nakedLife === void 0 ? void 0 : nakedLife.exp) !== null && _a !== void 0 ? _a : 0,
            };
        }
        catch (error) {
            throw new Error("CreateNakedLife failed: " + error.message);
        }
    };
    NakedLifeService.createNakedLifeChallenges = function (oldChallenges) {
        try {
            var challenges = [
                {
                    id: 1,
                    title: "Park Flash",
                    description: "Do a flash in the park.",
                    rank: NakedLifeRank.Newbie,
                    relatedScene: "JoggingFlash",
                    completed: false,
                    active: false,
                },
                {
                    id: 2,
                    title: "Beach Flash",
                    description: "Do a flash at the beach.",
                    rank: NakedLifeRank.Newbie,
                    relatedScene: "SwimFlash",
                    completed: false,
                    active: false,
                },
                {
                    id: 3,
                    title: "Pool Flash",
                    description: "Do a flash at a public pool.",
                    rank: NakedLifeRank.Newbie,
                    relatedScene: "PoolFlash",
                    completed: false,
                    active: false,
                },
                {
                    id: 4,
                    title: "Mall Flash",
                    description: "Do a flash at the mall.",
                    rank: NakedLifeRank.Newbie,
                    relatedScene: "MallFlash",
                    completed: false,
                    active: false,
                },
                {
                    id: 5,
                    title: "Gym Flash",
                    description: "Do a flash at the gym.",
                    rank: NakedLifeRank.Exhibitionist,
                    relatedScene: "GymFlash",
                    completed: false,
                    active: false,
                },
                {
                    id: 6,
                    title: "Restaurant Flash",
                    description: "Do a flash at a restaurant.",
                    rank: NakedLifeRank.Exhibitionist,
                    relatedScene: "RestaurantFlash",
                    completed: false,
                    active: false,
                },
                {
                    id: 7,
                    title: "Classroom Flash",
                    description: "Do a flash at the classroom.",
                    rank: NakedLifeRank.Exhibitionist,
                    relatedScene: "ClassroomFlash",
                    completed: false,
                    active: false,
                },
                {
                    id: 8,
                    title: "Public Transport Flash",
                    description: "Do a flash on public transport.",
                    rank: NakedLifeRank.Exhibitionist,
                    relatedScene: "BusFlash",
                    completed: false,
                    active: false,
                },
                {
                    id: 9,
                    title: "Naked Pizza Delivery",
                    description: "Order a pizza and answer the door naked.",
                    rank: NakedLifeRank.Shameless,
                    relatedScene: "PizzaDelivery",
                    completed: false,
                    active: false,
                },
                {
                    id: 10,
                    title: "Car Wash Challenge",
                    description: "Go to the car wash and meet our moderator",
                    rank: NakedLifeRank.Shameless,
                    relatedScene: "CarWashChallenge",
                    completed: false,
                    active: false,
                },
                {
                    id: 11,
                    title: "Park Challenge",
                    description: "Go to the park and meet our moderator",
                    rank: NakedLifeRank.Shameless,
                    relatedScene: "ParkChallenge",
                    completed: false,
                    active: false,
                },
                {
                    id: 12,
                    title: "Street Challenge I",
                    description: "Go to the center of town and meet our moderator",
                    rank: NakedLifeRank.Legend,
                    relatedScene: "StreetChallenge1",
                    completed: false,
                    active: false,
                },
                {
                    id: 13,
                    title: "Beach Challenge I",
                    description: "Go to the beach and meet our moderator",
                    rank: NakedLifeRank.Shameless,
                    relatedScene: "BeachChallenge1",
                    completed: false,
                    active: false,
                }
            ];
            if (!oldChallenges)
                return challenges;
            var _loop_1 = function (old) {
                var ex = challenges.find(function (c) { return c.id === old.id; });
                if (ex) {
                    ex.completed = !!old.completed;
                    ex.active = !!old.active;
                }
            };
            for (var _i = 0, oldChallenges_1 = oldChallenges; _i < oldChallenges_1.length; _i++) {
                var old = oldChallenges_1[_i];
                _loop_1(old);
            }
            return challenges;
        }
        catch (error) {
            throw new Error("CreateNakedLifeChallenges failed: " + error.message);
        }
    };
    NakedLifeService.startNakedLifeChallenge = function (nakedLifeId) {
        try {
            var challenge = this.getNakedLifeChallengeById(nakedLifeId);
            if (!challenge)
                throw new Error("Challenge not found");
            if (player().phone.nakedLife.exp < this.getXpThreshold(challenge.rank)) {
                PhoneService.showNotification("You need to be at least ".concat(challenge.rank, " rank to start this challenge."));
                return;
            }
            this.unlockChallengeLocation(challenge);
            challenge.active = true;
            challenge.completed = false;
            PhoneService.showNotification("Challenge \"".concat(challenge.title, "\" started!"));
        }
        catch (error) {
            throw new Error("startNakedLifeChallenge failed: " + error.message);
        }
    };
    NakedLifeService.unlockChallengeLocation = function (challenge) {
        var location = Object.values(game().location).find(function (loc) { return loc.passage === challenge.relatedScene; });
        if (location) {
            location.unlocked = true;
        }
    };
    NakedLifeService.getNakedLifeChallengeById = function (nakedLifeId) {
        try {
            return player().phone.nakedLife.challenges.find(function (c) { return c.id === nakedLifeId; });
        }
        catch (error) {
            throw new Error("GetNakedLifeChallengeById failed: " + error.message);
        }
    };
    NakedLifeService.getNakedLifeChallengeByScene = function (scene) {
        try {
            return player().phone.nakedLife.challenges.find(function (c) { return c.relatedScene === scene; });
        }
        catch (error) {
            throw new Error("GetNakedLifeChallengeByScene failed: " + error.message);
        }
    };
    NakedLifeService.completeNakedLifeChallenge = function (nakedLifeId) {
        try {
            var challenge = this.getNakedLifeChallengeById(nakedLifeId);
            if (!challenge)
                throw new Error("Challenge not found");
            if (challenge.completed)
                return;
            challenge.completed = true;
            challenge.active = false;
            var xpGain = 0;
            switch (challenge.rank) {
                case NakedLifeRank.Newbie:
                    xpGain = GAIN_NEWBIE;
                    break;
                case NakedLifeRank.Exhibitionist:
                    xpGain = GAIN_EXHIBITIONIST;
                    break;
                case NakedLifeRank.Shameless:
                    xpGain = GAIN_SHAMELESS;
                    break;
                case NakedLifeRank.Legend:
                    xpGain = GAIN_LEGEND;
                    break;
            }
            this.addExp(xpGain);
            createNotification("Challenge \"".concat(challenge.title, "\" completed! +").concat(xpGain, " XP"), NotificationType.SUCCESS);
        }
        catch (error) {
            throw new Error("completeNakedLifeChallenge failed: " + error.message);
        }
    };
    NakedLifeService.checkNakedLifeChallenge = function (scene) {
        try {
            var challenge = player().phone.nakedLife.challenges.find(function (c) { return c.active && c.relatedScene === scene; });
            if (challenge) {
                this.completeNakedLifeChallenge(challenge.id);
            }
        }
        catch (error) {
            throw new Error("checkNakedLifeChallenge failed: " + error.message);
        }
    };
    NakedLifeService.addExp = function (amount) {
        var nakedLife = player().phone.nakedLife;
        nakedLife.exp += amount | 0;
        if (nakedLife.exp < 0)
            nakedLife.exp = 0;
        this.rankUpByXp();
    };
    NakedLifeService.rankUpByXp = function () {
        var nakedLife = player().phone.nakedLife;
        var xp = nakedLife.exp || 0;
        var newRank = nakedLife.rank;
        if (xp >= XP_LEGEND)
            newRank = NakedLifeRank.Legend;
        else if (xp >= XP_SHAMELESS)
            newRank = NakedLifeRank.Shameless;
        else if (xp >= XP_EXHIBITIONIST)
            newRank = NakedLifeRank.Exhibitionist;
        else
            newRank = NakedLifeRank.Newbie;
        if (newRank !== nakedLife.rank) {
            nakedLife.rank = newRank;
            createNotification("Naked Life Rank Up! You are now \"".concat(nakedLife.rank, "\"."), NotificationType.SUCCESS);
        }
    };
    NakedLifeService.getNextRank = function (current) {
        switch (current) {
            case NakedLifeRank.Newbie:
                return NakedLifeRank.Exhibitionist;
            case NakedLifeRank.Exhibitionist:
                return NakedLifeRank.Shameless;
            case NakedLifeRank.Shameless:
                return NakedLifeRank.Legend;
            default:
                return null;
        }
    };
    NakedLifeService.getXpThreshold = function (rank) {
        switch (rank) {
            case NakedLifeRank.Newbie:
                return XP_NEWBIE;
            case NakedLifeRank.Exhibitionist:
                return XP_EXHIBITIONIST;
            case NakedLifeRank.Shameless:
                return XP_SHAMELESS;
            case NakedLifeRank.Legend:
                return XP_LEGEND;
            default:
                throw new Error("Invalid Naked Life rank: " + rank);
        }
    };
    NakedLifeService.getProgressToNextRank = function () {
        var nakedLife = player().phone.nakedLife;
        var current = nakedLife.rank;
        var currentXp = nakedLife.exp || 0;
        var next = this.getNextRank(current);
        if (!next) {
            if (!next)
                return { current: current, currentXp: currentXp, next: null, need: 0, left: 0 };
        }
        var from = this.getXpThreshold(current);
        var to = this.getXpThreshold(next);
        var need = Math.max(0, to - from);
        var gained = Math.max(0, currentXp - from);
        var left = Math.max(0, need - gained);
        return { current: current, currentXp: currentXp, next: next, need: need, left: left };
    };
    return NakedLifeService;
}());
/* twine-user-script #103: "PornCenterService.js" */
"use strict";
var PornCenterService = /** @class */ (function () {
    function PornCenterService() {
    }
    PornCenterService.createPornCenter = function (pornCenter) {
        try {
            return {
                account: pornCenter === null || pornCenter === void 0 ? void 0 : pornCenter.account,
                sites: this.createPornCenterSites(pornCenter === null || pornCenter === void 0 ? void 0 : pornCenter.sites)
            };
        }
        catch (error) {
            throw new Error("CreateNakedLife failed: " + error.message);
        }
    };
    PornCenterService.createPornCenterSites = function (oldPornSites) {
        try {
            var sites = [
                {
                    id: 1,
                    name: "ZVideos",
                    genre: "All",
                    corruption: 5,
                    description: "A popular site for amateur adult content.",
                    timesWatched: 0
                },
                {
                    id: 2,
                    name: "PornVub",
                    genre: "All",
                    corruption: 5,
                    description: "A site with a wide variety of professional and amateur videos.",
                    timesWatched: 0
                },
                {
                    id: 3,
                    name: "Blackez",
                    genre: "Interracial",
                    corruption: 10,
                    description: "A premium site known for high-quality interracial content.",
                    timesWatched: 0
                },
                {
                    id: 4,
                    name: "FamilyLove",
                    genre: "Taboo",
                    corruption: 15,
                    description: "A controversial site focusing on taboo family scenarios.",
                    timesWatched: 0
                },
                {
                    id: 5,
                    name: "F0rc3dWorld",
                    genre: "Non-consent",
                    corruption: 20,
                    description: "A highly controversial site featuring non-consensual scenarios. Viewer discretion is advised.",
                    timesWatched: 0
                }
            ];
            if (!oldPornSites)
                return sites;
            var _loop_1 = function (oldSite) {
                var site = sites.find(function (s) { return s.id === oldSite.id; });
                if (site) {
                    site.timesWatched = oldSite.timesWatched || 0;
                }
            };
            for (var _i = 0, oldPornSites_1 = oldPornSites; _i < oldPornSites_1.length; _i++) {
                var oldSite = oldPornSites_1[_i];
                _loop_1(oldSite);
            }
            return sites;
        }
        catch (error) {
            throw new Error("CreatePornCenterSites failed: " + error.message);
        }
    };
    return PornCenterService;
}());
/* twine-user-script #104: "TimeService.js" */
"use strict";
var TimeService = /** @class */ (function () {
    function TimeService() {
    }
    TimeService.initTime = function () {
        try {
            Wikifier.wikifyEval('<<newcycle \'time\' 2>><<phase \'EM\' \'M\' \'A\' \'E\' \'N\' \'LN\'>><</newcycle>>');
            Wikifier.wikifyEval('<<newcycle \'day\' 1>><<phase \'Monday\' \'Tuesday\' \'Wednesday\' \'Thursday\' \'Friday\' \'Saturday\' \'Sunday\'>><</newcycle>>');
            Cycle.get('day').suspend();
            Cycle.get('time').suspend();
        }
        catch (error) {
            error = "initTime failed: " + error;
            throw error;
        }
    };
    TimeService.newDay = function () {
        try {
            this.resetGameCycle();
            WeatherService.rollDailyWeather();
            this.saveGame();
            StatsService.improveMcMaximumStats();
            StatsService.resetPlayerStats();
            this.updateNPCs();
            this.updateLocations();
            this.resetLocationVariables();
            this.checkSchoolTest();
            this.updatePregnancy();
            this.checkQuests();
            this.relationshipMessages();
            BabyService.addBabyAge();
            BabyService.chargeWeeklyExpenses();
            BankService.generateBankIncome();
            PropertyService.decrementRentDays();
            this.reduceDaysFromVariables();
            this.changeLaundryCut();
        }
        catch (error) {
            var errorMessage = "Error in newDay: " + error;
            throw new Error(errorMessage);
        }
    };
    TimeService.updateGameTime = function () {
        var times = ['LN', 'N', 'E', 'A', 'M', 'EM'];
        var icons = ['🌑', '🌒', '⛅', '🌤️', '☀️', '🌤️'];
        for (var i = 0; i < times.length; i++) {
            if (Cycle.check('time', times[i])) {
                game().game.time = times[i];
                game().game.timeIcon = icons[i];
                break;
            }
        }
        var days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
        for (var i = 0; i < days.length; i++) {
            if (Cycle.check('day', days[i])) {
                game().game.day = days[i];
            }
        }
        this.updateLocations();
        NpcService.npcRoutine();
        updateBar();
    };
    TimeService.updateLocations = function () {
        var _this = this;
        var _a, _b;
        try {
            var time_1 = game().game.time;
            var day_1 = game().game.day;
            var playerLocation = game().player.location;
            masterLocationConfig.forEach(function (locationConfig) {
                var isOpen = _this.isLocationOpen(locationConfig, time_1, day_1);
                var opensAt = !isOpen ? _this.getNextOpenTime(locationConfig.name, time_1, day_1) : undefined;
                LocationService.setLocation(locationConfig.name, isOpen, locationConfig.title, opensAt);
            });
            var action = (_b = (_a = this.CLOSED_ACTIONS[time_1]) === null || _a === void 0 ? void 0 : _a.closedActions) === null || _b === void 0 ? void 0 : _b[playerLocation];
            if (action) {
                LocationService.enterLocation(action.passage);
            }
        }
        catch (error) {
            throw new Error("Error updating locations: ".concat(error));
        }
    };
    TimeService.isLocationOpen = function (location, period, day) {
        var isOpen = location.openPeriods ? location.openPeriods.includes(period) : true;
        switch (location.name) {
            case 'school':
                isOpen = isOpen && day !== 'Saturday' && day !== 'Sunday';
                break;
            case 'church':
                if (period === DayPeriod.Night || period === DayPeriod.LateNight) {
                    isOpen = QuestService.isQuestActive("PackageDelivering");
                }
                break;
            case 'marcusHouse':
                if (period === DayPeriod.Evening) {
                    isOpen = window.isBoyfriend("Marcus");
                }
                break;
        }
        return isOpen;
    };
    TimeService.getDayAfter = function (day, dayOffset) {
        var dayIndex = this.DAY_ORDER.indexOf(day);
        if (dayIndex === -1) {
            return day;
        }
        var nextIndex = (dayIndex + dayOffset) % this.DAY_ORDER.length;
        return this.DAY_ORDER[nextIndex];
    };
    TimeService.getNextOpenTime = function (locationName, currentTime, day) {
        var currentIndex = this.TIME_ORDER.indexOf(currentTime);
        var locationConfig = masterLocationConfig.find(function (location) { return location.name === locationName; });
        if (currentIndex === -1 || !locationConfig)
            return undefined;
        var maxSteps = this.TIME_ORDER.length * this.DAY_ORDER.length;
        for (var step = 1; step <= maxSteps; step++) {
            var nextIndex = currentIndex + step;
            var dayOffset = Math.floor(nextIndex / this.TIME_ORDER.length);
            var period = this.TIME_ORDER[nextIndex % this.TIME_ORDER.length];
            var candidateDay = this.getDayAfter(day, dayOffset);
            if (!this.isLocationOpen(locationConfig, period, candidateDay)) {
                continue;
            }
            var label = this.TIME_PERIOD_LABELS[period];
            if (dayOffset === 0) {
                return label;
            }
            if (dayOffset === 1) {
                return "Tomorrow (".concat(label, ")");
            }
            return "".concat(candidateDay, " (").concat(label, ")");
        }
        return undefined;
    };
    TimeService.addTime = function (timeCount) {
        if (game().game.time != 'LN') {
            Cycle.get('time').update(timeCount);
        }
        this.updateGameTime();
        DrugService.updateDrugStatus(timeCount);
        EnergyService.checkEnergy();
    };
    TimeService.reduceDaysFromVariables = function () {
        try {
            if (game().player.gang.daysToWork > 0)
                game().player.gang.daysToWork--;
            var location_1 = game().location;
            if (location_1.gym.days > 0)
                location_1.gym.days--;
            if (location_1.hospital.prenatal > 0)
                location_1.hospital.prenatal--;
            if (location_1.hospital.gynecologist > 0)
                location_1.hospital.gynecologist--;
            if (location_1.clandestineClinic.inseminationDays > 0)
                location_1.clandestineClinic.inseminationDays--;
            for (var _i = 0, _a = Object.values(fastJobs().jobs); _i < _a.length; _i++) {
                var job = _a[_i];
                if (job.delayDays && job.delayDays > 0) {
                    if (job.delayDays === 1) {
                        createNotification("The job ".concat(job.name, " is now available again!"), NotificationType.INFO);
                    }
                    if (job.delayDays > 0) {
                        job.delayDays--;
                    }
                }
            }
        }
        catch (error) {
            var errorMessage = "Error in reduceDaysFromVariables: " + error;
            throw new Error(errorMessage);
        }
    };
    TimeService.resetGameCycle = function () {
        try {
            Cycle.get('time').reset();
            Cycle.get('day').update(1);
            this.updateGameTime();
            game().game.days += 1;
        }
        catch (error) {
            var errorMessage = "Error in resetGameCycle: " + error;
            throw new Error(errorMessage);
        }
    };
    TimeService.saveGame = function () {
        var _a, _b;
        try {
            if (!game().game.preferences.autoSave)
                return;
            var slot = Math.max(0, Math.min(7, game().game.preferences.autoSaveSlot || 0));
            Save.browser.slot.save(slot, "Auto Save", {
                gameVersion: ((_a = game().game) === null || _a === void 0 ? void 0 : _a.version) || window.gameVersion || 'Unknown',
                timestamp: Date.now(),
                playerName: ((_b = game().player) === null || _b === void 0 ? void 0 : _b.name) || 'Unknown'
            });
            createNotification("The game has been saved", NotificationType.SUCCESS);
        }
        catch (error) {
            var errorMessage = "Error in saveGame: " + error;
            throw new Error(errorMessage);
        }
    };
    TimeService.updateNPCs = function () {
        try {
            Object.values(game().npc).forEach(function (npcObj) {
                npcObj.talkedToday = false;
                if (npcObj.scenes) {
                    Object.values(npcObj.scenes).forEach(function (scene) {
                        scene.executedToday = false;
                    });
                }
            });
            if (game().npc.Dad.arousal < 3)
                game().npc.Dad.arousal++;
            if (game().npc.Brother.arousal < 3)
                game().npc.Brother.arousal++;
            if (game().npc.Grandpa.arousal < 3)
                game().npc.Grandpa.arousal++;
        }
        catch (error) {
            var errorMessage = "Error in updateNPCs: " + error;
            throw new Error(errorMessage);
        }
    };
    TimeService.resetLocationVariables = function () {
        try {
            Object.values(game().location).forEach(function (locObj) {
                if (locObj.scenes) {
                    Object.values(locObj.scenes).forEach(function (scene) {
                        scene.executedToday = false;
                    });
                }
            });
            instafame().posted = false;
            game().player.xcam.streamed = false;
        }
        catch (error) {
            var errorMessage = "Error in resetLocationVariables: " + error;
            throw new Error(errorMessage);
        }
    };
    TimeService.checkSchoolTest = function () {
        try {
            var school = game().location.school;
            if (school === null || school === void 0 ? void 0 : school.graduated)
                return;
            if ((school === null || school === void 0 ? void 0 : school.daysToNextTest) > 0) {
                school.daysToNextTest--;
                if (school.daysToNextTest === 0 && game().game.day === "Monday") {
                    createNotification("You have a test at school today!", NotificationType.INFO);
                }
            }
        }
        catch (error) {
            var errorMessage = "Error in checkSchoolTest: " + error;
            throw new Error(errorMessage);
        }
    };
    TimeService.updatePregnancy = function () {
        try {
            var pregnancy = game().player.pregnancy;
            var oldStage = null;
            if (PregnancyService.isPregnant() && pregnancy.days > 0) {
                oldStage = PregnancyService.getPregnancyStage();
                pregnancy.days--;
            }
            if (pregnancy.pillDays > 0) {
                pregnancy.pillDays--;
                if (pregnancy.pillDays === 0) {
                    createNotification("You can take another contraceptive pill!", NotificationType.INFO);
                }
            }
            if (PregnancyService.isPregnant()) {
                var newStage = PregnancyService.getPregnancyStage();
                if (oldStage !== null && oldStage !== newStage) {
                    if (newStage === "showing") {
                        createNotification("Your pregnancy is becoming noticeable.", NotificationType.INFO);
                    }
                    else if (newStage === "late") {
                        createNotification("You're in the final stretch. Birth is getting close.", NotificationType.INFO);
                    }
                }
                if (pregnancy.days === 2) {
                    createNotification("You could go into labor any day now.", NotificationType.INFO);
                }
            }
            ClothService.updateClothes(PregnancyService.changeMediaPregnant());
        }
        catch (error) {
            var errorMessage = "Error in updatePregnancy: " + error;
            throw new Error(errorMessage);
        }
    };
    TimeService.checkQuests = function () {
        try {
            var isPhonePurchased = InventoryService.isPurchased("phone");
            QuestService.checkScheduledQuests();
            if (isPhonePurchased) {
                if (QuestService.isQuestActive("CostumeParty") && QuestService.getQuestProgress("CostumeParty") == 0) {
                    PhoneService.newMessage("VeronicaCostumeParty");
                }
                if (game().npc.Jamal.scenes.JamalBilliardsSex.unlocked &&
                    !QuestService.isQuestActive("PoolParty") &&
                    game().game.day === "Friday" &&
                    CorruptionService.getCorruptionLevel() >= 4) {
                    PhoneService.newMessage("JamalPoolParty");
                }
            }
            if (QuestService.isQuestActive("ThomasParty")) {
                var questProgress = QuestService.getQuestProgress("ThomasParty");
                var isFriday = game().game.day === "Friday";
                var THOMAS_PARTY_PROGRESS = {
                    INITIAL: 0,
                    REMINDED_FRIDAY: 1,
                    STEAL_KEY: 2,
                    KEY_STEALED: 3
                };
                if (isFriday && questProgress == THOMAS_PARTY_PROGRESS.REMINDED_FRIDAY) {
                    var questMessage = "I need to steal my ".concat(game().npc.Dad.relationship, "'s car so I can go to the party. I think the key is in his bedroom");
                    // Only update the quest progress if is the first friday since the invite
                    var points = questProgress == THOMAS_PARTY_PROGRESS.REMINDED_FRIDAY ? 1 : 0;
                    QuestService.updateQuest("ThomasParty", points, questMessage);
                    return;
                }
                else {
                    if (questProgress == THOMAS_PARTY_PROGRESS.KEY_STEALED || questProgress == THOMAS_PARTY_PROGRESS.STEAL_KEY) {
                        QuestService.cancelQuest("ThomasParty", "I missed Thomas's party. I should try again next time");
                        return;
                    }
                }
            }
        }
        catch (error) {
            var errorMessage = "Error in checkQuests: " + error;
            throw new Error(errorMessage);
        }
    };
    TimeService.getDayPeriodByEnum = function (timeEnum) {
        try {
            switch (timeEnum) {
                case DayPeriod.EarlyMorning:
                    return "Early Morning";
                case DayPeriod.Morning:
                    return "Morning";
                case DayPeriod.Afternoon:
                    return "Afternoon";
                case DayPeriod.Evening:
                    return "Evening";
                case DayPeriod.Night:
                    return "Night";
                case DayPeriod.LateNight:
                    return "Late Night";
                default:
                    throw new Error("Invalid time enum provided");
            }
        }
        catch (error) {
            var errorMessage = "Error in getDayPeriod: " + error;
            throw new Error(errorMessage);
        }
    };
    TimeService.relationshipMessages = function () {
        var isPhonePurchased = InventoryService.isPurchased("phone");
        if (isPhonePurchased) {
            //MARCUS
            var marcusRelation = game().npc.Marcus.relation;
            if (marcusRelation >= 15 && QuestService.isQuestAvailable("MarcusDate") && !PlayerService.isBoyfriend("Marcus")) {
                QuestService.startQuest("MarcusDate");
                PhoneService.newMessage("MarcusDate");
            }
        }
    };
    TimeService.changeLaundryCut = function () {
        if (game().game.day === "Saturday" || game().game.day === "Sunday") {
            game().location.laundry.cut = 10;
        }
        else {
            game().location.laundry.cut = 20;
        }
    };
    TimeService.getTime = function () {
        return game().game.time;
    };
    TimeService.getDay = function () {
        return game().game.day;
    };
    TimeService.TIME_ORDER = ['EM', 'M', 'A', 'E', 'N', 'LN'];
    TimeService.DAY_ORDER = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
    TimeService.TIME_PERIOD_LABELS = {
        EM: 'Early Morning',
        M: 'Morning',
        A: 'Afternoon',
        E: 'Evening',
        N: 'Night',
        LN: 'Late Night'
    };
    TimeService.CLOSED_ACTIONS = {
        E: {
            closedActions: {
                Office: { passage: 'center', message: "Office is closed!" },
                MarcusHouse: { passage: 'residential', message: "There's no one at Marcus's house at this time", check: function () { return !window.isBoyfriend("Marcus"); } },
            }
        },
        N: {
            closedActions: {
                EmmaHouse: { passage: 'residential', message: "There's no one at Emma's house at this time" },
                School: { passage: 'residential', message: "School is closed!" },
                Pool: { passage: 'center', message: "Pool is closed!" }
            }
        },
        LN: {
            closedActions: {
                Mall: { passage: 'center', message: "Mall is closed!" }
            }
        }
    };
    return TimeService;
}());
/* twine-user-script #105: "WeatherService.js" */
"use strict";
var WeatherService = /** @class */ (function () {
    function WeatherService() {
    }
    WeatherService.initWeather = function () {
        var weather = this.normalizeWeather(game().game.weather);
        game().game.weather = weather;
        game().game.weatherIcon = this.getWeatherIcon(weather);
    };
    WeatherService.rollDailyWeather = function () {
        var weather = this.getRandomWeather();
        game().game.weather = weather;
        game().game.weatherIcon = this.getWeatherIcon(weather);
    };
    WeatherService.updateWeatherUI = function () {
        var weather = this.normalizeWeather(game().game.weather);
        game().game.weather = weather;
        game().game.weatherIcon = this.getWeatherIcon(weather);
        this.applyWeatherClassToTimeSummaryCard(weather);
    };
    WeatherService.applyWeatherClassToTimeSummaryCard = function (weather) {
        var _this = this;
        var cards = document.querySelectorAll(".sidebar-card--time");
        if (!cards.length)
            return;
        cards.forEach(function (card) {
            for (var _i = 0, _a = _this.WEATHER_CLASSES; _i < _a.length; _i++) {
                var w = _a[_i];
                card.classList.remove("weather-".concat(w));
            }
            card.classList.add("weather-".concat(weather));
        });
    };
    WeatherService.normalizeWeather = function (weather) {
        if (weather === "cloudy" || weather === "rain" || weather === "clear") {
            return weather;
        }
        return "clear";
    };
    WeatherService.getWeatherIcon = function (weather) {
        switch (weather) {
            case "cloudy":
                return "☁️";
            case "rain":
                return "🌧️";
            default:
                return "☀️";
        }
    };
    WeatherService.getRandomWeather = function () {
        var roll = Math.random() * 100;
        if (roll < 55) {
            return "clear";
        }
        if (roll < 80) {
            return "cloudy";
        }
        return "rain";
    };
    WeatherService.WEATHER_CLASSES = ["clear", "cloudy", "rain"];
    return WeatherService;
}());
/* twine-user-script #106: "audio.utils.js" */
"use strict";
function loadAudioTracks() {
    // CENTER BGM
    SimpleAudio.tracks.add("centerbgm", "sounds/center/centerbgm.mp3");
    SimpleAudio.tracks.add("beachbgm", "sounds/center/beach/beachbgm.mp3");
    SimpleAudio.tracks.add("gymbgm", "sounds/center/gym/gymbgm.mp3");
    SimpleAudio.tracks.add("restaurantbgm", "sounds/center/restaurant/restaurantbgm.mp3");
    SimpleAudio.tracks.add("mallbgm", "sounds/center/mall/mallbgm.mp3");
    SimpleAudio.tracks.add("poolbgm", "sounds/center/pool/poolbgm.mp3");
    SimpleAudio.tracks.add("policebgm", "sounds/center/police/policebgm.mp3");
    SimpleAudio.tracks.add("hospitalbgm", "sounds/center/hospital/hospitalbgm.mp3");
    SimpleAudio.tracks.add("officebgm", "sounds/center/office/officebgm.mp3");
    SimpleAudio.tracks.add("hotelbgm", "sounds/center/hotel/hotelbgm.mp3");
    SimpleAudio.tracks.add("barbgm", "sounds/center/bar/barbgm.mp3");
    SimpleAudio.tracks.add("clubbgm", "sounds/center/club/clubbgm.mp3");
    SimpleAudio.tracks.add("clubhallbgm", "sounds/center/club/clubhallbgm.mp3");
    SimpleAudio.tracks.add("beachnightbgm", "sounds/center/beach/beachbgm.mp3");
    SimpleAudio.tracks.add("photostudiobgm", "sounds/center/photostudio/photostudiobmg.mp3");
    // RESIDENTIAL
    SimpleAudio.tracks.add("schoolbgm", "sounds/residential/school/schoolbgm.mp3");
    SimpleAudio.tracks.add("parkbgm", "sounds/residential/park/parkbgm.mp3");
    SimpleAudio.tracks.add("residentialbgm", "sounds/residential/residentialbgm.mp3");
    SimpleAudio.tracks.add("parklatenightbgm", "sounds/ghetto/darkalley/darkalleybgm.mp3");
    // ELITE
    SimpleAudio.tracks.add("elitebgm", "sounds/elite/elitebgm.mp3");
    // GHETTO
    SimpleAudio.tracks.add("ghettobgm", "sounds/ghetto/ghettobgm.mp3");
    SimpleAudio.tracks.add("churchbgm", "sounds/ghetto/church/churchbgm.mp3");
    SimpleAudio.tracks.add("stripclubbgm", "sounds/ghetto/stripclub/stripclubbgm.mp3");
    SimpleAudio.tracks.add("darkalleybgm", "sounds/ghetto/darkalley/darkalleybgm.mp3");
    SimpleAudio.tracks.add("abandonedbuildingbgm", "sounds/ghetto/darkalley/darkalleybgm.mp3");
    SimpleAudio.tracks.add("vipersbgm", "sounds/ghetto/vipers/vipersbgm.mp3");
    // BUS STOP
    SimpleAudio.tracks.add("busstopbgm", "sounds/center/centerbgm.mp3");
}
var BGM_VOLUME_RANGE_MAX = 100;
var BGM_VOLUME_DEFAULT = 0.5;
function getBgmVolume() {
    var settingsWithVolume = settings;
    var raw = typeof settings !== "undefined" && settingsWithVolume.volume != null
        ? Number(settingsWithVolume.volume)
        : BGM_VOLUME_RANGE_MAX * BGM_VOLUME_DEFAULT;
    var clamped = Math.max(0, Math.min(BGM_VOLUME_RANGE_MAX, raw));
    return clamped / BGM_VOLUME_RANGE_MAX;
}
function loadBgmAudio() {
    var bgmKey = "".concat(passage().toLowerCase(), "bgm");
    SimpleAudio.stop();
    if (SimpleAudio.tracks.has(bgmKey)) {
        var selectedAudio = SimpleAudio.select(bgmKey);
        if (selectedAudio) {
            selectedAudio.loop(true).volume(getBgmVolume()).play();
        }
    }
}
/* twine-user-script #107: "helpers.utils.js" */
"use strict";
function rollTheDice(chance) {
    return random(1, 100) <= chance;
}
function randomFrom(arr) {
    return arr[Math.floor(Math.random() * arr.length)];
}
function galleryMode() {
    return game().dev.galleryMode;
}
/* twine-user-script #108: "modal.utils.js" */
"use strict";
function openRandomEventModal(eventName) {
    var _a, _b, _c, _d;
    var randomEvents = [
        { eventName: "SpermCollect", title: "<h4>You collected his sperm!</h4>You can go to the hospital and do the <b>DNA Test</b>", img: "images/player/pregnancy/spermcollect.webp" },
    ];
    var event = randomEvents.find(function (e) { return e.eventName === eventName; });
    var randomEventTextElement = document.getElementById("randomEventText");
    if (randomEventTextElement) {
        randomEventTextElement.innerHTML = ((_a = event === null || event === void 0 ? void 0 : event.title) !== null && _a !== void 0 ? _a : "").replace(/\n/g, "<br>");
    }
    var randomEventImage = document.getElementById("randomEventImage");
    if (randomEventImage) {
        randomEventImage.src = (_b = event === null || event === void 0 ? void 0 : event.img) !== null && _b !== void 0 ? _b : "";
    }
    (_c = document.getElementById("randomEventOverlay")) === null || _c === void 0 ? void 0 : _c.classList.add("show");
    (_d = document.getElementById("randomEvent")) === null || _d === void 0 ? void 0 : _d.classList.add("show");
}
function createRandomEventModal() {
    var modalHtml = "\n    <div id=\"randomEventOverlay\"></div>\n    <div id=\"randomEvent\">\n      <img id=\"randomEventImage\" src=\"\" alt=\"\">\n      <p id=\"randomEventText\"></p>\n      <div style=\"text-align: center;\"><button id=\"closeRandomEvent\">Close</button></div>\n    </div>\n  ";
    var container = document.createElement('div');
    container.innerHTML = modalHtml;
    document.body.appendChild(container);
    document.addEventListener('click', function (event) {
        var _a, _b;
        if (event.target.id === 'closeRandomEvent') {
            (_a = document.getElementById('randomEventOverlay')) === null || _a === void 0 ? void 0 : _a.classList.remove('show');
            (_b = document.getElementById('randomEvent')) === null || _b === void 0 ? void 0 : _b.classList.remove('show');
        }
    });
}
function showVersionModal() {
    var modal = document.createElement('div');
    modal.className = 'version-modal-overlay';
    modal.setAttribute('role', 'dialog');
    modal.setAttribute('aria-modal', 'true');
    modal.setAttribute('aria-labelledby', 'version-modal-title');
    var gameUrl = "https://roadtosuccess.fun/";
    var downloadUrl = "https://f95zone.to/threads/road-to-success-v0-11-astk.191541/";
    if (window.patreon) {
        gameUrl = "https://patreon.roadtosuccess.fun/";
        downloadUrl = "https://www.patreon.com/c/astk1";
    }
    var content = document.createElement('div');
    content.className = 'version-modal-content';
    content.innerHTML = "\n        <button class=\"version-close\" aria-label=\"Close dialog\" id=\"closeModalBtn\">\n          <svg width=\"18\" height=\"18\" viewBox=\"0 0 24 24\" fill=\"none\" aria-hidden=\"true\">\n            <path d=\"M6 6l12 12M18 6L6 18\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\"/>\n          </svg>\n        </button>\n\n        <div class=\"version-modal-header\">\n          <div class=\"version-modal-icon\" aria-hidden=\"true\">\n            <svg width=\"22\" height=\"22\" viewBox=\"0 0 24 24\" fill=\"none\">\n              <path d=\"M12 3v18M3 12h18\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\"/>\n            </svg>\n          </div>\n          <h2 id=\"version-modal-title\">New version available</h2>\n        </div>\n\n        <div class=\"version-modal-body\">\n          <p>There's a newer version available! If you are playing the online version, please ask the site administrator to update it.</p>\n          <div class=\"version-grid\" role=\"group\" aria-label=\"Version information\">\n            <div class=\"version-cell\">\n              <span class=\"version-label\">Your version</span>\n              <span class=\"version-value\">".concat(window.gameVersion, "</span>\n            </div>\n            <div class=\"version-cell\">\n              <span class=\"version-label\">Latest version</span>\n              <span class=\"version-value\">").concat(window.lastVersion, "</span>\n            </div>\n          </div>\n        </div>\n\n        <div class=\"version-modal-actions\">\n          <button class=\"version-btn primary\"\n                  onclick=\"window.open('").concat(downloadUrl, "', '_blank')\">\n            Download the new version\n          </button>\n          <button class=\"version-btn secondary\"\n                  onclick=\"window.open('").concat(gameUrl, "', '_blank')\">\n            Play the new version online\n          </button>\n        </div>\n      ");
    modal.appendChild(content);
    document.body.appendChild(modal);
    var closeBtn = content.querySelector('#closeModalBtn');
    var laterBtn = content.querySelector('#dismissModalBtn');
    var updateBtn = content.querySelector('#goUpdateBtn');
    (updateBtn || laterBtn || closeBtn).focus();
    var focusables = content.querySelectorAll('button, [href], [tabindex]:not([tabindex="-1"])');
    var first = focusables[0], last = focusables[focusables.length - 1];
    content.addEventListener('keydown', function (e) {
        if (e.key === 'Tab') {
            if (e.shiftKey && document.activeElement === first) {
                e.preventDefault();
                last.focus();
            }
            else if (!e.shiftKey && document.activeElement === last) {
                e.preventDefault();
                first.focus();
            }
        }
        else if (e.key === 'Escape') {
            removeModal();
        }
    });
    // Close behaviors
    function removeModal() {
        modal.remove();
    }
    if (closeBtn) {
        closeBtn.addEventListener('click', removeModal);
    }
    if (laterBtn) {
        laterBtn.addEventListener('click', removeModal);
    }
    modal.addEventListener('click', function (e) {
        if (e.target === modal)
            removeModal();
    });
}
/* twine-user-script #109: "passageHeader.utils.js" */
"use strict";
var PassageHeaderEnhancer = /** @class */ (function () {
    function PassageHeaderEnhancer() {
    }
    PassageHeaderEnhancer.findPassageElement = function (root) {
        var $root = $(root);
        if ($root.hasClass("passage")) {
            return $root;
        }
        var $inRoot = $root.find(".passage").first();
        if ($inRoot.length) {
            return $inRoot;
        }
        var $closest = $root.closest(".passage");
        return $closest.length ? $closest : $();
    };
    PassageHeaderEnhancer.enhancePassageHeader = function (root) {
        var $passage = PassageHeaderEnhancer.findPassageElement(root);
        if (!$passage.length)
            return;
        var $firstChild = $passage.children().first();
        var $container = $firstChild.is("center") ? $firstChild : $passage;
        if ($container.children(".passage-header").length)
            return;
        var $first = $container.children().first();
        if (!$first.is("h1.ptitle, h2.ptitle"))
            return;
        var headerNodes = [];
        var $node = $first;
        while ($node.length && $node.is("h1, h2, h3")) {
            headerNodes.push($node[0]);
            $node = $node.next();
        }
        if (!headerNodes.length)
            return;
        var $header = $('<div class="passage-header"></div>');
        $(headerNodes[0]).before($header);
        $header.append(headerNodes);
    };
    PassageHeaderEnhancer.init = function () {
        if (PassageHeaderEnhancer.initialized)
            return;
        PassageHeaderEnhancer.initialized = true;
        $(document).on(":passageend", function (ev) {
            var root = (ev && (ev.content || ev.target)) || document;
            PassageHeaderEnhancer.enhancePassageHeader(root);
        });
        // Also enhance the currently displayed passage (if any).
        PassageHeaderEnhancer.enhancePassageHeader(document);
    };
    PassageHeaderEnhancer.initialized = false;
    return PassageHeaderEnhancer;
}());
window.PassageHeaderEnhancer = PassageHeaderEnhancer;
/* twine-user-script #110: "ui.utils.js" */
"use strict";
function toggleLeftBar() {
    if (UIBar.isStowed()) {
        UIBar.unstow();
        UIBar.show();
    }
    else {
        UIBar.stow();
        UIBar.hide();
    }
}
function hideRightBar() {
    $rightUiBar.addClass('stowed').css('display', 'none');
}
function toggleRightBar() {
    if ($rightUiBar.hasClass('stowed')) {
        $rightUiBar.removeClass('stowed').css('display', 'block');
    }
    else {
        $rightUiBar.addClass('stowed').css('display', 'none');
    }
}
function updateBar() {
    try {
        $('#story-caption').empty().wiki(Story.get('StoryCaption').processText());
        updateRight();
    }
    catch (error) {
        throw new Error("UpdateBar failed: " + error);
    }
}
function updateScreen() {
    try {
        Engine.show();
    }
    catch (error) {
        throw new Error("UpdateScreen failed: " + error);
    }
}
/* twine-user-script #111: "version.utils.js" */
"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g = Object.create((typeof Iterator === "function" ? Iterator : Object).prototype);
    return g.next = verb(0), g["throw"] = verb(1), g["return"] = verb(2), typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (g && (g = 0, op[0] && (_ = 0)), _) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
function checkVersion() {
    return __awaiter(this, void 0, void 0, function () {
        var isNothinGames, isMopoga, isLewdspot, _a;
        return __generator(this, function (_b) {
            switch (_b.label) {
                case 0:
                    isNothinGames = window.location.hostname.includes("nothingames");
                    isMopoga = window.location.hostname.includes("mopoga");
                    isLewdspot = window.location.hostname.includes("lewdspot");
                    if (isNothinGames || isMopoga || isLewdspot)
                        return [2 /*return*/];
                    _a = window;
                    return [4 /*yield*/, getLastGameVersion()];
                case 1:
                    _a.lastVersion = _b.sent();
                    console.log("Current version: ".concat(window.gameVersion, ", Latest version: ").concat(window.lastVersion));
                    if (isLatestGreater(window.gameVersion, window.lastVersion)) {
                        showVersionModal();
                    }
                    return [2 /*return*/];
            }
        });
    });
}
function parseSimpleVersion(v) {
    var _a, _b;
    var core = (_b = (_a = (v || "").match(/\d+(?:\.\d+)*/)) === null || _a === void 0 ? void 0 : _a[0]) !== null && _b !== void 0 ? _b : "0";
    var _c = core.split("."), _d = _c[0], maj = _d === void 0 ? "0" : _d, _e = _c[1], min = _e === void 0 ? "0" : _e, _f = _c[2], pat = _f === void 0 ? "0" : _f;
    return [parseInt(maj, 10) || 0, parseInt(min, 10) || 0, parseInt(pat, 10) || 0];
}
function isLatestGreater(current, latest) {
    var _a = parseSimpleVersion(current), cMaj = _a[0], cMin = _a[1], cPat = _a[2];
    var _b = parseSimpleVersion(latest), lMaj = _b[0], lMin = _b[1], lPat = _b[2];
    if (lMaj !== cMaj)
        return lMaj > cMaj; // e.g., 0.x -> 1.x
    if (lMin !== cMin)
        return lMin > cMin; // e.g., 0.19 -> 0.20
    return lPat > cPat; // e.g., 0.19.0 -> 0.19.1
}
window.isVersionOutdated = function () {
    if (!window.lastVersion)
        return false;
    return isLatestGreater(window.gameVersion, window.lastVersion);
};
window.getVersionWarningTooltip = function () {
    if (!window.isVersionOutdated())
        return "";
    return "A newer version is available: v".concat(window.lastVersion);
};
function getLastGameVersion() {
    return __awaiter(this, void 0, void 0, function () {
        var endpoint, response, data, error_1;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    _a.trys.push([0, 3, , 4]);
                    endpoint = "publicVersion";
                    if (window.patreon) {
                        endpoint = "patreonVersion";
                    }
                    return [4 /*yield*/, fetch("https://rts.astkgaming.workers.dev/".concat(endpoint))];
                case 1:
                    response = _a.sent();
                    return [4 /*yield*/, response.json()];
                case 2:
                    data = _a.sent();
                    console.log("Successfully fetched the latest game version:", data.version);
                    return [2 /*return*/, data.version];
                case 3:
                    error_1 = _a.sent();
                    console.error("Failed to fetch the latest game version:", error_1);
                    return [2 /*return*/, window.gameVersion];
                case 4: return [2 /*return*/];
            }
        });
    });
}
