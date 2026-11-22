(function (window) {
  'use strict';

  const STORAGE_KEY = 'sme-credit:reading-progress:v1';
  const VERSION = 1;
  let memoryDocument = emptyDocument();
  let hasUnsavedChanges = false;
  let loadedFromStorage = false;
  let dirtyCompletion = false;
  const dirtyDays = new Set();
  const recentlyWrittenDays = new Set();
  const subscribers = new Map();
  const completionSubscribers = new Set();
  const boundDays = new Set();
  const wrappedResetHandlers = new WeakSet();

  function emptyDocument() {
    return { version: VERSION, days: {}, completedDays: [], completedInitialized: false };
  }

  function normalizeCompletedDays(values) {
    if (!Array.isArray(values)) return [];
    return Array.from(new Set(values.filter(function (value) {
      return Number.isInteger(value) && value >= 1 && value <= 30;
    }))).sort(function (a, b) { return a - b; });
  }

  function normalizeDocument(value) {
    if (!value || typeof value !== 'object' || value.version !== VERSION || !value.days || typeof value.days !== 'object' || Array.isArray(value.days)) {
      return emptyDocument();
    }

    const days = {};
    Object.keys(value.days).forEach(function (key) {
      const day = Number(key);
      if (!Number.isInteger(day) || day < 1 || day > 30 || !Array.isArray(value.days[key])) return;
      days[String(day)] = normalizeIds(value.days[key]);
    });
    return {
      version: VERSION,
      days: days,
      completedDays: normalizeCompletedDays(value.completedDays),
      completedInitialized: value.completedInitialized === true
    };
  }

  function normalizeIds(ids) {
    if (!Array.isArray(ids)) return [];
    return Array.from(new Set(ids.filter(function (id) {
      return typeof id === 'string' && id.trim().length > 0;
    })));
  }

  function parseStoredDocument(raw) {
    try {
      const value = JSON.parse(raw);
      if (!value || typeof value !== 'object' || value.version !== VERSION || !value.days || typeof value.days !== 'object' || Array.isArray(value.days)) {
        return null;
      }
      return normalizeDocument(value);
    } catch (error) {
      return null;
    }
  }

  function readDocument() {
    if (hasUnsavedChanges || loadedFromStorage) return memoryDocument;
    loadedFromStorage = true;
    try {
      const raw = window.localStorage.getItem(STORAGE_KEY);
      memoryDocument = raw === null
        ? emptyDocument()
        : normalizeDocument(JSON.parse(raw));
    } catch (error) {
      // Keep the last valid in-memory value when storage is unavailable.
    }
    return memoryDocument;
  }

  function writeDocument(document, options) {
    const next = normalizeDocument(document);
    if (!(options && options.completion) && !dirtyCompletion) {
      try {
        const raw = window.localStorage.getItem(STORAGE_KEY);
        if (raw !== null) {
          const latest = normalizeDocument(JSON.parse(raw));
          if (latest.completedInitialized) {
            next.completedDays = latest.completedDays.slice();
            next.completedInitialized = true;
          }
        }
      } catch (error) {
        // Keep the completion state already in memory.
      }
    }
    memoryDocument = next;
    try {
      window.localStorage.setItem(STORAGE_KEY, JSON.stringify(memoryDocument));
      hasUnsavedChanges = false;
      loadedFromStorage = true;
      dirtyDays.clear();
      dirtyCompletion = false;
      return true;
    } catch (error) {
      // The current page continues from its in-memory copy.
      hasUnsavedChanges = true;
      return false;
    }
  }

  function commitDocument(document, options) {
    const carried = Array.from(dirtyDays);
    if (writeDocument(document, options)) {
      carried.forEach(function (key) { recentlyWrittenDays.add(key); });
      if (options && options.dayKey !== undefined) recentlyWrittenDays.add(options.dayKey);
    } else {
      if (options && options.dayKey !== undefined) dirtyDays.add(options.dayKey);
      if (options && options.completion) dirtyCompletion = true;
    }
  }

  function validateDay(dayNumber) {
    if (!Number.isInteger(dayNumber) || dayNumber < 1 || dayNumber > 30) {
      throw new RangeError('dayNumber must be an integer from 1 to 30');
    }
  }

  function validateChapterId(chapterId) {
    if (typeof chapterId !== 'string' || chapterId.trim().length === 0) {
      throw new TypeError('chapterId must be a non-empty string');
    }
  }

  function getReadIds(dayNumber) {
    validateDay(dayNumber);
    const document = readDocument();
    return (document.days[String(dayNumber)] || []).slice();
  }

  function initializeDay(dayNumber, legacyReadIds) {
    validateDay(dayNumber);
    const document = readDocument();
    const key = String(dayNumber);
    if (!Object.prototype.hasOwnProperty.call(document.days, key)) {
      document.days[key] = normalizeIds(legacyReadIds);
      commitDocument(document, { dayKey: key });
    }
    return (document.days[key] || []).slice();
  }

  function setRead(dayNumber, chapterId, isRead) {
    validateDay(dayNumber);
    validateChapterId(chapterId);
    const document = readDocument();
    const key = String(dayNumber);
    const ids = new Set(document.days[key] || []);
    if (isRead) ids.add(chapterId);
    else ids.delete(chapterId);
    document.days[key] = Array.from(ids);
    commitDocument(document, { dayKey: key });
    return document.days[key].slice();
  }

  function setDayReadIds(dayNumber, readIds) {
    validateDay(dayNumber);
    const document = readDocument();
    const key = String(dayNumber);
    document.days[key] = normalizeIds(readIds);
    commitDocument(document, { dayKey: key });
    return document.days[key].slice();
  }

  function resetDay(dayNumber) {
    validateDay(dayNumber);
    const document = readDocument();
    const key = String(dayNumber);
    // Keep an explicit empty entry so legacy state cannot repopulate a reset day.
    document.days[key] = [];
    commitDocument(document, { dayKey: key });
  }

  function getCompletedDays() {
    return readDocument().completedDays.slice();
  }

  function initializeCompletedDays(legacyCompletedDays) {
    const document = readDocument();
    if (document.completedInitialized) return document.completedDays.slice();
    document.completedDays = normalizeCompletedDays(legacyCompletedDays);
    document.completedInitialized = true;
    commitDocument(document, { completion: true });
    return document.completedDays.slice();
  }

  function setDayCompleted(dayNumber, isCompleted) {
    validateDay(dayNumber);
    const document = readDocument();
    const completed = new Set(document.completedDays);
    if (isCompleted) completed.add(dayNumber);
    else completed.delete(dayNumber);
    document.completedDays = Array.from(completed).sort(function (a, b) { return a - b; });
    document.completedInitialized = true;
    commitDocument(document, { completion: true });
    return document.completedDays.slice();
  }

  function setCompletedDays(completedDays) {
    const document = readDocument();
    document.completedDays = normalizeCompletedDays(completedDays);
    document.completedInitialized = true;
    commitDocument(document, { completion: true });
    return document.completedDays.slice();
  }

  function resetCompletedDays() {
    return setCompletedDays([]);
  }

  function subscribeCompleted(callback) {
    if (typeof callback !== 'function') throw new TypeError('callback must be a function');
    completionSubscribers.add(callback);
    return function unsubscribe() {
      completionSubscribers.delete(callback);
    };
  }

  function subscribe(dayNumber, callback) {
    validateDay(dayNumber);
    if (typeof callback !== 'function') throw new TypeError('callback must be a function');
    const key = String(dayNumber);
    if (!subscribers.has(key)) subscribers.set(key, new Set());
    subscribers.get(key).add(callback);
    return function unsubscribe() {
      const callbacks = subscribers.get(key);
      if (callbacks) {
        callbacks.delete(callback);
        if (callbacks.size === 0) subscribers.delete(key);
      }
    };
  }

  function parseChapterHandler(input) {
    if (!input || typeof input.getAttribute !== 'function') return null;
    const handler = input.getAttribute('onchange') || '';
    const call = handler.match(/\b(toggleRead[A-Za-z]*|toggleChapterRead)\s*\(\s*(?:['"]([^'"]+)['"]|(\d+))/);
    if (!call) return null;
    return {
      name: call[1],
      id: call[2] || call[3],
      isNumeric: call[2] === undefined
    };
  }

  function getChapterId(input) {
    const parsed = parseChapterHandler(input);
    return parsed ? parsed.id : null;
  }

  function getChapterInputs() {
    if (!window.document || typeof window.document.querySelectorAll !== 'function') return [];
    return Array.from(window.document.querySelectorAll('input[type="checkbox"][onchange]')).filter(function (input) {
      return getChapterId(input) !== null;
    });
  }

  function normalizeLegacyIds(legacyState) {
    if (Array.isArray(legacyState)) {
      return legacyState.filter(function (id) {
        return (typeof id === 'string' && id.trim().length > 0) || (typeof id === 'number' && Number.isFinite(id));
      }).map(String);
    }
    if (legacyState && typeof legacyState === 'object') {
      return Object.keys(legacyState).filter(function (id) { return legacyState[id] === true; });
    }
    return [];
  }

  function bindResetHandlers(dayNumber) {
    if (!window.document || typeof window.document.querySelectorAll !== 'function') return;
    const buttons = window.document.querySelectorAll('button[onclick]');
    Array.from(buttons).forEach(function (button) {
      const handlerText = button.getAttribute('onclick') || '';
      const match = handlerText.match(/^\s*([A-Za-z_$][\w$]*)\s*\(/);
      if (!match || !/reset/i.test(match[1])) return;
      const handler = window[match[1]];
      if (typeof handler !== 'function' || wrappedResetHandlers.has(handler)) return;
      const wrapped = function () {
        const args = Array.from(arguments);
        const resetButton = args.find(function (arg) { return arg && arg.dataset; });
        const wasArmed = Boolean(resetButton && resetButton.dataset.armed === 'true');
        const result = handler.apply(this, args);
        if (wasArmed && resetButton.dataset.armed !== 'true') resetDay(dayNumber);
        return result;
      };
      wrappedResetHandlers.add(handler);
      wrappedResetHandlers.add(wrapped);
      window[match[1]] = wrapped;
      button.__courseProgressResetHandler = match[1];
    });
  }

  function bindPage(dayNumber, legacyState) {
    validateDay(dayNumber);
    if (boundDays.has(dayNumber) || !window.document || typeof window.document.addEventListener !== 'function') return;
    boundDays.add(dayNumber);

    let syncing = false;
    let chapterHandler = null;
    function syncCheckboxes(readIds) {
      const wanted = new Set(readIds);
      const inputs = getChapterInputs();
      for (let index = 0; index < inputs.length && !chapterHandler; index += 1) {
        chapterHandler = parseChapterHandler(inputs[index]);
      }
      const groups = new Map();
      inputs.forEach(function (input) {
        const id = getChapterId(input);
        if (!groups.has(id)) groups.set(id, []);
        groups.get(id).push(input);
      });

      syncing = true;
      groups.forEach(function (inputs, id) {
        const checked = wanted.has(id);
        let changed = false;
        inputs.forEach(function (input) {
          if (input.checked !== checked) {
            input.checked = checked;
            changed = true;
          }
        });
        if (changed && inputs[0] && typeof inputs[0].dispatchEvent === 'function') {
          inputs[0].dispatchEvent(new window.Event('change', { bubbles: true }));
        }
      });
      syncing = false;
    }

    function reconcileDay(readIds, previousIds) {
      syncCheckboxes(readIds);
      if (!chapterHandler) return;
      const inputs = getChapterInputs();
      const handler = window[chapterHandler.name];
      if (typeof handler !== 'function') return;

      // Filtered-out chapters have no checkbox to dispatch, so update the page
      // through the same handler the chapter input uses.
      const visible = new Set(inputs.map(getChapterId));
      const wanted = new Set(readIds);
      const ids = new Set();
      (previousIds || []).forEach(function (id) { ids.add(String(id)); });
      readIds.forEach(function (id) { ids.add(String(id)); });
      ids.forEach(function (id) {
        if (visible.has(id)) return;
        const value = chapterHandler.isNumeric && /^\d+$/.test(id) ? Number(id) : id;
        try {
          handler.call(window, value, wanted.has(id));
        } catch (error) {
          // One chapter handler must not block the remaining chapters.
        }
      });
    }

    const legacyIds = normalizeLegacyIds(legacyState).concat(getChapterInputs().filter(function (input) { return input.checked; }).map(getChapterId));
    reconcileDay(initializeDay(dayNumber, legacyIds), legacyIds);
    subscribe(dayNumber, reconcileDay);
    window.document.addEventListener('change', function (event) {
      if (syncing || !event || !event.target) return;
      const chapterId = getChapterId(event.target);
      if (chapterId !== null) setRead(dayNumber, chapterId, Boolean(event.target.checked));
    });
    bindResetHandlers(dayNumber);

    if (typeof window.MutationObserver === 'function' && window.document.body) {
      let scheduled = false;
      const observer = new window.MutationObserver(function () {
        if (scheduled) return;
        scheduled = true;
        const run = function () {
          scheduled = false;
          syncCheckboxes(getReadIds(dayNumber));
        };
        if (typeof window.requestAnimationFrame === 'function') window.requestAnimationFrame(run);
        else run();
      });
      observer.observe(window.document.body, { childList: true, subtree: true });
    }
  }

  window.addEventListener('storage', function (event) {
    if (!event || (event.key !== null && event.key !== STORAGE_KEY)) return;
    const isClear = event.key === null || event.newValue === null;
    const previous = memoryDocument;
    let incoming;
    if (isClear) {
      incoming = emptyDocument();
    } else {
      incoming = parseStoredDocument(event.newValue);
      if (!incoming) return;
    }

    const merged = {
      version: VERSION,
      days: Object.assign({}, incoming.days),
      completedDays: incoming.completedDays.slice(),
      completedInitialized: incoming.completedInitialized
    };
    const repaired = new Set();
    let completionRepair = false;

    // Days whose writes failed stay local until a full write succeeds.
    dirtyDays.forEach(function (key) {
      if (!Object.prototype.hasOwnProperty.call(memoryDocument.days, key)) {
        delete merged.days[key];
        return;
      }
      merged.days[key] = memoryDocument.days[key].slice();
      repaired.add(key);
    });

    // A concurrently written document that omitted a day this tab just wrote
    // indicates a lost update; merge that day back in.
    if (isClear) {
      recentlyWrittenDays.clear();
    } else {
      Array.from(recentlyWrittenDays).forEach(function (key) {
        recentlyWrittenDays.delete(key);
        if (Object.prototype.hasOwnProperty.call(incoming.days, key)) return;
        if (!Object.prototype.hasOwnProperty.call(memoryDocument.days, key)) return;
        merged.days[key] = memoryDocument.days[key].slice();
        repaired.add(key);
      });
    }

    if (isClear) {
      if (dirtyCompletion) {
        merged.completedDays = memoryDocument.completedDays.slice();
        merged.completedInitialized = memoryDocument.completedInitialized;
      }
    } else if (dirtyCompletion) {
      merged.completedDays = memoryDocument.completedDays.slice();
      merged.completedInitialized = memoryDocument.completedInitialized;
      completionRepair = true;
    } else if (!incoming.completedInitialized) {
      merged.completedDays = memoryDocument.completedDays.slice();
      merged.completedInitialized = memoryDocument.completedInitialized;
      completionRepair = memoryDocument.completedInitialized;
    }

    memoryDocument = normalizeDocument(merged);
    loadedFromStorage = true;

    if (!isClear && (repaired.size > 0 || completionRepair)) {
      if (writeDocument(memoryDocument)) {
        repaired.forEach(function (key) { recentlyWrittenDays.add(key); });
      } else {
        repaired.forEach(function (key) { dirtyDays.add(key); });
        if (completionRepair) dirtyCompletion = true;
      }
    }

    const current = memoryDocument;
    subscribers.forEach(function (callbacks, dayKey) {
      const ids = (current.days[dayKey] || []).slice();
      const previousIds = (previous.days[dayKey] || []).slice();
      if (JSON.stringify(previousIds) === JSON.stringify(ids)) return;
      callbacks.forEach(function (callback) {
        try {
          callback(ids.slice(), previousIds.slice());
        } catch (error) {
          // One page listener must not block other subscribers.
        }
      });
    });

    const completedIds = current.completedDays.slice();
    const previousCompletedIds = previous.completedDays.slice();
    if (JSON.stringify(previousCompletedIds) !== JSON.stringify(completedIds)) {
      completionSubscribers.forEach(function (callback) {
        try {
          callback(completedIds.slice(), previousCompletedIds.slice());
        } catch (error) {
          // One completion listener must not block the others.
        }
      });
    }
  });

  window.CourseProgressStore = {
    getReadIds: getReadIds,
    initializeDay: initializeDay,
    setRead: setRead,
    setDayReadIds: setDayReadIds,
    resetDay: resetDay,
    subscribe: subscribe,
    bindPage: bindPage,
    getCompletedDays: getCompletedDays,
    initializeCompletedDays: initializeCompletedDays,
    setDayCompleted: setDayCompleted,
    setCompletedDays: setCompletedDays,
    resetCompletedDays: resetCompletedDays,
    subscribeCompleted: subscribeCompleted
  };
})(window);
