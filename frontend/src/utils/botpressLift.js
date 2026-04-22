// Lift the Botpress webchat launcher above the bottom navbar on mobile,
// only while the chat is closed. Runs once per page load and reacts to
// DOM mutations because the Botpress SDK creates the launcher async.
export function initBotpressLift() {
	const mq = window.matchMedia('(max-width: 768px)')
	const LIFT_BOTTOM = '60px'

	function apply() {
		const container = document.querySelector('.bpFabContainer')
		if (!container) return
		const isClosed = !!container.querySelector('.bpFabIcon')
		if (mq.matches && isClosed) {
			container.style.setProperty('bottom', LIFT_BOTTOM, 'important')
		} else {
			container.style.removeProperty('bottom')
		}
	}

	const observer = new MutationObserver(apply)
	observer.observe(document.body, { childList: true, subtree: true })

	if (mq.addEventListener) mq.addEventListener('change', apply)

	apply()
	setTimeout(apply, 500)
	setTimeout(apply, 1500)
	setTimeout(apply, 3000)
}
