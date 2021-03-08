export default function () {
  const oc = { _e: [] }
  const action = ['config', 'track', 'identify', 'visit', 'push', 'call', 'trackForm', 'trackClick']
  action.forEach(
    r => (oc[r] = function () { oc._e.push([r, ...arguments]) })
  )

  window._w = {}
  window._w.woopra = window.woopra = oc
  const script = document.createElement('script')
  script.src = '//static.woopra.com/js/w.js'
  document.head.append(script)
  window.woopra.config({ domain: 'hoffmannp.github.io' })
  window.woopra.track()
}
