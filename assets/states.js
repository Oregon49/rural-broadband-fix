// Per-state BEAD data for Rural Broadband Fix multi-state site.
// Researched Oct 17, 2026. See ~/workspace/grant-research/bead-three-state-numbers.md for sources.
// Starlink costs are national (same everywhere).
window.RBF_STATES = {
  "OR": {
    name: "Oregon",
    bead_allocation_usd: 689000000,
    bead_allocation_label: "$689 million",
    locations: 104654,
    fiber_per_location_usd: 9421,
    fiber_basis: "Oregon BEAD approved average ($517.2M ÷ 54,895 locations)",
    fiber_locations: 54895,
    fiber_share_pct: 52.5,
    satellite_per_location_usd: 550,
    satellite_locations: 48631,
    satellite_share_pct: 46.4,
    wireless_share_pct: 1.1,
    tech_mix_label: "52.5% fiber, 46.4% satellite, 1.1% fixed wireless",
    bead_tool_url: "https://www.oregon.gov/biz/programs/BEAD/",
    bead_tool_label: "Oregon's BEAD tool",
    approval_note: "Final Proposal approved by NTIA Feb 4, 2026",
    flyer_line: "Oregon will pay $9,421 per home for fiber — or $550 per home for satellite. Same program, same state.",
    zip_prefixes: ["970","971","972","973","974","975","976","977","978","979"],
    has_zip_data: true
  },
  "TX": {
    name: "Texas",
    bead_allocation_usd: 1260000000,
    bead_allocation_label: "$1.26 billion",
    locations: 242903,
    fiber_per_location_usd: 12400,
    fiber_basis: "Nexstream award: $401.8M ÷ 32,404 locations (fiber + fixed wireless)",
    fiber_locations: 123000,
    fiber_share_pct: 50.6,
    satellite_per_location_usd: 1703,
    satellite_basis: "Starlink award: $108.8M ÷ 63,887 locations",
    satellite_locations: 65800,
    satellite_share_pct: 27.1,
    wireless_share_pct: 22.3,
    tech_mix_label: "50.6% fiber, 27.1% satellite, 22.3% fixed wireless",
    bead_tool_url: "https://www.broadband.texas.gov/",
    bead_tool_label: "Texas Broadband Development Office",
    approval_note: "Final Proposal approved by NTIA Nov 2025",
    flyer_line: "Texas will pay ~$12,400 per home for fiber — or ~$1,700 per home for Starlink. Same program, same state.",
    zip_prefixes: ["750","751","752","753","754","755","756","757","758","759","760","761","762","763","764","765","766","767","768","769","770","771","772","773","774","775","776","777","778","779","780","781","782","783","784","785","786","787","788","789","790","791","792","793","794","795","796","797","798","799","885"],
    has_zip_data: false
  },
  "CA": {
    name: "California",
    bead_allocation_usd: 1420000000,
    bead_allocation_label: "$1.42 billion",
    locations: 270571,
    fiber_per_location_usd: 32000,
    fiber_basis: "California Advanced Services Fund projects average (state program, separate from BEAD)",
    fiber_locations: 143098,
    fiber_share_pct: 52.9,
    satellite_per_location_usd: 1086,
    satellite_basis: "Amazon Leo draft award: ~$100M ÷ ~92,000 locations (draft figure)",
    satellite_locations: 72937,
    satellite_share_pct: 27.0,
    wireless_share_pct: 20.1,
    tech_mix_label: "52.9% fiber, 27.0% satellite, 20.1% fixed wireless",
    bead_tool_url: "https://www.cpuc.ca.gov/broadband/",
    bead_tool_label: "California Public Utilities Commission broadband page",
    approval_note: "Final Proposal approved by NTIA July 17, 2026; CPUC ratified Sept 17, 2026",
    flyer_line: "California's own projects pay ~$32,000 per home for fiber. Satellite providers bid ~$1,100 per home. Same goal, 30x the price.",
    zip_prefixes: ["900","901","902","903","904","905","906","907","908","909","910","911","912","913","914","915","916","917","918","919","920","921","922","923","924","925","926","927","928","929","930","931","932","933","934","935","936","937","938","939","940","941","942","943","944","945","946","947","948","949","950","951","952","953","954","955","956","957","958","959","960","961"],
    has_zip_data: false
  },
  "MO": {
    name: "Missouri",
    bead_allocation_usd: 790500000,
    bead_allocation_label: "$790.5 million",
    locations: 204366,
    fiber_per_location_usd: 3877,
    fiber_basis: "Missouri BEAD all-technology average ($790.5M ÷ 204,366 locations); fiber-only cost will be higher",
    fiber_locations: 167282,
    fiber_share_pct: 81.9,
    satellite_per_location_usd: 644,
    satellite_basis: "Amazon Kuiper award: $17.56M ÷ 27,264 locations",
    satellite_locations: 23378,
    satellite_share_pct: 11.4,
    wireless_share_pct: 5.6,
    tech_mix_label: "81.9% fiber, 11.4% satellite, 5.6% fixed wireless",
    bead_tool_url: "https://ded.mo.gov/programs/community/broadband-equity-access-and-deployment-bead-program",
    bead_tool_label: "Missouri Office of Broadband Development",
    approval_note: "Final Proposal approved by NTIA Jan 6, 2026",
    flyer_line: "Missouri is spending 82% of its BEAD money on fiber — but Amazon's satellite bid came in at $644 per home. Ask what the fiber homes cost.",
    zip_prefixes: ["630","631","632","633","634","635","636","637","638","639","640","641","642","643","644","645","646","647","648","649","650","651","652","653","654","655","656","657","658"],
    has_zip_data: false
  }
};
// ZIP prefix -> state code lookup
window.RBF_ZIP_TO_STATE = (function(){
  var m = {};
  Object.keys(window.RBF_STATES).forEach(function(st){
    window.RBF_STATES[st].zip_prefixes.forEach(function(p){ m[p] = st; });
  });
  return m;
})();
window.RBF_STARLINK_PER_LOCATION = 3469; // $349 kit + $130/mo x 24
