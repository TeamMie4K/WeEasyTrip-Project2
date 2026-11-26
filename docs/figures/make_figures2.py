# -*- coding: utf-8 -*-
"""make_figures2.py — กราฟผลการทดลองสำหรับบทที่ 4 (อ่านจาก experiments/results/*.json)
fig_scores.png: คะแนนเฉลี่ย Greedy/GA/Hybrid 4 จังหวัด x 3 สถานการณ์ (แท่งผิดพลาด = SD)
fig_diag.png:   ระยะขับกับคะแนนดิบของจังหวัดข้อมูลน้อย 4 จังหวัด (S2)
fig_tradeoff.png: คะแนนกับระยะขับเมื่อปรับ DIST_WEIGHT (Hybrid, GA) และ GREEDY_KM_PENALTY (Greedy)"""
import os, json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'TH Sarabun New'
plt.rcParams['font.size'] = 15
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False
HERE = os.path.dirname(__file__)
RES = os.path.join(HERE, '..', '..', 'experiments', 'results')
C = {'Greedy': '#8A8A8A', 'GA': '#4C78A8', 'Hybrid': '#E2711D'}
TH = {'phuket': 'ภูเก็ต', 'chiangmai': 'เชียงใหม่', 'krabi': 'กระบี่', 'samui': 'เกาะสมุย', 'phichit': 'พิจิตร',
      'chaiyaphum': 'ชัยภูมิ', 'kalasin': 'กาฬสินธุ์', 'singburi': 'สิงห์บุรี'}
load = lambda f: json.load(open(os.path.join(RES, f), encoding='utf-8'))


def save(fig, name):
    fig.savefig(os.path.join(HERE, name), dpi=200, bbox_inches='tight', facecolor='white')
    plt.close(fig)


def scores():
    a = load('province_results.json')['part_a']
    provs = ['phuket', 'chiangmai', 'krabi', 'samui']
    fig, axs = plt.subplots(1, 3, figsize=(10, 3.6), sharey=False)
    for ax, sc, lab in zip(axs, ('S1_Short_Budget', 'S2_Medium_Standard', 'S3_Long_Premium'), ('S1 (3 วัน)', 'S2 (5 วัน)', 'S3 (7 วัน)')):
        for j, algo in enumerate(('Greedy', 'GA', 'Hybrid')):
            m = [a[f'{p}/{sc}'][algo]['score']['mean'] for p in provs]
            s = [a[f'{p}/{sc}'][algo]['score']['stdev'] for p in provs]
            ax.bar([i + (j - 1) * 0.26 for i in range(4)], m, 0.26, yerr=s, color=C[algo], label=algo, capsize=2, error_kw={'lw': 0.8})
        ax.set_xticks(range(4)); ax.set_xticklabels([TH[p] for p in provs], fontsize=12)
        ax.set_title(lab); ax.set_ylim(min(a[f'{p}/{sc}'][al]['score']['mean'] for p in provs for al in ('Greedy', 'GA', 'Hybrid')) * 0.9, None)
    axs[0].set_ylabel('คะแนนเฉลี่ย')
    h, l = axs[0].get_legend_handles_labels(); fig.legend(h, l, frameon=False, fontsize=13, loc='upper center', ncol=3, bbox_to_anchor=(0.5, 1.08))
    fig.tight_layout()
    save(fig, 'fig_scores.png')


def diag():
    p1 = load('diagnose.json')['part1']
    provs = ['phichit', 'chaiyaphum', 'kalasin', 'singburi']
    fig, axs = plt.subplots(1, 2, figsize=(10, 3.6))
    for ax, key, yl in ((axs[0], 'score', 'คะแนนดิบ'), (axs[1], 'km_day', 'ระยะขับ (กม./วัน)')):
        for j, algo in enumerate(('Greedy', 'GA', 'Hybrid')):
            ax.bar([i + (j - 1) * 0.26 for i in range(4)], [p1[p]['algo'][algo][key] for p in provs], 0.26, color=C[algo], label=algo)
        ax.set_xticks(range(4)); ax.set_xticklabels([TH[p] for p in provs], fontsize=12); ax.set_ylabel(yl)
    h, l = axs[0].get_legend_handles_labels(); fig.legend(h, l, frameon=False, fontsize=13, loc='upper center', ncol=3, bbox_to_anchor=(0.5, 1.08))
    fig.tight_layout()
    save(fig, 'fig_diag.png')


def tradeoff():
    D = load('sensitivity_dist.json')['results']; G = load('sensitivity_greedy.json')['results']
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    ks = sorted(D, key=float)
    for algo in ('Hybrid', 'GA'):
        ax.plot([D[k][algo]['km_day'] for k in ks], [D[k][algo]['score'] for k in ks], 'o-', color=C[algo], label=f'{algo} (DIST_WEIGHT 0-1)')
    gk = sorted(G, key=float)
    ax.plot([G[k]['Greedy']['km_day'] for k in gk], [G[k]['Greedy']['score'] for k in gk], 's--', color=C['Greedy'], label='Greedy (ค่าปรับ 0-100)')
    for k in ks:
        ax.annotate(k, (D[k]['Hybrid']['km_day'], D[k]['Hybrid']['score']), textcoords='offset points', xytext=(4, 5), fontsize=11, color=C['Hybrid'])
    ax.set_xlabel('ระยะขับเฉลี่ย (กม./วัน) (น้อยกว่าดีกว่า)'); ax.set_ylabel('คะแนนเฉลี่ย (มากกว่าดีกว่า)')
    ax.legend(frameon=False, fontsize=12, loc='lower right'); ax.grid(alpha=0.25)
    save(fig, 'fig_tradeoff.png')


if __name__ == '__main__':
    scores(); diag(); tradeoff(); print('ok')
