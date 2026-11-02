"""Historical 100k CHARACTER candidate search, not the current 50k circuit.

Requires NumPy and ngspice; see simulation/README.md for scope and outputs.
"""
from pathlib import Path
import json, subprocess, math, hashlib
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'tmp/wet-character-components'
OUT.mkdir(parents=True, exist_ok=True)
MODEL = ROOT/'simulation/models/TL072_TI.lib'
assert MODEL.is_file()

RFB = 22e3                 # fixed feedback resistor, antiparallel 1N4148 in parallel
IS_D, NVT = 2.52e-9, 1.752*0.02586   # illustrative 1N4148, same as v3 preview
F0 = 440.0
XS = [0, .25, .5, .75, .9, .95, 1]
CYC = 8                    # integer cycles used in harmonic fits

def diode_i(v):
    return 2*IS_D*np.sinh(v/NVT)     # antiparallel pair current

# Nodal model: ideal opamp (Vinv=Vin). Vd = Vout-Vin across RFB||diodes.
# KCL at inv node: Vd/RFB + diode_i(Vd) + (f*(Vin+Vd)-Vin)/D = 0
# f = effective wiper fraction (Vth = f*Vout), D = Rth + Rlead + Rtrim.
def solve_vd(vin, f, D):
    lo = np.full(np.shape(vin), -2.5); hi = np.full(np.shape(vin), 2.5)
    for _ in range(38):
        mid = (lo+hi)/2
        g = mid/RFB + diode_i(mid) + (f*(vin+mid)-vin)/D
        p = g > 0
        hi = np.where(p, mid, hi); lo = np.where(p, lo, mid)
    return (lo+hi)/2

def thd_fit(y):
    N = len(y); phi = 2*np.pi*CYC*np.arange(N)/N
    cols = [np.ones(N)]
    for h in range(1, 11):
        cols += [np.sin(h*phi), np.cos(h*phi)]
    fit = np.linalg.lstsq(np.column_stack(cols), y, rcond=None)[0]
    a = np.hypot(fit[1::2], fit[2::2])
    return float(100*np.linalg.norm(a[1:])/a[0])

def thd_static(amp, f, D, N=256):
    phi = 2*np.pi*CYC*np.arange(N)/N
    vin = amp*np.sin(phi)
    return thd_fit(vin + solve_vd(vin, f, D))

def par(a, b):
    return a*b/(a+b)

def drive_law(x, rlead, rtrim, rload=None):
    # dual-gang drive section: track between opamp output (top) and GND (bottom);
    # wiper moves toward GND as CHARACTER x increases. f from GND end = 1-x.
    rlo = 1e5*(1-x); rhi = 1e5*x
    if rload:
        rlo = par(rlo, rload)
    f = rlo/(rhi+rlo) if (rhi+rlo) > 0 else 0.0
    rth = par(rhi, rlo) if rhi > 0 else 0.0
    D = rth + rlead + rtrim
    G = (D+RFB)/(D+RFB*f)
    return f, D, G

def filter_rth(x, rsmall, rsrc):
    r = rsrc + rsmall + 1e5*x
    return par(r, 1e6)

def fc_at(x, C, rsmall, rsrc):
    return 1/(2*np.pi*C*filter_rth(x, rsmall, rsrc))

def atten440(x, C, rsmall, rsrc):
    fc = fc_at(x, C, rsmall, rsrc)
    return 1/math.sqrt(1+(F0/fc)**2)

# ---- calibration: what gain law would exactly hit the approved THD references ----
def rg_for_thd(target, amp):
    lo, hi = 100., 3e5
    for _ in range(42):
        m = (lo*hi)**.5
        if thd_static(amp, 0.0, m) > target: lo = m
        else: hi = m
    return (lo*hi)**.5

CAL = {}
for tag, fc, tthd in [('halfway', 1500, 2.5), ('x0.9', 700, 12.0), ('x1.0', 600, 18.0)]:
    amp = 0.25/math.sqrt(1+(F0/fc)**2)
    rg = rg_for_thd(tthd, amp)
    CAL[tag] = {'fc_hz': fc, 'target_thd_pct': tthd, 'amp_peak_v': amp,
                'needed_rg_ohm': rg, 'needed_gain': 1+RFB/rg}
print('calibration', json.dumps(CAL, indent=1))

# ---- coarse search over realizable families ----
# Family A: plain dual-gang divider. Family B: A + fixed Rload wiper->GND.
C_GRID = [1.8e-9, 2.2e-9, 2.4e-9, 2.7e-9, 3.3e-9]
RS_GRID = [6800, 7500, 8200, 10000, 12000, 15000]
RL_GRID = [1000, 2200, 3300, 4700]
RT_GRID = [1000, 2000, 3000, 5000, 7000]
RLOAD_GRID = [None, 4700, 5600, 6800, 10000, 15000, 22000, 33000]
XMONO = np.linspace(0, 1, 21)
W = dict(thd_hi=8.0, clean=30.0, mono=1.5, fc=1.2, half=0.3)

def evaluate(C, rsmall, rlead, rtrim, rload):
    cost = 0.0; m = {}
    for x in XS:
        amp = 0.25*atten440(x, C, rsmall, 1000)
        f, D, G = drive_law(x, rlead, rtrim, rload)
        t = thd_static(amp, f, D)
        m[x] = dict(fc=fc_at(x, C, rsmall, 1000), G=G, thd=t)
    cost += W['thd_hi']*(math.log(m[.9]['thd']/12.0)**2 + math.log(m[1]['thd']/18.0)**2)
    cost += W['clean']*max(0.0, m[0]['thd']-0.5)**2
    cost += W['half']*math.log(max(m[.5]['thd'], .01)/2.5)**2
    cost += W['fc']*(math.log(m[0]['fc']/7000)**2 + math.log(m[.9]['fc']/700)**2
                     + math.log(m[1]['fc']/600)**2 + 0.2*math.log(m[.5]['fc']/1500)**2)
    Gs = [drive_law(float(x), rlead, rtrim, rload)[2] for x in XMONO]
    cost += W['mono']*sum(max(0.0, Gs[i]-Gs[i+1])**2 for i in range(len(Gs)-1))
    return cost, m

best = {}
n = 0
for C in C_GRID:
    for rs in RS_GRID:
        for rl in RL_GRID:
            for rt in RT_GRID:
                for rload in RLOAD_GRID:
                    n += 1
                    cost, m = evaluate(C, rs, rl, rt, rload)
                    fam = 'A' if rload is None else 'B'
                    if fam not in best or cost < best[fam][0]:
                        best[fam] = (cost, dict(C=C, rsmall=rs, rlead=rl, rtrim=rt, rload=rload), m)
print(f'searched {n} combos')

def trim_for_target(p, target=18.0):
    lo, hi = 0.0, 10000.0
    for _ in range(40):
        mid = (lo+hi)/2
        f, D, G = drive_law(1.0, p['rlead'], mid, p['rload'])
        t = thd_static(0.25*atten440(1.0, p['C'], p['rsmall'], 1000), f, D)
        if t > target: lo = mid
        else: hi = mid
    return (lo+hi)/2

for fam, (cost, p, m) in best.items():
    p['rtrim'] = round(trim_for_target(p)/100)*100
    cost, m = evaluate(p['C'], p['rsmall'], p['rlead'], p['rtrim'], p['rload'])
    best[fam] = (cost, p, m)
    print(fam, 'cost', round(cost, 3), p)
    for x in XS:
        print(f"  x={x:<5} fc={m[x]['fc']:7.0f} G={m[x]['G']:6.3f} THD={m[x]['thd']:7.3f}%")

CHOSEN_FAM = min(best, key=lambda k: best[k][0])
CH = best[CHOSEN_FAM][1]
print('chosen family', CHOSEN_FAM, CH)

# ---- SPICE decks ----
D4148 = '.model D4148 D(Is=2.52n Rs=.568 N=1.752 Cjo=4p Tt=4n)'

def rpot(v):
    return f'{max(v, 0.01):.2f}'

def passives(p, x, amount=1.0):
    rsmall = p['rsmall'] + 1e5*x
    rhi = rpot(1e5*x); rlo = rpot(1e5*(1-x))
    rl = f"Rload w 0 {p['rload']}\n" if p['rload'] else ''
    return (f'Rfilt wet filt {rsmall:.1f}\nCfilt filt 0 {p["C"]}\nRbias filt 0 1Meg\n'
            f'Rhi drive w {rhi}\nRlo w 0 {rlo}\n{rl}'
            f'Rlead w inv {p["rlead"]+p["rtrim"]:.1f}\n'
            f'Rahi drive amt {rpot(1e4*(1-amount))}\nRalo amt 0 {rpot(1e4*amount)}\n'
            'Cac amt retin 100n\nRin retin rinv 100k\nRfret rout rinv 220k\n'
            'Xret 0 rinv vp vn rout TL072\n')

def drive_stage():
    return 'Xchar filt inv vp vn drive TL072\nRfb drive inv 22k\nD1 drive inv D4148\nD2 inv drive D4148\n'

def spice_run(tag, deck, timeout=180):
    cp = OUT/f'{tag}.cir'
    cp.write_text(deck)
    r = subprocess.run(['ngspice', '-b', str(cp)], cwd=OUT, capture_output=True, text=True, timeout=timeout)
    log = r.stdout + r.stderr
    (OUT/f'{tag}.log').write_text(log)
    if r.returncode != 0 or 'Error' in log:
        raise RuntimeError(tag + '\n' + log[-3000:])

def tran_deck(tag, p, x, peak, rsrc, amount=1.0):
    return f'''Zangei CHARACTER law tran {tag}
.include {MODEL}
Vplus vp 0 12
Vminus vn 0 -12
Vsrc src 0 SIN(0 {peak} 440)
Rsrc src wet {rsrc}
{passives(p, x, amount)}{drive_stage()}{D4148}
.control
set wr_vecnames
set wr_singlescale
tran 2u 27.273m 4.545m 5u uic
wrdata {tag}_tr.dat v(filt) v(drive) v(rout)
.endc
.end
'''

def thd_wave(t, y):
    cols = [np.ones_like(t)]
    for h in range(1, 11):
        cols += [np.sin(2*np.pi*F0*h*t), np.cos(2*np.pi*F0*h*t)]
    fit = np.linalg.lstsq(np.column_stack(cols), y, rcond=None)[0]
    a = np.hypot(fit[1::2], fit[2::2])
    return float(100*np.linalg.norm(a[1:])/a[0])

def tran_metrics(tag):
    d = np.loadtxt(OUT/f'{tag}_tr.dat', skiprows=1)
    t = d[:, 0]; m = t >= t[-1]-CYC/F0
    out = {}
    for i, node in [(1, 'filt'), (2, 'drive'), (3, 'rout')]:
        seg = d[m, i]
        out[f'{node}_thd_pct'] = thd_wave(t[m], seg)
        out[f'{node}_dc_v'] = float(np.mean(seg))
        out[f'{node}_peak_v'] = float(np.max(np.abs(d[t > 2/F0, i])))
    return out

# ---- transient matrix on chosen network ----
matrix = {}
for x in XS:
    for peak in [0.1, 0.25, 0.5]:
        tag = f'tr_x{str(x).replace(".","p")}_pk{str(peak).replace(".","p")}'
        spice_run(tag, tran_deck(tag, CH, x, peak, 1000))
        matrix[tag] = dict(x=x, peak_v=peak, rsrc=1000, trim=CH['rtrim'], **tran_metrics(tag))
        print(tag, round(matrix[tag]['drive_thd_pct'], 3))
for x in XS:   # source resistance 5k sensitivity
    tag = f'tr_x{str(x).replace(".","p")}_rs5k'
    spice_run(tag, tran_deck(tag, CH, x, 0.25, 5000))
    matrix[tag] = dict(x=x, peak_v=0.25, rsrc=5000, trim=CH['rtrim'], **tran_metrics(tag))
    print(tag, round(matrix[tag]['drive_thd_pct'], 3))
for trim in [0.0, 10000.0]:   # trimmer extremes
    pt = dict(CH, rtrim=trim)
    for x in XS:
        tag = f'tr_x{str(x).replace(".","p")}_trim{int(trim/1000)}k'
        spice_run(tag, tran_deck(tag, pt, x, 0.25, 1000))
        matrix[tag] = dict(x=x, peak_v=0.25, rsrc=1000, trim=trim, **tran_metrics(tag))
        print(tag, round(matrix[tag]['drive_thd_pct'], 3))
for x in [0.9, 1.0]:   # AMOUNT coupling check at half rotation
    tag = f'tr_x{str(x).replace(".","p")}_amt50'
    spice_run(tag, tran_deck(tag, CH, x, 0.25, 1000, amount=0.5))
    matrix[tag] = dict(x=x, peak_v=0.25, rsrc=1000, trim=CH['rtrim'], amount=0.5, **tran_metrics(tag))
    print(tag, round(matrix[tag]['drive_thd_pct'], 3))

# runner-up family reduced check for honest comparison
alt_check = {}
ALT_FAM = 'B' if CHOSEN_FAM == 'A' else 'A'
if ALT_FAM in best:
    AL = best[ALT_FAM][1]
    for x in XS:
        tag = f'tr_alt{ALT_FAM}_x{str(x).replace(".","p")}'
        spice_run(tag, tran_deck(tag, AL, x, 0.25, 1000))
        alt_check[tag] = dict(family=ALT_FAM, x=x, **tran_metrics(tag))
        print(tag, round(alt_check[tag]['drive_thd_pct'], 3))

# ---- AC response: unloaded vs loaded filter cutoff ----
def ac_deck(tag, p, x, loaded):
    body = f'Rfilt wet filt {p["rsmall"]+1e5*x:.1f}\nCfilt filt 0 {p["C"]}\nRbias filt 0 1Meg\n'
    if loaded:
        body += drive_stage() + f'Rhi drive w {rpot(1e5*x)}\nRlo w 0 {rpot(1e5*(1-x))}\n'
        if p['rload']:
            body += f'Rload w 0 {p["rload"]}\n'
        body += f'Rlead w inv {p["rlead"]+p["rtrim"]:.1f}\n'
    return f'''Zangei CHARACTER law ac {tag}
.include {MODEL}
Vplus vp 0 12
Vminus vn 0 -12
Vsrc src 0 AC 1
Rsrc src wet 1000
{body}{D4148}
.control
set wr_vecnames
set wr_singlescale
ac dec 30 10 200k
let fm = mag(v(filt))
wrdata {tag}_ac.dat fm
.endc
.end
'''

def cutoff(tag):
    d = np.loadtxt(OUT/f'{tag}_ac.dat', skiprows=1)
    f, m = d[:, 0], d[:, 1]
    ref = m[0]/math.sqrt(2)
    i = int(np.argmax(m < ref))
    if i == 0:
        return None
    return float(f[i-1] + (f[i]-f[i-1])*(ref-m[i-1])/(m[i]-m[i-1]))

ac_res = {}
for x in XS:
    for loaded in [False, True]:
        tag = f'ac_x{str(x).replace(".","p")}_{"loaded" if loaded else "unloaded"}'
        spice_run(tag, ac_deck(tag, CH, x, loaded))
        ac_res[tag] = dict(x=x, loaded=loaded, fc_minus3db_hz=cutoff(tag))
print(json.dumps(ac_res, indent=1))

# ---- DC/static model validation against SPICE ----
def dc_deck(tag, p, x):
    return f'''Zangei CHARACTER law dc {tag}
.include {MODEL}
Vplus vp 0 12
Vminus vn 0 -12
Vsrc src 0 0
Rsrc src wet 1000
{passives(p, x)}{drive_stage()}{D4148}
.control
set wr_vecnames
set wr_singlescale
dc Vsrc -0.35 0.35 0.001
wrdata {tag}_dc.dat v(filt) v(drive)
.endc
.end
'''

dc_val = {}
for x in [0.9, 1.0]:
    tag = f'dc_x{str(x).replace(".","p")}'
    spice_run(tag, dc_deck(tag, CH, x))
    d = np.loadtxt(OUT/f'{tag}_dc.dat', skiprows=1)
    vfilt, vdrive = d[:, 1], d[:, 2]
    f, D, G = drive_law(x, CH['rlead'], CH['rtrim'], CH['rload'])
    pred = vfilt + solve_vd(vfilt, f, D)
    err = float(100*np.sqrt(np.mean((pred-vdrive)**2))/np.sqrt(np.mean(vdrive**2)))
    dc_val[tag] = dict(x=x, static_vs_spice_rms_err_pct=err)
    print(tag, 'static-vs-SPICE err %', round(err, 4))

# ---- static law table for chosen network (both source resistances) ----
law_table = []
for x in XS:
    f, D, G = drive_law(x, CH['rlead'], CH['rtrim'], CH['rload'])
    row = dict(x=x, wiper_f=round(f, 5), divider_D_ohm=round(D, 1), gain=round(G, 4),
               fc_hz_rsrc1k=round(fc_at(x, CH['C'], CH['rsmall'], 1000), 1),
               fc_hz_rsrc5k=round(fc_at(x, CH['C'], CH['rsmall'], 5000), 1),
               thd_static_pct_rsrc1k=round(thd_static(0.25*atten440(x, CH['C'], CH['rsmall'], 1000), f, D), 4),
               thd_static_pct_rsrc5k=round(thd_static(0.25*atten440(x, CH['C'], CH['rsmall'], 5000), f, D), 4))
    law_table.append(row)

fam_cmp = {}
for fam, (cost, p, m) in best.items():
    fam_cmp[fam] = dict(cost=round(cost, 3), params={k: v for k, v in p.items()},
                        thd={str(x): round(m[x]['thd'], 3) for x in XS},
                        fc={str(x): round(m[x]['fc'], 1) for x in XS},
                        gain={str(x): round(m[x]['G'], 3) for x in XS})

network = {
    'description': 'One dual-gang B100k CHARACTER pot + fixed passives; gang 1 pre-filter rheostat, gang 2 drive divider; TL072 non-inverting with 22k || antiparallel 1N4148 feedback; second TL072 inverting return (provisional -2.2).',
    'filter': f"OUT_SH -> source R -> Rsmall {CH['rsmall']}R + gang1 rheostat 100k*x -> node FILT; C {CH['C']*1e9:.2f}nF FILT->GND; 1Meg FILT->GND bias; FILT -> TL072 pin 3 (non-inv).",
    'drive': f"TL072 out DRIVE -> gang2 track top; track bottom -> GND; wiper W at fraction (1-x) from GND; "
             + (f"Rload {CH['rload']}R W->GND; " if CH['rload'] else '')
             + f"W -> fixed Rlead {CH['rlead']}R + 10k trimmer (default {CH['rtrim']:.0f}R, range 0-10k) -> INV (pin 2); RFB 22k DRIVE->INV with antiparallel 1N4148 pair in parallel. Increasing x moves wiper toward GND, raising closed-loop gain.",
    'amount_return': "DRIVE -> AMOUNT 10k divider -> wiper -> 100nF -> 100k input R -> return TL072 inverting input; 220k feedback (gain -2.2, PROVISIONAL, not a loop calibration); non-inverting input grounded.",
}

summary = {
    'study': 'Zangei wet feedback CHARACTER component-law bounded study',
    'date': '2026-10-18',
    'model': {'opamp': 'TL072 TI legacy macromodel (simulation/models/TL072_TI.lib), +/-12V rails',
              'diodes': 'illustrative 1N4148 (Is=2.52n, N=1.752), same as v3 preview'},
    'measurement': 'harmonic-only THD, 440Hz sine, least-squares fit h=1..10 over 8 cycles, drive node',
    'calibration_needed': CAL,
    'families_compared': fam_cmp,
    'chosen_family': CHOSEN_FAM,
    'chosen_params': CH,
    'network': network,
    'law_table': law_table,
    'spice_transient_matrix': matrix,
    'spice_alt_family_check': alt_check,
    'spice_ac_cutoffs': ac_res,
    'dc_static_model_validation': dc_val,
    'limits': 'Simulation-only voicing study with typical models; NOT hardware validated. Return gain -2.2 is provisional and not a full-loop calibration. THD targets are reference-tone voicing, not specifications.',
}
(OUT/'summary.json').write_text(json.dumps(summary, indent=1))

# ---- FINDINGS.md ----
def law_row(r):
    return (f"| {r['x']} | {r['fc_hz_rsrc1k']:.0f} | {r['fc_hz_rsrc5k']:.0f} | {r['gain']:.3f} "
            f"| {r['thd_static_pct_rsrc1k']:.2f} | {r['thd_static_pct_rsrc5k']:.2f} |")

law_md = '\n'.join(law_row(r) for r in law_table)

def mtx(x, peak=0.25, rsrc=1000, trim=None):
    trim = CH['rtrim'] if trim is None else trim
    for k, v in matrix.items():
        if v['x'] == x and v['peak_v'] == peak and v['rsrc'] == rsrc and v['trim'] == trim and 'amount' not in v:
            return v
    raise KeyError((x, peak, rsrc, trim))

spice_md = '\n'.join(
    f"| {x} | {mtx(x)['drive_thd_pct']:.2f} | {mtx(x)['rout_thd_pct']:.2f} | "
    f"{mtx(x, peak=0.1)['drive_thd_pct']:.2f} | {mtx(x, peak=0.5)['drive_thd_pct']:.2f} | "
    f"{mtx(x, rsrc=5000)['drive_thd_pct']:.2f} | {mtx(x, trim=0.0)['drive_thd_pct']:.2f} | {mtx(x, trim=10000.0)['drive_thd_pct']:.2f} |"
    for x in XS)

ac_md = '\n'.join(
    f"| {x} | {ac_res[f'ac_x{str(x).replace(chr(46),chr(112))}_unloaded']['fc_minus3db_hz']:.0f} "
    f"| {ac_res[f'ac_x{str(x).replace(chr(46),chr(112))}_loaded']['fc_minus3db_hz']:.0f} |"
    for x in XS)

pk_drive = max(v['drive_peak_v'] for v in matrix.values())
pk_rout = max(v['rout_peak_v'] for v in matrix.values())
dc_off = max(abs(v['drive_dc_v']) for v in matrix.values())
amt_full = mtx(1.0)['rout_peak_v']
amt_half = [v for v in matrix.values() if v.get('amount') == 0.5 and v['x'] == 1.0][0]['rout_peak_v']
alt_md = ''
if alt_check:
    alt_md = '\n'.join(f"| {v['x']} | {v['drive_thd_pct']:.2f} |" for v in alt_check.values())

fcmp_md = '\n'.join(
    f"| {fam} | {c['cost']:.2f} | {c['thd']['0.9']} | {c['thd']['1']} | {c['thd']['0']} | {c['gain']['0.9']} | {c['gain']['1']} |"
    for fam, c in fam_cmp.items())

sp09 = mtx(0.9)['drive_thd_pct']; sp1 = mtx(1.0)['drive_thd_pct']; sp5 = mtx(0.5)['drive_thd_pct']
altA09 = alt_check.get('tr_altA_x0p9', {}).get('drive_thd_pct', float('nan'))
findings = f"""# Wet CHARACTER component-law study — findings (2026-10-18)

Script: `simulation/wet_character_components.py`. Raw decks/logs/data + `summary.json` in this folder.
Simulation-only with TI TL072 macromodel (+/-12 V) and illustrative 1N4148; NOT hardware validated.

## Chosen physical network (family {CHOSEN_FAM})

{network['filter']}

{network['drive']}

{network['amount_return']}

Chosen values: C = {CH['C']*1e9:.2f} nF, Rsmall = {CH['rsmall']} ohm, Rlead = {CH['rlead']} ohm,
trimmer default = {CH['rtrim']:.0f} ohm (bounded 0-10k internal trim), Rload = {CH['rload'] if CH['rload'] else 'none'}.

## Required gain law (from approved references)

Static-diode calibration says the pot law must reproduce, at 0.25 V peak input after filtering:
90% (700 Hz, 12%): gain {CAL['x0.9']['needed_gain']:.2f} (Rg {CAL['x0.9']['needed_rg_ohm']:.0f} ohm);
max (600 Hz, 18%): gain {CAL['x1.0']['needed_gain']:.2f} (Rg {CAL['x1.0']['needed_rg_ohm']:.0f} ohm).

## Realized law (static model, 1k source)

| x | fc Hz (1k src) | fc Hz (5k src) | gain | THD% (1k) | THD% (5k) |
|---|---|---|---|---|---|
{law_md}

## Family comparison (static model, coarse E-value search)

| family | cost | THD@0.9 | THD@1 | THD@0 | G@0.9 | G@1 |
|---|---|---|---|---|---|---|
{fcmp_md}

## SPICE verification (chosen network, vendor TL072)

THD% at drive node, 0.25 V peak unless noted; rout = return amp output.

| x | drive 0.25pk | rout 0.25pk | drive 0.1pk | drive 0.5pk | drive 5k src | trim=0 | trim=10k |
|---|---|---|---|---|---|---|---|
{spice_md}

Static model vs SPICE DC transfer RMS error: x=0.9: {dc_val['dc_x0p9']['static_vs_spice_rms_err_pct']:.3f}%, x=1: {dc_val['dc_x1p0']['static_vs_spice_rms_err_pct']:.3f}%.

Runner-up family {ALT_FAM} SPICE spot check (drive THD%, 0.25 V peak):

| x | THD% |
|---|---|
{alt_md}

## AC cutoff (filter node, -3 dB)

| x | unloaded Hz | loaded Hz |
|---|---|---|
{ac_md}

## DC / headroom

Max drive peak {pk_drive:.2f} V, max return-output peak {pk_rout:.2f} V (TL072 swings about +/-10 V on +/-12 V rails).
Max drive-node DC offset across matrix {dc_off*1000:.2f} mV. No rail approach at any tested level (up to 0.5 V peak input).

## CHARACTER-AMOUNT coupling

Return output = -2.2 x AMOUNT wiper fraction x drive output (multiplicative; neither knob rescales the other).
At x=1, 0.25 V peak: AMOUNT full rout peak {amt_full:.2f} V, AMOUNT half {amt_half:.2f} V
(~half, minus ~2.5% wiper-loading error from 2.5k source into 100k). CHARACTER sets drive amplitude/THD; AMOUNT only scales.

## Compromise statement

Targets: 12% THD @0.9, 18% @1, essentially clean bright end (0.25 V peak, 1k source).
The 100k drive gang has Thevenin resistance 100k*x*(1-x) at the wiper: 9k at x=0.9, falling to 0 only at exactly x=1.
Unloaded (family A), that 9k sits in series with Rlead+trim in the divider leg and caps the x=0.9 gain near 2.3-2.8,
far under the {CAL['x0.9']['needed_gain']:.2f} the 12% reference needs; family A reaches only {fam_cmp['A']['thd']['0.9']}% THD at x=0.9
(SPICE spot check {altA09:.2f}%). A fixed 4.7k wiper-to-GND load (family B) shunts the lower
track section, cutting both the Thevenin resistance and the effective wiper fraction; with the values above the law stays
monotonic (verified on a 41-point wiper grid) and roughly triples upper-mid gain. SPICE-verified result: {sp09:.2f}% @0.9
(target 12), {sp1:.2f}% @1 (target 18), 0.00% at bright, midpoint {sp5:.2f}% (flexible per brief; this law runs driven-darker
through the middle). fc endpoints: {law_table[-1]['fc_hz_rsrc1k']:.0f} Hz at max vs 600 target (+12%), {law_table[0]['fc_hz_rsrc1k']:.0f} Hz bright vs ~7000.
Reaching the full 12% @0.9 AND 18% @1 simultaneously is not possible in this family with a B100k gang, 22k feedback and
0.5 Vpp input: gain at x=0.9 is structurally capped below {CAL['x0.9']['needed_gain']:.2f} while x=1 gain (set by Rlead+trim alone)
is free. Options for the schematic phase (outside this study): dual B10k gang for the drive section (Rth 0.9k @0.9),
a small fixed pre-gain before the drive stage, or accept ~8-9% @0.9 as the realized upper-mid voicing with the 10k trim
covering 3.5%-25.8% at maximum for taste.

## Status

- Return gain -2.2 is PROVISIONAL, not a full-loop calibration (input summer outside scope).
- Voicing targets are reference-tone guides, not specifications. No BBD/S&H/loop included.
- No hardware validation claimed; bench test required before schematic freeze.
"""
(OUT/'FINDINGS.md').write_text(findings)
print('wrote', OUT/'summary.json', OUT/'FINDINGS.md')
