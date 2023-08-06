(self.webpackJsonp=self.webpackJsonp||[]).push([[55],{146:function(e,t,r){"use strict";r(150);var i=r(0);r(132);const o=window;"customIconsets"in o||(o.customIconsets={});const n=o.customIconsets;const a=r(153);var s=r(109);const l=new s.a("hass-icon-db","mdi-icon-store"),c=["mdi","hass","hassio","hademo"];let d=[];var f=r(83),u=r(12);function p(e){var t,r=y(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function h(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function m(e){return e.decorators&&e.decorators.length}function b(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function v(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function y(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function g(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}const x={"account-badge":"badge-account","account-badge-alert":"badge-account-alert","account-badge-alert-outline":"badge-account-alert-outline","account-badge-horizontal":"badge-account-horizontal","account-badge-horizontal-outline":"badge-account-horizontal-outline","account-badge-outline":"badge-account-outline","account-card-details":"card-account-details","account-card-details-outline":"card-account-details-outline",airplay:"apple-airplay",artist:"account-music","artist-outline":"account-music-outline",audiobook:"book-music",azure:"microsoft-azure","azure-devops":"microsoft-azure-devops",bible:"book-cross",bowl:"bowl-mix","calendar-repeat":"calendar-sync","calendar-repeat-outline":"calendar-sync-outline","camcorder-box":"video-box","camcorder-box-off":"video-box-off","cellphone-settings-variant":"cellphone-cog","chart-snakey":"chart-sankey","chart-snakey-variant":"chart-sankey-variant",coin:"currency-usd-circle","coin-outline":"currency-usd-circle-outline","coins-outline":"circle-multiple-outline","contact-mail":"card-account-mail","contact-mail-outline":"card-account-mail-outline","contact-phone":"card-account-phone","contact-phone-outline":"card-account-phone-outline",cowboy:"account-cowboy-hat","database-refresh":"database-sync",dictionary:"book-alphabet",edge:"microsoft-edge","edge-legacy":"microsoft-edge-legacy","file-document-box":"text-box","file-document-box-check-outline":"text-box-check-outline","file-document-box-minus":"text-box-minus","file-document-box-minus-outline":"text-box-minus-outline","file-document-box-multiple":"text-box-multiple","file-document-box-multiple-outline":"text-box-multiple-outline","file-document-box-outline":"text-box-outline","file-document-box-plus":"text-box-plus","file-document-box-plus-outline":"text-box-plus-outline","file-document-box-remove":"text-box-remove","file-document-box-remove-outline":"text-box-remove-outline","file-document-box-search":"text-box-search","file-document-box-search-outline":"text-box-search-outline","file-settings-variant":"file-cog","file-settings-variant-outline":"file-cog-outline","folder-settings-variant":"folder-cog","folder-settings-variant-outline":"folder-cog-outline","github-circle":"github","google-adwords":"google-ads",hackernews:"y-combinator",hotel:"bed","image-filter":"image-multiple-outline","internet-explorer":"microsoft-internet-explorer",json:"code-json",kotlin:"language-kotlin","library-books":"filmstrip-box","library-movie":"filmstrip-box-multiple","library-music":"music-box-multiple","library-music-outline":"music-box-multiple-outline","library-video":"play-box-multiple",markdown:"language-markdown","markdown-outline":"language-markdown-outline","message-settings-variant":"message-cog","message-settings-variant-outline":"message-cog-outline","microsoft-dynamics":"microsoft-dynamics-365","network-router":"router-network",office:"microsoft-office",onedrive:"microsoft-onedrive",onenote:"microsoft-onenote",outlook:"microsoft-outlook",playstation:"sony-playstation","periodic-table-co":"molecule-co","periodic-table-co2":"molecule-co2",pot:"pot-steam",ruby:"language-ruby",sailing:"sail-boat",scooter:"human-scooter",settings:"cog","settings-box":"cog-box","settings-outline":"cog-outline","settings-transfer":"cog-transfer","settings-transfer-outline":"cog-transfer-outline","shield-refresh":"shield-sync","shield-refresh-outline":"shield-sync-outline","sort-alphabetical":"sort-alphabetical-variant","sort-alphabetical-ascending":"sort-alphabetical-ascending-variant","sort-alphabetical-descending":"sort-alphabetical-descending-variant","sort-numeric":"sort-numeric-variant","star-half":"star-half-full",storefront:"storefront-outline",timer:"timer-outline","timer-off":"timer-off-outline",towing:"tow-truck",voice:"account-voice","wall-sconce-variant":"wall-sconce-round-variant",wii:"nintendo-wii",wiiu:"nintendo-wiiu",windows:"microsoft-windows","windows-classic":"microsoft-windows-classic",worker:"account-hard-hat",xbox:"microsoft-xbox","xbox-controller":"microsoft-xbox-controller","xbox-controller-battery-alert":"microsoft-xbox-controller-battery-alert","xbox-controller-battery-charging":"microsoft-xbox-controller-battery-charging","xbox-controller-battery-empty":"microsoft-xbox-controller-battery-empty","xbox-controller-battery-full":"microsoft-xbox-controller-battery-full","xbox-controller-battery-low":"microsoft-xbox-controller-battery-low","xbox-controller-battery-medium":"microsoft-xbox-controller-battery-medium","xbox-controller-battery-unknown":"microsoft-xbox-controller-battery-unknown","xbox-controller-menu":"microsoft-xbox-controller-menu","xbox-controller-off":"microsoft-xbox-controller-off","xbox-controller-view":"microsoft-xbox-controller-view",yammer:"microsoft-yammer","youtube-creator-studio":"youtube-studio","selection-mutliple":"selection-multiple",textarea:"form-textarea",textbox:"form-textbox","textbox-lock":"form-textbox-lock","textbox-password":"form-textbox-password","syllabary-katakana-half-width":"syllabary-katakana-halfwidth","visual-studio-code":"microsoft-visual-studio-code","visual-studio":"microsoft-visual-studio"},w=new Set(["accusoft","amazon-drive","android-head","basecamp","beats","behance","blackberry","cisco-webex","disqus-outline","dribbble","dribbble-box","etsy","eventbrite","facebook-box","flattr","flickr","foursquare","github-box","github-face","glassdoor","google-adwords","google-pages","google-physical-web","google-plus-box","houzz","houzz-box","instapaper","itunes","language-python-text","lastfm","linkedin-box","lyft","mail-ru","mastodon-variant","medium","meetup","mixcloud","mixer","nfc-off","npm-variant","npm-variant-outline","paypal","periscope","pinterest-box","pocket","quicktime","shopify","slackware","square-inc","square-inc-cash","steam-box","strava","tor","tumblr","tumblr-box","tumblr-reblog","twitter-box","twitter-circle","uber","venmo","vk-box","vk-circle","wunderlist","xda","xing-box","xing-circle","yelp"]),k={};Object(s.c)("_version",l).then(e=>{e?e!==a.version&&Object(s.b)(l).then(()=>Object(s.d)("_version",a.version,l)):Object(s.d)("_version",a.version,l)});const E=Object(f.a)(()=>(async e=>{const t=Object.keys(e),r=await Promise.all(Object.values(e));l._withIDBStore("readwrite",i=>{r.forEach((r,o)=>{Object.entries(r).forEach(([e,t])=>{i.put(t,e)}),delete e[t[o]]})})})(k),2e3),_={};!function(e,t,r,i){var o=function(){(function(){return e});var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var o=t.placement;if(t.kind===i&&("static"===o||"prototype"===o)){var n="static"===o?e:r;this.defineClassElement(n,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],o={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,o)}),this),e.forEach((function(e){if(!m(e))return r.push(e);var t=this.decorateElement(e,o);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var n=this.decorateConstructor(r,t);return i.push.apply(i,n.finishers),n.finishers=i,n},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],o=e.decorators,n=o.length-1;n>=0;n--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var s=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,o[n])(s)||s);e=l.element,this.addElementPlacement(e,t),l.finisher&&i.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);r.push.apply(r,c)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var o=this.fromClassDescriptor(e),n=this.toClassDescriptor((0,t[i])(o)||o);if(void 0!==n.finisher&&r.push(n.finisher),void 0!==n.elements){e=n.elements;for(var a=0;a<e.length-1;a++)for(var s=a+1;s<e.length;s++)if(e[a].key===e[s].key&&e[a].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return g(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(r):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?g(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=y(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var o=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var n={kind:t,key:r,placement:i,descriptor:Object.assign({},o)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(o,"get","The property descriptor of a field descriptor"),this.disallowProperty(o,"set","The property descriptor of a field descriptor"),this.disallowProperty(o,"value","The property descriptor of a field descriptor"),n.initializer=e.initializer),n},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:v(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=v(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}();if(i)for(var n=0;n<i.length;n++)o=i[n](o);var a=t((function(e){o.initializeInstanceElements(e,s.elements)}),r),s=o.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===n.key&&e.placement===n.placement},i=0;i<e.length;i++){var o,n=e[i];if("method"===n.kind&&(o=t.find(r)))if(b(n.descriptor)||b(o.descriptor)){if(m(n)||m(o))throw new ReferenceError("Duplicated methods ("+n.key+") can't be decorated.");o.descriptor=n.descriptor}else{if(m(n)){if(m(o))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+n.key+").");o.decorators=n.decorators}h(n,o)}else t.push(n)}return t}(a.d.map(p)),e);o.initializeClassElements(a.F,s.elements),o.runClassFinishers(a.F,s.finishers)}([Object(i.d)("ha-icon")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[Object(i.h)()],key:"icon",value:void 0},{kind:"field",decorators:[Object(i.g)()],key:"_path",value:void 0},{kind:"field",decorators:[Object(i.g)()],key:"_viewBox",value:void 0},{kind:"field",decorators:[Object(i.g)()],key:"_legacy",value:()=>!1},{kind:"method",key:"updated",value:function(e){e.has("icon")&&(this._path=void 0,this._viewBox=void 0,this._loadIcon())}},{kind:"method",key:"render",value:function(){return this.icon?this._legacy?i.f`<iron-icon .icon=${this.icon}></iron-icon>`:i.f`<ha-svg-icon
      .path=${this._path}
      .viewBox=${this._viewBox}
    ></ha-svg-icon>`:i.f``}},{kind:"method",key:"_loadIcon",value:async function(){if(!this.icon)return;const[e,t]=this.icon.split(":",2);let r,i=t;if(!e||!i)return;if(!c.includes(e)){if(e in n){const t=n[e];return void(t&&this._setCustomPath(t(i)))}return void(this._legacy=!0)}if(this._legacy=!1,i in x){i=x[i];const r=`Icon ${e}:${t} was renamed to ${e}:${i}, please change your config, it will be removed in version 0.115.`;console.warn(r),Object(u.a)(this,"write_log",{level:"warning",message:r})}else if(w.has(i)){const e=`Icon ${this.icon} was removed from MDI, please replace this icon with an other icon in your config, it will be removed in version 0.115.`;console.warn(e),Object(u.a)(this,"write_log",{level:"warning",message:e})}if(i in _)return void(this._path=_[i]);try{r=await(e=>new Promise((t,r)=>{if(d.push([e,t,r]),d.length>1)return;const i=[];l._withIDBStore("readonly",e=>{for(const[t,r]of d)i.push([r,e.get(t)]);d=[]}).then(()=>{for(const[e,t]of i)e(t.result)}).catch(()=>{for(const[,,e]of d)e();d=[]})}))(i)}catch(f){r=void 0}if(r)return this._path=r,void(_[i]=r);const o=(e=>{let t;for(const r of a.parts){if(void 0!==r.start&&e<r.start)break;t=r}return t.file})(i);if(o in k)return void this._setPath(k[o],i);const s=fetch(`/static/mdi/${o}.json`).then(e=>e.json());k[o]=s,this._setPath(s,i),E()}},{kind:"method",key:"_setCustomPath",value:async function(e){const t=await e;this._path=t.path,this._viewBox=t.viewBox}},{kind:"method",key:"_setPath",value:async function(e,t){const r=await e;this._path=r[t],_[t]=r[t]}},{kind:"get",static:!0,key:"styles",value:function(){return i.c`
      :host {
        fill: currentcolor;
      }
    `}}]}}),i.a)},153:function(e){e.exports=JSON.parse('{"version":"5.5.55","parts":[{"file":"c1dd3462813e8d8512ba45803042e98369616a5e"},{"start":"airbal","file":"749ed78140e2237d9e2455225d451d00d41933e6"},{"start":"apple-k","file":"6acf0043f606a971bfb59bba0e34f7037ad5bbc1"},{"start":"bad","file":"64e2f4e764d953d275d7991c48be40c56e4781f6"},{"start":"beehive-ou","file":"99f432e85e26dfee84de7049a9eee41c5e177652"},{"start":"border-h","file":"b6066832b5556a1309f58536a05e8b56227ab4cc"},{"start":"call","file":"912ecc5695dc33ab61100974db038a0c16632aee"},{"start":"cart-p","file":"799324f7e8568d2025521a1364843c0e9f8feb84"},{"start":"circle-slice-6","file":"8f966a9c09f590d5f9c6df8a5d53d25ff769f07e"},{"start":"cog-r","file":"8165badf07b2b247ce8774f088ae4277e889b93d"},{"start":"credit-card-mi","file":"d72f7d4365b34e8bbe330761405a3dfbd607b75a"},{"start":"dice-4","file":"2978b6ec593ca5da6d6f0d790f053e5f48f3906f"},{"start":"eig","file":"8af55ece617335b75e44b83f39e950bbd5c54b5d"},{"start":"expor","file":"bb4e34f5495c13f22e56fcc28c3e2e597a0ca3a8"},{"start":"file-pdf-o","file":"15f15fad384051346e60bcfe65c6677d1ab33545"},{"start":"focus-f","file":"0e759d4469a94835f7dbe910f59de9463b6a499b"},{"start":"fountain-","file":"9bdab66dff04b412cfaf3d7b72b420ecfd4b6dfa"},{"start":"gol","file":"828f59340487c4e899811da074cba26830820857"},{"start":"head-d","file":"b1a9bd3fa1e9e750ccd24134627f45e76b1ad768"},{"start":"human-male-g","file":"1f312f9c85fcc1581c8a67eed7a23c967902b763"},{"start":"key-r","file":"9b738eee0c9422c6e4dc0784e61cad45558a8193"},{"start":"lightbulb-group-ou","file":"e32d53ac0efc3008e44743c17092316173676e6a"},{"start":"math-i","file":"fcc6644198de39298dd2804f2a92a3d36ca7bfd0"},{"start":"mix","file":"7e63570dd4b5bcd07f7d90ea9f4a87fdf5b648e4"},{"start":"numeric-10-","file":"5d5a8bcc06920b1a0a9ca524cce1c327393ee2d0"},{"start":"pau","file":"f77ffde7f602c4003b0dbd6af0e678d0da71fac5"},{"start":"piston","file":"730c52a8acb328f671c385a9e0e89f797a18cf33"},{"start":"r","file":"e8ff41bf26d601cc4a563f65289a4c607e8c825c"},{"start":"router-w","file":"8c9bc4cba19910e21fdb3ddf1ce63e82f3bdc84c"},{"start":"shi","file":"681b25c220015aeee97beb54c23558dd835b3212"},{"start":"sno","file":"bd91dc8650163f091ae856161c9401a31ec86b93"},{"start":"star-off-","file":"5646fa1edff0598193aab25c4b9fda27532e668f"},{"start":"tag-plus-","file":"d9a40be6788c2ede85219a9d39d3d075d0aecf24"},{"start":"tow","file":"ee3a7cd7a2e6aef2f76f6e54c3c63a3832d77bf2"},{"start":"vector-difference-","file":"cc7afa26ce27291e2e626e8745312b920acabf56"},{"start":"weather-haz","file":"181ae9acbe7870f1af338ee1f7d55bb713865ef0"},{"start":"yel","file":"1cf8a6b4fab91b186af6b0e38296c740b549a0e6"}]}')},225:function(e,t,r){"use strict";r.d(t,"b",(function(){return i})),r.d(t,"a",(function(){return o}));const i=(e,t)=>e<t?-1:e>t?1:0,o=(e,t)=>i(e.toLowerCase(),t.toLowerCase())},372:function(e,t,r){"use strict";r.d(t,"a",(function(){return i}));const i=e=>(e.cache.cfg||(e.cache.cfg=e.sendMessage({type:"config/get"})),e.cache.cfg)},490:function(e,t,r){"use strict";var i=r(0),o=r(170);function n(e){var t,r=d(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function a(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function s(e){return e.decorators&&e.decorators.length}function l(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function c(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function d(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function f(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}function u(e,t,r){return(u="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,r){var i=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=p(e)););return e}(e,t);if(i){var o=Object.getOwnPropertyDescriptor(i,t);return o.get?o.get.call(r):o.value}})(e,t,r||e)}function p(e){return(p=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}const h=e=>e?e.trim().split(" ").slice(0,3).map(e=>e.substr(0,1)).join(""):"user";!function(e,t,r,i){var o=function(){(function(){return e});var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var o=t.placement;if(t.kind===i&&("static"===o||"prototype"===o)){var n="static"===o?e:r;this.defineClassElement(n,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],o={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,o)}),this),e.forEach((function(e){if(!s(e))return r.push(e);var t=this.decorateElement(e,o);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var n=this.decorateConstructor(r,t);return i.push.apply(i,n.finishers),n.finishers=i,n},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],o=e.decorators,n=o.length-1;n>=0;n--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var s=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,o[n])(s)||s);e=l.element,this.addElementPlacement(e,t),l.finisher&&i.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);r.push.apply(r,c)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var o=this.fromClassDescriptor(e),n=this.toClassDescriptor((0,t[i])(o)||o);if(void 0!==n.finisher&&r.push(n.finisher),void 0!==n.elements){e=n.elements;for(var a=0;a<e.length-1;a++)for(var s=a+1;s<e.length;s++)if(e[a].key===e[s].key&&e[a].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return f(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(r):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?f(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=d(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var o=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var n={kind:t,key:r,placement:i,descriptor:Object.assign({},o)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(o,"get","The property descriptor of a field descriptor"),this.disallowProperty(o,"set","The property descriptor of a field descriptor"),this.disallowProperty(o,"value","The property descriptor of a field descriptor"),n.initializer=e.initializer),n},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:c(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=c(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}();if(i)for(var u=0;u<i.length;u++)o=i[u](o);var p=t((function(e){o.initializeInstanceElements(e,h.elements)}),r),h=o.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===n.key&&e.placement===n.placement},i=0;i<e.length;i++){var o,n=e[i];if("method"===n.kind&&(o=t.find(r)))if(l(n.descriptor)||l(o.descriptor)){if(s(n)||s(o))throw new ReferenceError("Duplicated methods ("+n.key+") can't be decorated.");o.descriptor=n.descriptor}else{if(s(n)){if(s(o))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+n.key+").");o.decorators=n.decorators}a(n,o)}else t.push(n)}return t}(p.d.map(n)),e);o.initializeClassElements(p.F,h.elements),o.runClassFinishers(p.F,h.finishers)}([Object(i.d)("ha-user-badge")],(function(e,t){class r extends t{constructor(...t){super(...t),e(this)}}return{F:r,d:[{kind:"field",decorators:[Object(i.h)()],key:"user",value:void 0},{kind:"method",key:"render",value:function(){const e=this.user,t=e?h(e.name):"?";return i.f` ${t} `}},{kind:"method",key:"updated",value:function(e){u(p(r.prototype),"updated",this).call(this,e),Object(o.a)(this,"long",(this.user?h(this.user.name):"?").length>2)}},{kind:"get",static:!0,key:"styles",value:function(){return i.c`
      :host {
        display: inline-block;
        box-sizing: border-box;
        width: 40px;
        line-height: 40px;
        border-radius: 50%;
        text-align: center;
        background-color: var(--light-primary-color);
        text-decoration: none;
        color: var(--text-light-primary-color, var(--primary-text-color));
        overflow: hidden;
      }

      :host([long]) {
        font-size: 80%;
      }
    `}}]}}),i.a)},783:function(e,t,r){"use strict";r.r(t);r(134);var i=r(108),o=(r(178),r(147),r(136),r(0)),n=r(48),a=r(12),s=r(149),l=r(225),c=r(117),d=r(69),f=r(171),u=r(372);r(146),r(158),r(132),r(490);function p(e){var t,r=y(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function h(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function m(e){return e.decorators&&e.decorators.length}function b(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function v(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function y(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function g(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}function x(e,t,r){return(x="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,r){var i=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=w(e)););return e}(e,t);if(i){var o=Object.getOwnPropertyDescriptor(i,t);return o.get?o.get.call(r):o.value}})(e,t,r||e)}function w(e){return(w=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}const k=["config","developer-tools","hassio"],E="scrollIntoViewIfNeeded"in document.body,_={map:1,logbook:2,history:3,"developer-tools":9,hassio:10,config:11},O=(e,t)=>{const r="lovelace"===e.component_name,i="lovelace"===t.component_name;if(r&&i)return Object(l.b)(e.title,t.title);if(r&&!i)return-1;if(i)return 1;const o=e.url_path in _,n=t.url_path in _;return o&&n?_[e.url_path]-_[t.url_path]:o?-1:n?1:Object(l.b)(e.title,t.title)};!function(e,t,r,i){var o=function(){(function(){return e});var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var o=t.placement;if(t.kind===i&&("static"===o||"prototype"===o)){var n="static"===o?e:r;this.defineClassElement(n,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],o={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,o)}),this),e.forEach((function(e){if(!m(e))return r.push(e);var t=this.decorateElement(e,o);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var n=this.decorateConstructor(r,t);return i.push.apply(i,n.finishers),n.finishers=i,n},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],o=e.decorators,n=o.length-1;n>=0;n--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var s=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,o[n])(s)||s);e=l.element,this.addElementPlacement(e,t),l.finisher&&i.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);r.push.apply(r,c)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var o=this.fromClassDescriptor(e),n=this.toClassDescriptor((0,t[i])(o)||o);if(void 0!==n.finisher&&r.push(n.finisher),void 0!==n.elements){e=n.elements;for(var a=0;a<e.length-1;a++)for(var s=a+1;s<e.length;s++)if(e[a].key===e[s].key&&e[a].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return g(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(r):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?g(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=y(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var o=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var n={kind:t,key:r,placement:i,descriptor:Object.assign({},o)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(o,"get","The property descriptor of a field descriptor"),this.disallowProperty(o,"set","The property descriptor of a field descriptor"),this.disallowProperty(o,"value","The property descriptor of a field descriptor"),n.initializer=e.initializer),n},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:v(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=v(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}();if(i)for(var n=0;n<i.length;n++)o=i[n](o);var a=t((function(e){o.initializeInstanceElements(e,s.elements)}),r),s=o.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===n.key&&e.placement===n.placement},i=0;i<e.length;i++){var o,n=e[i];if("method"===n.kind&&(o=t.find(r)))if(b(n.descriptor)||b(o.descriptor)){if(m(n)||m(o))throw new ReferenceError("Duplicated methods ("+n.key+") can't be decorated.");o.descriptor=n.descriptor}else{if(m(n)){if(m(o))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+n.key+").");o.decorators=n.decorators}h(n,o)}else t.push(n)}return t}(a.d.map(p)),e);o.initializeClassElements(a.F,s.elements),o.runClassFinishers(a.F,s.finishers)}([Object(o.d)("ha-sidebar")],(function(e,t){class r extends t{constructor(...t){super(...t),e(this)}}return{F:r,d:[{kind:"field",decorators:[Object(o.h)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[Object(o.h)()],key:"narrow",value:void 0},{kind:"field",decorators:[Object(o.h)({type:Boolean})],key:"alwaysExpand",value:()=>!1},{kind:"field",decorators:[Object(o.h)({type:Boolean,reflect:!0})],key:"expanded",value:()=>!1},{kind:"field",decorators:[Object(o.g)()],key:"_externalConfig",value:void 0},{kind:"field",decorators:[Object(o.g)()],key:"_notifications",value:void 0},{kind:"field",decorators:[Object(o.h)({type:Boolean,reflect:!0})],key:"rtl",value:()=>!1},{kind:"field",key:"_mouseLeaveTimeout",value:void 0},{kind:"field",key:"_tooltipHideTimeout",value:void 0},{kind:"field",key:"_recentKeydownActiveUntil",value:()=>0},{kind:"method",key:"render",value:function(){const e=this.hass;if(!e)return o.f``;const[t,r]=(e=>{const t=e.panels;if(!t)return[[],[]];const r=[],i=[];return Object.values(t).forEach(t=>{t.title&&t.url_path!==e.defaultPanel&&(k.includes(t.url_path)?i:r).push(t)}),r.sort(O),i.sort(O),[r,i]})(e);let a=this._notifications?this._notifications.length:0;for(const i in e.states)"configurator"===Object(s.a)(i)&&a++;const l=Object(d.b)(e);return o.f`
      <div class="menu">
        ${this.narrow?"":o.f`
              <mwc-icon-button
                .label=${e.localize("ui.sidebar.sidebar_toggle")}
                @click=${this._toggleSidebar}
              >
                <ha-svg-icon
                  .path=${"docked"===e.dockedSidebar?i.I:i.H}
                ></ha-svg-icon>
              </mwc-icon-button>
            `}
        <span class="title">Home Assistant</span>
      </div>
      <paper-listbox
        attr-for-selected="data-panel"
        .selected=${e.panelUrl}
        @focusin=${this._listboxFocusIn}
        @focusout=${this._listboxFocusOut}
        @scroll=${this._listboxScroll}
        @keydown=${this._listboxKeydown}
      >
        ${this._renderPanel(l.url_path,l.title||e.localize("panel.states"),l.icon,l.icon?void 0:i.cb)}
        ${t.map(t=>this._renderPanel(t.url_path,e.localize("panel."+t.title)||t.title,t.icon,void 0))}
        <div class="spacer" disabled></div>

        ${r.map(t=>this._renderPanel(t.url_path,e.localize("panel."+t.title)||t.title,t.icon,void 0))}
        ${this._externalConfig&&this._externalConfig.hasSettingsScreen?o.f`
              <a
                aria-role="option"
                aria-label=${e.localize("ui.sidebar.external_app_configuration")}
                href="#external-app-configuration"
                tabindex="-1"
                @click=${this._handleExternalAppConfiguration}
                @mouseenter=${this._itemMouseEnter}
                @mouseleave=${this._itemMouseLeave}
              >
                <paper-icon-item>
                  <ha-svg-icon
                    slot="item-icon"
                    .path=${i.i}
                  ></ha-svg-icon>
                  <span class="item-text">
                    ${e.localize("ui.sidebar.external_app_configuration")}
                  </span>
                </paper-icon-item>
              </a>
            `:""}
      </paper-listbox>

      <div class="divider"></div>

      <div
        class="notifications-container"
        @mouseenter=${this._itemMouseEnter}
        @mouseleave=${this._itemMouseLeave}
      >
        <paper-icon-item
          class="notifications"
          aria-role="option"
          @click=${this._handleShowNotificationDrawer}
        >
          <ha-svg-icon slot="item-icon" .path=${i.g}></ha-svg-icon>
          ${!this.expanded&&a>0?o.f`
                <span class="notification-badge" slot="item-icon">
                  ${a}
                </span>
              `:""}
          <span class="item-text">
            ${e.localize("ui.notification_drawer.title")}
          </span>
          ${this.expanded&&a>0?o.f`
                <span class="notification-badge">${a}</span>
              `:""}
        </paper-icon-item>
      </div>

      <a
        class=${Object(n.a)({profile:!0,"iron-selected":"profile"===e.panelUrl})}
        href="/profile"
        data-panel="panel"
        tabindex="-1"
        aria-role="option"
        aria-label=${e.localize("panel.profile")}
        @mouseenter=${this._itemMouseEnter}
        @mouseleave=${this._itemMouseLeave}
      >
        <paper-icon-item>
          <ha-user-badge slot="item-icon" .user=${e.user}></ha-user-badge>

          <span class="item-text">
            ${e.user?e.user.name:""}
          </span>
        </paper-icon-item>
      </a>
      <div disabled class="bottom-spacer"></div>
      <div class="tooltip"></div>
    `}},{kind:"method",key:"shouldUpdate",value:function(e){if(e.has("expanded")||e.has("narrow")||e.has("alwaysExpand")||e.has("_externalConfig")||e.has("_notifications"))return!0;if(!this.hass||!e.has("hass"))return!1;const t=e.get("hass");if(!t)return!0;const r=this.hass;return r.panels!==t.panels||r.panelUrl!==t.panelUrl||r.user!==t.user||r.localize!==t.localize||r.language!==t.language||r.states!==t.states||r.defaultPanel!==t.defaultPanel}},{kind:"method",key:"firstUpdated",value:function(e){x(w(r.prototype),"firstUpdated",this).call(this,e),this.hass&&this.hass.auth.external&&Object(u.a)(this.hass.auth.external).then(e=>{this._externalConfig=e}),Object(f.a)(this.hass.connection,e=>{this._notifications=e})}},{kind:"method",key:"updated",value:function(e){if(x(w(r.prototype),"updated",this).call(this,e),e.has("alwaysExpand")&&(this.expanded=this.alwaysExpand),!e.has("hass"))return;const t=e.get("hass");if(t&&t.language===this.hass.language||(this.rtl=Object(c.a)(this.hass)),E&&(!t||t.panelUrl!==this.hass.panelUrl)){const e=this.shadowRoot.querySelector(".iron-selected");e&&e.scrollIntoViewIfNeeded()}}},{kind:"get",key:"_tooltip",value:function(){return this.shadowRoot.querySelector(".tooltip")}},{kind:"method",key:"_itemMouseEnter",value:function(e){this.expanded||(new Date).getTime()<this._recentKeydownActiveUntil||(this._mouseLeaveTimeout&&(clearTimeout(this._mouseLeaveTimeout),this._mouseLeaveTimeout=void 0),this._showTooltip(e.currentTarget))}},{kind:"method",key:"_itemMouseLeave",value:function(){this._mouseLeaveTimeout&&clearTimeout(this._mouseLeaveTimeout),this._mouseLeaveTimeout=window.setTimeout(()=>{this._hideTooltip()},500)}},{kind:"method",key:"_listboxFocusIn",value:function(e){this.expanded||"A"!==e.target.nodeName||this._showTooltip(e.target.querySelector("paper-icon-item"))}},{kind:"method",key:"_listboxFocusOut",value:function(){this._hideTooltip()}},{kind:"method",decorators:[Object(o.e)({passive:!0})],key:"_listboxScroll",value:function(){(new Date).getTime()<this._recentKeydownActiveUntil||this._hideTooltip()}},{kind:"method",key:"_listboxKeydown",value:function(){this._recentKeydownActiveUntil=(new Date).getTime()+100}},{kind:"method",key:"_showTooltip",value:function(e){this._tooltipHideTimeout&&(clearTimeout(this._tooltipHideTimeout),this._tooltipHideTimeout=void 0);const t=this._tooltip,r=this.shadowRoot.querySelector("paper-listbox");let i=e.offsetTop+11;r.contains(e)&&(i-=r.scrollTop),t.innerHTML=e.querySelector(".item-text").innerHTML,t.style.display="block",t.style.top=i+"px",t.style.left=e.offsetLeft+e.clientWidth+4+"px"}},{kind:"method",key:"_hideTooltip",value:function(){this._tooltipHideTimeout||(this._tooltipHideTimeout=window.setTimeout(()=>{this._tooltipHideTimeout=void 0,this._tooltip.style.display="none"},10))}},{kind:"method",key:"_handleShowNotificationDrawer",value:function(){Object(a.a)(this,"hass-show-notifications")}},{kind:"method",key:"_handleExternalAppConfiguration",value:function(e){e.preventDefault(),this.hass.auth.external.fireMessage({type:"config_screen/show"})}},{kind:"method",key:"_toggleSidebar",value:function(){Object(a.a)(this,"hass-toggle-menu")}},{kind:"method",key:"_renderPanel",value:function(e,t,r,i){return o.f`
      <a
        aria-role="option"
        href="${"/"+e}"
        data-panel="${e}"
        tabindex="-1"
        @mouseenter=${this._itemMouseEnter}
        @mouseleave=${this._itemMouseLeave}
      >
        <paper-icon-item>
          ${i?o.f`<ha-svg-icon
                slot="item-icon"
                .path=${i}
              ></ha-svg-icon>`:o.f`<ha-icon slot="item-icon" .icon=${r}></ha-icon>`}
          <span class="item-text">${t}</span>
        </paper-icon-item>
      </a>
    `}},{kind:"get",static:!0,key:"styles",value:function(){return o.c`
      :host {
        height: 100%;
        display: block;
        overflow: hidden;
        -ms-user-select: none;
        -webkit-user-select: none;
        -moz-user-select: none;
        border-right: 1px solid var(--divider-color);
        background-color: var(--sidebar-background-color);
        width: 64px;
      }
      :host([expanded]) {
        width: calc(256px + env(safe-area-inset-left));
      }
      :host([rtl]) {
        border-right: 0;
        border-left: 1px solid var(--divider-color);
      }
      .menu {
        box-sizing: border-box;
        height: 65px;
        display: flex;
        padding: 0 8.5px;
        border-bottom: 1px solid transparent;
        white-space: nowrap;
        font-weight: 400;
        color: var(--primary-text-color);
        border-bottom: 1px solid var(--divider-color);
        background-color: var(--primary-background-color);
        font-size: 20px;
        align-items: center;
        padding-left: calc(8.5px + env(safe-area-inset-left));
      }
      :host([rtl]) .menu {
        padding-left: 8.5px;
        padding-right: calc(8.5px + env(safe-area-inset-right));
      }
      :host([expanded]) .menu {
        width: calc(256px + env(safe-area-inset-left));
      }
      :host([rtl][expanded]) .menu {
        width: calc(256px + env(safe-area-inset-right));
      }
      .menu mwc-icon-button {
        color: var(--sidebar-icon-color);
      }
      :host([expanded]) .menu mwc-icon-button {
        margin-right: 23px;
      }
      :host([expanded][rtl]) .menu mwc-icon-button {
        margin-right: 0px;
        margin-left: 23px;
      }

      .title {
        display: none;
      }
      :host([expanded]) .title {
        display: initial;
      }

      paper-listbox::-webkit-scrollbar {
        width: 0.4rem;
        height: 0.4rem;
      }

      paper-listbox::-webkit-scrollbar-thumb {
        -webkit-border-radius: 4px;
        border-radius: 4px;
        background: var(--scrollbar-thumb-color);
      }

      paper-listbox {
        padding: 4px 0;
        display: flex;
        flex-direction: column;
        box-sizing: border-box;
        height: calc(100% - 196px - env(safe-area-inset-bottom));
        overflow-y: auto;
        overflow-x: hidden;
        scrollbar-color: var(--scrollbar-thumb-color) transparent;
        scrollbar-width: thin;
        background: none;
        margin-left: env(safe-area-inset-left);
      }

      :host([rtl]) paper-listbox {
        margin-left: initial;
        margin-right: env(safe-area-inset-right);
      }

      a {
        text-decoration: none;
        color: var(--sidebar-text-color);
        font-weight: 500;
        font-size: 14px;
        position: relative;
        display: block;
        outline: 0;
      }

      paper-icon-item {
        box-sizing: border-box;
        margin: 4px 8px;
        padding-left: 12px;
        border-radius: 4px;
        --paper-item-min-height: 40px;
        width: 48px;
      }
      :host([expanded]) paper-icon-item {
        width: 240px;
      }
      :host([rtl]) paper-icon-item {
        padding-left: auto;
        padding-right: 12px;
      }

      ha-icon[slot="item-icon"],
      ha-svg-icon[slot="item-icon"] {
        color: var(--sidebar-icon-color);
      }

      .iron-selected paper-icon-item::before,
      a:not(.iron-selected):focus::before {
        border-radius: 4px;
        position: absolute;
        top: 0;
        right: 0;
        bottom: 0;
        left: 0;
        pointer-events: none;
        content: "";
        transition: opacity 15ms linear;
        will-change: opacity;
      }
      .iron-selected paper-icon-item::before {
        background-color: var(--sidebar-selected-icon-color);
        opacity: 0.12;
      }
      a:not(.iron-selected):focus::before {
        background-color: currentColor;
        opacity: var(--dark-divider-opacity);
        margin: 4px 8px;
      }
      .iron-selected paper-icon-item:focus::before,
      .iron-selected:focus paper-icon-item::before {
        opacity: 0.2;
      }

      .iron-selected paper-icon-item[pressed]:before {
        opacity: 0.37;
      }

      paper-icon-item span {
        color: var(--sidebar-text-color);
        font-weight: 500;
        font-size: 14px;
      }

      a.iron-selected paper-icon-item ha-icon,
      a.iron-selected paper-icon-item ha-svg-icon {
        color: var(--sidebar-selected-icon-color);
      }

      a.iron-selected .item-text {
        color: var(--sidebar-selected-text-color);
      }

      paper-icon-item .item-text {
        display: none;
        max-width: calc(100% - 56px);
      }
      :host([expanded]) paper-icon-item .item-text {
        display: block;
      }

      .divider {
        bottom: 112px;
        padding: 10px 0;
      }
      .divider::before {
        content: " ";
        display: block;
        height: 1px;
        background-color: var(--divider-color);
      }
      .notifications-container {
        display: flex;
        margin-left: env(safe-area-inset-left);
      }
      :host([rtl]) .notifications-container {
        margin-left: initial;
        margin-right: env(safe-area-inset-right);
      }
      .notifications {
        cursor: pointer;
      }
      .notifications .item-text {
        flex: 1;
      }
      .profile {
        margin-left: env(safe-area-inset-left);
      }
      :host([rtl]) .profile {
        margin-left: initial;
        margin-right: env(safe-area-inset-right);
      }
      .profile paper-icon-item {
        padding-left: 4px;
      }
      :host([rtl]) .profile paper-icon-item {
        padding-left: auto;
        padding-right: 4px;
      }
      .profile .item-text {
        margin-left: 8px;
      }
      :host([rtl]) .profile .item-text {
        margin-right: 8px;
      }

      .notification-badge {
        min-width: 20px;
        box-sizing: border-box;
        border-radius: 50%;
        font-weight: 400;
        background-color: var(--accent-color);
        line-height: 20px;
        text-align: center;
        padding: 0px 6px;
        color: var(--text-accent-color, var(--text-primary-color));
      }
      ha-svg-icon + .notification-badge {
        position: absolute;
        bottom: 14px;
        left: 26px;
        font-size: 0.65em;
      }

      .spacer {
        flex: 1;
        pointer-events: none;
      }

      .subheader {
        color: var(--sidebar-text-color);
        font-weight: 500;
        font-size: 14px;
        padding: 16px;
        white-space: nowrap;
      }

      .dev-tools {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        padding: 0 8px;
        width: 256px;
        box-sizing: border-box;
      }

      .dev-tools a {
        color: var(--sidebar-icon-color);
      }

      .tooltip {
        display: none;
        position: absolute;
        opacity: 0.9;
        border-radius: 2px;
        white-space: nowrap;
        color: var(--sidebar-background-color);
        background-color: var(--sidebar-text-color);
        padding: 4px;
        font-weight: 500;
      }

      :host([rtl]) .menu mwc-icon-button {
        -webkit-transform: scaleX(-1);
        transform: scaleX(-1);
      }
    `}}]}}),o.a)}}]);
//# sourceMappingURL=chunk.d857df5f9a53929b9fc0.js.map