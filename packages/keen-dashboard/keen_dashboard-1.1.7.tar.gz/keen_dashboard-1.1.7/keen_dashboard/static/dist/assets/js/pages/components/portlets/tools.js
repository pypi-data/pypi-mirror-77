/******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, { enumerable: true, get: getter });
/******/ 		}
/******/ 	};
/******/
/******/ 	// define __esModule on exports
/******/ 	__webpack_require__.r = function(exports) {
/******/ 		if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 			Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 		}
/******/ 		Object.defineProperty(exports, '__esModule', { value: true });
/******/ 	};
/******/
/******/ 	// create a fake namespace object
/******/ 	// mode & 1: value is a module id, require it
/******/ 	// mode & 2: merge all properties of value into the ns
/******/ 	// mode & 4: return value when already ns object
/******/ 	// mode & 8|1: behave like require
/******/ 	__webpack_require__.t = function(value, mode) {
/******/ 		if(mode & 1) value = __webpack_require__(value);
/******/ 		if(mode & 8) return value;
/******/ 		if((mode & 4) && typeof value === 'object' && value && value.__esModule) return value;
/******/ 		var ns = Object.create(null);
/******/ 		__webpack_require__.r(ns);
/******/ 		Object.defineProperty(ns, 'default', { enumerable: true, value: value });
/******/ 		if(mode & 2 && typeof value != 'string') for(var key in value) __webpack_require__.d(ns, key, function(key) { return value[key]; }.bind(null, key));
/******/ 		return ns;
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = "../src/assets/js/pages/components/portlets/tools.js");
/******/ })
/************************************************************************/
/******/ ({

/***/ "../src/assets/js/pages/components/portlets/tools.js":
/*!***********************************************************!*\
  !*** ../src/assets/js/pages/components/portlets/tools.js ***!
  \***********************************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

"use strict";
eval("\r\nvar KTPortletTools = function () {\r\n    // Toastr\r\n    var initToastr = function() {\r\n        toastr.options.showDuration = 1000;\r\n    }\r\n\r\n    // Demo 1\r\n    var demo1 = function() {\r\n        // This portlet is lazy initialized using data-portlet=\"true\" attribute. You can access to the portlet object as shown below and override its behavior\r\n        var portlet = new KTPortlet('kt_portlet_tools_1', {\r\n            tools: {\r\n                toggle: {\r\n                    collapse: 'Collapse me',\r\n                    expand: 'Expand me'\r\n                },\r\n                reload: 'Reload me',\r\n                remove: 'Remove me'\r\n            }\r\n        });\r\n\r\n        // Toggle event handlers\r\n        portlet.on('beforeCollapse', function(portlet) {\r\n            setTimeout(function() {\r\n                toastr.info('Before collapse event fired!');\r\n            }, 100);\r\n        });\r\n\r\n        portlet.on('afterCollapse', function(portlet) {\r\n            setTimeout(function() {\r\n                toastr.warning('Before collapse event fired!');\r\n            }, 2000);            \r\n        });\r\n\r\n        portlet.on('beforeExpand', function(portlet) {\r\n            setTimeout(function() {\r\n                toastr.info('Before expand event fired!');\r\n            }, 100);  \r\n        });\r\n\r\n        portlet.on('afterExpand', function(portlet) {\r\n            setTimeout(function() {\r\n                toastr.warning('After expand event fired!');\r\n            }, 2000);\r\n        });\r\n\r\n        // Remove event handlers\r\n        portlet.on('beforeRemove', function(portlet) {\r\n            toastr.info('Before remove event fired!');\r\n\r\n            return confirm('Are you sure to remove this portlet ?');  // remove portlet after user confirmation\r\n        });\r\n\r\n        portlet.on('afterRemove', function(portlet) {\r\n            setTimeout(function() {\r\n                toastr.warning('After remove event fired!');\r\n            }, 2000);            \r\n        });\r\n\r\n        // Reload event handlers\r\n        portlet.on('reload', function(portlet) {\r\n            toastr.info('Reload event fired!');\r\n\r\n            KTApp.block(portlet.getSelf(), {\r\n                overlayColor: '#ffffff',\r\n                type: 'loader',\r\n                state: 'brand',\r\n                opacity: 0.3,\r\n                size: 'lg'\r\n            });\r\n\r\n            // update the content here\r\n\r\n            setTimeout(function() {\r\n                KTApp.unblock(portlet.getSelf());\r\n            }, 2000);\r\n        });\r\n    }\r\n\r\n    // Demo 2\r\n    var demo2 = function() {\r\n        // This portlet is lazy initialized using data-portlet=\"true\" attribute. You can access to the portlet object as shown below and override its behavior\r\n        var portlet = new KTPortlet('kt_portlet_tools_2');\r\n\r\n        // Toggle event handlers\r\n        portlet.on('beforeCollapse', function(portlet) {\r\n            setTimeout(function() {\r\n                toastr.info('Before collapse event fired!');\r\n            }, 100);\r\n        });\r\n\r\n        portlet.on('afterCollapse', function(portlet) {\r\n            setTimeout(function() {\r\n                toastr.warning('Before collapse event fired!');\r\n            }, 2000);            \r\n        });\r\n\r\n        portlet.on('beforeExpand', function(portlet) {\r\n            setTimeout(function() {\r\n                toastr.info('Before expand event fired!');\r\n            }, 100);  \r\n        });\r\n\r\n        portlet.on('afterExpand', function(portlet) {\r\n            setTimeout(function() {\r\n                toastr.warning('After expand event fired!');\r\n            }, 2000);\r\n        });\r\n\r\n        // Remove event handlers\r\n        portlet.on('beforeRemove', function(portlet) {\r\n            toastr.info('Before remove event fired!');\r\n\r\n            return confirm('Are you sure to remove this portlet ?');  // remove portlet after user confirmation\r\n        });\r\n\r\n        portlet.on('afterRemove', function(portlet) {\r\n            setTimeout(function() {\r\n                toastr.warning('After remove event fired!');\r\n            }, 2000);            \r\n        });\r\n\r\n        // Reload event handlers\r\n        portlet.on('reload', function(portlet) {\r\n            toastr.info('Reload event fired!');\r\n\r\n            KTApp.block(portlet.getSelf(), {\r\n                overlayColor: '#000000',\r\n                type: 'spinner',\r\n                state: 'brand',\r\n                opacity: 0.05,\r\n                size: 'lg'\r\n            });\r\n\r\n            // update the content here\r\n\r\n            setTimeout(function() {\r\n                KTApp.unblock(portlet.getSelf());\r\n            }, 2000);\r\n        });\r\n    }\r\n\r\n    // Demo 3\r\n    var demo3 = function() {\r\n        // This portlet is lazy initialized using data-portlet=\"true\" attribute. You can access to the portlet object as shown below and override its behavior\r\n        var portlet = new KTPortlet('kt_portlet_tools_3');\r\n\r\n        // Toggle event handlers\r\n        portlet.on('beforeCollapse', function(portlet) {\r\n            setTimeout(function() {\r\n                toastr.info('Before collapse event fired!');\r\n            }, 100);\r\n        });\r\n\r\n        portlet.on('afterCollapse', function(portlet) {\r\n            setTimeout(function() {\r\n                toastr.warning('Before collapse event fired!');\r\n            }, 2000);            \r\n        });\r\n\r\n        portlet.on('beforeExpand', function(portlet) {\r\n            setTimeout(function() {\r\n                toastr.info('Before expand event fired!');\r\n            }, 100);  \r\n        });\r\n\r\n        portlet.on('afterExpand', function(portlet) {\r\n            setTimeout(function() {\r\n                toastr.warning('After expand event fired!');\r\n            }, 2000);\r\n        });\r\n\r\n        // Remove event handlers\r\n        portlet.on('beforeRemove', function(portlet) {\r\n            toastr.info('Before remove event fired!');\r\n\r\n            return confirm('Are you sure to remove this portlet ?');  // remove portlet after user confirmation\r\n        });\r\n\r\n        portlet.on('afterRemove', function(portlet) {\r\n            setTimeout(function() {\r\n                toastr.warning('After remove event fired!');\r\n            }, 2000);            \r\n        });\r\n\r\n        // Reload event handlers\r\n        portlet.on('reload', function(portlet) {\r\n            toastr.info('Reload event fired!');\r\n\r\n            KTApp.block(portlet.getSelf(), {\r\n                type: 'loader',\r\n                state: 'success',\r\n                message: 'Please wait...'\r\n            });\r\n\r\n            // update the content here\r\n\r\n            setTimeout(function() {\r\n                KTApp.unblock(portlet.getSelf());\r\n            }, 2000);\r\n        });\r\n    }\r\n \r\n    // Demo 4\r\n    var demo4 = function() {\r\n        // This portlet is lazy initialized using data-portlet=\"true\" attribute. You can access to the portlet object as shown below and override its behavior\r\n        var portlet = new KTPortlet('kt_portlet_tools_4');\r\n\r\n        // Toggle event handlers\r\n        portlet.on('beforeCollapse', function(portlet) {\r\n            setTimeout(function() {\r\n                toastr.info('Before collapse event fired!');\r\n            }, 100);\r\n        });\r\n\r\n        portlet.on('afterCollapse', function(portlet) {\r\n            setTimeout(function() {\r\n                toastr.warning('Before collapse event fired!');\r\n            }, 2000);            \r\n        });\r\n\r\n        portlet.on('beforeExpand', function(portlet) {\r\n            setTimeout(function() {\r\n                toastr.info('Before expand event fired!');\r\n            }, 100);  \r\n        });\r\n\r\n        portlet.on('afterExpand', function(portlet) {\r\n            setTimeout(function() {\r\n                toastr.warning('After expand event fired!');\r\n            }, 2000);\r\n        });\r\n\r\n        // Remove event handlers\r\n        portlet.on('beforeRemove', function(portlet) {\r\n            toastr.info('Before remove event fired!');\r\n\r\n            return confirm('Are you sure to remove this portlet ?');  // remove portlet after user confirmation\r\n        });\r\n\r\n        portlet.on('afterRemove', function(portlet) {\r\n            setTimeout(function() {\r\n                toastr.warning('After remove event fired!');\r\n            }, 2000);            \r\n        });\r\n\r\n        // Reload event handlers\r\n        portlet.on('reload', function(portlet) {\r\n            toastr.info('Reload event fired!');\r\n\r\n            KTApp.block(portlet.getSelf(), {\r\n                type: 'loader',\r\n                state: 'brand',\r\n                message: 'Please wait...'\r\n            });\r\n\r\n            // update the content here\r\n\r\n            setTimeout(function() {\r\n                KTApp.unblock(portlet.getSelf());\r\n            }, 2000);\r\n        });\r\n    }\r\n\r\n    // Demo 5\r\n    var demo5 = function() {\r\n        // This portlet is lazy initialized using data-portlet=\"true\" attribute. You can access to the portlet object as shown below and override its behavior\r\n        var portlet = new KTPortlet('kt_portlet_tools_5');\r\n\r\n        // Toggle event handlers\r\n        portlet.on('beforeCollapse', function(portlet) {\r\n            setTimeout(function() {\r\n                toastr.info('Before collapse event fired!');\r\n            }, 100);\r\n        });\r\n\r\n        portlet.on('afterCollapse', function(portlet) {\r\n            setTimeout(function() {\r\n                toastr.warning('Before collapse event fired!');\r\n            }, 2000);            \r\n        });\r\n\r\n        portlet.on('beforeExpand', function(portlet) {\r\n            setTimeout(function() {\r\n                toastr.info('Before expand event fired!');\r\n            }, 100);  \r\n        });\r\n\r\n        portlet.on('afterExpand', function(portlet) {\r\n            setTimeout(function() {\r\n                toastr.warning('After expand event fired!');\r\n            }, 2000);\r\n        });\r\n\r\n        // Remove event handlers\r\n        portlet.on('beforeRemove', function(portlet) {\r\n            toastr.info('Before remove event fired!');\r\n\r\n            return confirm('Are you sure to remove this portlet ?');  // remove portlet after user confirmation\r\n        });\r\n\r\n        portlet.on('afterRemove', function(portlet) {\r\n            setTimeout(function() {\r\n                toastr.warning('After remove event fired!');\r\n            }, 2000);            \r\n        });\r\n\r\n        // Reload event handlers\r\n        portlet.on('reload', function(portlet) {\r\n            toastr.info('Reload event fired!');\r\n\r\n            KTApp.block(portlet.getSelf(), {\r\n                type: 'loader',\r\n                state: 'brand',\r\n                message: 'Please wait...'\r\n            });\r\n\r\n            // update the content here\r\n\r\n            setTimeout(function() {\r\n                KTApp.unblock(portlet.getSelf());\r\n            }, 2000);\r\n        });\r\n\r\n        // Reload event handlers\r\n        portlet.on('afterFullscreenOn', function(portlet) {\r\n            toastr.info('After fullscreen on event fired!');\r\n        });\r\n\r\n        portlet.on('afterFullscreenOff', function(portlet) {\r\n            toastr.warning('After fullscreen off event fired!');\r\n        });\r\n    }\r\n\r\n    // Demo 6\r\n    var demo6 = function() {\r\n        // This portlet is lazy initialized using data-portlet=\"true\" attribute. You can access to the portlet object as shown below and override its behavior\r\n        var portlet = new KTPortlet('kt_portlet_tools_6');\r\n\r\n        // Toggle event handlers\r\n        portlet.on('beforeCollapse', function(portlet) {\r\n            setTimeout(function() {\r\n                toastr.info('Before collapse event fired!');\r\n            }, 100);\r\n        });\r\n\r\n        portlet.on('afterCollapse', function(portlet) {\r\n            setTimeout(function() {\r\n                toastr.warning('Before collapse event fired!');\r\n            }, 2000);            \r\n        });\r\n\r\n        portlet.on('beforeExpand', function(portlet) {\r\n            setTimeout(function() {\r\n                toastr.info('Before expand event fired!');\r\n            }, 100);  \r\n        });\r\n\r\n        portlet.on('afterExpand', function(portlet) {\r\n            setTimeout(function() {\r\n                toastr.warning('After expand event fired!');\r\n            }, 2000);\r\n        });\r\n\r\n        // Remove event handlers\r\n        portlet.on('beforeRemove', function(portlet) {\r\n            toastr.info('Before remove event fired!');\r\n\r\n            return confirm('Are you sure to remove this portlet ?');  // remove portlet after user confirmation\r\n        });\r\n\r\n        portlet.on('afterRemove', function(portlet) {\r\n            setTimeout(function() {\r\n                toastr.warning('After remove event fired!');\r\n            }, 2000);            \r\n        });\r\n\r\n        // Reload event handlers\r\n        portlet.on('reload', function(portlet) {\r\n            toastr.info('Reload event fired!');\r\n\r\n            KTApp.block(portlet.getSelf(), {\r\n                type: 'loader',\r\n                state: 'brand',\r\n                message: 'Please wait...'\r\n            });\r\n\r\n            // update the content here\r\n\r\n            setTimeout(function() {\r\n                KTApp.unblock(portlet.getSelf());\r\n            }, 2000);\r\n        });\r\n\r\n        // Reload event handlers\r\n        portlet.on('afterFullscreenOn', function(portlet) {\r\n            toastr.info('After fullscreen on event fired!');\r\n        });\r\n\r\n        portlet.on('afterFullscreenOff', function(portlet) {\r\n            toastr.warning('After fullscreen off event fired!');\r\n        });\r\n    }\r\n\r\n    return {\r\n        //main function to initiate the module\r\n        init: function () {\r\n            initToastr();\r\n\r\n            // init demos\r\n            demo1();\r\n            demo2();\r\n            demo3();\r\n            demo4();\r\n            demo5();\r\n            demo6();\r\n        }\r\n    };\r\n}();\r\n\r\njQuery(document).ready(function() {\r\n    KTPortletTools.init();\r\n});\n\n//# sourceURL=webpack:///../src/assets/js/pages/components/portlets/tools.js?");

/***/ })

/******/ });