// Rural Broadband Fix — anonymous opt-in counter backend (v3: org attribution + contact forwarding)
// Paste into script.google.com → Deploy as Web app (Execute as: Me, Access: Anyone)
// IMPORTANT: after pasting, press Ctrl+S, then Deploy > Manage deployments > edit > New version
//
// CONTACT EMAIL SETUP: run setOrgEmail('orgtag', 'inbox@example.org') once per org in the
// script editor (▶ Run), or set a default with setOrgEmail('default', 'you@example.org').
// Contact form submissions are emailed to the org's address — nothing is stored.

var PROP_KEY = 'rbf_optin_counts_v1';
var ORG_EMAIL_KEY = 'rbf_org_emails_v1';

function setOrgEmail(org, email) {
  var raw = PropertiesService.getScriptProperties().getProperty(ORG_EMAIL_KEY);
  var m = {};
  try { m = JSON.parse(raw) || {}; } catch (x) {}
  m[String(org).toLowerCase()] = email;
  PropertiesService.getScriptProperties().setProperty(ORG_EMAIL_KEY, JSON.stringify(m));
  Logger.log('Org email set: ' + org + ' -> ' + email);
}

function getOrgEmail(org) {
  var raw = PropertiesService.getScriptProperties().getProperty(ORG_EMAIL_KEY);
  var m = {};
  try { m = JSON.parse(raw) || {}; } catch (x) {}
  return m[String(org).toLowerCase()] || m['default'] || null;
}
var OR_ZIPS = ["89421","97001","97002","97003","97004","97005","97006","97007","97008","97009","97011","97013","97014","97015","97016","97017","97018","97019","97020","97021","97022","97023","97024","97026","97027","97028","97029","97030","97031","97032","97033","97034","97035","97037","97038","97039","97040","97041","97042","97045","97048","97049","97050","97051","97053","97054","97055","97056","97057","97058","97060","97062","97063","97064","97065","97067","97068","97070","97071","97078","97080","97086","97089","97101","97102","97103","97106","97107","97108","97109","97110","97111","97112","97113","97114","97115","97116","97117","97118","97119","97121","97122","97123","97124","97125","97127","97128","97130","97131","97132","97133","97134","97135","97136","97137","97138","97140","97141","97144","97145","97146","97147","97148","97149","97201","97202","97203","97204","97205","97206","97208","97209","97210","97211","97212","97213","97214","97215","97216","97217","97218","97219","97220","97221","97222","97223","97224","97225","97227","97229","97230","97231","97232","97233","97236","97239","97258","97266","97267","97301","97302","97303","97304","97305","97306","97310","97317","97321","97322","97324","97325","97326","97327","97329","97330","97331","97333","97335","97336","97338","97341","97342","97343","97344","97345","97346","97347","97348","97350","97351","97352","97355","97357","97358","97360","97361","97362","97364","97365","97366","97367","97368","97369","97370","97371","97373","97374","97375","97376","97377","97378","97380","97381","97383","97384","97385","97386","97388","97389","97390","97391","97392","97394","97396","97401","97402","97403","97404","97405","97406","97408","97410","97411","97412","97413","97414","97415","97416","97417","97419","97420","97423","97424","97426","97429","97430","97431","97432","97434","97435","97436","97437","97438","97439","97441","97442","97443","97444","97446","97447","97448","97449","97450","97451","97452","97453","97454","97455","97456","97457","97458","97459","97461","97462","97463","97465","97466","97467","97469","97470","97471","97473","97476","97477","97478","97479","97480","97481","97484","97486","97487","97488","97489","97490","97492","97493","97494","97495","97496","97497","97498","97499","97501","97502","97503","97504","97520","97522","97523","97524","97525","97526","97527","97530","97531","97532","97534","97535","97536","97537","97538","97539","97540","97541","97543","97544","97601","97603","97604","97620","97621","97622","97623","97624","97625","97626","97627","97630","97632","97633","97634","97636","97637","97638","97639","97640","97641","97701","97702","97703","97707","97709","97710","97711","97712","97720","97721","97722","97730","97731","97732","97733","97734","97735","97736","97737","97738","97739","97741","97750","97751","97752","97753","97754","97756","97758","97759","97760","97761","97801","97810","97812","97813","97814","97817","97818","97819","97820","97823","97824","97825","97826","97827","97828","97830","97833","97834","97835","97836","97837","97838","97839","97840","97841","97842","97843","97844","97845","97846","97848","97850","97856","97857","97859","97862","97864","97865","97867","97868","97869","97870","97873","97874","97875","97876","97877","97880","97882","97883","97884","97885","97886","97901","97902","97903","97904","97905","97906","97907","97908","97909","97910","97911","97913","97914","97917","97918","97920"];

function doGet(e) {
  var p = (e && e.parameter) || {};
  var cb = /^[A-Za-z_$][A-Za-z0-9_$]*$/.test(p.callback || '') ? p.callback : null;
  var org = String(p.org || '').toLowerCase().replace(/[^a-z0-9_-]/g, '').substring(0, 32);
  var raw = PropertiesService.getScriptProperties().getProperty(PROP_KEY);
  var c = { zips: {}, total: 0, orgs: {} };
  try { var j = JSON.parse(raw); if (j.zips) c.zips = j.zips; if (j.total) c.total = j.total; if (j.orgs) c.orgs = j.orgs; } catch (x) {}
  if (p.optin) {
    var zip = String(p.optin).trim();
    if (!/^\d{5}$/.test(zip) || OR_ZIPS.indexOf(zip) === -1) {
      var err = JSON.stringify({ ok: false, error: 'invalid_zip' });
      return ContentService.createTextOutput(cb ? cb + '(' + err + ');' : err).setMimeType(cb ? ContentService.MimeType.JAVASCRIPT : ContentService.MimeType.JSON);
    }
    var lock = LockService.getScriptLock(); lock.waitLock(10000);
    try {
      c.zips[zip] = (c.zips[zip] || 0) + 1; c.total = (c.total || 0) + 1;
      if (org) { c.orgs[org] = (c.orgs[org] || 0) + 1; }
      PropertiesService.getScriptProperties().setProperty(PROP_KEY, JSON.stringify(c));
    } finally { lock.releaseLock(); }
    var ok = JSON.stringify({ ok: true, zip: zip, zipCount: c.zips[zip], total: c.total, org: org || null });
    return ContentService.createTextOutput(cb ? cb + '(' + ok + ');' : ok).setMimeType(cb ? ContentService.MimeType.JAVASCRIPT : ContentService.MimeType.JSON);
  }
  if (p.contact) {
    // Contact-me form: forward to the org's inbox, store nothing.
    var to = getOrgEmail(org);
    var out = function(obj) {
      var s = JSON.stringify(obj);
      return ContentService.createTextOutput(cb ? cb + '(' + s + ');' : s).setMimeType(cb ? ContentService.MimeType.JAVASCRIPT : ContentService.MimeType.JSON);
    };
    if (!to) { return out({ ok: false, error: 'no_org_email' }); }
    var cName = String(p.name || '').substring(0, 100);
    var cAddr = String(p.addr || '').substring(0, 200);
    var cZip = String(p.zip || '').substring(0, 10);
    var cPhone = String(p.phone || '').substring(0, 40);
    var cEmail = String(p.email || '').substring(0, 100);
    if (!cName || !cAddr || !/^\d{5}$/.test(cZip) || !cPhone) {
      return out({ ok: false, error: 'missing_fields' });
    }
    var subject = 'Rural Broadband Fix: contact request' + (org ? ' [' + org + ']' : '') + ' — ' + cZip;
    var body = 'New contact-me request from rural-broadband-fix.vercel.app\n\n'
      + 'Name: ' + cName + '\n'
      + 'Address: ' + cAddr + '\n'
      + 'ZIP: ' + cZip + '\n'
      + 'Phone: ' + cPhone + '\n'
      + (cEmail ? 'Email: ' + cEmail + '\n' : '')
      + (org ? 'Org tag: ' + org + '\n' : '')
      + '\nThis person asked to be contacted when satellite service is available in their area.';
    try {
      MailApp.sendEmail(to, subject, body, { name: 'Rural Broadband Fix' });
    } catch (err) {
      return out({ ok: false, error: 'send_failed' });
    }
    return out({ ok: true });
  }
  var body = JSON.stringify({ ok: true, total: c.total, zips: c.zips, orgs: c.orgs });
  return ContentService.createTextOutput(cb ? cb + '(' + body + ');' : body).setMimeType(cb ? ContentService.MimeType.JAVASCRIPT : ContentService.MimeType.JSON);
}
