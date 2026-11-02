"""Historical buffered-TIME-knob study, not validation of current Clock_CV.

Run with Python 3 and ngspice; see simulation/README.md for scope and outputs.
"""
from pathlib import Path
import csv
import json
import subprocess
import sys

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / 'tmp' / 'clock-active-fix' / 'simulation'
OUT.mkdir(parents=True, exist_ok=True)
MODEL = HERE / 'models' / 'TL072_TI.lib'


def run(name, pot, temperature=27, transient=False, source_only=True):
    top = max(0.001, 100000 * (1 - pot))
    bottom = max(0.001, 100000 * pot)
    rail = 'Breg 0 rail I=max(0,(5-v(rail))/1)' if source_only else 'Vrail rail 0 5'
    cv = 'PWL(0 -12 1m -12 1.001m 12 3m 12 3.001m -12 5m -12)' if transient else '0'
    body = f'''Zangei buffered knob plus half-scale external CV
.include {MODEL}
.temp {temperature}
Vplus vp 0 12
Vminus vn 0 -12
{rail}
R308 rail upper 470
R307 upper lower 3.9k
R309 lower 0 470
Crail rail 0 100n
Rtop rail knob {top}
Rbottom knob low {bottom}
R303 low 0 22.2k
X302A knob knobbuf vp vn knobbuf TL072
Vcv cv 0 {cv}
R501 knobbuf mix 100k
R502 cv mix 200k
R503 sum fb 20k
R504 fb 0 40k
X302B mix fb vp vn sum TL072
R306 sum vco 100k
D304 vco upper SCH
D303 lower vco SCH
Cvco vco 0 10p
Vinh inhraw 0 0
R304 inhraw inhibit 100k
R305 inhibit 0 1Meg
D301 inhibit upper SCH
D302 lower inhibit SCH
Cinh inhibit 0 10p
.model SCH D(Is=10n N=1.05 Rs=10 Cjo=10p M=.3 Vj=.4 Bv=30 Ibv=1m)
.control
set wr_vecnames
set wr_singlescale
save all @d301[id] @d302[id] @d303[id] @d304[id]
'''
    control = 'tran 100n 5m' if transient else 'dc Vcv -12 12 .25 Vinh -12 12 6'
    deck = OUT / f'{name}.cir'
    deck.write_text(body + control + f'\nwrdata {name}.dat v(cv) v(inhraw) v(knob) v(knobbuf) v(mix) v(sum) v(vco) v(inhibit) v(rail) @d301[id] @d302[id] @d303[id] @d304[id]\n.endc\n.end\n')
    r = subprocess.run(['ngspice', '-b', str(deck)], cwd=OUT, capture_output=True, text=True)
    log = r.stdout + r.stderr
    (OUT / f'{name}.log').write_text(log)
    if r.returncode or 'Error:' in log:
        raise RuntimeError(log)
    lines = (OUT / f'{name}.dat').read_text().splitlines()
    keys = lines[0].split()
    return [dict(zip(keys, map(float, line.split()))) for line in lines[1:]]


def main():
    rows = []
    for temperature in (0, 27, 60):
        for pot in (0, .25, .5, .75, 1):
            for row in run(f'dc_{temperature}_{pot}', pot, temperature):
                rows.append({'temperature': temperature, 'pot': pot, **row})
    edges = run('edges', .5, transient=True)
    for row in rows + edges:
        assert 0 < row['v(vco)'] < row['v(rail)']
        assert 0 < row['v(inhibit)'] < row['v(rail)']
        assert abs(row['v(rail)'] - 5) < .01
    linear = [r for r in rows if 1 < r['v(knob)'] + .5 * r['v(cv)'] < 4.5]
    summary = {
        'dc_rows': len(rows),
        'vco_dc_range': [min(r['v(vco)'] for r in rows), max(r['v(vco)'] for r in rows)],
        'inhibit_dc_range': [min(r['v(inhibit)'] for r in rows), max(r['v(inhibit)'] for r in rows)],
        'vco_edge_range': [min(r['v(vco)'] for r in edges), max(r['v(vco)'] for r in edges)],
        'rail_range': [min(r['v(rail)'] for r in rows), max(r['v(rail)'] for r in rows)],
        'linear_max_sum_error': max(abs(r['v(sum)'] - r['v(knob)'] - .5*r['v(cv)']) for r in linear),
        'max_upper_clamp_current': max(r['@d301[id]'] + r['@d304[id]'] for r in rows),
        'limitations': 'Inset references keep tested typical nodes within the rails, at the cost of endpoint headroom. Illustrative Schottky and TI legacy op-amp models; no ESD/power-off/resistor-tolerance qualification.'
    }
    with (OUT / 'dc.csv').open('w') as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    (OUT / 'summary.json').write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
