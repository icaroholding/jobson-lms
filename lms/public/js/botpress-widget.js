// Botpress Chat Widget Integration
(function() {
	// Load Botpress inject script
	const injectScript = document.createElement('script');
	injectScript.src = 'https://cdn.botpress.cloud/webchat/v3.5/inject.js';
	document.head.appendChild(injectScript);

	// Load Botpress config script
	const configScript = document.createElement('script');
	configScript.src = 'https://files.bpcontent.cloud/2025/11/17/23/20251117230919-434T858E.js';
	configScript.defer = true;
	document.head.appendChild(configScript);

	// Add mobile styling for bottom margin
	const style = document.createElement('style');
	style.textContent = `
		/* Botpress widget mobile styling */
		@media screen and (max-width: 768px) {
			#bp-web-widget,
			#bp-widget,
			[id^="bp-"],
			.bpWidget,
			.bp-widget-web {
				bottom: 60px !important;
			}
			
			/* Style for widget container if using iframe */
			iframe[id^="bp-web-widget"],
			iframe[title*="Botpress"],
			iframe[title*="botpress"] {
				bottom: 60px !important;
			}
		}

		/* Style to ensure widget doesn't cover important content */
		@media screen and (max-width: 768px) {
			body {
				padding-bottom: env(safe-area-inset-bottom);
			}
		}
	`;
	document.head.appendChild(style);
})();
